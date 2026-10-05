# Modelo 11 — Multi-Layer Perceptron

**Notebook**: `notebooks/11_modelo_mlp.ipynb`
**Modelo persistido**: `data/modelos/mlp.pkl`

## Configuración

- **Familia**: Red neuronal
- **Escalado**: sí
- **Estrategia**: `RandomizedSearchCV` con `n_iter = 20`,
  `cv = StratifiedKFold(5)`, `scoring = 'roc_auc'`
- **Tiempo de búsqueda**: 86.23 s

## Descripción

Red feed-forward con backpropagation. Early stopping para evitar overfitting.

## Resultados (test set, target `tuvo_atraso`)

| Métrica | Valor |
|---------|-------|
| CV AUC | 0.8700 |
| Test AUC | **0.8630** |
| F1 | 0.8263 |
| Precision | 0.8147 |
| Recall | 0.8382 |
| Accuracy | 0.7868 |

## Mejores hiperparámetros

- `activation`: `relu`
- `alpha`: `0.003363987115958792`
- `hidden_layer_sizes`: `[100, 100]`
- `learning_rate_init`: `0.007568292060167619`
