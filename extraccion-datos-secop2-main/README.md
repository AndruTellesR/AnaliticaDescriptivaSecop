# Analítica de la contratación de obra pública en Colombia (SECOP II)

Proyecto de trabajo de grado — Ingeniería de Sistemas, Universidad Francisco de Paula Santander (UFPS).
Director: MSc. Nelson Beltrán Galvis.

Este repositorio contiene todo el flujo de trabajo sobre los contratos de **obra pública** registrados en
SECOP II (datos abiertos de Colombia): extracción desde la API, estructuración y control de calidad,
indicadores de desempeño contractual, análisis exploratorio, contraste de hipótesis, un tablero
interactivo y un trabajo paralelo de modelado predictivo y chatbot.

---

## 1. Qué hace el proyecto

La pregunta de fondo es cómo se comportan los contratos de obra pública frente a la **restricción de hierro**
(tiempo, costo y alcance) y qué factores se asocian con sus desviaciones.

El flujo completo es:

```
API SODA (datos.gov.co)  →  Parquet crudos  →  Tabla integrada (48.331 contratos)
        →  Indicadores de desempeño  →  EDA + contraste de hipótesis  →  Tablero Streamlit
```

**Indicadores de desempeño contractual** (derivados en `eda-extendido-integral/`):

| Indicador | Qué mide |
|---|---|
| Deslizamiento del plazo | Días de desviación respecto al plazo pactado (tiempo) |
| Desviación de costo | Porcentaje de desviación del valor final frente al pactado (costo) |
| Índice de alcance | Cumplimiento del alcance del contrato (categórico) |

**Hipótesis del anteproyecto** (se contrastan con Mann-Whitney y Kruskal-Wallis, α = 0,05, con tamaño de efecto):

- **H0.** Licitación pública → menores desviaciones de costo y tiempo que modalidades de menor competencia.
- **H1.** Consorcios y uniones temporales → mayor índice de adiciones y modificaciones.
- **H2.** Municipios con mayor NBI → mayores desviaciones en tiempo y costo (no contrastable en su forma original por falta de NBI municipal).

El **universo oficial** de análisis es el total disponible: **48.331 contratos** de obra pública, sin restricción
temporal. Un subconjunto de 19.194 contratos (diseño original del anteproyecto, 2018-2024 con ejecución
avanzada o finalizada) se conserva como análisis de sensibilidad.

---

## 2. Estructura del repositorio

| Carpeta / archivo | Contenido |
|---|---|
| `notebooks/` | Notebooks 00-06: extracción desde la API SODA y estructuración de las fuentes (contratos, procesos, adiciones, proveedores, proponentes). |
| `analitica-descriptiva-andres/` | Primera versión del análisis propio: modelo dimensional, calidad, indicadores, EDA, correlaciones y contraste de hipótesis (notebooks 01-08, `docs/`, `figuras/`, `data/`). |
| `eda-extendido-integral/` | **Análisis oficial** sobre el universo completo: 11 notebooks, `src/eda_comun.py` (módulo común), `docs/` (síntesis dual y hallazgos etiquetados), `data/` (CSV y Parquet de resultados), `build/` (generadores de notebooks y verificación). |
| `tablero-streamlit/` | Tablero interactivo (Streamlit + Plotly) sobre el universo completo. |
| `visualizer/` | Explorador web de los datasets (Next.js + DuckDB-WASM), sin backend. |
| `scripts/` | Scripts de scraping de pliegos y RUP, extracción de indicadores con Gemini y generación del diccionario de datos. |
| `entregables/` | Entregables del trabajo dirigido del compañero (modelos predictivos, datasets, chatbot, pipeline). Ver `entregables/README.md`. |
| `trabajo-de-grado-final/` | Documento final (`TRABAJO_DE_GRADO.md` / `.tex`) y `notebooks-explicados/` (cada notebook explicado en lenguaje no técnico). |
| `documento-tesis/` | Capítulo de resultados en Markdown. |
| `InformesRev/` | Anteproyecto, matriz de objetivos-código y resúmenes de control. |
| `report/` | Informes formales y fuente LaTeX para Overleaf. |
| `definciones/`, `dataset.json`, `data/diccionario_datos.json` | Definiciones oficiales de las fuentes SECOP y diccionario de datos. |
| `excel_to_json.py`, `parquet_viewer.py` | Utilidades: convertir definiciones Excel a JSON y visor de Parquet con interfaz Tkinter. |

### Fuentes de datos (API SODA de datos.gov.co)

| Fuente | Notebook | Uso |
|---|---|---|
| Contratos electrónicos (`jbjy-vk9h`) | `01` | Fuente madre; filtro `tipo_de_contrato = 'Obra'` |
| Procesos de contratación | `02` | Modalidad y datos del proceso |
| Adiciones / modificaciones | `03` | Cambios contractuales (H2) |
| Proveedores registrados | `04` | Tipo de contratista |
| Proponentes por proceso | `06` | Competencia (número de oferentes) |

`05_integracion_contratos_adiciones.ipynb` une todo en la tabla central de 48.331 contratos.

---

## 3. Requisitos e instalación

- Python 3.10 o superior.
- Node.js 18 o superior (solo para `visualizer/`).

```bash
# Entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate

# Dependencias del análisis y los notebooks
pip install -r requirements.txt
pip install scipy statsmodels      # usadas por eda-extendido-integral/src/eda_comun.py

# Dependencias del tablero
pip install -r tablero-streamlit/requirements.txt
```

**Configuración de claves.** Copia `.env.example` a `.env` y completa las claves solo si vas a usar
los scripts de scraping/Gemini:

```
GEMINI_API_KEY=...      # Google AI Studio: extracción de indicadores de pliegos y chatbot
CAPSOLVER_API_KEY=...   # resolución de reCAPTCHA de SECOP II
```

