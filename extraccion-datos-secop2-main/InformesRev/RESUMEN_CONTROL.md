# RESUMEN CONTROL DEL ANTEPROYECTO

## 0. Metadatos del resumen

- **Archivo fuente analizado:** InformesRev/AnteproyectoAndres.md
- **Fecha de generación:** 2026-07-21
- **Tipo de documento:** Anteproyecto de grado (pregrado, Ingeniería de Sistemas, UFPS) — enfoque cuantitativo descriptivo-analítico.
- **Nivel de completitud del anteproyecto:** Alto en planteamiento del problema, justificación, marco teórico/referencial y diseño metodológico. Con vacíos puntuales: codirector no asignado, una referencia bibliográfica incompleta, ausencia de criterios de éxito cuantitativos y de definición de motor de almacenamiento físico.
- **Observaciones generales:** Documento bien redactado y sustentado en literatura (18 referencias). Existe una tensión no resuelta entre el enfoque declarado ("descriptivo-analítico") y elementos puntuales que introducen un componente predictivo (la pregunta de investigación usa el verbo "predecirlas" y el instrumento 3.7.4.a menciona scikit-learn para "modelos de clasificación supervisada") sin que exista un objetivo específico que lo sustente explícitamente.
- **Nota de contexto del repositorio (no proviene del anteproyecto):** En este mismo repositorio existe otro proyecto de analítica ya avanzado ("Propuesta de Analítica Predictiva — Caso SECOP II", dirigido también por el Ing. Nelson Beltrán Galvis) que usa el mismo dominio de datos (SECOP II, contratos de obra pública) y ya resuelve extracción, integración y modelado predictivo (LightGBM, AUC 0.9091) sobre variables de tiempo y costo. Esto es relevante para la sección 20 (riesgos) y 22 (preguntas pendientes), dado que ambos trabajos podrían compartir fuente de datos y fases de extracción/integración.

---

## 1. Identificación del proyecto

- **Título del proyecto:** Analítica descriptiva de la contratación de obra pública en Colombia
- **Carrera o programa académico:** Ingeniería de Sistemas
- **Área temática principal:** Analítica de datos aplicada a contratación pública / datos abiertos gubernamentales
- **Línea de investigación:** No especificado en el anteproyecto
- **Institución o contexto académico:** Universidad Francisco de Paula Santander (UFPS), Facultad de Ingeniería, San José de Cúcuta, 2025
- **Autor o autores:** Camilo Andrés Telles Ramírez (código 1151712)
- **Tutor/director:** Ing. Nelson Beltrán Galvis. Codirector: campo en blanco en el documento — No especificado en el anteproyecto
- **Organización, empresa o contexto de aplicación:** Sector público colombiano — contratación estatal vía SECOP (datos.gov.co, Colombia Compra Eficiente)

---

## 2. Resumen ejecutivo del anteproyecto

El proyecto aborda la ineficiencia estructural en la ejecución de contratos de obra pública en Colombia, evidenciada por altos porcentajes de prórrogas y sobrecostos reportados en fuentes oficiales y de control social. Propone construir, a partir de los datos abiertos de SECOP (datos.gov.co), una metodología reproducible de analítica descriptiva que integre información de procesos, contratos y proveedores en un modelo de datos analítico (modelo estrella), aplicando el marco teórico de la "restricción de hierro" (tiempo, costo, alcance) del PMI para operacionalizar el concepto de éxito contractual. El producto esperado es un flujo de trabajo automatizado (extracción vía API Socrata/OData, estructuración, limpieza ETL, cálculo de indicadores) que culmina en un tablero interactivo (dashboard) con visualizaciones para apoyar la interpretación, la transparencia y la toma de decisiones. Beneficia a entidades públicas, organismos de control, veedurías ciudadanas, academia y ciudadanía. La metodología es cuantitativa, descriptivo-analítica, de corte transversal, sobre el universo de contratos de obra pública 2018–2024 (criterio censal condicionado, sin muestreo probabilístico salvo restricciones técnicas). Se espera demostrar la factibilidad técnica de extraer y procesar datos abiertos a gran escala y construir un dataset analítico depurado y reutilizable.

---

## 3. Problema de investigación o necesidad identificada

- **Problema central:** Ineficiencia estructural en la ejecución de contratos de obra pública en Colombia (retrasos y sobrecostos), sin una metodología estandarizada y reproducible que la analice a partir de datos abiertos.
- **Contexto del problema:** Disponibilidad de datos SECOP en datos.gov.co; alto volumen de inversión estatal en obra pública.
- **Causas principales identificadas:** Alto volumen de registros, inconsistencias y valores faltantes, heterogeneidad de variables, dependencia de información complementaria en URLs asociadas a los contratos.
- **Consecuencias del problema:** Sobrecostos, dobles pagos, adiciones presupuestales sin sustento técnico, irregularidades por más de $5 billones COP en cuatro años (CGR, 2024).
- **Población, usuarios o actores afectados:** Entidades públicas, organismos de control, veedurías ciudadanas, sector académico, ciudadanía en general.
- **Situación actual descrita:** ~2 de cada 3 contratos de obra se ejecutan en plazo mayor al previsto; 1 de cada 4 cuesta más de lo presupuestado; 38% de contratos licitados en 8 años requirió prórrogas (86% de estas críticas).
- **Brecha o necesidad que justifica el proyecto:** No existe una metodología estandarizada, reproducible y orientada a datos abiertos que integre contrato, proveedor y evidencias de ejecución bajo criterios cuantificables de tiempo, costo y alcance.

