"""
Extracción de indicadores de Capacidad Financiera y Organizacional desde
pliegos de condiciones en PDF (SECOP II).

Estrategia:
1. Filtrar páginas relevantes excluyendo el índice/TOC.
2. Agrupar páginas hit en clusters contiguos; quedarse con el cluster más denso
   (el que contiene el bloque real de indicadores, no menciones sueltas).
3. Extraer valores umbral con regex específicos basados en el vocabulario real
   de los pliegos ("igual o superior a 2.5 Habilita", etc.).

Uso:
    python scripts/extraer_indicadores_pliegos.py [--n N]

    --n N   Número de contratos consorcio a procesar (default: 20)
"""

import argparse
import re
import sys
import json
from pathlib import Path
from collections import Counter

import pandas as pd
import pdfplumber


# ── Configuración ─────────────────────────────────────────────────────────────

RAIZ = Path(__file__).resolve().parent.parent
PLIEGOS_DIR = Path('C:/Users/angel/OneDrive/Escritorio/trabajo dirigido/secop-scraper/storage/pliegos')
DATA_PARQUET = RAIZ / 'data' / 'contratos_electronicos_obra.parquet'


# Keywords de sección (indican que la página menciona capacidad financiera/org)
KEYWORDS_SECCION = [
    'capacidad financiera', 'capacidad organizacional',
    'indicador de liquidez', 'índice de liquidez', 'indice de liquidez',
    'nivel de endeudamiento', 'razón de cobertura', 'razon de cobertura',
    'rentabilidad del patrimonio', 'rentabilidad del activo',
    'capital de trabajo',
]

# Keywords de valores umbral (página útil = tiene sección Y valores)
KEYWORDS_VALORES = [
    'habilita', 'no habilita',
    'igual o superior', 'inferior o igual',
    'igual o mayor', 'mayor o igual',
    'menor o igual', 'inferior a', 'superior a',
]


def normalizar_texto(txt: str) -> str:
    if not txt:
        return ''
    return re.sub(r'\s+', ' ', txt.lower())


def es_pagina_indice(txt: str) -> bool:
    """
    Detecta páginas de tabla de contenido / índice.

    Heurística: >= 5 líneas con patrón "texto ... número" (dots o espacios
    antes del número al final). Un TOC típico tiene docenas de estas líneas.
    """
    if not txt:
        return False
    # Contar líneas que terminan con puntos+número (patrón típico de TOC)
    patron_toc = re.compile(r'\.{3,}\s*\d+\s*$', re.MULTILINE)
    matches = patron_toc.findall(txt)
    return len(matches) >= 5


def agrupar_clusters(paginas_hit: list[int], max_gap: int = 3) -> list[list[int]]:
    """
    Agrupa páginas hit en clusters contiguos.

    max_gap=3 significa: si dos hits están a menos de 3 páginas de distancia,
    pertenecen al mismo cluster.
    """
    if not paginas_hit:
        return []
    clusters = [[paginas_hit[0]]]
    for p in paginas_hit[1:]:
        if p - clusters[-1][-1] <= max_gap:
            clusters[-1].append(p)
        else:
            clusters.append([p])
    return clusters


