"""
Validador de PDFs — Determina cuáles PDFs descargados contienen contenido relevante
(sin importar el nombre del archivo).

Itera todos los PDFs en la carpeta de almacenamiento, aplica el filtro preliminar
extraer_texto_filtrado() a cada uno, y registra:
- PDFs con contenido relevante (clusters encontrados)
- PDFs sin contenido relevante (sin_match)
- PDFs con errores (escaneados, corrupto, etc)

Uso:
    python scripts/gemini/validar_pliegos.py
    python scripts/gemini/validar_pliegos.py --output resultados.json
"""

import json
import sys
from pathlib import Path
from collections import Counter

import pandas as pd
from tqdm import tqdm

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
from extraer_indicadores_pliegos import extraer_texto_filtrado  # type: ignore

RAIZ = Path(__file__).resolve().parent.parent.parent
PLIEGOS_DIR = Path('C:/Users/angel/OneDrive/Escritorio/trabajo dirigido/secop-scraper/storage/pliegos')
OUTPUT_JSON = RAIZ / 'data' / 'validacion_pliegos.json'


def validar_todos_pliegos(output_file: Path = OUTPUT_JSON):
    """Valida todos los PDFs en PLIEGOS_DIR."""

    # Encontrar todos los PDFs
    pdfs = sorted([p for p in PLIEGOS_DIR.glob('*.*') if p.suffix.lower() == '.pdf'])
    print(f'\n📂 PDFs encontrados: {len(pdfs)}')

    resultados = []
    resumen = Counter()

    with tqdm(total=len(pdfs), desc='Validando', unit='pdf', ncols=80) as pbar:
        for pdf_path in pdfs:
            id_contrato = pdf_path.stem

            # Aplicar filtro
            extr = extraer_texto_filtrado(pdf_path)

            if extr.get('error'):
                estado = 'error_pdf'
                resumen[estado] += 1
                resultado = {
                    'id_contrato': id_contrato,
                    'archivo': pdf_path.name,
                    'estado': estado,
                    'error': extr['error'],
                }
            else:
                texto = extr.get('texto', '')
                paginas = extr.get('paginas_finales', [])
                clusters = len(extr.get('clusters_encontrados', []))

                if texto and clusters > 0:
                    estado = 'valido'
                    resumen[estado] += 1
                else:
                    estado = 'sin_match'
                    resumen[estado] += 1

                resultado = {
                    'id_contrato': id_contrato,
                    'archivo': pdf_path.name,
                    'estado': estado,
                    'total_paginas': extr.get('total_paginas', 0),
                    'clusters_encontrados': clusters,
                    'paginas_relevantes': paginas,
                    'longitud_texto': len(texto),
                }

            resultados.append(resultado)
            pbar.update(1)

    # Guardar resultados
    output_file.write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2, default=str),
        encoding='utf-8'
    )

    # Reporte
    print('\n' + '─' * 70)
    print('📊 RESUMEN DE VALIDACIÓN')
    print('─' * 70)
    total = len(resultados)
    for estado in ['valido', 'sin_match', 'error_pdf']:
        cnt = resumen[estado]
        pct = cnt / total * 100 if total > 0 else 0
        print(f'  {estado:<20} {cnt:>6,}  ({pct:>5.1f}%)')

    print('─' * 70)
    print(f'Total                : {total:>6,}')
    print(f'\n✅ Resultados guardados en: {output_file}')

    # Estadísticas de PDFs válidos
    validos = [r for r in resultados if r['estado'] == 'valido']
    print(f'\n💾 PDFs válidos para Gemini: {len(validos):,}')
    if validos:
        print(f'   Primeros 5:')
        for r in validos[:5]:
            print(f'     • {r["id_contrato"]} ({r["clusters_encontrados"]} clusters)')


if __name__ == '__main__':
    validar_todos_pliegos()
