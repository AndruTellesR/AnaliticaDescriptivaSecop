# MATRIZ DE OBJETIVOS VS CODIGO IMPLEMENTADO

## 0. Metadatos

- **Fecha de generacion:** 2026-07-23
- **Archivos fuente cruzados:**
  - `InformesRev/RESUMEN_CONTROL.md`
  - `InformesRev/RESUMEN_CODIGO.md`
  - `InformesRev/AnteproyectoAndres.md`
- **Autor del anteproyecto:** Andres Telles (Camilo Andres Telles Ramirez)
- **Proyecto paralelo detectado en el mismo repositorio:** SI (modelado predictivo del companero, metodologia CRISP-DM, RF/XGBoost/LightGBM + chatbot RAG)
- **Nivel de alineacion global entre anteproyecto y codigo:** **BAJO**. Ningun objetivo especifico presenta evidencia de cumplimiento total en `RESUMEN_CODIGO.md` (3 en estado Parcial, 1 en estado No cumple). El pipeline tecnico existente fue disenado explicitamente para un objetivo predictivo distinto (`doc/contexto/CONTEXTO.md`, linea 10), y los indicadores centrales del marco teorico (restriccion de hierro) existen unicamente como flags binarios de clasificacion, incompatibles con los indicadores continuos/categoricos exigidos.

---

## 1. Resumen ejecutivo del cruce

El cruce entre `InformesRev/AnteproyectoAndres.md` y la evidencia tecnica real documentada en `InformesRev/RESUMEN_CODIGO.md` muestra una alineacion baja. De los 4 objetivos especificos, ninguno esta en estado Cumple: OE-01 (extraccion SECOP) y OE-03 (normalizacion) estan Parciales, con evidencia tecnica real pero construida para un proposito distinto al declarado; OE-02 (modelo estrella) esta Parcial solo en el sentido de integracion por joins de pandas, sin esquema dimensional formal materializado; OE-04 (dashboard Dash/Plotly) esta en estado No cumple, sin ningun artefacto funcional en el stack exigido.

La brecha principal es doble: (1) el pipeline de datos existente (notebooks 00-08, `scripts/`) fue disenado explicitamente, segun `doc/contexto/CONTEXTO.md` (linea 10), para un trabajo de grado predictivo bajo CRISP-DM, no para el enfoque descriptivo-analitico de Andres basado en la restriccion de hierro; y (2) los indicadores de tiempo, costo y alcance que exige el anteproyecto (magnitudes continuas/categoricas) son incompatibles con los unicos indicadores existentes en el codigo (flags binarios en `notebooks/07_depuracion_variables_modelo.ipynb`, cuyo propio titulo dice "para Modelo Predictivo").

El riesgo mayor de autoria es que la mayor parte del peso del repositorio (`modelo_predictivo_global/`, `modelo-predictivo-preliminar/`, `entregables/05` a `11`, `extractor-indicadores-docker/`, `report/`) corresponde de forma verificable al companero y no debe presentarse como evidencia propia.

**Recomendacion global:** reformular parcialmente el anteproyecto en OE-02 y OE-04 (modelo dimensional simplificado y Streamlit+Plotly en lugar de Dash puro), manteniendo OE-01 y OE-03 con trabajo adicional puntual, y documentar formalmente el deslinde de autoria del pipeline compartido con el director.

---

## 2. Tabla maestra de cruce

| OE | Objetivo (resumido) | Requisito derivado | Evidencia esperada | Evidencia real encontrada | Archivos que respaldan | Archivos EXCLUIDOS (companero) | Estado | Brecha detectada | Decision recomendada | Tiempo estimado | Riesgo |
|---|---|---|---|---|---|---|---|---|---|---|---|
| OE-01 | Extraccion automatizada SECOP | Script/notebook con conexion API Socrata, filtro de fecha, logs y trazabilidad | Extraccion via `sodapy`, filtrada por `tipo_de_contrato="Obra"`, con paginacion por lotes | `notebooks/00_definicion_tabla_base.ipynb` a `06_proponentes_por_proceso.ipynb`; `dataset.json` (RESUMEN_CODIGO.md, seccion 5 y 8) | `notebooks/00-06`, `dataset.json`, `definciones/*.xlsx` (AUTORIA A CONFIRMAR CON DIRECTOR) | `scripts/extraer_rup_auto.py`, `scripts/extraer_indicadores_pliegos.py`, `scripts/gemini/` | Parcial | Sin filtro 2018-2024 verificable, sin logs persistentes, sin script `.py` reutilizable fuera de Jupyter | Mantener (construir lo faltante) | 1-1.5 semanas | Medio |
| OE-02 | Modelo de datos analitico (estructuracion procesos+contratos+proveedores) | Modelo estrella formal: tabla de hechos + dimensiones, reglas de integracion documentadas | Joins por `id_del_portafolio`, `codigo_proveedor`, `id_contrato`, con coberturas medidas | `notebooks/05_integracion_contratos_adiciones.ipynb`; `entregables/04-datasets/contratos_adiciones_obra.parquet` (RESUMEN_CODIGO.md, seccion 5 y 7) | `notebooks/05` (AUTORIA A CONFIRMAR CON DIRECTOR); `entregables/04-datasets/` (crudos, a confirmar) | `notebooks/08_integracion_rup_no_consorcios.ipynb`, `consolidado_global.parquet`, `consolidado_imputado.parquet` | Parcial | Sin modelo estrella materializado, sin motor de BD, sin DDL, sin diagrama | Reformular (modelo dimensional simplificado) | 1 semana | Medio |
| OE-03 | Normalizacion (duplicados, nulos, inconsistencias, tipificacion) | Pipeline de limpieza documentado + diccionario de datos + umbrales de calidad | Deteccion de duplicados/sentinelas + diccionario de datos generado automaticamente | `notebooks/01,02`; `scripts/generar_diccionario_datos.py`, `generar_diccionario_md.py`; `data/diccionario_datos.json` (RESUMEN_CODIGO.md, seccion 5, 6 y 9) | `notebooks/01,02` (AUTORIA A CONFIRMAR); `scripts/generar_diccionario_datos.py`, `generar_diccionario_md.py` (AUTORIA A CONFIRMAR) | `notebooks/07_depuracion_variables_modelo.ipynb` (targets ML) | Parcial | Sin umbrales cuantitativos de calidad, sin tratamiento final de deduplicacion documentado | Mantener (anadir umbrales y tratamiento final) | 1 semana | Bajo-Medio |
| OE-04 | Visualizaciones y tableros interactivos (distribuciones, box plots, segmentaciones) | Dashboard Dash/Plotly (o equivalente) funcional con filtros, box plots y segmentaciones por modalidad/entidad/territorio | Box plots exploratorios en notebooks EDA; `visualizer/` (Next.js) no funcional | Box plots en `notebooks/01,02,05` (EDA); `visualizer/src/hooks/useDuckDB.ts` roto por datos faltantes (RESUMEN_CODIGO.md, seccion 5, 11 y 15) | Ninguno funcional propio de Andres | `modelo_predictivo_global/chatbot/app.py` (Streamlit del companero, Fase IV predictiva); `visualizer/` (autoria a confirmar, stack no coincide) | No cumple | Ningun artefacto Dash/Plotly funcional; stack exigido no implementado | Reformular (Streamlit + Plotly) | 2 semanas | Alto |

---

## 3. Analisis detallado por objetivo

### OE-01: Extraccion automatizada de datos de SECOP

#### 3.1.1 Texto original del objetivo (desde anteproyecto)

"Implementar un mecanismo de extraccion automatizada de los datos de SECOP (datos.gov.co), garantizando trazabilidad, actualizacion y reproducibilidad del conjunto de datos de estudio."

#### 3.1.2 Requisito derivado

Debe existir codigo que se conecte a la API Socrata/OData de datos.gov.co, aplique el filtro `tipo_de_contrato = "Obra"` y el recorte temporal 2018-2024, registre logs de ejecucion (timestamps, numero de registros, parametros de consulta) y sea ejecutable de forma reproducible fuera de la dependencia manual de Jupyter.

#### 3.1.3 Evidencia real encontrada

`RESUMEN_CODIGO.md` (secciones 5, 6 y 8) confirma conexion real a la API Socrata via `sodapy` en `notebooks/00_definicion_tabla_base.ipynb` a `06_proponentes_por_proceso.ipynb`, con descarga filtrada por `tipo_de_contrato="Obra"` y paginacion por lotes de IDs en los notebooks 03 y 06. No se encontro filtro de fecha 2018-2024 verificable en el codigo estatico, no hay logs persistentes fuera de las celdas markdown, y no existe un script `.py` reutilizable equivalente (toda la logica vive dentro de los notebooks).

