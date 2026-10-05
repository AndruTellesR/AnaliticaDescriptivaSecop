# Plan de Modelado — CRISP-DM Fase 4

**Sprint**: 7 días
**Director**: Claude (rol asistido)
**Fecha inicio**: 2026-04-29

---

## Objetivo del modelo

Predecir si un contrato de obra pública en SECOP II **tendrá adiciones** (modificaciones al alcance original).

> Nota: Aunque la conversación inicial mencionó atrasos y extensión de presupuesto, ambos fenómenos están capturados por el campo `adiciones`. Una adición puede ser de plazo (atraso autorizado) o de presupuesto (sobrecosto). Por eso usamos un único target binario que cubre ambos.

---

## Target

**Variable objetivo principal:** `tuvo_atraso` (binaria)

| Valor | Definición |
|-------|-----------|
| `1` | El contrato tuvo extensión de plazo (modificación tipo "tiempo" en adiciones) |
| `0` | El contrato no tuvo extensión de plazo |

**Balance real (verificado en Día 1)**: 60.5% positivos / 39.5% negativos — **ideal para clasificación binaria**.

**Targets secundarios** (para iteración futura, no Día 1-7):
- `tuvo_sobrecosto` (83.4% positivos — muy desbalanceado)
- `tuvo_atraso_o_sobrecosto` (89.1% positivos — modelo trivial saturado)

> **Decisión Día 1**: Se descartó `tuvo_atraso_o_sobrecosto` como target primario. Con 89.1% positivos, un clasificador trivial "siempre predice 1" obtiene 89% accuracy → baja señal predictiva. `tuvo_atraso` ofrece mejor balance y mapea directamente al objetivo del proyecto (atrasos en tiempo).

---

## Universe

- **Dataset**: `data/contratos_depurado_modelo.parquet` — 48,331 contratos de obra
- **Sin filtrar por consorcios** (`es_grupo` será una feature más, no filtro)
- **Indicadores `pliego_*`**: feature ralo (cobertura ~2-3% al inicio, crecerá durante el sprint)

---

## Cronograma (7 días)

| Día | Notebook | Entregable |
|-----|----------|------------|
| **1** | `09_definicion_target_eda.ipynb` | Target derivado, EDA, distribuciones, identificación de leakage |
| **2** | `10_feature_engineering.ipynb` | Features finalizadas, train/test split, dataset listo para modelar |
| **3** | `11_baselines.ipynb` | Logistic Regression, Random Forest, XGBoost (default params) |
| **4** | `12_baselines_avanzados.ipynb` | LightGBM + análisis feature importance + comparativa con/sin `pliego_*` |
| **5** | `13_hyperparameter_tuning.ipynb` | Random Search 80 iters × top 2 modelos × CV 5-fold |
| **6** | `14_evaluacion.ipynb` | Métricas estadísticas + business value + análisis FP/FN |
| **7** | Buffer / writeup | Slides, conclusiones, documento final |

---

## Decisiones técnicas

### División train/test
- **Stratified split** por `tuvo_adicion`
- **80% train / 20% test**
- Random seed fija: `42`

### Manejo de missing
- `pliego_*`: NaN como categoría (flag `tiene_pliego_extraido`) — la extracción está en curso, ausencia no es informativa
- Categóricas con < 5% missing: imputar con moda
- Numéricas con < 10% missing: imputar mediana
- > 30% missing: descartar

### Codificación
- Categóricas baja cardinalidad (< 20): One-Hot
- Categóricas alta cardinalidad (> 20): Target Encoding con regularización
- Texto (`objeto_del_contrato`): TF-IDF top-100 features + features manuales (longitud, n_palabras)

### Leakage (variables PROHIBIDAS como features)
- `valor_pagado` → solo se conoce ex-post
- `valor_facturado` → idem
- `dias_adicionados` → ES el target indirecto
- `n_modif_general` → relacionado al target
- `estado_contrato` → relacionado al target
- Cualquier campo con `fecha_fin`, `fecha_terminacion`

### Algoritmos baseline
| Modelo | Por qué |
|--------|---------|
| Logistic Regression | Interpretable, baseline irreducible |
| Random Forest | No-linear, robusto a outliers, feature importance |
| XGBoost | SOTA en datos tabulares, manejo nativo de missing |
| LightGBM | Más rápido que XGB, alternativa |

### Métricas
**Estadísticas**:
- AUC-ROC (principal)
- F1-score (clase positiva)
- Precision, Recall, Accuracy
- Calibración (Brier score)

**Negocio**:
- Top decile lift (¿cuántas adiciones reales captura el top 10% de scores más altos?)
- Threshold tuning según costo asimétrico (FP vs FN)

---

## Riesgos y mitigaciones

| Riesgo | Probabilidad | Mitigación |
|--------|--------------|------------|
| Class imbalance moderado (69/31) | Alta | `class_weight='balanced'` o SMOTE solo si ayuda |
| Feature leakage no detectado | Media | Lista explícita de cols prohibidas + test con timestamp |
| `pliego_*` no aporta señal | Media | Comparativa explícita con/sin esos features |
| Cardinalidad alta en `nombre_entidad` | Alta | Target Encoding con CV |
| Texto en `objeto_del_contrato` ruidoso | Media | Empezar sin texto, agregar si métricas mejoran |

---

## Definición de "éxito" del sprint

**Mínimo aceptable**:
- AUC-ROC ≥ 0.70 en test
- Modelo entrenado, calibrado y serializado
- Análisis FP/FN documentado
- Comparativa con/sin `pliego_*` cuantificada

**Deseable**:
- AUC-ROC ≥ 0.78
- Top-decile lift ≥ 2.5x
- Insights accionables sobre features predictivas
- Pipeline reproducible (script + parquets versionados)

---

## Próximos pasos (después del sprint)

- Modelos multi-target (regresión sobre `dias_adicionados`, `monto_adicion`)
- Time-aware split (entrenar con contratos viejos, validar con nuevos)
- Tabular Deep Learning (TabNet, FT-Transformer) si baselines saturan
- Calibración isotónica para probabilidades confiables
- API de scoring (FastAPI) para deploy
