"""
Extraccion masiva de indicadores usando la Batch API de Gemini.

La Batch API procesa cientos/miles de requests de forma asincrona (tarda minutos
a unas pocas horas) y cobra ~50% menos que la API sincrona. Cola por modelo
para gemini-2.5-flash-lite en Tier 1: 10M tokens -- suficiente para ~500 PDFs
a la vez.

Subcomandos:
    submit  --n N            Prepara y envia un batch de N contratos pendientes.
    status                   Muestra el estado de todos los batches registrados.
    collect                  Descarga resultados de batches completados y
                             actualiza el JSON + parquets.
    cancel <job_name>        Cancela un batch en curso.

Uso tipico:
    # Dia 0: enviar
    python scripts/gemini/extraer_indicadores_gemini_batch.py submit --n 400

    # Dia 0 o 1 (esperar):
    python scripts/gemini/extraer_indicadores_gemini_batch.py status

    # Cuando diga SUCCEEDED:
    python scripts/gemini/extraer_indicadores_gemini_batch.py collect
"""

import argparse
import json
import os
import sys
import time
import tempfile
from datetime import datetime
from pathlib import Path

import pandas as pd
import pdfplumber
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tqdm import tqdm

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
from extraer_indicadores_pliegos import extraer_texto_filtrado  # type: ignore

# Reusar constantes y helpers del script sincrono
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extraer_indicadores_gemini import (  # type: ignore
    PLIEGOS_DIR, DATA_PARQUET, COMPLETO, DEPURADO, JSON_RESULTS,
    COLS_PLIEGO, MAPA_COLS, PROMPT_INSTRUCCIONES, SCHEMA_INDICADORES,
    ESTADOS_FINALES_BASE, MAX_CHARS_TEXTO,
    compactar_texto, extraer_texto_completo_pdf, poblar_datasets,
    cargar_resultados_existentes, guardar_resultados,
)


# ── Configuracion ─────────────────────────────────────────────────────────────

RAIZ = Path(__file__).resolve().parent.parent.parent
BATCH_JOBS_FILE = RAIZ / 'data' / 'batch_jobs.json'
MODELO_DEFAULT  = 'gemini-2.5-flash-lite'
MAX_BATCH_SIZE  = 400  # Tier 1 tiene 10M tokens en cola; 400*20K = 8M (margen)


# ── Estado de jobs ────────────────────────────────────────────────────────────

def cargar_jobs() -> list[dict]:
    if not BATCH_JOBS_FILE.exists():
        return []
    with BATCH_JOBS_FILE.open(encoding='utf-8') as f:
        return json.load(f)


def guardar_jobs(jobs: list[dict]):
    BATCH_JOBS_FILE.write_text(
        json.dumps(jobs, ensure_ascii=False, indent=2, default=str),
        encoding='utf-8'
    )


# ── Preparar requests del batch ───────────────────────────────────────────────

def construir_request(id_contrato: str, texto: str) -> dict:
    """Construye el formato de request para Batch API."""
    prompt = PROMPT_INSTRUCCIONES + texto[:MAX_CHARS_TEXTO] + '\n---'
    return {
        'key': id_contrato,
        'request': {
            'contents': [
                {'parts': [{'text': prompt}], 'role': 'user'}
            ],
            'generation_config': {
                'response_mime_type': 'application/json',
                'response_schema': SCHEMA_INDICADORES,
                'temperature': 0.0,
            },
        },
    }