#### 3.1.4 Archivos que respaldan (aporte propio o compartido)

| Archivo | Tipo |
|---|---|
| `notebooks/00_definicion_tabla_base.ipynb` | AUTORIA A CONFIRMAR CON DIRECTOR |
| `notebooks/01_contratos_electronicos.ipynb` | AUTORIA A CONFIRMAR CON DIRECTOR |
| `notebooks/02_procesos_contratacion.ipynb` | AUTORIA A CONFIRMAR CON DIRECTOR |
| `notebooks/03_adiciones.ipynb` | AUTORIA A CONFIRMAR CON DIRECTOR |
| `notebooks/04_proveedores.ipynb` | AUTORIA A CONFIRMAR CON DIRECTOR |
| `notebooks/06_proponentes_por_proceso.ipynb` | AUTORIA A CONFIRMAR CON DIRECTOR |
| `dataset.json` | AUTORIA A CONFIRMAR CON DIRECTOR |

#### 3.1.5 Archivos EXCLUIDOS del entregable

`scripts/extraer_rup_auto.py`, `scripts/extraer_indicadores_pliegos.py`, `scripts/poblar_indicadores_pliegos.py`, `scripts/scraper_pliegos_poc.py`, `scripts/validar_extraccion_pliegos.py`, `scripts/gemini/*` (extraccion de indicadores RUP/pliegos, exclusiva del modelo predictivo).

#### 3.1.6 Brecha tecnica

Falta: (a) filtro temporal 2018-2024 explicito y verificable en la consulta SoQL; (b) logging persistente (archivo, no solo celdas markdown) con timestamps, parametros de consulta y conteo de registros; (c) un script `.py` parametrizable y reutilizable fuera de Jupyter para regenerar la extraccion.

#### 3.1.7 Tres caminos de decision

**Camino A - MANTENER objetivo original:**
- Que se debe construir: script `extraer_secop.py` que encapsule la conexion Socrata ya usada en los notebooks, anadiendo filtro de fecha, logging a archivo y manejo de reintentos.
- Tiempo estimado: 1-1.5 semanas.
- Riesgo tecnico: Bajo (la logica de conexion ya existe y funciona; es refactorizacion, no desarrollo desde cero).
- Riesgo academico: Medio (depende de que el director confirme que el pipeline base puede usarse como insumo/aporte compartido).
- Ventajas: no requiere cambiar el objetivo; aprovecha codigo ya probado; bajo esfuerzo tecnico.
- Desventajas: depende de resolver primero la ambiguedad de autoria del pipeline base.

**Camino B - REFORMULAR objetivo:**
- Nueva redaccion propuesta: "Implementar un mecanismo de extraccion automatizada de los datos de SECOP (datos.gov.co) para el periodo 2018-2024, a partir de un pipeline de extraccion documentado, garantizando trazabilidad mediante registros de ejecucion y reproducibilidad del conjunto de datos de estudio."
- Que se conserva: el uso de la API Socrata y el filtro `tipo_de_contrato="Obra"`.
- Que se ajusta: se explicita el periodo temporal y el mecanismo de trazabilidad como parte del texto del objetivo, para que la evidencia de cumplimiento sea mas facil de verificar.
- Tiempo estimado: 1 semana (ajuste de redaccion + implementacion minima del filtro y logging).
- Riesgo academico: Bajo (ajuste menor, no cambia el fondo del objetivo).
- Ventajas: mayor precision y verificabilidad del objetivo.
- Desventajas: requiere aprobacion formal de cambio de texto por el comite/director.

**Camino C - EXCLUIR o CONVERTIR EN LIMITACION:**
- Justificacion tecnica: no aplica como primera opcion; la extraccion via API ya existe y es de bajo costo completar.
- Impacto sobre el objetivo general: alto si se excluye, porque OE-01 es la base de todo el pipeline.
- Como redactarlo en limitaciones: no recomendado.
- Riesgo ante jurado: alto si se excluye sin justificacion tecnica solida.
- Nota: **no recomendado**; solo se documenta por completitud metodologica de la matriz.

#### 3.1.8 Recomendacion final para este OE

**Mantener (Camino A)**, dado que la infraestructura de extraccion ya funciona tecnicamente y las brechas (filtro de fecha, logs, script reutilizable) son de bajo costo de implementacion relativo. La condicion critica es resolver primero la autoria del pipeline base con el director, ya que sin esa confirmacion cualquier evidencia presentada queda expuesta al riesgo de atribucion incorrecta.

---

### OE-02: Modelo de datos analitico (estructuracion)

#### 3.2.1 Texto original del objetivo (desde anteproyecto)

"Estructurar los conjuntos de datos de SECOP relacionados con obra publica (procesos, contratos y proveedores), definiendo el modelo de datos analitico y las reglas de integracion necesarias para su relacionamiento consistente."

#### 3.2.2 Requisito derivado

Debe existir un modelo de datos analitico formal (modelo estrella: tabla de hechos + dimensiones) materializado en algun motor de almacenamiento, con reglas de integracion documentadas (llaves, cardinalidad, cobertura de los joins).

#### 3.2.3 Evidencia real encontrada

`RESUMEN_CODIGO.md` (secciones 5, 6 y 7) confirma integracion real via joins de pandas en `notebooks/05_integracion_contratos_adiciones.ipynb` (contratos + adiciones, LEFT JOIN por `id_contrato`) y `notebooks/08_integracion_rup_no_consorcios.ipynb` (enriquecimiento RUP), con coberturas medidas (99.9% contrato-proceso, 54.4% contrato-proveedor, 69.2% adicion-contrato, documentadas en `doc/contexto/CONTEXTO.md`). El resultado se persiste en `entregables/04-datasets/contratos_adiciones_obra.parquet` (48,331 x 125). **No existe ningun esquema de modelo estrella formal**: no hay DDL, no hay motor de base de datos (SQLite/DuckDB/PostgreSQL) materializando hechos y dimensiones, no hay diagrama de modelo dimensional.

#### 3.2.4 Archivos que respaldan (aporte propio o compartido)

| Archivo | Tipo |
|---|---|
| `notebooks/05_integracion_contratos_adiciones.ipynb` | AUTORIA A CONFIRMAR CON DIRECTOR |
| `entregables/04-datasets/contratos_electronicos_obra.parquet` | AUTORIA A CONFIRMAR CON DIRECTOR (dataset crudo) |
| `entregables/04-datasets/procesos_contratacion_obra.parquet` | AUTORIA A CONFIRMAR CON DIRECTOR (dataset crudo) |
| `entregables/04-datasets/adiciones_obra.parquet` | AUTORIA A CONFIRMAR CON DIRECTOR (dataset crudo) |
| `entregables/04-datasets/proveedores_obra.parquet` | AUTORIA A CONFIRMAR CON DIRECTOR (dataset crudo) |
| `entregables/04-datasets/contratos_adiciones_obra.parquet` | AUTORIA A CONFIRMAR CON DIRECTOR (integrado v1) |

#### 3.2.5 Archivos EXCLUIDOS del entregable

`notebooks/08_integracion_rup_no_consorcios.ipynb` (enriquecimiento RUP exclusivo del modelado predictivo), `entregables/04-datasets/consolidado_global.parquet`, `entregables/04-datasets/consolidado_imputado.parquet` (version enriquecida y codificada para ML, fase del companero).

#### 3.2.6 Brecha tecnica

Falta por completo: (a) definicion explicita de tabla de hechos (contratos) y dimensiones (proceso, proveedor, entidad, modalidad); (b) materializacion en un motor real (DuckDB, SQLite u otro); (c) diagrama del modelo dimensional; (d) documentacion formal de reglas de integracion mas alla de lo narrado en `doc/contexto/CONTEXTO.md` (que ademas es documentacion del proyecto del companero).

#### 3.2.7 Tres caminos de decision

**Camino A - MANTENER objetivo original (modelo estrella formal en RDBMS):**
- Que se debe construir: esquema DDL completo con tabla de hechos y dimensiones, materializado en PostgreSQL o motor equivalente, con proceso ETL de carga.
- Tiempo estimado: 2-3 semanas.
- Riesgo tecnico: Medio-Alto (requiere disenar el esquema desde cero y migrar los joins de pandas existentes a un motor relacional).
- Riesgo academico: Bajo (cumple literalmente lo prometido).
- Ventajas: cumplimiento estricto del texto original; artefacto tecnicamente mas robusto.
- Desventajas: alto costo de tiempo frente al resto de objetivos pendientes; riesgo de retrasar toda la entrega.

