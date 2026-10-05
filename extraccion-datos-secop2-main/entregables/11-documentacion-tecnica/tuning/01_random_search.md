# Estrategia 01 — Random Search

**Notebook**: `notebooks/01_random_search.ipynb`
**Librería**: `sklearn.model_selection.RandomizedSearchCV`

## Idea

Muestrea N combinaciones aleatorias del espacio de hiperparámetros y
evalúa cada una con K-Fold CV. No asume estructura del espacio. Sirve
como referencia estadística contra la cual comparar métodos más
sofisticados.

## Configuración

- `n_iter = 80`
- `cv = StratifiedKFold(5)`
- `scoring = 'roc_auc'`
- `random_state = 42`
- `n_jobs = -1`

## Espacio de búsqueda

| Hiperparámetro | Distribución |
|----------------|--------------|
| `n_estimators` | `{200, 300, 500, 800}` |
| `max_depth` | `{4, 6, 8, 10, 12}` |
| `learning_rate` | `loguniform(0.01, 0.3)` |
| `subsample` | `uniform(0.6, 1.0)` |
| `colsample_bytree` | `uniform(0.6, 1.0)` |
| `gamma` | `uniform(0, 5)` |
| `reg_lambda` | `loguniform(0.1, 10)` |
| `reg_alpha` | `loguniform(0.001, 1.0)` |

## Resultados

(Se actualizan tras la ejecución; ver `data/resultados_tuning.json`
entrada `random_search`.)

## Ventajas

- Implementación nativa en scikit-learn, sin dependencias adicionales.
- Reproducible con `random_state`.
- Cubre el espacio de manera uniforme.

## Limitaciones

- No aprende de iteraciones previas: gasta presupuesto en zonas
  ya conocidas como pobres.
- Necesita un n_iter grande para converger.
