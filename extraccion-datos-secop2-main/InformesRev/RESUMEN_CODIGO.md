# RESUMEN CODIGO DEL PROYECTO

## 0. Metadatos de la auditoria

- **Fecha de auditoria:** 2026-07-23
- **Ruta del repositorio analizado:** `/home/william-telles/Documentos/extraccion-datos-secop2-main (1)/extraccion-datos-secop2-main/`
- **Anteproyecto de referencia:** `InformesRev/AnteproyectoAndres.md` (Analitica descriptiva de la contratacion de obra publica en Colombia — Camilo Andres Telles Ramirez)
- **RESUMEN_CONTROL.md disponible:** Si (`InformesRev/RESUMEN_CONTROL.md`), usado como referencia de objetivos.
- **Tamano aproximado del repositorio:** 288 MB totales. Distribucion por carpeta principal: `entregables/` 157 MB, `modelo-predictivo-preliminar/` 69 MB, `modelo_predictivo_global/` 56 MB, `notebooks/` 3.6 MB, `report/` 1.9 MB, `visualizer/` 496 KB, `doc/` 364 KB, `scripts/` 284 KB, `data/` 204 KB, `extractor-indicadores-docker/` 152 KB, `InformesRev/` 128 KB, `pdfs_procesos/` 80 KB, `definciones/` 72 KB.
- **Numero total de archivos:** 586
- **Numero de archivos .py:** 88
- **Numero de notebooks .ipynb:** 73
- **Numero de datasets detectados** (parquet + csv + xlsx + json): 59 (incluye duplicados entre `entregables/` y los directorios de origen)
- **Gestor de dependencias:** pip (`requirements.txt` simple, sin `pyproject.toml`, sin `environment.yml`, sin `Pipfile`)
- **Ultima modificacion aproximada:** la mayoria de archivos del pipeline de datos y modelado tienen timestamp `2026-06-19`; los archivos mas recientes son `doc/contexto/CONTEXTO.md`, `InformesRev/RESUMEN_CONTROL.md`, `InformesRev/AnteproyectoAndres.md` y `doc/AUDITORIA_INCONSISTENCIAS.md` (semana del 2026-07-20 al 2026-07-23).
- **Estado de git:** Activo. Rama `main`, working tree limpio. Historial de solo 2 commits (`e70d3d8` "COMMIT INICIAL proyecto", `4d3d9aa` "Checkpoint antes de generar RESUMEN_CONTROL.md"), ambos del mismo autor (`ndru <andrestera665@gmail.com>`). El historial no permite hacer `git blame` por autor real de cada modulo porque todo el codigo preexistente se importo en un unico commit inicial.

**Hallazgo critico transversal (fundamenta gran parte de este informe):** los documentos `doc/contexto/CONTEXTO.md` (linea 10: *"Trabajo de grado para construir un **modelo predictivo**..."*), `doc/contexto/plan-trabajo-dirigido.md` (titulo: *"Propuesta de analitica predictiva de datos abiertos caso SECOP"*) y `doc/contexto/tabla_fases_trabajo_dirigido.md` documentan explicitamente que **todo el pipeline de datos existente en este repositorio (notebooks 00-08, `scripts/`, `doc/fase2_comprension_datos/`, `doc/fase3_preparacion_datos/`) fue disenado y construido para un trabajo de grado de tipo predictivo bajo metodologia CRISP-DM**, con targets `tuvo_atraso`/`tuvo_sobrecosto`, algoritmos supervisados (Random Forest, XGBoost, LightGBM) y una interfaz RAG+LLM — es decir, corresponde al plan del companero, no al anteproyecto descriptivo de Andres Telles. Este informe distingue en cada seccion que evidencia es reutilizable como base tecnica y que evidencia es exclusiva de la fase predictiva.

---

## 1. Estructura general del repositorio

```
extraccion-datos-secop2-main/
├── dataset.json                      # Metadatos de las 4 fuentes Socrata (columnas, tipos, dataset IDs)
├── requirements.txt                  # Dependencias del pipeline base (pandas, sodapy, etc. — sin ML)
├── .env.example                      # Variables GEMINI_API_KEY / CAPSOLVER_API_KEY
├── prompt.md                         # Prompt operativo maestro CRISP-DM (fase del companero)
├── pasos.md                          # Nota generica sobre GridSearchCV / model zoo (no especifica el proyecto)
├── excel_to_json.py                  # Utilidad: Excel de definiciones -> JSON
├── parquet_viewer.py                 # Utilidad CLI para inspeccionar parquets
├── scrapper.html                     # Artefacto suelto sin referencias desde el codigo (no verificable su uso)
├── data/                             # Solo contiene diccionario_datos.json; los parquets crudos estan gitignored
├── definciones/                      # 5 Excel con definiciones oficiales de columnas SECOP
├── notebooks/                        # 9 notebooks (00-08): extraccion, integracion y depuracion CRISP-DM
├── scripts/                          # Extraccion RUP/pliegos + generadores de diccionario de datos
│   └── gemini/                       # Scripts de scraping y extraccion via Gemini (soporte al modelado)
├── doc/                               # Documentacion de fases CRISP-DM (fase 2 y 3) — plan del companero
│   ├── contexto/                     # CONTEXTO.md, plan-trabajo-dirigido.md, tabla de fases (predictivo)
│   ├── fase2_comprension_datos/      # Informes de comprension de datos + enriquecimiento RUP
│   └── fase3_preparacion_datos/      # Plan de limpieza, derivacion de targets, variables candidatas
├── modelo_predictivo_global/          # Modelado predictivo v2 (LightGBM ganador) — FASE DEL COMPANERO
│   ├── notebooks/ src/ data/ docs/ figuras/ chatbot/
├── modelo-predictivo-preliminar/       # Modelado predictivo v1 + sub-sprints consorcios/tuning — FASE DEL COMPANERO
├── extractor-indicadores-docker/       # Pipeline Docker de extraccion de indicadores RUP via PDFs — soporte predictivo
├── entregables/                        # Empaquetado de entrega (duplica notebooks/src/datasets/modelos) — FASE DEL COMPANERO
├── report/                             # Informes formales (PRIMER/SEGUNDO/INFORME-FINAL, anexos, main.tex) — FASE DEL COMPANERO
├── visualizer/                         # App Next.js/React de exploracion de esquema y calidad de datos
├── pdfs_procesos/                      # Carpeta casi vacia (1 archivo) — placeholder
├── InformesRev/                        # AnteproyectoAndres.md, RESUMEN_CONTROL.md, este archivo
└── .gitignore
```

**Nota sobre `visualizer/`:** no corresponde ni al stack (Dash/Plotly) especificado en el anteproyecto de Andres ni a un artefacto documentado del companero; es una aplicacion Next.js independiente de exploracion de esquema/calidad de datos, y esta actualmente rota (ver seccion 11).

---

## 2. Stack tecnologico detectado

| Tecnologia / libreria | Version detectada | Uso en el proyecto | Archivo donde se importa | Correspondencia con el anteproyecto |
|---|---|---|---|---|
| Python | 3.12.10 (metadata `language_info` de los notebooks, ej. `notebooks/01_contratos_electronicos.ipynb`) | Lenguaje base de todo el pipeline | Todos los `.py`/`.ipynb` | Coincide con lo previsto (Python) |
| Pandas | `>=2.0` en `requirements.txt`; `==2.2.3` en `extractor-indicadores-docker/requirements.txt` | Manipulacion tabular en notebooks 00-08 y scripts | `notebooks/*.ipynb`, `scripts/*.py` | Coincide (2.2.5 del anteproyecto) |
| PySpark | No declarado en ningun `requirements*.txt` ni importado en ningun `.py`/`.ipynb` del repo | No se usa | No aplica | El anteproyecto lo menciona (2.2.5) pero **no esta implementado** |
| sodapy | `>=2.2` en `requirements.txt` | Cliente API Socrata/OData (SODA v3) para extraccion | `notebooks/00_definicion_tabla_base.ipynb` y notebooks 01-06 (uso confirmado por referencias a `Socrata(...)` en las celdas de configuracion) | Coincide directamente con el instrumento 3.7.2.a del anteproyecto |
| Plotly | No declarado en `requirements.txt` raiz; no se detecto import en `.py` del pipeline base | No usado en el pipeline descriptivo/base | No aplica | Previsto en 2.2.5/3.7.4.b, **no implementado** en esta fase |
| Dash | No declarado en `requirements.txt` raiz; no se detecto import en ningun `.py` del repo | No usado en absoluto en el repositorio | No aplica | Previsto en 3.7.4.b, **no implementado en ningun modulo** |
| Streamlit | `>=1.50.0` solo en `modelo_predictivo_global/chatbot/requirements.txt` | Interfaz del chatbot RAG del modelo predictivo | `modelo_predictivo_global/chatbot/app.py` | No corresponde al OE-04 descriptivo; es la interfaz de consulta del companero (Fase IV `tabla_fases_trabajo_dirigido.md`) |
| matplotlib / seaborn | `>=3.7` / `>=0.13` en `requirements.txt` | Graficos EDA (distribuciones, box plots) en notebooks 00-08 | `notebooks/01_contratos_electronicos.ipynb`, `02_procesos_contratacion.ipynb`, `05_integracion_contratos_adiciones.ipynb` | Parcialmente reutilizable para OE-04, pero producido dentro del EDA del companero |
| scikit-learn | `>=1.5.0` en `modelo_predictivo_global/chatbot/requirements.txt`; tambien importado en `modelo_predictivo_global/src/*.py`, `modelo-predictivo-preliminar/**/src/*.py` | Preprocesamiento y entrenamiento de modelos supervisados | Ver seccion 12 (lista completa de archivos) | **ALERTA: libreria asociada a modelado predictivo. Corresponde a la fase del companero, no al alcance descriptivo de OE-01 a OE-04.** |
| XGBoost / LightGBM | Sin pin de version explicito en requirements de modelado; `lightgbm>=4.0.0` en `modelo_predictivo_global/chatbot/requirements.txt` | Modelos ganadores de clasificacion (atraso/sobrecosto) | `modelo_predictivo_global/notebooks/`, `modelo_predictivo_global/data/modelos/lgbm.pkl` | **ALERTA: mismo caso que scikit-learn — fase del companero** |
| SQLAlchemy / DuckDB / SQLite / PostgreSQL | No hay SQLAlchemy ni SQLite en el codigo Python. `@duckdb/duckdb-wasm` si aparece en `visualizer/package.json` (JS, no Python) | DuckDB-WASM se usa dentro de `visualizer/src/hooks/useDuckDB.ts` para consultar parquets en el navegador | `visualizer/src/hooks/useDuckDB.ts` | No hay motor de almacenamiento definido para el pipeline Python; el modelo estrella no esta materializado en ninguna base de datos real (ver seccion 7) |
| Jupyter / nbconvert | `>=1.0` / `>=7.0` en `requirements.txt` | Ejecucion y exportacion de notebooks | Todos los `.ipynb` | Coincide con 3.7.4.a (instrumento tecnico) |
| google-generativeai / google-genai | `>=0.8.0` (chatbot) y `google-genai==0.3.0` (extractor-indicadores-docker) | LLM Gemini para chatbot RAG y para extraccion de indicadores de PDFs de pliegos | `modelo_predictivo_global/chatbot/gemini_client.py`, `extractor-indicadores-docker/src/gemini.py` | No previsto en el anteproyecto de Andres |
| Playwright / CapSolver | `playwright==1.47.0` en `extractor-indicadores-docker/requirements.txt`; `CAPSOLVER_API_KEY` en `.env.example` | Scraping de pliegos SECOP con resolucion de reCAPTCHA | `extractor-indicadores-docker/src/scraper.py`, `scripts/gemini/descargar_pliego.py` | No previsto en el anteproyecto de Andres |
| Next.js / React / Recharts | `next 16.1.6`, `react 19.2.3`, `recharts ^3.8.0` en `visualizer/package.json` | Dashboard de exploracion de esquema/calidad (no Dash/Plotly) | `visualizer/src/app/*.tsx` | **Inconsistencia de stack**: el anteproyecto exige Dash/Plotly (3.7.4.b) o Streamlit/Plotly (2.2.5); el unico dashboard funcional en construccion usa Next.js/React |