**Camino B - REFORMULAR objetivo (modelo dimensional simplificado):**
- Nueva redaccion propuesta: "Estructurar los conjuntos de datos de SECOP relacionados con obra publica (procesos, contratos y proveedores) mediante un modelo dimensional simplificado (tabla de hechos y dimensiones representadas en archivos Parquet con convenciones documentadas y diagrama de esquema), definiendo las reglas de integracion necesarias para su relacionamiento consistente."
- Que se conserva: la logica de integracion ya construida (joins por `id_del_portafolio`, `codigo_proveedor`, `id_contrato`) y las coberturas ya medidas.
- Que se ajusta: se reemplaza la exigencia de un RDBMS formal por un modelo dimensional documentado sobre Parquet, con un diagrama explicito de hechos/dimensiones y un diccionario de convenciones (nombre de tabla de hechos, llaves foraneas, granularidad).
- Tiempo estimado: 1 semana (documentacion + diagrama + reestructuracion ligera de los parquets existentes en carpetas `hechos/` y `dimensiones/`).
- Riesgo academico: Medio (requiere aprobacion explicita del comite de que un modelo dimensional sobre archivos planos satisface el objetivo).
- Ventajas: reutiliza directamente el trabajo de integracion ya existente; tiempo de ejecucion realista.
- Desventajas: un jurado estricto podria considerar que no es un "modelo de datos analitico" en sentido pleno si no se materializa en un motor de consulta real.

**Camino C - EXCLUIR o CONVERTIR EN LIMITACION:**
- Justificacion tecnica: no aplica como primera opcion, dado que ya existe una base de integracion funcional reutilizable.
- Impacto sobre el objetivo general: alto si se excluye, porque el objetivo general depende de tener un dataset estructurado para calcular los indicadores.
- Como redactarlo en limitaciones: no recomendado.
- Riesgo ante jurado: alto si se excluye.
- Nota: **no recomendado**.

#### 3.2.8 Recomendacion final para este OE

**Reformular (Camino B)**, adoptando un modelo dimensional simplificado sobre Parquet con diagrama y diccionario de convenciones documentado. Un modelo estrella completo en RDBMS (Camino A) es tecnicamente superior pero desproporcionado en tiempo frente a las demas brechas pendientes (especialmente OE-04); el modelo simplificado permite cumplir el espiritu del objetivo con esfuerzo realista, siempre que el director apruebe explicitamente el cambio de exigencia tecnologica.

---

### OE-03: Normalizacion de variables

#### 3.3.1 Texto original del objetivo (desde anteproyecto)

"Normalizar las variables del conjunto de datos analiticos, gestionando duplicados, valores faltantes, inconsistencias y tipificacion, para garantizar la calidad de la informacion y la confiabilidad de los resultados de la analitica."

#### 3.3.2 Requisito derivado

Debe existir un pipeline de limpieza documentado (deduplicacion con criterio explicito, tratamiento de nulos/sentinelas, tipificacion de columnas) junto con un diccionario de datos y umbrales cuantitativos de calidad verificables (por ejemplo, porcentaje maximo de nulidad o duplicados aceptado).

#### 3.3.3 Evidencia real encontrada

`RESUMEN_CODIGO.md` (secciones 5, 6 y 9) confirma deteccion de duplicados (3,022 en `id_contrato`, 25,221 en `id_del_proceso`, 105,836 en `identificador` de adiciones, 499 en proveedores, segun `doc/contexto/CONTEXTO.md`) y tratamiento de sentinelas `"No Definido"` como NULL (`notebooks/03_adiciones.ipynb`, celda 13). El diccionario de datos existe y se genera automaticamente (`scripts/generar_diccionario_datos.py`, `scripts/generar_diccionario_md.py`, `data/diccionario_datos.json`, `doc/fase2_comprension_datos/diccionario_datos.md`). **No se encontraron umbrales cuantitativos de calidad** (por ejemplo, "maximo 5% de nulidad aceptable") ni confirmacion en codigo de que la deduplicacion final se aplique con el criterio "conservar el registro mas completo o reciente" que exige el anteproyecto (numeral 3.6.5).

#### 3.3.4 Archivos que respaldan (aporte propio o compartido)

| Archivo | Tipo |
|---|---|
| `notebooks/01_contratos_electronicos.ipynb` (deteccion de calidad, celda 35) | AUTORIA A CONFIRMAR CON DIRECTOR |
| `notebooks/02_procesos_contratacion.ipynb` (tipificacion, seccion 5.1) | AUTORIA A CONFIRMAR CON DIRECTOR |
| `scripts/generar_diccionario_datos.py` | AUTORIA A CONFIRMAR CON DIRECTOR |
| `scripts/generar_diccionario_md.py` | AUTORIA A CONFIRMAR CON DIRECTOR |
| `data/diccionario_datos.json` | AUTORIA A CONFIRMAR CON DIRECTOR |
| `doc/fase2_comprension_datos/diccionario_datos.md` | AUTORIA A CONFIRMAR CON DIRECTOR |

#### 3.3.5 Archivos EXCLUIDOS del entregable

`notebooks/07_depuracion_variables_modelo.ipynb` (deduplicacion/tipificacion realizada con fines de modelado predictivo, titulo explicito "para Modelo Predictivo"); imputacion por mediana + flags `_was_nan` de `modelo_predictivo_global/notebooks/02_preprocesamiento.ipynb` y `modelo_predictivo_global/data/imputers/` (exclusivos del companero).

#### 3.3.6 Brecha tecnica

Falta: (a) definicion explicita de umbrales cuantitativos de calidad (nulidad maxima, cobertura minima de joins aceptable); (b) confirmacion/documentacion del criterio de deduplicacion final aplicado (mas completo/reciente); (c) un reporte de calidad de datos reproducible (no solo narrativo en celdas markdown).

#### 3.3.7 Tres caminos de decision

**Camino A - MANTENER objetivo original:**
- Que se debe construir: definir umbrales de calidad (por ejemplo, nulidad maxima 20%, cobertura minima de join 50%), aplicar y documentar el criterio de deduplicacion, generar un reporte de calidad reproducible (script o notebook propio).
- Tiempo estimado: 1 semana.
- Riesgo tecnico: Bajo (se apoya en analisis ya existente, solo falta formalizar criterios y automatizar el reporte).
- Riesgo academico: Bajo.
- Ventajas: cierra la brecha con esfuerzo minimo; el objetivo ya esta mayormente resuelto en el fondo.
- Desventajas: depende de la misma confirmacion de autoria del pipeline base que OE-01/OE-02.

**Camino B - REFORMULAR objetivo:**
- Nueva redaccion propuesta: no es necesaria una reformulacion sustancial; se sugiere unicamente precisar el texto anadiendo "conforme a umbrales de calidad definidos previamente (por ejemplo, nulidad y cobertura de integracion)".
- Que se conserva: todo el texto original.
- Que se ajusta: se anade la mencion explicita a umbrales cuantitativos para facilitar la verificacion.
- Tiempo estimado: menor a 1 semana (ajuste de redaccion) + la misma 1 semana de implementacion del Camino A.
- Riesgo academico: Bajo.
- Ventajas: mayor precision sin cambiar el fondo del objetivo.
- Desventajas: ninguna relevante.

**Camino C - EXCLUIR o CONVERTIR EN LIMITACION:**
- Justificacion tecnica: no aplica; el objetivo esta cerca de cumplirse y su exclusion no se justifica tecnicamente.
- Impacto sobre el objetivo general: alto si se excluye, porque la confiabilidad de los indicadores depende de esta etapa.
- Como redactarlo en limitaciones: no recomendado.
- Riesgo ante jurado: alto si se excluye.
- Nota: **no recomendado**.

#### 3.3.8 Recomendacion final para este OE

**Mantener (Camino A)**, con el ajuste menor de precisar el texto (equivalente al Camino B, no excluyente). Es el objetivo mas cercano a cumplirse de los cuatro; el esfuerzo requerido (definir umbrales y formalizar el reporte de calidad) es bajo comparado con OE-02 y OE-04.

---

### OE-04: Visualizaciones y tableros interactivos

#### 3.4.1 Texto original del objetivo (desde anteproyecto)

"Disenar visualizaciones y tableros interactivos que presenten resultados (distribuciones, outliers con box plots, segmentaciones por modalidad/entidad/territorio) para apoyar la interpretacion, la transparencia y la toma de decisiones."

#### 3.4.2 Requisito derivado

