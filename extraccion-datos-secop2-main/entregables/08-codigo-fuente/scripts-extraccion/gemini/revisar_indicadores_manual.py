"""
Revisión manual de indicadores — iteración semi-automática.

Itera consorcios con indicadores nulos, abre cada urlproceso en el navegador,
lista documentos disponibles via Playwright, usuario elige cuál descargar,
extrae contenido completo y envía a Gemini.

Uso:
    python scripts/gemini/revisar_indicadores_manual.py
    python scripts/gemini/revisar_indicadores_manual.py --desde 50
"""

import argparse
import asyncio
import json
import os
import sys
import time
import webbrowser
from pathlib import Path

import pdfplumber
import docx as python_docx
from odf import text as odf_text
from odf.opendocument import load as odf_load
from odf.element import Element
import pandas as pd
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from playwright.async_api import async_playwright

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
RAIZ = Path(__file__).resolve().parent.parent.parent
DATA_PARQUET = RAIZ / 'data' / 'contratos_electronicos_obra.parquet'
PLIEGOS_DIR = Path('C:/Users/angel/OneDrive/Escritorio/trabajo dirigido/secop-scraper/storage/pliegos')
JSON_RESULTS = RAIZ / 'data' / 'indicadores_pliegos_extraidos.json'

BASE_URL = 'https://community.secop.gov.co'
SECOP_SITE_KEY = '6LcMmakZAAAAAB157Q90hORUGtNd790TCws4vBNw'
SECOP_SITE_URL = 'https://community.secop.gov.co/'
CAPSOLVER_URL = 'https://api.capsolver.com'
MODELO_DEFAULT = 'gemini-2.5-flash-lite'
MAX_CHARS = 120000

COLS_INDICADORES = [
    'pliego_liquidez_min', 'pliego_endeudamiento_max_pct',
    'pliego_cobertura_intereses_min', 'pliego_rentabilidad_patrimonio_min_pct',
    'pliego_rentabilidad_activo_min_pct', 'pliego_capital_trabajo_min_pct_presupuesto',
]

COLS_PLIEGO_RAW = [
    'liquidez_min', 'endeudamiento_max_pct', 'cobertura_intereses_min',
    'rentabilidad_patrimonio_min_pct', 'rentabilidad_activo_min_pct',
    'capital_trabajo_min_pct_presupuesto',
]

PROMPT = """Eres un analista que extrae indicadores habilitantes de un pliego de condiciones de SECOP II (Colombia).

CONTEXTO
El pliego establece umbrales mínimos/máximos para que un oferente sea "habilitado". Los valores aparecen de formas variadas:
- En tablas: "Índice de Liquidez   Mayor o igual a: 1.5"
- Narrativo: "Razón Corriente igual o superior a 2.5 Habilita"
- Con simbolos: "IL ≥ 1.5", "NDE ≤ 70%"

TAREA
Extrae los siguientes indicadores. Si NO aparece o no tiene umbral numérico claro, devuelve null.

1. liquidez_min: umbral MÍNIMO de liquidez / índice de liquidez / razón corriente (número, ej: 1.5)
2. endeudamiento_max_pct: umbral MÁXIMO de endeudamiento en % (si dice 0.5 → 50.0)
3. cobertura_intereses_min: umbral MÍNIMO de cobertura de intereses (número, ej: 2)
4. rentabilidad_patrimonio_min_pct: umbral MÍNIMO ROE en %
5. rentabilidad_activo_min_pct: umbral MÍNIMO ROA en %
6. capital_trabajo_min_pct_presupuesto: umbral MÍNIMO capital de trabajo como % presupuesto (solo si es %, no monto absoluto)

REGLAS: Solo JSON válido, números no strings, null si ambiguo.

TEXTO DEL PLIEGO:
---
"""

SCHEMA = {
    "type": "OBJECT",
    "properties": {k: {"type": "NUMBER", "nullable": True} for k in COLS_PLIEGO_RAW},
    "required": COLS_PLIEGO_RAW,
}