Nunca subas el archivo `.env` al repositorio. Los notebooks de extracción leen el token de la API SODA
desde `dataset.json` (clave `app_token`).

---

## 4. Cómo usarlo

### 4.1 Ejecutar el tablero (la forma más rápida de ver resultados)

No necesita internet ni credenciales: los datos están en `tablero-streamlit/data/universo_completo.parquet`.

```bash
cd tablero-streamlit
pip install -r requirements.txt
streamlit run app.py
```

Se abre en `http://localhost:8501`. Incluye:

- **Distribuciones:** histogramas de deslizamiento del plazo, desviación de costo, valor del contrato (log10) e índice de alcance.
- **Outliers:** box plots winsorizados P1-P99 solo para visualizar (el dato original no se modifica).
- **Segmentaciones:** por modalidad, tipo de contratista, sector, orden y departamento, con filtros en la barra lateral.

El tablero **no recalcula** indicadores: solo lee y visualiza los ya calculados en `eda-extendido-integral/`.
No incluye mapas ni el contraste de hipótesis (esos resultados están en el documento final y en `eda-extendido-integral/docs/`).

### 4.2 Reproducir el análisis desde cero

Ejecutar en este orden, siempre con Jupyter abierto en la carpeta del notebook (las rutas son relativas):

1. **Extracción y estructuración** — `notebooks/00` a `06` (descargan desde la API SODA; tardan según la conexión).
2. **Análisis extendido (oficial)** — `eda-extendido-integral/notebooks/01` a `11`, en orden numérico. Escriben sus resultados en `eda-extendido-integral/data/` y las figuras en `eda-extendido-integral/figuras/`.
3. **Primera iteración (opcional, sensibilidad)** — `analitica-descriptiva-andres/notebooks/01` a `08`.

```bash
jupyter lab
# o ejecutar un notebook sin interfaz:
jupyter nbconvert --to notebook --execute --inplace eda-extendido-integral/notebooks/10_hipotesis_extendido.ipynb
```

Dónde mirar los resultados sin ejecutar nada:

- Síntesis oficial: `eda-extendido-integral/docs/11_sintesis_dual.md` y `HALLAZGOS_ETIQUETADOS.md`.
- Hipótesis: `eda-extendido-integral/docs/10_hipotesis_extendido.md` y los CSV `h1_*`, `h2_*`, `h3_*` en `eda-extendido-integral/data/`.
- Explicación de cada notebook en lenguaje sencillo: `trabajo-de-grado-final/notebooks-explicados/README.md`.

### 4.3 Scripts de scraping y extracción con IA

Requieren las claves del `.env`, Playwright y, para algunos, `pdfplumber`.

| Script | Función |
|---|---|
| `scripts/scraper_pliegos_poc.py` | Descarga pliegos de condiciones desde SECOP II (Playwright + CapSolver). |
| `scripts/extraer_rup_auto.py` | Consulta el RUP de proveedores y guarda el resultado en el Parquet (con pausas anti-bloqueo y reanudación). |
| `scripts/extraer_indicadores_pliegos.py` | Extrae indicadores de capacidad financiera y organizacional de los PDF con regex. |
| `scripts/gemini/` | Extracción de indicadores con Gemini, descarga y validación de pliegos. |
| `scripts/generar_diccionario_datos.py` y `generar_diccionario_md.py` | Generan el diccionario de datos (JSON y Markdown). |

```bash
python scripts/generar_diccionario_datos.py
python scripts/generar_diccionario_md.py
```

### 4.4 Explorador web de datasets (`visualizer/`)

```bash
cd visualizer
npm install
npm run dev        # http://localhost:3000
```

Muestra el catálogo de datasets, tabla de columnas, valores centinela, esquema relacional y vista previa
de Parquet leído en el navegador con DuckDB-WASM.

### 4.5 Visor de Parquet de escritorio

```bash
python parquet_viewer.py ruta/al/archivo.parquet
```

### 4.6 Trabajo predictivo y chatbot (`entregables/`)

Es el trabajo dirigido del compañero: modelos de riesgo de atraso y sobrecosto (LightGBM ganador), artefactos
de preprocesamiento, un pipeline Docker de extracción de pliegos y un chatbot (Gemini + modelo + SHAP).
Las instrucciones están en `entregables/README.md` y `entregables/08-codigo-fuente/chatbot/README.md`.


## 5. Hallazgos principales

- 51,2 % de los contratos presentan retraso.
- **H1 (mixta):** la licitación pública es peor en tiempo pero mejor en costo que las modalidades de menor competencia. Al estratificar por cuantía el efecto de la modalidad cae cerca de 70 %, y medido con el número real de oferentes el efecto sobre el tiempo es nulo: lo que discrimina es la escala del proyecto, no la competencia.
- **H2 (parcial):** los consorcios y uniones temporales tienen más modificaciones totales, con efecto pequeño.
- **H3 (no contrastable):** no hay datos de NBI municipal; el proxy departamental muestra heterogeneidad, pero no valida la hipótesis como se formuló.

## 6. Limitaciones

- El indicador de costo solo cubre una parte de la muestra por la brecha de reporte de `valor_pagado` en SECOP.
- El índice de alcance no distingue la reducción del objeto contratado.
- Diseño transversal: ninguna asociación implica causalidad.
- Las hipótesis están preregistradas, por lo que no se aplicó corrección por comparaciones múltiples.
- El tablero corre localmente; no está desplegado en un servicio en línea.

## 7. Reproducibilidad

Todos los procesos estocásticos usan `random_state = 42`. Los resultados intermedios de cada notebook se
guardan en CSV/Parquet dentro de la carpeta `data/` correspondiente, de modo que se pueden consultar sin
volver a ejecutar la extracción.
