# Documento 12 — Comparativa final del zoológico (global v2)

**Notebook**: `notebooks/12_comparativa_final.ipynb`
**Inputs**: `data/resultados_modelos.json`, `data/modelos/*.pkl`
**Outputs**: `data/comparativa_modelos.csv`, `data/metricas_test_ganador.csv`,
`data/RESULTADO_FINAL.json`, `figuras/12_*.png`

## Tabla maestra de resultados (target `tuvo_atraso`)

| # | Modelo | CV AUC | AUC test | F1 | Precision | Recall | Accuracy | Tiempo |
|---|--------|--------|----------|------|-----------|--------|----------|--------|
| 1 | **lgbm** | 0,9094 | **0,9091** | **0,8503** | 0,8672 | 0,8341 | 0,8268 | 380 s |
| 2 | xgb | 0,9085 | 0,9069 | 0,8500 | 0,8765 | 0,8250 | 0,8238 | 186 s |
| 3 | rf | 0,8982 | 0,8996 | 0,8489 | 0,8262 | 0,8729 | 0,8120 | 368 s |
| 4 | mlp | 0,8700 | 0,8630 | 0,8263 | 0,8147 | 0,8382 | 0,7868 | 86 s |
| 5 | lr | 0,8424 | 0,8402 | 0,7982 | 0,8243 | 0,7737 | 0,7634 | 93 s |
| 6 | svm | 0,8397 | 0,8381 | 0,8144 | 0,7705 | 0,8635 | 0,7619 | 223 s |
| 7 | knn | 0,8258 | 0,8333 | 0,8077 | 0,7565 | 0,8663 | 0,7505 | 176 s |
| 8 | nb | 0,7492 | 0,7519 | 0,3482 | 0,9952 | 0,2110 | 0,5222 | 8 s |

## Modelo ganador

**LightGBM** — `data/modelos/lgbm.pkl`

Selección:
- Mayor AUC test (0,9091).
- Empate técnico con XGB (Δ = 0,0022).
- LGBM tiene mejor F1 (0,8503 vs 0,8500) y AUC marginal por encima.
- Tiempo 2× XGB (380 vs 186 s) pero compensa por desempeño.

Mejores hiperparámetros (LGBM):
```
n_estimators=800, num_leaves=127, learning_rate=0.0200,
max_depth=-1, min_child_samples=50,
subsample=0.6645, colsample_bytree=0.8159
```

## Lecturas por familia

**Boosting (LGBM / XGB)**: empatados en cabeza ~0,907-0,909. LGBM gana
por la combinación `num_leaves=127, learning_rate=0,02` con regularización
moderada vía `min_child_samples=50`.

**Bagging (RF)**: 0,8996. Tres puntos por debajo del boosting; baseline
robusto pero limitado por la independencia entre árboles.

**Red neuronal (MLP)**: 0,863. Significativamente debajo de los árboles.
Confirma que el patrón de la señal favorece a splits sobre features
discretas y `duracion_planificada_dias` no se modela bien con activaciones
continuas.

**Lineal (LR)**: 0,840. Sorprendentemente competitivo con `C=0,53` +
`class_weight='balanced'`; útil como modelo interpretable de respaldo.

**Margen (SVM lineal)**: 0,838. Cerca de LR, no aporta sobre lineal
puro. RBF queda descartado por costo computacional con 38k muestras y
154 features.

**Distancia (KNN)**: 0,833. Mejor `k=51` (vecindario amplio), sugiere
que el feature space mixto (numéricas + dummies + freq) tiene mucho
ruido en vecindades pequeñas.

**Probabilístico (NB)**: 0,752. Recall extremadamente bajo (0,21) con
precision casi perfecta (0,995). El modelo se vuelve muy conservador,
predice positivo solo cuando está casi seguro. La asunción de
independencia condicional se viola fuertemente con OHE + numéricas
correlacionadas.

## Métricas finales LGBM (ganador)

