# Modelo Predictivo — Consorcios

Sub-proyecto enfocado exclusivamente a contratos suscritos por **consorcios**
(`es_grupo = "Si"`, 10.629 contratos del dataset depurado).

Objetivo: predecir atraso en plazo y sobrecosto presupuestal en contratos
de obra pública adjudicados a consorcios, evaluando si el universo
restringido + indicadores `pliego_*` con mayor cobertura (36,5 %) genera
un modelo más preciso que el modelo global.

## Estructura

```
consorcios/
├── README.md                ← este archivo
├── src/
│   └── preprocesamiento.py  ← módulo compartido (imputación, encoding, scaling)
├── docs/                    ← un .md por etapa + uno por modelo
│   ├── 00_plan.md
│   ├── 01_dataset.md
│   ├── 02_imputacion.md
│   ├── 03_analisis_preliminar.md
│   └── modelos/
│       ├── 04_logistic.md
│       ├── 05_knn.md
│       ├── 06_svm.md
│       ├── 07_random_forest.md
│       ├── 08_xgboost.md
│       ├── 09_lightgbm.md
│       ├── 10_naive_bayes.md
│       ├── 11_mlp.md
│       └── 12_comparativa.md
├── notebooks/               ← uno por etapa, uno por modelo
├── data/
│   ├── imputers/            ← *.pkl de cada estrategia
│   └── modelos/             ← *.pkl entrenados
└── figuras/                 ← PNG por notebook
```

## Pipeline

1. **Notebook 01** — construcción dataset consorcios (filtro + features + targets)
2. **Notebook 02** — comparativa imputación (Mediana / KNN / MICE-BR / MICE-RF)
3. **Notebook 03** — análisis preliminar (capacidad real, cruces depto × pliego × target)
4. **Notebooks 04–11** — un algoritmo por archivo, con `RandomizedSearchCV` + CV=5
5. **Notebook 12** — comparativa final + selección modelo ganador

## Algoritmos evaluados (zoológico)

| # | Familia | Algoritmo |
|---|---------|-----------|
| 04 | Lineal | Logistic Regression |
| 05 | Distancia | K-Nearest Neighbors |
| 06 | Margen | Support Vector Machine |
| 07 | Bagging | Random Forest |
| 08 | Boosting | XGBoost |
| 09 | Boosting | LightGBM |
| 10 | Probabilístico | Naive Bayes |
| 11 | Red neuronal | Multi-Layer Perceptron |

## Convenciones (heredadas del sprint padre)

- `random_state = 42`
- Train/test split 80/20 stratified
- Targets: `tuvo_atraso`, `tuvo_sobrecosto`
- 14 columnas leakage prohibidas (ver `../docs/cols_leakage.txt`)
- Métricas: AUC, F1, Precision, Recall, Accuracy

## Resultados finales

| # | Modelo | AUC test | F1 | Tiempo |
|---|--------|----------|------|--------|
| 1 | **xgb** | **0,8630** | **0,7499** | 25 s |
| 2 | lgbm | 0,8627 | 0,7478 | 820 s |
| 3 | rf | 0,8518 | 0,7274 | 58 s |
| 4 | mlp | 0,8074 | 0,6789 | 59 s |
| 5 | svm | 0,8058 | 0,6786 | 771 s |
| 6 | lr | 0,7690 | 0,6114 | 10 s |
| 7 | knn | 0,7497 | 0,6190 | 9 s |
| 8 | nb | 0,6762 | 0,6219 | 5 s |

**Ganador**: XGBoost. Modelo persistido en `data/modelos/xgb.pkl`.

**Decisiones derivadas**:

- `rup_*` (5 cols) eliminadas: cobertura 0 % en consorcios.
- Imputación: mediana + flag `_was_nan` (AUC 0,8542 vs 0,80 con MICE/KNN).
- `pliego_*`: bajo aporte (MI ≤ 0,015 valores, ≤ 0,015 flags). Se mantienen
  por trazabilidad académica.
- **Modelo global del sprint padre (AUC 0,9047) sigue siendo superior**.
  Especialización en consorcios no aporta ventaja → no se unifica, queda
  como evidencia experimental.
