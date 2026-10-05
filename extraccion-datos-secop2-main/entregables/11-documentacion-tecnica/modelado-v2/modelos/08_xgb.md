# Modelo 08 — XGBoost

**Notebook**: `notebooks/08_modelo_xgb.ipynb`
**Modelo persistido**: `data/modelos/xgb.pkl`

## Configuración

- **Familia**: Boosting
- **Escalado**: no
- **Estrategia**: `RandomizedSearchCV` con `n_iter = 50`,
  `cv = StratifiedKFold(5)`, `scoring = 'roc_auc'`
- **Tiempo de búsqueda**: 185.7 s

## Descripción

Gradient boosting SOTA tabular. tree_method=hist.

## Resultados (test set, target `tuvo_atraso`)

| Métrica | Valor |
|---------|-------|
| CV AUC | 0.9085 |
| Test AUC | **0.9069** |
| F1 | 0.8500 |
| Precision | 0.8765 |
| Recall | 0.8250 |
| Accuracy | 0.8238 |

## Mejores hiperparámetros

- `colsample_bytree`: `0.8886918084659492`
- `gamma`: `1.1799245987447788`
- `learning_rate`: `0.02389152997793864`
- `max_depth`: `10`
- `n_estimators`: `300`
- `reg_alpha`: `0.1355154055297656`
- `reg_lambda`: `0.16664091501238187`
- `subsample`: `0.7757346007463081`