---

## 4. Formulación del problema

- **Pregunta problema principal:** "¿Qué condiciones de los contratos de obra pública registrados en SECOP se asocian estadísticamente con el cumplimiento de las dimensiones de tiempo, costo y alcance, y en qué medida una metodología basada en datos abiertos permite identificarlas y predecirlas de forma sistemática y reproducible?"
- **Preguntas secundarias:** No especificado en el anteproyecto (solo se formula la pregunta principal).
- **Comentario sobre alineación:** Parcialmente alineada. El objetivo general habla de "determinar la eficiencia" e "identificar variables críticas" (enfoque descriptivo-analítico), mientras la pregunta usa el verbo "predecirlas", lo que sugiere un componente predictivo no reflejado explícitamente en los objetivos específicos. Ver sección 21.

---

## 5. Justificación

- **Justificación académica:** Llena un vacío metodológico: no existe metodología reproducible orientada a datos abiertos para obra pública.
- **Justificación técnica:** Supera las limitaciones de revisiones manuales y fragmentadas de procesos de contratación.
- **Justificación social/organizacional:** Fortalece transparencia, control social y toma de decisiones basada en evidencia.
- **Justificación económica:** No especificado en el anteproyecto de forma directa (se menciona el riesgo fiscal de $5 billones COP en irregularidades, pero no un análisis costo-beneficio del proyecto mismo).
- **Justificación tecnológica:** Aprovechamiento de API Socrata/OData y herramientas de código abierto (Pandas, PySpark, Streamlit, Plotly, Dash).
- **Beneficios esperados:** Dataset analítico depurado y reutilizable, indicadores y visualizaciones de alto valor aplicado, demostración de factibilidad técnica.
- **Valor agregado del proyecto:** Operacionalización del "éxito contractual" mediante la restricción de hierro (PMI/Atkinson/Meredith & Mantel) como marco interpretativo consistente.
- **Evaluación:** Justificación sólida, bien sustentada con literatura (Atkinson, 1999; Meredith & Mantel, 2012; Sharifnia et al., 2025; Colombia Compra Eficiente, 2024). No es genérica.

---

## 6. Objetivos del proyecto

### 6.1 Objetivo general

"Analizar integralmente la contratación de obra pública en Colombia mediante el procesamiento de datos de SECOP, con el fin de determinar la eficiencia de los proyectos según su tiempo, costo y alcance, identificando las variables críticas que condicionan el éxito de la ejecución contractual."

### 6.2 Objetivos específicos

| Código | Objetivo específico | Verbo principal | Resultado esperado | Evidencia posible | Observación |
|---|---|---|---|---|---|
| OE-01 | Implementar un mecanismo de extracción automatizada de los datos de SECOP (datos.gov.co), garantizando trazabilidad, actualización y reproducibilidad del conjunto de datos de estudio. | Implementar | Mecanismo/script de extracción funcional | Código de extracción, logs de ejecución, parámetros de consulta documentados | Claro y medible |
| OE-02 | Estructurar los conjuntos de datos de SECOP relacionados con obra pública (procesos, contratos y proveedores), definiendo el modelo de datos analítico y las reglas de integración necesarias. | Estructurar | Modelo de datos analítico integrado (modelo estrella) | Esquema de datos, scripts de integración/joins, diagrama del modelo | Claro; falta especificar motor de almacenamiento |
| OE-03 | Normalizar las variables del conjunto de datos analíticos, gestionando duplicados, valores faltantes, inconsistencias y tipificación. | Normalizar | Dataset depurado y confiable | Protocolo ETL documentado, diccionario de datos, dataset final sin duplicados/nulos críticos | Claro; falta umbral cuantitativo de calidad aceptable |
| OE-04 | Diseñar visualizaciones y tableros interactivos que presenten resultados (distribuciones, outliers con box plots, segmentaciones por modalidad/entidad/territorio). | Diseñar | Tablero interactivo funcional | Dashboard Dash/Plotly, capturas, filtros dinámicos operativos | Claro y medible |

---

## 7. Alcance del proyecto

- **Alcance general declarado:** Fundamentalmente analítico y metodológico; demuestra la factibilidad de un flujo reproducible desde extracción hasta indicadores y visualizaciones, usando la restricción de hierro como marco de referencia.
- **Qué incluye:** Contratos de obra pública en Colombia, período 2018–2024, datos abiertos de SECOP (datos.gov.co).
- **Qué no incluye:** Otras tipologías contractuales (prestación de servicios, suministro, consultoría, convenios); auditoría jurídica; juicios de responsabilidad fiscal, disciplinaria o penal.
- **Límites funcionales:** Sin fuentes primarias de recolección (encuestas/entrevistas); sin comparación con sistemas internacionales.
- **Límites técnicos:** Sujeto a capacidad de cómputo disponible (memoria, CPU, almacenamiento).
- **Límites temporales:** Dataset acotado a 2018–2024; cronograma académico de 24 semanas (marzo–agosto).
- **Límites metodológicos:** Datos secundarios estructurados; procesos automatizados de extracción, estructuración, limpieza, análisis y visualización; sin técnicas primarias.
- **Nivel esperado del producto:** Dataset analítico depurado + indicadores + tablero interactivo (dashboard). No se declara explícitamente como "prototipo" o "MVP"; se infiere un producto de tipo sistema de analítica descriptiva con visualización, sin componente predictivo desplegado.
- **Comentario sobre viabilidad:** El alcance parece viable para un trabajo de pregrado dado su naturaleza descriptivo-exploratoria. Riesgo: la mención de "predecirlas" en la pregunta de investigación podría generar expectativas que excedan el alcance declarado (ver sección 21).

