"""
scraper_pliegos_poc.py -- PoC: descarga pliegos de condiciones desde SECOP II
==============================================================================
Lee contratos_electronicos_obra.parquet, filtra "Licitacion publica Obra Publica",
toma los primeros N registros, navega a cada URL con Playwright, resuelve el
reCAPTCHA con CapSolver, busca la ultima coincidencia de documento que contenga
"pliego" en la tabla de documentacion, y descarga el PDF.

Uso:
    python scripts/scraper_pliegos_poc.py
    python scripts/scraper_pliegos_poc.py --limit 10
"""

import argparse
import asyncio
import os
import re
import random
import time

import pandas as pd
import requests
from playwright.async_api import async_playwright
from rich.console import Console

console = Console()

PARQUET = "data/contratos_electronicos_obra.parquet"
OUTPUT_DIR = "data/pliegos"
MODALIDAD = "Licitaci\u00f3n p\u00fablica Obra Publica"
BASE_URL = "https://community.secop.gov.co"

# reCAPTCHA de SECOP II (distinto al del RUP)
SECOP_SITE_KEY = "6LcMmakZAAAAAB157Q90hORUGtNd790TCws4vBNw"
SECOP_SITE_URL = "https://community.secop.gov.co/"

# CapSolver
CAPSOLVER_API_KEY = os.getenv("CAPSOLVER_API_KEY", "")
CAPSOLVER_URL = "https://api.capsolver.com"
MAX_CAPTCHA_RETRIES = 3

DELAY_MIN = 2.0
DELAY_MAX = 4.0


# -- CapSolver ----------------------------------------------------------------

def _resolver_captcha_una_vez() -> str:
    payload = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL": SECOP_SITE_URL,
            "websiteKey": SECOP_SITE_KEY,
        },
    }
    resp = requests.post(f"{CAPSOLVER_URL}/createTask", json=payload, timeout=30)
    data = resp.json()

    if data.get("errorId") and data.get("errorId") != 0:
        return ""

    task_id = data.get("taskId")
    if not task_id:
        return ""

    for _ in range(120):
        time.sleep(1)
        poll = requests.post(
            f"{CAPSOLVER_URL}/getTaskResult",
            json={"clientKey": CAPSOLVER_API_KEY, "taskId": task_id},
            timeout=30,
        ).json()

        status = poll.get("status")
        if status == "ready":
            return poll.get("solution", {}).get("gRecaptchaResponse", "")
        elif status == "failed" or poll.get("errorId"):
            return ""

    return ""


def resolver_captcha() -> str:
    for intento in range(1, MAX_CAPTCHA_RETRIES + 1):
        console.print(f"  CapSolver intento {intento}/{MAX_CAPTCHA_RETRIES}...", end="")
        token = _resolver_captcha_una_vez()
        if token:
            console.print(f" OK ({len(token)} chars)")
            return token
        console.print(" fallo")
    console.print(f"  CapSolver: {MAX_CAPTCHA_RETRIES} intentos fallidos.")
    return ""


# -- Utilidades ----------------------------------------------------------------

def sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:150]


# -- Resolver CAPTCHA en el navegador ------------------------------------------

async def resolver_captcha_secop(page) -> bool:
    """
    Detecta si la pagina actual es la pagina de captcha de SECOP.
    Si lo es, resuelve el captcha con CapSolver y navega al CaptchaCheck.
    Retorna True si se resolvio (o no habia captcha), False si fallo.
    """
    # Verificar si estamos en la pagina de captcha
    current_url = page.url
    is_captcha = "GoogleReCaptcha" in current_url

    if not is_captcha:
        # Verificar por contenido (a veces la URL no cambia)
        has_captcha = await page.query_selector("#divGoogleReCaptcha")
        if not has_captcha:
            return True  # No hay captcha, todo bien

    console.print("  reCAPTCHA detectado - resolviendo con CapSolver...")

    # Extraer el mkey de la pagina de captcha
    mkey = await page.evaluate("""() => {
        const btn = document.getElementById('btnCaptchaCheckButton');
        if (!btn) return null;
        const onclick = btn.getAttribute('onclick') || '';
        const m = onclick.match(/mkey=([a-f0-9_]+)/);
        return m ? m[1] : null;
    }""")

    if not mkey:
        console.print("  No se pudo extraer mkey de la pagina de captcha")
        return False

    console.print(f"  mkey: {mkey}")

    # Resolver el captcha
    token = resolver_captcha()
    if not token:
        return False

    # Navegar al CaptchaCheck con el token
    check_url = f"{BASE_URL}/Public/Common/GoogleReCaptcha/CaptchaCheck?responseKey={token}&mkey={mkey}"
    console.print("  Enviando token a CaptchaCheck...")

    await page.goto(check_url, wait_until="domcontentloaded", timeout=60000)
    await asyncio.sleep(2)

    # Verificar que ya no estamos en captcha
    new_url = page.url
    if "GoogleReCaptcha" in new_url:
        console.print("  Aun en pagina de captcha despues del check")
        return False

    console.print("  CAPTCHA resuelto - sesion activa")
    return True


# -- Extraer documentos -------------------------------------------------------