---

## 3. Dependencias y entorno

- **Archivos de dependencias detectados:**
  - `requirements.txt` (raiz) — pipeline base, sin ML.
  - `extractor-indicadores-docker/requirements.txt` y su copia `entregables/09-pipeline-docker/requirements.txt` — scraping + Gemini.
  - `modelo_predictivo_global/chatbot/requirements.txt` y su copia `entregables/08-codigo-fuente/chatbot/requirements.txt` — ML + Streamlit + SHAP.
  - `visualizer/package.json` — dependencias Node.js.
  - No existe `pyproject.toml`, `environment.yml` ni `Pipfile` en ningun punto del repositorio.

- **Dependencias declaradas (raiz `requirements.txt`):** pandas>=2.0, numpy>=1.24, matplotlib>=3.7, seaborn>=0.13, sodapy>=2.2, pyarrow>=14.0, openpyxl>=3.1, jupyter>=1.0, nbconvert>=7.0.

- **Dependencias importadas en el codigo pero no declaradas en `requirements.txt` (raiz):** no se detectaron imports de terceros fuera de la lista anterior en `notebooks/*.ipynb` y `scripts/*.py` de nivel raiz (No verificable al 100% sin ejecutar `nbconvert` + analisis AST completo de cada celda; verificado por grep de `import` en el texto fuente de los notebooks).

- **Dependencias declaradas pero no usadas:** no se encontraron declaraciones huerfanas evidentes en `requirements.txt` raiz. `pasos.md` menciona `GridSearchCV`/`RandomizedSearchCV` (scikit-learn) pero ese archivo es generico y no forma parte del codigo ejecutable.

- **Instrucciones de instalacion detectadas:** no existe un `README.md` en la raiz del repositorio con pasos de instalacion. `modelo_predictivo_global/chatbot/README.md` si documenta instalacion local del chatbot (fase del companero). Ningun README describe como instalar/ejecutar el pipeline de extraccion base (notebooks 00-08).

- **Existencia de `.env`, `.env.example`, config files:** `.env.example` en la raiz (GEMINI_API_KEY, CAPSOLVER_API_KEY), `modelo_predictivo_global/chatbot/.env.example` (Gemini), `extractor-indicadores-docker/` (variables via `src/config.py`, no verificado en detalle). No se detecto ningun `.env` real versionado (serian bloqueados por `.gitignore`, que excluye `.env` y `.env.*`).

- **Riesgos de reproducibilidad:**
  - Sin `README.md` raiz ni instrucciones de instalacion del pipeline de extraccion/ETL.
  - Sin version de Python fijada en un archivo de configuracion (`.python-version`/`runtime.txt` no existen); solo se infiere 3.12.10 desde metadata de notebooks.
  - `data/*.parquet` esta excluido de git (`.gitignore` linea "Datos raw"); solo los parquets pequenos de `modelo_predictivo_global/data/`, `modelo-predictivo-preliminar/data/` y `entregables/04-datasets/` se versionan explicitamente. Esto significa que **los datasets crudos e intermedios producidos por los notebooks 00-06 no estan versionados** y solo pueden regenerarse re-ejecutando la extraccion contra la API en vivo.

---

## 4. Comandos de ejecucion detectados

- **Extraccion:** no hay un script/comando unico documentado. La extraccion se ejecuta manualmente celda por celda dentro de `notebooks/00_definicion_tabla_base.ipynb` a `notebooks/06_proponentes_por_proceso.ipynb` (uso de `sodapy.Socrata`). No existe un `main.py` ni CLI de orquestacion para esta fase.
- **Limpieza / ETL:** ejecucion manual de `notebooks/05_integracion_contratos_adiciones.ipynb`, `notebooks/07_depuracion_variables_modelo.ipynb` y `notebooks/08_integracion_rup_no_consorcios.ipynb`. Sin script equivalente en `.py`.
- **Calculo de indicadores:** no existe un modulo o notebook que calcule "desviacion de tiempo", "desviacion de costo" o "indice de cumplimiento de alcance" en terminos continuos tal como los define el anteproyecto (numeral 3.3). Lo mas cercano son los targets binarios `tiempo`/`presupuesto`/`alcance` construidos en `notebooks/07_depuracion_variables_modelo.ipynb` (celda 4, seccion "2. Construccion de variables binarias objetivo").
- **Levantar el dashboard:** `visualizer/` se levanta con `npm run dev` (script definido en `visualizer/package.json`), pero requiere datos en `visualizer/public/data/` que **no existen** en el checkout actual (ver seccion 11). No hay comando para un dashboard Dash/Streamlit del alcance descriptivo.
- **Scripts de orquestacion:** no existe `Makefile`, `run.sh` ni `main.py` a nivel de raiz. `extractor-indicadores-docker/entrypoint.sh` y `docker-compose.yml` orquestan el pipeline de extraccion de indicadores RUP (fase del companero), no el pipeline descriptivo.
- **Instrucciones en README:** no existe README en la raiz del repositorio. Los README existentes estan todos dentro de subcarpetas de la fase predictiva/entregables (ver listado seccion 1) o son boilerplate (`visualizer/README.md`, segun `doc/AUDITORIA_INCONSISTENCIAS.md`, seccion Bajo).

---

## 5. Modulos del pipeline detectados

