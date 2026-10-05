# Documento 02 — Comparativa de imputación

**Notebook**: `notebooks/02_imputacion_comparativa.ipynb`
**Inputs**: `data/consorcios_base.parquet` (10.629 × 38)
**Outputs**:

| Archivo | Descripción |
|---------|-------------|
| `data/consorcios_imputado.parquet` | Alias al dataset imputado con la estrategia ganadora |
| `data/consorcios_imputado_mediana.parquet` | Versión explícita con sufijo de estrategia |
| `data/comparativa_imputacion.csv` | Tabla con AUC, F1, nMAE y tiempos por estrategia |
| `data/recon_mae_por_col.csv` | MAE de reconstrucción desglosado por columna |
| `data/imputers/imputer_mediana.pkl` | Imputador entrenado (estrategia ganadora) |
| `data/imputers/freq_maps.pkl` | Mapas de Frequency Encoding (`departamento`, `ciudad`) |
| `data/imputers/winsor_limits.pkl` | Límites p1 / p99 aplicados a `pliego_*` |
| `figuras/dia_02_recon_nmae.png` | nMAE por columna y estrategia |
| `figuras/dia_02_auc_downstream.png` | AUC downstream por estrategia |

## Preprocesamiento previo a la imputación

1. **Drop de `rup_*`** (5 columnas): todas las observaciones en consorcios
   son NaN (registro RUP no aplica a consorcios). Justificación detallada
   en `01_dataset.md`.

2. **Normalización de formato mixto** en `pliego_endeudamiento_max_pct`:
   los valores en formato fracción (`≤ 1`) se multiplicaron por 100 para
   homogeneizar con los valores en formato porcentaje. El rango resultante
   quedó en una sola unidad (porcentaje), evitando que el imputador trate
   ambos formatos como observaciones contradictorias.

3. **Winsorización p1 / p99** sobre las seis columnas `pliego_*`: los
   valores fuera del rango [p1, p99] se recortaron a esos extremos. Los
   límites se persistieron en `imputers/winsor_limits.pkl` para reproducir
   la transformación en inferencia. Esto neutraliza outliers conocidos:
   - `capital_trabajo_min_pct_presupuesto`: max ~10¹¹ (error de extracción)
   - `cobertura_intereses_min`: min ~−10³ (error de signo)

4. **Encoding mínimo previo**: One-Hot Encoding para las categóricas con
   cardinalidad < 20 (la mayoría) y Frequency Encoding para `departamento`
   y `ciudad` (alta cardinalidad). Los mapas se serializaron en
   `freq_maps.pkl`. El resultado son **79 features** efectivas
   (numéricas + OHE + Freq + flags `_was_nan` cuando aplica).

## Estrategias evaluadas

| Código | Algoritmo | Hiperparámetros |
|--------|-----------|-----------------|
| `mediana` | `SimpleImputer(strategy='median')` + flag `_was_nan` | — |
| `knn`     | `KNNImputer` | k=5, `weights='distance'` |
| `mice_br` | `IterativeImputer` con `BayesianRidge` | `max_iter=10` |
| `mice_rf` | `IterativeImputer` con `RandomForestRegressor` | `n_estimators=30`, `max_depth=10`, `max_iter=5` |

Para KNN y los dos MICE se aplica `StandardScaler` antes y se invierte tras
la imputación, asegurando que las distancias y los modelos lineales operen
en escala homogénea.

## Evaluación dual

### Evaluación 1 — Reconstrucción artificial

Sobre los registros con todas las columnas `pliego_*` y `duracion_planificada_dias`
completas, se enmascaró el 30 % de los valores al azar (`random_state=42`)
y se midió el MAE normalizado por el rango de cada columna (`nMAE`).

### Evaluación 2 — AUC downstream

Split estratificado 80/20 sobre el target `tuvo_atraso`. Cada estrategia
ajusta el imputador sobre el train y transforma train y test. Se entrena
un XGBoost idéntico (`n_estimators=300`, `max_depth=6`, `lr=0.1`,
`scale_pos_weight` calculado) y se reporta el AUC y F1 sobre test.

## Resultados

| Estrategia | AUC (test) | F1 | nMAE | Tiempo imputación |
|------------|------------|------|--------|-------------------|
| **mediana** | **0,8542** | **0,7281** | 0,1013 | 0,02 s |
| knn        | 0,8093 | 0,7063 | 0,0846 | 6,09 s |
| mice_br    | 0,8066 | 0,6910 | 0,0748 | 44,32 s |
| mice_rf    | 0,8015 | 0,6878 | **0,0596** | 33,65 s |

### Hallazgo central

Los métodos sofisticados (MICE-RF, MICE-BR, KNN) reconstruyen mejor los
valores enmascarados (nMAE 0,06 frente a 0,10 de la mediana) pero
**generan peor capacidad predictiva downstream** (AUC 0,80 frente a 0,85
de la mediana). Esta paradoja se explica porque la mediana añade el flag
binario `_was_nan` como columna adicional, mientras que los métodos
sofisticados borran esa información al producir un valor "razonable".

En este dataset el **patrón de ausencia es más informativo que el valor
estimado**: que un pliego no haya podido extraerse codifica
implícitamente características del proceso (modalidad, tipo de entidad,
formato del PDF) que correlacionan con el target.

### Interpretación práctica

- La extracción del pliego no es aleatoria: depende del tipo de proceso y
  del formato documental. Esa no aleatoriedad es señal.
- Un imputador que "tape el hueco" con un valor plausible cubre el patrón
  de ausencia y, por tanto, degrada el modelo final.
- La mediana + flag `_was_nan` aprovecha ambos mundos: valor por defecto
  para que XGBoost no falle, y una columna explícita que señaliza el
  origen del dato.

## Decisión

**Estrategia ganadora: `mediana` + flag `_was_nan`**

Criterio aplicado: AUC downstream como métrica primaria (diferencia de
0,045 sobre la segunda, muy por encima del umbral de empate técnico de
0,003). Se mantiene el resultado del sprint padre y se descarta la
sospecha de que un método más sofisticado fuera necesario.

## Dataset final imputado

| Métrica | Valor |
|---------|-------|
| Filas | 10.629 |
| Columnas (features) | 79 |
| NaN restantes | 0 |
| Flags `_was_nan` agregadas | 7 |

Cobertura de flags `_was_nan` (señalan ausencia original):

| Columna | Flags = 1 |
|---------|-----------|
| `duracion_planificada_dias_was_nan` | 1.223 |
| `pliego_liquidez_min_was_nan` | 6.752 |
| `pliego_endeudamiento_max_pct_was_nan` | 6.771 |
| `pliego_cobertura_intereses_min_was_nan` | 6.963 |
| `pliego_rentabilidad_patrimonio_min_pct_was_nan` | 6.938 |
| `pliego_rentabilidad_activo_min_pct_was_nan` | 6.953 |
| `pliego_capital_trabajo_min_pct_presupuesto_was_nan` | 9.262 |

## Próximo paso

Notebook 03 — análisis preliminar sobre el dataset imputado:

- Distribuciones de los seis indicadores `pliego_*` tras winsorización.
- Cruces `departamento × modalidad × pliego × target` para validar la
  pregunta del director: ¿qué indicadores mínimos exige cada tipo de
  contrato en cada departamento, y qué probabilidad de éxito tienen los
  consorcios que los cumplen?
- Correlación entre `pliego_*` y los dos targets.
- Importancia preliminar de features (Mutual Information).
