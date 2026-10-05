# Tuning de hiperparámetros — modelo global multi-target

Sub-proyecto: ejecuta y compara cuatro estrategias de búsqueda de
hiperparámetros sobre el modelo XGBoost del sprint padre, con el fin
de superar las métricas de baseline (AUC 0,9035 atraso / 0,832 sobrecosto)
y dejar un único modelo afinado para producción.

## Modelo objetivo

- **Algoritmo**: XGBoost
- **Universo**: 48.331 contratos de obra pública (sin filtro de consorcios)
- **Targets**: `tuvo_atraso` (principal) y `tuvo_sobrecosto`
- **Features**: 30 columnas seleccionadas (output del Día 4b del sprint padre)
- **Split**: 80/20 stratified sobre `tuvo_atraso`, `random_state = 42`

## Estrategias evaluadas

| # | Estrategia | Librería | Idea central |
|---|------------|----------|--------------|
| 01 | Random Search | sklearn | Combinaciones aleatorias del espacio. Baseline. |
| 02 | Halving Random Search | sklearn (`HalvingRandomSearchCV`) | Asigna pocos recursos a muchos candidatos, descarta los peores y promueve los buenos a más recursos. |
| 03 | Bayesian (TPE) | Optuna | Aprende del histórico de trials, sugiere combinaciones prometedoras. |
| 04 | Grid Search reducido | sklearn | Grid manual diseñado con los mejores params del sprint consorcios. |

## Espacio de búsqueda (común a las cuatro)

```python
{
    'n_estimators':     [200, 300, 500, 800],
    'max_depth':        [4, 6, 8, 10, 12],
    'learning_rate':    loguniform(0.01, 0.3),
    'subsample':        uniform(0.6, 0.4),     # [0.6, 1.0]
    'colsample_bytree': uniform(0.6, 0.4),     # [0.6, 1.0]
    'gamma':            uniform(0, 5),
    'reg_lambda':       loguniform(0.1, 10),
    'reg_alpha':        loguniform(0.001, 1.0),
}
```

## Configuración estándar

- `n_iter / n_trials = 80` (las cuatro estrategias)
- `cv = StratifiedKFold(5)`
- `scoring = 'roc_auc'`
- `random_state = 42`
- `n_jobs = -1`

## Criterio de selección

1. **AUC CV máximo** sobre `tuvo_atraso`.
2. Empate técnico (Δ < 0,003) → menor desviación estándar entre folds.
3. Persistencia → menor tiempo de búsqueda.

Solo la estrategia ganadora se evalúa sobre el test set (para evitar
sobre-ajuste a la decisión).

## Estructura

```
tuning/
├── README.md
├── notebooks/
│   ├── 01_random_search.ipynb
│   ├── 02_halving_random.ipynb
│   ├── 03_bayesian_optuna.ipynb
│   ├── 04_grid_search.ipynb
│   └── 05_comparativa.ipynb
├── docs/
│   ├── 00_plan.md
│   └── 01..05_*.md
├── data/
│   └── modelos/         (xgb_tuned_<estrategia>.pkl)
└── figuras/
```

## Hipótesis previas

- Optuna (TPE) debería superar a Random Search por la exploración guiada.
- Halving Random reduce tiempo de búsqueda ~3-5× sin perder calidad.
- Grid reducido es competitivo si la región óptima del sprint consorcios
  generaliza al universo completo.
- Mejora esperada: +0,005 a +0,015 en AUC test (de 0,9035 a 0,91-0,92).