| Etapa esperada | Archivos / notebooks encontrados | Funcion principal | Estado | Observaciones |
|---|---|---|---|---|
| 1. Extraccion via API Socrata (SoQL, paginacion, trazabilidad, logs) | `notebooks/00_definicion_tabla_base.ipynb` a `06_proponentes_por_proceso.ipynb`; `dataset.json` | Conexion `sodapy.Socrata`, descarga filtrada por `tipo_de_contrato = "Obra"`, paginacion por lotes de IDs (notebook 03, 06) | Implementado (para fines del modelado predictivo) | Sin logs de ejecucion persistentes ni script reutilizable fuera del notebook; trazabilidad limitada a las celdas markdown de cada notebook |
| 2. Estructuracion (integracion procesos+contratos+proveedores) | `notebooks/05_integracion_contratos_adiciones.ipynb`, `08_integracion_rup_no_consorcios.ipynb`; `entregables/04-datasets/contratos_adiciones_obra.parquet` | JOINs por `id_del_portafolio`/`proceso_de_compra`, `codigo_proveedor`/`codigo`, `id_contrato` | Implementado | Reutilizable como base tecnica para OE-02, aunque orientado a features de modelado, no a un modelo estrella formal |
| 3. Modelo estrella (hechos + dimensiones) | No se encontro ningun esquema formal de modelo estrella (ni SQL DDL, ni diagrama, ni motor de BD) | — | **Ausente / No verificable** | Solo existen parquets planos integrados via joins de pandas; no hay tabla de hechos ni dimensiones materializadas como objetos de base de datos |
| 4. Limpieza / ETL (deduplicacion, imputacion, tipificacion) | `notebooks/01_contratos_electronicos.ipynb` (celda 35, "Problemas de calidad"), `02_procesos_contratacion.ipynb`, `07_depuracion_variables_modelo.ipynb` | Deteccion de duplicados, sentinelas "No Definido", casting de campos numericos | Implementado (parcial, con fines de modelado) | Cubre parte de OE-03, pero el criterio de "confiabilidad" no tiene umbral cuantitativo documentado |
| 5. Diccionario de datos | `scripts/generar_diccionario_datos.py`, `scripts/generar_diccionario_md.py`, `data/diccionario_datos.json`, `doc/fase2_comprension_datos/diccionario_datos.md` | Cruza columnas reales de los parquets contra `dataset.json` y genera `.md` | Implementado | Es generico (no exclusivo del modelado); reutilizable directamente para el instrumento 3.7.3.c del anteproyecto |
| 6. Calculo de indicadores (tiempo, costo, alcance) | `notebooks/07_depuracion_variables_modelo.ipynb` (targets binarios `tiempo`, `presupuesto`, `alcance`) | Construccion de variables binarias objetivo para clasificacion | **Parcial / No coincide con la definicion del anteproyecto** | El anteproyecto (3.3) exige indicadores continuos (dias de desviacion, % de adicion); el codigo solo produce flags binarios para ML |
| 7. Analisis descriptivo (tablas, box plots, distribuciones) | `notebooks/01_contratos_electronicos.ipynb`, `02_procesos_contratacion.ipynb`, `05_integracion_contratos_adiciones.ipynb` (box plots confirmados via grep) | EDA exploratorio con matplotlib/seaborn | Parcial | Existe EDA reutilizable, pero enmarcado como "Comprension de Datos" CRISP-DM del companero, no como analisis final de tiempo/costo/alcance segmentado por modalidad/entidad/territorio |
| 8. Visualizacion / dashboard (Dash/Plotly/Streamlit) | `visualizer/` (Next.js, no Dash/Plotly); `modelo_predictivo_global/chatbot/app.py` (Streamlit, pero es el chatbot RAG del companero) | Exploracion de esquema/calidad (`visualizer`) o consulta de predicciones (`chatbot`) | **Ausente para el alcance descriptivo** | Ningun artefacto usa Dash/Plotly como exige el anteproyecto; `visualizer/` esta ademas roto en tiempo de ejecucion (ver seccion 11) |
| 9. Reproducibilidad (README, requirements, scripts) | `requirements.txt` raiz; ausencia de README raiz | — | Parcial | Falta README raiz con instrucciones; existen requirements pero sin instrucciones de uso |
| 10. Almacenamiento (motor de datos usado) | Archivos Parquet planos (`entregables/04-datasets/`, `data/` gitignored) | Persistencia de dataframes via `to_parquet`/`read_parquet` | Implementado como almacenamiento de archivos, **no como motor de base de datos** | No hay SQLite/DuckDB/PostgreSQL materializado para el modelo estrella en Python; DuckDB-WASM solo se usa en el frontend `visualizer/` |

---

## 6. Detalle por archivo

### archivo: notebooks/00_definicion_tabla_base.ipynb
- **Proposito detectado:** Clasificar las 4 fuentes SECOP, definir llaves de integracion y seleccionar la "fuente madre" (`contratosElectronicos`).
- **Funciones principales:** No hay funciones Python reutilizables; es un notebook de analisis exploratorio con celdas secuenciales (23 celdas).
- **Entradas:** `dataset.json`, `definciones/*.xlsx` (via API Socrata en 1 registro de muestra por fuente).
- **Salidas:** Ninguna persistida (solo analisis en memoria); documenta la decision de fuente madre.
- **Dependencias:** pandas, sodapy.
- **Etapa del pipeline:** 1 (extraccion) y 2 (estructuracion, decision de esquema).
- **Objetivo especifico que apoya:** OE-01, OE-02 (parcial, como insumo conceptual).
- **Estado:** implementado.
- **Riesgos detectados:** sin logs de ejecucion; el notebook no fue re-verificado en ejecucion completa en esta auditoria (analisis estatico unicamente).

### archivo: notebooks/01_contratos_electronicos.ipynb
- **Proposito detectado:** Extraer y perfilar la fuente madre (`contratosElectronicos`, tipo Obra).
- **Funciones principales:** Celdas de conexion Socrata, descarga, analisis de distribuciones (celda 10), deteccion de calidad (celda 35).
- **Entradas:** API Socrata dataset `jbjy-vk9h` filtrado por `tipo_de_contrato = "Obra"`.
- **Salidas:** `data/contratos_electronicos_obra.parquet` (51,353 filas x 87 columnas, segun `doc/contexto/CONTEXTO.md` seccion 5; archivo no presente en el checkout actual por `.gitignore`, pero su version integrada final se encuentra en `entregables/04-datasets/contratos_electronicos_obra.parquet`).
- **Dependencias:** pandas, sodapy, matplotlib/seaborn (box plots confirmados por grep).
- **Etapa del pipeline:** 1 (extraccion), 7 (analisis descriptivo/EDA).
- **Objetivo especifico que apoya:** OE-01, OE-03 (parcial), OE-04 (parcial, EDA reutilizable).
- **Estado:** implementado.
- **Riesgos detectados:** el dataset crudo no esta versionado localmente; solo puede regenerarse re-ejecutando contra la API en vivo.

### archivo: notebooks/02_procesos_contratacion.ipynb
- **Proposito detectado:** Extraer y perfilar `procesosDeContratacion`, identificar la llave correcta de integracion (`id_del_portafolio`).
- **Funciones principales:** 66 celdas; deteccion del "hallazgo critico" de la llave correcta (celda 52).
- **Entradas:** API Socrata dataset `p6dx-8zbt`.
- **Salidas:** `procesos_contratacion_obra.parquet` (138,112 x 57, per `entregables/04-datasets/README.md`).
- **Dependencias:** pandas, sodapy, matplotlib/seaborn.
- **Etapa del pipeline:** 1 (extraccion), 4 (calidad/tipificacion), 7 (EDA).
- **Objetivo especifico que apoya:** OE-01, OE-03.
- **Estado:** implementado.
- **Riesgos detectados:** ninguno adicional a los generales de la seccion 14.

### archivo: notebooks/03_adiciones.ipynb
- **Proposito detectado:** Extraer el dataset de modificaciones contractuales (adiciones, prorrogas) filtrado por lotes de IDs.
- **Funciones principales:** Descarga por lotes con `WHERE IN` (seccion 3), analisis de duplicados (seccion 4), guardado en parquet (seccion 12).
- **Entradas:** API Socrata dataset `cb9c-h8sn`, lista de `id_contrato` de la fuente madre.
- **Salidas:** `adiciones_obra.parquet` (249,037 x 5).
- **Dependencias:** pandas, sodapy.
- **Etapa del pipeline:** 1 (extraccion).
- **Objetivo especifico que apoya:** OE-01, OE-02 (insumo para integracion).
- **Estado:** implementado.
- **Riesgos detectados:** 105,836 duplicados detectados en `identificador` (documentado en `doc/contexto/CONTEXTO.md`); no verificado si el notebook aplica deduplicacion final antes de guardar.

### archivo: notebooks/04_proveedores.ipynb
- **Proposito detectado:** Extraer y perfilar `proveedoresRegistrados`.
- **Salidas:** `proveedores_obra.parquet` (13,117 x 25, 54.4% cobertura respecto a proveedores de Obra).
- **Dependencias:** pandas, sodapy.
- **Etapa del pipeline:** 1 (extraccion), 4 (calidad).
- **Objetivo especifico que apoya:** OE-01, OE-02, OE-03.
- **Estado:** implementado.
- **Riesgos detectados:** cobertura parcial (54.4%) limita la representatividad de cualquier indicador que dependa del perfil de proveedor.

### archivo: notebooks/05_integracion_contratos_adiciones.ipynb
- **Proposito detectado:** Integrar contratos + adiciones (LEFT JOIN), construir variables derivadas y analizar extensiones/sobrecostos/suspensiones.
- **Funciones principales:** Agregacion de adiciones a nivel contrato (seccion 3), JOIN (seccion 4), construccion de targets/features (seccion 5), analisis de extensiones/sobrecostos/suspensiones (secciones 7-10).
- **Entradas:** `contratos_electronicos_obra.parquet`, `adiciones_obra.parquet`.
- **Salidas:** `contratos_adiciones_obra.parquet` (48,331 x 125, per `entregables/04-datasets/README.md` — nota: el diccionario de datos en `doc/fase2_comprension_datos/diccionario_datos.md` documenta 111 columnas para este mismo archivo; ver discrepancia en `doc/AUDITORIA_INCONSISTENCIAS.md`, item "Drift de columnas").
- **Dependencias:** pandas, matplotlib/seaborn (box plots confirmados).
- **Etapa del pipeline:** 2 (estructuracion/integracion), 7 (EDA).
- **Objetivo especifico que apoya:** OE-02, OE-04 (parcial).
- **Estado:** implementado.
- **Riesgos detectados:** discrepancia de conteo de columnas (111 vs 125) entre documentacion y el archivo final; no se pudo verificar en que notebook exacto ocurre el salto sin auditar `08_integracion_rup_no_consorcios.ipynb` celda por celda.

### archivo: notebooks/06_proponentes_por_proceso.ipynb
- **Proposito detectado:** Descargar oferentes por proceso y preparar el dataset unificado de proveedores para el scraper RUP.
- **Salidas:** `proponentes_por_proceso_obra.parquet` (276,770 x 9).
- **Dependencias:** pandas, sodapy.
- **Etapa del pipeline:** 1 (extraccion), 2 (estructuracion).
- **Objetivo especifico que apoya:** OE-01, OE-02.
- **Estado:** implementado.
- **Riesgos detectados:** este notebook alimenta directamente el scraper RUP (`scripts/extraer_rup_auto.py`), que es infraestructura de soporte al modelado predictivo — util tambien para el perfil de proveedores de OE-02/OE-03 de Andres, pero su proposito declarado es "modelado" (celda 8: "Dataset unificado de proveedores para scraper RUP").