Debe existir un tablero interactivo funcional (segun el anteproyecto: Dash/Plotly en 3.7.4.b, o Streamlit/Plotly en 2.2.5) con distribuciones, box plots de outliers y segmentaciones por modalidad de contratacion, entidad y territorio, ejecutable localmente.

#### 3.4.3 Evidencia real encontrada

`RESUMEN_CODIGO.md` (secciones 2, 5, 11 y 15) confirma que **no existe Dash ni Plotly en ningun archivo `.py` del repositorio**. El unico artefacto de visualizacion de datos es `visualizer/` (Next.js/React/DuckDB-WASM/Recharts), que **no es funcional**: `visualizer/src/hooks/useDuckDB.ts` y `useDiccionario.ts` hacen `fetch` contra `visualizer/public/data/`, carpeta inexistente en el checkout actual. El chatbot en Streamlit (`modelo_predictivo_global/chatbot/app.py`) existe pero es la interfaz RAG del modelo predictivo del companero, no un tablero descriptivo. Box plots exploratorios si existen dentro de los notebooks EDA (`notebooks/01,02,05`), pero como parte del analisis de comprension de datos del pipeline compartido, no como tablero interactivo final.

#### 3.4.4 Archivos que respaldan (aporte propio o compartido)

Ninguno funcional propio de Andres. Los unicos artefactos relacionados son:

| Archivo | Tipo |
|---|---|
| `notebooks/01_contratos_electronicos.ipynb` (box plots EDA) | AUTORIA A CONFIRMAR CON DIRECTOR (reutilizable parcialmente) |
| `notebooks/02_procesos_contratacion.ipynb` (box plots EDA) | AUTORIA A CONFIRMAR CON DIRECTOR (reutilizable parcialmente) |
| `notebooks/05_integracion_contratos_adiciones.ipynb` (box plots EDA) | AUTORIA A CONFIRMAR CON DIRECTOR (reutilizable parcialmente) |
| `visualizer/` (Next.js, roto) | AUTORIA A CONFIRMAR CON DIRECTOR — no coincide con el stack exigido independientemente de quien lo construyo |

#### 3.4.5 Archivos EXCLUIDOS del entregable

`modelo_predictivo_global/chatbot/app.py`, `gemini_client.py`, `prompts.py`, `predictor.py` (chatbot RAG Streamlit del modelo predictivo, Fase IV de `doc/contexto/tabla_fases_trabajo_dirigido.md`); `report/imagenes/*` (graficos de evaluacion de modelos: ROC, matrices de confusion, importancia de variables — no son visualizaciones descriptivas de contratacion).

#### 3.4.6 Brecha tecnica

Falta en su totalidad: (a) un tablero interactivo funcional en el stack exigido o uno equivalente aprobado; (b) filtros dinamicos por modalidad/entidad/territorio; (c) box plots de los indicadores continuos (que tampoco existen aun, ver seccion 5 de brechas globales); (d) mapas coropleticos; (e) reparacion o reemplazo de `visualizer/` si se decide reutilizarlo.

#### 3.4.7 Tres caminos de decision

**Camino A - MANTENER objetivo original (Dash puro):**
- Que se debe construir: aplicacion Dash desde cero, con componentes Plotly para distribuciones, box plots y mapas coropleticos, alimentada por los parquets de `entregables/04-datasets/` (una vez confirmada su autoria) o regenerados de forma propia.
- Tiempo estimado: 3-4 semanas (no existe ninguna base reutilizable en Dash; requiere ademas tener listos primero los indicadores continuos de OE-04/seccion 5).
- Riesgo tecnico: Medio (Dash tiene curva de aprendizaje si no se ha usado antes; no hay codigo previo que reutilizar).
- Riesgo academico: Bajo (cumple literalmente el texto original).
- Ventajas: fidelidad total al anteproyecto.
- Desventajas: es la tarea de mayor costo temporal de las cuatro; alto riesgo de no alcanzar a completarla dentro del cronograma.

**Camino B - REFORMULAR objetivo (Streamlit + Plotly):**
- Nueva redaccion propuesta: "Disenar un tablero interactivo basado en Streamlit y Plotly que presente resultados (distribuciones, outliers con box plots, segmentaciones por modalidad/entidad/territorio) para apoyar la interpretacion, la transparencia y la toma de decisiones."
- Que se conserva: el objetivo funcional completo (distribuciones, box plots, segmentaciones); la libreria de graficos Plotly.
- Que se ajusta: el framework de la aplicacion web cambia de Dash a Streamlit, tecnicamente equivalente para tableros de un solo desarrollador y con curva de aprendizaje menor.
- Tiempo estimado: 2 semanas (asumiendo que los indicadores continuos de tiempo/costo/alcance ya esten calculados; Streamlit permite iterar mas rapido que Dash).
- Riesgo academico: Medio (requiere aprobacion expresa del director/comite para el cambio de tecnologia respecto al texto original del anteproyecto).
- Ventajas: reduce significativamente el tiempo de desarrollo frente al Camino A; Streamlit+Plotly es una combinacion estandar y bien documentada para tableros analiticos.
- Desventajas: se aleja literalmente de "Dash" mencionado en el instrumento 3.7.4.b del anteproyecto; debe justificarse explicitamente en el documento final.

**Camino C - EXCLUIR o CONVERTIR EN LIMITACION:**
- Justificacion tecnica: solo seria viable si el tiempo restante hasta la entrega es insuficiente incluso para el Camino B.
- Impacto sobre el objetivo general: alto — OE-04 es uno de los cuatro objetivos especificos centrales; excluirlo debilita sustancialmente el cumplimiento del objetivo general ("apoyar la interpretacion, la transparencia y la toma de decisiones").
- Como redactarlo en limitaciones: declarar que, por restricciones de tiempo, las visualizaciones se entregan como notebooks estaticos (matplotlib/seaborn) con capturas incluidas en el documento final, en lugar de un tablero web interactivo, dejando el tablero interactivo como trabajo futuro.
- Riesgo ante jurado: alto; un jurado puede considerar que un objetivo especifico completo no fue alcanzado.
- Nota: recomendado **solo si** el Camino B resulta inviable por tiempo (ver seccion 11, Bloque C).

#### 3.4.8 Recomendacion final para este OE

**Reformular (Camino B)**, migrando de Dash a Streamlit+Plotly. Es la opcion que permite cumplir el espiritu completo del objetivo (interactividad, box plots, segmentaciones) dentro de un tiempo realista, dado que no existe ninguna base de codigo reutilizable en Dash y el desarrollo desde cero en ese framework (Camino A) tiene el mayor riesgo de incumplimiento por tiempo de todo el anteproyecto. Requiere aprobacion explicita del director dado que el anteproyecto nombra "Dash" especificamente en el instrumento 3.7.4.b.

---

## 4. Diferenciacion de autoria

