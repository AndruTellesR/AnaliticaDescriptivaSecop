# Plan — Tuning multi-estrategia del modelo global

## Contexto

El sprint padre cerró con XGB multi-target en baseline (sin tuning) con
AUC 0,9035 (atraso) y 0,832 (sobrecosto). El plan original contemplaba
Random Search de 80 iteraciones. Se amplía el experimento a cuatro
estrategias de búsqueda para comparar y quedarse con la mejor.

## Justificación de la elección XGB

- En sprint padre RF tenía AUC 0,9047 (ligeramente mayor que XGB 0,9035)
  pero RF tiene menos hiperparámetros tunables relevantes.
- XGB es más sensible al tuning: el sprint consorcios mostró ganancias
  de hasta 0,01-0,02 AUC con `RandomizedSearchCV`.
- Si XGB tuned supera RF baseline → XGB queda como producción.
- Si no, RF se mantiene como ganador histórico.

## Procedimiento estándar

1. Cargar `dataset_modelado.parquet` (48.331 × 42).
2. Reconstruir split estratificado con `random_state = 42` para tener
   ambos targets disponibles (`tuvo_atraso`, `tuvo_sobrecosto`).
3. Aplicar feature selection (30 cols del Día 4b).
4. Ejecutar la estrategia con 80 iteraciones / trials y CV 5-fold.
5. Persistir mejor estimador y métricas CV en `data/resultados_tuning.json`.
6. **No evaluar test** hasta el notebook 05 (comparativa).

## Métricas reportadas por estrategia

- `best_cv_auc`: media de los 5 folds para los mejores params.
- `cv_auc_std`: desviación estándar entre folds (estabilidad).
- `best_params`: dict de hiperparámetros óptimos.
- `tiempo_search_seg`: tiempo total de búsqueda.
- `n_iter_efectivo`: cuántas configuraciones se evaluaron realmente
  (en Halving es < n_iter por descarte temprano).

## Comparativa (notebook 05)

- Tabla maestra con las 4 estrategias.
- Selección ganadora.
- Reentrenamiento del ganador sobre train completo.
- Evaluación sobre test (`X_test_reducido` × `y_test`).
- Reentrenamiento como multi-target: aplicar mismos params a XGB sobre
  `tuvo_sobrecosto` con `MultiOutputClassifier`.
- Métricas test: AUC, F1, Precision, Recall sobre ambos targets.
- Persistencia del modelo final `xgb_tuned_FINAL.pkl`.

## Riesgos

- Overfitting al CV: por eso se mantiene test set intocado y se reporta
  std entre folds.
- Tiempo total: ~30-60 min por estrategia × 4 = 2-4h. Razonable.
- Optuna: dependencia nueva, ya instalada (`optuna 4.8.0`).

## Decisión post-tuning

Si AUC test ganador > 0,9047 (RF baseline) → XGB tuned reemplaza RF.
Si AUC test ganador ≤ 0,9047 → RF baseline queda, se documenta el
intento de tuning como evidencia de techo del XGB.