MAPA_COLS = {
    'liquidez_min': 'pliego_liquidez_min',
    'endeudamiento_max_pct': 'pliego_endeudamiento_max_pct',
    'cobertura_intereses_min': 'pliego_cobertura_intereses_min',
    'rentabilidad_patrimonio_min_pct': 'pliego_rentabilidad_patrimonio_min_pct',
    'rentabilidad_activo_min_pct': 'pliego_rentabilidad_activo_min_pct',
    'capital_trabajo_min_pct_presupuesto': 'pliego_capital_trabajo_min_pct_presupuesto',
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def cargar_resultados() -> dict:
    if not JSON_RESULTS.exists():
        return {}
    with JSON_RESULTS.open(encoding='utf-8') as f:
        data = json.load(f)
    return {r['id_contrato']: r for r in data if 'id_contrato' in r}


def guardar_resultado(id_contrato: str, resultado: dict):
    if not JSON_RESULTS.exists():
        data = []
    else:
        with JSON_RESULTS.open(encoding='utf-8') as f:
            data = json.load(f)
    data = [r for r in data if r.get('id_contrato') != id_contrato]
    data.append(resultado)
    data.sort(key=lambda r: r.get('id_contrato', ''))
    JSON_RESULTS.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, default=str),
        encoding='utf-8',
    )


def obtener_pendientes(df_consorcios: pd.DataFrame, resultados: dict) -> list:
    """Consorcios con indicadores nulos O sin estado final ok."""
    ESTADOS_OK = {'ok'}
    pendientes = []
    for _, row in df_consorcios.iterrows():
        id_c = row['id_contrato']
        prev = resultados.get(id_c)
        # Ya extraído correctamente → saltar
        if prev and prev.get('estado') in ESTADOS_OK:
            continue
        pendientes.append(row.to_dict())
    return pendientes


def url_browser(url_proceso: str) -> str:
    return url_proceso.replace('&isModal=true', '').replace('&asPopupView=true', '')


# ── CapSolver ─────────────────────────────────────────────────────────────────

def resolver_captcha_sync(api_key: str) -> str:
    try:
        resp = requests.post(f'{CAPSOLVER_URL}/createTask', json={
            'clientKey': api_key,
            'task': {
                'type': 'ReCaptchaV2TaskProxyLess',
                'websiteURL': SECOP_SITE_URL,
                'websiteKey': SECOP_SITE_KEY,
            },
        }, timeout=30).json()
        if resp.get('errorId'):
            return ''
        task_id = resp.get('taskId')
        for _ in range(120):
            time.sleep(1)
            poll = requests.post(f'{CAPSOLVER_URL}/getTaskResult', json={
                'clientKey': api_key, 'taskId': task_id,
            }, timeout=30).json()
            if poll.get('status') == 'ready':
                return poll.get('solution', {}).get('gRecaptchaResponse', '')
            if poll.get('status') == 'failed' or poll.get('errorId'):
                return ''
    except Exception:
        pass
    return ''


async def resolver_captcha_page(page, api_key: str) -> bool:
    if 'GoogleReCaptcha' not in page.url:
        if not await page.query_selector('#divGoogleReCaptcha'):
            return True
    print('  🔐 CAPTCHA — resolviendo...')
    mkey = await page.evaluate("""() => {
        const btn = document.getElementById('btnCaptchaCheckButton');
        if (!btn) return null;
        const m = (btn.getAttribute('onclick') || '').match(/mkey=([a-f0-9_]+)/);
        return m ? m[1] : null;
    }""")
    if not mkey:
        return False
    token = resolver_captcha_sync(api_key)
    if not token:
        return False
    await page.goto(
        f'{BASE_URL}/Public/Common/GoogleReCaptcha/CaptchaCheck?responseKey={token}&mkey={mkey}',
        wait_until='domcontentloaded', timeout=60000,
    )
    await asyncio.sleep(2)
    return 'GoogleReCaptcha' not in page.url