def preparar_requests(pendientes_df: pd.DataFrame) -> tuple[list[dict], list[dict]]:
    """
    Para cada contrato: extrae texto (filtrado o fallback compactado).
    Retorna (requests_batch, resultados_directos) donde resultados_directos
    son los que no van al batch (error_pdf, sin_match).
    """
    requests_batch = []
    resultados_directos = {}

    for _, row in tqdm(list(pendientes_df.iterrows()), desc='Extrayendo texto',
                        unit='pdf', ncols=80):
        id_c = row['id_contrato']
        pdf_path = Path(row['archivo'])

        extr = extraer_texto_filtrado(pdf_path)

        if extr.get('error'):
            resultados_directos[id_c] = {
                'id_contrato': id_c,
                'archivo':     pdf_path.name,
                'estado':      'error_pdf',
                'error':       extr['error'],
                'metodo':      'gemini_batch',
            }
            continue

        texto = extr.get('texto', '')
        metodo_texto = 'filtrado'

        if not texto:
            texto_raw = extraer_texto_completo_pdf(pdf_path)
            texto = compactar_texto(texto_raw)
            metodo_texto = 'completo_compactado'
            if not texto:
                resultados_directos[id_c] = {
                    'id_contrato':   id_c,
                    'archivo':       pdf_path.name,
                    'estado':        'sin_match',
                    'total_paginas': extr.get('total_paginas', 0),
                    'metodo':        'gemini_batch',
                }
                continue

        req = construir_request(id_c, texto)
        # Guardar metadata para el collect
        req['_meta'] = {
            'archivo':           pdf_path.name,
            'total_paginas':     extr.get('total_paginas', 0),
            'paginas_finales':   extr.get('paginas_finales', []),
            'longitud_filtrada': len(texto),
            'metodo_texto':      metodo_texto,
        }
        requests_batch.append(req)

    return requests_batch, resultados_directos


# ── Subcomando: SUBMIT ────────────────────────────────────────────────────────

def cmd_submit(client: genai.Client, args):
    print('─' * 65)
    print('  SUBMIT BATCH')
    print('─' * 65)

    if args.n > MAX_BATCH_SIZE:
        print(f'  Reduciendo n={args.n} a {MAX_BATCH_SIZE} (cap por cola de tokens en Tier 1)')
        args.n = MAX_BATCH_SIZE

    resultados = cargar_resultados_existentes()
    estados_finales = set(ESTADOS_FINALES_BASE)
    if not args.retry_sin_match:
        estados_finales.add('sin_match')

    # Marcar tambien como "no pendiente" los que estan en cola de otros batches
    jobs = cargar_jobs()
    ids_en_batches_activos = set()
    for j in jobs:
        if not j.get('completed'):
            ids_en_batches_activos.update(j.get('ids', []))

    # Obtener pendientes
    df = pd.read_parquet(DATA_PARQUET)
    consorcios = df[df['es_grupo'] == 'Si']
    pendientes = []
    for _, row in consorcios.iterrows():
        id_c = row['id_contrato']
        if id_c in ids_en_batches_activos:
            continue
        prev = resultados.get(id_c)
        if prev is not None and prev.get('estado', '') in estados_finales:
            continue
        archivos = list(PLIEGOS_DIR.glob(f'{id_c}.*'))
        if not archivos or archivos[0].suffix.lower() != '.pdf':
            continue
        pendientes.append({'id_contrato': id_c, 'archivo': str(archivos[0])})
        if len(pendientes) >= args.n:
            break

    if not pendientes:
        print('  Nada por enviar.')
        return

    df_pend = pd.DataFrame(pendientes)
    print(f'  Contratos a incluir: {len(df_pend)}')
    print(f'  Modelo: {args.modelo}')
    print()

    print('Paso 1/3: extrayendo texto de los PDFs...')
    requests_batch, resultados_directos = preparar_requests(df_pend)
    print(f'  Requests listos para batch: {len(requests_batch)}')
    print(f'  Resultados directos (no requieren LLM): {len(resultados_directos)}')

    # Guardar resultados directos (error_pdf, sin_match) ahora mismo
    if resultados_directos:
        for id_c, r in resultados_directos.items():
            resultados[id_c] = r
        guardar_resultados(resultados)
        print(f'  JSON actualizado con {len(resultados_directos)} resultados directos.')

    if not requests_batch:
        print('  No hay requests para enviar al batch.')
        return

    # Paso 2: escribir JSONL (sin _meta) y guardar meta separado
    print()
    print('Paso 2/3: subiendo archivo JSONL a Gemini...')
    meta_por_key = {r['key']: r.pop('_meta') for r in requests_batch}

    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.jsonl', delete=False, encoding='utf-8'
    ) as tmp:
        for req in requests_batch:
            tmp.write(json.dumps(req, ensure_ascii=False) + '\n')
        jsonl_path = tmp.name

    try:
        uploaded = client.files.upload(
            file=jsonl_path,
            config=types.UploadFileConfig(
                display_name=f'batch_pliegos_{datetime.now():%Y%m%d_%H%M%S}',
                mime_type='application/jsonl',
            ),
        )
        print(f'  Archivo subido: {uploaded.name} ({uploaded.size_bytes or 0:,} bytes)')
    finally:
        try:
            os.unlink(jsonl_path)
        except OSError:
            pass

    # Paso 3: crear el batch job
    print()
    print('Paso 3/3: creando batch job...')
    display_name = f'pliegos_{datetime.now():%Y%m%d_%H%M%S}'
    batch_job = client.batches.create(
        model=args.modelo,
        src=uploaded.name,
        config=types.CreateBatchJobConfig(display_name=display_name),
    )
    print(f'  Batch creado: {batch_job.name}')
    print(f'  Estado inicial: {batch_job.state}')

    # Guardar en registro local
    jobs.append({
        'job_name':     batch_job.name,
        'file_name':    uploaded.name,
        'display_name': display_name,
        'modelo':       args.modelo,
        'n_requests':   len(requests_batch),
        'ids':          list(meta_por_key.keys()),
        'meta_por_id':  meta_por_key,
        'created_at':   datetime.now().isoformat(),
        'status_last_seen': str(batch_job.state),
        'completed':    False,
    })
    guardar_jobs(jobs)
    print()
    print('─' * 65)
    print(f'  Batch enviado. Ejecuta:')
    print(f'    python scripts/gemini/extraer_indicadores_gemini_batch.py status')
    print(f'  para ver el progreso, y luego:')
    print(f'    python scripts/gemini/extraer_indicadores_gemini_batch.py collect')
    print('─' * 65)


