# Modelo 06 — Linear SVM (calibrado)

**Notebook**: `notebooks/06_modelo_svm.ipynb`
**Modelo persistido**: `data/modelos/svm.pkl`

## Configuración

- **Familia**: Margen
- **Escalado**: sí
- **Estrategia**: `RandomizedSearchCV` con `n_iter = 15`,
  `cv = StratifiedKFold(5)`, `scoring = 'roc_auc'`
- **Tiempo de búsqueda**: 222.67 s

## Descripción

SVM lineal con CalibratedClassifierCV para predict_proba. RBF inviable a 38k samples.

## Resultados (test set, target `tuvo_atraso`)

| Métrica | Valor |
|---------|-------|
| CV AUC | 0.8397 |
| Test AUC | **0.8381** |
| F1 | 0.8144 |
| Precision | 0.7705 |
| Recall | 0.8635 |
| Accuracy | 0.7619 |

## Mejores hiperparámetros

- `estimator__C`: `1.3311216080736887`
- `estimator__class_weight`: `None`
