"""
Pipeline integrado — Descarga (si falta) + Procesamiento con Gemini.

FLUJO:
1. Carga parquet de consorcios
2. Pre-carga (una sola vez) set de PDFs locales + set de procesados
3. Para cada consorcio:
   a. Si ya está procesado (estado final) → saltar
   b. Si tiene PDF local → procesar con Gemini directamente
   c. Si NO tiene PDF:
      - Abrir Playwright + resolver CAPTCHA (una vez por sesión)
      - Navegar a urlproceso
      - Aplicar heurística para seleccionar el mejor documento
      - Descargar y renombrar como {id_contrato}.{ext}
      - Procesar con Gemini
   d. Guardar resultado en JSON (incremental)
4. Al finalizar → actualizar parquets

Uso:
    python scripts/gemini/pipeline_consorcios.py --n 50
    python scripts/gemini/pipeline_consorcios.py --n 500 --cooldown 0.5
    python scripts/gemini/pipeline_consorcios.py --n 100 --headless false
"""

import argparse
import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

import pdfplumber
import pandas as pd
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from playwright.async_api import async_playwright
from tqdm import tqdm

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
from extraer_indicadores_pliegos import extraer_texto_filtrado  # type: ignore

# ── Configuración ─────────────────────────────────────────────────────────────

RAIZ = Path(__file__).resolve().parent.parent.parent
DATA_PARQUET = RAIZ / 'data' / 'contratos_electronicos_obra.parquet'
PLIEGOS_DIR = Path('C:/Users/angel/OneDrive/Escritorio/trabajo dirigido/secop-scraper/storage/pliegos')
COMPLETO = RAIZ / 'data' / 'contratos_adiciones_obra.parquet'
DEPURADO = RAIZ / 'data' / 'contratos_depurado_modelo.parquet'
JSON_RESULTS = RAIZ / 'data' / 'indicadores_pliegos_extraidos.json'

# Gemini
MODELO_DEFAULT = 'gemini-2.5-flash-lite'
COOLDOWN_DEFAULT = 1.0
MAX_CHARS_TEXTO = 60000

# SECOP II
BASE_URL = 'https://community.secop.gov.co'
SECOP_SITE_KEY = '6LcMmakZAAAAAB157Q90hORUGtNd790TCws4vBNw'
SECOP_SITE_URL = 'https://community.secop.gov.co/'
CAPSOLVER_URL = 'https://api.capsolver.com'
MAX_CAPTCHA_RETRIES = 3
DELAY_ENTRE_DESCARGAS = 2.5

COLS_PLIEGO = [
    'pliego_liquidez_min',
    'pliego_endeudamiento_max_pct',
    'pliego_cobertura_intereses_min',
    'pliego_rentabilidad_patrimonio_min_pct',
    'pliego_rentabilidad_activo_min_pct',
    'pliego_capital_trabajo_min_pct_presupuesto',
]

MAPA_COLS = {
    'liquidez_min': 'pliego_liquidez_min',
    'endeudamiento_max_pct': 'pliego_endeudamiento_max_pct',
    'cobertura_intereses_min': 'pliego_cobertura_intereses_min',
    'rentabilidad_patrimonio_min_pct': 'pliego_rentabilidad_patrimonio_min_pct',
    'rentabilidad_activo_min_pct': 'pliego_rentabilidad_activo_min_pct',
    'capital_trabajo_min_pct_presupuesto': 'pliego_capital_trabajo_min_pct_presupuesto',
}

ESTADOS_FINALES = {
    'ok', 'texto_sin_umbrales', 'no_descargado', 'no_pdf',
    'error_pdf', 'error_api_permanente', 'sin_match',
}

ERRORES_API_TRANSITORIOS = (
    'ServiceUnavailable', 'InternalServerError', 'DeadlineExceeded',
    'ResourceExhausted', 'Unavailable', 'Aborted', '503', '500', '504', '429',
)