### archivo: notebooks/07_depuracion_variables_modelo.ipynb
- **Proposito detectado:** Segun su propio titulo, "Depuracion de Variables **para Modelo Predictivo**". Construye las variables binarias objetivo (`tiempo`, `presupuesto`, `alcance`), analiza correlaciones y elimina columnas de leakage.
- **Funciones principales:** Construccion de targets binarios (celda 4), analisis de correlacion (celda 10), identificacion de columnas de leakage (celda 16), dataset depurado (celda 24).
- **Entradas:** `contratos_adiciones_obra.parquet`.
- **Salidas:** `contratos_depurado_modelo.parquet` (48,331 x 53/42 segun fuente — ver discrepancia en `doc/AUDITORIA_INCONSISTENCIAS.md`).
- **Dependencias:** pandas, numpy.
- **Etapa del pipeline:** 4 (limpieza/ETL), 6 (construccion de targets — version binaria, no la version continua del anteproyecto).
- **Objetivo especifico que apoya:** OE-03 directamente; **no corresponde exactamente** a los indicadores continuos de tiempo/costo/alcance exigidos por el anteproyecto de Andres (numeral 3.3), aunque los nombres de los targets (`tiempo`, `presupuesto`, `alcance`) coinciden conceptualmente con sus tres dimensiones de restriccion de hierro.
- **Estado:** implementado (para fines predictivos).
- **Riesgos detectados:** el titulo y el objetivo del notebook confirman que fue disenado para el modelado supervisado, no para indicadores descriptivos continuos. **POSIBLE FASE DEL COMPANERO en cuanto a proposito, aunque el dataset resultante es reutilizable como base para OE-03.**

### archivo: notebooks/08_integracion_rup_no_consorcios.ipynb
- **Proposito detectado:** Integrar indicadores financieros del RUP (Registro Unico de Proponentes) al dataset de contratos para proveedores no-consorciados.
- **Salidas:** dataset enriquecido con columnas RUP (contribuye al salto 111->125 columnas mencionado en `doc/AUDITORIA_INCONSISTENCIAS.md`).
- **Dependencias:** pandas.
- **Etapa del pipeline:** 2 (estructuracion/enriquecimiento).
- **Objetivo especifico que apoya:** Ninguno del anteproyecto de Andres (los indicadores financieros RUP no se mencionan en su alcance ni objetivos).
- **Estado:** implementado.
- **Riesgos detectados:** **POSIBLE FASE DEL COMPANERO — Verificar autoria.** Este enriquecimiento (indicadores de liquidez, endeudamiento, rentabilidad RUP) esta documentado como feature estructural para el modelo predictivo (`modelo_predictivo_global/docs/01_dataset_y_variables.md`, segun contexto de sesiones previas), sin relacion declarada con el alcance descriptivo.

### archivo: scripts/generar_diccionario_datos.py
- **Proposito detectado:** Genera `data/diccionario_datos.json` cruzando columnas reales de los parquets contra las definiciones oficiales de `dataset.json`.
- **Funciones principales:** Script secuencial (no modularizado en funciones con nombre propio mas alla del bloque principal); diccionario `PARQUETS` mapea cada archivo a su fuente Socrata (lineas 23-40 y siguientes).
- **Entradas:** Todos los `.parquet` del proyecto, `dataset.json`.
- **Salidas:** `data/diccionario_datos.json`.
- **Dependencias:** pandas, numpy, json, pathlib.
- **Etapa del pipeline:** 5 (diccionario de datos).
- **Objetivo especifico que apoya:** OE-03 (instrumento 3.7.3.c del anteproyecto: "Diccionario de datos").
- **Estado:** implementado.
- **Riesgos detectados:** ninguno relevante; es codigo generico reutilizable, no exclusivo del modelado.

### archivo: scripts/generar_diccionario_md.py
- **Proposito detectado:** Convierte `diccionario_datos.json` a Markdown legible (`doc/fase2_comprension_datos/diccionario_datos.md`).
- **Dependencias:** json, pathlib.
- **Etapa del pipeline:** 5 (diccionario de datos).
- **Objetivo especifico que apoya:** OE-03.
- **Estado:** implementado.
- **Riesgos detectados:** ninguno relevante.

### archivo: scripts/extraer_rup_auto.py, scripts/extraer_indicadores_pliegos.py, scripts/poblar_indicadores_pliegos.py, scripts/scraper_pliegos_poc.py, scripts/validar_extraccion_pliegos.py, scripts/gemini/*.py
- **Proposito detectado:** Scraping automatizado de RUP y pliegos SECOP (con CapSolver para reCAPTCHA) y extraccion de indicadores financieros via Gemini.
- **Dependencias:** requests, playwright (via `extractor-indicadores-docker`), google-genai.
- **Etapa del pipeline:** Soporte a estructuracion/enriquecimiento (fuera de las 5 etapas centrales del anteproyecto de Andres).
- **Objetivo especifico que apoya:** Ninguno declarado en el anteproyecto de Andres (RUP, pliegos y consorcios no aparecen en su alcance).
- **Estado:** implementado.
- **Riesgos detectados:** **POSIBLE FASE DEL COMPANERO — Verificar autoria.** Toda esta familia de scripts alimenta exclusivamente el enriquecimiento de features estructurales del modelo predictivo (RUP, consorcios); no hay referencia a ellos en `AnteproyectoAndres.md`.

### archivo: modelo_predictivo_global/chatbot/predictor.py
- **Proposito detectado:** Wrapper de inferencia sobre el modelo LightGBM ganador; replica el pipeline de preprocesamiento (winsorizacion, encoding, imputacion) y calcula SHAP.
- **Funciones principales:** Definicion de `COLS_CRUDAS` (linea 26 y siguientes), rutas `RAIZ`/`DATA`/`IMP`/`MOD` (lineas 21-24).
- **Entradas:** dict crudo de usuario con features de contrato.
- **Salidas:** probabilidades de atraso/sobrecosto + explicacion SHAP.
- **Dependencias:** joblib, numpy, pandas, scikit-learn, lightgbm, shap.
- **Etapa del pipeline:** No corresponde a ninguna de las 5 etapas del anteproyecto de Andres (es inferencia de modelo predictivo).
- **Objetivo especifico que apoya:** Ninguno del anteproyecto de Andres.
- **Estado:** implementado (funcional dentro de `modelo_predictivo_global/`, dado que sus rutas relativas `RAIZ/data/imputers` y `RAIZ/data/modelos` si existen en ese directorio).
- **Riesgos detectados:** **POSIBLE FASE DEL COMPANERO — Verificar autoria.** Ademas, su copia empaquetada en `entregables/08-codigo-fuente/chatbot/predictor.py` no es ejecutable porque `entregables/08-codigo-fuente/chatbot/data/` no existe (los modelos reales estan en `entregables/05-modelos/`), segun confirma `doc/AUDITORIA_INCONSISTENCIAS.md` (item critico 2).

### archivo: modelo_predictivo_global/src/preprocesamiento.py, entrenamiento.py, generar_notebooks_modelos.py
- **Proposito detectado:** Modulos reutilizables de split/escalado/metricas y wrapper de `RandomizedSearchCV`.
- **Dependencias:** scikit-learn (confirmado por grep de imports).
- **Etapa del pipeline:** Modelado predictivo (fuera del alcance de Andres).
- **Estado:** implementado.
- **Riesgos detectados:** **POSIBLE FASE DEL COMPANERO — Verificar autoria.**

### archivo: visualizer/src/hooks/useDuckDB.ts, useDiccionario.ts
- **Proposito detectado:** Cargar parquets y `diccionario_datos.json` en el navegador via DuckDB-WASM para alimentar las vistas de esquema/calidad/distribuciones.
- **Entradas esperadas:** `visualizer/public/data/*.parquet`, `visualizer/public/data/diccionario_datos.json` (fetch en rutas `/data/...`).
- **Estado:** **no funcional** — `visualizer/public/` no existe en el checkout actual (confirmado: no fue listado al explorar `visualizer/src`; ver seccion 11).
- **Riesgos detectados:** Cualquier intento de "levantar el dashboard" para evidencia de tesis fallara con 404 hasta que se sincronicen los datos.

---

## 7. Datasets y almacenamiento

| Archivo / dataset | Ubicacion | Formato | Tamano aprox. | Etapa del pipeline | Fuente inferida | Observaciones |
|---|---|---|---|---|---|---|
| `contratos_electronicos_obra.parquet` | `entregables/04-datasets/` (16.5 MB) | Parquet | 51,353 x 87 | Crudo | API Socrata `jbjy-vk9h` | Fuente madre |
| `procesos_contratacion_obra.parquet` | `entregables/04-datasets/` (35.3 MB) | Parquet | 138,112 x 57 (README dice 59; drift documentado en auditoria previa) | Crudo | API Socrata `p6dx-8zbt` | — |
| `adiciones_obra.parquet` | `entregables/04-datasets/` (12.3 MB) | Parquet | 249,037 x 5 | Crudo | API Socrata `cb9c-h8sn` | — |
| `proveedores_obra.parquet` | `entregables/04-datasets/` (1.8 MB) | Parquet | 13,117 x 25 | Crudo | API Socrata `qmzu-gj57` | — |
| `proveedores_rup.parquet` | `entregables/04-datasets/` (1.6 MB) | Parquet | 28,548 x 22 | Enriquecimiento | Scraping RUP (`scripts/extraer_rup_auto.py`) | Fase de soporte al modelado |
| `proponentes_por_proceso_obra.parquet` | `entregables/04-datasets/` (10.0 MB) | Parquet | 276,770 x 9 | Crudo | API Socrata (proponentes por proceso) | — |
| `contratos_adiciones_obra.parquet` | `entregables/04-datasets/` (17.2 MB) | Parquet | 48,331 x 125 | Intermedio (integrado) | Notebook 05 + 08 | Discrepancia de columnas documentada (111 vs 125) |
| `contratos_depurado_modelo.parquet` | `entregables/04-datasets/` (1.9 MB) | Parquet | 48,331 x 53 | Depurado v1 | Notebook 07 | Targets binarios `tiempo`/`presupuesto`/`alcance` |
| `consolidado_global.parquet` | `entregables/04-datasets/`, `modelo_predictivo_global/data/` (2.5 MB) | Parquet | 48,331 x 55 | Depurado v2 | Integracion + variables estructurales | Fase del companero |
| `consolidado_imputado.parquet` | `entregables/04-datasets/`, `modelo_predictivo_global/data/` (1.9 MB) | Parquet | 48,331 x 154 | Final para modelado | Preprocesamiento notebook 02 de `modelo_predictivo_global` | Fase del companero |
| `data/diccionario_datos.json` | `data/` (202 KB) | JSON | — | Diccionario de datos | `scripts/generar_diccionario_datos.py` | Reutilizable para OE-03 |
| Datasets de `modelo-predictivo-preliminar/` (X_train, X_test, etc.) | `modelo-predictivo-preliminar/data/` | Parquet | Varios (0.5-1.2 MB c/u) | Splits de modelado | Fase del companero | No relevante para OE-01 a OE-04 |
| Datasets de `modelo-predictivo-preliminar/consorcios/data/` | idem | Parquet | Varios | Sub-sprint consorcios | Fase del companero | No relevante |

