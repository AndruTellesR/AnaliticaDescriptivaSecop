# Estrategia 02 — Halving Random Search

**Notebook**: `notebooks/02_halving_random.ipynb`
**Librería**: `sklearn.model_selection.HalvingRandomSearchCV`
(detrás del flag experimental `enable_halving_search_cv`)

## Idea

Successive Halving: en la primera ronda, evalúa muchos candidatos con
**pocos recursos** (por ejemplo, una submuestra pequeña de los datos).
Descarta los peores y promueve los mejores a la siguiente ronda con
**más recursos**. Repite hasta dejar un ganador entrenado con el
recurso completo.

Recursos = `n_samples` (subsampling progresivo del train).

## Configuración

- `n_candidates = 80`
- `factor = 3` (tras cada ronda promueve 1/3 de los candidatos)
- `resource = 'n_samples'`
- `cv = StratifiedKFold(5)`
- `scoring = 'roc_auc'`

## Espacio de búsqueda

Idéntico al de Random Search (ver `01_random_search.md`).

## Resultados

(Se actualizan tras la ejecución; ver `data/resultados_tuning.json`
entrada `halving_random`.)

## Ventajas

- Mucho más rápido que Random Search: la mayoría de evaluaciones
  ocurren con datasets pequeños.
- Mantiene la cobertura del espacio del Random Search.

## Limitaciones

- Los candidatos descartados temprano podrían haber sido buenos con
  más datos (decisiones tempranas sesgadas a configuraciones que
  rinden bien con poco dato).
- Hyperparámetros propios (`factor`, `resource`, `max_resources`) que
  añaden complejidad al diseño.
