"""
Descargador interactivo de pliegos de SECOP II.

Lista los consorcios que AUN no tienen PDF descargado y permite al usuario
seleccionar (por indice, rango, ID o filtro) cuales descargar.

Flujo:
  1. Carga el parquet de contratos y filtra es_grupo='Si'.
  2. Cruza con la carpeta de PDFs para quedarse con los que faltan.
  3. Menu interactivo por consola:
       l / list              -> listar candidatos (paginados)
       f <campo>=<valor>     -> filtrar (entidad, departamento, proveedor, id)
       c / clear             -> limpiar filtros
       n / next, p / prev    -> paginar
       s / stats             -> estadisticas de candidatos
       d <seleccion>         -> descargar (ej: d 1-5,7,10)
       h / help              -> ayuda
       q / quit              -> salir

  4. Cada descarga usa Playwright + CapSolver (re-uso de la logica de
     secop-scraper/scraper_pliegos_poc.py).

Uso:
    python scripts/gemini/descargar_pliego.py
    python scripts/gemini/descargar_pliego.py --page-size 30
"""

import argparse
import asyncio
import os
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from playwright.async_api import async_playwright


# ── Configuracion ─────────────────────────────────────────────────────────────

RAIZ = Path(__file__).resolve().parent.parent.parent
DATA_PARQUET = RAIZ / 'data' / 'contratos_electronicos_obra.parquet'
PLIEGOS_DIR = Path('C:/Users/angel/OneDrive/Escritorio/trabajo dirigido/secop-scraper/storage/pliegos')

BASE_URL = 'https://community.secop.gov.co'
SECOP_SITE_KEY = '6LcMmakZAAAAAB157Q90hORUGtNd790TCws4vBNw'
SECOP_SITE_URL = 'https://community.secop.gov.co/'

CAPSOLVER_URL = 'https://api.capsolver.com'
MAX_CAPTCHA_RETRIES = 3

DELAY_ENTRE_DESCARGAS = 2.5  # segundos entre un PDF y el siguiente


# ── Utilidades ────────────────────────────────────────────────────────────────

def sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name[:150]


def fmt_money(v) -> str:
    try:
        n = float(v)
        return f'${n/1e6:.1f}M'
    except Exception:
        return '-'


def truncar(s: str, n: int) -> str:
    s = str(s or '')
    return s if len(s) <= n else s[:n-1] + '…'


# ── CapSolver ─────────────────────────────────────────────────────────────────

def _resolver_captcha_una_vez(api_key: str) -> str:
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
        status = poll.get('status')
        if status == 'ready':
            return poll.get('solution', {}).get('gRecaptchaResponse', '')
        if status == 'failed' or poll.get('errorId'):
            return ''
    return ''


def resolver_captcha(api_key: str) -> str:
    for intento in range(1, MAX_CAPTCHA_RETRIES + 1):
        print(f'    CapSolver intento {intento}/{MAX_CAPTCHA_RETRIES}...', end=' ', flush=True)
        token = _resolver_captcha_una_vez(api_key)
        if token:
            print(f'OK ({len(token)} chars)')
            return token
        print('fallo')
    return ''


async def resolver_captcha_secop(page, api_key: str) -> bool:
    current_url = page.url
    is_captcha = 'GoogleReCaptcha' in current_url
    if not is_captcha:
        has_captcha = await page.query_selector('#divGoogleReCaptcha')
        if not has_captcha:
            return True

    print('    reCAPTCHA detectado — resolviendo con CapSolver...')
    mkey = await page.evaluate("""() => {
        const btn = document.getElementById('btnCaptchaCheckButton');
        if (!btn) return null;
        const onclick = btn.getAttribute('onclick') || '';
        const m = onclick.match(/mkey=([a-f0-9_]+)/);
        return m ? m[1] : null;
    }""")

    if not mkey:
        print('    no se pudo extraer mkey')
        return False

    token = resolver_captcha(api_key)
    if not token:
        return False

    check_url = f'{BASE_URL}/Public/Common/GoogleReCaptcha/CaptchaCheck?responseKey={token}&mkey={mkey}'
    await page.goto(check_url, wait_until='domcontentloaded', timeout=60000)
    await asyncio.sleep(2)

    if 'GoogleReCaptcha' in page.url:
        return False
    return True


