# Documento 05 — Comparativa final del tuning multi-estrategia

**Notebook**: `notebooks/05_comparativa.ipynb`
**Inputs**: `data/resultados_tuning.json`, `data/modelos/xgb_tuned_*.pkl`
**Outputs**:
- `data/comparativa_tuning.csv`
- `data/metricas_test_ganador.csv`
- `data/RESULTADO_FINAL.json`
- `data/modelos/xgb_tuned_FINAL.pkl`
- `figuras/tuning_cv_auc.png`

## Tabla comparativa CV (target = `tuvo_atraso`)

| # | Estrategia | CV AUC | CV std | Tiempo | n_iter |
|---|------------|--------|--------|--------|--------|
| 1 | bayesian_optuna | 0,9103 | 0,00263 | 328,69 s | 80 trials |
| 2 | **grid_search** | **0,9101** | **0,00258** | 434,70 s | 288 combos |
| 3 | random_search | 0,9089 | 0,00267 | 87,86 s | 80 iters |
| 4 | halving_random | 0,8293 | 0,02337 | 9,52 s | 119 candidatos efectivos |

## Selección de la ganadora

Criterio aplicado:
1. AUC CV máximo (Optuna 0,9103).
2. Empate técnico (Δ < 0,003): Optuna y Grid Search caen dentro.
3. Desempate por menor std entre folds (estabilidad):
   - Grid Search: 0,00258
   - Optuna: 0,00263
4. **Ganadora**: `grid_search`

Comentario: el resultado favorece al grid manual construido a partir
de los mejores parámetros del sprint consorcios. La región óptima
encontrada en el sub-universo (XGB consorcios AUC 0,8630) generalizó
correctamente al universo completo. El método bayesiano encontró un
óptimo virtualmente idéntico, pero con marginalmente más varianza
entre folds.

## Análisis por estrategia

### Bayesian Optuna (TPE)

Lideró en CV AUC. Los mejores params:

```
n_estimators=800, max_depth=12, learning_rate=0.0187,
subsample=0.929, colsample_bytree=0.863, gamma=0.219,
reg_lambda=1.136, reg_alpha=0.0110
```

Configuración profunda (depth 12, 800 estimators) con learning rate
muy bajo (0,019). Compromete tiempo de inferencia futuro por modelo
más grande sin ventaja estadística sobre la alternativa Grid.

### Grid Search reducido (ganador)

Best params:

```
n_estimators=500, max_depth=10, learning_rate=0.03,
subsample=0.7, colsample_bytree=0.7, gamma=0.5, reg_lambda=1.0
```

Modelo más compacto que Optuna (500 vs 800 árboles, depth 10 vs 12),
con learning rate 0,03 y subsampling agresivo (0,7 / 0,7) para
regularización por bagging. Resultado: misma capacidad predictiva,
menor varianza, más eficiente en inferencia.

### Random Search (n=80)

Resultado competitivo (0,9089) en una fracción del tiempo (88 s).
Si el presupuesto computacional fuera el factor crítico, Random Search
sería la elección práctica. Diferencia vs ganador: 0,0012 AUC, perdible
para muchos casos de uso.

### Halving Random Search (fracaso)

AUC 0,8293 ± 0,0234. Significativamente por debajo del baseline sin
tuning (0,9035). El método descartó tempranamente configuraciones que
requerían más muestras para mostrar su verdadero valor (en particular
las de alto `n_estimators` y bajo `learning_rate`, sensibles al tamaño
del train). Confirma la limitación conocida del método para
hiperparámetros que interactúan con el volumen de datos.

**Lección**: Halving Random no es apropiado cuando los HP relevantes
escalan con `n_samples`. Reservado para casos donde el cuello de
botella sea computacional y los HP no dependan del tamaño del fit.

## Métricas de la ganadora sobre test (Grid Search)

| Target | AUC | F1 | Precision | Recall | Accuracy |
|--------|-----|------|-----------|--------|----------|
| `tuvo_atraso` | **0,9088** | 0,8522 | 0,8778 | 0,8281 | 0,8263 |
| `tuvo_sobrecosto` | **0,8358** | 0,8508 | 0,9282 | 0,7853 | 0,7715 |

## Mejora vs baselines del sprint padre

| Modelo | Target | AUC | Δ vs baseline |
|--------|--------|-----|----------------|
| RF multi baseline | atraso | 0,9047 | (ref) |
| XGB multi baseline | atraso | 0,9035 | −0,0012 |
| **XGB tuned (Grid)** | atraso | **0,9088** | **+0,0041 vs RF baseline** |
| RF multi baseline | sobrecosto | 0,8342 | (ref) |
| XGB multi baseline | sobrecosto | 0,8319 | −0,0023 |
| **XGB tuned (Grid)** | sobrecosto | **0,8358** | **+0,0016 vs RF baseline** |

**Conclusión técnica**: el XGBoost calibrado con Grid Search supera
por primera vez al Random Forest baseline en ambos targets. Por
diferencia pequeña pero consistente, el modelo XGB tuned reemplaza a
RF como modelo de producción del sprint padre.

## Best params finales (XGB tuned FINAL)

```json
{
  "n_estimators":     500,
  "max_depth":        10,
  "learning_rate":    0.03,
  "subsample":        0.7,
  "colsample_bytree": 0.7,
  "gamma":            0.5,
  "reg_lambda":       1.0
}
```

`scale_pos_weight` se calcula por target (1,653 para atraso, 0,197 para
sobrecosto) — multi-target queda como dos XGBs separados con los
mismos HP de árbol pero `scale_pos_weight` específico de cada target.

## Modelo final

`data/modelos/xgb_tuned_FINAL.pkl` contiene un dict:

```python
{
    'atraso':     XGBClassifier(...),
    'sobrecosto': XGBClassifier(...),
    'params':     <best_params>,
}
```

Cargar y predecir:

```python
import joblib
mods = joblib.load('xgb_tuned_FINAL.pkl')
proba_atraso     = mods['atraso'].predict_proba(X_new)[:, 1]
proba_sobrecosto = mods['sobrecosto'].predict_proba(X_new)[:, 1]
```

## Pendientes derivados

1. Comparar mejor threshold (no 0,50) para cada target según el costo
   asimétrico FP/FN. Pertinente para Día 7 (evaluación final).
2. Calibración de probabilidades (Platt scaling o isotonic regression).
3. Análisis SHAP sobre el modelo final para interpretabilidad.