def filtrar_paginas_relevantes(paginas_texto: list[str]) -> dict:
    """
    Selecciona las páginas que contienen el bloque real de indicadores.

    Retorna:
    - paginas_hit_original: todas las páginas con keyword (incluye TOC)
    - paginas_hit_limpias: sin páginas de índice
    - clusters: agrupadas
    - mejor_cluster: el cluster con mayor densidad de keywords de valores
    - paginas_finales: páginas expandidas del mejor cluster
    """
    textos_norm = [normalizar_texto(t) for t in paginas_texto]

    # Paso 1: páginas con keywords de sección
    hits = [i for i, t in enumerate(textos_norm)
            if any(kw in t for kw in KEYWORDS_SECCION)]

    # Paso 2: excluir TOC (índice)
    hits_sin_toc = [i for i in hits if not es_pagina_indice(paginas_texto[i])]

    # Paso 3: agrupar en clusters
    clusters = agrupar_clusters(hits_sin_toc)

    # Paso 4: elegir el cluster con mayor densidad de valores umbral
    def score_cluster(cluster):
        # Una página del cluster "puntúa" según cuántas keywords de valor tiene
        score = 0
        for p in cluster:
            t = textos_norm[p]
            score += sum(1 for kw in KEYWORDS_VALORES if kw in t)
        return score

    mejor_cluster = max(clusters, key=score_cluster) if clusters else []

    # Paso 5: expandir el cluster con 1 página antes y 1 después (contexto)
    if mejor_cluster:
        start = max(0, mejor_cluster[0] - 1)
        end = min(len(paginas_texto) - 1, mejor_cluster[-1] + 1)
        paginas_finales = list(range(start, end + 1))
    else:
        paginas_finales = []

    return {
        'hits_original': hits,
        'hits_sin_toc': hits_sin_toc,
        'clusters': clusters,
        'mejor_cluster': mejor_cluster,
        'paginas_finales': paginas_finales,
    }