| Ruta / archivo | Clasificacion | Justificacion | Uso permitido en la tesis de Andres |
|---|---|---|---|
| `notebooks/00_definicion_tabla_base.ipynb` | AUTORIA A CONFIRMAR CON DIRECTOR | `doc/contexto/CONTEXTO.md` (linea 10) declara el proposito predictivo del pipeline, pero el contenido tecnico (clasificacion de fuentes, llaves de integracion) es neutro y reutilizable | Como insumo tecnico, previa confirmacion; no citar como aporte propio sin autorizacion |
| `notebooks/01_contratos_electronicos.ipynb` a `04_proveedores.ipynb`, `06_proponentes_por_proceso.ipynb` | AUTORIA A CONFIRMAR CON DIRECTOR | Mismo fundamento; extraccion y perfilado de fuentes SECOP, sin logica de modelado | Como insumo tecnico, previa confirmacion |
| `notebooks/07_depuracion_variables_modelo.ipynb` | CODIGO DEL COMPANERO - EXCLUIR | Titulo explicito "para Modelo Predictivo"; produce targets binarios de clasificacion (`tiempo`, `presupuesto`, `alcance`) usados como `tuvo_atraso`/`tuvo_sobrecosto` en el modelado (RESUMEN_CODIGO.md, seccion 6) | No usar el notebook como evidencia; el dataset resultante puede usarse unicamente como materia prima para derivar indicadores propios, documentando la fuente |
| `notebooks/08_integracion_rup_no_consorcios.ipynb` | CODIGO DEL COMPANERO - EXCLUIR | Enriquecimiento con indicadores financieros RUP, exclusivo de las features estructurales del modelo predictivo | No usar como evidencia |
| `scripts/generar_diccionario_datos.py` | AUTORIA A CONFIRMAR CON DIRECTOR | Script generico, sin logica de modelado, reutilizable para OE-03 | Uso permitido como insumo tecnico previa confirmacion de autoria |
| `scripts/generar_diccionario_md.py` | AUTORIA A CONFIRMAR CON DIRECTOR | Mismo fundamento | Uso permitido como insumo tecnico previa confirmacion |
| `scripts/extraer_rup_auto.py` | CODIGO DEL COMPANERO - EXCLUIR | Alimenta exclusivamente el enriquecimiento RUP del modelo predictivo (RESUMEN_CODIGO.md, seccion 6 y 12) | No usar |
| `scripts/extraer_indicadores_pliegos.py` | CODIGO DEL COMPANERO - EXCLUIR | Extraccion de indicadores financieros de pliegos para features del modelo predictivo | No usar |
| `scripts/gemini/` (todos los archivos) | CODIGO DEL COMPANERO - EXCLUIR | Scraping y extraccion via Gemini para consorcios/pliegos, exclusivo del modelado predictivo | No usar |
| `modelo_predictivo_global/` (todo) | CODIGO DEL COMPANERO - EXCLUIR | Modelado predictivo v2 (LightGBM ganador), CRISP-DM, confirmado en `doc/contexto/CONTEXTO.md` y `plan-trabajo-dirigido.md` | No usar bajo ninguna circunstancia como evidencia propia |
| `modelo-predictivo-preliminar/` (todo) | CODIGO DEL COMPANERO - EXCLUIR | Modelado predictivo v1 y sub-sprints (consorcios, tuning) | No usar |
| `extractor-indicadores-docker/` (todo) | CODIGO DEL COMPANERO - EXCLUIR | Pipeline Docker de extraccion de indicadores RUP via PDFs, soporte exclusivo del modelado predictivo | No usar |
| `entregables/04-datasets/` (datasets crudos: contratos, procesos, adiciones, proveedores, proponentes) | AUTORIA A CONFIRMAR CON DIRECTOR | Son la version final empaquetada de los datasets producidos por notebooks 00-06 | Uso permitido como insumo tecnico (materia prima), previa confirmacion de autoria; no como "modelo estrella propio" sin transformacion adicional |
| `entregables/04-datasets/` (`contratos_depurado_modelo.parquet`, `consolidado_global.parquet`, `consolidado_imputado.parquet`) | CODIGO DEL COMPANERO - EXCLUIR | Version depurada/codificada especificamente para modelado ML (targets binarios, encoding, imputacion mediana+flags) | No usar |
| `entregables/05-modelos/` | CODIGO DEL COMPANERO - EXCLUIR | Modelos serializados (.pkl) del modelado predictivo | No usar |
| `entregables/07-notebooks/modelado-v1/` y `modelado-v2/` | CODIGO DEL COMPANERO - EXCLUIR | Notebooks de entrenamiento y evaluacion de modelos supervisados | No usar |
| `entregables/07-notebooks/extraccion-datos/` | AUTORIA A CONFIRMAR CON DIRECTOR | Copia byte-identica de `notebooks/00-08` (verificado por `diff -q`); aplica la misma clasificacion que el original, con la salvedad de que 07 y 08 dentro de esta copia son CODIGO DEL COMPANERO - EXCLUIR | Igual tratamiento que sus originales en `notebooks/` |
| `entregables/08-codigo-fuente/` | CODIGO DEL COMPANERO - EXCLUIR | Copia empaquetada de `modelo_predictivo_global/src/`, `chatbot/` y scripts de extraccion RUP/pliegos | No usar |
| `visualizer/` (todo) | AUTORIA A CONFIRMAR CON DIRECTOR | No coincide con el stack de ninguno de los dos anteproyectos de forma exacta (Next.js/DuckDB-WASM); proposito y autoria no documentados en `doc/contexto/` | No usar como evidencia de cumplimiento de OE-04 sin repararlo y sin confirmar autoria; en cualquier caso no satisface el stack exigido (Dash/Plotly) |
| `report/` (todo: informes, anexos, `main.tex`, `imagenes/`) | CODIGO DEL COMPANERO - EXCLUIR | Contiene PRIMER/SEGUNDO/INFORME-FINAL y anexos del modelado predictivo (ROC, matrices de confusion, SHAP, LightGBM) | No usar |
| `data/diccionario_datos.json` | AUTORIA A CONFIRMAR CON DIRECTOR | Generado por `scripts/generar_diccionario_datos.py`, generico | Uso permitido como insumo previa confirmacion |
| `doc/contexto/` (`CONTEXTO.md`, `plan-trabajo-dirigido.md`, `tabla_fases_trabajo_dirigido.md`) | CODIGO DEL COMPANERO - EXCLUIR | Documentacion explicita del proyecto predictivo del companero (CRISP-DM, RF/XGBoost/LightGBM, RAG+LLM); no debe presentarse como documentacion propia de Andres | Uso permitido unicamente como referencia de contexto interno, nunca como evidencia o documentacion propia en el entregable final |
| `requirements.txt` (raiz) | INSUMO EXTERNO (uso permitido) | No contiene librerias de modelado predictivo (pandas, numpy, matplotlib, seaborn, sodapy, pyarrow, openpyxl, jupyter, nbconvert); es generico para cualquier pipeline de datos | Uso permitido directamente |

---

## 5. Brechas globales detectadas

| Brecha | Descripcion | OE afectados | Impacto sobre el objetivo general | Prioridad | Accion sugerida |
|---|---|---|---|---|---|
| Ausencia de indicadores continuos de tiempo/costo/alcance | Solo existen flags binarios (`tiempo`, `presupuesto`, `alcance`) construidos para clasificacion ML en `notebooks/07` (companero); el anteproyecto exige magnitudes continuas/categoricas | OE-03, OE-04 | Alto — es el nucleo del marco teorico (restriccion de hierro) | Critica | Construir notebook propio de indicadores continuos a partir de columnas ya integradas |
| Ausencia de modelo estrella formal | Sin DDL, sin motor de BD, sin diagrama; solo joins de pandas persistidos como Parquet | OE-02 | Alto — exigido explicitamente en el texto de OE-02 | Alta | Reformular a modelo dimensional simplificado (seccion 3.2.7, Camino B) |
| Ausencia de dashboard Dash/Plotly funcional | Ningun archivo `.py` usa Dash o Plotly; `visualizer/` (Next.js) esta roto; el unico Streamlit existente es del companero | OE-04 | Alto — OE-04 completo sin evidencia funcional | Critica | Reformular a Streamlit+Plotly y construir desde cero (seccion 3.4.7, Camino B) |
| Ausencia de umbrales cuantitativos de calidad de datos | Ni el anteproyecto ni el codigo definen umbrales de nulidad/cobertura aceptables | OE-03 | Medio | Media | Definir umbrales explicitos y verificarlos programaticamente |
| Ausencia de logs persistentes en la extraccion | Solo hay narrativa en celdas markdown, sin archivos de log con timestamps | OE-01 | Medio | Media | Anadir logging a archivo en el script de extraccion refactorizado |
| Ausencia de filtro de fecha 2018-2024 verificable | No se encontro en el codigo estatico un filtro `WHERE fecha_de_firma BETWEEN ...` | OE-01 | Medio | Alta | Anadir el filtro explicito en la consulta SoQL |
| Ausencia de script reutilizable de extraccion | Toda la logica de extraccion vive dentro de notebooks, no hay `.py` parametrizable | OE-01 | Medio | Media | Extraer la logica a `extraer_secop.py` |
| Ausencia de README raiz para la porcion descriptiva | No existe `README.md` en la raiz del repositorio con instrucciones de instalacion/ejecucion del pipeline base | OE-01, OE-02, OE-03, OE-04 | Medio | Media | Redactar README raiz especifico de la porcion descriptiva |
| Riesgo de contaminacion con codigo predictivo del companero | Mayoria del peso del repositorio (157 MB en `entregables/`, 69 MB en `modelo-predictivo-preliminar/`, 56 MB en `modelo_predictivo_global/`) corresponde al companero | Todos | Muy alto — riesgo de atribucion incorrecta ante jurado | Critica | Ejecutar el plan de exclusion de la seccion 6 |
| Ambiguedad predictivo/descriptivo en el propio anteproyecto | El anteproyecto menciona "predecirlas" en la pregunta de investigacion y scikit-learn en el instrumento 3.7.4.a sin un OE asociado (ya senalado en `RESUMEN_CONTROL.md`, seccion 21) | Todos (afecta la coherencia general) | Medio-Alto — puede sugerir al jurado que el alcance no esta bien delimitado | Alta | Resolver con el director si el anteproyecto se ajusta para eliminar la ambiguedad (retirar "predecirlas" y la mencion a scikit-learn, o justificar su presencia) |

