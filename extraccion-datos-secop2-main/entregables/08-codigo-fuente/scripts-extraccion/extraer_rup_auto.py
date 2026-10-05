"""
extraer_rup_auto.py — Extracción automática RUP con CapSolver + Playwright
==========================================================================
Lee proveedores_rup.parquet (procesar=True, procesado=False), consulta la API
del RUP y escribe los resultados de vuelta al parquet.

Estrategia anti-bloqueo:
  - Delay aleatorio entre peticiones (2-4s)
  - Cooldown de 5 min cada N NITs (configurable)
  - Auto-brake: 3 errores consecutivos → pausa 15 min
  - Token CAPTCHA se reutiliza hasta que expire (400/403)
  - Resume automático: solo procesa procesado=False

Uso:
    python scripts/extraer_rup_auto.py
    python scripts/extraer_rup_auto.py --limit 500
    python scripts/extraer_rup_auto.py --limit 500 --cooldown-every 300
"""

import argparse
import asyncio
import os
import random
import time

import pandas as pd
import requests
from playwright.async_api import async_playwright
from rich.console import Console

console = Console()

# ── Configuración ────────────────────────────────────────────────────────────
CAPSOLVER_API_KEY = os.getenv("CAPSOLVER_API_KEY", "")
CAPSOLVER_URL     = "https://api.capsolver.com"
RUP_SITE_KEY      = "6LfssZMrAAAAAEHbwOrGkKzKR9TFnmZFBwkQqw73"
RUP_SITE_URL      = "https://ruppro.colombiacompra.gov.co/"
RUP_API_URL       = "https://ruppro.colombiacompra.gov.co/msrup/api/v1/consultas/nit/completo"
PARQUET           = "data/proveedores_rup.parquet"

DELAY_MIN         = 2.5  # segundos entre peticiones
DELAY_MAX         = 4.0
COOLDOWN_SECS     = 180  # 3 minutos
BRAKE_PAUSE       = 900  # 15 minutos
MAX_ERRORES_SEGUIDOS = 3
MAX_CAPTCHA_RETRIES  = 3


# ── CapSolver ────────────────────────────────────────────────────────────────

def _resolver_captcha_una_vez() -> str:
    payload = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL": RUP_SITE_URL,
            "websiteKey": RUP_SITE_KEY,
        }
    }
    resp = requests.post(f"{CAPSOLVER_URL}/createTask", json=payload, timeout=30)
    data = resp.json()

    if data.get("errorId") and data.get("errorId") != 0:
        return ""

    task_id = data.get("taskId")
    if not task_id:
        return ""

    for _ in range(60):
        time.sleep(1)
        poll = requests.post(f"{CAPSOLVER_URL}/getTaskResult", json={
            "clientKey": CAPSOLVER_API_KEY,
            "taskId": task_id,
        }, timeout=30).json()

        status = poll.get("status")
        if status == "ready":
            return poll.get("solution", {}).get("gRecaptchaResponse", "")
        elif status == "failed" or poll.get("errorId"):
            return ""

    return ""


def resolver_captcha() -> str:
    for intento in range(1, MAX_CAPTCHA_RETRIES + 1):
        console.print(f"  [dim]CapSolver intento {intento}/{MAX_CAPTCHA_RETRIES}...[/dim]", end="")
        token = _resolver_captcha_una_vez()
        if token:
            console.print(f" [green]OK[/green] ({len(token)} chars)")
            return token
        console.print(" [yellow]falló[/yellow]")

    console.print(f"  [red]CapSolver: {MAX_CAPTCHA_RETRIES} intentos fallidos.[/red]")
    return ""


# ── Parquet I/O ──────────────────────────────────────────────────────────────