# ── Carga y filtrado de candidatos ────────────────────────────────────────────

def cargar_candidatos() -> pd.DataFrame:
    """Lee el parquet y retorna consorcios sin PDF descargado."""
    df = pd.read_parquet(DATA_PARQUET)
    consorcios = df[df['es_grupo'] == 'Si'].copy()

    pdfs_existentes = {p.stem for p in PLIEGOS_DIR.iterdir() if p.is_file()}

    pendientes = consorcios[~consorcios['id_contrato'].isin(pdfs_existentes)].copy()

    cols = [
        'id_contrato', 'urlproceso', 'proveedor_adjudicado',
        'nombre_entidad', 'departamento', 'valor_del_contrato',
    ]
    existentes = [c for c in cols if c in pendientes.columns]
    pendientes = pendientes[existentes].reset_index(drop=True)
    return pendientes


# ── Menu interactivo ──────────────────────────────────────────────────────────

def parsear_seleccion(sel: str, n_max: int) -> list[int]:
    """'1-5,7,10-12' -> [0,1,2,3,4,6,9,10,11] (indices 0-based)."""
    indices = set()
    for parte in sel.replace(' ', '').split(','):
        if not parte:
            continue
        if '-' in parte:
            try:
                a, b = parte.split('-', 1)
                for i in range(int(a), int(b) + 1):
                    if 1 <= i <= n_max:
                        indices.add(i - 1)
            except ValueError:
                raise ValueError(f'rango invalido: {parte}')
        else:
            try:
                i = int(parte)
                if 1 <= i <= n_max:
                    indices.add(i - 1)
            except ValueError:
                raise ValueError(f'indice invalido: {parte}')
    return sorted(indices)


def imprimir_tabla(df: pd.DataFrame, page: int, page_size: int):
    total = len(df)
    ini = page * page_size
    fin = min(ini + page_size, total)
    chunk = df.iloc[ini:fin]

    print()
    print(f'┌─ Candidatos {ini+1}–{fin} de {total} ' + '─' * 40)
    print(f'  {"#":>4}  {"id_contrato":<22} {"Entidad":<28} {"Depto":<18} {"Valor":>8}')
    print(f'  {"-"*4}  {"-"*22} {"-"*28} {"-"*18} {"-"*8}')
    for idx_rel, (_, row) in enumerate(chunk.iterrows(), start=1):
        idx_abs = ini + idx_rel
        print(
            f'  {idx_abs:>4}  '
            f'{row["id_contrato"]:<22} '
            f'{truncar(row.get("nombre_entidad", ""), 28):<28} '
            f'{truncar(row.get("departamento", ""), 18):<18} '
            f'{fmt_money(row.get("valor_del_contrato")):>8}'
        )
    print('└' + '─' * 70)
    n_paginas = (total + page_size - 1) // page_size
    print(f'  Pag {page+1}/{n_paginas}  |  n/p=paginar  d <sel>=descargar interactivo  da <sel>=auto  h=ayuda  q=salir')
    print()


def imprimir_ayuda():
    print("""
Comandos disponibles:

  l, list                  Listar candidatos (pagina actual)
  n, next                  Siguiente pagina
  p, prev                  Pagina anterior

  f <campo>=<valor>        Aplicar filtro. Campos: entidad, depto, proveedor, id
                           Ej: f entidad=INVIAS
                           Ej: f depto=Bogota
                           Ej: f id=CO1.PCCNTR.1020
  c, clear                 Limpiar filtros

  s, stats                 Estadisticas de candidatos (por entidad/depto)
  show <indice>            Ver detalles de un candidato especifico

  d <seleccion>            Descargar INTERACTIVO — por cada contrato te lista
                           los documentos disponibles y eliges cual bajar
                           (o Enter para usar la recomendacion automatica).
                             d 1        -> descargar el #1
                             d 1-5      -> del 1 al 5
                             d 1,3,7    -> los que elijas
                             d 1-3,8    -> combinados

  da <seleccion>           Descargar AUTOMATICO — usa la heuristica sin preguntar
                           (util para batches grandes sin supervision).

  h, help                  Esta ayuda
  q, quit                  Salir
""")


# ── Descarga de un pliego ─────────────────────────────────────────────────────

