# Día 3 — Baselines

**Notebook**: [`notebooks/03_baselines.ipynb`](../notebooks/03_baselines.ipynb)
**Fecha**: 2026-04-29

---

## Resultados (test set, n=9,667)

| Modelo | AUC | F1 | Precision | Recall | Accuracy | Train (s) |
|--------|-----|-----|-----------|--------|----------|-----------|
| LogisticRegression | 0.8301 | 0.7862 | 0.8186 | 0.7563 | 0.7512 | 0.2 |
| RandomForest | 0.8989 | **0.8457** | 0.8500 | **0.8415** | 0.8143 | 1.6 |
| XGBoost | **0.9015** | 0.8421 | **0.8801** | 0.8073 | **0.8169** | 0.8 |

> Métricas sin tuning, parámetros default (más `class_weight='balanced'` o `scale_pos_weight`).

---

## Hallazgos clave

### 1. Ambos modelos tree-based superan ampliamente las metas

- **Mínimo aceptable**: AUC ≥ 0.70 → ✅ todos lo cumplen
- **Deseable**: AUC ≥ 0.78 → ✅ todos lo cumplen
- **XGBoost AUC = 0.9015** ya está en territorio "excelente" para baseline default

### 2. Logistic Regression solidísimo como interpretable

AUC 0.83 con un modelo lineal sugiere que muchas features tienen
señal directa con el target (relaciones aproximadamente lineales / monótonas).
Útil para explicabilidad ante stakeholders.

### 3. Trade-offs entre RF y XGB

| | RF | XGB |
|---|-----|-----|
| Mejor en | Recall (no perder atrasos) | Precision (alertar con confianza) |
| Implicación | Más sensible, menos preciso | Más conservador |
| Caso de uso | "No quiero que se me escape ningún caso" | "Si lo marco, debe ser real" |

Ambos pasan al tuning del Día 5.

### 4. Tiempos de entrenamiento

LR: 0.2s | RF: 1.6s | XGB: 0.8s — todos entrenan en < 2 segundos.
Random Search con 80 iters será muy viable.

---

## Validación de no-leakage

Las métricas son altas pero plausibles:
- **AUC 0.90** es realista para un dataset bien estructurado con features informativas
- El balance es 60/40 (no es trivial 90/10)
- El Recall del 80-84% sugiere que los positivos NO son linealmente separables (sino sería 100%)

**Verificación pendiente** (Día 4): feature importance debe mostrar features
sensatas en top (entidad, modalidad, valor, departamento), NO algo sospechoso
como `dias_adicionados` (ya excluida pero sanity check).

---

## Outputs

```
data/
├── modelos/
│   ├── lr.pkl       (LR + StandardScaler pipeline)
│   ├── rf.pkl       (RandomForest, n=300 árboles)
│   └── xgb.pkl      (XGBoost, n=300, depth=6)
└── resultados_baselines.csv

figuras/
├── dia_03_comparativa_baselines.png
├── dia_03_roc_baselines.png
└── dia_03_confusion_matrices.png
```

---

## Decisión: modelos a tunear (Día 5)

- **XGBoost** (mejor AUC + mejor Precision)
- **Random Forest** (mejor Recall + mejor F1)
- LR queda como referencia interpretable, no se tunea

---

## Próximo (Día 4)

- **LightGBM** como cuarto baseline (alternativa más rápida que XGB)
- **Feature Importance** top 20 — verificar que no hay leakage residual
- **Comparativa con vs sin `pliego_*`** — cuantificar el aporte de la extracción Gemini
- Decisión final del shortlist para tuning
