# Entregables del Trabajo Dirigido

**Título**: Propuesta de analítica predictiva de datos abiertos caso SECOP
**Autor**: Ángel Gabriel García Rangel — Código 1152069
**Director**: MSc. Nelson Beltrán Galvis
**Programa**: Ingeniería de Sistemas — UFPS
**Período**: 16 de febrero – 21 de mayo de 2026

---

Este directorio contiene la totalidad de los entregables del trabajo dirigido,
organizados por categoría. Cada subcarpeta tiene su propio `README.md` con la
descripción detallada de su contenido.

## Estructura

| # | Carpeta | Contenido | Tamaño |
|---|---------|-----------|--------|
| 01 | [01-informes/](01-informes/) | Tres informes formales (primer, segundo y final) en formato Markdown | 208 KB |
| 02 | [02-anexos/](02-anexos/) | Tres anexos del informe final: fuentes, detalle modelo, repositorio | 36 KB |
| 03 | [03-documento-final-pdf/](03-documento-final-pdf/) | Fuente LaTeX para compilar el PDF en Overleaf, con las 26 imágenes | 1.7 MB |
| 04 | [04-datasets/](04-datasets/) | Diez datasets en formato Apache Parquet (crudos, integrados, depurados) | 97 MB |
| 05 | [05-modelos/](05-modelos/) | Nueve modelos serializados con joblib + archivo del ganador | 285 MB |
| 06 | [06-imputers/](06-imputers/) | Tres artefactos de preprocesamiento (winsorización, encoding, imputación) | 1.2 MB |
| 07 | [07-notebooks/](07-notebooks/) | 28 notebooks Jupyter agrupados en tres etapas | 5.7 MB |
| 08 | [08-codigo-fuente/](08-codigo-fuente/) | Módulos Python, scripts auxiliares y código del chatbot | 363 KB |
| 09 | [09-pipeline-docker/](09-pipeline-docker/) | Pipeline desatendido containerizado para extracción de pliegos | 139 KB |
| 10 | [10-figuras/](10-figuras/) | Todas las figuras del proyecto (informe + sub-sprints) | 3.9 MB |
| 11 | [11-documentacion-tecnica/](11-documentacion-tecnica/) | Documentación interna del proceso, decisiones, conceptos | 280 KB |

**Tamaño total aproximado**: 395 MB

## Mapa de cumplimiento con el informe final

| Sección del informe | Carpeta donde se sustenta |
|---------------------|---------------------------|
| Capítulo 1 — Datos crudos | 04-datasets/, 07-notebooks/extraccion-datos/, 08-codigo-fuente/scripts-extraccion/, 09-pipeline-docker/ |
| Capítulo 2 — Análisis estadístico | 07-notebooks/modelado-v1/ (notebook 01 EDA), 07-notebooks/modelado-v2/ (notebook 03 feature importance), 10-figuras/ |
| Capítulo 3 — Elaboración del modelo | 07-notebooks/modelado-v1/, 07-notebooks/modelado-v2/, 05-modelos/, 06-imputers/, 11-documentacion-tecnica/ |
| Capítulo 4 — Chatbot | 08-codigo-fuente/chatbot/ |
| Anexo A | 02-anexos/ANEXO-A-fuentes-y-variables.md |
| Anexo B | 02-anexos/ANEXO-B-detalle-modelo.md |
| Anexo C | 02-anexos/ANEXO-C-repositorio.md |

## Cómo recorrer este material

Si vas a evaluar el trabajo, el orden recomendado es:

1. **Empezar por el informe final**: [01-informes/INFORME-FINAL.md](01-informes/INFORME-FINAL.md) o la versión PDF que se compile desde `03-documento-final-pdf/main.tex`.
2. **Consultar los anexos** según los enlaces del informe: `02-anexos/`.
3. **Para verificar resultados**: abrir los notebooks en `07-notebooks/modelado-v2/` en orden numérico.
4. **Para inspeccionar el modelo final**: cargar `05-modelos/lgbm.pkl` con joblib (ver instrucciones en `05-modelos/README.md`).
5. **Para probar el chatbot**: seguir los pasos de `08-codigo-fuente/chatbot/README.md`.
6. **Para entender decisiones técnicas**: consultar `11-documentacion-tecnica/`, especialmente el documento exhaustivo `modelado-v2/03_conceptos_tecnicos.md`.

## Reproducibilidad

Todo el trabajo se desarrolló con `random_state = 42` en todos los procesos
estocásticos. Los artefactos de preprocesamiento (06-imputers/) y los modelos
serializados (05-modelos/) permiten reproducir exactamente las predicciones del
informe sin necesidad de re-entrenar.

Para una reproducción completa desde cero, seguir las instrucciones de
[02-anexos/ANEXO-C-repositorio.md](02-anexos/ANEXO-C-repositorio.md).

## Servicios externos integrados

| Servicio | Uso |
|----------|-----|
| API SODA v3 (datos.gov.co) | Extracción de los datasets primarios |
| Cámaras de Comercio | Información financiera del RUP (vía scraping) |
| Google AI Studio (Gemini 2.5 Flash) | Extracción de indicadores de pliego + chatbot |
| CapSolver | Resolución de reCAPTCHA durante scraping |
| Cloudflare R2 | Backup del pipeline Docker |
| Docker Hub | Distribución de la imagen del pipeline |
| ntfy.sh | Notificaciones push del pipeline |

## Contacto

Para preguntas sobre el contenido o solicitudes de información adicional:

- **Codirector**: MSc. Nelson Beltrán Galvis — nelsonbeltran@ufps.edu.co
