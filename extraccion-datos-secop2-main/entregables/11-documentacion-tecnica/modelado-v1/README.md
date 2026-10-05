# Modelo Predictivo Preliminar — Fase 4 CRISP-DM

Sprint de 7 días para construir un modelo predictivo binario que estime
si un contrato de obra pública en SECOP II tendrá **atraso en el plazo**.

> **Target primario**: `tuvo_atraso` (60.5% positivos)
> **Universe**: 48,331 contratos de obra (no solo consorcios)
> **Estado**: Día 1 completado, Día 2 en curso

---

## Estructura

```
modelo-predictivo-preliminar/
├── README.md                         ← Este índice
├── docs/                             ← Documentación por día
│   ├── 00_plan_global.md             ← Plan del sprint
│   ├── cols_leakage.txt              ← Cols prohibidas como feature
│   ├── dia_01_resumen.md             ← Día 1: target + EDA
│   └── dia_02_resumen.md             ← Día 2: feature engineering
├── notebooks/                        ← Jupyter notebooks
│   ├── 01_definicion_target_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_baselines.ipynb
│   ├── 04_baselines_avanzados.ipynb
│   ├── 05_hyperparameter_tuning.ipynb
│   └── 06_evaluacion_final.ipynb
├── data/                             ← Datasets generados
│   ├── dataset_modelado.parquet      ← Dataset listo para FE
│   ├── X_train.parquet, X_test.parquet
│   └── y_train.parquet, y_test.parquet
└── figuras/                          ← Plots y visualizaciones
    └── *.png
```

---

## Cronograma del sprint

| Día | Notebook | Descripción | Estado |
|-----|----------|-------------|--------|
| **1** | [`01_definicion_target_eda.ipynb`](notebooks/01_definicion_target_eda.ipynb) | Target, EDA, leakage | ✅ |
| **2** | [`02_feature_engineering.ipynb`](notebooks/02_feature_engineering.ipynb) | Encoding, imputación, split | 🔄 |
| **3** | [`03_baselines.ipynb`](notebooks/03_baselines.ipynb) | LR, RF, XGBoost | ⏳ |
| **4** | [`04_baselines_avanzados.ipynb`](notebooks/04_baselines_avanzados.ipynb) | LightGBM + comparativa pliego | ⏳ |
| **5** | [`05_hyperparameter_tuning.ipynb`](notebooks/05_hyperparameter_tuning.ipynb) | Random Search 80 iters × top 2 | ⏳ |
| **6** | [`06_evaluacion_final.ipynb`](notebooks/06_evaluacion_final.ipynb) | AUC, F1, FP/FN, business value | ⏳ |
| **7** | — | Writeup + slides | ⏳ |

---

## Documentación

- [Plan global del sprint](docs/00_plan_global.md) — decisiones técnicas, riesgos, métricas
- [Resumen Día 1](docs/dia_01_resumen.md) — definición del target, EDA inicial
- [Cols leakage](docs/cols_leakage.txt) — variables prohibidas como features

---

## Convenciones

### Paths en notebooks

```python
RAIZ_PROYECTO = Path('../..').resolve()   # extraccion-datos/
RAIZ_MODELO   = Path('..').resolve()      # modelo-predictivo-preliminar/
DATA_RAW      = RAIZ_PROYECTO / 'data'    # input crudo (parquets originales)
DATA          = RAIZ_MODELO / 'data'      # outputs propios
DOCS          = RAIZ_MODELO / 'docs'
FIGS          = RAIZ_MODELO / 'figuras'
```

### Outputs por notebook

- **Datasets**: `parquet` en `data/`
- **Documentación**: `.md` en `docs/dia_NN_*.md`
- **Figuras**: `.png` en `figuras/dia_NN_<descripcion>.png`
- **Modelos**: `.pkl` (joblib) en `data/modelos/`

### Reproducibilidad

- `random_state = 42` en todas las divisiones y modelos
- Train/test split: stratified 80/20
- CV: 5-fold stratified

---

## Decisiones clave (vivas, se actualizan)

| Decisión | Razón | Día |
|----------|-------|-----|
| Target = `tuvo_atraso`, no `tuvo_atraso_o_sobrecosto` | Balance 60/40 vs 89/11 (este último trivializa) | 1 |
| No filtrar por consorcios | `es_grupo` será feature, no filtro | 1 |
| `pliego_*` como features ralos + flag | Cobertura 2-3% al inicio, crecerá | 1 |
| 14 cols leakage excluidas | Construyen el target o post-hoc | 1 |
