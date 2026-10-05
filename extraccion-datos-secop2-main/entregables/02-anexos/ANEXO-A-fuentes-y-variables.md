# Anexo A — Fuentes de datos y diccionario de variables

Documento complementario al Informe Final del Trabajo Dirigido. Detalla
las fuentes de datos integradas, las llaves de relación, las variables
finalmente utilizadas en el modelo predictivo y las catorce variables
excluidas por riesgo de fuga de información.

---

## A.1. Fuentes de datos integradas

| # | Fuente | Origen | Acceso | Volumen |
|---|--------|--------|--------|---------|
| 1 | Contratos Electrónicos | `datos.gov.co` | API SODA v3 (dataset `jbjy-vk9h`) | 51.353 registros de obra |
| 2 | Procesos de Contratación | `datos.gov.co` | API SODA v3 (dataset `p6dx-8zbt`) | 138.112 registros |
| 3 | Adiciones Contractuales | `datos.gov.co` | API SODA v3 (dataset `cb9c-h8sn`) | 249.037 registros |
| 4 | Proveedores Registrados | `datos.gov.co` | API SODA v3 (dataset `qmzu-gj57`) | 13.117 registros |
| 5 | Proponentes por Proceso | `datos.gov.co` | API SODA v3 | 276.770 registros |
| 6 | Registro Único de Proponentes | Cámaras de Comercio | Scraping con Playwright + CapSolver | 28.548 proveedores |
| 7 | Pliegos de Condiciones | Portal SECOP II | Pipeline Docker + Gemini 2.5 Flash Lite | 7.994 contratos procesados, 4.276 con indicadores |

## A.2. Esquema relacional

```
procesosDeContratacion
   id_del_portafolio (PK)  ──→  contratosElectronicos.proceso_de_compra
   id_del_proceso         ──→  proponentesPorProceso.id_procedimiento

contratosElectronicos
   id_contrato (PK)       ──→  adiciones.id_contrato
   codigo_proveedor       ──→  proveedoresRegistrados.codigo

proveedoresRegistrados
   nit                    ──→  proveedoresRUP.nit
```

### Cobertura observada en los joins

| Relación | Cobertura |
|----------|-----------|
| procesosDeContratacion → contratosElectronicos | 99,9 % |
| adiciones → contratosElectronicos | 69,2 % |
| proveedoresRegistrados → contratosElectronicos | 54,4 % |
| proveedoresRUP → proveedoresRegistrados | 63,5 % |
| proponentesPorProceso → procesosDeContratacion | 48,2 % |
| pliego_* → contratos (global) | 8,0 % |
| pliego_* → consorcios | 36,5 % |

## A.3. Variables finalmente utilizadas en el modelo

Las 152 variables predictoras del dataset final se agrupan en seis familias
funcionales:

### A.3.1. Familia Entidad (6 variables crudas, ampliadas por encoding)

| Variable | Tipo | Cardinalidad | Encoding |
|----------|------|--------------|----------|
| `departamento` | categórica | 32 | Frequency |
| `ciudad` | categórica | ~1.000 | Frequency |
| `orden` | categórica | 3 | One-Hot |
| `sector` | categórica | 32 | Frequency |
| `rama` | categórica | 6 | One-Hot |
| `entidad_centralizada` | categórica | 2 | One-Hot |

### A.3.2. Familia Contrato (19 variables crudas)

| Variable | Tipo | Cardinalidad | Encoding |
|----------|------|--------------|----------|
| `modalidad_de_contratacion` | categórica | 8 | One-Hot |
| `condiciones_de_entrega` | categórica | 13 | One-Hot |
| `valor_del_contrato` | numérica | continua | Bruto + log |
| `valor_de_pago_adelantado` | numérica | continua | Bruto |
| `duracion_planificada_dias` | numérica | continua | Bruto + flag `_was_nan` |
| `documentos_tipo` | categórica | 6 | One-Hot |
| `el_contrato_puede_ser_prorrogado` | categórica | 3 | One-Hot |
| `habilita_pago_adelantado` | categórica | 3 | One-Hot |
| `obligaci_n_ambiental` | categórica | 3 | One-Hot |
| `origen_de_los_recursos` | categórica | 5 | One-Hot |
| `destino_gasto` | categórica | 5 | One-Hot |
| `tipo_de_cuenta` | categórica | 5 | One-Hot |
| `estado_bpin` | categórica | 4 | One-Hot |
| 6 variables binarias de financiación | categóricas | 2 | One-Hot |