# ── Playwright: listar y descargar ────────────────────────────────────────────

async def listar_documentos(page, url: str, capsolver_key: str) -> list:
    """Navega al proceso y retorna lista de documentos."""
    await page.goto(url, wait_until='domcontentloaded', timeout=60000)
    await asyncio.sleep(2)

    if 'GoogleReCaptcha' in page.url or await page.query_selector('#divGoogleReCaptcha'):
        ok = await resolver_captcha_page(page, capsolver_key)
        if not ok:
            print('  ❌ CAPTCHA no resuelto')
            return []
        await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        await asyncio.sleep(3)

    try:
        await page.wait_for_selector('#grdGridDocumentList_tbl', timeout=30000)
    except Exception:
        await page.wait_for_load_state('networkidle')
        await asyncio.sleep(3)
        try:
            await page.wait_for_selector('#grdGridDocumentList_tbl', timeout=15000)
        except Exception:
            return []

    return await page.evaluate("""() => {
        const rows = document.querySelectorAll(
            '#grdGridDocumentList_tbl tbody tr:not(#grdGridDocumentList_header)'
        );
        return Array.from(rows).map((row, i) => {
            const span = row.querySelector('span.VortalSpan');
            const link = row.querySelector('a[onclick*="DownloadFile"]');
            return (span && link)
                ? { idx: i + 1, name: span.textContent.trim(), linkId: link.id }
                : null;
        }).filter(Boolean);
    }""")


async def descargar_doc(page, doc: dict, id_contrato: str) -> Path:
    """Descarga el documento elegido."""
    link_el = page.locator(f'#{doc["linkId"]}')
    try:
        async with page.expect_download(timeout=90000) as dl_info:
            await link_el.click()
        download = await dl_info.value
        suggested = download.suggested_filename or f'{id_contrato}.pdf'
        ext = Path(suggested).suffix.lower() or '.pdf'
        dest = PLIEGOS_DIR / f'{id_contrato}{ext}'
        await download.save_as(str(dest))
        size_kb = dest.stat().st_size / 1024
        print(f'  ✅ Descargado: {dest.name} ({size_kb:.1f} KB)')
        return dest
    except Exception as e:
        print(f'  ❌ Descarga fallida: {e}')
        return None


# ── PDF + Gemini ──────────────────────────────────────────────────────────────

