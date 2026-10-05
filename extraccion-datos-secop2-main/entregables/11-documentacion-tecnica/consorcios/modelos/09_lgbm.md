# Documento 09 — LightGBM

**Notebook**: `notebooks/09_modelo_lgbm.ipynb`
**Familia**: Ensamble por boosting (eficiente)
**Target optimizado**: `tuvo_atraso`
**Modelo persistido**: `data/modelos/lgbm.pkl`

## Descripción del algoritmo

Variante de gradient boosting que crece los árboles por hoja en lugar de por nivel. Eficiente para datasets medianos. No requiere escalado.

## Configuración

- `RandomizedSearchCV` con `n_iter = 50`
- `StratifiedKFold(5)`
- Scoring: `roc_auc`
- `random_state = 42`

## Métricas sobre test (20 % stratified)

| Métrica | Valor |
|---------|-------|
| AUC test | 0.8627 |
| F1       | 0.7478 |
| Precision | 0.7794 |
| Recall   | 0.7187 |
| Accuracy | 0.7836 |
| AUC CV (mejor)   | 0.8786 |

## Mejores hiperparámetros

- `colsample_bytree`: 0.713936197750987
- `learning_rate`: 0.011336695817840537
- `max_depth`: -1
- `min_child_samples`: 20
- `n_estimators`: 300
- `num_leaves`: 127
- `subsample`: 0.6205915004999957

## Tiempo de búsqueda

819.94 segundos.
