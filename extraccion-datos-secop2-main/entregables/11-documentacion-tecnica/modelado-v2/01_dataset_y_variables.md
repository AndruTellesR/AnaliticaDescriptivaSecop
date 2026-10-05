# Documento 01 — Dataset y variables

**Notebook**: `notebooks/01_dataset_global_completo.ipynb`
**Output**: `data/consolidado_global.parquet` (48.331 × 55)

## Construcción del dataset

Se parte del archivo más rico del proyecto (`contratos_adiciones_obra.parquet`,
125 columnas) y se cruzan tres fuentes auxiliares para enriquecer cada
contrato con información estructural del proveedor y del proceso.

### Fuentes integradas

| Fuente | Cardinalidad | Rol | Cobertura del join |
|--------|--------------|-----|---------------------|
| `contratos_adiciones_obra.parquet` | 48.331 × 125 | Tabla madre del contrato | 100 % |
| `proveedores_obra.parquet` | 13.117 × 25 | Info empresa (creación, país, depto) | 66,5 % |
| `proveedores_rup.parquet` | 28.548 × 22 | Datos financieros y estructurales RUP | 49 % |
| `proponentes_por_proceso_obra.parquet` | 276.770 × 9 | Conteo de oferentes por proceso | 48,2 % |

### Llaves de join

```
contratos.codigo_proveedor (PK) ─→ proveedores_obra.codigo
                                    │
                                    └─ .nit ─→ proveedores_rup.nit
                              
contratos.proceso_de_compra (CO1.BDOS.*)
       │
       └─ via procesos_contratacion.id_del_portafolio (BDOS)
              ↔ .id_del_proceso (CO1.REQ.*)
              ↔ proponentes.id_procedimiento (REQ)
```

La tabla puente entre `BDOS` y `REQ` es **crítica**: sin ella el join
directo con proponentes falla por formato distinto de la clave.

## Composición final del dataset (55 columnas)

### Targets (2)

- `tuvo_atraso` = 1 si contrato tuvo extensión de plazo (60,48 % positivos)
- `tuvo_sobrecosto` = 1 si tuvo adición presupuestal (83,41 % positivos)

### Features ya usadas en v1 (33 columnas)

Provenían del dataset depurado. Se mantienen para comparabilidad:

- **Entidad**: `departamento`, `ciudad`, `orden`, `sector`, `rama`,
  `entidad_centralizada`
- **Contrato**: `modalidad_de_contratacion`, `condiciones_de_entrega`,
  `valor_del_contrato`, `valor_de_pago_adelantado`,
  `duracion_planificada_dias`, `documentos_tipo`, etc.
- **Proponente (limitado)**: `es_grupo`, `es_pyme`,
  `g_nero_representante_legal`
- **Financiación**: `presupuesto_general_de_la_nacion_pgn`,
  `sistema_general_de_participaciones`, `sistema_general_de_regal_as`,
  `recursos_propios_*`, `recursos_de_credito`
- **RUP v1**: `rup_idx_endeudamiento`, `rup_idx_liquidez`, `rup_ingresos`,
  `rup_utilidad_neta`, `rup_multas`
- **Otras**: `habilita_pago_adelantado`, `obligaci_n_ambiental`,
  `origen_de_los_recursos`, `destino_gasto`, `estado_bpin`,
  `tipo_de_cuenta`, `el_contrato_puede_ser_prorrogado`

### Features ESTRUCTURALES nuevas (20 columnas)

**Foco del experimento**. Variables que la v1 no usó.

#### Del proveedor (vía join codigo → nit)

