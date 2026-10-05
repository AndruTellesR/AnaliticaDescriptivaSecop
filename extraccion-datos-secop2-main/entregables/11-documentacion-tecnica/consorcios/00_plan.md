# Plan — modelo predictivo Consorcios

## Motivación

El modelo global (sprint padre) alcanzó AUC 0,9047 (atraso) y 0,834
(sobrecosto) sobre los 48.331 contratos. Dos observaciones empíricas
motivan un modelo especializado a consorcios:

1. Los consorcios tienen un comportamiento de riesgo distinto:
   tasa de atraso 44,6 % vs 60,5 % global y tasa de sobrecosto
   77,9 % vs 83,4 % global.
2. La cobertura de los indicadores financieros del pliego (`pliego_*`)
   es 36,5 % en consorcios frente a apenas 8 % en el universo total.

Hipótesis: especializar el modelo al sub-universo permite explotar la
mayor cobertura de variables financieras, posiblemente subiendo AUC
en sobrecosto (target con peor desempeño hoy).

## Universo

- `es_grupo = "Si"` → 10.629 contratos.
- Sin más filtros.

## Targets

- `tuvo_atraso` (derivado de `tiempo`)
- `tuvo_sobrecosto` (derivado de `presupuesto`)

Multi-target manteniendo arquitectura validada en el sprint padre.

## Guía técnica (de `pasos.md`)

El líder pidió cubrir el espectro completo:

1. **Preprocesamiento**: imputación, encoding, escalado.
2. **Zoológico de algoritmos**: representante por familia.
3. **Grid de hiperparámetros** por modelo.
4. **K-Fold CV** (K=5) estratificado.
5. **Loop maestro**: `RandomizedSearchCV` para evitar tiempos prohibitivos.
6. **Comparativa final**: F1 / AUC priorizados.

Adaptaciones:

- Cada modelo en su propio notebook (orden y trazabilidad).
- Pre-procesamiento común extraído a `src/preprocesamiento.py`.
- Imputación elegida tras comparativa formal (notebook 02), no por defecto.

## Fases

| Fase | Notebook(s) | Output esperado |
|------|-------------|-----------------|
| 1. Dataset | 01 | `consorcios_base.parquet` (10.629 × N) |
| 2. Imputación | 02 | `consorcios_imputado_<ganador>.parquet` + decisión documentada |
| 3. Análisis preliminar | 03 | Figuras, tablas cruzadas, hallazgos |
| 4. Modelado | 04–11 | 8 modelos entrenados con mejores hiperparámetros |
| 5. Comparativa | 12 | Tabla métricas + selección modelo ganador |

## Algoritmos del zoológico

| ID | Algoritmo | Hiperparámetros (clave) | Necesita escalado |
|----|-----------|-------------------------|-------------------|
| 04 | Logistic Regression | `C`, `penalty`, `solver` | Sí |
| 05 | KNN | `n_neighbors`, `weights`, `metric` | Sí |
| 06 | SVM (RBF / lineal) | `C`, `gamma`, `kernel` | Sí |
| 07 | Random Forest | `n_estimators`, `max_depth`, `min_samples_leaf` | No |
| 08 | XGBoost | `learning_rate`, `max_depth`, `subsample`, `colsample_bytree` | No |
| 09 | LightGBM | `learning_rate`, `num_leaves`, `min_child_samples` | No |
| 10 | Naive Bayes (Gaussian) | `var_smoothing` | Sí |
| 11 | MLP | `hidden_layer_sizes`, `alpha`, `learning_rate_init` | Sí |

## Estrategia de búsqueda

`RandomizedSearchCV` por modelo:

- `n_iter = 40` (compromiso tiempo / cobertura espacio)
- `cv = StratifiedKFold(5)`
- `scoring = 'roc_auc'` (single-target por simplicidad; multi-target se hace al final con mejor configuración)
- `n_jobs = -1`
- `random_state = 42`

## Métricas reportadas (por modelo)

- AUC-ROC
- F1 (clase positiva)
- Precision
- Recall
- Accuracy
- Tiempo entrenamiento + tiempo búsqueda
- Mejores hiperparámetros

## Comparativa final (notebook 12)

Tabla unificada con todos los modelos. Ranking por AUC y por F1.
Selección del ganador. Análisis FP/FN del ganador. Curvas ROC y PR.

## Unificación con modelo global

**Pospuesta**. Primero terminar el modelo especializado, comparar contra
el global aplicado al subset consorcios, decidir después si se hace
ensemble o se queda como modelos paralelos.

## Estado

| Etapa | Estado |
|-------|--------|
| Estructura | ✅ |
| Plan | ✅ |
| Dataset (01) | ⏳ |
| Imputación (02) | ⏳ |
| Análisis preliminar (03) | ⏳ |
| Modelado (04–11) | ⏳ |
| Comparativa (12) | ⏳ |
