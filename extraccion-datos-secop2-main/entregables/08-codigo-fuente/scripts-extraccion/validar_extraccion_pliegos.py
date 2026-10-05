"""
Script de validación: ¿podemos detectar y extraer las secciones de capacidad
financiera y organizacional en los pliegos PDF?

No llama a ningún LLM. Solo usa pdfplumber para filtrar páginas por keywords
y reporta cobertura. El objetivo es responder: ¿vale la pena invertir en el
pipeline con LLM, o los PDFs son tan heterogéneos que ni siquiera podemos
encontrar las páginas correctas?

Uso:
    python scripts/validar_extraccion_pliegos.py
"""

import sys
import re
from pathlib import Path

import pandas as pd
import pdfplumber


# ── Configuración ─────────────────────────────────────────────────────────────

RAIZ = Path(__file__).resolve().parent.parent
PLIEGOS_DIR = Path('C:/Users/angel/OneDrive/Escritorio/trabajo dirigido/secop-scraper/storage/pliegos')
DATA_PARQUET = RAIZ / 'data' / 'contratos_electronicos_obra.parquet'

N_MUESTRA = 20  # primeros N consorcios a validar


# Keywords que indican que la página contiene la información que buscamos.
# Combinamos términos de capacidad financiera + organizacional.
KEYWORDS_SECCION = [
    'capacidad financiera',
    'capacidad organizacional',
    'indicador de liquidez',
    'índice de liquidez',
    'indice de liquidez',
    'nivel de endeudamiento',
    'razón de cobertura de intereses',
    'razon de cobertura de intereses',
    'rentabilidad del patrimonio',
    'rentabilidad del activo',
    'capital de trabajo',
    'patrimonio',
]

# Keywords específicas para validar que los valores numéricos están presentes
# (si una página dice "capacidad financiera" pero no tiene umbrales, no sirve)
KEYWORDS_VALORES = [
    'habilita',
    'no habilita',
    'igual o superior',
    'inferior o igual',
    'igual o mayor',
    'mayor o igual',
]


def normalizar_texto(txt: str) -> str:
    """Lowercase + colapsar espacios, para matching consistente."""
    if not txt:
        return ''
    txt = txt.lower()
    txt = re.sub(r'\s+', ' ', txt)
    return txt


