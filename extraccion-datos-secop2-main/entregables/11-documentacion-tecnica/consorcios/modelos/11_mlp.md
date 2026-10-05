# Documento 11 — Multi-Layer Perceptron

**Notebook**: `notebooks/11_modelo_mlp.ipynb`
**Familia**: Red neuronal
**Target optimizado**: `tuvo_atraso`
**Modelo persistido**: `data/modelos/mlp.pkl`

## Descripción del algoritmo

Red neuronal feedforward con dos a tres capas ocultas. Early stopping activo para evitar sobreajuste. Necesita escalado.

## Configuración

- `RandomizedSearchCV` con `n_iter = 25`
- `StratifiedKFold(5)`
- Scoring: `roc_auc`
- `random_state = 42`

## Métricas sobre test (20 % stratified)

| Métrica | Valor |
|---------|-------|
| AUC test | 0.8074 |
| F1       | 0.6789 |
| Precision | 0.7431 |
| Recall   | 0.6249 |
| Accuracy | 0.7361 |
| AUC CV (mejor)   | 0.8248 |

## Mejores hiperparámetros

- `activation`: tanh
- `alpha`: 3.521342459487091e-05
- `hidden_layer_sizes`: [100, 50]
- `learning_rate_init`: 0.0004201672054372534

## Tiempo de búsqueda

59.02 segundos.
