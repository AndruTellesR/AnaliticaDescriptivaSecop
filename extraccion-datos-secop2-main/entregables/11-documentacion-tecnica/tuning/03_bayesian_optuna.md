# Estrategia 03 — Bayesian Optimization (Optuna TPE)

**Notebook**: `notebooks/03_bayesian_optuna.ipynb`
**Librería**: `optuna 4.8.0`

## Idea

Tree-structured Parzen Estimator (TPE): mantiene dos densidades
condicionales sobre el espacio de hiperparámetros — una para
configuraciones "buenas" y otra para "malas" — y propone la siguiente
configuración a evaluar que maximiza el ratio entre ambas. En la
práctica, **aprende del histórico de trials** y enfoca la búsqueda en
zonas prometedoras del espacio.

A diferencia de Random Search y Halving, Bayesian no muestrea
uniformemente: cada trial se basa en lo aprendido en trials previos.

## Configuración

- `n_trials = 80`
- `sampler = TPESampler(seed=42)`
- `cv = StratifiedKFold(5)`
- `scoring = 'roc_auc'`
- `direction = 'maximize'`

## Espacio de búsqueda

Definido vía `trial.suggest_*`:

| Hiperparámetro | API |
|----------------|-----|
| `n_estimators` | `suggest_categorical({200, 300, 500, 800})` |
| `max_depth` | `suggest_categorical({4, 6, 8, 10, 12})` |
| `learning_rate` | `suggest_float(0.01, 0.3, log=True)` |
| `subsample` | `suggest_float(0.6, 1.0)` |
| `colsample_bytree` | `suggest_float(0.6, 1.0)` |
| `gamma` | `suggest_float(0, 5)` |
| `reg_lambda` | `suggest_float(0.1, 10, log=True)` |
| `reg_alpha` | `suggest_float(0.001, 1.0, log=True)` |

## Resultados

(Se actualizan tras la ejecución; ver `data/resultados_tuning.json`
entrada `bayesian_optuna`.)

## Ventajas

- Convergencia más rápida que Random Search en igual presupuesto.
- Mejor manejo de espacios mixtos (continuos + categóricos).
- Permite condicionar hiperparámetros y definir constrains.

## Limitaciones

- Sensible al tamaño inicial de "exploración aleatoria" (TPE necesita
  10-20 trials previos para estabilizar su modelo interno).
- Dependencia externa (`optuna`).
- No paraleliza tan limpiamente como Random Search.
