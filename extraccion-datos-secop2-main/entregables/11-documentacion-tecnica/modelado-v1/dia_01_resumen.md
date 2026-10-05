# Día 1 — Resumen

**Notebook**: [`notebooks/09_definicion_target_eda.ipynb`](../../notebooks/09_definicion_target_eda.ipynb)
**Fecha**: 2026-04-29
**Director**: Asistido (rol Claude)

---

## Lo que se hizo

1. Carga de `data/contratos_depurado_modelo.parquet` (48,331 × 53)
2. Análisis de las columnas binarias preexistentes `tiempo`, `presupuesto`, `alcance`
3. Construcción de 3 candidatos a target
4. Identificación de leakage (14 columnas)
5. EDA inicial: distribución de valor, tasa por modalidad/orden/departamento, cobertura `pliego_*`
6. Persistencia del dataset listo: `data/dataset_modelado.parquet` (48,331 × 42)

---

## Hallazgos clave

### 1. Balance de targets

| Target | % positivos | Decisión |
|--------|-------------|----------|
| `tuvo_atraso_o_sobrecosto` (OR) | **89.1%** | ❌ Descartado — trivial predecir 1 |
| `tuvo_atraso` | **60.5%** | ✅ **Target primario del sprint** |
| `tuvo_sobrecosto` | **83.4%** | ⚠️ Secundario, requiere técnicas de imbalance |

### 2. Cobertura `pliego_*`

Hoy (extracción aún corriendo): ~2-3% del dataset tiene los 6 indicadores.
Para el sprint: tratar como feature ralo + flag `tiene_pliego_extraido`.

### 3. Leakage identificado (14 cols)

```
tiempo, presupuesto, alcance,
n_modif_general, n_tipos_distintos, n_tipo_no_definido, n_suspension,
tiene_cesion, tiene_conclusion, tiene_suspension,
dias_adicionados, dias_hasta_primera_adicion, ventana_adiciones_dias,
ratio_extension_duracion
```

Lista persistida en `cols_leakage.txt` para uso en notebooks 10-14.

### 4. Variabilidad por departamento

La tasa de target varía significativamente entre departamentos
(visualizado en `fig_tasa_por_depto.png`). `departamento` es feature
con señal predictiva fuerte → mantener pero codificar con cuidado
(alta cardinalidad, posible target encoding).

---

## Outputs

- `data/dataset_modelado.parquet` — 48,331 × 42 (38 features candidatas + 3 targets + 1 flag)
- `doc/fase4_modelado/cols_leakage.txt`
- `doc/fase4_modelado/fig_balance_target.png`
- `doc/fase4_modelado/fig_valor_contrato.png`
- `doc/fase4_modelado/fig_tasa_por_depto.png`

---

## Próximo paso (Día 2)

Notebook `10_feature_engineering.ipynb`:

1. Audit final de tipos y cardinalidades
2. Codificación:
   - Categóricas binarias / `Si`/`No` → 0/1
   - Categóricas baja cardinalidad (< 20) → One-Hot
   - Categóricas alta cardinalidad (`departamento`, `ciudad`, `entidad_centralizada`) → Target Encoding con CV
3. Imputación:
   - Numéricas con < 10% missing → mediana
   - Categóricas con < 5% missing → moda
   - `pliego_*` → mantener NaN como categoría (XGB/LGBM lo manejan nativamente) o flag binario
4. Stratified train/test split 80/20 (random_state=42)
5. Persistir `X_train.parquet`, `X_test.parquet`, `y_train.parquet`, `y_test.parquet`

**Tiempo estimado**: 2-4 horas.