def cargar_pendientes(limit: int | None) -> tuple[pd.DataFrame, list[str]]:
    df = pd.read_parquet(PARQUET)
    pendientes = df[(df["procesar"]) & (~df["procesado"])]
    nits = pendientes["nit"].tolist()
    if limit:
        nits = nits[:limit]

    total = len(df)
    ya = df["procesado"].sum()
    no_proc = (~df["procesar"]).sum()

    console.print(f"[bold]Dataset:[/bold] {total:,} NITs totales")
    console.print(f"  procesados:     {ya:,}")
    console.print(f"  no procesar:    {no_proc:,}")
    console.print(f"  [bold]pendientes:     {len(nits):,}[/bold]")
    return df, nits


def guardar_resultado(df: pd.DataFrame, nit: str, data: dict | None):
    """Escribe el resultado de un NIT en el DataFrame (en memoria)."""
    idx = df.index[df["nit"] == nit]
    if len(idx) == 0:
        return

    i = idx[0]
    df.at[i, "procesado"] = True

    if data is None:
        return

    basico = data.get("informacionBasica") or {}
    df.at[i, "rup_estado"]   = basico.get("estado_matricula", "")
    df.at[i, "rup_tamano"]   = basico.get("codigo_tamano_empresa", "")
    df.at[i, "rup_empleados"] = basico.get("numero_empleados", "")
    df.at[i, "rup_municipio"] = basico.get("municipio_comercial", "")
    df.at[i, "rup_sanciones"] = len(basico.get("sanciones") or [])
    df.at[i, "rup_multas"]    = len(basico.get("multas") or [])

    detalle = data.get("informacionDetalle") or {}
    df.at[i, "rup_inhabilidad"] = detalle.get("inhabilidad", "")

    fin_list = basico.get("informacionFinanciera") or []
    if fin_list:
        fin = fin_list[0]
        df.at[i, "rup_ano_financiero"]    = fin.get("ano_informacion_financiera", "")
        df.at[i, "rup_activo_total"]      = fin.get("activo_total", "")
        df.at[i, "rup_patrimonio"]        = fin.get("patrimonio_neto", "")
        df.at[i, "rup_ingresos"]          = fin.get("ingresos_actividad_ordinaria", "")
        df.at[i, "rup_utilidad_neta"]     = fin.get("resultado_del_periodo", "")

        def to_f(v):
            try:
                return float(str(v).replace(",", "."))
            except Exception:
                return None

        ac = to_f(fin.get("activo_corriente"))
        pc = to_f(fin.get("pasivo_corriente"))
        at = to_f(fin.get("activo_total"))
        pt = to_f(fin.get("pasivo_total"))
        pn = to_f(fin.get("patrimonio_neto"))
        uo = to_f(fin.get("utilidad_perdida_operacional"))
        un = to_f(fin.get("resultado_del_periodo"))
        gi = to_f(fin.get("gastos_intereses", "0"))

        df.at[i, "rup_idx_liquidez"]       = round(ac / pc, 4) if (ac and pc and pc != 0) else None
        df.at[i, "rup_idx_endeudamiento"]  = round(pt / at, 4) if (at and pt and at != 0) else None
        df.at[i, "rup_idx_cobertura"]      = round(uo / gi, 4) if (uo and gi and gi != 0) else None
        df.at[i, "rup_rent_patrimonio"]    = round(un / pn, 4) if (un and pn and pn != 0) else None
        df.at[i, "rup_rent_activo"]        = round(un / at, 4) if (un and at and at != 0) else None


def persistir(df: pd.DataFrame):
    df.to_parquet(PARQUET, index=False)


# ── Consulta RUP via Playwright ──────────────────────────────────────────────

async def consultar_rup(page, nit: str, captcha_token: str) -> dict:
    try:
        resp = await page.evaluate(f"""async () => {{
            const r = await fetch('{RUP_API_URL}', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{nit: '{nit}', recaptchaToken: '{captcha_token}'}})
            }});
            let body;
            try {{ body = await r.json(); }} catch(e) {{ body = {{success: false, message: 'No JSON: ' + r.statusText}}; }}
            return {{ status: r.status, body: body }};
        }}""")
        return resp
    except Exception as e:
        return {"status": 0, "body": {"success": False, "message": str(e)}}