**Modelo estrella materializado:** No. No se encontro ningun archivo `.sql`, definicion de esquema dimensional, ni motor de base de datos (SQLite/DuckDB/PostgreSQL) que materialice una tabla de hechos con dimensiones. La "estructuracion" existente es una serie de joins de pandas persistidos como archivos Parquet planos.

**Motor de almacenamiento real:** Archivos Parquet planos via `pandas.to_parquet`/`read_parquet`. DuckDB-WASM se usa unicamente en el frontend (`visualizer/`), no como motor de persistencia del pipeline Python.

**Ausencia de motor de almacenamiento explicito:** Confirmada. Ni el anteproyecto ni el codigo definen un motor fisico (PostgreSQL, SQLite, DuckDB nativo) para el modelo estrella propuesto en OE-02.

---

## 8. Extraccion desde SECOP

- **¿Se usa API Socrata/OData?** Si. Confirmado via `sodapy>=2.2` en `requirements.txt` y uso en `notebooks/00` a `06` (celdas de configuracion con `Socrata(...)`, segun `doc/contexto/CONTEXTO.md` seccion 5 "Lecciones tecnicas sobre la API Socrata").
- **¿Se usan consultas SoQL?** Si, documentado en `doc/contexto/CONTEXTO.md` ("SoQL NO soporta backticks para nombres de campos") y en `plan-trabajo-dirigido.md`.
- **¿Hay paginacion?** Si, para `adiciones` (notebook 03) y `proponentes_por_proceso` (notebook 06) se usa descarga por lotes de IDs (`WHERE IN`), segun sus celdas markdown ("Descarga filtrada desde la API", "Descarga por lotes").
- **¿Hay manejo de errores/reintentos?** Documentado como recomendacion en `CONTEXTO.md` ("Implementar reintentos con backoff exponencial"), pero **no verificable en el codigo estatico de los notebooks** sin ejecutar celda por celda; no se encontro un modulo Python separado con logica de retry explicita (`tenacity` solo aparece en `extractor-indicadores-docker/requirements.txt`, ajeno a la extraccion SECOP base).
- **¿Hay logs de ejecucion?** No se encontraron archivos de log persistentes para la fase de extraccion base (`notebooks/00-06`). `extractor-indicadores-docker/src/logger.py` si implementa logging, pero es exclusivo del pipeline de indicadores RUP/pliegos.
- **¿Se documenta el conjunto de datos consultado (IDs en datos.gov.co)?** Si, en `dataset.json` y `doc/contexto/CONTEXTO.md` (tabla seccion 2.1: `jbjy-vk9h`, `p6dx-8zbt`, `cb9c-h8sn`, `qmzu-gj57`).
- **¿Hay parametros de fecha (2018-2024)?** No verificado directamente en el codigo de los notebooks (analisis estatico no confirmo un filtro `WHERE fecha_de_firma BETWEEN ...` explicito); el anteproyecto de Andres exige este filtro (numeral 1.2 delimitacion) pero no se encontro evidencia de que el codigo actual lo aplique — **No verificable / posible ausencia**.
- **¿Se extraen procesos, contratos y proveedores?** Si, los tres (mas adiciones y proponentes), confirmado por los notebooks 01, 02, 03, 04, 06.
- **¿Se guarda evidencia de trazabilidad?** Parcial: las celdas markdown de cada notebook documentan hallazgos y decisiones, pero no hay logs tecnicos (timestamps de ejecucion, parametros exactos de consulta) persistidos fuera del propio notebook.
- **Riesgos y recomendaciones:** Falta un script de extraccion parametrizable y reutilizable fuera de Jupyter; falta filtro temporal 2018-2024 explicito y verificable; falta logging tecnico dedicado. Se recomienda extraer la logica de conexion Socrata de los notebooks a un modulo `.py` con manejo de reintentos y logs, y anadir explicitamente el filtro de fecha exigido por el anteproyecto.

---

## 9. ETL y calidad de datos

- **Reglas de limpieza detectadas:** tratamiento de sentinelas `"No Definido"` como NULL (notebook 03, celda 13; documentado tambien en `CONTEXTO.md` seccion "Sentineles"); casting de campos numericos que llegan como texto desde la API (`CONTEXTO.md`: "Todos los campos numericos llegan como texto").
- **Deduplicacion:** detectada en analisis (notebook 01: 3,022 duplicados en `id_contrato`; notebook 02: 25,221 duplicados en `id_del_proceso`; notebook 03: 105,836 duplicados en `identificador`; notebook 04: 499 duplicados), pero **no se verifico en el codigo estatico si el tratamiento final (eliminacion) se aplica de forma explicita y documentada con el criterio "conservar el mas completo/reciente"** que exige el anteproyecto (numeral 3.6.5).
- **Imputacion de nulos:** No se encontro imputacion en la fase base (notebooks 00-08) mas alla del tratamiento de sentinelas. La imputacion por mediana + flags `_was_nan` esta implementada en `modelo_predictivo_global/notebooks/02_preprocesamiento.ipynb` (fase del companero, confirmado por `modelo_predictivo_global/data/imputers/imputer_mediana.pkl`), no en el pipeline descriptivo de Andres.
- **Tipificacion / casting:** Confirmado en notebook 02 (seccion "5.1 Conversion de tipos") y notebook 08 (seccion 3, "rup_ingresos y rup_utilidad_neta vienen como string").
- **Manejo de outliers:** Winsorizacion (p1/p99) implementada en `modelo_predictivo_global/data/imputers/winsor_limits.pkl` — **fase del companero**. En el pipeline base (notebooks 00-08), el manejo de outliers se limita a deteccion visual con box plots, sin una regla de tratamiento cuantitativa documentada en codigo.
- **Estandarizacion de nombres, entidades, territorios:** Parcial; se documenta normalizacion de nombres de campos Socrata (`CONTEXTO.md`: "Socrata normaliza nombres, ej. Id contrato -> id_contrato"), pero no se encontro un modulo de estandarizacion de nombres de entidades/territorios (p. ej. unificacion de nombres de municipios con variantes de escritura).
- **Diccionario de datos:** Existe. `data/diccionario_datos.json` + `doc/fase2_comprension_datos/diccionario_datos.md`, generado por `scripts/generar_diccionario_datos.py`/`generar_diccionario_md.py`. Cumple directamente el instrumento 3.7.3.c del anteproyecto.
- **Umbrales cuantitativos de calidad:** No existen. Ni el anteproyecto ni el codigo definen un umbral minimo de completitud/calidad aceptable (ver tambien seccion 21 de `RESUMEN_CONTROL.md`).
- **Reportes de calidad de datos:** Existen de forma narrativa dentro de las celdas markdown de cada notebook ("Resumen de problemas de calidad detectados") y en `doc/fase2_comprension_datos/INFORME_FASE2_COMPRENSION_DATOS.md`, pero no como un reporte automatizado/reproducible (p. ej. un `pandas-profiling` o `great_expectations` persistido). No se detecto `pandas-profiling` importado en ningun `.py`/`.ipynb` pese a mencionarse en `requirements.txt` de otro proyecto relacionado (no en este `requirements.txt` raiz).

---

## 10. Indicadores calculados

| Indicador | Archivo donde se calcula | Formula detectada | Objetivo relacionado | Estado |
|---|---|---|---|---|
| `tiempo` (target binario, equivalente conceptual a "desviacion de tiempo") | `notebooks/07_depuracion_variables_modelo.ipynb`, celda 4 | Binarizacion (No verificable la formula exacta sin ejecutar el notebook; documentado como derivado de `dias_adicionados`/extension de plazo segun `doc/contexto/CONTEXTO.md` seccion 4.3: `tiene_extension = dias_adicionados > 0`) | Corresponde conceptualmente a la dimension "tiempo" de la restriccion de hierro, pero como flag binario, no como magnitud continua | Implementado como binario; **no coincide con la definicion continua exigida por el anteproyecto** (numeral 3.3: "diferencia entre plazo pactado y plazo real") |
| `presupuesto` (target binario, equivalente a "desviacion de costo") | `notebooks/07_depuracion_variables_modelo.ipynb` | Binarizacion de `sobrecosto_ratio` (formula documentada en `CONTEXTO.md` 4.3: `(valor_pagado - valor_del_contrato) / valor_del_contrato`) | Corresponde a la dimension "costo", pero como flag binario | Implementado como binario; el anteproyecto exige la razon continua ("expresada como porcentaje de adicion presupuestal") |
| `alcance` (target binario, prevalencia 3.5%/96.5% segun `doc/AUDITORIA_INCONSISTENCIAS.md`) | `notebooks/07_depuracion_variables_modelo.ipynb` | No verificable la formula exacta sin ejecutar el notebook (probable a partir de `liquidacion`/`estado_contrato`) | Corresponde a la dimension "alcance", como flag binario | Implementado como binario; el anteproyecto exige un indicador categorico (entregado en su totalidad / parcialmente / no entregado), mas granular que un binario |
| `tuvo_atraso` / `tuvo_sobrecosto` | `entregables/04-datasets/README.md` (formula documentada: `tuvo_atraso = (tiempo == 1)`, `tuvo_sobrecosto = (presupuesto == 1)`) | Renombre directo de `tiempo`/`presupuesto` | Targets de clasificacion del modelo predictivo — **no corresponden al anteproyecto de Andres** | Implementado — fase del companero |
| Desviacion de tiempo continua (dias) | No encontrado en ningun notebook/script | — | OE-04 / numeral 3.3 del anteproyecto | **No implementado** |
| Desviacion de costo continua (% adicion) | No encontrado como indicador independiente reportado (solo como base del target binario) | — | OE-04 / numeral 3.3 | **Parcial**: existe la logica de calculo del ratio como paso intermedio, pero no se reporta ni visualiza como indicador continuo final |
| Indice de cumplimiento de alcance (categorico) | No encontrado | — | OE-04 / numeral 3.3 | **No implementado** |