def extraer_texto_filtrado(pdf_path: Path) -> dict:
    """
    Abre el PDF, aplica el filtro y devuelve el texto concatenado de las
    páginas finales + stats de diagnóstico.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            paginas_texto = []
            for page in pdf.pages:
                try:
                    paginas_texto.append(page.extract_text() or '')
                except Exception:
                    paginas_texto.append('')
    except Exception as e:
        return {'error': f'{type(e).__name__}: {e}'}

    total_chars = sum(len(t) for t in paginas_texto)
    if total_chars < 1000:
        return {'error': 'pdf_sin_texto_probablemente_escaneado',
                'total_paginas': len(paginas_texto)}

    filtro = filtrar_paginas_relevantes(paginas_texto)
    texto_final = '\n\n--- PAGINA ---\n\n'.join(
        paginas_texto[i] for i in filtro['paginas_finales']
    )

    return {
        'total_paginas': len(paginas_texto),
        'hits_original': filtro['hits_original'],
        'hits_sin_toc': filtro['hits_sin_toc'],
        'clusters': filtro['clusters'],
        'mejor_cluster': filtro['mejor_cluster'],
        'paginas_finales': filtro['paginas_finales'],
        'longitud_original': sum(len(t) for t in paginas_texto),
        'longitud_filtrada': len(texto_final),
        'texto': texto_final,
    }


# ── Extracción de valores con regex ──────────────────────────────────────────

def _num(s: str) -> float | None:
    """Convierte '2,5' o '2.5' a float."""
    try:
        return float(s.replace(',', '.'))
    except (ValueError, AttributeError):
        return None


# Patrones para cada indicador. Cada tupla: (campo, [patrones]).
# Los patrones se aplican sobre texto normalizado (lowercase, espacios colapsados).
#
# Los pliegos usan 2 formatos principales:
#   A) Narrativo: "Razón Corriente igual o superior a 2.5 Habilita"
#   B) Tabla:    "Índice de Liquidez    Mayor o igual a: 1.5"
#
# Los conectores comunes entre nombre del indicador y el valor son:
#   "mayor o igual a", "igual o superior a", "superior a", "mayor a",
#   "menor o igual a", "inferior o igual a", ">=", "<=", ":"
#
# Por eso construimos patrones tolerantes con:
#   - [\s:=]* entre el nombre y el comparador (acepta ": " de tablas)
#   - (?:a|al)?\s*[:]? antes del valor (acepta "a:" o "al ")

COMP_MAYOR = r'(?:igual\s+o\s+superior|mayor\s+o\s+igual|superior\s+o\s+igual|igual\s+o\s+mayor|superior\s+a|mayor\s+a|[>≥]=?)'
COMP_MENOR = r'(?:inferior\s+o\s+igual|menor\s+o\s+igual|igual\s+o\s+inferior|igual\s+o\s+menor|inferior\s+a|menor\s+a|[<≤]=?)'
SEP_VALOR = r'\s*a?l?\s*:?\s*\$?\s*'  # "a: ", "al ", ": ", "a$" → permisivo

PATRONES = {
    'liquidez_min': [
        # Nombre del indicador: índice/razón de liquidez o razón corriente
        rf'(?:[íi]ndice\s+de\s+liquidez|raz[óo]n\s+corriente|\bliquidez\b|\bidl\b|\bil\b)[\s:=]*{COMP_MAYOR}{SEP_VALOR}([\d\.,]+)',
    ],
    'endeudamiento_max_pct': [
        # Acepta "Índice de Endeudamiento (10% PO)" con paréntesis opcional
        rf'(?:[íi]ndice\s+de\s+endeudamiento|nivel\s+de\s+endeudamiento|\bendeudamiento\b|\bnde\b)(?:\s*\([^)]*\))?[\s:=]*{COMP_MENOR}{SEP_VALOR}([\d\.,]+)\s*%?',
    ],
    'cobertura_intereses_min': [
        rf'(?:raz[óo]n\s+(?:de\s+)?cobertura\s+de\s+inter[eé]s(?:es)?|cobertura\s+de\s+inter[eé]s(?:es)?|\bci\b)[\s:=]*{COMP_MAYOR}{SEP_VALOR}([\d\.,]+)',
    ],
    'rentabilidad_patrimonio_min_pct': [
        # Acepta "del patrimonio" y "sobre el patrimonio" / "sobre patrimonio"
        rf'rentabilidad\s+(?:del|sobre\s+(?:el\s+)?)\s*patrimonio[\s:=]*{COMP_MAYOR}{SEP_VALOR}([\d\.,]+)\s*%?',
    ],
    'rentabilidad_activo_min_pct': [
        # Acepta "del activo" y "sobre activos" / "sobre el activo"
        rf'rentabilidad\s+(?:del|sobre\s+(?:el\s+)?)\s*activos?(?:\s+total)?[\s:=]*{COMP_MAYOR}{SEP_VALOR}([\d\.,]+)\s*%?',
    ],
    'capital_trabajo_min_pct_presupuesto': [
        # "Capital de Trabajo igual o Superior al 70% del valor del Presupuesto"
        rf'capital\s+de\s+trabajo[^\n]{{0,120}}?{COMP_MAYOR}\s*al?\s*([\d\.,]+)\s*%\s*del\s+(?:valor\s+del\s+)?presupuesto',
    ],
}


def extraer_indicadores(texto: str) -> dict:
    """Aplica los patrones y devuelve un dict con los valores encontrados."""
    texto_norm = normalizar_texto(texto)
    resultado = {}
    for campo, patrones in PATRONES.items():
        valor = None
        for patron in patrones:
            m = re.search(patron, texto_norm)
            if m:
                valor = _num(m.group(1))
                if valor is not None:
                    break
        resultado[campo] = valor
    return resultado


# ── Orquestación ─────────────────────────────────────────────────────────────

def procesar_contrato(id_contrato: str, pliegos_dir: Path) -> dict:
    archivos = list(pliegos_dir.glob(f'{id_contrato}.*'))
    if not archivos:
        return {'id_contrato': id_contrato, 'estado': 'no_descargado'}

    archivo = archivos[0]
    if archivo.suffix.lower() != '.pdf':
        return {'id_contrato': id_contrato, 'estado': 'no_pdf',
                'formato': archivo.suffix}

    extr = extraer_texto_filtrado(archivo)
    if extr.get('error'):
        return {'id_contrato': id_contrato, 'estado': 'error',
                'error': extr['error']}

    if not extr['texto']:
        return {'id_contrato': id_contrato, 'estado': 'sin_match',
                'total_paginas': extr['total_paginas']}

    indicadores = extraer_indicadores(extr['texto'])
    n_extraidos = sum(1 for v in indicadores.values() if v is not None)

    return {
        'id_contrato': id_contrato,
        'archivo': archivo.name,
        'estado': 'ok' if n_extraidos > 0 else 'texto_sin_umbrales',
        'total_paginas': extr['total_paginas'],
        'hits_original': len(extr['hits_original']),
        'hits_sin_toc': len(extr['hits_sin_toc']),
        'clusters': len(extr['clusters']),
        'paginas_finales': extr['paginas_finales'],
        'longitud_original': extr['longitud_original'],
        'longitud_filtrada': extr['longitud_filtrada'],
        'reduccion_pct': round(
            (1 - extr['longitud_filtrada'] / extr['longitud_original']) * 100, 1
        ) if extr['longitud_original'] else 0,
        'indicadores_extraidos': n_extraidos,
        **indicadores,
    }


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--solo-consorcios', action='store_true', default=True)
    args = ap.parse_args()

    df = pd.read_parquet(DATA_PARQUET)
    if args.solo_consorcios:
        muestra = df[df['es_grupo'] == 'Si'].head(args.n)
    else:
        muestra = df.head(args.n)

    print('=' * 80)
    print(f'EXTRACCIÓN DE INDICADORES — {args.n} contratos consorcio')
    print('=' * 80)

    resultados = []
    for _, row in muestra.iterrows():
        id_c = row['id_contrato']
        r = procesar_contrato(id_c, PLIEGOS_DIR)
        resultados.append(r)

        estado = r.get('estado', '?')
        if estado in ['ok', 'texto_sin_umbrales']:
            extr = r.get('indicadores_extraidos', 0)
            print(f'\n[{id_c}] {estado}')
            print(f'  Páginas totales: {r["total_paginas"]} | '
                  f'hits raw: {r["hits_original"]} | '
                  f'sin TOC: {r["hits_sin_toc"]} | '
                  f'clusters: {r["clusters"]}')
            print(f'  Páginas finales: {r["paginas_finales"]}')
            print(f'  Texto original: {r["longitud_original"]:,} ch → '
                  f'filtrado: {r["longitud_filtrada"]:,} ch '
                  f'(reducción {r["reduccion_pct"]}%)')
            print(f'  Indicadores extraídos ({extr}/6):')
            for k in ['liquidez_min', 'endeudamiento_max_pct',
                      'cobertura_intereses_min',
                      'rentabilidad_patrimonio_min_pct',
                      'rentabilidad_activo_min_pct',
                      'capital_trabajo_min_pct_presupuesto']:
                v = r.get(k)
                marca = '✓' if v is not None else ' '
                print(f'    {marca} {k:40s} = {v}')
        else:
            print(f'\n[{id_c}] {estado}')

    # ── Resumen ──
    print()
    print('=' * 80)
    print('RESUMEN')
    print('=' * 80)
    estados = Counter(r.get('estado') for r in resultados)
    for estado, n in estados.most_common():
        print(f'  {estado:30s}: {n}')

    # Tasas de extracción por indicador
    ok = [r for r in resultados if r.get('estado') == 'ok']
    print(f'\nTasa de extracción por indicador (sobre {len(ok)} con texto OK):')
    for k in ['liquidez_min', 'endeudamiento_max_pct',
              'cobertura_intereses_min',
              'rentabilidad_patrimonio_min_pct',
              'rentabilidad_activo_min_pct',
              'capital_trabajo_min_pct_presupuesto']:
        con_valor = sum(1 for r in ok if r.get(k) is not None)
        pct = con_valor / len(ok) * 100 if ok else 0
        print(f'  {k:40s}: {con_valor}/{len(ok)} ({pct:.0f}%)')

    # Guardar resultados como JSON
    out = RAIZ / 'data' / 'indicadores_pliegos_extraidos.json'
    # Limpiar el texto para no saturar el JSON
    for r in resultados:
        r.pop('texto', None)
    out.write_text(
        json.dumps(resultados, ensure_ascii=False, indent=2, default=str),
        encoding='utf-8'
    )
    print(f'\nResultados guardados en: {out}')


if __name__ == '__main__':
    main()