async def extraer_documentos(page, url: str, id_contrato: str, idx: int, total: int):
    console.print(f"\n  [{idx}/{total}] {id_contrato}")
    console.print(f"    URL: {url}")

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(2)

        # Verificar si hay captcha
        if "GoogleReCaptcha" in page.url or await page.query_selector("#divGoogleReCaptcha"):
            ok = await resolver_captcha_secop(page)
            if not ok:
                console.print("    No se pudo resolver el CAPTCHA")
                return None
            # Reintentar la URL original despues del captcha
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(3)

        # Esperar a que la tabla de documentos se renderice
        try:
            await page.wait_for_selector("#grdGridDocumentList_tbl", timeout=30000)
        except Exception:
            console.print("    Tabla no encontrada - esperando networkidle...")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(3)
            try:
                await page.wait_for_selector("#grdGridDocumentList_tbl", timeout=15000)
            except Exception:
                # Tomar screenshot para debug
                ss_path = f"debug_fail_{id_contrato}.png"
                await page.screenshot(path=ss_path)
                console.print(f"    Tabla de documentos no cargo (screenshot: {ss_path})")
                return None

        # Extraer nombres de documentos y sus links de descarga
        doc_info = await page.evaluate("""() => {
            const rows = document.querySelectorAll(
                '#grdGridDocumentList_tbl tbody tr:not(#grdGridDocumentList_header)'
            );
            const docs = [];
            for (const row of rows) {
                const span = row.querySelector('span.VortalSpan');
                const link = row.querySelector('a[onclick*="DownloadFile"]');
                if (span && link) {
                    docs.push({
                        name: span.textContent.trim(),
                        linkId: link.id,
                    });
                }
            }
            return docs;
        }""")

        if not doc_info:
            console.print("    No se encontraron documentos en la tabla")
            return None

        console.print(f"    Documentos encontrados: {len(doc_info)}")
        for d in doc_info:
            console.print(f"      - {d['name']}")

        # Buscar la ULTIMA coincidencia que contenga "pliego" (case insensitive)
        pliego_docs = [d for d in doc_info if "pliego" in d["name"].lower()]

        if not pliego_docs:
            console.print("    Ningun documento contiene 'pliego'")
            return None

        target = pliego_docs[-1]
        console.print(f"    >> Seleccionado: {target['name']}")

        # Hacer clic en el boton de descarga y capturar el archivo
        link_el = page.locator(f"#{target['linkId']}")

        console.print(f"    Descargando via clic...")

        try:
            async with page.expect_download(timeout=60000) as download_info:
                await link_el.click()
            download = await download_info.value

            # Nombre del archivo: id_contrato + nombre original
            suggested = download.suggested_filename or target["name"]
            filename = f"{id_contrato}_{sanitize_filename(suggested)}"
            filepath = os.path.join(OUTPUT_DIR, filename)

            await download.save_as(filepath)
            size_kb = os.path.getsize(filepath) / 1024

            console.print(f"    OK - {size_kb:.1f} KB -> {filepath}")
            return filepath

        except Exception as dl_err:
            console.print(f"    Descarga fallida: {dl_err}")
            return None

    except Exception as e:
        console.print(f"    Error: {e}")
        return None


# -- Main ----------------------------------------------------------------------

async def run(limit: int):
    df = pd.read_parquet(PARQUET)
    lp = df[df["modalidad_de_contratacion"] == MODALIDAD].head(limit)
    total = len(lp)

    console.print("Scraper Pliegos PoC")
    console.print(f"  Registros Licitacion publica Obra Publica: {len(df[df['modalidad_de_contratacion'] == MODALIDAD]):,}")
    console.print(f"  Procesando: {total}")

    # Balance CapSolver
    balance = requests.post(
        f"{CAPSOLVER_URL}/getBalance",
        json={"clientKey": CAPSOLVER_API_KEY},
        timeout=10,
    ).json().get("balance", 0)
    console.print(f"  CapSolver balance: ${balance:.4f} USD")
    if balance <= 0:
        console.print("  Sin saldo en CapSolver.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()

        # Visitar SECOP para que salte el captcha y resolverlo UNA vez
        console.print("\n  Inicializando sesion SECOP II...")
        first_url = lp.iloc[0]["urlproceso"]
        await page.goto(first_url, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(2)

        # Resolver captcha inicial
        captcha_ok = await resolver_captcha_secop(page)
        if not captcha_ok:
            console.print("  No se pudo resolver el CAPTCHA inicial")
            await browser.close()
            return
        console.print("  Sesion SECOP II activa\n")

        ok_count = 0
        fail_count = 0

        for i, (_, row) in enumerate(lp.iterrows(), 1):
            url = row["urlproceso"]
            id_contrato = str(
                row.get("id_contrato", row.get("proceso_de_compra", f"registro_{i}"))
            )

            if i > 1:
                delay = random.uniform(DELAY_MIN, DELAY_MAX)
                await asyncio.sleep(delay)

            result = await extraer_documentos(page, url, id_contrato, i, total)
            if result:
                ok_count += 1
            else:
                fail_count += 1

        await browser.close()

    # Resumen
    console.print(f"\n=== RESUMEN ===")
    console.print(f"  Descargados: {ok_count}/{total}")
    console.print(f"  Fallidos:    {fail_count}/{total}")
    console.print(f"  Directorio:  {OUTPUT_DIR}/")


def main():
    parser = argparse.ArgumentParser(description="PoC: descarga pliegos de SECOP II")
    parser.add_argument(
        "--limit", type=int, default=5, help="Registros a procesar (default: 5)"
    )
    args = parser.parse_args()
    asyncio.run(run(args.limit))


if __name__ == "__main__":
    main()