def _aplicar_heuristica(doc_info: list[dict]) -> tuple[dict | None, int]:
    """Devuelve (target_doc, nivel_usado) o (None, 0) si no hay candidato."""
    EXCLUSIONES = ['anexo', 'estudio previ', 'estudio del sector', 'matriz',
                    'formulario', 'propuesta', 'presupuesto oficial', 'minuta',
                    'borrador', 'acta de', 'adenda', 'observacion']
    PRIORIDADES = [
        ['pliego de condiciones definitiv', 'pliego definitiv'],
        ['invitacion publica', 'invitación pública', 'invitacion pública'],
        ['pliego'],
        ['condiciones definitiv', 'bases definitiv', 'condiciones del proceso'],
        ['términos de referencia', 'terminos de referencia'],
    ]

    def encontrar(keywords, exclude):
        out = []
        for d in doc_info:
            nombre = d['name'].lower()
            if any(kw in nombre for kw in keywords) and not any(ex in nombre for ex in exclude):
                out.append(d)
        return out

    for nivel, kws in enumerate(PRIORIDADES, start=1):
        excl = EXCLUSIONES + (['proyecto de pliego'] if nivel == 3 else [])
        docs = encontrar(kws, excl)
        if docs:
            return docs[-1], nivel
    docs = encontrar(['proyecto de pliego'], [])
    if docs:
        return docs[-1], 99
    return None, 0


def _seleccionar_documento_interactivo(doc_info: list[dict]) -> dict | None:
    """
    Muestra todos los documentos, la recomendacion, y pide al usuario que elija.
    Retorna el doc seleccionado o None si el user decide saltar.
    """
    print(f'    {len(doc_info)} documentos disponibles:')
    rec, nivel = _aplicar_heuristica(doc_info)
    rec_idx = doc_info.index(rec) + 1 if rec else None
    for i, d in enumerate(doc_info, start=1):
        marca = ' ← recomendado' if i == rec_idx else ''
        print(f'      {i:>2}  {d["name"]}{marca}')

    if rec:
        nota = 'borrador' if nivel == 99 else f'nivel {nivel}'
        prompt = f'    Elegir # [Enter={rec_idx} ({nota}), s=saltar]: '
    else:
        prompt = f'    Elegir # [sin recomendacion, s=saltar]: '

    try:
        resp = input(prompt).strip().lower()
    except EOFError:
        return rec  # stdin cerrado → usa recomendacion

    if resp in ('s', 'skip', 'saltar'):
        return None
    if resp == '' and rec:
        return rec
    try:
        idx = int(resp)
        if 1 <= idx <= len(doc_info):
            return doc_info[idx - 1]
        print('    indice fuera de rango; saltando este contrato')
        return None
    except ValueError:
        print('    respuesta invalida; saltando este contrato')
        return None


async def descargar_uno(page, url: str, id_contrato: str, capsolver_key: str,
                          auto: bool = False) -> Path | None:
    print(f'    URL: {url[:90]}...')
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        await asyncio.sleep(2)

        if 'GoogleReCaptcha' in page.url or await page.query_selector('#divGoogleReCaptcha'):
            ok = await resolver_captcha_secop(page, capsolver_key)
            if not ok:
                print('    no se pudo resolver CAPTCHA')
                return None
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
                print('    tabla de documentos no cargo')
                return None

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
            print('    no se encontraron documentos')
            return None

        if auto:
            target, nivel_usado = _aplicar_heuristica(doc_info)
            if not target:
                print('    ningun documento parece ser un pliego (modo auto). Disponibles:')
                for d in doc_info[:10]:
                    print(f'      - {d["name"]}')
                if len(doc_info) > 10:
                    print(f'      ... ({len(doc_info)-10} mas)')
                return None
            nota = ' (borrador)' if nivel_usado == 99 else f' (nivel {nivel_usado})'
            print(f'    seleccionado: {target["name"]}{nota}')
        else:
            target = _seleccionar_documento_interactivo(doc_info)
            if target is None:
                print('    saltado por el usuario')
                return None
            print(f'    descargando: {target["name"]}')

        link_el = page.locator(f'#{target["linkId"]}')
        try:
            async with page.expect_download(timeout=60000) as download_info:
                await link_el.click()
            download = await download_info.value

            suggested = download.suggested_filename or f'{id_contrato}.pdf'
            ext = Path(suggested).suffix or '.pdf'
            filepath = PLIEGOS_DIR / f'{id_contrato}{ext}'

            await download.save_as(str(filepath))
            size_kb = filepath.stat().st_size / 1024
            print(f'    OK — {size_kb:.1f} KB -> {filepath.name}')
            return filepath
        except Exception as dl_err:
            print(f'    descarga fallida: {dl_err}')
            return None

    except Exception as e:
        print(f'    error: {e}')
        return None


