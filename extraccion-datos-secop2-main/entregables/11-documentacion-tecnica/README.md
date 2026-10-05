# 11 — Documentación técnica complementaria

Esta carpeta contiene la documentación técnica detallada que se produjo
durante el desarrollo del proyecto. Va más allá de los anexos formales del
informe e incluye documentos de decisiones, conceptos, sub-sprints y
operación.

## Subcarpetas

### `modelado-v1/` — Sprint principal de modelado

Documentación del sprint padre. Incluye plan global, resúmenes diarios y
hallazgos de cada etapa.

| Archivo | Foco |
|---------|------|
| `00_plan_global.md` | Plan completo del sprint de modelado |
| `dia_01_resumen.md` | Resumen del día 1 (definición del target y EDA) |
| `dia_02_resumen.md` | Resumen del día 2 (feature engineering y split) |
| `dia_03_resumen.md` | Resumen del día 3 (entrenamiento de baselines) |
| `dia_04b_resumen.md` | Resumen del día 4b (selección de variables) |
| `cols_leakage.txt` | Lista de las 14 variables prohibidas por leakage temporal |
| `README.md` | Visión general del sprint |

### `modelado-v2/` — Modelo final del proyecto

Documentación del segundo sprint que produce el modelo final LightGBM.

| Archivo | Foco |
|---------|------|
| `00_plan.md` | Plan del sprint v2 |
| `01_dataset_y_variables.md` | Descripción detallada del dataset enriquecido y las variables incorporadas |
| `02_imputacion_encoding.md` | Decisiones de preprocesamiento (winsorización, encoding, imputación) |
| `03_conceptos_tecnicos.md` | **Documento exhaustivo de 15 secciones** que cubre todos los conceptos técnicos del proyecto |
| `analisis_modelos_y_chatbot.md` | Análisis detallado del modelo ganador y su interacción con el chatbot |
| `modelos/` | Documento por cada algoritmo del zoológico |
| `README.md` | Visión general del sprint v2 |

El documento más relevante es `modelado-v2/03_conceptos_tecnicos.md`. Incluye
definiciones y justificaciones de:

1. CRISP-DM
2. Train/test split y estratificación
3. K-Fold Cross Validation
4. Data leakage
5. Imputación de valores ausentes
6. Codificación de variables categóricas
7. Escalado de características
8. Métricas de clasificación
9. Class imbalance
10. Algoritmos del zoológico
11. Hyperparameter tuning
12. Feature importance
13. Overfitting y regularización
14. Threshold tuning y costo asimétrico
15. SHAP para explicabilidad

### `consorcios/` — Sub-sprint especializado

Documentación del análisis específico sobre el sub-universo de consorcios
(10.629 contratos).

| Archivo | Foco |
|---------|------|
| `00_plan.md` | Plan del sub-sprint |
| `01_dataset.md` | Construcción del dataset de consorcios |
| `02_imputacion.md` | Comparativa cuantitativa de 4 estrategias de imputación |
| `03_analisis_preliminar.md` | Análisis exploratorio del sub-universo |
| `modelos/` | Documentos por algoritmo (8 modelos del zoológico) |
| `README.md` | Visión general |

### `tuning/` — Sub-sprint de tuning multi-estrategia

Documentación del experimento que comparó cuatro estrategias de búsqueda de
hiperparámetros (Grid Search, Bayesian Optimization, Random Search, Halving
Random Search).

| Archivo | Foco |
|---------|------|
| `00_plan.md` | Plan del sub-sprint |
| `01_random_search.md` | Detalle de la estrategia Random Search |
| `02_halving_random.md` | Detalle de la estrategia Halving Random |
| `03_bayesian_optuna.md` | Detalle de la estrategia Bayesian Optimization con Optuna |
| `04_grid_search.md` | Detalle de la estrategia Grid Search |
| `05_comparativa.md` | Comparativa cuantitativa y selección del ganador |
| `README.md` | Visión general |

## Cómo usar esta documentación

- **Para entender una decisión técnica concreta**: ir directamente al
  documento `modelado-v2/03_conceptos_tecnicos.md`, que es el más completo.
- **Para entender la evolución cronológica del proyecto**: leer en orden los
  resúmenes diarios de `modelado-v1/`.
- **Para entender los experimentos secundarios**: revisar las carpetas
  `consorcios/` y `tuning/`.
- **Para entender el modelo final**: combinar `modelado-v2/01_dataset_y_variables.md`
  con `modelado-v2/02_imputacion_encoding.md` y los documentos por algoritmo
  en `modelado-v2/modelos/`.

## Hallazgos consolidados documentados

A lo largo de la documentación se reportan los siguientes hallazgos centrales:

1. La variable `duracion_planificada_dias` es la dominante absoluta, con MI
   cinco veces mayor que la segunda variable.
2. La relación entre valor y atraso es inversa: contratos pequeños se atrasan
   más, no menos.
3. La modalidad de Licitación Pública es la menos riesgosa (38.7 % de atraso).
4. Los consorcios presentan 20 puntos porcentuales menos de atraso que los
   proponentes individuales.
5. La estrategia de imputación con mediana + flag supera a métodos
   sofisticados (KNN, MICE) por preservar el patrón de ausencia como señal.
6. Las variables estructurales del proveedor aportan información predictiva
   marginal.
7. El modelo de boosting (LightGBM, XGBoost) domina ampliamente sobre las
   demás familias de algoritmos para este problema tabular.
