# Diccionario de datos

## Datasets del proyecto - Modelo Predictivo SECOP II Obra Publica

> Generado automaticamente por `scripts/generar_diccionario_datos.py`
> Contrastado con definiciones oficiales del SECOP en `dataset.json`

---

## Indice de datasets

| # | Dataset | Registros | Columnas | Fuente SECOP |
|---|---|---|---|---|
| 1 | [Contratos Electrónicos — Obra](#contratos-electronicos-obra) | 51.353 | 87 | contratosElectronicos |
| 2 | [Procesos de Contratación — Obra](#procesos-contratacion-obra) | 138.112 | 57 | procesosDeContratacion |
| 3 | [Adiciones — Obra](#adiciones-obra) | 249.037 | 5 | adiciones |
| 4 | [Proveedores Registrados — Obra](#proveedores-obra) | 13.117 | 25 | proveedoresRegistrados |
| 5 | [Proponentes por Proceso — Obra](#proponentes-por-proceso-obra) | 276.770 | 9 | proponentesporProceso |
| 6 | [Contratos + Adiciones (integrado)](#contratos-adiciones-obra) | 48.331 | 111 | Derivado |
| 7 | [Proveedores RUP (enriquecido)](#proveedores-rup) | 28.548 | 22 | Derivado |

---

## 1. Contratos Electrónicos — Obra

**Archivo**: `data/contratos_electronicos_obra.parquet`

**Descripcion**: Contratos de Obra Pública firmados electrónicamente en SECOP II. Fuente madre del proyecto: contiene variables de ejecución, estados contractuales y datos del proveedor adjudicado.

| Atributo | Valor |
|---|---|
| Granularidad | 1 fila = 1 contrato firmado |
| Registros | 51.353 |
| Columnas | 87 |
| Notebook/Script | `01_contratos_electronicos.ipynb` |
| Fuente SECOP | `contratosElectronicos` |

### Definicion de columnas

| # | Columna API | Nombre original | Tipo | Descripcion | No nulos | Nulos (%) | Unicos |
|---|---|---|---|---|---|---|---|
| 1 | `nombre_entidad` | Nombre Entidad | Texto | Nombre de la entidad del estado que publica el contrato | 51.353 | 0 (0%) | 2.528 |
| 2 | `nit_entidad` | Nit Entidad | Número | NIT de la entidad del estado que publica el contrato | 51.353 | 0 (0%) | 2.270 |
| 3 | `departamento` | Departamento | Texto | Departamento en el cual se registró la entidad del estado que publica el contrato | 51.353 | 0 (0%) | 34 |
| 4 | `ciudad` | Ciudad | Texto | Ciudad en el cual se registró la entidad del estado que publica el contrato | 51.353 | 0 (0%) | 617 |
| 5 | `localizaci_n` | Localización | Texto | Ubicación completa de la entidad del estado que publica el contrato | 51.353 | 0 (0%) | 737 |
| 6 | `orden` | Orden | Texto | Orden entidad del estado que publica el contrato | 51.353 | 0 (0%) | 3 |
| 7 | `sector` | Sector | Texto | Sector entidad del estado que publica el contrato | 51.353 | 0 (0%) | 25 |
| 8 | `rama` | Rama | Texto | Rama del estado de la entidad que publica el contrato | 51.353 | 0 (0%) | 4 |
| 9 | `entidad_centralizada` | Entidad Centralizada | Texto | Define si la entidad es descentralizada o centralizada | 51.353 | 0 (0%) | 2 |
| 10 | `proceso_de_compra` | Proceso de Compra | Texto | Identificador del proceso de compra publicado | 51.353 | 0 (0%) | 43.451 |
| 11 | `id_contrato` | ID Contrato | Texto | Identificador del contrato firmado, generado por la plataforma | 51.353 | 0 (0%) | 48.331 |
| 12 | `referencia_del_contrato` | Referencia del Contrato | Texto | Identificador del contrato firmado, generado por la entidad del estado | 51.353 | 0 (0%) | 45.910 |
| 13 | `estado_contrato` | Estado Contrato | Texto | Estado del contrato, frente a su ejecución, firma o liquidación | 51.353 | 0 (0%) | 11 |
| 14 | `codigo_de_categoria_principal` | Código de Categoría Principal | Texto | Código UNSPSC de la categoría principal para el contrato | 51.353 | 0 (0%) | 1.506 |
| 15 | `descripcion_del_proceso` | Descripción del Proceso | Texto | Descripción del objeto del proceso de compra | 51.353 | 0 (0%) | 43.445 |
| 16 | `tipo_de_contrato` | Tipo de Contrato | Texto | Tipo de contrato de acuerdo con su marco jurídico | 51.353 | 0 (0%) | 1 |
| 17 | `modalidad_de_contratacion` | Modalidad de Contratación | Texto | Modalidad de contratación de acuerdo con el modelo de selección | 51.353 | 0 (0%) | 9 |
| 18 | `justificacion_modalidad_de` | Justificación Modalidad de Contratación | Texto | Justificación de la modalidad, el escenario bajo el cual se toma la decisión de definir una u otr... | 51.353 | 0 (0%) | 21 |
| 19 | `fecha_de_firma` | Fecha de Firma | Marca de tiempo variable | Fecha de firma del contrato electrónico | 45.975 | 5.378 (10.5%) | 2.402 |
| 20 | `fecha_de_inicio_del_contrato` | Fecha de Inicio del Contrato | Marca de tiempo variable | Fecha de inicio de las responsabilidades contractuales | 44.975 | 6.378 (12.4%) | 2.471 |
| 21 | `fecha_de_fin_del_contrato` | Fecha de Fin del Contrato | Marca de tiempo variable | Fecha de fin de las responsabilidades contractuales | 49.788 | 1.565 (3.0%) | 3.468 |
| 22 | `condiciones_de_entrega` | Condiciones de Entrega | Texto | Condiciones bajo las cuales se entrega el producto o servicio | 51.353 | 0 (0%) | 14 |
| 23 | `tipodocproveedor` | Tipo Doc Proveedor | Texto | Tipo de documento del proveedor adjudicado | 51.353 | 0 (0%) | 7 |
| 24 | `documento_proveedor` | Documento Proveedor | Texto | Número de documento del proveedor adjudicado | 51.353 | 0 (0%) | 18.641 |
| 25 | `proveedor_adjudicado` | Proveedor Adjudicado | Texto | Nombre del proveedor adjudicado | 51.353 | 0 (0%) | 22.770 |
| 26 | `es_grupo` | Es Grupo | Texto | Determina el proveedor es un grupo de entidades, existe un conjunto de datos de CCE que contiene ... | 51.353 | 0 (0%) | 2 |
| 27 | `es_pyme` | Es Pyme | Texto | Determina si la empresa es una Pyme | 51.353 | 0 (0%) | 2 |
| 28 | `habilita_pago_adelantado` | Habilita Pago Adelantado | Texto | Determina si el contrato tiene habilitada la opción de pago de adelantos | 51.353 | 0 (0%) | 3 |
| 29 | `liquidaci_n` | Liquidación | Texto | Determina si el contrato ha sido liquidado | 51.353 | 0 (0%) | 2 |
| 30 | `obligaci_n_ambiental` | Obligación Ambiental | Texto | Determina si el contrato tiene compromisos de cumplimiento a obligaciones ambientales | 51.353 | 0 (0%) | 2 |
| 31 | `obligaciones_postconsumo` | Obligaciones Post consumo | Texto | Determina si el contrato tiene compromisos de cumplimiento a obligaciones posteriores a la entreg... | 51.353 | 0 (0%) | 2 |
| 32 | `reversion` | Reversión | Texto | Determina si el contrato ha sido reversado | 51.353 | 0 (0%) | 2 |
| 33 | `origen_de_los_recursos` | Origen de los Recursos | Texto | Origen de los Recursos, a nivel presupuestal | 51.353 | 0 (0%) | 2 |
| 34 | `destino_gasto` | Destino Gasto | Texto | Destino del gasto, a nivel presupuestal | 51.353 | 0 (0%) | 3 |
| 35 | `valor_del_contrato` | Valor del Contrato | Número | Valor total del contrato | 51.353 | 0 (0%) | 39.774 |
| 36 | `valor_de_pago_adelantado` | Valor de pago adelantado | Número | Valor del pago por adelantado | 51.353 | 0 (0%) | 1.106 |
| 37 | `valor_facturado` | Valor Facturado | Número | Valor Facturado a la fecha | 51.353 | 0 (0%) | 16.252 |
| 38 | `valor_pendiente_de_pago` | Valor Pendiente de Pago | Número | Valor Pendiente de Pago a la fecha | 51.353 | 0 (0%) | 33.906 |
| 39 | `valor_pagado` | Valor Pagado | Número | Valor Pagado a la fecha | 51.353 | 0 (0%) | 13.144 |
| 40 | `valor_amortizado` | Valor Amortizado | Número | Valor Amortizado a la fecha | 51.353 | 0 (0%) | 239 |
| 41 | `valor_pendiente_de` | Valor Pendiente de Amortización | Número | Valor Pendiente de Amortización a la fecha | 51.353 | 0 (0%) | 998 |
| 42 | `valor_pendiente_de_ejecucion` | Valor Pendiente de Ejecución | Número | Valor Pendiente de Ejecución a la fecha | 51.353 | 0 (0%) | 33.882 |
| 43 | `estado_bpin` | Estado BPIN | Texto | Estado de asignación del código del Banco de Proyectos de Inversión | 51.353 | 0 (0%) | 2 |
| 44 | `c_digo_bpin` | Código BPIN | Texto | Código asociado al Banco de Proyectos de Inversión | 51.353 | 0 (0%) | 8.244 |
| 45 | `anno_bpin` | Anno BPIN | Texto | Año de asignación del código del Banco de Proyectos de Inversión | 51.353 | 0 (0%) | 8 |
| 46 | `saldo_cdp` | Saldo CDP | Número | Saldo del CDP asignado al proceso y al contrato | 51.353 | 0 (0%) | 20.651 |
| 47 | `saldo_vigencia` | Saldo Vigencia | Número | Saldo actual para la vigencia del CDP asignado al proceso y al contrato | 51.353 | 0 (0%) | 902 |
| 48 | `espostconflicto` | Es Post Conflicto | Texto | Determina si el proceso está asociado a algún evento de acuerdo de paz | 51.353 | 0 (0%) | 2 |
| 49 | `dias_adicionados` | Días adicionados | Número | Días adicionados al contrato electrónico | 51.353 | 0 (0%) | 427 |
| 50 | `puntos_del_acuerdo` | Puntos del Acuerdo | Texto | Pilares del acuerdo de paz, si el contrato es post conflicto | 51.353 | 0 (0%) | 5 |
| 51 | `pilares_del_acuerdo` | Pilares del Acuerdo | Texto | Pilares del acuerdo de paz | 51.353 | 0 (0%) | 14 |
| 52 | `urlproceso` | URL Proceso | URL | URL del proceso de compra en la plataforma SECOP II | 51.353 | 0 (0%) | 43.449 |
| 53 | `nombre_representante_legal` | Nombre Representante Legal | Texto | Nombre del representante legal de la entidad | 51.353 | 0 (0%) | 15.760 |
| 54 | `nacionalidad_representante_legal` | Nacionalidad Representante Legal | Texto | Nacionalidad del representante legal de la entidad | 51.353 | 0 (0%) | 9 |
| 55 | `domicilio_representante_legal` | Domicilio Representante Legal | Texto | Dirección de domicilio del representante legal de la entidad | 51.353 | 0 (0%) | 4.511 |
| 56 | `tipo_de_identificaci_n_representante_legal` | Tipo de Identificación Representante Legal | Texto | Tipo de identificación del representante legal de la entidad | 51.353 | 0 (0%) | 7 |
| 57 | `identificaci_n_representante_legal` | Identificación Representante Legal | Texto | Número de identificación del representante legal de la entidad | 51.353 | 0 (0%) | 5.809 |
| 58 | `g_nero_representante_legal` | Género Representante Legal | Texto | Género sexual del representante legal de la entidad | 51.353 | 0 (0%) | 4 |
| 59 | `presupuesto_general_de_la_nacion_pgn` | Presupuesto General de la Nación – PGN | Número | Valor de origen de los recursos que corresponde al Presupuesto General de la Nación – PGN | 51.353 | 0 (0%) | 7.314 |
| 60 | `sistema_general_de_participaciones` | Sistema General de Participaciones | Número | Valor de origen de los recursos que corresponde al Sistema General de Participaciones | 51.353 | 0 (0%) | 4.531 |
| 61 | `sistema_general_de_regal_as` | Sistema General de Regalías | Número | Valor de origen de los recursos que corresponde al Sistema General de Regalías | 51.353 | 0 (0%) | 1.669 |
| 62 | `recursos_propios_alcald_as_gobernaciones_y_resguardos_ind_genas_` | Recursos Propios (Alcaldías, Gobernaciones y Resguardos Indígenas) | Número | Indica el valor de recursos de la entidad en el contrato electrónico | 51.353 | 0 (0%) | 14.909 |
| 63 | `recursos_de_credito` | Recursos de Crédito | Número | Valor de origen de los recursos que corresponde a Recursos de Crédito | 51.353 | 0 (0%) | 750 |
| 64 | `recursos_propios` | Recursos Propios | Número | Valor de origen de los recursos que corresponde a Recursos Propios | 51.353 | 0 (0%) | 7.607 |
| 65 | `ultima_actualizacion` | Ultima Actualización | Marca de tiempo variable | Fecha de última actualización del contrato electrónico | 33.301 | 18.052 (35.2%) | 2.083 |
| 66 | `codigo_entidad` | Código Entidad | Número | Código de la entidad en la plataforma SECOPII | 51.353 | 0 (0%) | 2.534 |
| 67 | `codigo_proveedor` | Código Proveedor | Texto | Código del proveedor en la plataforma SECOPII | 51.353 | 0 (0%) | 23.192 |
| 68 | `fecha_inicio_liquidacion` | Fecha Inicio Liquidación | Marca de tiempo variable | Fecha de inicio de liquidación del contrato electrónico | 25.664 | 25.689 (50.0%) | 3.008 |
| 69 | `fecha_fin_liquidacion` | Fecha Fin Liquidación | Marca de tiempo variable | Fecha de fin de liquidación del contrato electrónico | 25.658 | 25.695 (50.0%) | 3.511 |
| 70 | `objeto_del_contrato` | Objeto del Contrato | Texto | Objeto del contrato electrónico | 51.353 | 0 (0%) | 43.572 |
| 71 | `duraci_n_del_contrato` | Duración del contrato | Texto | Describe la duración del contrato en el tiempo | 51.353 | 0 (0%) | 986 |
| 72 | `nombre_del_banco` | Nombre del banco | Texto | Indica el nombre del banco en donde se consignarán los pagos del contrato | 51.353 | 0 (0%) | 288 |
| 73 | `tipo_de_cuenta` | Tipo de cuenta | Texto | Tipo de cuenta en la que se se consignaran los pagos del contrato | 51.353 | 0 (0%) | 3 |
| 74 | `n_mero_de_cuenta` | Número de cuenta | Texto | Número de cuenta en donde se harán los pagos del contrato | 51.353 | 0 (0%) | 5.574 |
| 75 | `el_contrato_puede_ser_prorrogado` | El contrato puede ser prorrogado | Texto | Indica si el contrato puede ser o no prorrogado | 51.353 | 0 (0%) | 2 |
| 76 | `nombre_ordenador_del_gasto` | Nombre ordenador del gasto | Texto | Describe el nombre del ordenador del gasto de la entidad compradora | 51.353 | 0 (0%) | 4.487 |
| 77 | `tipo_de_documento_ordenador_del_gasto` | Tipo de documento Ordenador del gasto | Texto | Indica el tipo de documento del ordenador del gasto de la entidad compradora | 51.353 | 0 (0%) | 8 |
| 78 | `n_mero_de_documento_ordenador_del_gasto` | Número de documento Ordenador del gasto | Texto | Indica el número de documento del ordenador del gasto | 51.353 | 0 (0%) | 4.422 |
| 79 | `nombre_supervisor` | Nombre supervisor | Texto | Describe el nombre del supervisor de la entidad compradora | 51.353 | 0 (0%) | 6.084 |
| 80 | `tipo_de_documento_supervisor` | Tipo de documento supervisor | Texto | Indica el tipo de documento del supervisor de la entidad compradora | 51.353 | 0 (0%) | 7 |
| 81 | `n_mero_de_documento_supervisor` | Número de documento supervisor | Texto | Indica el número de documento del supervisor | 51.353 | 0 (0%) | 5.911 |
| 82 | `nombre_ordenador_de_pago` | Nombre Ordenador de Pago | Texto | Describe el nombre del Ordenador de Pago de la entidad compradora | 51.353 | 0 (0%) | 908 |
| 83 | `tipo_de_documento_ordenador_de_pago` | Tipo de documento Ordenador de Pago | Texto | Indica el tipo de documento del Ordenador de Pago de la entidad compradora | 51.353 | 0 (0%) | 7 |
| 84 | `n_mero_de_documento_ordenador_de_pago` | Número de documento Ordenador de Pago | Texto | Indica el número de documento del Ordenador de Pago | 51.353 | 0 (0%) | 907 |
| 85 | `documentos_tipo` | Documentos Tipo | Texto | Indica si se utilizaron documentos tipo en el contrato | 51.353 | 0 (0%) | 2 |
| 86 | `descripcion_documentos_tipo` | Descripcion Documentos Tipo | Texto | Descripción de los documentos tipo utilizados | 51.353 | 0 (0%) | 9 |
| 87 | `fecha_de_notificaci_n_de_prorrogaci_n` | Fecha de notificación de prorrogación | Marca de tiempo variable | Infica la fecha de notificación de la prorrogación del contrato | 6.312 | 45.041 (87.7%) | 2.029 |

### Distribucion de valores (categoricas con <= 30 valores unicos)

**`orden`** (3 valores unicos)

| Valor | Cantidad |
|---|---|
| Territorial | 33.994 |
| Nacional | 16.689 |
| Corporación Autónoma | 670 |

**`sector`** (25 valores unicos)

| Valor | Cantidad |
|---|---|
| Servicio Público | 16.378 |
| No aplica/No pertenece | 9.699 |
| Transporte | 8.383 |
| defensa | 3.454 |
| Educación Nacional | 2.301 |
| Ambiente y Desarrollo Sostenible | 1.631 |
| Salud y Protección Social | 1.461 |
| Ley de Justicia | 1.253 |
| Trabajo | 1.143 |
| Vivienda, Ciudad y Territorio | 1.023 |

**`rama`** (4 valores unicos)

| Valor | Cantidad |
|---|---|
| Ejecutivo | 41.521 |
| Corporación Autónoma | 8.692 |
| Judicial | 1.092 |
| Legislativo | 48 |

**`entidad_centralizada`** (2 valores unicos)

| Valor | Cantidad |
|---|---|
| Centralizada | 42.959 |
| Descentralizada | 8.394 |

**`estado_contrato`** (11 valores unicos)

| Valor | Cantidad |
|---|---|
| Modificado | 16.390 |
| terminado | 12.003 |
| En ejecución | 10.331 |
| Cerrado | 3.222 |
| Aprobado | 2.694 |
| Borrador | 2.507 |
| Cancelado | 1.781 |
| Suspendido | 1.283 |
| enviado Proveedor | 661 |
| En aprobación | 441 |

**`tipo_de_contrato`** (1 valores unicos)

| Valor | Cantidad |
|---|---|
| Obra | 51.353 |

**`modalidad_de_contratacion`** (9 valores unicos)

| Valor | Cantidad |
|---|---|
| Selección Abreviada de Menor Cuantía | 14.129 |
| Mínima cuantía | 10.442 |
| Contratación directa | 10.239 |
| Licitación pública Obra Publica | 9.154 |
| Contratación régimen especial | 2.987 |
| Contratación régimen especial (con ofertas) | 2.006 |
| Contratación Directa (con ofertas) | 1.648 |
| Licitación pública | 437 |
| Seleccion Abreviada Menor Cuantia Sin Manifestacion Interes | 311 |

**`justificacion_modalidad_de`** (21 valores unicos)

| Valor | Cantidad |
|---|---|
| Presupuesto menor al 10% de la Menor Cuantía | 13.687 |
| Presupuesto inferior al 10% de la menor cuantía | 10.442 |
| Article30_1993 | 9.154 |
| Contratos o convenios Interadministrativos (valor cero) | 5.548 |
| Regla aplicable | 4.993 |
| Convenios Solidarios Regimen articulo 92 Ley 2166 de 2021 | 2.207 |
| Law2166of2021_Article95_SolidarityAgreements | 1.513 |
| Contratos o convenios Interadministrativos (con valor) | 1.446 |
| Urgencia manifiesta | 937 |
| Ley 1150 de 2007 | 437 |

**`condiciones_de_entrega`** (14 valores unicos)

| Valor | Cantidad |
|---|---|
| No Definido | 20.679 |
| A convenir | 15.159 |
| Como acordado previamente | 14.276 |
| Transporte incluido | 1.020 |
| DAP - Entregado en un punto (lugar de destino convenido) | 138 |
| Transporte no incluído | 37 |
| Transporte a cargo del comprador | 14 |
| CPT - Transporte pagado hasta (lugar de destino convenido) | 13 |
| DDP - Delivery duty place | 9 |
| CIF - Coste, seguro y flete (puerto de destino convenido) | 2 |

**`tipodocproveedor`** (7 valores unicos)

| Valor | Cantidad |
|---|---|
| NIT | 39.373 |
| Cédula de Ciudadanía | 7.243 |
| No Definido | 3.564 |
| Otro | 1.158 |
| Cédula de Extranjería | 13 |
| Tarjeta de Identidad | 1 |
| Permiso especial de permanencia | 1 |

---

## 2. Procesos de Contratación — Obra

**Archivo**: `data/procesos_contratacion_obra.parquet`

**Descripcion**: Procesos de compra pública de Obra en SECOP II. Contiene información pre-contractual: modalidad, plazos de publicación, presupuesto estimado y cantidad de oferentes.

| Atributo | Valor |
|---|---|
| Granularidad | 1 fila = 1 proceso de compra |
| Registros | 138.112 |
| Columnas | 57 |
| Notebook/Script | `02_procesos_contratacion.ipynb` |
| Fuente SECOP | `procesosDeContratacion` |

### Definicion de columnas

| # | Columna API | Nombre original | Tipo | Descripcion | No nulos | Nulos (%) | Unicos |
|---|---|---|---|---|---|---|---|
| 1 | `entidad` | Entidad | Texto | Nombre de la Entidad que publica el proceso de compra pública | 138.112 | 0 (0%) | 5.379 |
| 2 | `nit_entidad` | Nit Entidad | Texto | NIT de la Entidad que publicó el proceso | 138.112 | 0 (0%) | 5.266 |
| 3 | `departamento_entidad` | Departamento Entidad | Texto | Departamento en el cual está registrada la entidad | 138.112 | 0 (0%) | 34 |
| 4 | `ciudad_entidad` | Ciudad Entidad | Texto | Ciudad en la cual está registrada la entidad | 138.112 | 0 (0%) | 834 |
| 5 | `ordenentidad` | Orden Entidad | Texto | Orden de la Entidad (Nacional, Regional) | 138.112 | 0 (0%) | 3 |
| 6 | `codigo_pci` | Entidad Centralizada | Texto | Identifica si la entidad es o no centralizada | 138.112 | 0 (0%) | 2 |
| 7 | `id_del_proceso` | ID del Proceso | Texto | Identificador Único del Proceso, valor generado por la plataforma | 138.112 | 0 (0%) | 112.891 |
| 8 | `referencia_del_proceso` | Referencia del Proceso | Texto | Identificador del Proceso, valor generado por la Entidad | 138.112 | 0 (0%) | 96.938 |
| 9 | `ppi` | PCI | Texto | Código de Unidad - Sub-Unidad Contratación | 138.112 | 0 (0%) | 5.538 |
| 10 | `id_del_portafolio` | ID del Portafolio | Texto | Identificador del Portafolio al cual corresponde el proceso de compra | 138.112 | 0 (0%) | 76.322 |
| 11 | `nombre_del_procedimiento` | Nombre del Procedimiento | Texto | Nombre dado al proceso de compra por la Entidad | 138.112 | 0 (0%) | 91.352 |
| 12 | `descripci_n_del_procedimiento` | Descripción del Procedimiento | Texto | Primera definición de las características principales del proceso | 138.112 | 0 (0%) | 69.932 |
| 13 | `fase` | Fase | Texto | Fase en la que actualmente se encuentra el proceso | 136.413 | 1.699 (1.2%) | 10 |
| 14 | `fecha_de_publicacion_del` | Fecha de Publicación del Proceso | Marca de tiempo variable | Fecha de la publicación inicial del proceso de compra | 136.575 | 1.537 (1.1%) | 2.951 |
| 15 | `fecha_de_ultima_publicaci` | Fecha de Ultima Publicación | Marca de tiempo variable | Fecha de la última publicación hecha para el proceso de compra | 136.575 | 1.537 (1.1%) | 2.951 |
| 16 | `fecha_de_publicacion_fase_2` | Fecha de Publicación (Fase Borrador) | Marca de tiempo variable | Fecha de publicación, dentro del proceso, de la fase Borrador | 23.684 | 114.428 (82.9%) | 2.358 |
| 17 | `precio_base` | Precio Base | Número | Precio Base, proyectado, del proceso de Compra | 138.112 | 0 (0%) | 55.518 |
| 18 | `modalidad_de_contratacion` | Modalidad de Contratación | Texto | Modalidad de selección bajo la cual se desarrolla el proceso de Compra | 138.112 | 0 (0%) | 9 |
| 19 | `justificaci_n_modalidad_de` | Justificación Modalidad de Contratación | Texto | En caso de requerirse, Justificación para la modalidad de selección elegida para el proceso de co... | 138.112 | 0 (0%) | 17 |
| 20 | `duracion` | Duración | Número | Valor de la Duración estimada del proceso de compra pública | 138.112 | 0 (0%) | 518 |
| 21 | `unidad_de_duracion` | Unidad de Duración | Texto | Unidad que aplica a la Duración estimada del proceso de compra pública | 138.112 | 0 (0%) | 5 |
| 22 | `fecha_de_recepcion_de` | Fecha de Recepción de Respuestas | Marca de tiempo variable | Fecha asignada para la recepción de respuestas por parte de los proveedores, dentro del proceso d... | 100.044 | 38.068 (27.6%) | 2.414 |
| 23 | `fecha_de_apertura_de_respuesta` | Fecha de Apertura de Respuesta | Marca de tiempo variable | Fecha Estimada para la Apertura de las respuestas | 98.142 | 39.970 (28.9%) | 2.420 |
| 24 | `fecha_de_apertura_efectiva` | Fecha de Apertura Efectiva | Marca de tiempo variable | Fecha Real para la Apertura de las respuestas | 95.148 | 42.964 (31.1%) | 2.522 |
| 25 | `ciudad_de_la_unidad_de` | Ciudad de la Unidad de Contratación | Texto | Cuidad en la que aparece registrada la unidad de contratación de la Entidad | 138.112 | 0 (0%) | 855 |
| 26 | `nombre_de_la_unidad_de` | Nombre de la Unidad de Contratación | Texto | Nombre de la unidad de contratación de la Entidad | 138.112 | 0 (0%) | 5.171 |
| 27 | `proveedores_invitados` | Proveedores Invitados | Número | Número de Proveedores invitados a participar del proceso, en total | 138.112 | 0 (0%) | 562 |
| 28 | `proveedores_con_invitacion` | Proveedores con Invitación Directa | Número | Proveedores con Invitación a participar hecha de forma directa | 138.112 | 0 (0%) | 283 |
| 29 | `visualizaciones_del` | Visualizaciones del Procedimiento | Número | Número de Visualizaciones hechas a través de la herramienta, del Proceso de Compra | 138.112 | 0 (0%) | 564 |
| 30 | `proveedores_que_manifestaron` | Proveedores que Manifestaron Interés | Número | Proveedores que Manifestaron Interés en el proceso a través de la plataforma | 138.112 | 0 (0%) | 1 |
| 31 | `respuestas_al_procedimiento` | Respuestas al Procedimiento | Número | Respuestas hechas al procedimiento, tanto de proveedores como de la misma entidad | 138.112 | 0 (0%) | 170 |
| 32 | `respuestas_externas` | Respuestas Externas | Número | Número de Respuestas hechas por entes externos | 138.112 | 0 (0%) | 14 |
| 33 | `conteo_de_respuestas_a_ofertas` | Conteo de Respuestas a Ofertas | Número | Número de Respuestas hechas de forma directa en las ofertas | 138.112 | 0 (0%) | 1 |
| 34 | `proveedores_unicos_con` | Proveedores Únicos con Respuestas | Número | Proveedores Únicos que han redactado respuestas en el proceso | 138.112 | 0 (0%) | 170 |
| 35 | `numero_de_lotes` | Numero de Lotes | Número | Número de lotes de artículos solicitados dentro del proceso | 138.112 | 0 (0%) | 21 |
| 36 | `estado_del_procedimiento` | Estado del Procedimiento | Texto | Estado actual de desarrollo del procedimiento de compra pública | 138.112 | 0 (0%) | 9 |
| 37 | `id_estado_del_procedimiento` | ID, Estado del Procedimiento | Número | Identificador del Estado del procedimiento | 138.112 | 0 (0%) | 5 |
| 38 | `adjudicado` | Adjudicado | Texto | Determina si el proceso fue adjudicado | 138.112 | 0 (0%) | 2 |
| 39 | `id_adjudicacion` | ID Adjudicación | Texto | Identificador de la adjudicación | 138.112 | 0 (0%) | 33.566 |
| 40 | `codigoproveedor` | Código Proveedor | Texto | Código, en la plataforma, del proveedor adjudicado | 138.112 | 0 (0%) | 23.233 |
| 41 | `departamento_proveedor` | Departamento Proveedor | Texto | Departamento en el que está registrado el proveedor adjudicado | 138.112 | 0 (0%) | 37 |
| 42 | `ciudad_proveedor` | Ciudad Proveedor | Texto | Ciudad en la que está registrado el proveedor adjudicado | 138.112 | 0 (0%) | 861 |
| 43 | `valor_total_adjudicacion` | Valor Total Adjudicación | Número | Valor total Adjudicado | 138.112 | 0 (0%) | 32.375 |
| 44 | `nombre_del_adjudicador` | Nombre del Adjudicador | Texto | Nombre del Usuario que ejecutó la acción de adjudicación | 138.112 | 0 (0%) | 7.718 |
| 45 | `nombre_del_proveedor` | Nombre del Proveedor Adjudicado | Texto | Nombre del Proveedor Adjudicado | 138.112 | 0 (0%) | 22.816 |
| 46 | `nit_del_proveedor_adjudicado` | NIT del Proveedor Adjudicado | Texto | NIT del Proveedor Adjudicado | 138.112 | 0 (0%) | 8.437 |
| 47 | `codigo_principal_de_categoria` | Código Principal de Categoría | Texto | Código UNSPSC de la categoría principal del producto o servicio adquirido en proceso de compra | 138.112 | 0 (0%) | 2.541 |
| 48 | `estado_de_apertura_del_proceso` | Estado de Apertura del Proceso | Texto | Estado actual de Apertura de información del proceso | 138.112 | 0 (0%) | 2 |
| 49 | `tipo_de_contrato` | Tipo de Contrato | Texto | Tipo de Contrato definido para el proceso de compra | 138.112 | 0 (0%) | 1 |
| 50 | `subtipo_de_contrato` | Subtipo de Contrato | Texto | Subtipo de Contrato definido para el proceso de compra | 138.112 | 0 (0%) | 1 |
| 51 | `categorias_adicionales` | Categorías Adicionales | Texto | Identificador de las categorías UNSPSC adicionales, incluidas en el producto o servicio adquirido... | 138.112 | 0 (0%) | 10.273 |
| 52 | `urlproceso` | URL Proceso | URL | URL, en la plataforma, en la que se puede consultar el proceso de compra | 138.112 | 0 (0%) | 111.194 |
| 53 | `codigo_entidad` | Código Entidad | Número | Código de la entidad en la plataforma SECOPII | 138.112 | 0 (0%) | 5.538 |
| 54 | `estado_resumen` | Estado Resumen | Texto | Resumen del estado del proceso de compra pública | 138.112 | 0 (0%) | 12 |
| 55 | `fecha_de_publicacion_fase_3` | Fecha de Publicación (Fase Selección) | Marca de tiempo variable | Fecha de publicación, dentro del proceso, de la fase Selección | 98.809 | 39.303 (28.5%) | 2.749 |
| 56 | `fecha_adjudicacion` | Fecha Adjudicación | Marca de tiempo variable | Fecha en la que se hizo la adjudicación del proceso para el proveedor seleccionado | 50.974 | 87.138 (63.1%) | 2.345 |
| 57 | `fecha_de_publicacion` | Fecha de Publicación (Manifestación de Interés) | Marca de tiempo variable | Fecha de publicación, dentro del proceso, de la fase de Manifestación de Interés | 14.082 | 124.030 (89.8%) | 1.969 |

### Distribucion de valores (categoricas con <= 30 valores unicos)

**`ordenentidad`** (3 valores unicos)

| Valor | Cantidad |
|---|---|
| Territorial | 88.255 |
| Nacional | 47.860 |
| Corporación Autónoma | 1.997 |

**`codigo_pci`** (2 valores unicos)

| Valor | Cantidad |
|---|---|
| Centralizada | 117.832 |
| Descentralizada | 20.280 |

**`fase`** (10 valores unicos)

| Valor | Cantidad |
|---|---|
| Presentación de oferta | 71.464 |
| Fase de Selección (Presentación de ofertas) | 22.688 |
| Presentación de observaciones | 21.874 |
| Manifestación de interés (Menor Cuantía) | 13.415 |
| Fase de ofertas | 4.546 |
| Clarification submission | 1.006 |
| Selección de ofertas (borrador) | 740 |
| Pré-Calificación de competidores | 639 |
| Presentación de Observaciones | 29 |
| Proceso de ofertas | 12 |

**`modalidad_de_contratacion`** (9 valores unicos)

| Valor | Cantidad |
|---|---|
| Selección Abreviada de Menor Cuantía | 46.720 |
| Licitación pública Obra Publica | 32.270 |
| Contratación régimen especial | 27.947 |
| Mínima cuantía | 13.358 |
| Contratación directa | 10.085 |
| Contratación régimen especial (con ofertas) | 3.316 |
| Contratación Directa (con ofertas) | 1.904 |
| Licitación pública | 1.735 |
| Seleccion Abreviada Menor Cuantia Sin Manifestacion Interes | 777 |

**`justificaci_n_modalidad_de`** (17 valores unicos)

| Valor | Cantidad |
|---|---|
| Presupuesto menor al 10% de la Menor Cuantía | 45.232 |
| No Defenido | 33.753 |
| Regla aplicable | 31.261 |
| Presupuesto inferior al 10% de la menor cuantía | 13.358 |
| Contratos o convenios Interadministrativos (valor cero) | 5.493 |
| Convenios Solidarios Regimen articulo 92 Ley 2166 de 2021 | 2.171 |
| Ley 1150 de 2007 | 1.735 |
| Contratos o convenios Interadministrativos (con valor) | 1.670 |
| Defensa y seguridad nacional | 1.257 |
| Proceso de licitación pública declarado desierto | 958 |

**`unidad_de_duracion`** (5 valores unicos)

| Valor | Cantidad |
|---|---|
| Mes(es) | 72.963 |
| día(s) | 64.447 |
| Semana(s) | 488 |
| Año(s) | 187 |
| Hora(s) | 27 |

**`proveedores_que_manifestaron`** (1 valores unicos)

| Valor | Cantidad |
|---|---|
| 0 | 138.112 |

**`respuestas_externas`** (14 valores unicos)

| Valor | Cantidad |
|---|---|
| 0 | 136.442 |
| 1 | 1.184 |
| 6 | 210 |
| 2 | 84 |
| 4 | 81 |
| 3 | 66 |
| 7 | 12 |
| 8 | 12 |
| 5 | 9 |
| 9 | 8 |

**`conteo_de_respuestas_a_ofertas`** (1 valores unicos)

| Valor | Cantidad |
|---|---|
| 0 | 138.112 |

**`numero_de_lotes`** (21 valores unicos)

| Valor | Cantidad |
|---|---|
| 0 | 117.989 |
| 2 | 2.332 |
| 3 | 2.306 |
| 38 | 1.889 |
| 4 | 1.836 |
| 5 | 1.305 |
| 18 | 1.298 |
| 7 | 1.193 |
| 15 | 978 |
| 8 | 903 |

---

## 3. Adiciones — Obra

**Archivo**: `data/adiciones_obra.parquet`

**Descripcion**: Modificaciones contractuales (adiciones en valor, tiempo, o ambos) registradas sobre contratos de Obra en SECOP II.

| Atributo | Valor |
|---|---|
| Granularidad | 1 fila = 1 modificación contractual |
| Registros | 249.037 |
| Columnas | 5 |
| Notebook/Script | `03_adiciones.ipynb` |
| Fuente SECOP | `adiciones` |

### Definicion de columnas

| # | Columna API | Nombre original | Tipo | Descripcion | No nulos | Nulos (%) | Unicos |
|---|---|---|---|---|---|---|---|
| 1 | `identificador` | Identificador | Texto | Identificador único del evento de modificación | 249.037 | 0 (0%) | 143.201 |
| 2 | `id_contrato` | id_contrato | str | (sin definición oficial — columna derivada o calculada) | 249.037 | 0 (0%) | 33.465 |
| 3 | `tipo` | Tipo | Texto | Tipo de modificación, de acuerdo con el impacto que tiene sobre el contrato | 249.037 | 0 (0%) | 8 |
| 4 | `descripcion` | descripcion | str | (sin definición oficial — columna derivada o calculada) | 249.037 | 0 (0%) | 102.053 |
| 5 | `fecharegistro` | fecharegistro | str | (sin definición oficial — columna derivada o calculada) | 249.037 | 0 (0%) | 658 |

### Distribucion de valores (categoricas con <= 30 valores unicos)

**`tipo`** (8 valores unicos)

| Valor | Cantidad |
|---|---|
| MODIFICACION GENERAL | 124.918 |
| No definido | 43.038 |
| REACTIVACIoN | 31.802 |
| SUSPENSIoN | 29.834 |
| CONCLUSION | 10.683 |
| ADICION EN EL VALOR | 7.672 |
| CESION | 1.088 |
| EXTENSION | 2 |

---

## 4. Proveedores Registrados — Obra

**Archivo**: `data/proveedores_obra.parquet`

**Descripcion**: Proveedores registrados en SECOP II que participan en contratos de Obra. Incluye datos de registro, clasificación UNSPSC, tamaño de empresa y ubicación.

| Atributo | Valor |
|---|---|
| Granularidad | 1 fila = 1 proveedor registrado |
| Registros | 13.117 |
| Columnas | 25 |
| Notebook/Script | `04_proveedores.ipynb` |
| Fuente SECOP | `proveedoresRegistrados` |

### Definicion de columnas

| # | Columna API | Nombre original | Tipo | Descripcion | No nulos | Nulos (%) | Unicos |
|---|---|---|---|---|---|---|---|
| 1 | `codigo` | Código | Texto | Es el código del proveedor en la plataforma SECOPII | 13.117 | 0 (0%) | 12.618 |
| 2 | `nombre` | Nombre | Texto | Nombre del Proveedor, como se registró en SECOP II | 13.117 | 0 (0%) | 12.429 |
| 3 | `nit` | NIT | Texto | Número de Identificación con el que figura el proveedor en SECOP II | 13.117 | 0 (0%) | 12.571 |
| 4 | `es_entidad` | Es Entidad | Texto | Indica si el proveedor también es una entidad compradora en SECOPII | 13.117 | 0 (0%) | 2 |
| 5 | `es_grupo` | Es grupo | Texto | Indica si la entidad pertenece a un grupo | 13.117 | 0 (0%) | 1 |
| 6 | `esta_activa` | Esta Activa | Texto | Indica si el proveedor esta activo en el SECOPII | 13.117 | 0 (0%) | 2 |
| 7 | `fecha_creacion` | Fecha Creación | Marca de tiempo variable | Fecha en la que se hizo el primer registro del proveedor | 13.117 | 0 (0%) | 3.010 |
| 8 | `codigo_categoria_principal` | Código Categoría Principal | Texto | Código UNSPSC principal del proveedor | 13.117 | 0 (0%) | 69 |
| 9 | `descripcion_categoria_principal` | Descripción Categoría Principal | Texto | Descripción UNSPSC principal del proveedor | 13.117 | 0 (0%) | 69 |
| 10 | `telefono` | telefono | str | (sin definición oficial — columna derivada o calculada) | 13.117 | 0 (0%) | 8.939 |
| 11 | `fax` | Fax | Texto | Indica el número de fax reportado por el proveedor | 13.117 | 0 (0%) | 792 |
| 12 | `correo` | Correo | Texto | Indica la dirección de correo electrónico del proveedor | 13.117 | 0 (0%) | 9.254 |
| 13 | `direccion` | direccion | str | (sin definición oficial — columna derivada o calculada) | 13.117 | 0 (0%) | 8.932 |
| 14 | `pais` | pais | str | (sin definición oficial — columna derivada o calculada) | 13.117 | 0 (0%) | 3 |
| 15 | `departamento` | Departamento | Texto | En caso de Ser un proveedor colombiano, indica el departamento al que corresponde la ubicación pr... | 13.117 | 0 (0%) | 36 |
| 16 | `municipio` | Municipio | Texto | En caso de Ser un proveedor colombiano, indica el Municipio al que corresponde la ubicación princ... | 13.117 | 0 (0%) | 708 |
| 17 | `sitio_web` | Sitio web | Texto | Indica el enlace del sitio web del proveedor | 13.117 | 0 (0%) | 1.386 |
| 18 | `tipo_empresa` | Tipo Empresa | Texto | Tipo de Empresa que declara el proveedor al registrarse | 13.117 | 0 (0%) | 30 |
| 19 | `nombre_representante_legal` | Nombre representante legal | Texto | Indica el nombre del representa nte legal del proveedor | 13.117 | 0 (0%) | 12.394 |
| 20 | `tipo_doc_representante_legal` | Tipo doc. representante legal | Texto | Indica el tipo de documento del representante legal del proveedor | 13.117 | 0 (0%) | 4 |
| 21 | `n_mero_doc_representante_legal` | Número doc. representante legal | Texto | Indica el número de documento del representante legal del proveedor | 13.117 | 0 (0%) | 12.571 |
| 22 | `telefono_representante_legal` | Teléfono representante legal | Texto | Indica el número telefónico del representante legal del proveedor | 13.117 | 0 (0%) | 11.784 |
| 23 | `correo_representante_legal` | Correo representante legal | Texto | Indica el correo electrónico del representante legal del proveedor | 13.117 | 0 (0%) | 12.453 |
| 24 | `espyme` | Es Pyme | Texto | Determina si el proveedor se registró como pequeña empresa | 13.117 | 0 (0%) | 2 |
| 25 | `ubicacion` | ubicacion | str | (sin definición oficial — columna derivada o calculada) | 13.117 | 0 (0%) | 774 |

### Distribucion de valores (categoricas con <= 30 valores unicos)

**`es_entidad`** (2 valores unicos)

| Valor | Cantidad |
|---|---|
| No | 13.115 |
| Si | 2 |

**`es_grupo`** (1 valores unicos)

| Valor | Cantidad |
|---|---|
| No | 13.117 |

**`esta_activa`** (2 valores unicos)

| Valor | Cantidad |
|---|---|
| Si | 13.116 |
| No | 1 |

**`pais`** (3 valores unicos)

| Valor | Cantidad |
|---|---|
| CO | 13.115 |
| BE | 1 |
| US | 1 |

**`tipo_empresa`** (30 valores unicos)

| Valor | Cantidad |
|---|---|
| SOCIEDAD POR ACCIONES SIMPLIFICADA | 4.461 |
| PERSONA NATURAL COLOMBIANA | 2.261 |
| OTRO | 2.077 |
| ENTIDADES SIN aNIMO DE LUCRO | 1.603 |
| ASOCIACIONES | 652 |
| SOCIEDAD ANoNIMA ABIERTA COLOMBIANA | 318 |
| JUNTA DE ACCIoN COMUNAL. | 315 |
| SOCIEDAD DE RESPONSABILIDAD LIMITADA COLOMBIANA | 299 |
| COOPERATIVAS | 280 |
| SOCIEDAD ANoNIMA CERRADA COLOMBIANA | 185 |

**`tipo_doc_representante_legal`** (4 valores unicos)

| Valor | Cantidad |
|---|---|
| NIT | 10.494 |
| Cédula de Ciudadanía | 2.515 |
| Otro | 102 |
| Cédula de Extranjería | 6 |

**`espyme`** (2 valores unicos)

| Valor | Cantidad |
|---|---|
| SI | 7.870 |
| NO | 5.247 |

---

## 5. Proponentes por Proceso — Obra

**Archivo**: `data/proponentes_por_proceso_obra.parquet`

**Descripcion**: Listado de todos los proveedores que presentaron oferta en cada proceso de contratación de Obra. Permite conocer la competencia real de cada licitación.

| Atributo | Valor |
|---|---|
| Granularidad | 1 fila = 1 proponente en 1 proceso |
| Registros | 276.770 |
| Columnas | 9 |
| Notebook/Script | `06_proponentes_por_proceso.ipynb` |
| Fuente SECOP | `proponentesporProceso` |

### Definicion de columnas

| # | Columna API | Nombre original | Tipo | Descripcion | No nulos | Nulos (%) | Unicos |
|---|---|---|---|---|---|---|---|
| 1 | `id_procedimiento` | ID Procedimiento | Texto | Identificador del procedimiento | 276.770 | 0 (0%) | 33.171 |
| 2 | `fecha_publicaci_n` | Fecha Publicación | Marca de tiempo variable | Fecha de publicacion del proceso | 276.767 | 3 (0%) | 2.417 |
| 3 | `nombre_procedimiento` | Nombre Procedimiento | Texto | Nombre del proceso | 276.770 | 0 (0%) | 30.284 |
| 4 | `nit_entidad` | NIT Entidad | Número | Nit de la entidad contratante | 276.770 | 0 (0%) | 2.020 |
| 5 | `codigo_entidad` | Código Entidad | Número | Codigo de la entidad contratante | 276.770 | 0 (0%) | 2.268 |
| 6 | `entidad_compradora` | Entidad Compradora | Texto | Entidad compradora | 276.770 | 0 (0%) | 2.264 |
| 7 | `proveedor` | Proveedor | Texto | Nombre del proveedor | 276.770 | 0 (0%) | 89.561 |
| 8 | `nit_proveedor` | NIT Proveedor | Texto | Nit del proveedor | 276.770 | 0 (0%) | 23.759 |
| 9 | `codigo_proveedor` | Código Proveedor | Número | Identificador único de la plataforma SECOP II, del Proveedor | 276.770 | 0 (0%) | 98.575 |

---

## 6. Contratos + Adiciones (integrado)

**Archivo**: `data/contratos_adiciones_obra.parquet`

**Descripcion**: Dataset resultado del JOIN entre contratos electrónicos y adiciones. Consolida la información contractual con las modificaciones, a nivel de contrato.

| Atributo | Valor |
|---|---|
| Granularidad | 1 fila = 1 contrato (con adiciones agregadas) |
| Registros | 48.331 |
| Columnas | 111 |
| Notebook/Script | `05_integracion_contratos_adiciones.ipynb` |

### Definicion de columnas

| # | Columna API | Nombre original | Tipo | Descripcion | No nulos | Nulos (%) | Unicos |
|---|---|---|---|---|---|---|---|
| 1 | `nombre_entidad` | Nombre Entidad | Texto | Nombre de la entidad del estado que publica el contrato | 48.331 | 0 (0%) | 2.528 |
| 2 | `nit_entidad` | Nit Entidad | Número | NIT de la entidad del estado que publica el contrato | 48.331 | 0 (0%) | 2.270 |
| 3 | `departamento` | Departamento | Texto | Departamento en el cual se registró la entidad del estado que publica el contrato | 48.331 | 0 (0%) | 34 |
| 4 | `ciudad` | Ciudad | Texto | Ciudad en el cual se registró la entidad del estado que publica el contrato | 48.331 | 0 (0%) | 617 |
| 5 | `localizaci_n` | Localización | Texto | Ubicación completa de la entidad del estado que publica el contrato | 48.331 | 0 (0%) | 737 |
| 6 | `orden` | Orden | Texto | Orden entidad del estado que publica el contrato | 48.331 | 0 (0%) | 3 |
| 7 | `sector` | Sector | Texto | Sector entidad del estado que publica el contrato | 48.331 | 0 (0%) | 25 |
| 8 | `rama` | Rama | Texto | Rama del estado de la entidad que publica el contrato | 48.331 | 0 (0%) | 4 |
| 9 | `entidad_centralizada` | Entidad Centralizada | Texto | Define si la entidad es descentralizada o centralizada | 48.331 | 0 (0%) | 2 |
| 10 | `proceso_de_compra` | Proceso de Compra | Texto | Identificador del proceso de compra publicado | 48.331 | 0 (0%) | 43.451 |
| 11 | `id_contrato` | ID Contrato | Texto | Identificador del contrato firmado, generado por la plataforma | 48.331 | 0 (0%) | 48.331 |
| 12 | `referencia_del_contrato` | Referencia del Contrato | Texto | Identificador del contrato firmado, generado por la entidad del estado | 48.331 | 0 (0%) | 45.910 |
| 13 | `estado_contrato` | Estado Contrato | Texto | Estado del contrato, frente a su ejecución, firma o liquidación | 48.331 | 0 (0%) | 11 |
| 14 | `codigo_de_categoria_principal` | Código de Categoría Principal | Texto | Código UNSPSC de la categoría principal para el contrato | 48.331 | 0 (0%) | 1.506 |
| 15 | `descripcion_del_proceso` | Descripción del Proceso | Texto | Descripción del objeto del proceso de compra | 48.331 | 0 (0%) | 43.445 |
| 16 | `tipo_de_contrato` | Tipo de Contrato | Texto | Tipo de contrato de acuerdo con su marco jurídico | 48.331 | 0 (0%) | 1 |
| 17 | `modalidad_de_contratacion` | Modalidad de Contratación | Texto | Modalidad de contratación de acuerdo con el modelo de selección | 48.331 | 0 (0%) | 9 |
| 18 | `justificacion_modalidad_de` | Justificación Modalidad de Contratación | Texto | Justificación de la modalidad, el escenario bajo el cual se toma la decisión de definir una u otr... | 48.331 | 0 (0%) | 21 |
| 19 | `fecha_de_firma` | Fecha de Firma | Marca de tiempo variable | Fecha de firma del contrato electrónico | 43.181 | 5.150 (10.7%) | 2.402 |
| 20 | `fecha_de_inicio_del_contrato` | Fecha de Inicio del Contrato | Marca de tiempo variable | Fecha de inicio de las responsabilidades contractuales | 42.252 | 6.079 (12.6%) | 2.471 |
| 21 | `fecha_de_fin_del_contrato` | Fecha de Fin del Contrato | Marca de tiempo variable | Fecha de fin de las responsabilidades contractuales | 46.832 | 1.499 (3.1%) | 3.468 |
| 22 | `condiciones_de_entrega` | Condiciones de Entrega | Texto | Condiciones bajo las cuales se entrega el producto o servicio | 48.331 | 0 (0%) | 14 |
| 23 | `tipodocproveedor` | Tipo Doc Proveedor | Texto | Tipo de documento del proveedor adjudicado | 48.331 | 0 (0%) | 7 |
| 24 | `documento_proveedor` | Documento Proveedor | Texto | Número de documento del proveedor adjudicado | 48.331 | 0 (0%) | 18.641 |
| 25 | `proveedor_adjudicado` | Proveedor Adjudicado | Texto | Nombre del proveedor adjudicado | 48.331 | 0 (0%) | 22.770 |
| 26 | `es_grupo` | Es Grupo | Texto | Determina el proveedor es un grupo de entidades, existe un conjunto de datos de CCE que contiene ... | 48.331 | 0 (0%) | 2 |
| 27 | `es_pyme` | Es Pyme | Texto | Determina si la empresa es una Pyme | 48.331 | 0 (0%) | 2 |
| 28 | `habilita_pago_adelantado` | Habilita Pago Adelantado | Texto | Determina si el contrato tiene habilitada la opción de pago de adelantos | 48.331 | 0 (0%) | 3 |
| 29 | `liquidaci_n` | Liquidación | Texto | Determina si el contrato ha sido liquidado | 48.331 | 0 (0%) | 2 |
| 30 | `obligaci_n_ambiental` | Obligación Ambiental | Texto | Determina si el contrato tiene compromisos de cumplimiento a obligaciones ambientales | 48.331 | 0 (0%) | 2 |
| 31 | `obligaciones_postconsumo` | Obligaciones Post consumo | Texto | Determina si el contrato tiene compromisos de cumplimiento a obligaciones posteriores a la entreg... | 48.331 | 0 (0%) | 2 |
| 32 | `reversion` | Reversión | Texto | Determina si el contrato ha sido reversado | 48.331 | 0 (0%) | 2 |
| 33 | `origen_de_los_recursos` | Origen de los Recursos | Texto | Origen de los Recursos, a nivel presupuestal | 48.331 | 0 (0%) | 2 |
| 34 | `destino_gasto` | Destino Gasto | Texto | Destino del gasto, a nivel presupuestal | 48.331 | 0 (0%) | 3 |
| 35 | `valor_del_contrato` | Valor del Contrato | Número | Valor total del contrato | 48.331 | 0 (0%) | 39.774 |
| 36 | `valor_de_pago_adelantado` | Valor de pago adelantado | Número | Valor del pago por adelantado | 48.331 | 0 (0%) | 1.106 |
| 37 | `valor_facturado` | Valor Facturado | Número | Valor Facturado a la fecha | 48.331 | 0 (0%) | 16.252 |
| 38 | `valor_pendiente_de_pago` | Valor Pendiente de Pago | Número | Valor Pendiente de Pago a la fecha | 48.331 | 0 (0%) | 33.906 |
| 39 | `valor_pagado` | Valor Pagado | Número | Valor Pagado a la fecha | 48.331 | 0 (0%) | 13.144 |
| 40 | `valor_amortizado` | Valor Amortizado | Número | Valor Amortizado a la fecha | 48.331 | 0 (0%) | 239 |
| 41 | `valor_pendiente_de` | Valor Pendiente de Amortización | Número | Valor Pendiente de Amortización a la fecha | 48.331 | 0 (0%) | 998 |
| 42 | `valor_pendiente_de_ejecucion` | Valor Pendiente de Ejecución | Número | Valor Pendiente de Ejecución a la fecha | 48.331 | 0 (0%) | 33.882 |
| 43 | `estado_bpin` | Estado BPIN | Texto | Estado de asignación del código del Banco de Proyectos de Inversión | 48.331 | 0 (0%) | 2 |
| 44 | `c_digo_bpin` | Código BPIN | Texto | Código asociado al Banco de Proyectos de Inversión | 48.331 | 0 (0%) | 7.771 |
| 45 | `anno_bpin` | Anno BPIN | Texto | Año de asignación del código del Banco de Proyectos de Inversión | 48.331 | 0 (0%) | 8 |
| 46 | `saldo_cdp` | Saldo CDP | Número | Saldo del CDP asignado al proceso y al contrato | 48.331 | 0 (0%) | 20.651 |
| 47 | `saldo_vigencia` | Saldo Vigencia | Número | Saldo actual para la vigencia del CDP asignado al proceso y al contrato | 48.331 | 0 (0%) | 902 |
| 48 | `espostconflicto` | Es Post Conflicto | Texto | Determina si el proceso está asociado a algún evento de acuerdo de paz | 48.331 | 0 (0%) | 2 |
| 49 | `dias_adicionados` | Días adicionados | Número | Días adicionados al contrato electrónico | 48.331 | 0 (0%) | 427 |
| 50 | `puntos_del_acuerdo` | Puntos del Acuerdo | Texto | Pilares del acuerdo de paz, si el contrato es post conflicto | 48.331 | 0 (0%) | 5 |
| 51 | `pilares_del_acuerdo` | Pilares del Acuerdo | Texto | Pilares del acuerdo de paz | 48.331 | 0 (0%) | 14 |
| 52 | `urlproceso` | URL Proceso | URL | URL del proceso de compra en la plataforma SECOP II | 48.331 | 0 (0%) | 43.449 |
| 53 | `nombre_representante_legal` | Nombre Representante Legal | Texto | Nombre del representante legal de la entidad | 48.331 | 0 (0%) | 15.760 |
| 54 | `nacionalidad_representante_legal` | Nacionalidad Representante Legal | Texto | Nacionalidad del representante legal de la entidad | 48.331 | 0 (0%) | 9 |
| 55 | `domicilio_representante_legal` | Domicilio Representante Legal | Texto | Dirección de domicilio del representante legal de la entidad | 48.331 | 0 (0%) | 4.511 |
| 56 | `tipo_de_identificaci_n_representante_legal` | Tipo de Identificación Representante Legal | Texto | Tipo de identificación del representante legal de la entidad | 48.331 | 0 (0%) | 7 |
| 57 | `identificaci_n_representante_legal` | Identificación Representante Legal | Texto | Número de identificación del representante legal de la entidad | 48.331 | 0 (0%) | 5.809 |
| 58 | `g_nero_representante_legal` | Género Representante Legal | Texto | Género sexual del representante legal de la entidad | 48.331 | 0 (0%) | 4 |
| 59 | `presupuesto_general_de_la_nacion_pgn` | Presupuesto General de la Nación – PGN | Número | Valor de origen de los recursos que corresponde al Presupuesto General de la Nación – PGN | 48.331 | 0 (0%) | 7.314 |
| 60 | `sistema_general_de_participaciones` | Sistema General de Participaciones | Número | Valor de origen de los recursos que corresponde al Sistema General de Participaciones | 48.331 | 0 (0%) | 4.531 |
| 61 | `sistema_general_de_regal_as` | Sistema General de Regalías | Número | Valor de origen de los recursos que corresponde al Sistema General de Regalías | 48.331 | 0 (0%) | 1.669 |
| 62 | `recursos_propios_alcald_as_gobernaciones_y_resguardos_ind_genas_` | Recursos Propios (Alcaldías, Gobernaciones y Resguardos Indígenas) | Número | Indica el valor de recursos de la entidad en el contrato electrónico | 48.331 | 0 (0%) | 14.909 |
| 63 | `recursos_de_credito` | Recursos de Crédito | Número | Valor de origen de los recursos que corresponde a Recursos de Crédito | 48.331 | 0 (0%) | 750 |
| 64 | `recursos_propios` | Recursos Propios | Número | Valor de origen de los recursos que corresponde a Recursos Propios | 48.331 | 0 (0%) | 7.607 |
| 65 | `ultima_actualizacion` | Ultima Actualización | Marca de tiempo variable | Fecha de última actualización del contrato electrónico | 31.142 | 17.189 (35.6%) | 2.083 |
| 66 | `codigo_entidad` | Código Entidad | Número | Código de la entidad en la plataforma SECOPII | 48.331 | 0 (0%) | 2.534 |
| 67 | `codigo_proveedor` | Código Proveedor | Texto | Código del proveedor en la plataforma SECOPII | 48.331 | 0 (0%) | 23.192 |
| 68 | `fecha_inicio_liquidacion` | Fecha Inicio Liquidación | Marca de tiempo variable | Fecha de inicio de liquidación del contrato electrónico | 24.024 | 24.307 (50.3%) | 3.008 |
| 69 | `fecha_fin_liquidacion` | Fecha Fin Liquidación | Marca de tiempo variable | Fecha de fin de liquidación del contrato electrónico | 24.019 | 24.312 (50.3%) | 3.511 |
| 70 | `objeto_del_contrato` | Objeto del Contrato | Texto | Objeto del contrato electrónico | 48.331 | 0 (0%) | 43.572 |
| 71 | `duraci_n_del_contrato` | Duración del contrato | Texto | Describe la duración del contrato en el tiempo | 48.331 | 0 (0%) | 986 |
| 72 | `nombre_del_banco` | Nombre del banco | Texto | Indica el nombre del banco en donde se consignarán los pagos del contrato | 48.331 | 0 (0%) | 288 |
| 73 | `tipo_de_cuenta` | Tipo de cuenta | Texto | Tipo de cuenta en la que se se consignaran los pagos del contrato | 48.331 | 0 (0%) | 3 |
| 74 | `n_mero_de_cuenta` | Número de cuenta | Texto | Número de cuenta en donde se harán los pagos del contrato | 48.331 | 0 (0%) | 5.574 |
| 75 | `el_contrato_puede_ser_prorrogado` | El contrato puede ser prorrogado | Texto | Indica si el contrato puede ser o no prorrogado | 48.331 | 0 (0%) | 2 |
| 76 | `nombre_ordenador_del_gasto` | Nombre ordenador del gasto | Texto | Describe el nombre del ordenador del gasto de la entidad compradora | 48.331 | 0 (0%) | 4.487 |
| 77 | `tipo_de_documento_ordenador_del_gasto` | Tipo de documento Ordenador del gasto | Texto | Indica el tipo de documento del ordenador del gasto de la entidad compradora | 48.331 | 0 (0%) | 8 |
| 78 | `n_mero_de_documento_ordenador_del_gasto` | Número de documento Ordenador del gasto | Texto | Indica el número de documento del ordenador del gasto | 48.331 | 0 (0%) | 4.422 |
| 79 | `nombre_supervisor` | Nombre supervisor | Texto | Describe el nombre del supervisor de la entidad compradora | 48.331 | 0 (0%) | 6.084 |
| 80 | `tipo_de_documento_supervisor` | Tipo de documento supervisor | Texto | Indica el tipo de documento del supervisor de la entidad compradora | 48.331 | 0 (0%) | 7 |
| 81 | `n_mero_de_documento_supervisor` | Número de documento supervisor | Texto | Indica el número de documento del supervisor | 48.331 | 0 (0%) | 5.911 |
| 82 | `nombre_ordenador_de_pago` | Nombre Ordenador de Pago | Texto | Describe el nombre del Ordenador de Pago de la entidad compradora | 48.331 | 0 (0%) | 908 |
| 83 | `tipo_de_documento_ordenador_de_pago` | Tipo de documento Ordenador de Pago | Texto | Indica el tipo de documento del Ordenador de Pago de la entidad compradora | 48.331 | 0 (0%) | 7 |
| 84 | `n_mero_de_documento_ordenador_de_pago` | Número de documento Ordenador de Pago | Texto | Indica el número de documento del Ordenador de Pago | 48.331 | 0 (0%) | 907 |
| 85 | `documentos_tipo` | Documentos Tipo | Texto | Indica si se utilizaron documentos tipo en el contrato | 48.331 | 0 (0%) | 2 |
| 86 | `descripcion_documentos_tipo` | Descripcion Documentos Tipo | Texto | Descripción de los documentos tipo utilizados | 48.331 | 0 (0%) | 9 |
| 87 | `fecha_de_notificaci_n_de_prorrogaci_n` | Fecha de notificación de prorrogación | Marca de tiempo variable | Infica la fecha de notificación de la prorrogación del contrato | 5.926 | 42.405 (87.7%) | 2.029 |
| 88 | `n_adicion_valor` | n_adicion_valor | int64 | Cantidad de adiciones en valor monetario registradas para el contrato | 48.331 | 0 (0%) | 8 |
| 89 | `n_cesion` | n_cesion | int64 | Cantidad de cesiones (transferencia del contrato a otro contratista) | 48.331 | 0 (0%) | 6 |
| 90 | `n_conclusion` | n_conclusion | int64 | Cantidad de registros de conclusión/terminación anticipada | 48.331 | 0 (0%) | 8 |
| 91 | `n_extension` | n_extension | int64 | Cantidad de extensiones en plazo (prórrogas) | 48.331 | 0 (0%) | 2 |
| 92 | `n_modif_general` | n_modif_general | int64 | Cantidad de modificaciones generales al contrato | 48.331 | 0 (0%) | 37 |
| 93 | `n_tipo_no_definido` | n_tipo_no_definido | int64 | Cantidad de modificaciones sin tipo definido | 48.331 | 0 (0%) | 11 |
| 94 | `n_reactivacion` | n_reactivacion | int64 | Cantidad de reactivaciones del contrato | 48.331 | 0 (0%) | 32 |
| 95 | `n_suspension` | n_suspension | int64 | Cantidad de suspensiones del contrato | 48.331 | 0 (0%) | 31 |
| 96 | `n_modificaciones_total` | n_modificaciones_total | int64 | Total de modificaciones contractuales (suma de todos los tipos) | 48.331 | 0 (0%) | 76 |
| 97 | `n_tipos_distintos` | n_tipos_distintos | int64 | Cantidad de tipos distintos de modificación aplicados al contrato | 48.331 | 0 (0%) | 8 |
| 98 | `fecha_primera_adicion` | fecha_primera_adicion | datetime64[us] | Fecha de la primera modificación registrada | 33.465 | 14.866 (30.8%) | 557 |
| 99 | `fecha_ultima_adicion` | fecha_ultima_adicion | datetime64[us] | Fecha de la última modificación registrada | 33.465 | 14.866 (30.8%) | 587 |
| 100 | `tiene_extension_dias` | tiene_extension_dias | int64 | Indicador binario: el contrato tuvo al menos una extensión de plazo | 48.331 | 0 (0%) | 2 |
| 101 | `tiene_adicion_valor` | tiene_adicion_valor | int64 | Indicador binario: el contrato tuvo al menos una adición en valor | 48.331 | 0 (0%) | 2 |
| 102 | `tiene_suspension` | tiene_suspension | int64 | Indicador binario: el contrato tuvo al menos una suspensión | 48.331 | 0 (0%) | 2 |
| 103 | `tiene_cesion` | tiene_cesion | int64 | Indicador binario: el contrato tuvo al menos una cesión | 48.331 | 0 (0%) | 2 |
| 104 | `tiene_conclusion` | tiene_conclusion | int64 | Indicador binario: el contrato tuvo al menos una conclusión anticipada | 48.331 | 0 (0%) | 2 |
| 105 | `tiene_modificacion` | tiene_modificacion | int64 | (sin definición oficial — columna derivada o calculada) | 48.331 | 0 (0%) | 2 |
| 106 | `sobrecosto_ratio` | sobrecosto_ratio | float64 | (sin definición oficial — columna derivada o calculada) | 15.033 | 33.298 (68.9%) | 7.193 |
| 107 | `duracion_planificada_dias` | duracion_planificada_dias | float64 | (sin definición oficial — columna derivada o calculada) | 42.252 | 6.079 (12.6%) | 1.476 |
| 108 | `ratio_extension_duracion` | ratio_extension_duracion | float64 | (sin definición oficial — columna derivada o calculada) | 42.055 | 6.276 (13.0%) | 6.138 |
| 109 | `dias_hasta_primera_adicion` | dias_hasta_primera_adicion | float64 | Días transcurridos entre la firma del contrato y la primera modificación | 33.465 | 14.866 (30.8%) | 1.540 |
| 110 | `ventana_adiciones_dias` | ventana_adiciones_dias | float64 | (sin definición oficial — columna derivada o calculada) | 33.465 | 14.866 (30.8%) | 1.087 |
| 111 | `log_valor_contrato` | log_valor_contrato | float64 | (sin definición oficial — columna derivada o calculada) | 48.331 | 0 (0%) | 39.773 |

### Distribucion de valores (categoricas con <= 30 valores unicos)

**`orden`** (3 valores unicos)

| Valor | Cantidad |
|---|---|
| Territorial | 32.016 |
| Nacional | 15.667 |
| Corporación Autónoma | 648 |

**`sector`** (25 valores unicos)

| Valor | Cantidad |
|---|---|
| Servicio Público | 15.333 |
| No aplica/No pertenece | 9.056 |
| Transporte | 8.071 |
| defensa | 3.178 |
| Educación Nacional | 2.179 |
| Ambiente y Desarrollo Sostenible | 1.540 |
| Salud y Protección Social | 1.380 |
| Ley de Justicia | 1.187 |
| Trabajo | 1.067 |
| Vivienda, Ciudad y Territorio | 990 |

**`rama`** (4 valores unicos)

| Valor | Cantidad |
|---|---|
| Ejecutivo | 38.882 |
| Corporación Autónoma | 8.381 |
| Judicial | 1.024 |
| Legislativo | 44 |

**`entidad_centralizada`** (2 valores unicos)

| Valor | Cantidad |
|---|---|
| Centralizada | 40.360 |
| Descentralizada | 7.971 |

**`estado_contrato`** (11 valores unicos)

| Valor | Cantidad |
|---|---|
| Modificado | 15.248 |
| terminado | 11.259 |
| En ejecución | 9.805 |
| Cerrado | 3.072 |
| Aprobado | 2.565 |
| Borrador | 2.410 |
| Cancelado | 1.681 |
| Suspendido | 1.181 |
| enviado Proveedor | 650 |
| En aprobación | 421 |

**`tipo_de_contrato`** (1 valores unicos)

| Valor | Cantidad |
|---|---|
| Obra | 48.331 |

**`modalidad_de_contratacion`** (9 valores unicos)

| Valor | Cantidad |
|---|---|
| Selección Abreviada de Menor Cuantía | 12.932 |
| Contratación directa | 9.981 |
| Mínima cuantía | 9.747 |
| Licitación pública Obra Publica | 8.575 |
| Contratación régimen especial | 2.905 |
| Contratación régimen especial (con ofertas) | 1.932 |
| Contratación Directa (con ofertas) | 1.541 |
| Licitación pública | 421 |
| Seleccion Abreviada Menor Cuantia Sin Manifestacion Interes | 297 |

**`justificacion_modalidad_de`** (21 valores unicos)

| Valor | Cantidad |
|---|---|
| Presupuesto menor al 10% de la Menor Cuantía | 12.524 |
| Presupuesto inferior al 10% de la menor cuantía | 9.747 |
| Article30_1993 | 8.575 |
| Contratos o convenios Interadministrativos (valor cero) | 5.417 |
| Regla aplicable | 4.837 |
| Convenios Solidarios Regimen articulo 92 Ley 2166 de 2021 | 2.177 |
| Law2166of2021_Article95_SolidarityAgreements | 1.451 |
| Contratos o convenios Interadministrativos (con valor) | 1.370 |
| Urgencia manifiesta | 904 |
| Ley 1150 de 2007 | 421 |

**`condiciones_de_entrega`** (14 valores unicos)

| Valor | Cantidad |
|---|---|
| No Definido | 19.553 |
| A convenir | 14.258 |
| Como acordado previamente | 13.344 |
| Transporte incluido | 972 |
| DAP - Entregado en un punto (lugar de destino convenido) | 129 |
| Transporte no incluído | 34 |
| CPT - Transporte pagado hasta (lugar de destino convenido) | 13 |
| Transporte a cargo del comprador | 12 |
| DDP - Delivery duty place | 9 |
| CFR - Cost and freight | 2 |

**`tipodocproveedor`** (7 valores unicos)

| Valor | Cantidad |
|---|---|
| NIT | 36.965 |
| Cédula de Ciudadanía | 6.802 |
| No Definido | 3.469 |
| Otro | 1.080 |
| Cédula de Extranjería | 13 |
| Tarjeta de Identidad | 1 |
| Permiso especial de permanencia | 1 |

---

## 7. Proveedores RUP (enriquecido)

**Archivo**: `data/proveedores_rup.parquet`

**Descripcion**: Dataset unificado de NITs de proveedores/proponentes de Obra, enriquecido con información financiera extraída del Registro Único de Proponentes (RUP) mediante web scraping.

| Atributo | Valor |
|---|---|
| Granularidad | 1 fila = 1 NIT de proveedor/proponente |
| Registros | 28.548 |
| Columnas | 22 |
| Notebook/Script | `06_proponentes_por_proceso.ipynb + scripts/extraer_rup_auto.py` |

### Definicion de columnas

| # | Columna API | Nombre original | Tipo | Descripcion | No nulos | Nulos (%) | Unicos |
|---|---|---|---|---|---|---|---|
| 1 | `nit` | nit | Texto | NIT del proveedor/proponente (llave única, sin dígito verificador) | 28.548 | 0 (0%) | 28.548 |
| 2 | `nombre_proveedor` | nombre_proveedor | Texto | Nombre o razón social del proveedor | 28.548 | 0 (0%) | 28.113 |
| 3 | `origen` | origen | Texto | Fuente de donde se obtuvo el NIT: 'procesos', 'electronicos' o 'ambos' | 28.548 | 0 (0%) | 3 |
| 4 | `rup_estado` | rup_estado | Texto | Estado de la matrícula RUP (ACTIVA, CANCELADA, etc.) | 13.530 | 15.018 (52.6%) | 6 |
| 5 | `rup_tamano` | rup_tamano | Texto | Tamaño de empresa según clasificación RUP (01=Micro, 02=Pequeña, 03=Mediana, 04=Grande) | 13.530 | 15.018 (52.6%) | 6 |
| 6 | `rup_empleados` | rup_empleados | Número | Número de empleados declarados ante la Cámara de Comercio | 13.530 | 15.018 (52.6%) | 331 |
| 7 | `rup_municipio` | rup_municipio | Texto | Municipio del domicilio comercial del proveedor | 13.530 | 15.018 (52.6%) | 682 |
| 8 | `rup_sanciones` | rup_sanciones | Número | Cantidad de sanciones registradas en el RUP | 13.530 | 15.018 (52.6%) | 6 |
| 9 | `rup_multas` | rup_multas | Número | Cantidad de multas registradas en el RUP | 13.530 | 15.018 (52.6%) | 4 |
| 10 | `rup_inhabilidad` | rup_inhabilidad | Texto | Inhabilidad vigente registrada en el RUP (si aplica) | 13.530 | 15.018 (52.6%) | 3 |
| 11 | `rup_ano_financiero` | rup_ano_financiero | Texto | Año fiscal de la información financiera reportada | 13.174 | 15.374 (53.9%) | 45 |
| 12 | `rup_activo_total` | rup_activo_total | Número | Activo total en COP según estados financieros | 13.173 | 15.375 (53.9%) | 11.216 |
| 13 | `rup_patrimonio` | rup_patrimonio | Número | Patrimonio neto en COP según estados financieros | 13.171 | 15.377 (53.9%) | 11.140 |
| 14 | `rup_ingresos` | rup_ingresos | Número | Ingresos por actividad ordinaria en COP | 13.132 | 15.416 (54.0%) | 10.542 |
| 15 | `rup_utilidad_neta` | rup_utilidad_neta | Número | Resultado del período (utilidad o pérdida) en COP | 13.166 | 15.382 (53.9%) | 9.853 |
| 16 | `rup_idx_liquidez` | rup_idx_liquidez | Número | Índice de liquidez: Activo Corriente / Pasivo Corriente | 10.292 | 18.256 (63.9%) | 9.813 |
| 17 | `rup_idx_endeudamiento` | rup_idx_endeudamiento | Número | Índice de endeudamiento: Pasivo Total / Activo Total | 10.407 | 18.141 (63.5%) | 5.312 |
| 18 | `rup_idx_cobertura` | rup_idx_cobertura | Número | Cobertura de intereses: Utilidad Operacional / Gastos Intereses | 0 | 28.548 (100.0%) | 0 |
| 19 | `rup_rent_patrimonio` | rup_rent_patrimonio | Número | Rentabilidad sobre patrimonio: Utilidad Neta / Patrimonio | 9.970 | 18.578 (65.1%) | 4.838 |
| 20 | `rup_rent_activo` | rup_rent_activo | Número | Rentabilidad sobre activos: Utilidad Neta / Activo Total | 10.001 | 18.547 (65.0%) | 4.118 |
| 21 | `procesado` | procesado | Booleano | Indica si el NIT ya fue consultado en la API del RUP | 28.548 | 0 (0%) | 2 |
| 22 | `procesar` | procesar | Booleano | Indica si el NIT debe procesarse (False para consorcios/UT) | 28.548 | 0 (0%) | 2 |

### Distribucion de valores (categoricas con <= 30 valores unicos)

**`origen`** (3 valores unicos)

| Valor | Cantidad |
|---|---|
| ambos | 12.760 |
| procesos | 10.020 |
| electronicos | 5.768 |

**`rup_estado`** (6 valores unicos)

| Valor | Cantidad |
|---|---|
| ACTIVA | 11.802 |
| CANCELADA | 1.452 |
| MATRÍCULA NUEVA, CONSTITUCIÓN POR TRASLADO | 166 |
|  | 92 |
| MATRÍCULA CANCELADA POR TRASLADO DE DOMICILIO | 10 |
| MATRÍCULA CANCELADA LEY 1429 | 8 |

**`rup_tamano`** (6 valores unicos)

| Valor | Cantidad |
|---|---|
| 01 | 8.195 |
| 02 | 2.949 |
| 03 | 1.196 |
| 00 | 555 |
| 04 | 488 |
|  | 147 |

**`rup_sanciones`** (6 valores unicos)

| Valor | Cantidad |
|---|---|
| 0.0 | 13.346 |
| 1.0 | 147 |
| 2.0 | 26 |
| 3.0 | 7 |
| 4.0 | 3 |
| 6.0 | 1 |

**`rup_multas`** (4 valores unicos)

| Valor | Cantidad |
|---|---|
| 0.0 | 13.434 |
| 1.0 | 78 |
| 2.0 | 15 |
| 3.0 | 3 |

**`rup_inhabilidad`** (3 valores unicos)

| Valor | Cantidad |
|---|---|
| false | 11.151 |
|  | 2.371 |
| true | 8 |

**`procesado`** (2 valores unicos)

| Valor | Cantidad |
|---|---|
| True | 21.164 |
| False | 7.384 |

**`procesar`** (2 valores unicos)

| Valor | Cantidad |
|---|---|
| True | 21.164 |
| False | 7.384 |

---

## Esquema relacional entre datasets

```
contratos_electronicos_obra (FUENTE MADRE)
  |
  |-- proceso_de_compra = id_del_portafolio --> procesos_contratacion_obra
  |                                               |
  |                                               |-- id_del_proceso = id_procedimiento --> proponentes_por_proceso_obra
  |
  |-- id_contrato = id_contrato --> adiciones_obra
  |
  |-- codigo_proveedor = codigo --> proveedores_obra
  |
  |-- codigo_proveedor = nit --> proveedores_rup
  |
  +-- [JOIN con adiciones] --> contratos_adiciones_obra
```

### Llaves de integracion

| Origen | Llave origen | Destino | Llave destino | Cobertura |
|---|---|---|---|---|
| contratos_electronicos | `proceso_de_compra` | procesos_contratacion | `id_del_portafolio` | 99.9% |
| contratos_electronicos | `id_contrato` | adiciones | `id_contrato` | 69.2% |
| contratos_electronicos | `codigo_proveedor` | proveedores_registrados | `codigo` | 54.4% |
| contratos_electronicos | `codigo_proveedor` | proveedores_rup | `nit` | 63.5% (de procesados) |
| procesos_contratacion | `id_del_proceso` | proponentes_por_proceso | `id_procedimiento` | 29.4% |

---

## Notas metodologicas

1. **Filtro global**: Todos los datasets estan filtrados por `tipo_de_contrato = 'Obra'`
2. **Fuente oficial**: Las descripciones de columnas provienen del diccionario oficial del SECOP publicado en datos.gov.co
3. **Columnas derivadas**: Las columnas marcadas como '(sin definicion oficial)' fueron calculadas durante la fase de comprension/integracion de datos
4. **Valores sentinela**: El SECOP usa cadenas como 'No Definido', 'No Provisto', '' en lugar de nulos reales. Estos deben tratarse como datos faltantes
5. **Dataset integrado** (`contratos_adiciones_obra`): Resultado del LEFT JOIN entre contratos y adiciones agregadas. Las 24 columnas adicionales son features derivadas del conteo y tipificacion de modificaciones contractuales
6. **Proveedores RUP**: Dataset enriquecido mediante web scraping de la API del RUP. Las columnas `rup_*` provienen de la consulta automatizada al Registro Unico de Proponentes