# ── Subcomando: STATUS ────────────────────────────────────────────────────────

def _fmt_duracion(segs: float) -> str:
    if segs < 60:
        return f'{segs:.0f}s'
    if segs < 3600:
        return f'{segs/60:.1f}min'
    return f'{segs/3600:.1f}h'


def cmd_status(client: genai.Client, args):
    from datetime import datetime, timezone
    jobs = cargar_jobs()
    if not jobs:
        print('No hay batches registrados.')
        return

    ahora = datetime.now(timezone.utc)

    print('─' * 95)
    print(f'  {"#":>3}  {"display_name":<24}  {"n":>4}  {"estado":<10}  {"fase":<14}  {"stats":<16}')
    print('─' * 95)

    for i, j in enumerate(jobs, start=1):
        if j.get('completed'):
            estado = 'COLLECTED'
            fase = '—'
            stats = '—'
        else:
            try:
                info = client.batches.get(name=j['job_name'])
                estado = str(info.state).replace('JobState.', '').replace('JOB_STATE_', '')

                # Fase: tiempo en PENDING/RUNNING/terminado
                if estado == 'PENDING':
                    creado = info.create_time or ahora
                    fase = f'en cola {_fmt_duracion((ahora - creado).total_seconds())}'
                elif estado == 'RUNNING':
                    inicio = info.start_time or info.create_time or ahora
                    fase = f'corriendo {_fmt_duracion((ahora - inicio).total_seconds())}'
                elif estado in ('SUCCEEDED', 'FAILED'):
                    if info.start_time and info.end_time:
                        dur = (info.end_time - info.start_time).total_seconds()
                    elif info.end_time and info.create_time:
                        dur = (info.end_time - info.create_time).total_seconds()
                    else:
                        dur = 0
                    fase = f'total {_fmt_duracion(dur)}'
                else:
                    fase = '—'

                # Completion stats (solo hay datos cuando termina o durante RUNNING a veces)
                cs = info.completion_stats
                if cs:
                    ok = cs.successful_count or 0
                    ko = cs.failed_count or 0
                    stats = f'{ok} ok / {ko} err'
                else:
                    stats = '—'

                j['status_last_seen'] = str(info.state)
            except Exception as e:
                estado = f'ERR'
                fase = f'{type(e).__name__}'[:14]
                stats = '—'

        print(f'  {i:>3}  {j["display_name"]:<24}  {j["n_requests"]:>4}  {estado:<10}  {fase:<14}  {stats:<16}')

    guardar_jobs(jobs)
    print('─' * 95)
    print('  Nota: la API de Google NO expone progreso en %. Solo PENDING/RUNNING/SUCCEEDED/FAILED.')
    print('        completion_stats (ok/err) aparece solo al finalizar.')


# ── Subcomando: COLLECT ───────────────────────────────────────────────────────