| Target | AUC | F1 | Precision | Recall | Accuracy |
|--------|-----|------|-----------|--------|----------|
| tuvo_atraso | 0,9091 | 0,8503 | 0,8672 | 0,8341 | 0,8268 |
| tuvo_sobrecosto | 0,8338 | 0,8731 | 0,8896 | 0,8572 | 0,8071 |

## Comparativa contra v1 (sprint padre, XGB tuned)

| Versión | Target | AUC | F1 | Δ AUC |
|---------|--------|-----|------|-------|
| v1 XGB tuned (Grid) | atraso | 0,9088 | 0,8522 | (ref) |
| **v2 LGBM** | atraso | **0,9091** | 0,8503 | **+0,0003** |
| v1 XGB tuned (Grid) | sobrecosto | 0,8358 | 0,8508 | (ref) |
| **v2 LGBM** | sobrecosto | **0,8338** | 0,8731 | **−0,0020** |

### Lectura

**Atraso**: empate técnico. v2 gana por +0,0003 AUC (no significativo).
Con +2× features no se mejora medible.

**Sobrecosto**: v2 pierde por −0,002 AUC pero **gana en F1 por +0,022**.
El modelo v2 es más balanceado (Precision 0,89 vs 0,93 v1; Recall 0,86
vs 0,79 v1). En contextos donde Recall importa más que AUC puro, v2
puede ser preferible.

## ¿Aportaron las features estructurales nuevas?

Hipótesis del experimento:
> Las features estructurales nuevas (RUP, competencia, post-conflicto,
> UNSPSC, localización fina) aportan señal predictiva no capturada por v1.

Resultado: **confirmada solo marginalmente**.

**A favor**:
- En el top 10 de Permutation Importance aparecen 3 features nuevas:
  `log_valor_contrato`, `localizaci_n_freq`, `codigo_de_categoria_principal_freq`.
- `anios_empresa` en top 11.
- F1 mejora en sobrecosto (+0,022).

**En contra**:
- `duracion_planificada_dias` sigue dominando absolutamente (MI 0,217;
  permutation 0,230 vs siguiente 0,012).
- `n_proponentes_por_proceso` NO aparece en top 30 a pesar de 48 %
  de cobertura.
- RUP estructurales (`rup_tamano`, `rup_empleados`, `rup_sanciones`,
  `rup_inhabilidad`) NO aparecen en top, probablemente por su cobertura
  limitada (49 %).
- Mejora final en AUC atraso es de 0,0003 (≪ umbral significancia).

**Conclusión**: el dataset depurado v1 ya capturaba ~99 % de la señal
predictiva accesible. La estructura del proveedor (tamaño, empleados,
sanciones) y la competencia (proponentes) tienen valor descriptivo
pero impacto predictivo limitado en este universo.

## Justificación de mantener v2 como modelo de referencia

Aunque la mejora es marginal, v2 se prefiere para producción porque:

1. **Más completo metodológicamente**: incluye variables que el negocio
   considera relevantes (RUP, empresa, competencia), aunque no aporten
   AUC. Defendible ante stakeholders.
2. **F1 mayor en sobrecosto** (+0,022): mejora la capacidad operativa
   en el target peor.
3. **Mejor cobertura conceptual**: incorpora dimensión empresa que es
   esencial para el caso de uso del chatbot final.
4. **Foundation para iteraciones**: si la cobertura de RUP sube (ej.
   integración con nuevas fuentes), v2 ya tiene el slot abierto.

## Modelo final persistido

`data/modelos/lgbm.pkl` — LightGBM con los hiperparámetros listados arriba.

Para inferencia hay que sanitizar nombres de columnas:

```python
import re, joblib
mod = joblib.load('lgbm.pkl')
X_new.columns = [re.sub(r'[^A-Za-z0-9_]+', '_', c) for c in X_new.columns]
proba = mod.predict_proba(X_new)[:, 1]
```

## Próximo paso

Fase 5 CRISP-DM (Evaluation) → notebook de evaluación final con
FP/FN, calibración, SHAP, threshold tuning, business value.
