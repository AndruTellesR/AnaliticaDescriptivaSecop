"""
Inspector interactivo de contratos.

Lista documentos del contrato, usuario elige cuál descargar,
se envía CONTENIDO COMPLETO a Gemini (sin filtros).

Uso:
    python scripts/gemini/inspeccionar_contrato.py CO1.PCCNTR.1003010
    python scripts/gemini/inspeccionar_contrato.py CO1.PCCNTR.1003010 --guardar
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
MAX_CHARS = 120000  # Sin filtros → documento completo, aumentamos el límite

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


# ── CapSolver ─────────────────────────────────────────────────────────────────

def resolver_captcha_sync(api_key: str) -> str:
    payload = {
        'clientKey': api_key,
        'task': {
            'type': 'ReCaptchaV2TaskProxyLess',
            'websiteURL': SECOP_SITE_URL,
            'websiteKey': SECOP_SITE_KEY,
        },
    }
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
        if poll.get('status') == 'ready':
            return poll.get('solution', {}).get('gRecaptchaResponse', '')
        if poll.get('status') == 'failed' or poll.get('errorId'):
            return ''
    return ''


async def resolver_captcha_secop(page, api_key: str) -> bool:
    if 'GoogleReCaptcha' not in page.url:
        if not await page.query_selector('#divGoogleReCaptcha'):
            return True

    print('  🔐 CAPTCHA detectado — resolviendo...')
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


# ── Core ──────────────────────────────────────────────────────────────────────

async def listar_y_descargar(url_proceso: str, id_contrato: str,
                               capsolver_key: str) -> Path:
    """Abre Playwright, lista documentos, usuario elige, descarga."""
    PLIEGOS_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # visible para debug
        context = await browser.new_context(
            user_agent=(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
        )
        page = await context.new_page()

        print(f'\n  Navegando a: {url_proceso[:80]}...')
        await page.goto(url_proceso, wait_until='domcontentloaded', timeout=60000)
        await asyncio.sleep(2)

        # CAPTCHA
        ok = await resolver_captcha_secop(page, capsolver_key)
        if not ok:
            await browser.close()
            print('  ❌ No se pudo resolver CAPTCHA')
            return None

        # Esperar tabla
        try:
            await page.wait_for_selector('#grdGridDocumentList_tbl', timeout=30000)
        except Exception:
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(3)
            try:
                await page.wait_for_selector('#grdGridDocumentList_tbl', timeout=15000)
            except Exception:
                await browser.close()
                print('  ❌ Tabla de documentos no cargó')
                return None

        # Leer documentos
        doc_info = await page.evaluate("""() => {
            const rows = document.querySelectorAll(
                '#grdGridDocumentList_tbl tbody tr:not(#grdGridDocumentList_header)'
            );
            return Array.from(rows).map((row, i) => {
                const span = row.querySelector('span.VortalSpan');
                const link = row.querySelector('a[onclick*="DownloadFile"]');
                return span && link
                    ? { idx: i+1, name: span.textContent.trim(), linkId: link.id }
                    : null;
            }).filter(Boolean);
        }""")

        if not doc_info:
            await browser.close()
            print('  ❌ No se encontraron documentos')
            return None

        # Mostrar lista
        print(f'\n  ┌─ Documentos disponibles ({len(doc_info)}) ──────────────────────────')
        for d in doc_info:
            print(f'  │  {d["idx"]:>3}.  {d["name"]}')
        print(f'  └──────────────────────────────────────────────────────────────────')

        # Usuario elige
        try:
            resp = input('\n  Número del documento a descargar (o Enter para cancelar): ').strip()
        except EOFError:
            resp = ''

        if not resp:
            await browser.close()
            print('  Cancelado.')
            return None

        try:
            elegido_idx = int(resp)
            target = next((d for d in doc_info if d['idx'] == elegido_idx), None)
        except ValueError:
            target = None

        if not target:
            await browser.close()
            print(f'  ❌ Número inválido: {resp}')
            return None

        print(f'\n  Descargando: {target["name"]}')

        # Descargar
        link_el = page.locator(f'#{target["linkId"]}')
        try:
            async with page.expect_download(timeout=90000) as dl_info:
                await link_el.click()
            download = await dl_info.value
            suggested = download.suggested_filename or f'{id_contrato}.pdf'
            ext = Path(suggested).suffix.lower() or '.pdf'
            dest = PLIEGOS_DIR / f'{id_contrato}{ext}'
            await download.save_as(str(dest))
            size_kb = dest.stat().st_size / 1024
            print(f'  ✅ {size_kb:.1f} KB → {dest.name}')
        except Exception as e:
            await browser.close()
            print(f'  ❌ Descarga fallida: {e}')
            return None

        await browser.close()
        return dest


def extraer_texto_completo(pdf_path: Path) -> str:
    """Extrae TODO el texto del PDF, sin filtros."""
    try:
        partes = []
        with pdfplumber.open(pdf_path) as pdf:
            n_paginas = len(pdf.pages)
            for i, page in enumerate(pdf.pages, 1):
                txt = page.extract_text() or ''
                if txt.strip():
                    partes.append(txt)
        texto = '\n'.join(partes)
        print(f'  📄 {n_paginas} páginas — {len(texto):,} caracteres extraídos')
        return texto
    except Exception as e:
        print(f'  ❌ Error leyendo PDF: {e}')
        return ''


def enviar_a_gemini(client: genai.Client, modelo: str, texto: str) -> dict:
    """Envía texto completo a Gemini y retorna indicadores."""
    chars_a_enviar = min(len(texto), MAX_CHARS)
    print(f'  📡 Enviando {chars_a_enviar:,} chars a {modelo}...')

    prompt = PROMPT_INSTRUCCIONES + texto[:MAX_CHARS] + '\n---'
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


def guardar_en_json(id_contrato: str, resultado: dict):
    """Actualiza el JSON maestro de resultados."""
    if not JSON_RESULTS.exists():
        data = []
    else:
        with JSON_RESULTS.open(encoding='utf-8') as f:
            data = json.load(f)

    # Remover entrada anterior del mismo contrato
    data = [r for r in data if r.get('id_contrato') != id_contrato]
    data.append(resultado)
    data.sort(key=lambda r: r.get('id_contrato', ''))

    JSON_RESULTS.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, default=str),
        encoding='utf-8'
    )
    print(f'  💾 Guardado en JSON maestro')


async def main_async(args):
    load_dotenv(RAIZ / '.env')
    gemini_key = os.getenv('GEMINI_API_KEY')
    capsolver_key = os.getenv('CAPSOLVER_API_KEY')

    if not gemini_key:
        print('ERROR: Falta GEMINI_API_KEY en .env')
        return
    if not capsolver_key:
        print('ERROR: Falta CAPSOLVER_API_KEY en .env')
        return

    # Buscar contrato en parquet
    df = pd.read_parquet(DATA_PARQUET)
    fila = df[df['id_contrato'] == args.id_contrato]
    if fila.empty:
        print(f'❌ Contrato {args.id_contrato} no encontrado en parquet')
        return

    row = fila.iloc[0]
    url_proceso = row.get('urlproceso', '')
    if not url_proceso:
        print(f'❌ Sin urlproceso para {args.id_contrato}')
        return

    # URL para abrir en navegador normal (sin modal)
    url_browser = url_proceso.replace('&isModal=true', '').replace('&asPopupView=true', '')

    print('─' * 70)
    print(f'  Contrato  : {args.id_contrato}')
    print(f'  Entidad   : {row.get("nombre_entidad", "")[:60]}')
    print(f'  Proveedor : {row.get("proveedor_adjudicado", "")[:60]}')
    print(f'  URL browser: {url_browser}')
    print('─' * 70)

    # Abrir en navegador del sistema (distinto al Playwright)
    print('  🌐 Abriendo en tu navegador...')
    webbrowser.open(url_browser)

    # ¿Ya tiene PDF local?
    pdfs = list(PLIEGOS_DIR.glob(f'{args.id_contrato}.*'))
    pdf_path = next((p for p in pdfs if p.suffix.lower() == '.pdf'), None)

    if pdf_path and not args.forzar_descarga:
        print(f'\n  PDF ya existe: {pdf_path.name}')
        resp = input('  ¿Usar este PDF? [S/n]: ').strip().lower()
        if resp not in ('n', 'no'):
            pass  # usar el existente
        else:
            pdf_path = None

    if not pdf_path:
        pdf_path = await listar_y_descargar(url_proceso, args.id_contrato, capsolver_key)
        if not pdf_path:
            return

    # Extraer texto completo (sin filtros)
    print(f'\n  Extrayendo texto completo...')
    texto = extraer_texto_completo(pdf_path)
    if not texto:
        print('  ❌ PDF sin texto (posiblemente escaneado)')
        return

    if args.guardar_texto:
        out = RAIZ / 'data' / 'prompts_inspeccion' / f'{args.id_contrato}_completo.txt'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(texto, encoding='utf-8')
        print(f'  📝 Texto guardado: {out}')

    # Enviar a Gemini
    print()
    client = genai.Client(api_key=gemini_key)
    indicadores = enviar_a_gemini(client, args.modelo, texto)

    # Mostrar resultado
    print('\n  ┌─ INDICADORES EXTRAÍDOS ─────────────────────────────────────────')
    if '_parse_error' in indicadores:
        print(f'  │  ❌ Error de parseo: {indicadores["_parse_error"]}')
    else:
        labels = {
            'liquidez_min': 'Liquidez mín',
            'endeudamiento_max_pct': 'Endeudamiento máx %',
            'cobertura_intereses_min': 'Cobertura intereses mín',
            'rentabilidad_patrimonio_min_pct': 'ROE mín %',
            'rentabilidad_activo_min_pct': 'ROA mín %',
            'capital_trabajo_min_pct_presupuesto': 'Capital trabajo %',
        }
        n_ok = 0
        for k, label in labels.items():
            val = indicadores.get(k)
            marca = '✅' if val is not None else '—'
            print(f'  │  {marca}  {label:<30}: {val}')
            if val is not None:
                n_ok += 1
        print(f'  │')
        print(f'  │  Total extraídos: {n_ok}/6')
    print('  └────────────────────────────────────────────────────────────────')

    # Guardar en JSON
    if '_parse_error' not in indicadores:
        n_ok = sum(1 for v in indicadores.values() if v is not None)
        resultado = {
            'id_contrato': args.id_contrato,
            'archivo': pdf_path.name,
            'estado': 'ok' if n_ok > 0 else 'texto_sin_umbrales',
            'metodo_texto': 'completo',
            'indicadores_extraidos': n_ok,
            'metodo': 'gemini',
            **indicadores,
        }
        guardar_en_json(args.id_contrato, resultado)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('id_contrato', help='ID del contrato, ej: CO1.PCCNTR.1003010')
    ap.add_argument('--modelo', default=MODELO_DEFAULT)
    ap.add_argument('--guardar-texto', action='store_true',
                    help='Guardar texto completo extraído a disco')
    ap.add_argument('--forzar-descarga', action='store_true',
                    help='Re-descargar aunque ya exista PDF local')
    args = ap.parse_args()

    asyncio.run(main_async(args))


if __name__ == '__main__':
    main()