def extraer_fragmento_relevante(pdf_path: Path, max_paginas_contexto: int = 2) -> dict:
    """
    Abre el PDF y busca las páginas que contienen secciones de capacidad.

    Estrategia:
    1. Recorrer todas las páginas detectando keywords de sección.
    2. Para cada página-hit, incluir también las siguientes 1-2 páginas (el
       detalle de los umbrales suele abarcar varias páginas).
    3. Devolver stats y el texto concatenado.
    """
    resultado = {
        'archivo': pdf_path.name,
        'total_paginas': 0,
        'paginas_hit': [],
        'paginas_seleccionadas': [],
        'longitud_texto': 0,
        'tiene_valores_umbral': False,
        'texto_extraido': '',
        'error': None,
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            resultado['total_paginas'] = len(pdf.pages)

            paginas_texto = []
            for i, page in enumerate(pdf.pages):
                try:
                    paginas_texto.append(page.extract_text() or '')
                except Exception:
                    paginas_texto.append('')

            # Detectar páginas que mencionan la sección
            paginas_hit = set()
            for i, txt in enumerate(paginas_texto):
                txt_norm = normalizar_texto(txt)
                if any(kw in txt_norm for kw in KEYWORDS_SECCION):
                    paginas_hit.add(i)

            resultado['paginas_hit'] = sorted(paginas_hit)

            # Expandir: incluir páginas de contexto
            paginas_sel = set(paginas_hit)
            for p in paginas_hit:
                for j in range(1, max_paginas_contexto + 1):
                    if p + j < len(paginas_texto):
                        paginas_sel.add(p + j)
            resultado['paginas_seleccionadas'] = sorted(paginas_sel)

            # Concatenar texto de esas páginas
            fragmentos = [paginas_texto[i] for i in sorted(paginas_sel)]
            texto_extraido = '\n\n--- PÁGINA ---\n\n'.join(fragmentos)
            resultado['texto_extraido'] = texto_extraido
            resultado['longitud_texto'] = len(texto_extraido)

            # Detectar si hay valores de umbral (no solo menciones)
            texto_norm = normalizar_texto(texto_extraido)
            resultado['tiene_valores_umbral'] = any(
                kw in texto_norm for kw in KEYWORDS_VALORES
            )

    except Exception as e:
        resultado['error'] = f'{type(e).__name__}: {e}'

    return resultado


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    # Cargar contratos consorcio
    df = pd.read_parquet(DATA_PARQUET)
    consorcios = df[df['es_grupo'] == 'Si'].head(N_MUESTRA)

    print('=' * 70)
    print(f'VALIDACIÓN DE EXTRACCIÓN — {N_MUESTRA} contratos consorcio')
    print('=' * 70)

    resultados = []
    for idx, row in consorcios.iterrows():
        id_c = row['id_contrato']
        archivos = list(PLIEGOS_DIR.glob(f'{id_c}.*'))

        if not archivos:
            print(f'\n[SKIP] {id_c} — archivo no descargado')
            resultados.append({'id_contrato': id_c, 'estado': 'no_descargado'})
            continue

        archivo = archivos[0]
        if archivo.suffix.lower() not in ['.pdf']:
            print(f'\n[SKIP] {id_c} — formato {archivo.suffix} (no PDF)')
            resultados.append({
                'id_contrato': id_c,
                'estado': 'no_pdf',
                'formato': archivo.suffix
            })
            continue

        print(f'\n[{id_c}] procesando...')
        r = extraer_fragmento_relevante(archivo)
        r['id_contrato'] = id_c
        r['estado'] = 'error' if r['error'] else (
            'ok_con_umbrales' if r['tiene_valores_umbral']
            else 'ok_sin_umbrales' if r['paginas_hit']
            else 'sin_match'
        )
        resultados.append(r)

        if r['error']:
            print(f'  ERROR: {r["error"]}')
        else:
            print(f'  Total páginas PDF:    {r["total_paginas"]}')
            print(f'  Páginas hit:          {len(r["paginas_hit"])} ({r["paginas_hit"][:10]})')
            print(f'  Páginas seleccionadas: {len(r["paginas_seleccionadas"])}')
            print(f'  Texto extraído:       {r["longitud_texto"]:,} caracteres')
            print(f'  Tiene valores umbral: {"SÍ" if r["tiene_valores_umbral"] else "NO"}')

    # ── Resumen ──
    print()
    print('=' * 70)
    print('RESUMEN')
    print('=' * 70)
    from collections import Counter
    estados = Counter(r.get('estado') for r in resultados)
    for estado, n in estados.most_common():
        print(f'  {estado:25s}: {n}')

    # ── Guardar resultados ──
    out_dir = RAIZ / 'data'
    out_dir.mkdir(exist_ok=True)
    out_path = out_dir / 'validacion_extraccion_pliegos.txt'

    with out_path.open('w', encoding='utf-8') as f:
        for r in resultados:
            if r.get('estado') not in ['ok_con_umbrales', 'ok_sin_umbrales']:
                continue
            f.write('=' * 80 + '\n')
            f.write(f'ID CONTRATO: {r["id_contrato"]}\n')
            f.write(f'Archivo: {r["archivo"]}\n')
            f.write(f'Total páginas PDF: {r["total_paginas"]}\n')
            f.write(f'Páginas seleccionadas: {r["paginas_seleccionadas"]}\n')
            f.write(f'Longitud texto: {r["longitud_texto"]:,} caracteres\n')
            f.write(f'Tiene valores umbral: {r["tiene_valores_umbral"]}\n')
            f.write('\n--- TEXTO EXTRAÍDO (primeros 5000 chars) ---\n\n')
            f.write(r['texto_extraido'][:5000])
            f.write('\n\n')

    print(f'\nMuestras guardadas en: {out_path}')


if __name__ == '__main__':
    main()
