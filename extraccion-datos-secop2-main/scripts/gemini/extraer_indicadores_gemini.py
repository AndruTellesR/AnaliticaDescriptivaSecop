"""
Extracción de indicadores de capacidad financiera/organizacional usando Gemini.

Modelo por defecto: gemini-2.5-flash-lite (Tier 1 — RPD ilimitado, 4K RPM, 4M TPM).

Estrategia:
1. Leer `data/indicadores_pliegos_extraidos.json` para saber qué contratos ya
   fueron procesados.
2. Obtener la lista de consorcios con PDF descargado que aún no se han procesado
   (o que están en estado retryable, ej. error_api).
3. Para cada uno:
   a. Filtrar páginas relevantes del PDF (detección de TOC + clustering de keywords).
   b. Si el filtro no encuentra páginas, FALLBACK: extraer todo el PDF y
      compactarlo (quitar whitespace redundante, headers/footers, líneas de TOC).
   c. Enviar el fragmento a Gemini con schema JSON estructurado.
   d. Clasificar el resultado: ok / error_api (retryable) / error_api_permanente.
4. Guardado incremental al JSON (idempotente).
5. Al finalizar, actualiza automáticamente los parquets (completo + depurado).

Uso:
    python scripts/gemini/extraer_indicadores_gemini.py --n 500
    python scripts/gemini/extraer_indicadores_gemini.py --n 500 --cooldown 0.5
    python scripts/gemini/extraer_indicadores_gemini.py --n 100 --retry-sin-match
    python scripts/gemini/extraer_indicadores_gemini.py --n 50 --modelo gemini-2.0-flash-lite
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
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tqdm import tqdm

# Importar la lógica de filtrado del script hermano
SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
from extraer_indicadores_pliegos import extraer_texto_filtrado  # type: ignore


# ── Configuración ─────────────────────────────────────────────────────────────

RAIZ = Path(__file__).resolve().parent.parent.parent
PLIEGOS_DIR = Path('C:/Users/angel/OneDrive/Escritorio/trabajo dirigido/secop-scraper/storage/pliegos')
DATA_PARQUET  = RAIZ / 'data' / 'contratos_electronicos_obra.parquet'
COMPLETO      = RAIZ / 'data' / 'contratos_adiciones_obra.parquet'
DEPURADO      = RAIZ / 'data' / 'contratos_depurado_modelo.parquet'
JSON_RESULTS  = RAIZ / 'data' / 'indicadores_pliegos_extraidos.json'

# Modelo por defecto: 2.5-flash-lite tiene RPD ilimitado en Tier 1 y es estable
MODELO_DEFAULT = 'gemini-2.5-flash-lite'

# Con Tier 1 (4K RPM, 4M TPM, RPD ilimitado) podemos relajar el rate limit.
# 1.0s ≈ 60 RPM (muy por debajo del límite), cómodo y sin saturar.
COOLDOWN_DEFAULT = 1.0

# Corte de texto que se envía al modelo (caracteres, no tokens)
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
    'liquidez_min':                        'pliego_liquidez_min',
    'endeudamiento_max_pct':               'pliego_endeudamiento_max_pct',
    'cobertura_intereses_min':             'pliego_cobertura_intereses_min',
    'rentabilidad_patrimonio_min_pct':     'pliego_rentabilidad_patrimonio_min_pct',
    'rentabilidad_activo_min_pct':         'pliego_rentabilidad_activo_min_pct',
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
- Si el pliego lista varias alternativas (ej: "nacionales 1.5, extranjeros 2.0"), usa el umbral para nacionales.

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

# Estados finales (no se reintentan). `sin_match` solo se considera final si
# NO se pasa --retry-sin-match. `error_api_permanente` tampoco se reintenta.
ESTADOS_FINALES_BASE = {
    'ok', 'texto_sin_umbrales', 'no_descargado', 'no_pdf',
    'error_pdf', 'error_api_permanente',
}

# Errores transitorios de API que SÍ vale la pena reintentar
ERRORES_API_TRANSITORIOS = (
    'ServiceUnavailable', 'InternalServerError', 'DeadlineExceeded',
    'ResourceExhausted', 'Unavailable', 'Aborted', '503', '500', '504', '429',
)

INDICADOR_LABELS = {
    'liquidez_min':                        'Liquidez mín',
    'endeudamiento_max_pct':               'Endeudamiento máx%',
    'cobertura_intereses_min':             'Cobertura int mín',
    'rentabilidad_patrimonio_min_pct':     'ROE mín%',
    'rentabilidad_activo_min_pct':         'ROA mín%',
    'capital_trabajo_min_pct_presupuesto': 'Cap. trabajo %',
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def log(msg: str = ''):
    """Escribe respetando la barra de tqdm si está activa."""
    tqdm.write(msg)


def sep():
    log('─' * 65)


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


def obtener_contratos_pendientes(n: int, resultados_existentes: dict,
                                  estados_finales: set) -> pd.DataFrame:
    df = pd.read_parquet(DATA_PARQUET)
    consorcios = df[df['es_grupo'] == 'Si']

    pendientes = []
    for _, row in consorcios.iterrows():
        id_c = row['id_contrato']
        prev = resultados_existentes.get(id_c)
        if prev is not None and prev.get('estado', '') in estados_finales:
            continue

        archivos = list(PLIEGOS_DIR.glob(f'{id_c}.*'))
        if not archivos:
            continue
        archivo = archivos[0]
        if archivo.suffix.lower() != '.pdf':
            continue

        pendientes.append({
            'id_contrato':  id_c,
            'archivo':      str(archivo),
            'nombre_pdf':   archivo.name,
            'proveedor':    row.get('proveedor_adjudicado', ''),
            'entidad':      row.get('nombre_entidad', ''),
            'departamento': row.get('departamento', ''),
            'estado_prev':  prev.get('estado', '') if prev else '',
        })
        if len(pendientes) >= n:
            break

    return pd.DataFrame(pendientes)


# ── Extracción de texto ───────────────────────────────────────────────────────

RE_LINEAS_TOC = re.compile(r'^\s*.{3,}?\.{3,}\s*\d+\s*$', re.MULTILINE)
RE_WS_MULTI   = re.compile(r'[ \t]+')
RE_LINEAS_VACIAS = re.compile(r'\n{3,}')
RE_NUMS_PAG   = re.compile(r'^\s*(página\s+)?\d+\s*(de\s+\d+)?\s*$', re.IGNORECASE | re.MULTILINE)


def compactar_texto(texto: str) -> str:
    """
    Reduce tokens manteniendo el contenido relevante:
    - Detecta y elimina headers/footers repetidos (líneas que aparecen >3 veces)
    - Quita líneas tipo "....... 42" (índices/TOC)
    - Quita números de página sueltos
    - Normaliza whitespace múltiple
    - Colapsa líneas vacías consecutivas
    """
    if not texto:
        return ''

    # 1) Quitar líneas TOC tipo "Sección 3 ......... 42"
    texto = RE_LINEAS_TOC.sub('', texto)

    # 2) Quitar números de página sueltos
    texto = RE_NUMS_PAG.sub('', texto)

    # 3) Detectar headers/footers repetidos (líneas cortas que se repiten mucho)
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

    # 4) Normalizar whitespace interno
    texto = RE_WS_MULTI.sub(' ', texto)

    # 5) Colapsar líneas vacías consecutivas
    texto = RE_LINEAS_VACIAS.sub('\n\n', texto)

    return texto.strip()


def extraer_texto_completo_pdf(pdf_path: Path) -> str:
    """Fallback: extrae todo el texto del PDF sin filtrar páginas."""
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


# ── Llamada a Gemini ──────────────────────────────────────────────────────────

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
    """Retorna 'error_api' (retryable) o 'error_api_permanente'."""
    nombre = type(exc).__name__
    mensaje = str(exc)
    for keyword in ERRORES_API_TRANSITORIOS:
        if keyword in nombre or keyword in mensaje:
            return 'error_api'
    return 'error_api_permanente'


# ── Pipeline por contrato ─────────────────────────────────────────────────────

def procesar_uno(client: genai.Client, modelo: str,
                  id_contrato: str, pdf_path: Path) -> dict:
    extr = extraer_texto_filtrado(pdf_path)

    if extr.get('error'):
        return {
            'id_contrato': id_contrato,
            'archivo':     pdf_path.name,
            'estado':      'error_pdf',
            'error':       extr['error'],
            'metodo':      'gemini',
        }

    texto = extr.get('texto', '')
    metodo_texto = 'filtrado'

    # Fallback: si el filtro no encontró páginas relevantes, usar todo el PDF compactado
    if not texto:
        texto_raw = extraer_texto_completo_pdf(pdf_path)
        texto = compactar_texto(texto_raw)
        metodo_texto = 'completo_compactado'
        if not texto:
            return {
                'id_contrato':   id_contrato,
                'archivo':       pdf_path.name,
                'estado':        'sin_match',
                'total_paginas': extr.get('total_paginas', 0),
                'metodo':        'gemini',
            }

    try:
        indicadores = extraer_con_gemini(client, modelo, texto)
    except Exception as e:
        return {
            'id_contrato': id_contrato,
            'archivo':     pdf_path.name,
            'estado':      clasificar_error_api(e),
            'error':       f'{type(e).__name__}: {str(e)[:200]}',
            'metodo':      'gemini',
        }

    if '_parse_error' in indicadores:
        return {
            'id_contrato': id_contrato,
            'archivo':     pdf_path.name,
            'estado':      'error_parse',
            'error':       indicadores['_parse_error'],
            'metodo':      'gemini',
        }

    n_extraidos = sum(1 for v in indicadores.values() if v is not None)

    return {
        'id_contrato':           id_contrato,
        'archivo':               pdf_path.name,
        'estado':                'ok' if n_extraidos > 0 else 'texto_sin_umbrales',
        'total_paginas':         extr.get('total_paginas', 0),
        'paginas_finales':       extr.get('paginas_finales', []),
        'longitud_filtrada':     len(texto),
        'metodo_texto':          metodo_texto,
        'indicadores_extraidos': n_extraidos,
        'metodo':                'gemini',
        **indicadores,
    }


# ── Actualizar parquets ───────────────────────────────────────────────────────

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
    assert len(df_dep) == len(df_full), 'Mismatch de filas entre depurado y completo'
    for col in COLS_PLIEGO:
        df_dep[col] = df_full[col].values
    df_dep.to_parquet(DEPURADO, index=False)

    log(f'  Contratos con indicadores:  {n_ok:,}')
    log(f'  Completo  -> {df_full.shape[0]:,} filas x {df_full.shape[1]} cols')
    log(f'  Depurado  -> {df_dep.shape[0]:,} filas x {df_dep.shape[1]} cols')
    for col in COLS_PLIEGO:
        n_val = df_dep[col].notna().sum()
        log(f'    {col:<52}: {n_val:>5,} ({n_val/len(df_dep)*100:.2f}%)')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=5,
                    help='Numero maximo de contratos a procesar')
    ap.add_argument('--cooldown', type=float, default=COOLDOWN_DEFAULT,
                    help=f'Segundos entre llamadas (default {COOLDOWN_DEFAULT}s)')
    ap.add_argument('--modelo', type=str, default=MODELO_DEFAULT,
                    help=f'Modelo de Gemini (default {MODELO_DEFAULT})')
    ap.add_argument('--retry-sin-match', action='store_true',
                    help='Reintentar contratos sin_match usando fallback de texto completo')
    args = ap.parse_args()

    estados_finales = set(ESTADOS_FINALES_BASE)
    if not args.retry_sin_match:
        estados_finales.add('sin_match')

    load_dotenv(RAIZ / '.env')
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print('ERROR: Falta GEMINI_API_KEY en .env', file=sys.stderr)
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    resultados = cargar_resultados_existentes()
    ya_procesados = len(resultados)

    pendientes = obtener_contratos_pendientes(args.n, resultados, estados_finales)
    total = len(pendientes)

    sep()
    log(f'  Modelo         : {args.modelo}')
    log(f'  Cooldown       : {args.cooldown}s entre llamadas  (~{60/args.cooldown:.0f} RPM max)')
    log(f'  Ya en JSON     : {ya_procesados}')
    log(f'  A procesar hoy : {total}')
    if args.retry_sin_match:
        log(f'  Modo           : retry-sin-match activado')
    sep()

    if total == 0:
        log('Nada por hacer.')
        return

    ok_count = 0
    err_count = 0
    err_transitorio = 0

    with tqdm(total=total, desc='Extrayendo', unit='pdf', ncols=80) as pbar:
        for idx, (_, row) in enumerate(pendientes.iterrows(), start=1):
            id_c       = row['id_contrato']
            pdf_path   = Path(row['archivo'])
            proveedor  = row['proveedor']
            entidad    = row['entidad']
            depto      = row['departamento']
            estado_prev = row['estado_prev']

            log('')
            reintento_txt = f'  (reintento desde: {estado_prev})' if estado_prev else ''
            log(f'[{idx}/{total}]  {id_c}{reintento_txt}')
            log(f'  Proveedor  : {proveedor[:60]}')
            log(f'  Entidad    : {entidad[:60]}')
            log(f'  Depto      : {depto}')
            log(f'  PDF        : {pdf_path.name}')

            t0 = time.time()
            r  = procesar_uno(client, args.modelo, id_c, pdf_path)
            dt = time.time() - t0

            estado = r.get('estado')

            if estado == 'ok':
                ok_count += 1
                n_extr = r.get('indicadores_extraidos', 0)
                metodo_txt = r.get('metodo_texto', '')
                fallback_txt = ' [fallback compactado]' if metodo_txt == 'completo_compactado' else ''
                log(f'  Estado     : ok  ({n_extr}/6 indicadores, {dt:.1f}s){fallback_txt}')
                log('  Indicadores extraidos:')
                for k, label in INDICADOR_LABELS.items():
                    v = r.get(k)
                    marca = f'{v}' if v is not None else '-'
                    log(f'    {label:<26}: {marca}')
            else:
                err_count += 1
                if estado == 'error_api':
                    err_transitorio += 1
                metodo_txt = r.get('metodo_texto', '')
                fallback_txt = ' [fallback compactado]' if metodo_txt == 'completo_compactado' else ''
                log(f'  Estado     : {estado}  ({dt:.1f}s){fallback_txt}')
                if r.get('error'):
                    log(f'  Error      : {r["error"][:120]}')

            resultados[id_c] = r
            guardar_resultados(resultados)
            log(f'  JSON       : guardado ({len(resultados)} entradas)')

            pbar.update(1)
            pbar.set_postfix({'ok': ok_count, 'err': err_count})

            if idx < total:
                tiempo_restante = max(0, args.cooldown - dt)
                if tiempo_restante > 0:
                    time.sleep(tiempo_restante)

    # ── Resumen extraccion ──
    log('')
    sep()
    log(f'  EXTRACCION COMPLETADA')
    log(f'  Procesados       : {total}')
    log(f'  OK               : {ok_count}')
    log(f'  Errores (total)  : {err_count}')
    log(f'     transitorios  : {err_transitorio}  (se reintentan en la proxima corrida)')
    log(f'  JSON total       : {len(resultados)} contratos')
    sep()

    # ── Actualizar parquets ──
    log('')
    log('  Actualizando datasets (parquets)...')
    poblar_datasets(resultados)
    sep()
    log(f'  Parquets en: {RAIZ / "data"}')
    sep()


if __name__ == '__main__':
    main()