---

## 11. Visualizacion y dashboard

- **Framework usado:** Next.js 16 / React 19 / Recharts / Tailwind (`visualizer/package.json`). No se encontro Dash, Plotly ni Streamlit en ningun modulo orientado al alcance descriptivo (Streamlit solo existe en el chatbot predictivo, `modelo_predictivo_global/chatbot/app.py`).
- **Archivos del dashboard:** `visualizer/src/app/page.tsx`, `dataset/[slug]/page.tsx`, `esquema/page.tsx`, `sentinelas/page.tsx`; componentes `ColumnTable.tsx`, `DatasetDetail.tsx`, `DistributionsTab.tsx`, `PreviewTab.tsx`, `QualityTab.tsx`, `RelationalDiagram.tsx`, `SentinelContent.tsx`, `Sidebar.tsx`.
- **Componentes detectados:** Tabla de columnas, pestana de distribuciones (`DistributionsTab.tsx`), pestana de calidad (`QualityTab.tsx`), diagrama relacional (`RelationalDiagram.tsx`), vista de valores centinela/sentinelas (`SentinelContent.tsx`). No se detectaron mapas coropleticos ni box plots interactivos especificos en los nombres de archivo (**no verificable el contenido interno de cada `.tsx` sin lectura linea por linea, no realizada por estar fuera del stack Python/notebooks priorizado en esta auditoria**).
- **Interactividad real vs estatica:** Basada en DuckDB-WASM (consulta interactiva de parquets en el navegador), por lo que **seria interactiva si los datos estuvieran disponibles**.
- **¿Se puede levantar localmente?** Comando detectado: `npm run dev` (`visualizer/package.json`, script `"dev": "next dev"`). **No funcional en el estado actual**: `visualizer/src/hooks/useDuckDB.ts` y `useDiccionario.ts` hacen `fetch("/data/...")` contra `visualizer/public/data/`, carpeta que no existe en este checkout (confirmado por ausencia en el arbol de `visualizer/`; hallazgo tambien reportado como critico en `doc/AUDITORIA_INCONSISTENCIAS.md`).
- **Capturas o assets guardados:** No se encontraron capturas de pantalla del `visualizer/` en `visualizer/` ni en `report/imagenes/` (esa carpeta contiene graficos del modelado predictivo: ROC, matrices de confusion, importancia de variables).
- **Estado:** **no funcional** (roto por datos faltantes) y **no corresponde al stack tecnologico exigido por el anteproyecto** (Dash/Plotly). No existe ningun dashboard Dash/Plotly/Streamlit implementado para el alcance descriptivo de Andres.

---

## 12. Codigo relacionado con modelado predictivo (ALERTA)

Se detecto codigo predictivo extenso. Lista de archivos con `import`/`from` de `sklearn`, `xgboost`, `lightgbm` o `statsmodels` (55 coincidencias totales via grep):

| Archivo | Tipo de uso |
|---|---|
| `modelo_predictivo_global/src/preprocesamiento.py` | Split, escalado, metricas — **POSIBLE FASE DEL COMPANERO — Verificar autoria y separar del alcance descriptivo.** |
| `modelo_predictivo_global/src/entrenamiento.py` | Wrapper de `RandomizedSearchCV` — **POSIBLE FASE DEL COMPANERO.** |
| `modelo_predictivo_global/src/generar_notebooks_modelos.py` | Generador automatico de notebooks de modelado — **POSIBLE FASE DEL COMPANERO.** |
| `modelo_predictivo_global/chatbot/predictor.py` | Inferencia con LightGBM + SHAP — **POSIBLE FASE DEL COMPANERO.** |
| `modelo-predictivo-preliminar/consorcios/src/entrenamiento.py`, `generar_notebooks_modelos.py`, `preprocesamiento.py` | Sub-sprint consorcios (modelado) — **POSIBLE FASE DEL COMPANERO.** |
| `modelo-predictivo-preliminar/tuning/src/comun.py`, `generar_notebooks.py` | Sub-sprint de tuning de hiperparametros — **POSIBLE FASE DEL COMPANERO.** |
| `entregables/08-codigo-fuente/modulos-python/preprocesamiento.py`, `entrenamiento.py`, `generar_notebooks_modelos.py` | Copias empaquetadas de los modulos anteriores — **POSIBLE FASE DEL COMPANERO.** |
| `entregables/08-codigo-fuente/chatbot/predictor.py` | Copia empaquetada de `predictor.py` — **POSIBLE FASE DEL COMPANERO.** |

Adicionalmente, `notebooks/07_depuracion_variables_modelo.ipynb` (dentro del pipeline "base") tiene en su propio titulo la frase "para Modelo Predictivo" y produce los targets que alimentan directamente el modelado — se marca como **POSIBLE FASE DEL COMPANERO en cuanto a proposito**, aunque fisicamente resida fuera de las carpetas `modelo*`.

Se detectaron ademas notebooks de modelado (fuera del pipeline base) con nombres explicitos: `modelo_predictivo_global/notebooks/04_modelo_lr.ipynb` a `11_modelo_mlp.ipynb`, `12_comparativa_final.ipynb`; `modelo-predictivo-preliminar/notebooks/*` (varios); `modelo-predictivo-preliminar/consorcios/notebooks/*`; `modelo-predictivo-preliminar/tuning/notebooks/*`; y sus copias en `entregables/07-notebooks/modelado-v1/` y `modelado-v2/`. Todos corresponden a entrenamiento y evaluacion de modelos supervisados (metricas AUC-ROC, F1, matrices de confusion segun `report/imagenes/`).

**Riesgo academico de incluir esto en la tesis descriptiva:** Si Andres Telles presenta como evidencia propia cualquiera de estos modulos o notebooks (modelado_predictivo_global, modelo-predictivo-preliminar, entregables/05-modelos, entregables/07-notebooks/modelado-v1 y v2, entregables/08-codigo-fuente, extractor-indicadores-docker, report/), incurriria en una atribucion incorrecta de autoria que puede ser detectada facilmente por un jurado (los nombres de carpeta, los README internos y los documentos `doc/contexto/plan-trabajo-dirigido.md`/`tabla_fases_trabajo_dirigido.md` declaran explicitamente que este codigo responde a un objetivo predictivo con metodologia CRISP-DM, distinto del objetivo general descriptivo-analitico de su propio anteproyecto). Se recomienda excluir estas carpetas del entregable de Andres y, si su tutor confirma coautoria compartida en la fase de extraccion (notebooks 00-08), documentar explicitamente cual porcion es aporte propio y cual es insumo compartido.

**Conclusion de la seccion:** Si se detecto codigo predictivo extenso, concentrado casi en su totalidad en `modelo_predictivo_global/`, `modelo-predictivo-preliminar/`, sus copias en `entregables/`, y el pipeline de indicadores RUP (`extractor-indicadores-docker/`, `scripts/gemini/`, `scripts/extraer_rup_auto.py`, `scripts/extraer_indicadores_pliegos.py`). Ningun archivo de estas rutas debe considerarse evidencia de cumplimiento del anteproyecto descriptivo de Andres.

---

## 13. Reproducibilidad

- **README presente:** No en la raiz. Parcial en subcarpetas (chatbot, entregables, modelo_predictivo_global, modelo-predictivo-preliminar, extractor-indicadores-docker, visualizer — este ultimo es boilerplate segun auditoria previa).
- **Instrucciones de instalacion:** Ausentes para el pipeline base (notebooks 00-08); presentes mas completas para el chatbot y el pipeline Docker de indicadores (fase del companero).
- **Instrucciones de ejecucion:** Ausentes para el pipeline base; presentes para `extractor-indicadores-docker` (`docker-compose.yml`, `DEPLOY_SERVER.md`, `OPERACION.md`).
- **Semillas aleatorias fijadas:** No aplica al pipeline base (no hay componente estocastico en extraccion/ETL descriptivo). En el modelado predictivo si se documenta `random_state=42` (fase del companero, no verificado por esta auditoria en detalle por estar fuera de alcance).
- **Datos versionados o descargables:** Parcial. Los datasets crudos e intermedios del pipeline base (`data/*.parquet`) estan excluidos de git; solo los datasets finales de `entregables/04-datasets/` y los del modelado (`modelo_predictivo_global/data/`, `modelo-predictivo-preliminar/data/`) se versionan explicitamente via excepciones en `.gitignore`.
- **Notebooks reproducibles:** No verificable sin ejecutarlos (regla de "no ejecutar codigo" de esta auditoria). Estructuralmente estan completos (celdas de codigo y markdown en orden logico), pero dependen de acceso en vivo a la API Socrata para regenerar los datasets crudos, ya que estos no estan versionados.

---