---

## 6. Codigo predictivo del companero: plan de exclusion

### 6.1 Carpetas y archivos a excluir explicitamente del entregable

- `modelo_predictivo_global/` (completa)
- `modelo-predictivo-preliminar/` (completa, incluye `consorcios/` y `tuning/`)
- `extractor-indicadores-docker/` (completa)
- `entregables/05-modelos/`
- `entregables/06-imputers/`
- `entregables/07-notebooks/modelado-v1/`
- `entregables/07-notebooks/modelado-v2/`
- `entregables/08-codigo-fuente/` (completa, incluye la copia del chatbot y de los scripts de extraccion RUP/pliegos)
- `entregables/09-pipeline-docker/`
- `entregables/10-figuras/`
- `entregables/11-documentacion-tecnica/`
- `report/` (completa: informes, anexos, `main.tex`, `imagenes/`)
- `scripts/gemini/` (completa)
- `scripts/extraer_rup_auto.py`
- `scripts/extraer_indicadores_pliegos.py`
- `scripts/poblar_indicadores_pliegos.py`
- `scripts/scraper_pliegos_poc.py`
- `scripts/validar_extraccion_pliegos.py`
- `notebooks/07_depuracion_variables_modelo.ipynb`
- `notebooks/08_integracion_rup_no_consorcios.ipynb`
- `entregables/04-datasets/contratos_depurado_modelo.parquet`, `consolidado_global.parquet`, `consolidado_imputado.parquet`
- `doc/contexto/CONTEXTO.md`, `doc/contexto/plan-trabajo-dirigido.md`, `doc/contexto/tabla_fases_trabajo_dirigido.md` (como documentacion propia; permitido solo como referencia interna de contexto)

### 6.2 Justificacion academica de la exclusion

`doc/contexto/CONTEXTO.md` (linea 10) declara literalmente: "Trabajo de grado para construir un **modelo predictivo** sobre contratos de Obra Publica del SECOP II [...] Metodologia: CRISP-DM". `doc/contexto/plan-trabajo-dirigido.md` (titulo completo: "Propuesta de analitica predictiva de datos abiertos caso SECOP") formula un objetivo general y objetivos especificos centrados en "identificar tempranamente riesgos de sobrecostos y retrasos" mediante "algoritmos de Aprendizaje Automatico" y una "interfaz de consulta inteligente" con RAG+LLM — un objeto de estudio y una metodologia (CRISP-DM) distintos del ciclo de vida del dato (NIST, 2015) que sustenta el anteproyecto de Andres. `doc/contexto/tabla_fases_trabajo_dirigido.md` formaliza 4 fases (ETL para modelado, Modelado Predictivo, Evaluacion, Despliegue RAG+LLM) con fechas especificas (16 feb 2026 a 7 jun 2026), un cronograma que no corresponde al de `AnteproyectoAndres.md`. Los nombres explicitos de carpetas (`modelo_predictivo_global`, `modelo-predictivo-preliminar`, `extractor-indicadores-docker`) y de notebooks (`07_depuracion_variables_modelo.ipynb` — literalmente "para Modelo Predictivo") confirman de forma consistente e independiente que este codigo pertenece a un trabajo de grado distinto.

### 6.3 Como redactarlo en la tesis

Propuesta de parrafo para el capitulo de metodologia o un anexo de deslinde de autoria:

"El presente trabajo de grado comparte el repositorio de codigo con un proyecto paralelo de analitica predictiva, desarrollado por otro estudiante de Ingenieria de Sistemas bajo la direccion del mismo tutor, Ing. Nelson Beltran Galvis. Dicho proyecto, documentado internamente bajo metodologia CRISP-DM (ver `doc/contexto/CONTEXTO.md` y `doc/contexto/plan-trabajo-dirigido.md` del repositorio), tiene como objetivo construir modelos de clasificacion supervisada (Random Forest, XGBoost, LightGBM) y un prototipo de interfaz conversacional basado en Modelos de Lenguaje de Gran Escala, orientados a predecir la probabilidad de prorrogas y sobrecostos en contratos de obra publica. Este trabajo de grado, de naturaleza descriptivo-analitica y sustentado en el marco teorico de la restriccion de hierro (Atkinson, 1999; Meredith & Mantel, 2012), no reclama como aporte propio ningun artefacto de las carpetas `modelo_predictivo_global/`, `modelo-predictivo-preliminar/`, `extractor-indicadores-docker/`, `entregables/05` a `11/`, `report/`, ni de los scripts de extraccion de indicadores RUP y pliegos (`scripts/gemini/`, `scripts/extraer_rup_auto.py`, `scripts/extraer_indicadores_pliegos.py`). La autoria del pipeline base de extraccion e integracion de datos (`notebooks/00` a `06`) se documenta como insumo compartido, sujeto a confirmacion formal por parte del director de tesis."

### 6.4 Riesgos si NO se excluye correctamente

- Un jurado o comite que revise el repositorio completo puede detectar facilmente, por los nombres de carpeta y la documentacion interna (`doc/contexto/`), que gran parte del codigo corresponde a un objetivo predictivo ajeno, lo que puede interpretarse como apropiacion indebida de trabajo de un tercero.
- Riesgo de sancion academica por presentar como propio un trabajo que no lo es, incluyendo posible apertura de un proceso disciplinario segun el reglamento estudiantil de la institucion.
- Perdida de credibilidad del documento completo, incluyendo las partes que si son aporte genuino de Andres, si el jurado detecta la mezcla y generaliza la sospecha a todo el trabajo.
- Conflicto directo con el companero si este ya presento o va a presentar el mismo codigo como su propio trabajo de grado, generando un problema de solapamiento visible ante ambos comites evaluadores.
- Invalidacion parcial o total de la sustentacion si se determina que el deslinde de autoria no fue declarado de forma transparente desde el inicio.

---

## 7. Reformulacion sugerida de objetivos

### 7.1 Objetivo general

**Version original:** "Analizar integralmente la contratacion de obra publica en Colombia mediante el procesamiento de datos de SECOP, con el fin de determinar la eficiencia de los proyectos segun su tiempo, costo y alcance, identificando las variables criticas que condicionan el exito de la ejecucion contractual."

**Version propuesta:** "Analizar integralmente la contratacion de obra publica en Colombia mediante el procesamiento de datos de SECOP, con el fin de determinar la eficiencia de los proyectos segun su tiempo, costo y alcance, identificando las variables criticas que condicionan el exito de la ejecucion contractual, a traves de un modelo dimensional simplificado y un tablero interactivo basado en Streamlit y Plotly."

La version propuesta conserva integramente el espiritu descriptivo-analitico y el marco de restriccion de hierro; unicamente precisa el mecanismo tecnologico para alinearlo con lo viable en el tiempo disponible.

### 7.2 Objetivos especificos

| OE | Version original | Version propuesta | Justificacion | Requiere aprobacion |
|---|---|---|---|---|
| OE-01 | "Implementar un mecanismo de extraccion automatizada de los datos de SECOP (datos.gov.co), garantizando trazabilidad, actualizacion y reproducibilidad del conjunto de datos de estudio." | "Implementar un mecanismo de extraccion automatizada de los datos de SECOP (datos.gov.co) para el periodo 2018-2024, garantizando trazabilidad mediante registros de ejecucion, actualizacion y reproducibilidad del conjunto de datos de estudio." | Precisa el periodo temporal y el mecanismo de trazabilidad para facilitar la verificacion objetiva del cumplimiento | Director |
| OE-02 | "Estructurar los conjuntos de datos de SECOP relacionados con obra publica (procesos, contratos y proveedores), definiendo el modelo de datos analitico y las reglas de integracion necesarias para su relacionamiento consistente." | "Estructurar los conjuntos de datos de SECOP relacionados con obra publica (procesos, contratos y proveedores) mediante un modelo dimensional simplificado (tabla de hechos y dimensiones sobre archivos Parquet, con diagrama y diccionario de convenciones), definiendo las reglas de integracion necesarias para su relacionamiento consistente." | Reemplaza la exigencia implicita de un RDBMS formal por un modelo dimensional documentado, viable en el tiempo disponible | Director y Comite (cambio de exigencia tecnologica) |
| OE-03 | "Normalizar las variables del conjunto de datos analiticos, gestionando duplicados, valores faltantes, inconsistencias y tipificacion, para garantizar la calidad de la informacion y la confiabilidad de los resultados de la analitica." | "Normalizar las variables del conjunto de datos analiticos, gestionando duplicados, valores faltantes, inconsistencias y tipificacion, conforme a umbrales de calidad definidos previamente (nulidad maxima y cobertura minima de integracion), para garantizar la calidad de la informacion y la confiabilidad de los resultados de la analitica." | Anade umbrales cuantitativos explicitos para hacer el objetivo medible y verificable | Director |
| OE-04 | "Disenar visualizaciones y tableros interactivos que presenten resultados (distribuciones, outliers con box plots, segmentaciones por modalidad/entidad/territorio) para apoyar la interpretacion, la transparencia y la toma de decisiones." | "Disenar un tablero interactivo basado en Streamlit y Plotly que presente resultados (distribuciones, outliers con box plots, segmentaciones por modalidad/entidad/territorio) para apoyar la interpretacion, la transparencia y la toma de decisiones." | Streamlit+Plotly es tecnicamente equivalente a Dash/Plotly para un tablero de un solo desarrollador, con menor curva de aprendizaje y tiempo de desarrollo | Director y Comite (cambio de tecnologia respecto al texto original) |