async def descargar_batch(seleccion_df: pd.DataFrame, capsolver_key: str, auto: bool = False):
    """Abre Playwright, resuelve captcha inicial, itera descargas."""
    PLIEGOS_DIR.mkdir(parents=True, exist_ok=True)

    print()
    print(f'Abriendo navegador e iniciando sesion SECOP II...')

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
        )
        page = await context.new_page()

        # CAPTCHA inicial con la primera URL
        primera_url = seleccion_df.iloc[0]['urlproceso']
        await page.goto(primera_url, wait_until='domcontentloaded', timeout=60000)
        await asyncio.sleep(2)
        ok = await resolver_captcha_secop(page, capsolver_key)
        if not ok:
            print('  no se pudo iniciar sesion SECOP II')
            await browser.close()
            return
        print('  sesion activa\n')

        ok_count = 0
        fail_count = 0
        total = len(seleccion_df)

        for i, (_, row) in enumerate(seleccion_df.iterrows(), start=1):
            id_c = row['id_contrato']
            url  = row['urlproceso']
            print(f'  [{i}/{total}] {id_c}')
            result = await descargar_uno(page, url, id_c, capsolver_key, auto=auto)
            if result:
                ok_count += 1
            else:
                fail_count += 1
            if i < total:
                await asyncio.sleep(DELAY_ENTRE_DESCARGAS)

        await browser.close()

    print()
    print(f'─ Resumen ─')
    print(f'  Descargados OK : {ok_count}/{total}')
    print(f'  Fallidos       : {fail_count}/{total}')
    print(f'  Carpeta        : {PLIEGOS_DIR}')


# ── Balance CapSolver ─────────────────────────────────────────────────────────

def balance_capsolver(api_key: str) -> float:
    try:
        r = requests.post(
            f'{CAPSOLVER_URL}/getBalance',
            json={'clientKey': api_key},
            timeout=10,
        ).json()
        return float(r.get('balance', 0))
    except Exception:
        return -1.0


# ── Loop principal ────────────────────────────────────────────────────────────