---

## 8. Limitaciones y delimitaciones

**Limitaciones**
- Disponibilidad y calidad de los datos publicados en SECOP.
- Acceso a información complementaria mediante enlaces/URLs (pueden estar caídos, requerir autenticación o no ser estructurables).
- Recursos tecnológicos y de infraestructura (memoria, CPU, almacenamiento).
- Tiempo disponible dentro del calendario académico.
- Imposibilidad de verificación externa caso a caso (no hay contraste con expedientes internos).

**Delimitaciones**
- Temática: exclusivamente contratos de obra pública.
- Espacial: contexto colombiano, sin comparación internacional.
- Temporal: período 2018–2024.
- Metodológica: datos secundarios estructurados; sin técnicas primarias de recolección.

**Restricciones técnicas:** Capacidad de cómputo del investigador (equipo portátil compartido, servicios en la nube tipo Colab Pro).
**Restricciones de tiempo:** Cronograma académico de un semestre (24 semanas).
**Restricciones de acceso a datos:** Entidades con regímenes especiales pueden no estar completamente integradas en SECOP.
**Restricciones de recursos:** Presupuesto de fuente propia (~$4.672.500 COP), sin financiación institucional.
**Riesgos derivados:** Reducción de alcance si las limitaciones técnicas obligan a un muestreo; sesgo por exclusión de entidades de régimen especial; pérdida de completitud por enlaces rotos.

---

## 9. Antecedentes o trabajos relacionados

- **Antecedente 1:** Rodríguez Arévalo (2021) — Predicción de ineficiencias en contratación pública de Bogotá mediante ML sobre SECOP I; precisión >90% en prórrogas/sobrecostos. Limitado al nivel distrital, sin diferenciar obra pública, sin usar SECOP II.
- **Antecedente 2:** Universidad Distrital (2018) — Análisis de gobierno abierto y contratación pública; evidencia potencial de datos abiertos para toma de decisiones. Estudio conceptual, sin análisis a nivel de contrato individual.
- **Antecedente 3:** Pulgarín Gómez & Yepes Gómez (2024) — Participación de oferentes en obras civiles de Risaralda tras migración SECOP I→II; impacto positivo en pluralidad de proponentes, brechas de completitud.
- **Antecedente 4 (tabla):** Unaciencia (2021) — Eficacia de SECOP I y II; reporta falencias en bases de datos y ausencia de documentos.
- **Antecedente 5 (tabla):** Pontificia Universidad Javeriana (2018) — Plataforma de datos abiertos para obra pública; antecedente directo de productos analíticos y visualizaciones.
- **Relación con este proyecto:** Todos validan la viabilidad de usar SECOP/datos abiertos para analítica, pero ninguno construye una metodología reproducible orientada específicamente a obra pública bajo el marco de tiempo/costo/alcance.
- **Vacíos identificados:** Ausencia de metodología estandarizada y reproducible que integre contrato + proveedor + ejecución bajo criterios cuantificables de restricción de hierro, con foco exclusivo en obra pública y SECOP II.

---

## 10. Marco teórico y conceptual

| Concepto | Definición resumida | Relación con el proyecto | Fuente citada en el anteproyecto |
|---|---|---|---|
| Datos abiertos | Información accesible en línea, en formato legible por máquina, libre de uso y reutilizable | Fundamento legal/técnico de la extracción vía SECOP | Open Definition (2021); Ley 1712 (2014) |
| Restricción de hierro (Iron Triangle) | Marco que define tiempo, costo y alcance como dimensiones interdependientes del éxito de un proyecto | Marco central para operacionalizar "éxito contractual" | Atkinson (1999); Meredith & Mantel (2012); PMI (2021) |
| Ciclo de vida del dato | Etapas secuenciales: colección, procesamiento, limpieza, análisis, visualización | Cada objetivo específico corresponde a una etapa del ciclo | NIST (2015) |
| Marco normativo (Ley 1712, Decreto 1082) | Regulan acceso a datos públicos y publicación de información contractual | Sustento legal de la extracción y reutilización de datos | Ley 1712 (2014); Decreto 1082 (2015) |
| ISO 8000 | Estándar internacional de calidad de datos (exactitud, completitud, consistencia, accesibilidad) | Referente metodológico para la fase de depuración | ISO (2011); Sharifnia et al. (2025) |
| Modelo estrella (dimensional) | Arquitectura con tabla de hechos central y tablas de dimensiones | Modelo de datos propuesto para estructurar el dataset analítico | Kimball & Ross (2013) |

---

## 11. Marco tecnológico