def extraer_texto_archivo(path: Path) -> str:
    """Extrae texto de PDF, DOCX, DOC, ODT."""
    ext = path.suffix.lower()

    if ext == '.pdf':
        try:
            partes = []
            with pdfplumber.open(path) as pdf:
                n = len(pdf.pages)
                for pg in pdf.pages:
                    txt = pg.extract_text() or ''
                    if txt.strip():
                        partes.append(txt)
            texto = '\n'.join(partes)
            print(f'  📄 PDF — {n} páginas — {len(texto):,} chars')
            return texto
        except Exception as e:
            print(f'  ❌ Error leyendo PDF: {e}')
            return ''

    elif ext == '.docx':
        try:
            doc = python_docx.Document(str(path))
            partes = [p.text for p in doc.paragraphs if p.text.strip()]
            for tabla in doc.tables:
                for fila in tabla.rows:
                    fila_txt = '  '.join(c.text.strip() for c in fila.cells if c.text.strip())
                    if fila_txt:
                        partes.append(fila_txt)
            texto = '\n'.join(partes)
            print(f'  📝 DOCX — {len(doc.paragraphs)} párrafos — {len(texto):,} chars')
            return texto
        except Exception as e:
            print(f'  ❌ Error leyendo DOCX: {e}')
            return ''

    elif ext == '.doc':
        raw = path.read_bytes()
        magic4 = raw[:4]
        magic5 = raw[:5]

        # Caso 1: Es DOCX disfrazado de .doc
        if magic4 == b'PK\x03\x04':
            try:
                doc = python_docx.Document(str(path))
                partes = [p.text for p in doc.paragraphs if p.text.strip()]
                for tabla in doc.tables:
                    for fila in tabla.rows:
                        fila_txt = '  '.join(c.text.strip() for c in fila.cells if c.text.strip())
                        if fila_txt:
                            partes.append(fila_txt)
                texto = '\n'.join(partes)
                print(f'  📝 DOC(DOCX) — {len(texto):,} chars')
                return texto
            except Exception as e:
                print(f'  ❌ Error leyendo DOC como DOCX: {e}')
                return ''

        # Caso 2: RTF disfrazado de .doc (muy común en entidades colombianas)
        if magic5 == b'{\\rtf' or raw[:6] == b'{\r\n\\rt':
            try:
                from striprtf.striprtf import rtf_to_text
                texto = rtf_to_text(raw.decode('latin-1', errors='ignore'))
                texto = texto.strip()
                print(f'  📝 DOC(RTF) — {len(texto):,} chars')
                return texto
            except Exception as e:
                print(f'  ❌ Error leyendo RTF: {e}')
                return ''

        # Caso 3: OLE binario real (Word 97-2003)
        # Extraer texto del stream WordDocument usando UTF-16LE
        # El texto está en bloques de chars UTF-16LE consecutivos
        try:
            import olefile
            import re as _re

            with olefile.OleFileIO(str(path)) as ole:
                if not ole.exists('WordDocument'):
                    print('  ⚠️  DOC: sin stream WordDocument')
                    return ''

                data = ole.openstream('WordDocument').read()

                # El texto real está codificado en UTF-16LE
                # Escanear bloques de chars válidos de ≥8 bytes consecutivos
                partes = []
                i = 0
                bloque = []
                while i < len(data) - 1:
                    word = data[i:i+2]
                    cp = int.from_bytes(word, 'little')
                    # Caracteres imprimibles: letras, números, puntuación, espacios, acentos
                    if (0x0020 <= cp <= 0x007E or   # ASCII imprimible
                            0x00C0 <= cp <= 0x024F or  # Latín extendido (tildes, ñ)
                            cp == 0x000A or cp == 0x000D or cp == 0x0009):  # \n \r \t
                        bloque.append(chr(cp))
                    else:
                        if len(bloque) >= 8:
                            partes.append(''.join(bloque))
                        bloque = []
                    i += 2

                if len(bloque) >= 8:
                    partes.append(''.join(bloque))

                texto = '\n'.join(partes)
                # Limpiar ruido residual
                texto = _re.sub(r'[ \t]{4,}', ' ', texto)
                texto = _re.sub(r'\n{3,}', '\n\n', texto)
                texto = texto.strip()

                if texto:
                    print(f'  📝 DOC(OLE/UTF16) — {len(texto):,} chars')
                    return texto

            print('  ⚠️  DOC OLE: sin texto extraíble')
            return ''
        except Exception as e:
            print(f'  ❌ Error leyendo DOC OLE: {e}')
            return ''

    elif ext == '.odt':
        try:
            doc_odf = odf_load(str(path))
            partes = []
            for nodo in doc_odf.getElementsByType(odf_text.P):
                txt = str(nodo).strip()
                if txt:
                    partes.append(txt)
            texto = '\n'.join(partes)
            print(f'  📝 ODT — {len(partes)} párrafos — {len(texto):,} chars')
            return texto
        except Exception as e:
            print(f'  ❌ Error leyendo ODT: {e}')
            return ''

    else:
        print(f'  ⚠️  Formato no soportado: {ext}')
        return ''


def enviar_gemini(client: genai.Client, modelo: str, texto: str) -> dict:
    print(f'  📡 Enviando {min(len(texto), MAX_CHARS):,} chars a Gemini...')
    prompt = PROMPT + texto[:MAX_CHARS] + '\n---'
    response = client.models.generate_content(
        model=modelo,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=SCHEMA,
            temperature=0.0,
        ),
    )
    try:
        return json.loads(response.text or '{}')
    except json.JSONDecodeError:
        return {'_parse_error': (response.text or '')[:500]}