| Feature | Tipo | Cobertura | Origen |
|---------|------|-----------|--------|
| `rup_tamano` | categórico (6) | 49 % | proveedores_rup |
| `rup_empleados` | numérico | 49 % | proveedores_rup |
| `rup_sanciones` | categórico (6) | 49 % | proveedores_rup |
| `rup_inhabilidad` | categórico (3) | 49 % | proveedores_rup |
| `rup_activo_total` | numérico | 48 % | proveedores_rup |
| `rup_patrimonio` | numérico | 48 % | proveedores_rup |
| `esta_activa` | binario | 66,5 % | proveedores_obra |
| `anios_empresa` | numérico | 66,5 % | derivado de `fecha_creacion` |
| `pais_proveedor` | categórico (3) | 66,5 % | proveedores_obra |
| `departamento_proveedor` | categórico (36) | 66,5 % | proveedores_obra |

#### Del proceso (vía join proceso_de_compra → puente → id_procedimiento)

| Feature | Tipo | Cobertura | Origen |
|---------|------|-----------|--------|
| `n_proponentes_por_proceso` | numérico | 48,2 % | proponentes_por_proceso_obra |

Distribución: mediana 3 proponentes, p75 = 8, max = 118. Proxy de
presión competitiva en el proceso de adjudicación.

#### Del contrato (cols ignoradas en v1)

| Feature | Tipo | Cobertura | Origen |
|---------|------|-----------|--------|
| `log_valor_contrato` | numérico | 100 % | base (transformación) |
| `nacionalidad_representante_legal` | categórico (9) | 100 % | base |
| `obligaciones_postconsumo` | binario | 100 % | base |
| `espostconflicto` | binario | 100 % | base |
| `pilares_del_acuerdo` | categórico (14) | 100 % | base |
| `puntos_del_acuerdo` | categórico (5) | 100 % | base |
| `codigo_de_categoria_principal` | categórico (1506) | 100 % | base (UNSPSC) |
| `localizaci_n` | categórico (737) | 100 % | base (geo fino) |
| `tipodocproveedor` | categórico (7) | 100 % | base |

### Variables leakage prohibidas (36 columnas)

Documentadas en `data/cols_leakage.txt`. Categorías:

- **Targets directos** (3): `tiempo`, `presupuesto`, `alcance`
- **Conteos post-contractuales** (10): `n_modif_*`, `n_extension`,
  `n_adicion_valor`, `tiene_*`, etc.
- **Días y ratios post** (4): `dias_adicionados`, `dias_hasta_primera_adicion`,
  `ventana_adiciones_dias`, `ratio_extension_duracion`
- **Fechas posteriores a firma** (7): `fecha_de_fin_*`, `fecha_*_adicion`,
  `fecha_*_liquidacion`, etc.
- **Valores de ejecución** (8): `valor_pagado`, `valor_facturado`,
  `valor_amortizado`, `valor_pendiente_*`, `saldo_*`, `sobrecosto_ratio`
- **Estados terminales** (4): `estado_contrato`, `liquidaci_n`,
  `ultima_actualizacion`, `reversion`

### Variables descartadas por ser IDs / PII / texto libre

- IDs: `id_contrato`, `codigo_entidad`, `codigo_proveedor`,
  `proceso_de_compra`, `urlproceso`, `nit_*`, `c_digo_bpin`
- PII: `nombre_*_representante_legal`, `documento_*`, `telefono`,
  `correo`, `direccion`
- Texto libre: `objeto_del_contrato`, `descripcion_del_proceso`,
  `justificacion_modalidad_de`

## Hipótesis empírica del experimento

> Las features estructurales nuevas (capacidad operativa, antigüedad,
> presión competitiva, UNSPSC, localización fina) aportan señal
> predictiva no capturada por las 33 cols de la v1.

Esta hipótesis se valida en el notebook 03 (feature importance) y
se confirma indirectamente en el notebook 12 (comparativa) si el AUC
del XGB tuned mejora sobre el baseline v1.

## Salidas del notebook

| Archivo | Descripción |
|---------|-------------|
| `data/consolidado_global.parquet` | Dataset enriquecido (48.331 × 55) |
| `data/schema_features.csv` | Tipo, cardinalidad y cobertura por columna |
| `data/cols_leakage.txt` | 36 columnas prohibidas |
