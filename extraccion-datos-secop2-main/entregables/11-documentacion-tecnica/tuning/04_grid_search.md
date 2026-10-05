# Estrategia 04 — Grid Search reducido

**Notebook**: `notebooks/04_grid_search.ipynb`
**Librería**: `sklearn.model_selection.GridSearchCV`

## Idea

Grid Search clásico sobre un grid manual de valores **discretos
seleccionados con criterio**. A diferencia de los demás métodos,
no muestrea aleatoriamente: evalúa **todas** las combinaciones del
grid. El truco está en armar un grid lo bastante pequeño para que
el tiempo sea manejable pero centrado en la región esperada como
óptima.

El grid de este experimento se construye a partir de los mejores
parámetros del sprint consorcios (XGB ganador, AUC 0,8630) sobre el
sub-universo, ampliando ligeramente cada eje.

## Configuración

- `cv = StratifiedKFold(5)`
- `scoring = 'roc_auc'`
- `n_jobs = -1`

## Grid

| Hiperparámetro | Valores |
|----------------|---------|
| `n_estimators` | `{300, 500}` |
| `max_depth` | `{6, 8, 10}` |
| `learning_rate` | `{0.03, 0.05, 0.1}` |
| `subsample` | `{0.7, 0.85}` |
| `colsample_bytree` | `{0.7, 0.85}` |
| `gamma` | `{0.5, 1.0}` |
| `reg_lambda` | `{1.0, 3.0}` |

Total: 288 combinaciones × 5 folds = 1.440 fits. Con XGB `tree_method='hist'`
sobre 38.664 train × 30 features, ~1 segundo por fit ⇒ ~24 minutos.

## Resultados

(Se actualizan tras la ejecución; ver `data/resultados_tuning.json`
entrada `grid_search`.)

## Ventajas

- Determinístico: mismo grid produce mismo resultado.
- Fácil de razonar: sabes exactamente qué combinaciones se evaluaron.
- Útil para validar hallazgos de métodos aleatorios.

## Limitaciones

- Crece exponencialmente con la dimensión del grid.
- No explora regiones fuera del grid.
- Si la región óptima del sprint consorcios no generaliza al universo
  completo, el grid puede quedar mal centrado y reportar AUC inferior
  a los métodos exploratorios.