def mostrar_indicadores(indicadores: dict):
    labels = {
        'liquidez_min': 'Liquidez mín',
        'endeudamiento_max_pct': 'Endeudamiento máx %',
        'cobertura_intereses_min': 'Cobertura intereses mín',
        'rentabilidad_patrimonio_min_pct': 'ROE mín %',
        'rentabilidad_activo_min_pct': 'ROA mín %',
        'capital_trabajo_min_pct_presupuesto': 'Capital trabajo %',
    }
    print()
    print('  ┌─ INDICADORES ──────────────────────────────────────────────────')
    if '_parse_error' in indicadores:
        print(f'  │  ❌ Parse error: {indicadores["_parse_error"][:80]}')
    else:
        for k, label in labels.items():
            val = indicadores.get(k)
            marca = '✅' if val is not None else '  '
            print(f'  │  {marca}  {label:<30}: {val}')
        n_ok = sum(1 for v in indicadores.values() if v is not None)
        print(f'  │')
        print(f'  │  Extraídos: {n_ok}/6')
    print('  └────────────────────────────────────────────────────────────────')


# ── Main ──────────────────────────────────────────────────────────────────────

async def main_async(args):
    load_dotenv(RAIZ / '.env')
    gemini_key = os.getenv('GEMINI_API_KEY')
    capsolver_key = os.getenv('CAPSOLVER_API_KEY')
    if not gemini_key:
        print('ERROR: Falta GEMINI_API_KEY'); return
    if not capsolver_key:
        print('ERROR: Falta CAPSOLVER_API_KEY'); return

    client = genai.Client(api_key=gemini_key)
    PLIEGOS_DIR.mkdir(parents=True, exist_ok=True)

    # ── Cargar datos ─────────────────────────────────────────────────────────
    print('📂 Cargando dataset...')
    df = pd.read_parquet(DATA_PARQUET)
    consorcios = df[df['es_grupo'] == 'Si'].copy()
    resultados = cargar_resultados()

    pendientes = obtener_pendientes(consorcios, resultados)

    total_consorcios = len(consorcios)
    ya_ok = sum(1 for r in resultados.values() if r.get('estado') == 'ok')
    total_pendientes = len(pendientes)

    print()
    print('═' * 65)
    print(f'  Total consorcios            : {total_consorcios:,}')
    print(f'  Ya con indicadores (ok)     : {ya_ok:,}')
    print(f'  Pendientes de revisar       : {total_pendientes:,}')
    print('═' * 65)

    if total_pendientes == 0:
        print('\n✅ Nada pendiente.')
        return

    # Aplicar offset si se pasa --desde
    pendientes = pendientes[args.desde:]
    print(f'\n  Empezando desde #{args.desde + 1}  ({len(pendientes)} por revisar)\n')

    # ── Abrir Playwright ─────────────────────────────────────────────────────
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(
        user_agent=(
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
    )
    page = await context.new_page()

    try:
        for i, row in enumerate(pendientes, start=args.desde + 1):
            id_c = row['id_contrato']
            url_proc = row.get('urlproceso', '')
            entidad = str(row.get('nombre_entidad', ''))[:55]
            proveedor = str(row.get('proveedor_adjudicado', ''))[:55]

            print()
            print('─' * 65)
            print(f'  [{i}/{total_pendientes + args.desde}]  {id_c}')
            print(f'  Entidad  : {entidad}')
            print(f'  Proveedor: {proveedor}')
            print('─' * 65)

            if not url_proc:
                print('  ⚠️  Sin urlproceso — saltando')
                guardar_resultado(id_c, {
                    'id_contrato': id_c, 'estado': 'no_descargado',
                    'error': 'sin_urlproceso', 'metodo': 'gemini',
                })
                continue

            # Abrir en navegador del usuario
            url_vis = url_browser(url_proc)
            print(f'  🌐 Abriendo en tu navegador: {url_vis[:70]}...')
            webbrowser.open(url_vis)

            # Listar documentos via Playwright
            print('  📋 Cargando documentos via Playwright...')
            docs = await listar_documentos(page, url_proc, capsolver_key)

            if not docs:
                print('\n  ⚠️  No se encontraron documentos en la tabla.')
                print('  Opciones: [s] saltar  |  [q] salir')
                try:
                    resp = input('  > ').strip().lower()
                except EOFError:
                    resp = 'q'
                if resp == 'q':
                    break
                guardar_resultado(id_c, {
                    'id_contrato': id_c, 'estado': 'sin_match',
                    'error': 'sin_documentos', 'metodo': 'gemini',
                })
                continue

            # Mostrar lista de documentos
            print()
            print(f'  ┌─ Documentos disponibles ({len(docs)}) ─────────────────────────')
            for d in docs:
                print(f'  │  {d["idx"]:>3}.  {d["name"]}')
            print(f'  └────────────────────────────────────────────────────────────')
            print()
            print('  Opciones: [número] descargar doc  |  [s] saltar  |  [q] salir')

            try:
                resp = input('  > ').strip().lower()
            except EOFError:
                resp = 'q'

            if resp == 'q':
                print('  Saliendo...')
                break

            if resp in ('s', 'skip', ''):
                print('  Saltando...')
                guardar_resultado(id_c, {
                    'id_contrato': id_c, 'estado': 'sin_match',
                    'error': 'usuario_salto', 'metodo': 'gemini',
                })
                continue

            # Descargar el doc elegido
            try:
                elegido_num = int(resp)
                target = next((d for d in docs if d['idx'] == elegido_num), None)
            except ValueError:
                target = None

            if not target:
                print(f'  ❌ Número inválido: {resp} — saltando')
                continue

            print(f'\n  Descargando #{elegido_num}: {target["name"]}')
            pdf_path = await descargar_doc(page, target, id_c)

            if not pdf_path or not pdf_path.exists():
                print('  ❌ Descarga fallida — saltando')
                continue

            EXTS_SOPORTADAS = {'.pdf', '.docx', '.doc', '.odt'}
            if pdf_path.suffix.lower() not in EXTS_SOPORTADAS:
                print(f'  ⚠️  Formato no soportado ({pdf_path.suffix}) — saltando')
                guardar_resultado(id_c, {
                    'id_contrato': id_c, 'archivo': pdf_path.name,
                    'estado': 'no_pdf', 'metodo': 'gemini',
                })
                continue

            # Extraer texto y enviar a Gemini
            texto = extraer_texto_archivo(pdf_path)
            if not texto:
                print('  ❌ PDF sin texto (escaneado?) — saltando')
                guardar_resultado(id_c, {
                    'id_contrato': id_c, 'archivo': pdf_path.name,
                    'estado': 'error_pdf', 'metodo': 'gemini',
                })
                continue

            indicadores = enviar_gemini(client, args.modelo, texto)
            mostrar_indicadores(indicadores)

            # Guardar
            if '_parse_error' not in indicadores:
                n_ok = sum(1 for v in indicadores.values() if v is not None)
                guardar_resultado(id_c, {
                    'id_contrato': id_c,
                    'archivo': pdf_path.name,
                    'estado': 'ok' if n_ok > 0 else 'texto_sin_umbrales',
                    'metodo_texto': 'completo',
                    'indicadores_extraidos': n_ok,
                    'metodo': 'gemini',
                    **indicadores,
                })
                ya_ok += 1 if n_ok > 0 else 0

            print(f'\n  Procesados OK hasta ahora: {ya_ok}')

    finally:
        await browser.close()
        await playwright.stop()

    print()
    print('═' * 65)
    print(f'  Sesión terminada. Contratos con indicadores: {ya_ok:,}')
    print('═' * 65)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--modelo', default=MODELO_DEFAULT)
    ap.add_argument('--desde', type=int, default=0,
                    help='Empezar desde el N-ésimo pendiente (para retomar)')
    args = ap.parse_args()
    asyncio.run(main_async(args))


if __name__ == '__main__':
    main()