| Tecnología | Tipo | Uso previsto | Estado en el anteproyecto | Riesgo o dependencia |
|---|---|---|---|---|
| Python | Lenguaje de programación | Extracción, procesamiento, análisis | Decisión definitiva | Ninguno relevante mencionado |
| API Socrata/OData (SoQL) | Servicio externo/API | Extracción automatizada de registros SECOP | Decisión definitiva | Dependencia de disponibilidad y estabilidad del portal datos.gov.co |
| Pandas / PySpark | Framework/biblioteca | Estructuración y transformación de datos | Propuesta | Escalabilidad para grandes volúmenes (millones de registros) |
| scikit-learn | Framework/biblioteca | "Modelos de clasificación supervisada" (mención puntual en instrumento 3.7.4.a) | Propuesta, sin objetivo específico asociado | Inconsistencia: no hay OE que declare modelado predictivo (ver sección 21) |
| matplotlib / Plotly | Herramienta de visualización | Generación de gráficos y visualizaciones | Decisión definitiva | Ninguno relevante mencionado |
| Dash / Streamlit | Framework web | Tablero interactivo (dashboard) | Propuesta (ambos mencionados en distintas secciones) | Ambigüedad: no se define cuál de los dos se usará finalmente |
| Google Colab Pro (o equivalente) | Infraestructura en la nube | Procesamiento de grandes volúmenes | Propuesta | Dependencia de presupuesto propio ($120.000 COP) |
| Base de datos / almacenamiento físico | Base de datos | No especificado | No especificado en el anteproyecto | Riesgo: no se define motor (Parquet, SQL, etc.) |
| Control de versiones | Herramienta de desarrollo | No especificado en el anteproyecto | No especificado | — |
| Herramientas de pruebas | Testing | No especificado en el anteproyecto | No especificado | — |

---

## 12. Metodología del proyecto

- **Tipo de investigación:** Cuantitativa, descriptivo-analítica, de diseño transversal.
- **Metodología de desarrollo de software:** No especificado en el anteproyecto (no se menciona Scrum, cascada, XP ni ágil; se usa el "ciclo de vida del dato" NIST como marco de fases, no como metodología de desarrollo de software).
- **Enfoque metodológico:** Empírico-analítico, basado en datos administrativos secundarios.
- **Técnicas de recolección de información:** Revisión documental y análisis de registros administrativos secundarios (no encuestas ni entrevistas).
- **Instrumentos:** API Socrata/OData; scripts Python de extracción/filtrado; matriz de operacionalización de variables; protocolo ETL; diccionario de datos; módulo analítico en Python; tablero interactivo (Dash/Plotly).
- **Población o muestra:** Criterio censal condicionado (universo completo que cumpla criterios de inclusión); muestreo estratificado por nivel territorial y modalidad solo si hay restricciones técnicas (mínimo 10% de la población).
- **Actividades principales:** Ver sección 13 (cronograma).
- **Comentario sobre coherencia:** Coherente en general entre metodología y objetivos. Se observa que CRISP-DM (IBM, 2021) figura en las referencias bibliográficas pero no se menciona ni utiliza en el cuerpo metodológico, donde en su lugar se usa el ciclo de vida del dato del NIST (ver sección 21).

---

## 13. Fases del proyecto o plan de trabajo

| Fase | Nombre | Descripción | Actividades principales | Entregables esperados | Objetivos relacionados |
|---|---|---|---|---|---|
| 1 | Revisión de literatura y ajuste del marco teórico | Consolidación de antecedentes y marco conceptual | Revisión bibliográfica | Marco teórico ajustado | Transversal |
| 2 | Definición del modelo de datos y variables | Diseño del modelo analítico | Matriz de operacionalización de variables | Modelo de datos definido | OE-02 |
| 3 | Extracción automatizada vía API Socrata/OData | Obtención de registros SECOP | Consultas SoQL, scripts de extracción | Dataset crudo extraído | OE-01 |
| 4 | Estructuración del dataset (modelo estrella) | Integración de fuentes | Construcción de tablas de hechos/dimensiones | Dataset estructurado | OE-02 |
| 5 | Depuración y limpieza de datos (ETL) | Tratamiento de calidad de datos | Protocolo ETL, imputación, deduplicación | Dataset depurado | OE-03 |
| 6 | Construcción de indicadores (tiempo, costo, alcance) | Cálculo de variables dependientes | Fórmulas de desviación de tiempo/costo/alcance | Indicadores calculados | OE-03 |
| 7 | Análisis descriptivo e inferencial | Exploración de patrones | Tablas de contingencia, visualizaciones comparativas | Resultados de análisis | OG |
| 8 | Diseño de visualizaciones y tablero interactivo | Construcción del dashboard | Desarrollo en Dash/Plotly | Tablero interactivo | OE-04 |
| 9 | Validación de resultados y ajustes | Revisión de hallazgos | Verificación de consistencia | Resultados validados | Transversal |
| 10 | Redacción del informe final | Documento de trabajo de grado | Redacción y consolidación | Informe final | Transversal |
| 11 | Revisión por el director de tesis | Retroalimentación del asesor | Ajustes según observaciones | Documento revisado | Transversal |
| 12 | Correcciones y entrega final | Cierre del proyecto | Ajustes finales y entrega | Documento final entregado | Transversal |

**Síntesis del cronograma (Tabla 2 del anteproyecto):**
- **Duración total estimada:** 24 semanas (marzo a agosto). El año exacto no se indica explícitamente en la tabla; la portada data el documento en 2025.
- **Hitos principales:** Fin de extracción (~semana 9), fin de estructuración (~semana 11), fin de ETL (~semana 13), indicadores calculados (~semana 17), visualizaciones (~semana 19), validación (~semana 21), entrega final (~semana 24).
- **Actividades críticas:** Extracción automatizada (depende de disponibilidad/estabilidad de la API); depuración ETL (base para todas las fases posteriores); validación de resultados (previa a redacción final).
- **Dependencias entre fases:** Estructura secuencial tipo cascada — cada fase depende de la finalización parcial de la anterior (literatura → modelo de datos → extracción → estructuración → ETL → indicadores → análisis → visualización → validación → redacción → revisión → entrega).

---

## 14. Producto o solución propuesta

