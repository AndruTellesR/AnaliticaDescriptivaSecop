# Anexo C — Estructura del repositorio y guía de reproducibilidad

Documento complementario al Informe Final del Trabajo Dirigido. Describe
la estructura del repositorio del proyecto y los pasos necesarios para
reproducir los resultados.

---

## C.1. Estructura del repositorio

```
extraccion-datos/
├── README.md
├── dataset.json                      ← Definiciones de las fuentes (API URLs, columnas, tipos)
├── excel_to_json.py                  ← Utilidad para convertir definiciones Excel a JSON
├── .env                              ← Variables sensibles (no se versiona)
├── .env.example                      ← Plantilla del archivo de variables
│
├── data/                             ← Datasets crudos y depurados (Parquet)
│   ├── contratos_electronicos_obra.parquet
│   ├── procesos_contratacion_obra.parquet
│   ├── adiciones_obra.parquet
│   ├── proveedores_obra.parquet
│   ├── proveedores_rup.parquet
│   ├── proponentes_por_proceso_obra.parquet
│   ├── contratos_adiciones_obra.parquet
│   ├── contratos_depurado_modelo.parquet
│   └── resultados-final.json         ← Output del pipeline Docker de pliegos
│
├── notebooks/                        ← Notebooks de exploración y depuración
│   ├── 00_definicion_tabla_base.ipynb
│   ├── 01_contratos_electronicos.ipynb
│   ├── 02_procesos_contratacion.ipynb
│   ├── 03_adiciones.ipynb
│   ├── 04_proveedores.ipynb
│   ├── 05_integracion_contratos_adiciones.ipynb
│   ├── 06_proponentes_por_proceso.ipynb
│   ├── 07_depuracion_variables_modelo.ipynb
│   └── 08_integracion_rup_no_consorcios.ipynb
│
├── scripts/                          ← Scripts auxiliares
│   ├── extraer_indicadores_pliegos.py
│   ├── poblar_indicadores_pliegos.py
│   └── gemini/                       ← Scripts del pipeline Docker
│
├── extractor-indicadores-docker/     ← Pipeline desatendido de extracción
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── DEPLOY_SERVER.md
│   ├── OPERACION.md
│   └── src/                          ← Código fuente del pipeline
│
├── modelo-predictivo-preliminar/     ← Sprint principal de modelado (v1)
│   ├── README.md
│   ├── notebooks/                    ← Notebooks por día (01–06)
│   ├── docs/                         ← Resúmenes diarios y plan
│   ├── data/                         ← Datasets intermedios y modelos v1
│   ├── figuras/                      ← Gráficas generadas
│   ├── consorcios/                   ← Sub-sprint especializado en consorcios
│   └── tuning/                       ← Sub-sprint de comparativa de estrategias
│
├── modelo_predictivo_global/         ← Modelo final v2 con variables estructurales
│   ├── README.md
│   ├── notebooks/                    ← 12 notebooks numerados (01–12)
│   ├── docs/                         ← Documentación técnica detallada
│   ├── src/                          ← Módulos Python reutilizables
│   ├── data/                         ← Datasets, modelos e imputers
│   ├── figuras/                      ← Gráficas del proceso de modelado
│   └── chatbot/                      ← Prototipo de chatbot conversacional
│       ├── README.md
│       ├── predictor.py
│       ├── prompts.py
│       ├── gemini_client.py
│       ├── app.py
│       └── requirements.txt
│
├── doc/                              ← Documentación general
│   ├── contexto/                     ← Contexto y plan de trabajo
│   ├── fase3_preparacion_datos/      ← Decisiones de la fase 3 CRISP-DM
│   └── comandos_extraccion_pliegos.md
│
└── report/                           ← Informes oficiales del trabajo dirigido
    ├── PRIMER-INFORME.md
    ├── SEGUNDO-INFORME.md
    ├── INFORME-FINAL.md              ← Documento principal
    ├── ANEXO-A-fuentes-y-variables.md
    ├── ANEXO-B-detalle-modelo.md
    ├── ANEXO-C-repositorio.md
    └── imagenes/                     ← Figuras del informe (26 archivos PNG)
```

## C.2. Dependencias

Las dependencias Python del proyecto se gestionan mediante un entorno
virtual local (`.venv/`) con Python 3.12. Las librerías principales son:

```
pandas        >= 2.0.0
numpy         >= 1.26.0
scikit-learn  >= 1.5.0
xgboost       >= 3.0.0
lightgbm      >= 4.0.0
shap          >= 0.50.0
optuna        >= 4.0.0
sodapy        >= 2.0.0
playwright    >= 1.40.0
matplotlib    >= 3.7.0
seaborn       >= 0.13.0
jupyter       >= 1.0.0
joblib        >= 1.3.0
google-generativeai >= 0.8.0
streamlit     >= 1.50.0
python-dotenv >= 1.0.0
```