def aplicar_filtro(df: pd.DataFrame, campo: str, valor: str) -> pd.DataFrame:
    valor = valor.strip().lower()
    mapa = {
        'entidad':   'nombre_entidad',
        'depto':     'departamento',
        'departamento': 'departamento',
        'proveedor': 'proveedor_adjudicado',
        'id':        'id_contrato',
    }
    col = mapa.get(campo.strip().lower())
    if col is None or col not in df.columns:
        raise ValueError(f'campo desconocido: {campo}  (usa: {list(mapa.keys())})')
    return df[df[col].astype(str).str.lower().str.contains(valor, na=False)]


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    ap = argparse.ArgumentParser()
    ap.add_argument('--page-size', type=int, default=20,
                    help='Filas por pagina en el listado (default 20)')
    args = ap.parse_args()

    load_dotenv(RAIZ / '.env')
    capsolver_key = os.getenv('CAPSOLVER_API_KEY')
    if not capsolver_key:
        print('ERROR: falta CAPSOLVER_API_KEY en .env', file=sys.stderr)
        sys.exit(1)

    print('─' * 65)
    print('  Descargador interactivo de pliegos SECOP II')
    print('─' * 65)
    bal = balance_capsolver(capsolver_key)
    print(f'  CapSolver balance : ${bal:.4f} USD' if bal >= 0 else '  CapSolver balance : desconocido')
    print(f'  Carpeta destino   : {PLIEGOS_DIR}')
    print()

    print('Cargando candidatos...')
    all_candidatos = cargar_candidatos()
    print(f'  Consorcios sin PDF descargado: {len(all_candidatos):,}')

    df_vista = all_candidatos.copy()
    page = 0
    filtros = []

    imprimir_tabla(df_vista, page, args.page_size)

    while True:
        try:
            cmd = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not cmd:
            continue

        partes = cmd.split(None, 1)
        op = partes[0].lower()
        arg = partes[1] if len(partes) > 1 else ''

        if op in ('q', 'quit', 'exit'):
            break

        elif op in ('h', 'help', '?'):
            imprimir_ayuda()

        elif op in ('l', 'list'):
            imprimir_tabla(df_vista, page, args.page_size)

        elif op in ('n', 'next'):
            max_page = (len(df_vista) - 1) // args.page_size
            if page < max_page:
                page += 1
            imprimir_tabla(df_vista, page, args.page_size)

        elif op in ('p', 'prev'):
            if page > 0:
                page -= 1
            imprimir_tabla(df_vista, page, args.page_size)

        elif op == 'f':
            if '=' not in arg:
                print('uso: f <campo>=<valor>')
                continue
            campo, valor = arg.split('=', 1)
            try:
                df_vista = aplicar_filtro(df_vista, campo, valor)
                filtros.append(f'{campo}={valor}')
                page = 0
                print(f'  filtros activos: {", ".join(filtros)}  →  {len(df_vista):,} candidatos')
                imprimir_tabla(df_vista, page, args.page_size)
            except ValueError as e:
                print(f'  {e}')

        elif op in ('c', 'clear'):
            df_vista = all_candidatos.copy()
            filtros = []
            page = 0
            print(f'  filtros limpiados — {len(df_vista):,} candidatos')
            imprimir_tabla(df_vista, page, args.page_size)

        elif op in ('s', 'stats'):
            print()
            print(f'  Total candidatos : {len(df_vista):,}')
            if 'nombre_entidad' in df_vista.columns:
                print(f'\n  Top 10 entidades:')
                for ent, n in df_vista['nombre_entidad'].value_counts().head(10).items():
                    print(f'    {n:>5}  {truncar(ent, 55)}')
            if 'departamento' in df_vista.columns:
                print(f'\n  Top 10 departamentos:')
                for d, n in df_vista['departamento'].value_counts().head(10).items():
                    print(f'    {n:>5}  {d}')
            print()

        elif op == 'show':
            try:
                i = int(arg)
                if 1 <= i <= len(df_vista):
                    row = df_vista.iloc[i-1]
                    print()
                    for k, v in row.items():
                        print(f'  {k:<24}: {v}')
                    print()
                else:
                    print(f'  indice fuera de rango (1..{len(df_vista)})')
            except ValueError:
                print('  uso: show <indice>')

        elif op in ('d', 'download', 'da'):
            auto_mode = (op == 'da')
            if not arg:
                print(f'  uso: {op} <seleccion>   ej: {op} 1-5,7')
                continue
            try:
                idx_list = parsear_seleccion(arg, len(df_vista))
            except ValueError as e:
                print(f'  {e}')
                continue
            if not idx_list:
                print('  seleccion vacia')
                continue

            seleccion = df_vista.iloc[idx_list].reset_index(drop=True)
            modo_txt = 'AUTO (heuristica)' if auto_mode else 'INTERACTIVO (eliges el doc)'
            print()
            print(f'Vas a descargar {len(seleccion)} PDF(s) en modo {modo_txt}:')
            for _, r in seleccion.iterrows():
                print(f'  {r["id_contrato"]:<22}  {truncar(r.get("nombre_entidad",""), 50)}')
            conf = input('confirmar? [s/N]: ').strip().lower()
            if conf not in ('s', 'si', 'y', 'yes'):
                print('  cancelado')
                continue

            try:
                asyncio.run(descargar_batch(seleccion, capsolver_key, auto=auto_mode))
            except Exception as e:
                print(f'  error en la descarga: {e}')

            # Refrescar candidatos (quitar los recien descargados)
            all_candidatos = cargar_candidatos()
            df_vista = all_candidatos.copy()
            for f in filtros:
                campo, valor = f.split('=', 1)
                try:
                    df_vista = aplicar_filtro(df_vista, campo, valor)
                except ValueError:
                    pass
            page = 0
            print(f'\n  candidatos restantes (aplicando filtros actuales): {len(df_vista):,}')

        else:
            print(f'  comando desconocido: {op}  (usa "h" para ayuda)')

    print('Chao.')


if __name__ == '__main__':
    main()