def parsear_respuesta_batch(resp_obj: dict, meta: dict) -> dict:
    """Convierte la respuesta de un request del batch en una fila del JSON."""
    id_c = resp_obj.get('key', '')
    response = resp_obj.get('response', {})
    error = resp_obj.get('error')

    base = {
        'id_contrato':    id_c,
        'archivo':        meta.get('archivo', ''),
        'total_paginas':  meta.get('total_paginas', 0),
        'paginas_finales': meta.get('paginas_finales', []),
        'longitud_filtrada': meta.get('longitud_filtrada', 0),
        'metodo_texto':   meta.get('metodo_texto', ''),
        'metodo':         'gemini_batch',
    }

    if error:
        return {**base, 'estado': 'error_api', 'error': str(error)[:300]}

    # Extraer texto JSON de la respuesta
    try:
        candidates = response.get('candidates', [])
        if not candidates:
            return {**base, 'estado': 'error_parse', 'error': 'sin candidates'}
        text = candidates[0]['content']['parts'][0].get('text', '')
        indicadores = json.loads(text) if text else {}
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return {**base, 'estado': 'error_parse', 'error': f'{type(e).__name__}: {e}'}

    n_extraidos = sum(1 for v in indicadores.values() if v is not None)
    return {
        **base,
        'estado': 'ok' if n_extraidos > 0 else 'texto_sin_umbrales',
        'indicadores_extraidos': n_extraidos,
        **indicadores,
    }


def cmd_collect(client: genai.Client, args):
    jobs = cargar_jobs()
    if not jobs:
        print('No hay batches para recolectar.')
        return

    resultados = cargar_resultados_existentes()
    total_nuevos = 0

    for j in jobs:
        if j.get('completed'):
            continue

        info = client.batches.get(name=j['job_name'])
        estado_str = str(info.state)
        if 'SUCCEEDED' not in estado_str and 'FAILED' not in estado_str:
            print(f'  [{j["display_name"]}] aun no finalizado: {estado_str}')
            continue

        print(f'  [{j["display_name"]}] estado: {estado_str}')

        if 'FAILED' in estado_str:
            err = getattr(info, 'error', None) or 'sin detalles'
            print(f'    Batch fallo: {err}')
            j['completed'] = True
            j['status_last_seen'] = estado_str
            continue

        # Descargar resultados
        dest = info.dest if hasattr(info, 'dest') else None
        if not dest:
            print('    sin destino de resultados; saltando.')
            continue

        result_file_name = getattr(dest, 'file_name', None)
        if not result_file_name:
            print('    no se encontro archivo de resultados; saltando.')
            continue

        print(f'    descargando resultados de {result_file_name}...')
        content_bytes = client.files.download(file=result_file_name)
        content = content_bytes.decode('utf-8') if isinstance(content_bytes, bytes) else str(content_bytes)

        nuevos_en_job = 0
        meta_por_id = j.get('meta_por_id', {})
        for linea in content.splitlines():
            linea = linea.strip()
            if not linea:
                continue
            try:
                obj = json.loads(linea)
            except json.JSONDecodeError:
                continue
            id_c = obj.get('key', '')
            meta = meta_por_id.get(id_c, {})
            fila = parsear_respuesta_batch(obj, meta)
            resultados[id_c] = fila
            nuevos_en_job += 1

        guardar_resultados(resultados)
        total_nuevos += nuevos_en_job
        print(f'    {nuevos_en_job} resultados incorporados al JSON.')

        j['completed'] = True
        j['status_last_seen'] = estado_str
        j['collected_at'] = datetime.now().isoformat()

    guardar_jobs(jobs)

    if total_nuevos == 0:
        print('\nNingun batch nuevo listo para recolectar.')
        return

    print()
    print(f'Total nuevos resultados: {total_nuevos}')
    print('Actualizando datasets (parquets)...')
    poblar_datasets(resultados)


# ── Subcomando: LIST-ALL (lista todos los batches del proyecto en Google) ────

def cmd_list_all(client: genai.Client, args):
    """Lista TODOS los batches visibles con esta API key (no solo los de este script)."""
    print('─' * 95)
    print(f'  {"name":<45}  {"display_name":<22}  {"estado":<12}  {"create":<14}')
    print('─' * 95)
    count = 0
    for b in client.batches.list():
        estado = str(b.state).replace('JobState.JOB_STATE_', '').replace('JobState.', '')
        disp = (b.display_name or '—')[:22]
        nombre_corto = b.name.replace('batches/', '')[:45]
        creado = str(getattr(b, 'create_time', ''))[:14]
        print(f'  {nombre_corto:<45}  {disp:<22}  {estado:<12}  {creado}')
        count += 1
    print('─' * 95)
    print(f'  Total: {count} batches')


