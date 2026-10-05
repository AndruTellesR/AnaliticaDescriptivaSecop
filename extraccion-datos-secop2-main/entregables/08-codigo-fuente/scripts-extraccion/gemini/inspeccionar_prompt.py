"""
Muestra el prompt exacto que se le enviaría a Gemini para un contrato.
NO hace llamadas a la API — solo imprime (y opcionalmente guarda a disco)
el texto filtrado del PDF que se inserta después de "TEXTO DEL PLIEGO:".

Uso:
    python scripts/gemini/inspeccionar_prompt.py CO1.PCCNTR.1005228
    python scripts/gemini/inspeccionar_prompt.py CO1.PCCNTR.1005228 --guardar
    python scripts/gemini/inspeccionar_prompt.py CO1.PCCNTR.1005228 --solo-texto
"""

import argparse
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))
from extraer_indicadores_pliegos import extraer_texto_filtrado  # type: ignore

# Reusar las mismas constantes del script de Gemini
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extraer_indicadores_gemini import PROMPT_INSTRUCCIONES  # type: ignore


PLIEGOS_DIR = Path('C:/Users/angel/OneDrive/Escritorio/trabajo dirigido/secop-scraper/storage/pliegos')
RAIZ = Path(__file__).resolve().parent.parent.parent
SALIDA_DIR = RAIZ / 'data' / 'prompts_inspeccion'


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    ap = argparse.ArgumentParser()
    ap.add_argument('id_contrato', help='ID del contrato, ej: CO1.PCCNTR.1005228')
    ap.add_argument('--guardar', action='store_true',
                    help='Guarda el prompt completo a data/prompts_inspeccion/')
    ap.add_argument('--solo-texto', action='store_true',
                    help='Muestra solo el texto filtrado, sin las instrucciones')
    args = ap.parse_args()

    pdf_path = next(PLIEGOS_DIR.glob(f'{args.id_contrato}.*'), None)
    if not pdf_path or pdf_path.suffix.lower() != '.pdf':
        print(f'ERROR: no se encontró PDF para {args.id_contrato}')
        sys.exit(1)

    print(f'PDF: {pdf_path.name}')
    print(f'Tamaño: {pdf_path.stat().st_size / 1024:.1f} KB')
    print()

    extr = extraer_texto_filtrado(pdf_path)

    if extr.get('error'):
        print(f'ERROR en extracción: {extr["error"]}')
        sys.exit(1)

    texto = extr.get('texto', '')
    print(f'Total de páginas del PDF : {extr["total_paginas"]}')
    print(f'Páginas finales filtradas: {extr["paginas_finales"]}')
    print(f'Longitud del texto       : {extr["longitud_filtrada"]:,} chars')
    print(f'Se enviarán              : {min(len(texto), 60000):,} chars (corte a 60K)')
    print()
    print('=' * 70)

    if args.solo_texto:
        print('TEXTO FILTRADO DEL PDF (lo que va después de "TEXTO DEL PLIEGO: ---")')
        print('=' * 70)
        print(texto[:60000])
    else:
        print('PROMPT COMPLETO QUE SE ENVÍA A GEMINI')
        print('=' * 70)
        prompt_completo = PROMPT_INSTRUCCIONES + texto[:60000] + '\n---'
        print(prompt_completo)

    print('=' * 70)

    if args.guardar:
        SALIDA_DIR.mkdir(parents=True, exist_ok=True)
        out = SALIDA_DIR / f'{args.id_contrato}_prompt.txt'
        prompt_completo = PROMPT_INSTRUCCIONES + texto[:60000] + '\n---'
        out.write_text(prompt_completo, encoding='utf-8')
        print()
        print(f'✓ Prompt guardado en: {out}')
        print(f'  ({out.stat().st_size / 1024:.1f} KB)')


if __name__ == '__main__':
    main()