### 7.3 Alcance ajustado

"El alcance del proyecto se mantiene analitico y metodologico, circunscrito a contratos de obra publica en Colombia (SECOP, 2018-2024). Se ajusta unicamente la implementacion tecnologica de dos componentes: (a) el modelo de datos analitico se materializa como un modelo dimensional simplificado sobre archivos Parquet, documentado mediante diagrama y diccionario de convenciones, en lugar de un motor de base de datos relacional formal; y (b) el tablero interactivo se construye sobre Streamlit y Plotly, en lugar de Dash, por ser tecnicamente equivalente para los fines de visualizacion descriptiva de este trabajo. Ambos ajustes preservan integramente el objetivo general y los cuatro objetivos especificos en su espiritu, y se documentan explicitamente como decisiones tecnicas aprobadas por el director."

### 7.4 Limitaciones nuevas a declarar

- El modelo dimensional se materializa sobre archivos Parquet con convenciones documentadas, no sobre un motor de base de datos relacional formal, por restricciones de tiempo del cronograma academico.
- El tablero interactivo se implementa en Streamlit y Plotly en lugar de Dash, dado que no existia base de codigo previa en Dash y el tiempo disponible no permite un desarrollo equivalente desde cero en ese framework.
- El pipeline de extraccion e integracion de datos base (notebooks 00-06) se comparte tecnicamente con un proyecto paralelo de analitica predictiva desarrollado bajo la misma direccion de tesis; su autoria conjunta se documenta explicitamente y no se reclama como aporte exclusivo de este trabajo.
- Los indicadores de tiempo, costo y alcance se construyen como magnitudes continuas/categoricas especificas para este trabajo, de forma independiente a los targets binarios de clasificacion usados en el proyecto predictivo paralelo, para evitar cualquier ambiguedad de autoria o de proposito analitico.
- No se realiza validacion primaria (encuestas/entrevistas) ni contraste caso a caso con expedientes internos de las entidades contratantes, dado que el estudio se basa exclusivamente en datos administrativos secundarios abiertos.

---

## 8. Plan de accion priorizado

| Prioridad | Tarea | OE relacionado | Entregable | Tiempo estimado | Dependencia | Responsable |
|---|---|---|---|---|---|---|
| 1 | Reunion con director para confirmar autoria del pipeline base (notebooks 00-06, scripts de diccionario de datos) | Todos | Acta o correo de confirmacion de autoria | 0.5 semana | Ninguna | Andres Telles + Director |
| 2 | Decision formal del director sobre reformulacion de OE-02 (modelo dimensional simplificado) y OE-04 (Streamlit+Plotly) | OE-02, OE-04 | Aprobacion escrita de cambio de objetivos | 0.5 semana | Tarea 1 | Andres Telles + Director |
| 3 | Redaccion del deslinde de autoria (parrafo de seccion 6.3 de este documento) | Todos | Seccion de metodologia o anexo de deslinde de autoria | 0.5 semana | Tareas 1-2 | Andres Telles |
| 4 | Creacion de carpeta `tesis-andres/` separada y, si aplica, rama git especifica | Todos | Estructura de repositorio limpia | 0.2 semana | Tarea 1 | Andres Telles |
| 5 | Generacion del filtro de fecha 2018-2024 verificable en la extraccion | OE-01 | Consulta SoQL con filtro temporal documentado | 0.3 semana | Tarea 1 | Andres Telles |
| 6 | Construccion de script reutilizable de extraccion (`extraer_secop.py`) con logging | OE-01 | Script `.py` + log de ejecucion | 1 semana | Tareas 1, 5 | Andres Telles |
| 7 | Documentacion del protocolo ETL con umbrales cuantitativos de calidad | OE-03 | Documento de umbrales + reporte de calidad reproducible | 1 semana | Tarea 1 | Andres Telles |
| 8 | Construccion de indicadores continuos de tiempo, costo y alcance (notebook propio) | OE-03, OE-04 | Notebook de indicadores (aporte propio) | 1 semana | Tareas 1, 7 | Andres Telles |
| 9 | Diseno y materializacion del modelo dimensional simplificado (diagrama + convenciones) | OE-02 | Diagrama (svg/png) + parquets organizados en `hechos/`/`dimensiones/` | 1 semana | Tareas 1, 6 | Andres Telles |
| 10 | Construccion del dashboard Streamlit + Plotly | OE-04 | Aplicacion funcional con filtros y box plots | 2 semanas | Tarea 8 | Andres Telles |
| 11 | README raiz de la porcion descriptiva (instalacion, ejecucion, alcance) | Todos | `README.md` en `tesis-andres/` o raiz | 0.2 semana | Tareas 4, 6 | Andres Telles |
| 12 | Capturas de evidencia del dashboard funcionando | OE-04 | Imagenes/capturas para el documento final | 0.2 semana | Tarea 10 | Andres Telles |
| 13 | Redaccion del capitulo de desarrollo tecnico | Todos | Capitulo de tesis | 1.5 semanas | Tareas 6-12 | Andres Telles |
| 14 | Revision de coherencia final antes de la entrega (cruce contra este documento) | Todos | Checklist de cierre completado | 0.3 semana | Tarea 13 | Andres Telles + Director |

**Tiempo total estimado del plan:** aproximadamente 9-10 semanas de trabajo secuencial completo, o 5-6 semanas si algunas tareas se paralelizan (por ejemplo, tareas 5-7 pueden avanzar en paralelo con la tarea 2 en tramite de aprobacion). Esta estimacion asume dedicacion significativa y continua; debe contrastarse contra el tiempo real disponible hasta la fecha de entrega (ver Bloque C de la seccion 11).

---

## 9. Evidencias tecnicas a generar

| Evidencia | OE que respalda | Como generarla | Herramienta | Estado |
|---|---|---|---|---|
| Log de extraccion con timestamps y numero de registros por consulta | OE-01 | Anadir logging a archivo dentro de `extraer_secop.py` | Modulo `logging` de Python | Pendiente |
| Diagrama del modelo dimensional (svg/png) | OE-02 | Disenar diagrama de hechos/dimensiones sobre los parquets integrados | Draw.io / Mermaid / similar | Pendiente |
| Script reutilizable de extraccion (`extraer_secop.py`) fuera de notebooks | OE-01 | Refactorizar la logica ya existente en `notebooks/00-06` hacia un modulo parametrizable | Python + `sodapy` | Pendiente |
| Notebook de indicadores continuos (aporte propio, no del companero) | OE-03, OE-04 | Calcular desviacion de tiempo (dias), desviacion de costo (%), indice de alcance categorico, a partir de `entregables/04-datasets/contratos_adiciones_obra.parquet` | Jupyter + pandas | Pendiente |
| Reporte de calidad de datos con umbrales aplicados | OE-03 | Formalizar en script/notebook los umbrales de nulidad/cobertura y verificar su cumplimiento | Python + pandas | Pendiente |
| Dataset intermedio y depurado con hash de version | OE-02, OE-03 | Registrar hash (`sha256`) de cada version de parquet generado | Python (`hashlib`) | Pendiente |
| Diccionario de datos exportado (md y json) | OE-03 | Ya existe generador; solo requiere re-ejecutarse contra los parquets vigentes | `scripts/generar_diccionario_datos.py`, `generar_diccionario_md.py` | Parcialmente disponible (requiere confirmar autoria y regenerar) |
| Capturas del dashboard Streamlit+Plotly funcionando | OE-04 | Capturas de pantalla de cada vista del tablero | Navegador + captura de pantalla | Pendiente |
| Segmentaciones por modalidad, entidad y territorio | OE-04 | Construir dentro del dashboard, con filtros interactivos | Streamlit + Plotly | Pendiente |
| Box plots de indicadores continuos | OE-04 | Generar box plots de los indicadores propios (no los del companero) por modalidad/entidad | Plotly (dentro del dashboard) o matplotlib/seaborn (notebook) | Pendiente |
| Mapa coropletico (si el tiempo lo permite) | OE-04 | Mapa por departamento con Plotly (`choropleth`) usando codigos DANE o similar | Plotly | Pendiente (condicionado a tiempo disponible) |
| README con instrucciones de reproduccion | Todos | Redactar README raiz o en `tesis-andres/` | Markdown | Pendiente |
| Deslinde de autoria firmado o documentado | Todos | Formalizar el parrafo de la seccion 6.3 con firma o correo de aprobacion del director | Documento firmado / correo institucional | Pendiente |