# ── Main ─────────────────────────────────────────────────────────────────────

async def run(limit: int | None, cooldown_every: int):
    # Balance CapSolver
    balance = requests.post(f"{CAPSOLVER_URL}/getBalance", json={
        "clientKey": CAPSOLVER_API_KEY,
    }, timeout=10).json().get("balance", 0)
    console.print(f"[bold]CapSolver balance:[/bold] ${balance:.4f} USD")
    if balance <= 0:
        console.print("[red]Sin saldo en CapSolver.[/red]")
        return

    # Cargar datos
    df, nits = cargar_pendientes(limit)
    total = len(nits)
    if total == 0:
        console.print("[green]No hay NITs pendientes.[/green]")
        return

    # Navegador
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await (await browser.new_context()).new_page()
        await page.goto(RUP_SITE_URL, wait_until="domcontentloaded")
        console.print("[bold]Navegador Playwright listo[/bold]")

        ok_total = 0
        fail_total = 0
        captchas_usados = 0
        errores_seguidos = 0
        token_usos = 0

        # Primer CAPTCHA
        console.print("\n[bold]Resolviendo CAPTCHA #1...[/bold]")
        token = resolver_captcha()
        if not token:
            await browser.close()
            return
        captchas_usados = 1

        for i, nit in enumerate(nits, 1):
            # ── Cooldown periódico ───────────────────────────────────
            if (i - 1) > 0 and (i - 1) % cooldown_every == 0:
                console.print(f"\n[yellow]⏸ Cooldown {COOLDOWN_SECS // 60} min después de {i-1} NITs...[/yellow]")
                persistir(df)
                console.print(f"  [dim]Parquet guardado ({df['procesado'].sum():,} procesados)[/dim]")
                await asyncio.sleep(COOLDOWN_SECS)

            # ── Delay aleatorio ──────────────────────────────────────
            delay = random.uniform(DELAY_MIN, DELAY_MAX)
            await asyncio.sleep(delay)

            t0 = time.time()
            console.print(f"  [{i}/{total}] NIT: [cyan]{nit}[/cyan] ... ", end="")

            resp = await consultar_rup(page, nit, token)
            status = resp.get("status", 0)
            body   = resp.get("body", {})
            elapsed = time.time() - t0

            # ── 200 OK ───────────────────────────────────────────────
            if status == 200 and body.get("success") and body.get("data"):
                guardar_resultado(df, nit, body["data"])
                ok_total += 1
                token_usos += 1
                errores_seguidos = 0
                nombre = body["data"].get("informacionBasica", {}).get("razon_social", "?")
                console.print(f"[green]OK[/green] ({elapsed:.1f}s) — {nombre}")

            # ── 200 pero sin data (NIT no encontrado en RUP) ─────────
            elif status == 200 and body.get("success") and not body.get("data"):
                guardar_resultado(df, nit, None)
                fail_total += 1
                token_usos += 1
                errores_seguidos = 0
                console.print(f"[dim]NO REGISTRADO[/dim] ({elapsed:.1f}s)")

            # ── 200 pero success=false (NIT no existe en RUP) ────────
            elif status == 200 and not body.get("success"):
                guardar_resultado(df, nit, None)
                fail_total += 1
                token_usos += 1
                errores_seguidos = 0
                msg = body.get("message", "sin mensaje")
                console.print(f"[dim]NO ENCONTRADO[/dim] ({elapsed:.1f}s) — {msg}")

            # ── 400/403: token expirado ──────────────────────────────
            elif status in (400, 403):
                console.print(f"[yellow]TOKEN EXPIRADO[/yellow] (duró {token_usos} consultas)")
                console.print(f"  [bold]Resolviendo CAPTCHA #{captchas_usados + 1}...[/bold]")
                token = resolver_captcha()
                if not token:
                    console.print("[red]No se pudo resolver CAPTCHA — terminando.[/red]")
                    break
                captchas_usados += 1
                token_usos = 0

                # Reintentar este NIT
                resp = await consultar_rup(page, nit, token)
                status = resp.get("status", 0)
                body   = resp.get("body", {})

                if status == 200 and body.get("success") and body.get("data"):
                    guardar_resultado(df, nit, body["data"])
                    ok_total += 1
                    token_usos += 1
                    errores_seguidos = 0
                    nombre = body["data"].get("informacionBasica", {}).get("razon_social", "?")
                    console.print(f"  [green]OK (reintento)[/green] — {nombre}")
                elif status == 200 and body.get("success"):
                    guardar_resultado(df, nit, None)
                    fail_total += 1
                    token_usos += 1
                    errores_seguidos = 0
                    console.print(f"  [dim]NO REGISTRADO (reintento)[/dim]")
                elif status == 200 and not body.get("success"):
                    guardar_resultado(df, nit, None)
                    fail_total += 1
                    token_usos += 1
                    errores_seguidos = 0
                    msg = body.get("message", "sin mensaje")
                    console.print(f"  [dim]NO ENCONTRADO (reintento)[/dim] — {msg}")
                else:
                    fail_total += 1
                    errores_seguidos += 1
                    console.print(f"  [red]FALLÓ (reintento)[/red] — {body.get('message', f'HTTP {status}')}")

            # ── NIT no encontrado (status != 200, ej. 404) ───────────
            elif "no se encontr" in str(body.get("message", "")).lower():
                guardar_resultado(df, nit, None)
                fail_total += 1
                token_usos += 1
                errores_seguidos = 0
                console.print(f"[dim]NO ENCONTRADO[/dim] ({elapsed:.1f}s) — {body.get('message', '')}")

            # ── Otro error real (NO marcar procesado → se reintenta) ──
            else:
                fail_total += 1
                token_usos += 1
                errores_seguidos += 1
                console.print(f"[red]ERROR[/red] ({elapsed:.1f}s) HTTP {status} — {body.get('message', '?')}")

            # ── Auto-brake ───────────────────────────────────────────
            if errores_seguidos >= MAX_ERRORES_SEGUIDOS:
                console.print(f"\n[red bold]⚠ {MAX_ERRORES_SEGUIDOS} errores seguidos — pausa {BRAKE_PAUSE // 60} min[/red bold]")
                persistir(df)
                await asyncio.sleep(BRAKE_PAUSE)
                errores_seguidos = 0

            # ── Guardar cada 50 NITs ─────────────────────────────────
            if i % 50 == 0:
                persistir(df)

        await browser.close()

    # Guardar final
    persistir(df)

    # Reporte
    balance_final = requests.post(f"{CAPSOLVER_URL}/getBalance", json={
        "clientKey": CAPSOLVER_API_KEY,
    }, timeout=10).json().get("balance", 0)

    procesados_total = df["procesado"].sum()
    console.print(f"\n[bold]═══ RESUMEN ═══[/bold]")
    console.print(f"  Sesión:      {ok_total} OK | {fail_total} fallidos de {total}")
    console.print(f"  CAPTCHAs:    {captchas_usados}")
    console.print(f"  Costo:       ${balance - balance_final:.4f} USD (saldo: ${balance_final:.4f})")
    console.print(f"  Progreso:    {procesados_total:,} / {len(df):,} procesados ({procesados_total/len(df)*100:.1f}%)")
    console.print(f"  Parquet:     {PARQUET}")


def main():
    parser = argparse.ArgumentParser(description="Extracción RUP automática — lee/escribe proveedores_rup.parquet")
    parser.add_argument("--limit", type=int, default=None,
                        help="Máximo de NITs a procesar en esta sesión (default: todos los pendientes)")
    parser.add_argument("--cooldown-every", type=int, default=500,
                        help="Pausa de cooldown cada N NITs (default: 500)")
    args = parser.parse_args()

    asyncio.run(run(args.limit, args.cooldown_every))


if __name__ == "__main__":
    main()
