# Modelo 09 — LightGBM

**Notebook**: `notebooks/09_modelo_lgbm.ipynb`
**Modelo persistido**: `data/modelos/lgbm.pkl`

## Configuración

- **Familia**: Boosting
- **Escalado**: no
- **Estrategia**: `RandomizedSearchCV` con `n_iter = 50`,
  `cv = StratifiedKFold(5)`, `scoring = 'roc_auc'`
- **Tiempo de búsqueda**: 379.78 s

## Descripción

Gradient boosting con leaf-wise growth e histogramas.

## Resultados (test set, target `tuvo_atraso`)

| Métrica | Valor |
|---------|-------|
| CV AUC | 0.9094 |
| Test AUC | **0.9091** |
| F1 | 0.8503 |
| Precision | 0.8730 |
| Recall | 0.8288 |
| Accuracy | 0.8235 |

## Mejores hiperparámetros

- `colsample_bytree`: `0.8159364365206693`
- `learning_rate`: `0.019950144748611585`
- `max_depth`: `-1`
- `min_child_samples`: `50`
- `n_estimators`: `800`
- `num_leaves`: `127`
- `subsample`: `0.6644885149016018`