- **Producto esperado:** Dataset analítico depurado (modelo estrella) + indicadores de desempeño (tiempo, costo, alcance) + tablero interactivo.
- **Tipo de sistema:** Sistema de analítica descriptiva con visualización interactiva (no transaccional, no predictivo desplegado).
- **Usuarios principales:** Entidades públicas, organismos de control, veedurías ciudadanas, academia, ciudadanía — Inferencia basada en el texto: se mencionan como beneficiarios en la justificación, no como "usuarios del sistema" formalmente definidos.
- **Roles de usuario:** No especificado en el anteproyecto.
- **Módulos previstos:** Inferencia basada en el texto: módulo de extracción (API), módulo de estructuración/integración (modelo estrella), módulo de limpieza (ETL), módulo de cálculo de indicadores, módulo de visualización (dashboard).
- **Funcionalidades esperadas:** Extracción automatizada, integración de tres fuentes (procesos, contratos, proveedores), limpieza/normalización, cálculo de indicadores de tiempo/costo/alcance, visualizaciones con filtros dinámicos, box plots, mapas coropléticos.
- **Entradas del sistema:** Registros abiertos de SECOP vía API Socrata/OData.
- **Procesos principales:** Extracción → estructuración → limpieza → análisis → visualización.
- **Salidas o resultados del sistema:** Dataset analítico, indicadores (desviación de tiempo, desviación de costo, índice de cumplimiento de alcance), tablero interactivo.
- **Reportes, dashboards o indicadores:** Tablero Dash/Plotly con filtros dinámicos y mapas coropléticos por territorio o modalidad de contratación.

| Módulo | Funcionalidades esperadas | Usuario relacionado | Objetivo que apoya |
|---|---|---|---|
| Extracción | Consultas SoQL, paginación, trazabilidad | Investigador | OE-01 |
| Estructuración | Modelo estrella, integración de fuentes | Investigador | OE-02 |
| Limpieza (ETL) | Deduplicación, imputación, tipificación | Investigador | OE-03 |
| Indicadores | Cálculo de desviaciones de tiempo/costo/alcance | Investigador, entidades, control | OG |
| Visualización | Dashboard interactivo, box plots, mapas | Entidades, veedurías, ciudadanía | OE-04 |

---

## 15. Requisitos preliminares identificados

### 15.1 Requisitos funcionales preliminares

- **RF-01:** El sistema debe extraer automáticamente datos de contratos de obra pública desde la API Socrata/OData de datos.gov.co.
- **RF-02:** El sistema debe integrar los datasets de procesos, contratos y proveedores en un modelo de datos analítico (modelo estrella).
- **RF-03:** El sistema debe detectar y tratar duplicados, valores faltantes e inconsistencias de tipificación.
- **RF-04:** El sistema debe calcular indicadores de desviación de tiempo, desviación de costo e índice de cumplimiento de alcance.
- **RF-05:** El sistema debe generar visualizaciones interactivas (distribuciones, box plots, segmentaciones por modalidad/entidad/territorio).

### 15.2 Requisitos no funcionales preliminares

- **RNF-01:** Reproducibilidad — el proceso de extracción y transformación debe ser replicable bajo las mismas condiciones.
- **RNF-02:** Trazabilidad — cada transformación debe quedar documentada y ser auditable.
- **RNF-03:** Escalabilidad — debe soportar procesamiento de grandes volúmenes (del orden de millones de registros).
- **RNF-04:** Uso de herramientas de código abierto.
- **RNF-05:** Calidad de datos alineada a ISO 8000 (exactitud, completitud, consistencia, accesibilidad).

| Código | Requisito | Tipo | Sección que lo respalda | Prioridad inferida |
|---|---|---|---|---|
| RF-01 | Extracción automatizada vía API | Funcional | 1.4.2 OE-01; 3.7.2.a | Alta |
| RF-02 | Integración en modelo estrella | Funcional | 1.4.2 OE-02; 2.2.5 | Alta |
| RF-03 | Limpieza y normalización | Funcional | 1.4.2 OE-03; 3.7.3.b | Alta |
| RF-04 | Cálculo de indicadores tiempo/costo/alcance | Funcional | 3.3 | Media |
| RF-05 | Visualizaciones interactivas | Funcional | 1.4.2 OE-04; 3.7.4.b | Media |
| RNF-01 | Reproducibilidad | No funcional | 3.7.6 | Alta |
| RNF-02 | Trazabilidad | No funcional | 3.7.3.b; 3.7.6 | Alta |
| RNF-03 | Escalabilidad | No funcional | 1.2; 2.2.5 | Media |
| RNF-04 | Código abierto | No funcional | 2.2.5 | Baja |
| RNF-05 | Calidad ISO 8000 | No funcional | 2.2.4 | Media |

---

## 16. Actores y usuarios del sistema

| Actor/usuario | Rol en el sistema | Necesidad principal | Funcionalidades asociadas |
|---|---|---|---|
| Investigador principal (Camilo Andrés Telles Ramírez) | Desarrollador/analista | Construir el flujo de extracción-análisis | Todos los módulos |
| Director de tesis (Nelson Beltrán Galvis) | Asesor metodológico | Validar rigor metodológico y avance | Revisión y validación (fase 11) |
| Entidades públicas | Usuario final / beneficiario | Monitoreo institucional del desempeño contractual | Consulta de indicadores y dashboard |
| Organismos de control / veedurías | Usuario final / beneficiario | Vigilancia y control social | Consulta de indicadores y dashboard |
| Academia / ciudadanía | Usuario final / beneficiario | Investigación y transparencia | Consulta del dataset y visualizaciones |