## 14. Deuda tecnica y riesgos detectados

| Riesgo | Ubicacion | Severidad | Impacto en la tesis | Recomendacion |
|---|---|---|---|---|
| Ausencia de README raiz con instrucciones de instalacion/ejecucion del pipeline base | Raiz del repositorio | Alta | Dificulta que un jurado reproduzca la extraccion/ETL de Andres | Crear `README.md` raiz con pasos de instalacion (`pip install -r requirements.txt`), configuracion de `.env` y orden de ejecucion de notebooks 00-08 |
| Motor de almacenamiento / modelo estrella no definido ni materializado | Todo el pipeline (solo parquets planos) | Alta | OE-02 exige explicitamente un "modelo de datos analitico" con "reglas de integracion"; actualmente es solo un conjunto de joins de pandas sin esquema formal | Definir y documentar un motor real (DuckDB, SQLite o esquema Parquet particionado) con tabla de hechos y dimensiones explicitas |
| Indicadores de tiempo/costo/alcance implementados como binarios, no como magnitudes continuas/categoricas segun el anteproyecto | `notebooks/07_depuracion_variables_modelo.ipynb` | Alta | El numeral 3.3 del anteproyecto exige indicadores continuos/categoricos; el codigo actual solo produce flags de clasificacion | Derivar indicadores continuos (dias de desviacion, % de adicion, categoria de alcance) a partir de las mismas columnas base ya integradas |
| Codigo predictivo mezclado en el mismo repositorio sin separacion de carpetas por autor/tesis | `modelo_predictivo_global/`, `modelo-predictivo-preliminar/`, `entregables/`, `extractor-indicadores-docker/`, `report/` | Alta | Riesgo de atribucion incorrecta de autoria ante el jurado | Separar en repositorios o carpetas claramente delimitadas por autor; documentar coautoria de la fase compartida (notebooks 00-08) |
| Dashboard `visualizer/` no funcional (datos faltantes) | `visualizer/public/data/` (inexistente) | Alta | Sin evidencia de visualizacion funcional para OE-04 | Sincronizar `entregables/04-datasets/*.parquet` y `diccionario_datos.json` hacia `visualizer/public/data/`, o construir el dashboard Dash/Plotly que exige el anteproyecto |
| Inconsistencia de stack tecnologico: anteproyecto exige Dash/Plotly (o Streamlit/Plotly); el unico dashboard construido usa Next.js/React | `visualizer/` vs `AnteproyectoAndres.md` (2.2.5, 3.7.4.b) | Media | Genera expectativa incumplida ante el jurado si no se aclara el cambio de tecnologia | Decidir y documentar explicitamente si se migra a Dash/Plotly o se justifica el cambio a Next.js en el documento final |
| Ausencia de umbrales cuantitativos de calidad de datos | Todo el pipeline | Media | Dificulta demostrar objetivamente el cumplimiento de OE-03 | Definir umbrales explicitos (p. ej. % maximo de nulidad aceptable, % minimo de cobertura de joins) y verificarlos en codigo |
| Falta de logs de ejecucion / trazabilidad tecnica en la extraccion | `notebooks/00-06` | Media | Afecta el criterio de "trazabilidad" exigido en 3.7.6 del anteproyecto | Anadir logging (timestamps, parametros de consulta, conteo de registros) persistido en archivo, no solo en celdas markdown |
| Discrepancias de conteo de columnas entre documentacion y datasets reales (111 vs 125 en `contratos_adiciones_obra.parquet`; 57 vs 59 en `procesos_contratacion_obra.parquet`) | `doc/fase2_comprension_datos/diccionario_datos.md` vs `entregables/04-datasets/*.parquet` | Media | Reduce la confiabilidad del diccionario de datos como evidencia de OE-03 | Regenerar el diccionario de datos ejecutando `scripts/generar_diccionario_datos.py` contra los parquets vigentes |
| Datasets crudos e intermedios no versionados (`data/*.parquet` gitignored) | `.gitignore`, `data/` | Media | Sin acceso a la API en vivo, no se puede regenerar el dataset desde cero | Documentar explicitamente la dependencia de la API en vivo, o versionar copias reducidas de los datasets crudos para fines de reproducibilidad academica |
| Codigo suelto sin referencias claras (`scrapper.html`) | Raiz del repositorio | Baja | Ambiguedad sobre su proposito | Confirmar con el autor si es un artefacto util o descartable |
| No se detectaron credenciales expuestas | `.env.example` (solo placeholders), `.gitignore` excluye `.env` | Baja (verificado, no es un riesgo activo) | — | Mantener la practica actual |
| Hard-coding de rutas absolutas | No se detecto en los archivos revisados (los scripts usan `Path(__file__).resolve()` de forma relativa, ej. `predictor.py` linea 21) | Baja | — | Mantener la practica actual |

---

## 15. Relacion preliminar entre codigo y objetivos del anteproyecto

| Objetivo especifico | Requisito derivado | Archivos que lo respaldan | Evidencia tecnica | Estado | Observaciones |
|---|---|---|---|---|---|
| OE-01 (Extraccion automatizada SECOP, trazabilidad y reproducibilidad) | Script/notebook de extraccion via API Socrata con parametros documentados | `notebooks/00_definicion_tabla_base.ipynb` a `06_proponentes_por_proceso.ipynb`, `dataset.json` | Uso confirmado de `sodapy`/API Socrata; descarga filtrada por `tipo_de_contrato = "Obra"`; paginacion por lotes en notebooks 03 y 06 | **Parcial** | La extraccion existe y funciona conceptualmente, pero fue construida para el modelado predictivo del companero (`CONTEXTO.md` linea 10); falta filtro de fecha 2018-2024 verificable, logs persistentes y un script reutilizable fuera de Jupyter |
| OE-02 (Modelo de datos analitico / integracion procesos-contratos-proveedores) | Integracion formal con reglas de relacionamiento consistente (modelo estrella) | `notebooks/05_integracion_contratos_adiciones.ipynb`, `08_integracion_rup_no_consorcios.ipynb`, `entregables/04-datasets/contratos_adiciones_obra.parquet` | Joins por `id_del_portafolio`, `codigo_proveedor`, `id_contrato` documentados y con coberturas medidas (99.9%, 54.4%, 69.2%) | **Parcial** | Existe integracion de datos, pero no un "modelo estrella" formal (sin tabla de hechos/dimensiones materializada); ademas incorpora enriquecimiento RUP ajeno al alcance de Andres |
| OE-03 (Normalizacion: duplicados, nulos, inconsistencias, tipificacion) | Pipeline de limpieza documentado con diccionario de datos | `notebooks/01,02,07`, `scripts/generar_diccionario_datos.py`, `scripts/generar_diccionario_md.py`, `data/diccionario_datos.json` | Deteccion de duplicados y sentinelas documentada; diccionario de datos generado automaticamente | **Parcial** | Deteccion de problemas de calidad si existe; tratamiento final (deduplicacion efectiva) y umbrales cuantitativos de calidad no verificados/ausentes |
| OE-04 (Visualizaciones y tableros interactivos: distribuciones, box plots, segmentaciones) | Dashboard interactivo Dash/Plotly (o Streamlit/Plotly) con box plots, distribuciones y segmentaciones por modalidad/entidad/territorio | `visualizer/` (Next.js/React), box plots en `notebooks/01,02,05` | Box plots confirmados solo dentro de notebooks EDA del companero; `visualizer/` no usa Dash/Plotly y esta actualmente no funcional (datos faltantes en `public/data/`) | **No cumple** | Ningun artefacto satisface simultaneamente el stack exigido y el estado funcional; se requiere construir el dashboard desde cero o reformular el requisito tecnologico |

---

## 16. Funcionalidades implementadas no previstas en el anteproyecto

- **Modelado predictivo completo (8 algoritmos, LightGBM ganador, SHAP)** — `modelo_predictivo_global/`, `modelo-predictivo-preliminar/`. Corresponde a otra fase (companero); no enriquece el alcance descriptivo de Andres, debe documentarse aparte o excluirse del entregable.
- **Chatbot RAG con Gemini (Streamlit)** — `modelo_predictivo_global/chatbot/`. Corresponde a otra fase (companero, Fase IV de `tabla_fases_trabajo_dirigido.md`).
- **Pipeline Docker de extraccion de indicadores financieros RUP via scraping + Gemini** — `extractor-indicadores-docker/`, `scripts/gemini/*`. Corresponde a otra fase (companero); util solo si Andres decide incorporar variables financieras de proveedor, lo cual no esta en su anteproyecto.
- **Visualizador Next.js de esquema/calidad/distribuciones de datos** — `visualizer/`. No previsto en el anteproyecto (que exige Dash/Plotly); podria enriquecer el proyecto de Andres si se repara y se documenta el cambio de stack, o debe descartarse/reemplazarse si se exige fidelidad estricta al anteproyecto.
- **Analisis y modelado especifico de consorcios/uniones temporales** — `modelo-predictivo-preliminar/consorcios/`. Relacionado con la hipotesis H2 del anteproyecto de Andres (consorcios vs personas juridicas), pero implementado con fines predictivos, no descriptivos; podria reutilizarse parcialmente para el analisis descriptivo de esa hipotesis.
- **Informes formales tipo tesis (PRIMER-INFORME, SEGUNDO-INFORME, INFORME-FINAL, anexos, `main.tex`)** — `report/`. Corresponde al documento final del companero; no debe confundirse con el documento de Andres.

---

## 17. Funcionalidades del anteproyecto no implementadas

