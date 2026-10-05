# Documento 06 — Support Vector Machine

**Notebook**: `notebooks/06_modelo_svm.ipynb`
**Familia**: Modelo de margen máximo
**Target optimizado**: `tuvo_atraso`
**Modelo persistido**: `data/modelos/svm.pkl`

## Descripción del algoritmo

Maximiza el margen entre clases. Probado con kernel RBF y lineal. Probabilidades calibradas internamente. Necesita escalado.

## Configuración

- `RandomizedSearchCV` con `n_iter = 12`
- `StratifiedKFold(5)`
- Scoring: `roc_auc`
- `random_state = 42`

## Métricas sobre test (20 % stratified)

| Métrica | Valor |
|---------|-------|
| AUC test | 0.8058 |
| F1       | 0.6786 |
| Precision | 0.7226 |
| Recall   | 0.6396 |
| Accuracy | 0.7295 |
| AUC CV (mejor)   | 0.816 |

## Mejores hiperparámetros

- `C`: 6.358358856676251
- `class_weight`: balanced
- `gamma`: auto
- `kernel`: rbf

## Tiempo de búsqueda

771.14 segundos.
