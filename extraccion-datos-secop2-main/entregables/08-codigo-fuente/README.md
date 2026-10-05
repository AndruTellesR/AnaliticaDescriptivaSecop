# 08 — Código fuente del proyecto

Esta carpeta contiene el código fuente desarrollado durante el proyecto,
organizado en tres subcarpetas según su rol.

## Subcarpetas

### `modulos-python/` — Módulos compartidos del modelo v2

Módulos Python reutilizables que encapsulan la lógica común de los notebooks
de modelado.

| Archivo | Rol |
|---------|-----|
| `preprocesamiento.py` | Funciones de carga, división train/test, escalado y construcción de pesos por clase |
| `entrenamiento.py` | Orquestación de `RandomizedSearchCV`, persistencia de modelos y métricas |
| `generar_notebooks_modelos.py` | Generador automático de los notebooks 04–11 a partir de plantilla |
| `generar_docs_modelos.py` | Generador automático de la documentación por modelo a partir de los resultados |
| `__init__.py` | Inicialización del paquete |

### `scripts-extraccion/` — Scripts auxiliares de extracción

Scripts independientes que automatizan tareas de extracción no cubiertas
por la API de Socrata.

| Archivo | Rol |
|---------|-----|
| `extraer_rup_auto.py` | Extracción automatizada del Registro Único de Proponentes mediante scraping con Playwright y CapSolver |
| `extraer_indicadores_pliegos.py` | Lógica de extracción de indicadores financieros desde los pliegos de condiciones (versión inicial) |
| `poblar_indicadores_pliegos.py` | Cruce de los indicadores extraídos con el dataset principal |
| `scraper_pliegos_poc.py` | Prueba de concepto inicial del scraper de pliegos |
| `validar_extraccion_pliegos.py` | Validación cuantitativa de los resultados del pipeline de pliegos |
| `generar_diccionario_datos.py` | Generación automática del diccionario de variables a partir del esquema |
| `generar_diccionario_md.py` | Renderización del diccionario en formato Markdown |
| `gemini/` | Utilidades específicas para integración con Gemini API |

### `chatbot/` — Prototipo de chatbot conversacional

Código del prototipo de Consultor de Riesgo Contractual que cumple con el
cuarto objetivo específico del proyecto.

| Archivo | Rol |
|---------|-----|
| `predictor.py` | Wrapper sobre el modelo LightGBM. Encapsula el pipeline completo de preprocesamiento y la integración con SHAP para explicabilidad local |
| `prompts.py` | Prompt de sistema para Gemini y declaración formal de la función `predecir_riesgo` |
| `gemini_client.py` | Cliente del modelo de lenguaje con bucle de function calling. Incluye modo CLI ejecutable directamente |
| `app.py` | Interfaz web mediante Streamlit |
| `requirements.txt` | Dependencias Python específicas del chatbot |
| `README.md` | Guía de instalación y uso del prototipo |

## Cómo ejecutar el chatbot

### Modo línea de comandos

```bash
cd chatbot
python gemini_client.py
```

Conversación interactiva. Escribir `salir` para terminar.

### Modo interfaz web (Streamlit)

```bash
cd chatbot
streamlit run app.py
```

Se abre `http://localhost:8501` con una interfaz de chat moderna.

## Configuración necesaria

El chatbot requiere una API key de Google Gemini configurada en un archivo
`.env` en la raíz del proyecto:

```
GEMINI_API_KEY=tu-api-key-de-google-ai-studio
```

La cuota gratuita de Google AI Studio es suficiente para el uso académico.
Solicitar la key en `https://aistudio.google.com/app/apikey`.

## Dependencias

Todas las dependencias se listan en `chatbot/requirements.txt`. Las
principales son:

- `pandas`, `numpy`, `scikit-learn`, `lightgbm`
- `joblib`, `shap`
- `google-generativeai`, `streamlit`, `python-dotenv`

## Convenciones del código

- Idioma español para nombres de variables, funciones y comentarios.
- `random_state = 42` para reproducibilidad.
- Docstrings explicativas en módulos y funciones públicas.
- Tipado mediante `typing` donde aporta claridad.