| Elemento prometido | Impacto en la tesis | Prioridad de implementacion | Alternativa |
|---|---|---|---|
| Indicadores continuos de desviacion de tiempo (dias) y costo (% adicion) | Alto — es el nucleo del marco teorico (restriccion de hierro) | Alta | Derivar directamente de columnas ya integradas (`contratos_adiciones_obra.parquet`) sin necesidad de nueva extraccion |
| Indice de cumplimiento de alcance categorico (entregado/parcial/no entregado) | Alto | Alta | Definir la regla de negocio explicita (posiblemente a partir de `estado_contrato`/`liquidacion`) y documentarla en un nuevo notebook |
| Dashboard Dash/Plotly (o Streamlit/Plotly) interactivo con filtros dinamicos y mapas coropleticos | Alto — es el entregable central de OE-04 | Alta | Construir un dashboard nuevo en el stack exigido, reutilizando los parquets de `entregables/04-datasets/`; o formalizar y justificar el uso de Next.js/Recharts como alternativa documentada |
| Modelo estrella formal (tabla de hechos + dimensiones) | Medio-Alto — exigido explicitamente en OE-02 | Media | Documentar un esquema dimensional explicito (aunque sea materializado como Parquet particionado o SQLite) a partir de los joins ya existentes |
| Umbrales cuantitativos de calidad de datos | Medio | Media | Definir metricas objetivo (p. ej. % maximo de nulidad, % minimo de cobertura) y verificarlas programaticamente |
| Filtro temporal explicito 2018-2024 | Medio | Media | Anadir el filtro en la consulta SoQL o como paso de limpieza posterior, y documentarlo |
| Logs tecnicos de extraccion (trazabilidad, numeral 3.7.6) | Medio | Media | Anadir logging basico (timestamps, conteo de registros, parametros de consulta) a un script de extraccion dedicado |
| README raiz con instrucciones de instalacion/ejecucion | Medio | Alta (bajo costo, alto retorno) | Redactar un README que cubra el flujo completo del alcance descriptivo |
| Segmentaciones por modalidad/entidad/territorio en visualizaciones finales | Medio | Media | Puede construirse sobre los datos ya integrados una vez exista el dashboard |

---

## 18. Evidencias que deberian capturarse para la tesis

- Capturas del dashboard descriptivo funcionando (una vez construido/reparado), con filtros por modalidad/entidad/territorio.
- Diagrama del modelo estrella (tabla de hechos contratos + dimensiones proceso/proveedor/entidad), aunque sea conceptual si no se materializa en un motor de BD.
- Diccionario de datos exportado y actualizado (`doc/fase2_comprension_datos/diccionario_datos.md` regenerado contra los parquets vigentes).
- Reporte de calidad de datos con cifras de nulidad, duplicados y cobertura de joins (ya existen cifras narrativas en `CONTEXTO.md`; formalizarlas en un reporte reproducible).
- Logs de extraccion (timestamps, cantidad de registros descargados, parametros de consulta SoQL usados).
- Tabla comparativa de los tres indicadores (tiempo, costo, alcance) una vez implementados en su forma continua/categorica, segmentada por modalidad de contratacion.
- Ejemplos concretos de outliers detectados (valores de contrato extremos, duraciones absurdas — ya mencionados narrativamente en `CONTEXTO.md`: "max $11 cuatrillones", "max 27M dias").
- Box plots por modalidad de contratacion (ya existe codigo reutilizable en `notebooks/01,02,05`; adaptar para el reporte final).
- Mapas coropleticos por departamento/territorio (no implementados aun; requieren el dashboard final).
- README raiz con instrucciones de instalacion y ejecucion.
- Ejemplo de dataset crudo, intermedio y depurado (usar `entregables/04-datasets/contratos_electronicos_obra.parquet` -> `contratos_adiciones_obra.parquet` -> `contratos_depurado_modelo.parquet` como cadena de evidencia).

---

## 19. Preguntas criticas para el autor

- ¿Que motor de almacenamiento se usara realmente para el "modelo estrella" exigido en OE-02, dado que actualmente todo son parquets planos sin esquema dimensional formal?
- ¿El pipeline de extraccion e integracion de datos (notebooks 00-08, `scripts/generar_diccionario_datos.py`) es trabajo compartido con el companero de modelado predictivo, o corresponde exclusivamente a otro autor? `doc/contexto/CONTEXTO.md` y `plan-trabajo-dirigido.md` lo documentan como parte del trabajo predictivo — ¿hay coautoria formal reconocida por el director?
- ¿Que notebooks/carpetas corresponden estrictamente a la fase descriptiva de Andres? Segun esta auditoria, ninguno de los notebooks o modulos actuales fue disenado especificamente para el enfoque descriptivo de restriccion de hierro; se requiere confirmacion explicita del autor sobre que planea construir de cero.
- ¿Los datasets de `entregables/04-datasets/` estan descargados de forma definitiva, o se re-descargan bajo demanda contra la API en vivo? Esto determina si son reproducibles sin conexion a datos.gov.co.
- ¿Que version del dashboard es la definitiva: el `visualizer/` Next.js (actualmente roto) o se construira un Dash/Plotly nuevo segun lo exige el anteproyecto?
- ¿Hay ramas git relevantes? El repositorio actual solo tiene `main` con 2 commits del mismo autor; ¿existe un repositorio separado o rama del companero con el codigo predictivo que deberia excluirse de este entregable?
- ¿Los indicadores binarios `tiempo`/`presupuesto`/`alcance` de `notebooks/07_depuracion_variables_modelo.ipynb` pueden reutilizarse como base para derivar los indicadores continuos/categoricos que exige el anteproyecto, o deben construirse independientemente para evitar cualquier confusion de autoria con el modelo predictivo?
- ¿Hay experimentos o carpetas completas (`modelo_predictivo_global/`, `modelo-predictivo-preliminar/`, `extractor-indicadores-docker/`, `report/`, `entregables/05 a 11`) que deban excluirse explicitamente del repositorio que se entregue como evidencia de este trabajo de grado especifico?

---

## 20. Version ultracompacta del codigo

**Stack real:** Python 3.12.10, pandas, sodapy (API Socrata), matplotlib/seaborn para EDA. Sin Dash, sin Plotly, sin motor de base de datos formal. El unico dashboard construido (`visualizer/`) usa Next.js/React/DuckDB-WASM/Recharts, no coincide con el stack exigido por el anteproyecto (Dash/Plotly o Streamlit/Plotly) y actualmente esta roto por falta de datos en `public/data/`.

**Estructura resumida:** `notebooks/00-08` (extraccion + integracion + depuracion, 9 notebooks) y `scripts/` (diccionario de datos + scraping RUP/pliegos) forman el pipeline de datos base. Todo el resto del repositorio (`modelo_predictivo_global/`, `modelo-predictivo-preliminar/`, `extractor-indicadores-docker/`, `entregables/05 a 11`, `report/`) implementa un proyecto DISTINTO: modelado predictivo con metodologia CRISP-DM (Random Forest, XGBoost, LightGBM ganador) mas un chatbot RAG con Gemini/Streamlit, segun documentan explicitamente `doc/contexto/CONTEXTO.md` y `doc/contexto/plan-trabajo-dirigido.md`.

**Etapas del pipeline efectivamente implementadas (para el alcance descriptivo de Andres):** extraccion via API Socrata (parcial, sin filtro de fecha verificado ni logs persistentes); integracion de contratos+adiciones+proveedores+RUP (parcial, sin modelo estrella formal); limpieza/tipificacion basica y diccionario de datos (parcial); deteccion de duplicados y sentinelas (si, a nivel de analisis).

**Etapas ausentes:** indicadores continuos de tiempo/costo/alcance segun restriccion de hierro; dashboard Dash/Plotly funcional; modelo estrella materializado; umbrales cuantitativos de calidad; README raiz con instrucciones.

**Codigo predictivo:** presente y extenso (55 referencias a sklearn/xgboost/lightgbm/statsmodels en 13 archivos), concentrado en `modelo_predictivo_global/`, `modelo-predictivo-preliminar/` y sus copias en `entregables/`. Debe tratarse como fase del companero y excluirse del entregable descriptivo de Andres.

**Estado de reproducibilidad:** Bajo-medio. Sin README raiz, sin logs, con datasets crudos no versionados (dependientes de la API en vivo), pero con requirements.txt claro para el pipeline base.

**Principales riesgos tecnicos:** (1) todo el codigo base fue disenado para un objetivo predictivo distinto al de Andres; (2) OE-04 no tiene ningun artefacto funcional que cumpla el stack exigido; (3) los indicadores calculados son binarios de clasificacion, no las magnitudes continuas/categoricas del anteproyecto; (4) ausencia de modelo estrella formal; (5) riesgo alto de mezclar codigo del companero como evidencia propia.

**Recomendacion general:** antes de redactar el capitulo de desarrollo tecnico, Andres debe decidir junto al director que porcion del pipeline base (notebooks 00-08) reclama como aporte propio o compartido, construir desde cero los indicadores continuos y el dashboard Dash/Plotly, y excluir explicitamente del entregable todo lo relacionado con modelado predictivo, chatbot RAG y extraccion de indicadores RUP.

---

## 21. Checklist de siguientes pasos

- [ ] Validar RESUMEN_CODIGO.md manualmente.
- [ ] Confirmar autoria de los archivos ambiguos (notebooks 00-08, `scripts/`, `doc/fase2` y `doc/fase3`).
- [ ] Separar codigo predictivo si corresponde a otra fase (`modelo_predictivo_global/`, `modelo-predictivo-preliminar/`, `extractor-indicadores-docker/`, `entregables/05 a 11`, `report/`).
- [ ] Definir motor de almacenamiento para el modelo estrella de OE-02.
- [ ] Completar modulos ausentes (indicadores continuos, dashboard Dash/Plotly) o reformular los objetivos/alcance si se decide mantener el stack actual.
- [ ] Generar MATRIZ_OBJETIVOS_CODIGO.md cruzando RESUMEN_CONTROL.md y RESUMEN_CODIGO.md.
- [ ] Capturar las evidencias listadas en la seccion 18.
- [ ] Redactar el capitulo de desarrollo tecnico con base en este archivo.
