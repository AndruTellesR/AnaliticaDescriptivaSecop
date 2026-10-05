# Plan — Modelo Predictivo Global v2

## Objetivo

Construir un modelo predictivo de atraso/sobrecosto sobre el universo
completo de contratos de obra pública, integrando variables
estructurales del proveedor y del proceso que la v1 no usó, y validando
cuáles aportan valor predictivo real.

## Etapas

| Etapa | Notebook | Output |
|---|---|---|
| 1. Inventario + integración | `01_dataset_global_completo.ipynb` | `data/consolidado_global.parquet` |
| 2. Preprocesamiento | `02_preprocesamiento.ipynb` | `data/consolidado_imputado.parquet` + imputers |
| 3. Feature importance | `03_feature_importance.ipynb` | MI + Permutation Importance |
| 4. Zoológico 8 modelos | `04_modelo_lr.ipynb` a `11_modelo_mlp.ipynb` | 8 `.pkl` + `resultados_modelos.json` |
| 5. Comparativa final | `12_comparativa_final.ipynb` | Ganador + métricas test |

## Zoológico (idéntico al sub-sprint consorcios)

| # | Familia | Algoritmo |
|---|---|---|
| 04 | Lineal | Logistic Regression |
| 05 | Distancia | K-Nearest Neighbors |
| 06 | Margen | Support Vector Machine |
| 07 | Bagging | Random Forest |
| 08 | Boosting | XGBoost |
| 09 | Boosting | LightGBM |
| 10 | Probabilístico | Gaussian Naive Bayes |
| 11 | Red neuronal | Multi-Layer Perceptron |

## Features estructurales a integrar (clave del experimento)

### De `proveedores_rup` (join por `codigo_proveedor`)

Variables que la v1 sí usó (5):
- `rup_idx_endeudamiento`, `rup_idx_liquidez`
- `rup_ingresos`, `rup_utilidad_neta`, `rup_multas`

Variables NUEVAS a integrar:
- `rup_tamano` (categórico: micro/pequena/mediana/grande)
- `rup_empleados` (numérico)
- `rup_sanciones` (binario)
- `rup_inhabilidad` (binario)
- `rup_activo_total` (numérico)
- `rup_patrimonio` (numérico)

### De `proveedores_obra` (join por `codigo_proveedor`)

- `esta_activa` (binario)
- `fecha_creacion` → derivar `años_empresa` (numérico)
- `pais` (mayoritariamente Colombia, pero útil)
- `departamento_proveedor` (categórico, distinto al depto del contrato)

### De `proponentes_por_proceso_obra` (derivar agregado)

- `n_proponentes_por_proceso` (numérico) → proxy de presión competitiva

### De `contratos_adiciones_obra` (cols ya disponibles, ignoradas en v1)

- `log_valor_contrato` (transformación de `valor_del_contrato`)
- `nacionalidad_representante_legal` (categórico)
- `obligaciones_postconsumo` (binario)
- `espostconflicto` (binario)
- `pilares_del_acuerdo` (categórico)
- `puntos_del_acuerdo` (categórico)
- `codigo_de_categoria_principal` (UNSPSC, alta cardinalidad → freq encoding)
- `localizaci_n` (geo más fina que `ciudad`, alta cardinalidad → freq)
- `tipodocproveedor` (categórico)

### Cols leakage (prohibidas como features)

Las 14 del sprint padre + nuevas detectadas:
- Las 14 originales: `tiempo`, `presupuesto`, `alcance`, `n_modif_*`, `tiene_*`, `dias_adicionados`, `dias_hasta_primera_adicion`, `ventana_adiciones_dias`, `ratio_extension_duracion`
- Adicionales: `fecha_de_fin_del_contrato`, `fecha_primera_adicion`, `fecha_ultima_adicion`, `duraci_n_del_contrato`, `liquidaci_n`, `fecha_*_liquidacion`, `n_adicion_valor`, `n_extension`, `n_cesion`, `n_conclusion`, `n_reactivacion`, `n_modificaciones_total`, `tiene_adicion_valor`, `tiene_extension_dias`, `tiene_modificacion`, `valor_amortizado`, `valor_facturado`, `valor_pagado`, `valor_pendiente_*`, `saldo_*`, `sobrecosto_ratio`, `estado_contrato`, `ultima_actualizacion`, `reversion`

### Cols de IDs / PII / texto (no usar como features)

- IDs: `id_contrato`, `codigo_entidad`, `codigo_proveedor`, `proceso_de_compra`, `referencia_del_contrato`, `urlproceso`, `nit_*`, `c_digo_bpin`, `anno_bpin`
- PII: `nombre_*`, `identificaci_n_*`, `documento_*`, `domicilio_*`, `telefono`, `correo`, `fax`, `direccion`
- Texto libre: `objeto_del_contrato`, `descripcion_del_proceso`, `justificacion_modalidad_de`, `descripcion_documentos_tipo`

## Pasos del modelado (de `pasos.md` del líder)

1. **Preprocesamiento**: imputación, encoding, escalado
2. **Zoológico**: 8 algoritmos
3. **Grid de hiperparámetros** por modelo
4. **K-Fold CV** (5)
5. **Loop maestro**: `RandomizedSearchCV` por modelo
6. **Evaluación final**: tabla AUC/F1, selección ganador

## Reglas

- `random_state = 42` siempre
- 80/20 stratified sobre `tuvo_atraso`
- Mediana + flag `_was_nan` para imputación
- OHE < 20, Freq Encoding ≥ 20
- StandardScaler para LR, KNN, SVM, NB, MLP
- AUC primario, F1 desempate, tiempo secundario

## Criterio ganador

1. AUC test máximo
2. Empate técnico (Δ < 0,003) → mayor F1
3. Empate persistente → menor tiempo

## Doc conceptos técnicos

`docs/03_conceptos_tecnicos.md` reúne definición + justificación de:

1. CRISP-DM (fases + iteratividad)
2. Train/test split + estratificación
3. K-Fold Cross Validation
4. Data leakage
5. Imputación (mediana, KNN, MICE)
6. Encoding (OHE, Frequency, Label, Target)
7. Escalado (Standard, MinMax)
8. Métricas (AUC-ROC, F1, Precision, Recall, Accuracy, F-beta)
9. Class imbalance (class_weight, scale_pos_weight, SMOTE)
10. Algoritmos del zoológico (cuándo + por qué cada uno)
11. Hyperparameter tuning (Grid, Random, Halving, Bayesian)
12. Feature importance (MI, Permutation, SHAP)
13. Overfitting + regularización
14. Threshold tuning + business value