---

## 10. Riesgos academicos y tecnicos consolidados

| Riesgo | Tipo | Severidad | Probabilidad | Impacto sobre la tesis | Mitigacion |
|---|---|---|---|---|---|
| Presentar codigo predictivo del companero como propio | Autoria | Alta | Media (si no se actua) | Muy alto — posible sancion academica y perdida de credibilidad total del trabajo | Ejecutar el plan de exclusion (seccion 6) y el deslinde de autoria antes de cualquier entrega |
| Redactar la tesis prometiendo funcionalidades no implementadas (Dash, modelo estrella formal) | Academico | Alta | Media | Alto — incumplimiento detectable por el jurado al revisar el repositorio | Reformular OE-02 y OE-04 con aprobacion formal antes de redactar el documento final |
| Ambiguedad predictivo/descriptivo del propio anteproyecto ("predecirlas", scikit-learn en 3.7.4.a) | Academico | Media | Alta (ya presente en el texto) | Medio-Alto — puede sugerir alcance mal delimitado ante el jurado | Ajustar el texto del anteproyecto con el director antes de la sustentacion (ver `RESUMEN_CONTROL.md`, seccion 21) |
| Solapamiento visible con la tesis del companero | Academico / autoria | Alta | Media | Alto — riesgo de conflicto entre ambos comites evaluadores | Coordinar con el companero y el director que codigo aparece en cada entregable (ver seccion 11, Bloque D) |
| Falta de tiempo para construir el dashboard desde cero | Temporal | Alta | Media-Alta | Alto — OE-04 es el objetivo con mayor brecha | Priorizar Streamlit sobre Dash (menor curva de aprendizaje) y iniciar cuanto antes (tarea 10 del plan de accion) |
| Falta de aprobacion del director para reformular OE-02/OE-04 | Academico | Media | Media | Alto — bloquea la ejecucion del plan de accion completo | Agendar la reunion de la tarea 1 y 2 del plan de accion lo antes posible |
| Contradiccion entre stack exigido (Dash/PySpark) y stack implementado (Next.js roto, sin PySpark) | Tecnico | Media | Alta (ya confirmada) | Medio | Formalizar la reformulacion tecnologica (seccion 7) con el director |
| El jurado abre el repositorio completo y detecta carpetas ajenas (`modelo_predictivo_global/`, `report/`, etc.) | Autoria | Alta | Alta si no se separa el repositorio | Muy alto | Crear `tesis-andres/` separada y/o repositorio independiente antes de la entrega (tareas 4 del plan de accion) |
| Falta de trazabilidad entre objetivos y evidencias | Academico | Media | Media | Medio | Usar esta matriz y `RESUMEN_CODIGO.md` como base del capitulo de desarrollo tecnico, citando rutas exactas |

---

## 11. Preguntas criticas al autor

**Bloque A - Autoria:**
- ¿Que notebooks del pipeline base (00-06) son aporte propio, del companero o compartidos?
- ¿Existe documentacion (correos, actas, commits) que respalde la autoria? (El historial git actual solo tiene 2 commits del mismo autor tecnico y no permite diferenciar autoria real, segun `RESUMEN_CODIGO.md`, seccion 0.)
- ¿El director acepta que la extraccion sea insumo compartido entre ambos trabajos de grado?

**Bloque B - Alcance:**
- ¿Se acepta reformular OE-04 hacia Streamlit + Plotly en lugar de Dash?
- ¿Se acepta un modelo dimensional simplificado (Parquet + diagrama + convenciones) en lugar de un modelo estrella formal en un motor de base de datos relacional?
- ¿Se acepta definir los umbrales de calidad de datos de forma ex-post (una vez revisados los datos ya integrados)?

**Bloque C - Tiempo:**
- ¿Cuantas semanas hay hasta la entrega final? (No especificado en el anteproyecto ni en los documentos de control disponibles; es indispensable para decidir entre los caminos A y B en cada OE.)
- ¿Se puede sustentar despues del companero, para evitar solapamiento visual ante el jurado?

**Bloque D - Coordinacion:**
- ¿El companero ya sustento o presentara los mismos notebooks (00-08) como parte de su propio trabajo?
- ¿Hay acuerdo escrito entre ambos estudiantes y el director sobre que codigo puede aparecer en cada tesis?

---

## 12. Version ultracompacta de decisiones

Cruce entre `AnteproyectoAndres.md` (descriptivo, restriccion de hierro) y el codigo real (`RESUMEN_CODIGO.md`). Alineacion global: BAJA. Ningun OE en estado Cumple: OE-01 y OE-03 Parciales, OE-02 Parcial (solo integracion, sin modelo estrella formal), OE-04 No cumple (sin Dash/Plotly funcional). El pipeline existente (notebooks 00-08, scripts/) fue construido explicitamente para un trabajo de grado predictivo paralelo (CRISP-DM, LightGBM, chatbot RAG) del companero, segun `doc/contexto/CONTEXTO.md` linea 10.

**Decision por OE:** OE-01 Mantener (completar filtro fecha, logs, script reutilizable, 1-1.5 semanas). OE-02 Reformular hacia modelo dimensional simplificado sobre Parquet (1 semana). OE-03 Mantener (anadir umbrales de calidad, 1 semana). OE-04 Reformular hacia Streamlit+Plotly en lugar de Dash (2 semanas).

**Codigo a excluir del entregable:** `modelo_predictivo_global/`, `modelo-predictivo-preliminar/`, `extractor-indicadores-docker/`, `entregables/05` a `11`, `report/`, `scripts/gemini/`, `scripts/extraer_rup_auto.py`, `scripts/extraer_indicadores_pliegos.py`, `notebooks/07_depuracion_variables_modelo.ipynb`, `notebooks/08_integracion_rup_no_consorcios.ipynb`.

**Codigo a confirmar autoria con el director:** `notebooks/00-06`, `scripts/generar_diccionario_datos.py`, `generar_diccionario_md.py`, `data/diccionario_datos.json`, `entregables/04-datasets/` (datasets crudos e integrados v1), `visualizer/`.

**Brechas principales:** indicadores continuos de tiempo/costo/alcance inexistentes (solo binarios del companero); dashboard Dash/Plotly inexistente; modelo estrella no materializado; sin README raiz; alto riesgo de contaminacion de autoria.

**Plan de accion (5 tareas criticas):** (1) reunion con director para confirmar autoria del pipeline base; (2) aprobacion formal de reformulacion de OE-02 y OE-04; (3) redaccion del deslinde de autoria; (4) construccion de indicadores continuos propios; (5) construccion del dashboard Streamlit+Plotly.

**Tiempo total estimado:** 9-10 semanas en modo secuencial, 5-6 semanas si se paralelizan tareas independientes.

**Riesgo global:** ALTO, dominado por el riesgo de autoria (contaminacion con el trabajo del companero) y por el tiempo requerido para OE-04, el objetivo con mayor brecha.

---

## 13. Checklist de siguientes pasos

- [ ] Reunion con director para validar autoria del pipeline base.
- [ ] Decision formal sobre camino A, B o C por cada OE.
- [ ] Creacion de rama git especifica: `tesis-andres-descriptivo`.
- [ ] Creacion de carpeta `tesis-andres/` separada.
- [ ] Redaccion del deslinde de autoria.
- [ ] Construccion de indicadores continuos.
- [ ] Diseno e implementacion del modelo dimensional.
- [ ] Construccion del dashboard.
- [ ] Documentacion del protocolo ETL con umbrales.
- [ ] Generacion de evidencias listadas en la seccion 9.
- [ ] Redaccion del capitulo de desarrollo tecnico.
- [ ] Revision de coherencia final antes de entrega.