No se definen roles técnicos de sistema (p. ej. administrador vs. usuario básico) — No especificado en el anteproyecto.

---

## 17. Datos e información manejada

| Dato/entidad | Descripción | Origen | Uso en el sistema | Sensibilidad |
|---|---|---|---|---|
| Contrato de obra pública | Registro individual con valor, fechas, modalidad, estado | SECOP / datos.gov.co (API Socrata/OData) | Unidad de análisis principal | Pública (dato abierto) |
| Proceso de contratación | Información del proceso asociado al contrato | SECOP | Dimensión del modelo estrella | Pública |
| Proveedor | Persona natural, jurídica, consorcio o unión temporal | SECOP | Dimensión del modelo estrella | Pública |
| Entidad contratante | Nivel territorial y sector de la entidad | SECOP | Dimensión del modelo estrella | Pública |

- **Consideraciones de privacidad o seguridad:** No especificado en el anteproyecto (los datos son abiertos/públicos; no se discute anonimización).
- **Necesidad de almacenamiento:** No especificado explícitamente el motor físico. Inferencia basada en el texto: dado el uso previsto de Pandas/PySpark, es probable un almacenamiento en archivos tabulares (no confirmado en el documento).

---

## 18. Entregables esperados

- **Documento de anteproyecto:** Explícito en el anteproyecto (el propio documento).
- **Software/prototipo:** Explícito (mecanismo de extracción, módulo analítico, tablero interactivo).
- **Manual de usuario:** No especificado en el anteproyecto.
- **Manual técnico:** Inferido (el diccionario de datos y el protocolo ETL cumplen una función técnica documental similar).
- **Código fuente:** Explícito (scripts Python de extracción y módulo analítico).
- **Base de datos:** Inferido (dataset analítico estructurado en modelo estrella).
- **Pruebas:** No especificado en el anteproyecto.
- **Presentación:** Inferido (defensa de trabajo de grado, estándar institucional UFPS).
- **Otros anexos:** No especificado en el anteproyecto (la lista de anexos aparece vacía: "Completar según anexos del proyecto").

---

## 19. Criterios de éxito o validación

No existe una sección explícita de "validación" o "pruebas de aceptación". Lo más cercano es la validez y confiabilidad de instrumentos (numerales 3.7.5 y 3.7.6).

| Criterio | Cómo se valida | Evidencia necesaria | Objetivo relacionado |
|---|---|---|---|
| Validez de contenido | Las variables extraídas corresponden a los constructos definidos (valor, plazo, adiciones, estado) | Matriz de operacionalización de variables | OE-02, OE-03 |
| Validez de criterio | Los indicadores calculados son proxies usados en estudios previos | Comparación con literatura (Feigenbaum et al., 2024; Rodríguez Arévalo, 2021) | OG |
| Reproducibilidad | Extracción con parámetros fijos replica el mismo dataset | Scripts documentados, logs de ejecución | OE-01 |
| Trazabilidad | Protocolo ETL y diccionario de datos auditables | Documentación ETL | OE-03 |
| Consistencia interna | Fórmulas de indicadores aplicadas uniformemente | Código de cálculo de indicadores | OE-03 |

**Nota:** No se mencionan métricas cuantitativas objetivo (p. ej. porcentaje mínimo de cobertura esperada del dataset o umbral de calidad aceptable). Ver sección 21.

---

## 20. Riesgos académicos y técnicos detectados

| Riesgo | Tipo | Severidad | Evidencia en el anteproyecto | Recomendación |
|---|---|---|---|---|
| Ambigüedad entre enfoque descriptivo declarado y componente predictivo insinuado | Alcance/objetivos | Alta | Pregunta de investigación usa "predecirlas"; instrumento 3.7.4.a menciona scikit-learn para "modelos de clasificación supervisada" sin OE asociado | Aclarar si el proyecto incluye modelado predictivo o eliminar la mención de scikit-learn/predicción |
| Posible solapamiento con otro proyecto relacionado bajo el mismo director | Solapamiento de fases | Alta | Observación de contexto de repositorio (no del documento): existe otro proyecto de modelo predictivo LightGBM sobre SECOP II, obra pública, mismo director | Definir explícitamente la diferenciación y/o reutilización de datasets/fases ya resueltas en el otro proyecto |
| Ausencia de criterios de éxito cuantitativos | Validación | Media | Sección 3.7.5/3.7.6 solo describe validez conceptual, sin umbrales numéricos | Definir métricas objetivo (p. ej. % completitud mínima, cobertura de indicadores) |
| Falta de definición de motor de almacenamiento físico | Técnico | Media | Solo se menciona modelo estrella conceptual (2.2.5) | Especificar tecnología de persistencia (Parquet, SQL, etc.) |
| Codirector no asignado | Administrativo | Media | Campo en blanco en la portada | Definir codirector o remover el campo si no aplica |
| Referencia bibliográfica incompleta | Documental | Baja | Birks et al. (2024) marcada "[Completar... pendiente de verificación]" | Completar la referencia antes de la entrega formal |
| CRISP-DM citado pero no utilizado en el cuerpo metodológico | Metodológico | Baja | IBM (2021) aparece en referencias; el cuerpo usa el ciclo de vida del dato (NIST, 2015) en su lugar | Aclarar si CRISP-DM se usará o remover la referencia |
| Cronograma sin año explícito | Documental | Baja | Tabla 2 no indica año; portada indica 2025 | Añadir año explícito en el cronograma |

---

