"""
Pipeline integrado — Descarga + Procesamiento de indicadores.

Para cada consorcio sin procesar:
1. Verificar si tiene PDF descargado
2. Si NO → obtener documento de SECOP II + descargar (heurística)
3. Procesar PDF con Gemini
4. Guardar resultado

Uso:
    python scripts/gemini/procesar_consorcios_completo.py --n 100
    python scripts/gemini/procesar_consorcios_completo.py --n 500 --cooldown 0.5
"""

import argparse
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
from tqdm import tqdm

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
from extraer_indicadores_pliegos import extraer_texto_filtrado  # type: ignore

RAIZ = Path(__file__).resolve().parent.parent.parent
DATA_PARQUET = RAIZ / 'data' / 'contratos_electronicos_obra.parquet'
PLIEGOS_DIR = Path('C:/Users/angel/OneDrive/Escritorio/trabajo dirigido/secop-scraper/storage/pliegos')
COMPLETO = RAIZ / 'data' / 'contratos_adiciones_obra.parquet'
DEPURADO = RAIZ / 'data' / 'contratos_depurado_modelo.parquet'
JSON_RESULTS = RAIZ / 'data' / 'indicadores_pliegos_extraidos.json'

MODELO_DEFAULT = 'gemini-2.5-flash-lite'
COOLDOWN_DEFAULT = 1.0
MAX_CHARS_TEXTO = 60000

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

ESTADOS_FINALES = {
    'ok', 'texto_sin_umbrales', 'no_descargado', 'no_pdf',
    'error_pdf', 'error_api_permanente', 'sin_match',
}

ERRORES_API_TRANSITORIOS = (
    'ServiceUnavailable', 'InternalServerError', 'DeadlineExceeded',
    'ResourceExhausted', 'Unavailable', 'Aborted', '503', '500', '504', '429',
)

# Heurística: patrones de nombre de documento en orden de preferencia
HEURISTICA_NOMBRES = [
    r'pliego de condiciones definitivo',
    r'invitacion publica',
    r'pliego',
    r'condiciones definitivas',
    r'bases definitivas',
    r'terminos de referencia',
    r'proyecto de pliego',
]

SECOP_API = 'https://community.secop.gov.co/api/3/action/datastore_search_sql'
SECOP_DATASET = 'c29ef1f0-bcf2-4e4e-8988-0e9d5fe54bb7'
APP_TOKEN = 'nrnMDVHrooMY3wZIGrYfPsAq3'


def log(msg: str = ''):
    tqdm.write(msg)


def sep():
    log('─' * 70)


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


def obtener_documentos_secop(id_proceso: str) -> list:
    """Obtiene documentos disponibles de SECOP II para un proceso."""
    if not id_proceso:
        return []
    try:
        query = f"""
        SELECT
            "Nombre del Documento" as nombre,
            "Enlace del Documento" as url
        FROM "{SECOP_DATASET}"
        WHERE "Proceso de Contratacion" = '{id_proceso}'
        AND "Enlace del Documento" IS NOT NULL
        LIMIT 100
        """
        resp = requests.get(
            SECOP_API,
            params={'sql': query, 'resource_id': SECOP_DATASET},
            headers={'X-CKAN-API-Token': APP_TOKEN},
            timeout=15,
        )
        if resp.status_code != 200:
            return []
        data = resp.json()
        if not data.get('success'):
            return []
        records = data.get('result', {}).get('records', [])
        return [
            {'nombre': r.get('nombre', '').strip(), 'url': r.get('url', '').strip()}
            for r in records if r.get('url')
        ]
    except Exception:
        return []


def seleccionar_mejor_documento(documentos: list) -> dict:
    """Selecciona el mejor documento usando heurística."""
    if not documentos:
        return None
    nombres_lower = {d['nombre'].lower(): d for d in documentos}
    for patron in HEURISTICA_NOMBRES:
        for nombre, doc in nombres_lower.items():
            if patron in nombre:
                return doc
    return documentos[0]


def descargar_archivo(url: str, ruta_local: Path) -> bool:
    """Descarga un archivo desde URL."""
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            ruta_local.write_bytes(resp.content)
            return True
    except Exception:
        pass
    return False


