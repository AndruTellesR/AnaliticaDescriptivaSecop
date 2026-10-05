# Modelo Predictivo Global v2 — Foco en variables estructurales

Sub-proyecto: segunda versión del modelo predictivo de atraso/sobrecosto
sobre el universo completo de **48.331 contratos de obra pública**.

A diferencia de la v1 (sprint padre en `modelo-predictivo-preliminar/`),
esta versión:

1. **Inventaria todas las variables disponibles** en el dataset crudo y
   tablas auxiliares (no solo las 53 cols del depurado).
2. **Integra variables estructurales** de empresa, proveedor y proceso
   que la v1 ignoró: tamaño empresa, empleados, antigüedad, sanciones,
   activo total, patrimonio, competencia (proponentes por proceso),
   nacionalidad rep. legal, post-conflicto, UNSPSC, localización fina.
3. **Re-entrena el zoológico de 8 algoritmos** siguiendo la guía técnica
   de `pasos.md` y replicando el flujo validado en el sub-sprint
   consorcios.
4. **Documenta cada concepto y decisión técnica** en `docs/03_conceptos_tecnicos.md`
   para sustentación académica.

## Universo

- `tipo_de_contrato = "Obra"`: 48.331 contratos
- Sin filtro por consorcios
- Target principal: `tuvo_atraso` (60,5 % positivos)
- Target secundario: `tuvo_sobrecosto` (83,4 % positivos)

## Hipótesis a validar

**Las variables estructurales del proveedor y del proceso aportan señal
predictiva no capturada por las features del contrato**.

En particular:
- `rup_tamano` y `rup_empleados` → capacidad operativa
- `años_empresa` (derivado de `fecha_creacion`) → experiencia
- `n_proponentes_por_proceso` → presión competitiva
- `espostconflicto`, `pilares_del_acuerdo` → contexto político-territorial
- `rup_sanciones`, `rup_inhabilidad`, `rup_multas` → historial de cumplimiento

## Estructura

```
modelo_predictivo_global/
├── README.md
├── docs/
│   ├── 00_plan.md
│   ├── 01_dataset_y_variables.md     ← inventario completo + cobertura
│   ├── 02_imputacion_encoding.md
│   ├── 03_conceptos_tecnicos.md      ← DEFINICIONES + JUSTIFICACIÓN
│   └── modelos/{04_lr..11_mlp}.md + 12_comparativa.md
├── notebooks/
│   ├── 01_dataset_global_completo.ipynb
│   ├── 02_preprocesamiento.ipynb
│   ├── 03_feature_importance.ipynb
│   ├── 04_modelo_lr.ipynb..11_modelo_mlp.ipynb
│   └── 12_comparativa_final.ipynb
├── src/
│   ├── preprocesamiento.py
│   ├── entrenamiento.py
│   └── generar_notebooks.py
├── data/
│   ├── consolidado_global.parquet     ← dataset con features estructurales
│   ├── consolidado_imputado.parquet
│   ├── resultados_modelos.json
│   ├── comparativa_modelos.csv
│   ├── imputers/{freq_maps, winsor_limits, imputer}.pkl
│   └── modelos/{lr,knn,svm,rf,xgb,lgbm,nb,mlp,GANADOR}.pkl
└── figuras/
```

## Convenciones (heredadas)

- `random_state = 42`
- Train/test split 80/20 stratified sobre `tuvo_atraso`
- CV: StratifiedKFold(5)
- Imputación: mediana + flag `_was_nan` (validado en consorcios)
- Encoding: OHE para cardinalidad < 20, Frequency Encoding ≥ 20
- Métricas: AUC-ROC, F1, Precision, Recall, Accuracy
- 14 cols leakage prohibidas (ver `data/cols_leakage.txt`)

## Foco

Predecir `tuvo_atraso`. Sobrecosto se reporta como secundario en el
notebook de comparativa final, pero el tuning se optimiza para atraso.

## Diferencia con sprint padre v1

| Aspecto | v1 (padre) | v2 (este) |
|---|---|---|
| Universo | 48.331 | 48.331 |
| Features iniciales | 53 cols depurado | ~70 cols con estructurales |
| Tablas integradas | 1 (depurado) | 4 (depurado + RUP + proveedores + proponentes) |
| Análisis exploratorio | Extenso (notebook 06 consorcios) | Omitido (foco modelo) |
| Algoritmos evaluados | 4 (LR/RF/XGB/LGBM) | 8 (zoológico completo) |
| Tuning | Random Search 80 iters | RandomizedSearchCV por modelo (40-50 iters) |
| Doc conceptos técnicos | Distribuida | Centralizada en `03_conceptos_tecnicos.md` |