## 21. Inconsistencias, vacíos o ambigüedades

- **Ambigüedad 1:** La pregunta de investigación principal usa el verbo "predecirlas", lo cual sugiere un componente predictivo, mientras que el objetivo general y los objetivos específicos son de naturaleza descriptivo-analítica. *Por qué es un problema:* genera expectativas distintas sobre el producto final. *Pregunta a resolver:* ¿el proyecto incluye modelado predictivo o es puramente descriptivo? *Sección a ajustar:* 1.2 (pregunta de investigación) o 1.4.2 (objetivos específicos).

- **Inconsistencia 1:** El instrumento 3.7.4.a menciona scikit-learn para "construcción de modelos de clasificación supervisada", pero ningún objetivo específico contempla modelado predictivo. *Por qué es un problema:* introduce una herramienta sin propósito declarado. *Pregunta a resolver:* ¿se usará scikit-learn realmente, y para qué? *Sección a ajustar:* 3.7.4.a o 1.4.2.

- **Vacío 1:** CRISP-DM (IBM, 2021) aparece en las referencias bibliográficas pero no se menciona en el cuerpo del documento; en su lugar se usa el "ciclo de vida del dato" del NIST. *Por qué es un problema:* referencia bibliográfica sin uso aparente. *Pregunta a resolver:* ¿se pretendía citar CRISP-DM como metodología y se sustituyó sin actualizar referencias? *Sección a ajustar:* 2.2.3 o referencias bibliográficas.

- **Vacío 2:** No se definen métricas cuantitativas de éxito o validación (umbrales de completitud, calidad o cobertura). *Por qué es un problema:* dificulta evaluar objetivamente el cumplimiento de OE-03. *Pregunta a resolver:* ¿qué porcentaje de completitud/calidad se considerará aceptable? *Sección a ajustar:* 3.7.5/3.7.6.

- **Ambigüedad 2:** Se mencionan tanto Dash como Streamlit y Plotly como herramientas de visualización en distintas secciones (2.2.5 y 3.7.4.b), sin indicar cuál será la tecnología final. *Por qué es un problema:* puede generar decisiones técnicas tardías o redundantes. *Pregunta a resolver:* ¿Dash o Streamlit? *Sección a ajustar:* 2.2.5 y 3.7.4.b.

- **Vacío 3:** Referencia bibliográfica de Birks et al. (2024) explícitamente incompleta en el propio documento ("pendiente de verificación en base de datos institucional"). *Por qué es un problema:* riesgo de observación en evaluación formal. *Pregunta a resolver:* ¿cuál es la referencia completa? *Sección a ajustar:* Referencias bibliográficas.

- **Ambigüedad 3:** Las hipótesis H1–H3 (numeral 3.2) se formulan como orientadoras, aclarando que "su contrastación no implica necesariamente inferencia estadística formal". *Por qué es un problema:* no queda claro si el estudio pretende probar hipótesis estadísticamente o solo explorar tendencias. *Pregunta a resolver:* ¿se aplicarán pruebas estadísticas formales (chi-cuadrado, ANOVA) o solo análisis descriptivo? *Sección a ajustar:* 3.2 y 3.1.

---

## 22. Preguntas pendientes para el autor

**Problema y contexto**
- ¿La investigación es puramente descriptiva-analítica o incluye un componente predictivo real, dado el uso del verbo "predecirlas" en la pregunta de investigación?
- ¿Cómo se tratarán los contratos cuya información complementaria depende de URLs no accesibles?

**Objetivos**
- ¿Los cuatro objetivos específicos cubren completamente el objetivo general, considerando que ninguno declara explícitamente el "análisis" de eficiencia mencionado en el OG?
- ¿Cómo se medirá cuantitativamente la "confiabilidad de los resultados de la analítica" señalada en OE-03?

**Alcance**
- ¿Se incluyen o excluyen explícitamente los consorcios/uniones temporales del alcance, dado que H2 los menciona directamente?
- ¿Qué tratamiento se dará a entidades de régimen especial no cubiertas por SECOP?

**Metodología**
- ¿Se usará CRISP-DM (citado en referencias) o el ciclo de vida del dato del NIST como marco metodológico oficial?
- ¿Las hipótesis H1–H3 se someterán a pruebas estadísticas formales o solo a análisis descriptivo de tendencias?
- ¿Se usará Dash o Streamlit para el tablero interactivo?

**Código o implementación**
- ¿Existe ya infraestructura o código reutilizable de proyectos relacionados sobre SECOP II y obra pública que se pueda aprovechar para evitar duplicar la fase de extracción/integración?
- ¿Qué motor de almacenamiento se usará para el modelo estrella (Parquet, PostgreSQL, SQLite u otro)?

**Validación y pruebas**
- ¿Qué umbral cuantitativo de completitud/calidad de datos se considerará aceptable para validar el dataset final?
- ¿Se realizará alguna prueba de usabilidad sobre el tablero interactivo?

**Relación con otros proyectos o fases**
- ¿Este anteproyecto es independiente o complementario a otro proyecto de analítica/modelado predictivo sobre SECOP II y obra pública que pudiera existir bajo la misma dirección de tesis?
- ¿Se reutilizarán datasets ya depurados de un proyecto relacionado, o se construirá el dataset completamente desde cero?

---

## 23. Información clave para comparar contra el código implementado

### 23.1 Objetivos que deben tener evidencia en el código