PROMPT_INSTRUCCIONES = """Eres un analista que extrae indicadores habilitantes de un pliego de condiciones de SECOP II (Colombia).

CONTEXTO
El pliego establece umbrales mínimos/máximos para que un oferente sea "habilitado". Los valores aparecen de formas variadas:
- En tablas: "Índice de Liquidez   Mayor o igual a: 1.5"
- Narrativo: "Razón Corriente igual o superior a 2.5 Habilita"
- Con simbolos: "IL ≥ 1.5", "NDE ≤ 70%"

TAREA
Extrae los siguientes indicadores del texto. Si un indicador NO aparece o no tiene un umbral numérico claro, devuelve null.

INDICADORES A EXTRAER:
1. liquidez_min: umbral MÍNIMO de liquidez / índice de liquidez / razón corriente (número sin %, ej: 1.5, 2.5)
2. endeudamiento_max_pct: umbral MÁXIMO de endeudamiento / nivel de endeudamiento (número en %; si dice 0.5 convertir a 50.0)
3. cobertura_intereses_min: umbral MÍNIMO de cobertura de intereses / razón de cobertura (número, ej: 2, 4)
4. rentabilidad_patrimonio_min_pct: umbral MÍNIMO de rentabilidad del patrimonio / ROE (número en %)
5. rentabilidad_activo_min_pct: umbral MÍNIMO de rentabilidad del activo / ROA (número en %)
6. capital_trabajo_min_pct_presupuesto: umbral MÍNIMO de capital de trabajo como % del presupuesto oficial (solo si se expresa como %, ej: 70). Si es monto absoluto ($35M), devolver null.

REGLAS IMPORTANTES:
- Responde SOLO con JSON válido conforme al schema.
- Devuelve números (no strings), null si no hay valor.
- No inventes valores. Si está ambiguo o no está → null.

TEXTO DEL PLIEGO:
---
"""

SCHEMA_INDICADORES = {
    "type": "OBJECT",
    "properties": {
        "liquidez_min": {"type": "NUMBER", "nullable": True},
        "endeudamiento_max_pct": {"type": "NUMBER", "nullable": True},
        "cobertura_intereses_min": {"type": "NUMBER", "nullable": True},
        "rentabilidad_patrimonio_min_pct": {"type": "NUMBER", "nullable": True},
        "rentabilidad_activo_min_pct": {"type": "NUMBER", "nullable": True},
        "capital_trabajo_min_pct_presupuesto": {"type": "NUMBER", "nullable": True},
    },
    "required": [
        "liquidez_min", "endeudamiento_max_pct", "cobertura_intereses_min",
        "rentabilidad_patrimonio_min_pct", "rentabilidad_activo_min_pct",
        "capital_trabajo_min_pct_presupuesto",
    ],
}


def log(msg: str = ''):
    tqdm.write(msg)


def sep():
    log('─' * 70)


# ── CAPTCHA (CapSolver) ───────────────────────────────────────────────────────

def _resolver_captcha_una_vez(api_key: str) -> str:
    payload = {
        'clientKey': api_key,
        'task': {
            'type': 'ReCaptchaV2TaskProxyLess',
            'websiteURL': SECOP_SITE_URL,
            'websiteKey': SECOP_SITE_KEY,
        },
    }
    try:
        resp = requests.post(f'{CAPSOLVER_URL}/createTask', json=payload, timeout=30)
        data = resp.json()
        if data.get('errorId'):
            return ''
        task_id = data.get('taskId')
        if not task_id:
            return ''
        for _ in range(120):
            time.sleep(1)
            poll = requests.post(
                f'{CAPSOLVER_URL}/getTaskResult',
                json={'clientKey': api_key, 'taskId': task_id},
                timeout=30,
            ).json()
            status = poll.get('status')
            if status == 'ready':
                return poll.get('solution', {}).get('gRecaptchaResponse', '')
            if status == 'failed' or poll.get('errorId'):
                return ''
    except Exception:
        pass
    return ''


