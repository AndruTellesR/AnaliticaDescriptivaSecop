# Documento 08 — XGBoost

**Notebook**: `notebooks/08_modelo_xgb.ipynb`
**Familia**: Ensamble por boosting
**Target optimizado**: `tuvo_atraso`
**Modelo persistido**: `data/modelos/xgb.pkl`

## Descripción del algoritmo

Gradient boosting con regularización L1/L2, manejo nativo de NaN (aquí ya imputados) y histogram-based splitting (`tree_method=hist`).

## Configuración

- `RandomizedSearchCV` con `n_iter = 50`
- `StratifiedKFold(5)`
- Scoring: `roc_auc`
- `random_state = 42`

## Métricas sobre test (20 % stratified)

| Métrica | Valor |
|---------|-------|
| AUC test | 0.863 |
| F1       | 0.7499 |
| Precision | 0.7765 |
| Recall   | 0.725 |
| Accuracy | 0.7841 |
| AUC CV (mejor)   | 0.8797 |

## Mejores hiperparámetros

- `colsample_bytree`: 0.7975574860733738
- `gamma`: 0.8941135461066441
- `learning_rate`: 0.03477913936744648
- `max_depth`: 10
- `n_estimators`: 500
- `reg_lambda`: 2.7661762518652755
- `subsample`: 0.7232243167409557

## Tiempo de búsqueda

25.27 segundos.