# ── Subcomando: LIST-FILES (archivos JSONL subidos) ──────────────────────────

def cmd_list_files(client: genai.Client, args):
    """Lista los archivos subidos (incluye los JSONL de los batches)."""
    print('─' * 95)
    print(f'  {"name":<30}  {"display_name":<35}  {"size (KB)":>10}  {"mime":<12}')
    print('─' * 95)
    count = 0
    total_bytes = 0
    for f in client.files.list():
        size = f.size_bytes or 0
        total_bytes += size
        nombre_corto = f.name.replace('files/', '')[:30]
        disp = (f.display_name or '—')[:35]
        mime = (f.mime_type or '—')[:12]
        print(f'  {nombre_corto:<30}  {disp:<35}  {size/1024:>10.1f}  {mime:<12}')
        count += 1
    print('─' * 95)
    print(f'  Total: {count} archivos  |  {total_bytes/1024/1024:.2f} MB en total')


# ── Subcomando: CLEAN-FILES (borra archivos viejos para no pagar storage) ────

def cmd_clean_files(client: genai.Client, args):
    """Borra archivos subidos que ya no se necesitan."""
    borrados = 0
    for f in client.files.list():
        # Filtra los de nuestros batches (display_name empieza con "batch_pliegos_")
        if not f.display_name or not f.display_name.startswith('batch_pliegos_'):
            continue
        try:
            client.files.delete(name=f.name)
            print(f'  borrado: {f.name}  ({f.display_name})')
            borrados += 1
        except Exception as e:
            print(f'  error borrando {f.name}: {e}')
    print(f'\n  Total archivos borrados: {borrados}')


# ── Subcomando: CANCEL ────────────────────────────────────────────────────────

def cmd_cancel(client: genai.Client, args):
    jobs = cargar_jobs()
    target = None
    for j in jobs:
        if j['job_name'] == args.job_name or j['display_name'] == args.job_name:
            target = j
            break
    if not target:
        print(f'  No se encontro batch: {args.job_name}')
        return
    try:
        client.batches.cancel(name=target['job_name'])
        target['completed'] = True
        target['status_last_seen'] = 'CANCELLED'
        guardar_jobs(jobs)
        print(f'  Cancelado: {target["display_name"]}')
    except Exception as e:
        print(f'  Error cancelando: {e}')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)

    sp_submit = sub.add_parser('submit', help='Preparar y enviar un batch')
    sp_submit.add_argument('--n', type=int, default=100,
                            help=f'Numero de contratos (max {MAX_BATCH_SIZE})')
    sp_submit.add_argument('--modelo', type=str, default=MODELO_DEFAULT)
    sp_submit.add_argument('--retry-sin-match', action='store_true')

    sub.add_parser('status', help='Mostrar estado de los batches registrados localmente')
    sub.add_parser('collect', help='Descargar resultados de batches completados')
    sub.add_parser('list-all', help='Listar TODOS los batches del proyecto en Google')
    sub.add_parser('list-files', help='Listar archivos subidos a Files API')
    sub.add_parser('clean-files', help='Borrar archivos JSONL antiguos de los batches')

    sp_cancel = sub.add_parser('cancel', help='Cancelar un batch')
    sp_cancel.add_argument('job_name', help='job_name completo o display_name')

    args = ap.parse_args()

    load_dotenv(RAIZ / '.env')
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print('ERROR: falta GEMINI_API_KEY en .env', file=sys.stderr)
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    if args.cmd == 'submit':
        cmd_submit(client, args)
    elif args.cmd == 'status':
        cmd_status(client, args)
    elif args.cmd == 'collect':
        cmd_collect(client, args)
    elif args.cmd == 'list-all':
        cmd_list_all(client, args)
    elif args.cmd == 'list-files':
        cmd_list_files(client, args)
    elif args.cmd == 'clean-files':
        cmd_clean_files(client, args)
    elif args.cmd == 'cancel':
        cmd_cancel(client, args)


if __name__ == '__main__':
    main()