def resolver_captcha(api_key: str) -> str:
    for intento in range(1, MAX_CAPTCHA_RETRIES + 1):
        token = _resolver_captcha_una_vez(api_key)
        if token:
            return token
    return ''


async def resolver_captcha_secop(page, api_key: str) -> bool:
    current_url = page.url
    is_captcha = 'GoogleReCaptcha' in current_url
    if not is_captcha:
        has_captcha = await page.query_selector('#divGoogleReCaptcha')
        if not has_captcha:
            return True

    log('    🔐 reCAPTCHA detectado — resolviendo con CapSolver...')
    mkey = await page.evaluate("""() => {
        const btn = document.getElementById('btnCaptchaCheckButton');
        if (!btn) return null;
        const onclick = btn.getAttribute('onclick') || '';
        const m = onclick.match(/mkey=([a-f0-9_]+)/);
        return m ? m[1] : null;
    }""")

    if not mkey:
        return False

    token = resolver_captcha(api_key)
    if not token:
        return False

    check_url = f'{BASE_URL}/Public/Common/GoogleReCaptcha/CaptchaCheck?responseKey={token}&mkey={mkey}'
    await page.goto(check_url, wait_until='domcontentloaded', timeout=60000)
    await asyncio.sleep(2)
    return 'GoogleReCaptcha' not in page.url


# ── Selección por CONTENIDO del documento ─────────────────────────────────────

# Keywords para evaluar si un PDF es el pliego con indicadores habilitantes
KEYWORDS_CAPACIDAD_FINANCIERA = [
    'liquidez', 'endeudamiento', 'cobertura de intereses', 'razon de cobertura',
    'rentabilidad del patrimonio', 'rentabilidad del activo',
    'capital de trabajo', 'capacidad financiera', 'indicadores financieros',
    'indice de liquidez', 'razon corriente', 'habilita', 'habilitante',
    'habilitacion', 'patrimonio minimo', 'nivel de endeudamiento',
]

# Excluir por nombre SOLO docs que nunca contienen indicadores (ahorra descarga)
EXTENSIONES_IGNORAR = ['.xlsx', '.xls', '.xlsm', '.zip', '.rar', '.png', '.jpg']
NOMBRES_IGNORAR = [
    'matriz de riesgos', 'formato', 'formulario', 'acta de',
    'presupuesto oficial', 'apu ', 'analisis de precios',
    'cronograma', 'plano', 'garantia', 'observacion',
]


def filtrar_candidatos_a_descargar(doc_info: list) -> list:
    """
    Filtra lista de documentos para quedarse solo con los que VALE LA PENA
    descargar (podrían ser el pliego). Usa filtros ligeros por nombre/extensión.
    """
    candidatos = []
    for d in doc_info:
        nombre_lower = d['name'].lower()

        # Ignorar por extensión (no podemos extraer texto fácil)
        if any(nombre_lower.endswith(ext) for ext in EXTENSIONES_IGNORAR):
            continue

        # Ignorar docs que NUNCA contienen indicadores
        if any(patron in nombre_lower for patron in NOMBRES_IGNORAR):
            continue

        candidatos.append(d)

    return candidatos


