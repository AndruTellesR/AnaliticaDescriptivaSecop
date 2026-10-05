# Modelo 05 — K-Nearest Neighbors

**Notebook**: `notebooks/05_modelo_knn.ipynb`
**Modelo persistido**: `data/modelos/knn.pkl`

## Configuración

- **Familia**: Distancia
- **Escalado**: sí
- **Estrategia**: `RandomizedSearchCV` con `n_iter = 25`,
  `cv = StratifiedKFold(5)`, `scoring = 'roc_auc'`
- **Tiempo de búsqueda**: 176.25 s

## Descripción

Clasifica por mayoría entre k vecinos más cercanos.

## Resultados (test set, target `tuvo_atraso`)

| Métrica | Valor |
|---------|-------|
| CV AUC | 0.8258 |
| Test AUC | **0.8333** |
| F1 | 0.8077 |
| Precision | 0.7565 |
| Recall | 0.8663 |
| Accuracy | 0.7505 |

## Mejores hiperparámetros

- `weights`: `distance`
- `n_neighbors`: `51`
- `metric`: `manhattan`
