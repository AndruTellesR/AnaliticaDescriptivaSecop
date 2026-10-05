# Documento 05 — K-Nearest Neighbors

**Notebook**: `notebooks/05_modelo_knn.ipynb`
**Familia**: Modelo basado en distancia
**Target optimizado**: `tuvo_atraso`
**Modelo persistido**: `data/modelos/knn.pkl`

## Descripción del algoritmo

Clasificación por mayoría ponderada entre los k vecinos más cercanos. Necesita escalado. Sensible a la cardinalidad alta del feature space.

## Configuración

- `RandomizedSearchCV` con `n_iter = 30`
- `StratifiedKFold(5)`
- Scoring: `roc_auc`
- `random_state = 42`

## Métricas sobre test (20 % stratified)

| Métrica | Valor |
|---------|-------|
| AUC test | 0.7497 |
| F1       | 0.619 |
| Precision | 0.6909 |
| Recall   | 0.5606 |
| Accuracy | 0.6919 |
| AUC CV (mejor)   | 0.7661 |

## Mejores hiperparámetros

- `weights`: distance
- `n_neighbors`: 31
- `metric`: manhattan

## Tiempo de búsqueda

8.81 segundos.