def evaluar_pdf_score(pdf_path: Path) -> dict:
    """
    Evalúa un PDF y retorna un score basado en el contenido.
    Score = clusters_encontrados * 100 + hits_keywords + longitud_filtrada/1000
    """
    try:
        extr = extraer_texto_filtrado(pdf_path)
        if extr.get('error'):
            return {'score': -1, 'error': extr['error']}

        texto = extr.get('texto', '')
        clusters = len(extr.get('clusters_encontrados', []))
        hits = extr.get('hits_sin_toc', 0) or extr.get('hits_original', 0)
        longitud = len(texto)

        # Contar keywords específicas en el texto filtrado (más preciso)
        texto_lower = texto.lower()
        hits_kw = sum(1 for kw in KEYWORDS_CAPACIDAD_FINANCIERA if kw in texto_lower)

        # Score: prioriza docs con clusters y keywords financieras
        score = (clusters * 100) + (hits_kw * 10) + (hits) + (longitud // 1000)

        return {
            'score': score,
            'clusters': clusters,
            'hits': hits,
            'hits_kw': hits_kw,
            'longitud': longitud,
            'total_paginas': extr.get('total_paginas', 0),
        }
    except Exception as e:
        return {'score': -1, 'error': str(e)[:100]}


# ── Descarga desde SECOP II ───────────────────────────────────────────────────

async def descargar_y_evaluar(page, url: str, id_contrato: str,
                                capsolver_key: str) -> Path:
    """
    Descarga TODOS los PDFs candidatos del contrato, los evalúa por contenido,
    se queda con el de mejor score (renombrado a {id_contrato}.pdf) y borra
    el resto.
    """
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        await asyncio.sleep(2)

        # Re-resolver CAPTCHA si cayó sesión
        if 'GoogleReCaptcha' in page.url or await page.query_selector('#divGoogleReCaptcha'):
            ok = await resolver_captcha_secop(page, capsolver_key)
            if not ok:
                log('    ❌ CAPTCHA no resuelto')
                return None
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)
            await asyncio.sleep(3)

        # Esperar tabla de documentos
        try:
            await page.wait_for_selector('#grdGridDocumentList_tbl', timeout=30000)
        except Exception:
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(3)
            try:
                await page.wait_for_selector('#grdGridDocumentList_tbl', timeout=15000)
            except Exception:
                log('    ❌ Tabla de documentos no cargó')
                return None

        # Obtener lista de documentos
        doc_info = await page.evaluate("""() => {
            const rows = document.querySelectorAll(
                '#grdGridDocumentList_tbl tbody tr:not(#grdGridDocumentList_header)'
            );
            const docs = [];
            for (const row of rows) {
                const span = row.querySelector('span.VortalSpan');
                const link = row.querySelector('a[onclick*="DownloadFile"]');
                if (span && link) {
                    docs.push({ name: span.textContent.trim(), linkId: link.id });
                }
            }
            return docs;
        }""")

        if not doc_info:
            log('    ❌ No se encontraron documentos')
            return None

        # Filtro rápido: solo candidatos plausibles (PDFs, sin matrices/formatos)
        candidatos = filtrar_candidatos_a_descargar(doc_info)
        if not candidatos:
            log(f'    ❌ Sin PDFs candidatos ({len(doc_info)} docs totales)')
            return None

        log(f'    📥 {len(candidatos)} PDFs candidatos a descargar y evaluar')

        # Carpeta temporal para este contrato
        temp_dir = PLIEGOS_DIR / f'_tmp_{id_contrato}'
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Descargar cada candidato
        descargas = []  # [(nombre, path), ...]
        for i, doc in enumerate(candidatos, start=1):
            nombre = doc['name']
            link_el = page.locator(f'#{doc["linkId"]}')
            try:
                async with page.expect_download(timeout=60000) as download_info:
                    await link_el.click()
                download = await download_info.value
                suggested = download.suggested_filename or f'doc_{i}.pdf'
                ext = Path(suggested).suffix.lower() or '.pdf'
                if ext != '.pdf':
                    log(f'      [{i}] {nombre[:50]} → ext {ext}, ignorado')
                    continue
                dest = temp_dir / f'doc_{i}{ext}'
                await download.save_as(str(dest))
                size_kb = dest.stat().st_size / 1024
                log(f'      [{i}] {nombre[:50]} ({size_kb:.1f} KB)')
                descargas.append((nombre, dest))
                await asyncio.sleep(0.5)
            except Exception as dl_err:
                log(f'      [{i}] ❌ {nombre[:50]}: {str(dl_err)[:50]}')

        if not descargas:
            # Limpiar carpeta temp
            for f in temp_dir.glob('*'):
                f.unlink(missing_ok=True)
            temp_dir.rmdir()
            log('    ❌ No se descargó ningún PDF')
            return None

        # Evaluar cada PDF descargado
        log(f'    🔎 Evaluando {len(descargas)} PDFs por contenido...')
        scores = []
        for nombre, path in descargas:
            ev = evaluar_pdf_score(path)
            scores.append((nombre, path, ev))
            log(f'      {nombre[:45]:<45} score={ev["score"]:>5}  '
                f'clusters={ev.get("clusters",0)} kw={ev.get("hits_kw",0)}')

        # Elegir el mejor (mayor score)
        scores.sort(key=lambda x: x[2]['score'], reverse=True)
        mejor_nombre, mejor_path, mejor_ev = scores[0]

        if mejor_ev['score'] < 0:
            # Ninguno sirvió
            for _, p, _ in scores:
                p.unlink(missing_ok=True)
            temp_dir.rmdir()
            log('    ❌ Ningún PDF procesable')
            return None

        log(f'    🏆 Ganador: {mejor_nombre[:60]} (score={mejor_ev["score"]})')

        # Mover el ganador a PLIEGOS_DIR/{id_contrato}.pdf
        destino_final = PLIEGOS_DIR / f'{id_contrato}.pdf'
        mejor_path.rename(destino_final)

        # Borrar los demás + carpeta temp
        for _, p, _ in scores[1:]:
            p.unlink(missing_ok=True)
        try:
            temp_dir.rmdir()
        except Exception:
            pass

        size_kb = destino_final.stat().st_size / 1024
        log(f'    ✅ {size_kb:.1f} KB → {destino_final.name}')
        return destino_final

    except Exception as e:
        log(f'    ❌ Error: {str(e)[:100]}')
        return None


