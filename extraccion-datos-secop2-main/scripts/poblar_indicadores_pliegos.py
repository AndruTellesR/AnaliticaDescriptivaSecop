"""
Poblar el dataset depurado con los indicadores extraídos de los pliegos.

Toma los resultados del script `extraer_indicadores_pliegos.py` y:
1. Añade columnas `pliego_*` al dataset depurado.
2. Sólo rellena los id_contrato que tienen valores extraídos.
3. El resto queda como NaN (los procesaremos luego con LLM o mejores regex).

Las columnas añadidas aplican a TODOS los contratos en el futuro (no solo
consorcios), porque el pliego define el umbral requerido del proceso,
independiente del tipo de proveedor.
"""

import json
import sys
from pathlib import Path

import pandas as pd


RAIZ = Path(__file__).resolve().parent.parent
DEPURADO = RAIZ / 'data' / 'contratos_depurado_modelo.parquet'
COMPLETO = RAIZ / 'data' / 'contratos_adiciones_obra.parquet'
JSON_INDIC = RAIZ / 'data' / 'indicadores_pliegos_extraidos.json'


COLS_PLIEGO = [
    'pliego_liquidez_min',
    'pliego_endeudamiento_max_pct',
    'pliego_cobertura_intereses_min',
    'pliego_rentabilidad_patrimonio_min_pct',
    'pliego_rentabilidad_activo_min_pct',
    'pliego_capital_trabajo_min_pct_presupuesto',
]

MAPA = {
    'liquidez_min': 'pliego_liquidez_min',
    'endeudamiento_max_pct': 'pliego_endeudamiento_max_pct',
    'cobertura_intereses_min': 'pliego_cobertura_intereses_min',
    'rentabilidad_patrimonio_min_pct': 'pliego_rentabilidad_patrimonio_min_pct',
    'rentabilidad_activo_min_pct': 'pliego_rentabilidad_activo_min_pct',
    'capital_trabajo_min_pct_presupuesto': 'pliego_capital_trabajo_min_pct_presupuesto',
}


def main():
    sys.stdout.reconfigure(encoding='utf-8')

    # 1. Cargar indicadores extraídos (JSON)
    with JSON_INDIC.open(encoding='utf-8') as f:
        resultados = json.load(f)

    # Construir DataFrame con id_contrato + columnas pliego_*
    filas = []
    for r in resultados:
        if r.get('estado') != 'ok':
            continue
        fila = {'id_contrato': r['id_contrato']}
        for k_orig, k_nuevo in MAPA.items():
            fila[k_nuevo] = r.get(k_orig)
        filas.append(fila)

    df_pliegos = pd.DataFrame(filas)
    print(f'Contratos con indicadores extraídos: {len(df_pliegos)}')
    print()
    print(df_pliegos.to_string(index=False))

    # 2. Merge con el dataset COMPLETO (tiene id_contrato)
    df_full = pd.read_parquet(COMPLETO)
    # Eliminar columnas pliego_* previas para evitar sufijos en el re-merge
    cols_previas = [c for c in COLS_PLIEGO if c in df_full.columns]
    if cols_previas:
        df_full = df_full.drop(columns=cols_previas)
    df_full_out = df_full.merge(df_pliegos, on='id_contrato', how='left')
    n_filled = df_full_out[COLS_PLIEGO[0]].notna().sum()
    print(f'\nContratos en dataset completo con indicadores: {n_filled:,} / {len(df_full_out):,}')

    # Guardar
    df_full_out.to_parquet(COMPLETO, index=False)
    print(f'✓ Guardado completo: {COMPLETO}')
    print(f'  {df_full_out.shape[0]:,} filas × {df_full_out.shape[1]} columnas')

    # 3. Actualizar el DEPURADO (no tiene id_contrato, hacemos asignación posicional)
    df_dep = pd.read_parquet(DEPURADO)
    assert len(df_dep) == len(df_full_out), 'Mismatch de filas'

    for col in COLS_PLIEGO:
        df_dep[col] = df_full_out[col].values

    df_dep.to_parquet(DEPURADO, index=False)
    print(f'✓ Guardado depurado: {DEPURADO}')
    print(f'  {df_dep.shape[0]:,} filas × {df_dep.shape[1]} columnas')

    # 4. Mostrar las columnas nuevas y su estado
    print('\n=== Columnas pliego_* añadidas ===')
    for col in COLS_PLIEGO:
        n_no_null = df_dep[col].notna().sum()
        print(f'  {col:55s}: {n_no_null:>6,} con valor ({n_no_null/len(df_dep)*100:.2f}%)')

    print('\n=== Muestra del dataset depurado (solo los rellenos) ===')
    llenos = df_dep[df_dep['pliego_liquidez_min'].notna()]
    cols_muestra = ['departamento', 'valor_del_contrato'] + COLS_PLIEGO[:5]
    print(llenos[cols_muestra].to_string(index=False, max_rows=20))


if __name__ == '__main__':
    main()