### A.3.3. Familia Proponente (perfil del adjudicatario)

| Variable | Tipo | Cardinalidad | Encoding |
|----------|------|--------------|----------|
| `es_grupo` | binaria | 2 | One-Hot |
| `es_pyme` | binaria | 2 | One-Hot |
| `g_nero_representante_legal` | categórica | 3 | One-Hot |
| `nacionalidad_representante_legal` | categórica | 9 | One-Hot |
| `tipodocproveedor` | categórica | 7 | One-Hot |
| `esta_activa` | binaria | 2 | One-Hot |
| `pais_proveedor` | categórica | 3 | One-Hot |
| `departamento_proveedor` | categórica | 36 | Frequency |
| `anios_empresa` | numérica | continua | Bruto + flag `_was_nan` |

### A.3.4. Familia RUP (registro financiero del proveedor)

Todas con cobertura 48–49 % y flag `_was_nan` agregado:

| Variable | Tipo | Encoding |
|----------|------|----------|
| `rup_idx_endeudamiento` | numérica | Bruto |
| `rup_idx_liquidez` | numérica | Bruto |
| `rup_ingresos` | numérica | Bruto |
| `rup_utilidad_neta` | numérica | Bruto |
| `rup_multas` | numérica | Bruto |
| `rup_tamano` | categórica | One-Hot |
| `rup_empleados` | categórica (text) | Frequency |
| `rup_activo_total` | categórica (text) | Frequency |
| `rup_patrimonio` | categórica (text) | Frequency |
| `rup_sanciones` | numérica | Bruto |
| `rup_inhabilidad` | numérica | Bruto |

### A.3.5. Familia Proceso (información pre-contractual)

| Variable | Tipo | Encoding |
|----------|------|----------|
| `n_proponentes_por_proceso` | numérica | Bruto + flag `_was_nan` |
| `codigo_de_categoria_principal` (UNSPSC) | categórica | Frequency |
| `localizaci_n` | categórica | Frequency |

### A.3.6. Familia Pliego (indicadores financieros exigidos)

Todas con cobertura 8 % global / 37 % consorcios. Tras pruebas se confirmó
aporte predictivo marginal, aunque se mantienen en el dataset por
trazabilidad:

| Variable | Significado |
|----------|-------------|
| `pliego_liquidez_min` | Índice de liquidez mínimo exigido |
| `pliego_endeudamiento_max_pct` | Nivel de endeudamiento máximo permitido |
| `pliego_cobertura_intereses_min` | Razón mínima de cobertura de intereses |
| `pliego_rentabilidad_patrimonio_min_pct` | Rentabilidad mínima sobre patrimonio |
| `pliego_rentabilidad_activo_min_pct` | Rentabilidad mínima sobre activo |
| `pliego_capital_trabajo_min_pct_presupuesto` | Capital de trabajo como porcentaje del presupuesto |

## A.4. Variables excluidas por riesgo de fuga de información (data leakage)

Las siguientes catorce variables fueron explícitamente excluidas del set
de predictores porque su información solo se conoce **después** de la
ejecución del contrato:

```
tiempo
presupuesto
alcance
n_modif_general
n_tipos_distintos
n_tipo_no_definido
n_suspension
tiene_cesion
tiene_conclusion
tiene_suspension
dias_adicionados
dias_hasta_primera_adicion
ventana_adiciones_dias
ratio_extension_duracion
```

Estas variables se documentan en el archivo `cols_leakage.txt` que
acompaña al dataset.

## A.5. Construcción de los targets

Los dos targets binarios del modelo se construyen a partir de variables
intermedias del dataset depurado:

```python
tuvo_atraso     = (tiempo == 1).astype(int)       # 60,48 % positivos
tuvo_sobrecosto = (presupuesto == 1).astype(int)  # 83,41 % positivos
```

Donde `tiempo` y `presupuesto` son binarios derivados durante la
depuración que indican respectivamente si el contrato tuvo al menos una
prórroga de plazo o al menos una adición presupuestal.

Se evaluó adicionalmente una tercera variable combinada
(`tuvo_atraso_o_sobrecosto`) pero se descartó por su prevalencia trivial
del 89,1 %.
