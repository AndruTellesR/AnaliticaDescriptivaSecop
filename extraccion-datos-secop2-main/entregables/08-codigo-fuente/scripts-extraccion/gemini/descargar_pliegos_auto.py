"""
Descargador automático de pliegos — Sin Playwright, directo desde API Socrata.

Obtiene URLs de documentos para consorcios sin PDF descargado, selecciona
el más relevante usando heurística, y descarga en lote.

Uso:
    python scripts/gemini/descargar_pliegos_auto.py --n 500
    python scripts/gemini/descargar_pliegos_auto.py --n 1000 --solo-contar
"""

import argparse
import sys
import time
from pathlib import Path
from collections import defaultdict

import pandas as pd
import requests
from tqdm import tqdm
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent.parent
DATA_PARQUET = RAIZ / 'data' / 'contratos_electronicos_obra.parquet'
PLIEGOS_DIR = Path('C:/Users/angel/OneDrive/Escritorio/trabajo dirigido/secop-scraper/storage/pliegos')

SECOP_API = 'https://community.secop.gov.co/api/3/action/datastore_search_sql'
SECOP_DATASET = 'c29ef1f0-bcf2-4e4e-8988-0e9d5fe54bb7'  # Dataset de procesos de contratación
APP_TOKEN = 'nrnMDVHrooMY3wZIGrYfPsAq3'

# Heurística de selección: orden de preferencia de nombres de documento
HEURISTICA_NOMBRES = [
    r'pliego de condiciones definitivo',
    r'invitacion publica',
    r'pliego',
    r'condiciones definitivas',
    r'bases definitivas',
    r'terminos de referencia',
    r'proyecto de pliego',
]


def log(msg=''):
    """Escribe sin interferir con tqdm."""
    tqdm.write(msg)


def obtener_documentos_contrato(id_proceso: str) -> list:
    """
    Obtiene lista de documentos disponibles para un contrato desde SECOP II.

    Returns: lista de dicts con {nombre, url, tipo}
    """
    try:
        # Busca documentos enlazados al proceso
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
            {
                'nombre': r.get('nombre', '').strip(),
                'url': r.get('url', '').strip(),
            }
            for r in records if r.get('url')
        ]
    except Exception as e:
        return []


def seleccionar_mejor_documento(documentos: list) -> dict:
    """
    Aplica heurística para elegir el mejor documento.
    Retorna el primer match de HEURISTICA_NOMBRES.
    """
    if not documentos:
        return None

    nombres_lower = {d['nombre'].lower(): d for d in documentos}

    # Aplicar heurística en orden de preferencia
    for patron in HEURISTICA_NOMBRES:
        for nombre, doc in nombres_lower.items():
            if patron in nombre:
                return doc

    # Fallback: retornar el primero
    return documentos[0]


def obtener_id_proceso(id_contrato: str, df_procesos: pd.DataFrame) -> str:
    """
    Obtiene el ID del proceso de contratación a partir del id_contrato.
    """
    fila = df_procesos[df_procesos['id_contrato'] == id_contrato]
    if fila.empty:
        return None
    return fila.iloc[0].get('id_del_portafolio')


def descargar_archivo(url: str, ruta_local: Path, max_retries: int = 3) -> bool:
    """Descarga un archivo desde URL."""
    for intento in range(max_retries):
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                ruta_local.write_bytes(resp.content)
                return True
        except Exception as e:
            if intento < max_retries - 1:
                time.sleep(1)
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=500,
                    help='Máximo de contratos a descargar')
    ap.add_argument('--solo-contar', action='store_true',
                    help='Solo contar sin descargar')
    args = ap.parse_args()

    # Cargar parquet de consorcios
    df = pd.read_parquet(DATA_PARQUET)
    consorcios = df[df['es_grupo'] == 'Si'].copy()
    log(f'📊 Consorcios totales: {len(consorcios):,}')

    # PDFs ya descargados
    pdfs_existentes = {p.stem for p in PLIEGOS_DIR.glob('*.*') if p.suffix.lower() == '.pdf'}
    log(f'📥 PDFs descargados: {len(pdfs_existentes):,}')

    # Consorcios sin PDF
    sin_pdf = consorcios[~consorcios['id_contrato'].isin(pdfs_existentes)]
    log(f'⏳ Consorcios sin PDF: {len(sin_pdf):,}')

    if args.solo_contar:
        log(f'\n✅ Total a descargar: {min(args.n, len(sin_pdf)):,}')
        return

    # Seleccionar primeros N
    a_descargar = sin_pdf.head(args.n).copy()
    log(f'\n🚀 Iniciando descarga de {len(a_descargar):,} contratos...\n')

    exitos = 0
    fallos = 0
    sin_docs = 0

    PLIEGOS_DIR.mkdir(parents=True, exist_ok=True)

    with tqdm(total=len(a_descargar), desc='Descargando', unit='pdf', ncols=80) as pbar:
        for _, row in a_descargar.iterrows():
            id_contrato = row['id_contrato']
            id_proceso = row.get('id_del_portafolio')

            # Obtener documentos disponibles
            documentos = obtener_documentos_contrato(id_proceso) if id_proceso else []

            if not documentos:
                sin_docs += 1
                pbar.update(1)
                continue

            # Seleccionar mejor documento
            doc = seleccionar_mejor_documento(documentos)
            if not doc or not doc.get('url'):
                sin_docs += 1
                pbar.update(1)
                continue

            # Descargar
            url = doc['url']
            ext = Path(url).suffix.lower() or '.pdf'
            ruta_local = PLIEGOS_DIR / f'{id_contrato}{ext}'

            if descargar_archivo(url, ruta_local):
                exitos += 1
            else:
                fallos += 1
                ruta_local.unlink(missing_ok=True)

            pbar.update(1)
            time.sleep(0.5)  # Rate limit amable

    # Reporte final
    log('')
    log('─' * 70)
    log('📋 RESUMEN')
    log('─' * 70)
    log(f'  Exitosas     : {exitos:>6,}')
    log(f'  Fallidas     : {fallos:>6,}')
    log(f'  Sin documentos: {sin_docs:>6,}')
    log(f'  Total        : {exitos + fallos + sin_docs:>6,}')
    log('─' * 70)


if __name__ == '__main__':
    main()
