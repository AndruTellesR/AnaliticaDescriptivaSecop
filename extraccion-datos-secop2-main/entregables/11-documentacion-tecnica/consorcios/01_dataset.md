# Documento 01 — Dataset Consorcios

**Notebook**: `notebooks/01_construccion_dataset.ipynb`
**Inputs**: `data/contratos_depurado_modelo.parquet` (48.331 × 53)
**Outputs**:

| Archivo | Forma | Descripción |
|---------|-------|-------------|
| `data/consorcios_base.parquet` | 10.629 × 38 | Features + 2 targets sin imputar |
| `data/consorcios_features_raw.parquet` | 10.629 × 36 | Solo features (sin codificar, sin imputar) |
| `data/consorcios_targets.parquet` | 10.629 × 2 | `tuvo_atraso`, `tuvo_sobrecosto` |
| `data/consorcios_schema.csv` | 36 filas | Familia + tipo lógico + cardinalidad + cobertura |
| `data/consorcios_cobertura.csv` | 36 filas | Cobertura por feature (orden ascendente) |
| `data/cols_leakage.txt` | 14 líneas | Cols leakage prohibidas |

## Universo

- Filtro aplicado: `es_grupo == "Si"`
- N consorcios: **10.629** (22 % del dataset depurado)
- Columna `es_grupo` queda fuera del set de features (es filtro, no predictor)

## Targets

| Target | Construcción | Tasa positivos |
|--------|--------------|----------------|
| `tuvo_atraso` | `tiempo == 1` | **44,63 %** (4.744 / 10.629) |
| `tuvo_sobrecosto` | `presupuesto == 1` | **77,89 %** (8.279 / 10.629) |

Comparado con el dataset global (60,5 % atraso, 83,4 % sobrecosto), los
consorcios muestran consistentemente menor riesgo en ambas dimensiones,
en línea con el hallazgo del notebook 06 del sprint padre.

## Columnas leakage (14, excluidas como features)

```
tiempo, presupuesto, alcance,
n_modif_general, n_tipos_distintos, n_tipo_no_definido, n_suspension,
tiene_cesion, tiene_conclusion, tiene_suspension,
dias_adicionados, dias_hasta_primera_adicion, ventana_adiciones_dias,
ratio_extension_duracion
```

Las tres primeras (`tiempo`, `presupuesto`, `alcance`) son los binarios de
los que se derivan los targets. Las demás son contables / temporales
post-contractuales.

## Composición del set de features (36 columnas)

| Familia | N | Columnas |
|---------|---|----------|
| Entidad | 6 | `departamento`, `ciudad`, `orden`, `sector`, `rama`, `entidad_centralizada` |
| Contrato | 19 | modalidad, valor, duración planificada, condiciones, banderas de financiación, documentos tipo, prorrogabilidad, etc. |
| RUP | 5 | `rup_idx_endeudamiento`, `rup_idx_liquidez`, `rup_ingresos`, `rup_utilidad_neta`, `rup_multas` |
| Pliego | 6 | `pliego_liquidez_min`, `pliego_endeudamiento_max_pct`, `pliego_cobertura_intereses_min`, `pliego_rentabilidad_patrimonio_min_pct`, `pliego_rentabilidad_activo_min_pct`, `pliego_capital_trabajo_min_pct_presupuesto` |

## Cobertura por feature

### Hallazgo crítico — RUP: 100 % NaN en consorcios

| Feature RUP | NaN | Cobertura |
|-------------|-----|-----------|
| `rup_idx_endeudamiento` | 10.629 | 0,0 % |
| `rup_idx_liquidez` | 10.629 | 0,0 % |
| `rup_ingresos` | 10.629 | 0,0 % |
| `rup_utilidad_neta` | 10.629 | 0,0 % |
| `rup_multas` | 10.629 | 0,0 % |

**Razón**: el RUP se indexa por `codigo_proveedor` único de un proveedor
individual. Los consorcios contractualmente no tienen un código único de
proveedor RUP — cada miembro lo tiene por separado, pero el consorcio
como entidad jurídica de propósito específico no aparece en el registro.

**Decisión**: las 5 columnas `rup_*` se **eliminan** del set de features
de consorcios en el notebook 02 (paso pre-imputación). No tiene sentido
imputarlas porque no hay un solo valor observado del cual aprender.

### Cobertura `pliego_*`

| Feature | NaN | Cobertura |
|---------|-----|-----------|
| `pliego_liquidez_min` | 6.752 | 36,48 % |
| `pliego_endeudamiento_max_pct` | 6.771 | 36,30 % |
| `pliego_rentabilidad_patrimonio_min_pct` | 6.938 | 34,73 % |
| `pliego_rentabilidad_activo_min_pct` | 6.953 | 34,58 % |
| `pliego_cobertura_intereses_min` | 6.963 | 34,49 % |
| `pliego_capital_trabajo_min_pct_presupuesto` | 9.262 | **12,86 %** |

Los cinco primeros tienen cobertura similar (~35 %), congruentes con la
cobertura final del pipeline Docker (36,5 % consorcios). El indicador
`capital_trabajo` queda significativamente por debajo (13 %), porque
no todos los pliegos lo incluyen explícitamente; en muchos procesos el
capital de trabajo se calcula como ratio derivado, no como umbral mínimo
declarado.

### Otras features con NaN

| Feature | NaN | Cobertura |
|---------|-----|-----------|
| `duracion_planificada_dias` | 1.223 | 88,49 % |

El resto de las 30 features (entidad + contrato + flags) están al 100 %
de cobertura.

## Verificación cruzada — pliego vs target

Reconfirma el hallazgo del notebook 06 del sprint padre: tener o no
pliego extraído no discrimina por sí solo el target en el sub-universo
de consorcios.

| Subgrupo | N contratos | tasa atraso | tasa sobrecosto |
|----------|-------------|-------------|-----------------|
| Con pliego extraído | 3.877 | 0,45 | 0,79 |
| Sin pliego extraído | 6.752 | 0,44 | 0,78 |

La diferencia entre ambos subgrupos es de menos de un punto porcentual.
Esto refuerza que el valor predictivo de `pliego_*` no está en la presencia
del dato sino en los valores numéricos específicos, y que la imputación
del 63 % restante debe ser sofisticada para preservar la señal latente.

## Decisiones tomadas

1. **Targets duales**: ambos targets se conservan para el modelado
   multi-target. La diferencia de prevalencia (44 % vs 78 %) requiere
   manejo de desbalance vía `class_weight` / `scale_pos_weight` en cada
   algoritmo del zoológico.
2. **Drop `rup_*` en notebook 02**: 5 columnas a eliminar antes de
   cualquier imputación.
3. **Sub-imputación `pliego_*`**: foco de la comparativa del notebook 02
   por ser el grupo con mayor NaN imputable (~63 % faltante).
4. **Imputación de `duracion_planificada_dias`**: 11,5 % NaN, se incluye
   en la comparativa del notebook 02 pero no es el centro del análisis.

## Próximo paso

Notebook 02 — comparativa de cuatro estrategias de imputación:

- Mediana + flag `_was_nan` (línea base actual del sprint padre)
- KNN Imputer (k = 5)
- Iterative Imputer (MICE) con Bayesian Ridge
- Iterative Imputer (MICE) con Random Forest

Métrica de comparación: AUC downstream con XGBoost single-target +
reconstrucción artificial (inyectar NaN simulados, medir MAE).