- **OE-01:** Debe existir un script/módulo de extracción automatizada vía API Socrata/OData, con manejo de trazabilidad (logs, parámetros de consulta documentados, control de actualización).
- **OE-02:** Debe existir un modelo de datos analítico implementado (modelo estrella), con tabla de hechos (contratos) y tablas de dimensión (proveedores, entidades, modalidades), junto con scripts de integración/joins.
- **OE-03:** Debe existir un pipeline de limpieza (ETL) con tratamiento de duplicados, valores nulos y tipificación, y un diccionario de datos documentado.
- **OE-04:** Debe existir un tablero interactivo (Dash, Streamlit o Plotly) con visualizaciones de distribuciones, box plots y segmentaciones por modalidad/entidad/territorio.

### 23.2 Módulos esperados según el anteproyecto

- Módulo de extracción (API Socrata/OData)
- Módulo de estructuración/integración (modelo estrella)
- Módulo de limpieza/ETL
- Módulo de cálculo de indicadores (tiempo, costo, alcance)
- Módulo de visualización/dashboard

### 23.3 Funcionalidades mínimas esperadas

- Conexión a la API con consultas SoQL parametrizadas y filtrado por tipo de contrato = obra.
- Cálculo de tres indicadores: desviación de tiempo, desviación de costo, índice de cumplimiento de alcance.
- Al menos un tablero interactivo con filtros dinámicos y mapas coropléticos por territorio o modalidad.

### 23.4 Evidencias técnicas necesarias

- Capturas del tablero interactivo funcionando.
- Código de extracción reproducible (scripts Python).
- Diccionario de datos y protocolo ETL documentados.
- Dataset final depurado (formato tabular).
- Notebook o reporte con los indicadores calculados.

| Objetivo | Qué debería existir en el código | Evidencia esperada | Estado actual |
|---|---|---|---|
| OE-01 | Script de extracción vía API Socrata/OData | Código + logs de ejecución | Pendiente de auditoría del código |
| OE-02 | Modelo de datos analítico (modelo estrella) | Esquema + scripts de integración | Pendiente de auditoría del código |
| OE-03 | Pipeline ETL + diccionario de datos | Código de limpieza + documento diccionario | Pendiente de auditoría del código |
| OE-04 | Tablero interactivo con visualizaciones | Dashboard funcional + capturas | Pendiente de auditoría del código |

---

## 24. Versión ultracompacta para contexto IA

**Título:** Analítica descriptiva de la contratación de obra pública en Colombia (UFPS, Ing. de Sistemas, autor: Camilo Andrés Telles Ramírez, director: Nelson Beltrán Galvis).

**Problema:** ~2 de cada 3 contratos de obra pública en Colombia se ejecutan con retraso y 1 de cada 4 con sobrecosto. No existe metodología reproducible basada en datos abiertos de SECOP que integre contrato, proveedor y ejecución bajo criterios cuantificables.

**Objetivo general:** Analizar integralmente la contratación de obra pública en Colombia procesando datos de SECOP, para determinar la eficiencia de los proyectos según tiempo, costo y alcance, e identificar variables críticas de éxito contractual.

**Objetivos específicos:** (1) Extracción automatizada de SECOP vía API; (2) Estructuración de un modelo de datos analítico (modelo estrella) integrando procesos, contratos y proveedores; (3) Normalización/limpieza de variables (duplicados, faltantes, inconsistencias); (4) Diseño de visualizaciones y tableros interactivos.

**Alcance:** Solo contratos de obra pública, Colombia, 2018–2024. No incluye otras tipologías contractuales ni auditoría jurídica/fiscal. Producto: dataset analítico + indicadores + dashboard (no un sistema predictivo desplegado).

**Metodología:** Cuantitativa, descriptivo-analítica, transversal, empírico-analítica. Marco teórico central: restricción de hierro (tiempo, costo, alcance — PMI/Atkinson). Ciclo de vida del dato (NIST) como estructura de fases. Universo censal condicionado (sin muestreo probabilístico salvo restricciones técnicas, mínimo 10%).

**Producto esperado:** Dataset analítico depurado (modelo estrella), indicadores de desviación de tiempo/costo e índice de cumplimiento de alcance, tablero interactivo (Dash/Plotly/Streamlit).

**Tecnologías previstas:** Python, API Socrata/OData (SoQL), Pandas, PySpark, matplotlib, Plotly, Dash/Streamlit, scikit-learn (mención puntual sin objetivo asociado), Google Colab Pro.

**Módulos esperados:** Extracción, estructuración/integración, limpieza (ETL), cálculo de indicadores, visualización/dashboard.

**Riesgos principales:** (1) Ambigüedad entre enfoque descriptivo declarado y mención de "predecirlas"/scikit-learn sin objetivo predictivo explícito; (2) posible solapamiento con otro proyecto de modelado predictivo sobre SECOP II/obra pública bajo el mismo director; (3) ausencia de métricas cuantitativas de validación; (4) motor de almacenamiento no definido; (5) codirector no asignado.

---

## 25. Checklist de uso posterior

- [ ] Comparar objetivos contra código.
- [ ] Crear RESUMEN_CODIGO.md.
- [ ] Crear matriz objetivo-funcionalidad-evidencia.
- [ ] Validar alcance real.
- [ ] Identificar funcionalidades faltantes.
- [ ] Diferenciar aporte propio frente a fases de otros compañeros (incluida la posible relación con el proyecto de modelo predictivo SECOP II ya existente en el repositorio).
- [ ] Ajustar objetivos si el código no los cumple.
- [ ] Preparar evidencias.
- [ ] Redactar trabajo final.
- [ ] Revisar coherencia antes de entregar.