## C.3. Variables de entorno

El archivo `.env` (no versionado) contiene las credenciales necesarias
para los servicios externos:

```
# Para extracción de pliegos y chatbot
GEMINI_API_KEY=...

# Para extracción de pliegos
CAPSOLVER_API_KEY=...

# Para backup del pipeline Docker
R2_ACCOUNT_ID=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_BUCKET=secop2bk

# Para notificaciones del pipeline
NTFY_TOPIC=extractor-secop-angeldev07-alerts-2026

# App token de la API Socrata (opcional, mejora rate limit)
SOCRATA_APP_TOKEN=nrnMDVHrooMY3wZIGrYfPsAq3
```

## C.4. Pasos para reproducir los resultados

### C.4.1. Preparar el ambiente

```bash
git clone <repo-url>
cd extraccion-datos
python -m venv .venv
.venv/Scripts/activate                # Windows
pip install -r requirements.txt
cp .env.example .env                   # Editar con las credenciales reales
```

### C.4.2. Reproducir la extracción de datos

Ejecutar en orden los notebooks de `notebooks/`. La extracción completa
toma varias horas debido a la cantidad de datos. Los datasets ya
extraídos están persistidos en `data/`, por lo que esta etapa puede
omitirse para reproducir solo el modelado.

### C.4.3. Reproducir el modelado v2 (modelo final)

```bash
cd modelo_predictivo_global/notebooks
jupyter nbconvert --to notebook --execute --inplace 01_dataset_global_completo.ipynb
jupyter nbconvert --to notebook --execute --inplace 02_preprocesamiento.ipynb
jupyter nbconvert --to notebook --execute --inplace 03_feature_importance.ipynb
# Ejecutar los notebooks 04–11 en orden o en paralelo
for nb in 04_modelo_lr 05_modelo_knn 06_modelo_svm 07_modelo_rf 08_modelo_xgb 09_modelo_lgbm 10_modelo_nb 11_modelo_mlp; do
  jupyter nbconvert --to notebook --execute --inplace ${nb}.ipynb
done
jupyter nbconvert --to notebook --execute --inplace 12_comparativa_final.ipynb
```

El tiempo total de ejecución es de aproximadamente 60–90 minutos en una
máquina estándar.

### C.4.4. Ejecutar el prototipo de chatbot

**Modo línea de comandos**:

```bash
cd modelo_predictivo_global/chatbot
python gemini_client.py
```

**Modo web (Streamlit)**:

```bash
cd modelo_predictivo_global/chatbot
streamlit run app.py
```

Se abre automáticamente el navegador en `http://localhost:8501`.

### C.4.5. Reproducir el pipeline Docker (extracción de pliegos)

```bash
cd extractor-indicadores-docker
docker compose up -d
```

Para detalles operativos consultar `OPERACION.md` y `DEPLOY_SERVER.md`.

## C.5. Garantía de reproducibilidad

Todos los procesos estocásticos del proyecto utilizan la semilla
`random_state = 42`. Ejecutar los notebooks en orden produce
exactamente los mismos resultados reportados en este informe. Los
artefactos serializados (modelos, imputers, mapas de codificación) están
versionados junto al código y permiten replicar la inferencia sin
necesidad de re-entrenar.

## C.6. Servicios externos utilizados

| Servicio | Rol | Tipo |
|----------|-----|------|
| API SODA v3 (datos.gov.co) | Extracción de datos abiertos | Público |
| Cámaras de Comercio (RUP) | Información financiera de proveedores | Público con scraping |
| CapSolver | Resolución de reCAPTCHA durante scraping | Pago por uso |
| Google AI Studio (Gemini API) | Extracción de indicadores y chatbot | Tier gratuito |
| Cloudflare R2 | Backup del pipeline Docker | Tier gratuito |
| Docker Hub | Distribución de la imagen del pipeline | Tier gratuito |
| ntfy.sh | Notificaciones push del pipeline | Tier gratuito |
| GitHub | Hosting del código y documentación | Tier gratuito |

## C.7. Tamaño aproximado del proyecto

| Componente | Volumen |
|------------|---------|
| Código fuente (Python + notebooks) | ~12.000 líneas |
| Datasets Parquet | ~250 MB |
| Modelos serializados | ~80 MB |
| Documentación Markdown | ~150.000 palabras |
| Figuras PNG | ~30 archivos |

## C.8. Contacto

Para preguntas sobre el proyecto o solicitudes de acceso a recursos
adicionales, contactar al codirector del trabajo:

**Nelson Beltrán Galvis** — nelsonbeltran@ufps.edu.co
