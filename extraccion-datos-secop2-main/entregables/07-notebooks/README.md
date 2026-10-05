# 07 — Notebooks Jupyter del proyecto

Esta carpeta contiene los 28 notebooks Jupyter desarrollados durante el
proyecto, agrupados en tres subcarpetas según la etapa a la que pertenecen.

## Subcarpetas

### `extraccion-datos/` — Fase I de CRISP-DM

Nueve notebooks que cubren la extracción, perfilado y depuración de las
fuentes de datos del SECOP. Se ejecutaron secuencialmente durante el
periodo del primer informe de avance.

| Notebook | Foco |
|----------|------|
| `00_definicion_tabla_base.ipynb` | Definición de la fuente madre y clasificación de columnas |
| `01_contratos_electronicos.ipynb` | Extracción y perfilado de la fuente madre (51.353 contratos) |
| `02_procesos_contratacion.ipynb` | Procesos de compra (138.112 procesos) |
| `03_adiciones.ipynb` | Modificaciones contractuales (249.037 registros) |
| `04_proveedores.ipynb` | Proveedores registrados (13.117 únicos) |
| `05_integracion_contratos_adiciones.ipynb` | Integración primaria de las dos fuentes principales |
| `06_proponentes_por_proceso.ipynb` | Oferentes por proceso para derivar variables de competencia |
| `07_depuracion_variables_modelo.ipynb` | Producción del dataset depurado v1 |
| `08_integracion_rup_no_consorcios.ipynb` | Integración con datos financieros del RUP |

### `modelado-v1/` — Sprint principal de modelado

Seis notebooks que cubren el primer ciclo completo de modelado predictivo,
desde la definición del target hasta la arquitectura multi-target.

| Notebook | Foco |
|----------|------|
| `01_definicion_target_eda.ipynb` | Análisis exploratorio y definición de los targets |
| `02_feature_engineering.ipynb` | Codificación, imputación y división train/test |
| `03_baselines.ipynb` | Entrenamiento de los tres modelos de línea base (LR, RF, XGB) |
| `04_baselines_avanzados.ipynb` | Comparativa adicional (escrito pero no ejecutado completamente) |
| `04b_feature_selection.ipynb` | Selección automatizada de variables (94 → 30) |
| `05_modelo_multi_target.ipynb` | Arquitectura multi-target unificada |
| `06_analisis_consorcios.ipynb` | Análisis específico del sub-universo de consorcios |

### `modelado-v2/` — Modelo final con variables estructurales

Doce notebooks que producen el modelo final del proyecto. Incluyen
construcción del dataset enriquecido, preprocesamiento, feature importance,
entrenamiento del zoológico de 8 algoritmos y comparativa final.

| Notebook | Foco |
|----------|------|
| `01_dataset_global_completo.ipynb` | Construcción del dataset enriquecido v2 (55 columnas) |
| `02_preprocesamiento.ipynb` | Winsorización + encoding + imputación (152 features) |
| `03_feature_importance.ipynb` | Análisis MI + Permutation Importance |
| `04_modelo_lr.ipynb` | Logistic Regression |
| `05_modelo_knn.ipynb` | K-Nearest Neighbors |
| `06_modelo_svm.ipynb` | SVM lineal calibrado |
| `07_modelo_rf.ipynb` | Random Forest |
| `08_modelo_xgb.ipynb` | XGBoost |
| `09_modelo_lgbm.ipynb` | LightGBM (modelo ganador) |
| `10_modelo_nb.ipynb` | Gaussian Naive Bayes |
| `11_modelo_mlp.ipynb` | Multi-Layer Perceptron |
| `12_comparativa_final.ipynb` | Comparativa, selección del ganador, evaluación final |

## Cómo ejecutarlos

Cada notebook puede ejecutarse independientemente, pero es recomendable
seguir el orden numérico porque los siguientes consumen artefactos producidos
por los anteriores.

```bash
cd modelado-v2
jupyter notebook
# Luego abrir y ejecutar cada notebook en orden
```

Para ejecución sin interfaz:

```bash
jupyter nbconvert --to notebook --execute --inplace 01_dataset_global_completo.ipynb
jupyter nbconvert --to notebook --execute --inplace 02_preprocesamiento.ipynb
# ... y así sucesivamente
```

## Reproducibilidad

Todos los notebooks utilizan `random_state = 42` en los procesos estocásticos.
Re-ejecutar los notebooks produce exactamente los mismos resultados reportados
en el informe.

## Tiempo de ejecución estimado

- Extracción: varias horas (depende de la velocidad de respuesta de la API
  SODA y de Cloudflare R2 para el backup).
- Modelado v1: aproximadamente 20 minutos en una máquina estándar.
- Modelado v2: aproximadamente 90 minutos por la calibración fina de los 8
  algoritmos.