# ── Procesamiento de texto + Gemini ───────────────────────────────────────────

RE_LINEAS_TOC = re.compile(r'^\s*.{3,}?\.{3,}\s*\d+\s*$', re.MULTILINE)
RE_WS_MULTI = re.compile(r'[ \t]+')
RE_LINEAS_VACIAS = re.compile(r'\n{3,}')
RE_NUMS_PAG = re.compile(r'^\s*(página\s+)?\d+\s*(de\s+\d+)?\s*$', re.IGNORECASE | re.MULTILINE)


def compactar_texto(texto: str) -> str:
    if not texto:
        return ''
    texto = RE_LINEAS_TOC.sub('', texto)
    texto = RE_NUMS_PAG.sub('', texto)
    lineas = texto.split('\n')
    conteo = {}
    for l in lineas:
        l_strip = l.strip()
        if 3 <= len(l_strip) <= 100:
            conteo[l_strip] = conteo.get(l_strip, 0) + 1
    repetidas = {l for l, c in conteo.items() if c >= 4}
    if repetidas:
        lineas = [l for l in lineas if l.strip() not in repetidas]
        texto = '\n'.join(lineas)
    texto = RE_WS_MULTI.sub(' ', texto)
    texto = RE_LINEAS_VACIAS.sub('\n\n', texto)
    return texto.strip()


def extraer_texto_completo_pdf(pdf_path: Path) -> str:
    try:
        partes = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                txt = page.extract_text() or ''
                if txt.strip():
                    partes.append(txt)
        return '\n'.join(partes)
    except Exception:
        return ''


def extraer_con_gemini(client: genai.Client, modelo: str, texto: str) -> dict:
    prompt = PROMPT_INSTRUCCIONES + texto[:MAX_CHARS_TEXTO] + '\n---'
    response = client.models.generate_content(
        model=modelo,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=SCHEMA_INDICADORES,
            temperature=0.0,
        ),
    )
    text = response.text or '{}'
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {'_parse_error': text[:500]}