def obtener_pdf(id_contrato: str, id_proceso: str) -> Path:
    """
    Obtiene PDF para un contrato.
    Si ya existe → lo retorna
    Si NO existe → busca en SECOP II, descarga y lo retorna
    Si no se puede → retorna None
    """
    # ¿Ya existe?
    archivos = list(PLIEGOS_DIR.glob(f'{id_contrato}.*'))
    for arch in archivos:
        if arch.suffix.lower() == '.pdf':
            return arch

    # Buscar en SECOP II
    log(f'    📥 Buscando documento en SECOP II...')
    documentos = obtener_documentos_secop(id_proceso)
    if not documentos:
        return None

    doc = seleccionar_mejor_documento(documentos)
    if not doc or not doc.get('url'):
        return None

    # Descargar
    url = doc['url']
    ext = Path(url).suffix.lower() or '.pdf'
    ruta = PLIEGOS_DIR / f'{id_contrato}{ext}'

    log(f'    📌 Descargando: {doc["nombre"][:50]}...')
    if not descargar_archivo(url, ruta):
        return None

    return ruta if ruta.exists() else None


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


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=10,
                    help='Máximo de consorcios a procesar')
    ap.add_argument('--cooldown', type=float, default=COOLDOWN_DEFAULT,
                    help=f'Segundos entre llamadas (default {COOLDOWN_DEFAULT}s)')
    ap.add_argument('--modelo', type=str, default=MODELO_DEFAULT,
                    help=f'Modelo de Gemini (default {MODELO_DEFAULT})')
    args = ap.parse_args()

    load_dotenv(RAIZ / '.env')
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print('ERROR: Falta GEMINI_API_KEY en .env', file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)
    PLIEGOS_DIR.mkdir(parents=True, exist_ok=True)

    # Cargar parquet
    df = pd.read_parquet(DATA_PARQUET)
    consorcios = df[df['es_grupo'] == 'Si'].copy()
    resultados = cargar_resultados_existentes()

    # Filtrar: solo los que aún no tienen estado final
    pendientes = []
    for _, row in consorcios.iterrows():
        id_c = row['id_contrato']
        prev = resultados.get(id_c)
        if prev is not None and prev.get('estado', '') in ESTADOS_FINALES:
            continue
        pendientes.append(row)

    pendientes_df = pd.DataFrame(pendientes).head(args.n)
    total = len(pendientes_df)

    sep()
    log(f'  Modelo          : {args.modelo}')
    log(f'  Cooldown        : {args.cooldown}s entre llamadas')
    log(f'  Ya procesados   : {len(resultados)}')
    log(f'  A procesar hoy  : {total}')
    sep()

    if total == 0:
        log('✅ Nada por hacer.')
        return

    ok_count = 0
    err_count = 0

    with tqdm(total=total, desc='Procesando', unit='consorcio', ncols=80) as pbar:
        for idx, (_, row) in enumerate(pendientes_df.iterrows(), start=1):
            id_c = row['id_contrato']
            id_proc = row.get('id_del_portafolio')
            proveedor = row.get('proveedor_adjudicado', '')[:60]
            entidad = row.get('nombre_entidad', '')[:60]

            log(f'\n[{idx}/{total}]  {id_c}')
            log(f'  Proveedor : {proveedor}')
            log(f'  Entidad   : {entidad}')

            # Obtener PDF
            pdf_path = obtener_pdf(id_c, id_proc)
            if not pdf_path or not pdf_path.exists():
                log(f'  ❌ No se pudo obtener PDF')
                resultados[id_c] = {
                    'id_contrato': id_c,
                    'estado': 'no_descargado',
                    'metodo': 'gemini',
                }
                guardar_resultados(resultados)
                err_count += 1
                pbar.update(1)
                continue

            # Procesar con Gemini
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
            time.sleep(args.cooldown)

    # Actualizar parquets
    log('\n📊 Actualizando parquets...')
    poblar_datasets(resultados)

    log('\n' + '─' * 70)
    log(f'✅ Exitosos: {ok_count}  |  ⚠️  Errores: {err_count}')
    log('─' * 70)


if __name__ == '__main__':
    main()
