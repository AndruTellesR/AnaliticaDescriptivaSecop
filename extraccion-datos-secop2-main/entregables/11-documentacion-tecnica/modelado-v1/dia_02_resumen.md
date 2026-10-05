# Día 2 — Feature Engineering + Train/Test Split

**Notebook**: [`notebooks/02_feature_engineering.ipynb`](../notebooks/02_feature_engineering.ipynb)
**Fecha**: 2026-04-29
**Input**: `data/dataset_modelado.parquet` (48,331 × 42)
**Output**: 4 parquets (`X_train`, `X_test`, `y_train`, `y_test`) + freq_maps + schema CSV

---

## Lo que se hizo

1. Audit de tipos y cardinalidades de las 39 features
2. Drop de cols sin varianza
3. **Frequency Encoding** para categóricas alta cardinalidad (≥ 20 valores únicos)
4. **One-Hot Encoding** para categóricas baja cardinalidad (< 20)
5. **Imputación**: mediana + flag `_was_nan` para todas las cols numéricas con NaN
6. **Stratified split** 80/20 (random_state=42)
7. Persistencia parquets + pkl + CSV schema

---

## Resultados clave

| Métrica | Valor |
|---------|-------|
| Train | **38,664 × 94** |
| Test | **9,667 × 94** |
| Balance train | 60.48% positivos |
| Balance test | 60.48% positivos |
| Diferencia balance | < 0.01% (split perfecto) |
| Cols numéricas raw | 23 |
| Cols OHE + flags `_was_nan` | 71 |
| **Total cols finales** | **94** |

---

## Decisiones técnicas

### Frequency Encoding (no Target Encoding)

Cardinalidad alta detectada:
- `departamento`: 34 valores
- `ciudad`: 617 valores
- `entidad_centralizada`: probablemente similar
- `modalidad_de_contratacion`, `sector`, `documentos_tipo`: > 20

**Por qué Frequency Encoding (proxy):**
- No requiere CV para evitar leakage (Target Encoding sí)
- Captura la prevalencia de cada categoría
- Si Día 5 (tuning) las métricas se quedan cortas → upgrade a Target Encoding con `category_encoders.TargetEncoder` con CV interno

**`freq_maps.pkl`** persistido para inference futura: dict {col: {valor: frecuencia}}

### Imputación con flag `_was_nan`

Para preservar la información "este valor era NaN", agregamos un flag binario.
Los modelos (especialmente árboles) pueden aprender que "campo X faltante" es predictor.

- `pliego_*`: ~98% NaN → flag `_was_nan` muy informativo (cobertura crece con extracción)
- `rup_*`: ~60% NaN → idem
- `duracion_planificada_dias`: 12.6% NaN → flag útil

### Por qué no escalado todavía

Solo Logistic Regression necesita StandardScaler. RF/XGBoost/LightGBM no.
Decisión: aplicar StandardScaler en pipeline del modelo LR (Día 3), no en el dataset compartido.

---

## Outputs persistidos

```
data/
├── X_train.parquet         (38,664 × 94)
├── X_test.parquet          (9,667 × 94)
├── y_train.parquet         (38,664 × 1)  60.48% pos
├── y_test.parquet          (9,667 × 1)   60.48% pos
├── freq_maps.pkl           (dict para inference)
├── schema_features.csv     (dtypes + nunique + nan)
└── dataset_modelado.parquet (preservado, input del notebook)

figuras/
├── dia_02_balance_split.png       (visual del balance preservado)
└── dia_02_top_corr_features.png   (top 20 corr abs con target)
```

---

## Hallazgos del análisis exploratorio post-FE

**Top features con correlación absoluta más alta con target** (en train):
La gráfica `dia_02_top_corr_features.png` muestra que las top features
provienen tanto de la modalidad de contratación como del valor del contrato
y el origen de los recursos, alineado con el EDA de Día 1.

> **Nota**: Correlación lineal sólo da pista preliminar. Los modelos no-lineales
> (árboles) pueden aprovechar interacciones no capturadas por correlación de Pearson.

---

## Riesgos identificados / a monitorear

| Riesgo | Mitigación planeada |
|--------|---------------------|
| Frequency Encoding pierde señal vs Target Encoding | Alternativa lista para Día 5 si métricas no llegan |
| `pliego_*` con 98% NaN puede no aportar | Día 4: comparativa con/sin esos features |
| 94 cols puede ser ruido | Día 4: feature importance + selección si hace sentido |

---

## Próximo (Día 3)

Notebook `03_baselines.ipynb`:
1. **Logistic Regression** (con StandardScaler en pipeline) — baseline interpretable
2. **Random Forest** (default + `class_weight='balanced'`)
3. **XGBoost** (default, maneja NaN nativamente — pero ya están imputados)
4. Métricas en test: AUC-ROC, F1, Precision, Recall, Confusion Matrix
5. Comparativa rápida en tabla
6. **Decisión**: pasar 1-2 modelos a tuning del Día 5

**Tiempo estimado**: 2-3 horas (incluye entrenamiento RF y XGB).