def clasificar_error_api(exc: Exception) -> str:
    nombre = type(exc).__name__
    mensaje = str(exc)
    for keyword in ERRORES_API_TRANSITORIOS:
        if keyword in nombre or keyword in mensaje:
            return 'error_api'
    return 'error_api_permanente'


def procesar_pdf(client: genai.Client, modelo: str,
                  id_contrato: str, pdf_path: Path) -> dict:
    extr = extraer_texto_filtrado(pdf_path)

    if extr.get('error'):
        return {
            'id_contrato': id_contrato,
            'archivo': pdf_path.name,
            'estado': 'error_pdf',
            'error': extr['error'],
            'metodo': 'gemini',
        }

    texto = extr.get('texto', '')
    metodo_texto = 'filtrado'

    if not texto:
        texto_raw = extraer_texto_completo_pdf(pdf_path)
        texto = compactar_texto(texto_raw)
        metodo_texto = 'completo_compactado'
        if not texto:
            return {
                'id_contrato': id_contrato,
                'archivo': pdf_path.name,
                'estado': 'sin_match',
                'total_paginas': extr.get('total_paginas', 0),
                'metodo': 'gemini',
            }

    try:
        indicadores = extraer_con_gemini(client, modelo, texto)
    except Exception as e:
        return {
            'id_contrato': id_contrato,
            'archivo': pdf_path.name,
            'estado': clasificar_error_api(e),
            'error': f'{type(e).__name__}: {str(e)[:200]}',
            'metodo': 'gemini',
        }

    if '_parse_error' in indicadores:
        return {
            'id_contrato': id_contrato,
            'archivo': pdf_path.name,
            'estado': 'error_parse',
            'error': indicadores['_parse_error'],
            'metodo': 'gemini',
        }

    n_extraidos = sum(1 for v in indicadores.values() if v is not None)

    return {
        'id_contrato': id_contrato,
        'archivo': pdf_path.name,
        'estado': 'ok' if n_extraidos > 0 else 'texto_sin_umbrales',
        'total_paginas': extr.get('total_paginas', 0),
        'paginas_finales': extr.get('paginas_finales', []),
        'longitud_filtrada': len(texto),
        'metodo_texto': metodo_texto,
        'indicadores_extraidos': n_extraidos,
        'metodo': 'gemini',
        **indicadores,
    }


# ── JSON / Parquets ───────────────────────────────────────────────────────────

def cargar_resultados_existentes() -> dict:
    if not JSON_RESULTS.exists():
        return {}
    with JSON_RESULTS.open(encoding='utf-8') as f:
        data = json.load(f)
    return {r['id_contrato']: r for r in data if 'id_contrato' in r}


def guardar_resultados(dict_resultados: dict):
    data = sorted(dict_resultados.values(), key=lambda r: r.get('id_contrato', ''))
    JSON_RESULTS.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, default=str),
        encoding='utf-8'
    )


def poblar_datasets(dict_resultados: dict):
    filas = []
    for r in dict_resultados.values():
        if r.get('estado') != 'ok':
            continue
        fila = {'id_contrato': r['id_contrato']}
        for k_orig, k_nuevo in MAPA_COLS.items():
            fila[k_nuevo] = r.get(k_orig)
        filas.append(fila)

    if not filas:
        log('  Sin contratos ok — parquets sin cambios.')
        return

    df_pliegos = pd.DataFrame(filas)
    n_ok = len(df_pliegos)

    df_full = pd.read_parquet(COMPLETO)
    cols_previas = [c for c in COLS_PLIEGO if c in df_full.columns]
    if cols_previas:
        df_full = df_full.drop(columns=cols_previas)
    df_full = df_full.merge(df_pliegos, on='id_contrato', how='left')
    df_full.to_parquet(COMPLETO, index=False)

    df_dep = pd.read_parquet(DEPURADO)
    for col in COLS_PLIEGO:
        df_dep[col] = df_full[col].values
    df_dep.to_parquet(DEPURADO, index=False)

    log(f'  ✅ {n_ok:,} contratos con indicadores')
    for col in COLS_PLIEGO:
        n_val = df_dep[col].notna().sum()
        log(f'    {col:<50}: {n_val:>5,} ({n_val/len(df_dep)*100:.1f}%)')


# ── Pipeline principal ────────────────────────────────────────────────────────

async def pipeline(args):
    load_dotenv(RAIZ / '.env')
    gemini_key = os.getenv('GEMINI_API_KEY')
    capsolver_key = os.getenv('CAPSOLVER_API_KEY')

    if not gemini_key:
        log('❌ ERROR: Falta GEMINI_API_KEY en .env')
        return
    if not capsolver_key:
        log('❌ ERROR: Falta CAPSOLVER_API_KEY en .env')
        return

    client = genai.Client(api_key=gemini_key)
    PLIEGOS_DIR.mkdir(parents=True, exist_ok=True)

    # ── Paso 1: Cargar datos (rápido, una sola vez) ─────────────────────────
    log('📂 Cargando datos...')

    # PDFs locales: set O(1) lookup
    pdfs_locales = {p.stem for p in PLIEGOS_DIR.iterdir()
                    if p.is_file() and p.suffix.lower() == '.pdf'}
    log(f'  PDFs locales: {len(pdfs_locales):,}')

    # Consorcios
    df = pd.read_parquet(DATA_PARQUET)
    consorcios = df[df['es_grupo'] == 'Si']
    log(f'  Consorcios totales: {len(consorcios):,}')

    # Resultados previos
    resultados = cargar_resultados_existentes()
    procesados_finales = {k for k, v in resultados.items()
                          if v.get('estado') in ESTADOS_FINALES}
    log(f'  Ya procesados (finales): {len(procesados_finales):,}')

    # ── Paso 2: Construir lista de pendientes (filtro rápido en memoria) ────
    pendientes = []
    for _, row in consorcios.iterrows():
        id_c = row['id_contrato']
        if id_c in procesados_finales:
            continue
        pendientes.append({
            'id_contrato': id_c,
            'urlproceso': row.get('urlproceso', ''),
            'proveedor': str(row.get('proveedor_adjudicado', ''))[:60],
            'entidad': str(row.get('nombre_entidad', ''))[:60],
            'tiene_pdf_local': id_c in pdfs_locales,
        })
        if len(pendientes) >= args.n:
            break

    total = len(pendientes)
    con_pdf = sum(1 for p in pendientes if p['tiene_pdf_local'])
    sin_pdf = total - con_pdf

    sep()
    log(f'  Modelo            : {args.modelo}')
    log(f'  Cooldown          : {args.cooldown}s')
    log(f'  A procesar        : {total}')
    log(f'  ├─ Con PDF local  : {con_pdf}')
    log(f'  └─ Sin PDF (descargar): {sin_pdf}')
    sep()

    if total == 0:
        log('✅ Nada por hacer.')
        return

    # ── Paso 3: Abrir Playwright (solo si hay PDFs a descargar) ─────────────
    browser = None
    context = None
    page = None
    sesion_secop_ok = False

    async def abrir_navegador():
        nonlocal browser, context, page, sesion_secop_ok
        if browser is not None:
            return
        log('🌐 Iniciando navegador SECOP II...')
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=args.headless)
        context = await browser.new_context(
            user_agent=(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
        )
        page = await context.new_page()

        # Primera navegación + CAPTCHA inicial
        primera_url = next(
            (p['urlproceso'] for p in pendientes if not p['tiene_pdf_local'] and p['urlproceso']),
            None
        )
        if primera_url:
            await page.goto(primera_url, wait_until='domcontentloaded', timeout=60000)
            await asyncio.sleep(2)
            sesion_secop_ok = await resolver_captcha_secop(page, capsolver_key)
            if sesion_secop_ok:
                log('  ✅ Sesión SECOP II activa')
            else:
                log('  ⚠️  No se pudo iniciar sesión — abortando descargas')

    # ── Paso 4: Iterar pendientes ───────────────────────────────────────────
    ok_count = 0
    err_count = 0
    descargados = 0

    with tqdm(total=total, desc='Pipeline', unit='consorcio', ncols=80) as pbar:
        for idx, p in enumerate(pendientes, start=1):
            id_c = p['id_contrato']

            log(f'\n[{idx}/{total}]  {id_c}')
            log(f'  Entidad: {p["entidad"]}')

            # Paso A: obtener PDF
            pdf_path = None
            if p['tiene_pdf_local']:
                # Buscar el archivo (solo un glob rápido, ya sabemos que existe)
                archivos = list(PLIEGOS_DIR.glob(f'{id_c}.*'))
                pdf_path = next(
                    (a for a in archivos if a.suffix.lower() == '.pdf'),
                    None
                )
                if pdf_path:
                    log(f'  📁 PDF local: {pdf_path.name}')
            else:
                # Abrir navegador si no está abierto
                if browser is None:
                    await abrir_navegador()

                if not sesion_secop_ok:
                    log('  ❌ Sin sesión SECOP — saltando')
                    resultados[id_c] = {
                        'id_contrato': id_c,
                        'estado': 'no_descargado',
                        'error': 'sesion_captcha',
                        'metodo': 'gemini',
                    }
                    guardar_resultados(resultados)
                    err_count += 1
                    pbar.update(1)
                    continue

                if not p['urlproceso']:
                    log('  ❌ Sin urlproceso')
                    resultados[id_c] = {
                        'id_contrato': id_c,
                        'estado': 'no_descargado',
                        'error': 'sin_urlproceso',
                        'metodo': 'gemini',
                    }
                    guardar_resultados(resultados)
                    err_count += 1
                    pbar.update(1)
                    continue

                # Descargar y evaluar
                pdf_path = await descargar_y_evaluar(
                    page, p['urlproceso'], id_c, capsolver_key
                )
                if pdf_path:
                    descargados += 1
                    await asyncio.sleep(DELAY_ENTRE_DESCARGAS)

            if not pdf_path or not pdf_path.exists() or pdf_path.suffix.lower() != '.pdf':
                resultados[id_c] = {
                    'id_contrato': id_c,
                    'estado': 'no_descargado' if not pdf_path else 'no_pdf',
                    'metodo': 'gemini',
                }
                guardar_resultados(resultados)
                err_count += 1
                pbar.update(1)
                continue

            # Paso B: procesar con Gemini
            log(f'  📄 Procesando con {args.modelo}...')
            resultado = procesar_pdf(client, args.modelo, id_c, pdf_path)
            resultados[id_c] = resultado

            if resultado['estado'] == 'ok':
                n_ind = resultado.get('indicadores_extraidos', 0)
                log(f'  ✅ {n_ind} indicadores extraídos')
                ok_count += 1
            else:
                log(f'  ⚠️  {resultado["estado"]}')
                err_count += 1

            guardar_resultados(resultados)
            pbar.update(1)

            # Cooldown Gemini
            time.sleep(args.cooldown)

    # ── Cleanup ─────────────────────────────────────────────────────────────
    if browser is not None:
        await browser.close()

    # ── Actualizar parquets ─────────────────────────────────────────────────
    log('\n📊 Actualizando parquets...')
    poblar_datasets(resultados)

    sep()
    log(f'✅ OK: {ok_count}  |  ⚠️  Errores: {err_count}  |  📥 Descargados: {descargados}')
    sep()


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=50)
    ap.add_argument('--cooldown', type=float, default=COOLDOWN_DEFAULT)
    ap.add_argument('--modelo', type=str, default=MODELO_DEFAULT)
    ap.add_argument('--headless', type=lambda x: x.lower() != 'false', default=True)
    args = ap.parse_args()

    asyncio.run(pipeline(args))


if __name__ == '__main__':
    main()
