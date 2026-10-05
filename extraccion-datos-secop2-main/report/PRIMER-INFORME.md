# Introducción
La contratación pública en Colombia constituye un pilar fundamental del desarrollo
socioeconómico del país, movilizando anualmente miles de millones de pesos a través del Sistema
Electrónico para la Contratación Pública (SECOP), administrado por la Agencia Nacional de
Contratación Pública — Colombia Compra Eficiente (ANCP-CCE). Dentro de este ecosistema, los
contratos de obra pública representan el segmento de mayor envergadura presupuestal y, al mismo
tiempo, el más propenso a desviaciones significativas en costo y tiempo. Estudios previos en el
contexto colombiano señalan que hasta un 81,9 % de los proyectos de infraestructura vial
experimentan algún tipo de sobrecosto o atraso durante su ejecución, lo cual evidencia la necesidad
de transitar de esquemas de auditoría reactiva hacia mecanismos de monitoreo preventivo basados
en datos.
En este contexto, el presente trabajo dirigido tiene como objetivo general diseñar una
metodología integral para el procesamiento y análisis predictivo de contratos de obra pública en
Colombia, mediante la integración de datos heterogéneos provenientes del SECOP y la aplicación
de algoritmos de Aprendizaje Automático (Machine Learning), con el fin de identificar
tempranamente riesgos de sobrecostos y retrasos en la ejecución contractual. Para ello, se han
definido cuatro objetivos específicos que articulan el alcance del proyecto: en primer lugar,
estructurar un proceso de Ingeniería de Datos (ETL) que permita la extracción, limpieza y
homologación semántica de los registros de obras civiles, preparando el dataset para el modelado
predictivo; en segundo lugar, realizar un Análisis Exploratorio de Datos (EDA) que caracterice el
comportamiento histórico de la contratación de infraestructura e identifique patrones, correlaciones
y variables críticas asociadas a la eficiencia o ineficiencia administrativa; en tercer lugar, desarrollar
y validar modelos predictivos basados en algoritmos supervisados, orientados a estimar la
probabilidad de ocurrencia de adiciones presupuestales o prórrogas; y, en cuarto lugar, implementar
un prototipo de interfaz de consulta inteligente utilizando técnicas de agentes RAG y Grandes
Modelos de Lenguaje (LLM), que permita la interacción con la información predictiva mediante
lenguaje natural.

## Objetivos
### Objetivo General
Diseñar una metodología integral para el procesamiento y análisis predictivo de contratos
de obra pública en Colombia, mediante la integración de datos heterogéneos (SECOP) y la
aplicación de algoritmos de Aprendizaje Automático (Machine Learning), con el fin de identificar
tempranamente riesgos de sobrecostos y retrasos en la ejecución contractual.
## ### Objetivos Específicos
● Estructurar un proceso de Ingeniería de Datos (ETL) que permita la extracción,
limpieza y homologación semántica de los registros de obras civiles provenientes de los
datos del SECOP, resolviendo inconsistencias de formato y calidad.
● Realizar un Análisis Exploratorio de Datos (EDA) para caracterizar el comportamiento
histórico de la contratación de infraestructura, identificando patrones, correlaciones y
variables críticas asociadas a la eficiencia o ineficiencia administrativa.
● Desarrollar y validar modelos predictivos basados en algoritmos supervisados
(Regresión/Clasificación), orientados a estimar la probabilidad de ocurrencia de adiciones
presupuestales o prórrogas en tiempo en los contratos analizados.
● Implementar un prototipo de interfaz de consulta inteligente utilizando técnicas de
agentes RAG y Grandes Modelos de Lenguaje (LLM), que permita la interacción y
extracción de información predictiva mediante preguntas en lenguaje natural
### Alcance
El presente informe parcial corresponde al periodo comprendido entre el 16 de febrero y el
25 de marzo de 2026, durante el cual se ha avanzado en la ejecución de la Fase I del proyecto,
denominada «Comprensión del Negocio y Estructuración de Datos». Esta fase responde
directamente al primer objetivo específico y comprende actividades de revisión normativa,
extracción de datos mediante la API pública de Socrata (SODA v3), elaboración del diccionario de
variables, exploración y perfilado de las fuentes de datos disponibles, y el diseño del esquema de
integración relacional entre las distintas fuentes.
Si bien la Fase I aún se encuentra en curso — dado que resta completar la integración
definitiva de las fuentes en un dataset analítico unificado, la ejecución del pipeline de limpieza y
transformación, y la extracción de indicadores a partir de los documentos de pliegos de condiciones
—, los avances alcanzados hasta la fecha permiten reportar resultados parciales sustantivos que se
detallan en las secciones subsiguientes del presente documento.

# Avances del Proyecto
Descripción y cumplimiento de los objetivos y actividades realizadas
## Objetivos cumplidos
. Durante el periodo evaluado, el trabajo se ha concentrado en el primer objetivo específico:
estructurar un proceso de Ingeniería de Datos (ETL) que permita la extracción, limpieza y
homologación semántica de los registros de obras civiles provenientes del SECOP, preparando
el dataset para el modelado predictivo. Este objetivo se encuentra en estado avanzado de ejecución,
habiéndo completado las actividades de revisión normativa, extracción de datos, elaboración del
diccionario de variables y exploración de las fuentes, mientras que las actividades de integración
definitiva, limpieza y validación del dataset se encuentran en curso.
Actividades desarrolladas hasta el momento
Las actividades ejecutadas durante el periodo se corresponden con las definidas en el plan
de trabajo para la Fase I del proyecto. A continuación se describe el alcance de cada una.
En relación con la revisión normativa y definición de variables clave (Actividad 1.1), se
llevó a cabo un estudio del ecosistema de datos del SECOP, identificando cuatro fuentes de datos
oficiales publicadas en el portal datos.gov.co como relevantes para el análisis de contratos de obra
pública: Contratos Electrónicos, Procesos de Contratación, Adiciones contractuales y
Proveedores Registrados. Hasta el momento, se tiene al dataset de Contratos Electrónicos como
fuente madre del proyecto, dado que contiene el ciclo de vida completo del contrato y alberga las
variables objetivo del modelo predictivo. A partir de esta fuente se clasificaron las 87 columnas
disponibles en ocho categorías funcionales, lo que permitió identificar tempranamente 15 columnas
que representan riesgo de fuga de información temporal (leakage) y que deben excluirse del
conjunto de variables predictoras.
Respecto a la extracción de datos vía API Socrata y scripts automatizados (Actividad 1.2),
se implementó un proceso sistemático de extracción mediante la API pública SODA v3 del portal
datos.gov.co, utilizando la librería sodapy de Python. La extracción se realizó de manera iterativa,
fuente por fuente, a través de seis notebooks de Jupyter. Para los datasets de gran volumen se diseñó
una estrategia de descarga por lotes de 150 identificadores con cláusulas WHERE IN, incorporando
reintentos con retroceso exponencial y paginación de 50.000 registros. Todos los datos se

almacenaron en formato Apache Parquet. Adicionalmente, se desarrolló un script automatizado para
la extracción de información financiera del Registro Único de Proponentes (RUP), administrado por
las Cámaras de Comercio, utilizando Playwright y el servicio CapSolver para resolver los desafíos
reCAPTCHA de la plataforma. Mediante este procedimiento se obtuvo información financiera para
28.548 proveedores únicos. Complementariamente, se desarrolló un script de prueba de concepto
para la descarga automatizada de documentos de pliegos de condiciones desde el portal del SECOP,
cuya finalidad es derivar indicadores cuantitativos que enriquezcan el conjunto de variables
predictoras. Esta última actividad se encuentra en fase de desarrollo.
En cuanto a la elaboración del diccionario de variables y criterios de éxito (Actividad 1.3),
se construyó un diccionario de datos integral que documenta los siete datasets generados,
totalizando 316 columnas y aproximadamente 805.000 registros. Para cada columna se registró el
nombre en la API, el tipo de dato, la descripción funcional, el porcentaje de nulidad y el número de
valores únicos. Respecto a los criterios de éxito, se identificaron cinco variables objetivo candidatas
para el modelo predictivo, siendo la variable binaria «tiene extensión de plazo» la recomendada
como target principal por su prevalencia del 22,1 % y un ratio de desbalance de 1:3,5. Pero esto
sigue en discusión, se seleccionará una vez se tenga los datos limpios, estructurados y unificados.
Sobre la estructuración, selección de variables y descarte de atributos irrelevantes
(Actividad 1.4), se confirmó el esquema relacional entre las fuentes con tres relaciones clave, se
ejecutó una primera integración parcial entre contratos y adiciones generando una tabla de 48.331
contratos únicos con 111 columnas, y se elaboró un documento de 66 variables candidatas
organizadas en siete grupos con hipótesis predictivas formuladas y clasificación de prioridad.
Asimismo, se documentó el plan preliminar (no aprobado ni avalado aun) de limpieza,
transformación e imputación que guiará la construcción del dataset analítico final.
Finalmente, la validación del dataset estructurado para modelado (Actividad 1.5) se
encuentra pendiente de ejecución, dado que requiere la finalización previa de la integración
completa y la aplicación del pipeline de limpieza.
Relación con los objetivos trazados en el plan de trabajo
El conjunto de actividades desarrolladas responde de forma directa al primer objetivo
específico del proyecto. La extracción de seis fuentes de datos, la elaboración del diccionario de
variables, la clasificación de columnas por rol funcional y la identificación de variables de leakage
constituyen los cimientos del proceso ETL que requiere el modelo predictivo. La integración parcial
contratos-adiciones y el documento de variables candidatas representan avances concretos hacia la
estructuración del dataset analítico que servirá de insumo para las fases posteriores de análisis
exploratorio y modelado.

Es pertinente destacar que, si bien la Fase I no se ha completado en su totalidad, el trabajo
realizado ha producido insumos que trascienden el alcance estricto del primer objetivo. El perfilado
estadístico de cada fuente, el análisis bivariado entre variables predictoras y la variable objetivo, y
la identificación de factores de riesgo contractual (valor del contrato, duración planificada,
modalidad de contratación, historial de sanciones del proveedor) constituyen hallazgos que
alimentan directamente el segundo objetivo específico relativo al análisis exploratorio de datos,
anticipando trabajo que facilitará la ejecución de la Fase II.
Resultados parciales obtenidos
A continuación se presentan los entregables producidos durante el periodo evaluado, organizados
por tipo.
- Datasets generados
Se construyó un repositorio de datos estructurado compuesto por siete archivos en formato Apache
Parquet, que en conjunto totalizan aproximadamente 805.000 registros y 316 columnas.
● Contratos Electrónicos — Obra (contratos_electronicos_obra.parquet). Fuente madre
del proyecto. Contiene 51.353 registros (48.331 contratos únicos) con 87 columnas que
abarcan el ciclo de vida completo de los contratos de obra pública: identificación, entidad
contratante, modalidad, fechas, valores, datos del proveedor y estado de ejecución.
● Procesos de Contratación — Obra (procesos_contratacion_obra.parquet). Contiene
138.112 registros con 57 columnas correspondientes a los procesos de compra que preceden
a la firma del contrato. Aporta variables de competencia (proveedores invitados, oferentes,
visualizaciones) que representan información disponible antes de la firma y, por tanto, libre
de leakage temporal. Cobertura del 99,9 % respecto a la fuente madre.
● Adiciones — Obra (adiciones_obra.parquet). Contiene 249.037 registros con 5 columnas
que documentan los eventos de modificación contractual: adiciones en valor, extensiones,
suspensiones, cesiones y conclusiones. Se vincula con la fuente madre mediante el
identificador del contrato, con una cobertura del 69,2 %.
● Proveedores Registrados — Obra (proveedores_obra.parquet). Contiene 13.117
registros (12.618 proveedores únicos) con 25 columnas que describen el perfil del
proveedor: tipo de empresa, tamaño, ubicación geográfica y clasificación UNSPSC.
Cobertura del 54,4 % respecto a los proveedores de la fuente madre.
● Proponentes por Proceso — Obra (proponentes_por_proceso_obra.parquet). Contiene
276.770 registros con 9 columnas que identifican a los proveedores que presentaron oferta
en cada proceso de contratación de obra. Cobertura del 29,4 % respecto a los procesos de
obra, limitada a las modalidades que registran proponentes en el portal de datos abiertos.

● Contratos + Adiciones integrado (contratos_adiciones_obra.parquet). Tabla derivada
de 48.331 contratos únicos con 111 columnas, resultado de la deduplicación de contratos y
adiciones y su integración mediante LEFT JOIN. Incluye 24 variables derivadas de las
modificaciones contractuales: conteos por tipo de modificación, indicadores binarios de
riesgo y métricas temporales.
● Proveedores RUP enriquecido (proveedores_rup.parquet). Tabla derivada de 28.548
proveedores únicos con 22 columnas que integran información financiera extraída del
Registro Único de Proponentes: activos totales, patrimonio, ingresos, utilidad neta,
indicadores de liquidez y endeudamiento, tamaño de empresa, número de empleados e
historial de sanciones y multas.
# Metodología Aplicada
Enfoque metodológico seguido en el trabajo
El desarrollo del presente trabajo dirigido se fundamenta en la metodología CRISP-DM
(Cross-Industry Standard Process for Data Mining), un modelo de proceso estándar para proyectos
de minería de datos y aprendizaje automático que organiza el ciclo de vida del proyecto en seis
fases iterativas: comprensión del negocio, comprensión de los datos, preparación de los datos,
modelado, evaluación y despliegue. Para efectos del plan de trabajo, estas seis fases se agruparon en
cuatro fases operativas alineadas con los objetivos específicos del proyecto: la Fase I abarca la
comprensión del negocio y la estructuración de datos, la Fase II corresponde al modelado
predictivo, la Fase III a la evaluación, y la Fase IV al despliegue de la interfaz inteligente.
La selección de CRISP-DM como marco de referencia obedece a tres criterios
fundamentales. En primer lugar, su orientación hacia el problema de negocio, lo cual garantiza que
las decisiones técnicas de modelado respondan a necesidades reales de fiscalización y gestión
pública, y no constituyan ejercicios puramente teóricos. En segundo lugar, su naturaleza iterativa,
que permite retroceder entre las fases de preparación de datos y modelado tantas veces como sea
necesario para refinar la calidad del dataset y mejorar la precisión de las predicciones; esta
característica resulta especialmente pertinente dado que los datos del SECOP presentan problemas
de calidad heterogéneos (sentinelas en lugar de nulos, duplicados masivos, tipos incorrectos) que
requieren múltiples ciclos de exploración y limpieza. En tercer lugar, su condición de estándar
ampliamente adoptado en la industria y la academia, lo que garantiza que la metodología resultante
sea replicable y comprensible para futuros investigadores y analistas que trabajen con datos de
contratación pública.
Durante el periodo evaluado, el trabajo se ha situado en las dos primeras fases del ciclo
CRISP-DM — comprensión del negocio y comprensión de los datos —, las cuales convergen
operativamente en la Fase I del plan de trabajo. La comprensión del negocio se materializó en la

definición del problema, la selección de las fuentes de datos relevantes y la formulación de las
variables objetivo del modelo. La comprensión de los datos se llevó a cabo mediante la extracción,
el perfilado estadístico y la exploración de las siete fuentes identificadas. Paralelamente, se ha
iniciado la transición hacia la tercera fase de CRISP-DM — preparación de los datos — con la
elaboración del plan de limpieza, transformación e imputación y la ejecución de la primera
integración parcial.
Herramientas, tecnologías y recursos utilizados.
El ecosistema tecnológico del proyecto se compone de herramientas de código abierto
seleccionadas por su madurez, su amplia adopción en la comunidad de ciencia de datos y su
compatibilidad con el flujo de trabajo CRISP-DM.
● Python 3.x. Lenguaje de programación principal del proyecto, seleccionado por su
ecosistema de librerías para ciencia de datos y aprendizaje automático.
● Jupyter Notebooks. Entorno de desarrollo interactivo que permite combinar código
ejecutable, visualizaciones y texto explicativo en un mismo documento, facilitando la
reproducibilidad y la documentación del análisis.
● Pandas. Librería de manipulación y análisis de datos tabulares utilizada para la carga de
archivos Parquet, la limpieza de datos, las operaciones de agrupación, los joins entre
datasets y el cálculo de estadísticas descriptivas.
● Sodapy. Cliente Python para la API SODA (Socrata Open Data API) que permite la
consulta directa a los datasets publicados en el portal datos.gov.co mediante filtros SoQL,
paginación y control de timeouts.
● Apache Parquet. Formato de almacenamiento columnar utilizado para la persistencia de
todos los datasets del proyecto, seleccionado por su eficiencia en compresión, la
preservación de tipos de datos y su compatibilidad nativa con pandas.
● Playwright. Framework de automatización de navegadores utilizado en los scripts de
extracción del RUP y de pliegos de condiciones, permitiendo la navegación programática
en portales web protegidos por reCAPTCHA.
● CapSolver. Servicio externo de resolución automatizada de desafíos reCAPTCHA v2,
empleado como componente auxiliar en los scripts de web scraping para acceder a las
plataformas del RUP y del SECOP.
● Matplotlib y Seaborn. Librerías de visualización estadística utilizadas para la generación
de gráficos de distribución, diagramas de barras y matrices de correlación durante la fase
de exploración de datos.
● Git y GitHub. Sistema de control de versiones y plataforma de alojamiento del
repositorio del proyecto, que garantizan la trazabilidad de los cambios en el código y la
documentación.

Para las fases posteriores del proyecto se prevé la incorporación de scikit-learn y XGBoost
para el modelado predictivo, así como de LangChain y modelos de lenguaje para la implementación
de la interfaz de consulta inteligente.
Estrategias para la validación de resultados.
La estrategia de validación del proyecto opera en dos niveles complementarios según la fase
del ciclo CRISP-DM.
A nivel de datos, correspondiente a la fase actual, la validación se realiza mediante el
contraste sistemático entre los registros descargados y las estadísticas reportadas por la API de
origen, la verificación de integridad referencial entre las fuentes (porcentajes de cobertura en los
joins), el diagnóstico de duplicados y valores atípicos, y la documentación de cada hallazgo de
calidad en los informes de exploración. Esta validación ha permitido, por ejemplo, detectar que la
llave de integración entre procesos y contratos no era el campo inicialmente asumido
(id_del_proceso) sino un campo diferente (id_del_portafolio), corrección que elevó la cobertura del
join del 0 % al 99,9 %.
# Análisis de Resultados Parciales
Evaluación de los avances logrados frente a los objetivos iniciales.
El periodo evaluado se ha concentrado en la ejecución del primer objetivo específico del
proyecto: estructurar un proceso de Ingeniería de Datos (ETL) que permita la extracción, limpieza y
homologación de los registros de obras civiles provenientes del SECOP, preparando el dataset para
el modelado predictivo. Este objetivo contempla cinco actividades en el plan de trabajo, de las
cuales tres se encuentran completadas, una presenta avance sustancial y una permanece pendiente.
Las actividades de revisión normativa y definición de variables clave (1.1), extracción de
datos vía API y scripts automatizados (1.2) se consideran completadas. Se logró extraer la
información de seis fuentes de datos distintas — cuatro previstas originalmente y dos adicionales
identificadas durante la exploración —, se construyó un repositorio de siete archivos Parquet con
aproximadamente 805.000 registros, y se documentó un diccionario de datos integral con 316
columnas. La actividad de estructuración y selección de variables (1.4) presenta un avance
significativo: se confirmó el esquema relacional, se ejecutó una primera integración parcial y se
documentaron las 66 variables candidatas con su clasificación de prioridad. No obstante, resta
ejecutar la integración completa de todas las fuentes, aplicar el pipeline de limpieza y
transformación, y completar la extracción de indicadores desde los documentos de pliegos de

condiciones. La actividad de validación del dataset estructurado (1.5) se encuentra pendiente, dado
que depende de la finalización de las anteriores.
En términos porcentuales, se estima un avance aproximado del 70 % en el primer objetivo
específico. Los entregables comprometidos para esta fase — documento de definición del alcance,
diccionario de variables, scripts de extracción y dataset estructurado — se encuentran en estado
avanzado, restando principalmente la consolidación del dataset analítico unificado y su validación.
Identificación de Logros, Dificultades y Desviaciones del Plan
Logros: El logro más relevante del periodo ha sido la construcción exitosa de un repositorio
de datos que excede el alcance inicialmente previsto. El plan original contemplaba la extracción de
cuatro fuentes de datos del portal datos.gov.co; durante la ejecución se identificaron dos fuentes
adicionales — Proponentes por Proceso y datos financieros del Registro Único de Proponentes
(RUP) — que enriquecen significativamente el poder predictivo del dataset. La extracción del RUP
constituye un aporte diferenciador, ya que esta información no está disponible como dataset abierto
y requirió el desarrollo de herramientas de scraping automatizado para su obtención. Otro logro
destacable es la identificación temprana de los factores de riesgo contractual mediante el análisis
bivariado, lo que ha permitido formular hipótesis predictivas con sustento empírico antes de iniciar
la fase de modelado.
Dificultades: Durante la ejecución se enfrentaron obstáculos técnicos de diversa índole. La
API Socrata presentó limitaciones no documentadas: el timeout por defecto de la librería sodapy (10
segundos) resultó insuficiente para las consultas sobre datasets de gran volumen, y el lenguaje de
consulta SoQL mostró incompatibilidades con la sintaxis esperada, como la ausencia de soporte
para comillas invertidas en los nombres de campos. Se descubrió, además, que la plataforma
normaliza los nombres de las columnas de forma inconsistente, lo que obligó a descargar un registro
de prueba antes de cada extracción para identificar los nombres reales.
La calidad de los datos del SECOP representó una dificultad transversal. Se identificaron
ocho patrones distintos de valores sentinela utilizados en lugar de nulos reales (incluyendo errores
ortográficos como «No Defenido»), duplicados masivos en todas las fuentes (hasta 96.942 filas
idénticas en el dataset de adiciones), campos numéricos almacenados como texto y outliers
extremos claramente erróneos (duraciones de 27 millones de días, precios base de 11 cuatrillones de
pesos). Estos problemas demandaron un esfuerzo de diagnóstico y documentación
significativamente mayor al previsto.

La integración entre fuentes reveló que la llave de relación entre Procesos de Contratación y
Contratos Electrónicos no era el campo asumido inicialmente (id_del_proceso, con prefijo
CO1.REQ.), sino un campo diferente (id_del_portafolio, con prefijo CO1.BDOS.), cuya
identificación requirió investigación adicional. Asimismo, la cobertura parcial de la fuente de
proveedores registrados (54,4 %) y del RUP (63,5 %) implica que una proporción importante de
contratos carecerá de información del proveedor en el dataset analítico, lo cual plantea desafíos para
la fase de imputación. Por último, la variable de sobrecosto calculada como la razón entre valor
pagado y valor contratado resultó no ser confiable como variable objetivo, dado que el campo
«valor del contrato» se actualiza con las adiciones presupuestales, ocultando el incremento real, y
que el 67,5 % de los contratos reportan cero pesos en valor pagado.
Desviaciones del plan: Se identifican dos desviaciones respecto al plan de trabajo original.
La primera es la incorporación de dos fuentes de datos no previstas (Proponentes por Proceso y
RUP), lo que amplió el alcance de la actividad de extracción pero enriqueció sustancialmente el
dataset. La segunda es el desarrollo del script de scraping de pliegos de condiciones, actividad que
surgió durante la exploración al identificarse la oportunidad de extraer indicadores cuantitativos de
estos documentos para mejorar la capacidad predictiva del modelo. Ambas desviaciones representan
ampliaciones del alcance motivadas por hallazgos del proceso exploratorio, y no desviaciones
negativas del cronograma.
En cuanto al cronograma, la Fase I se encuentra en ejecución más allá de la fecha estimada
de cierre, principalmente debido a la complejidad no anticipada de los problemas de calidad de
datos y a la incorporación de las fuentes adicionales mencionadas.
Medidas correctivas adoptadas en caso de ser necesarias.
Frente a las dificultades identificadas, se adoptaron las siguientes medidas correctivas
durante el periodo evaluado.
Para resolver las limitaciones de la API Socrata, se incrementó el timeout de las conexiones
de 10 a 120 segundos y se implementó una estrategia de descarga por lotes con reintentos y
retroceso exponencial, lo que eliminó las fallas de conexión en datasets de gran volumen. Se
adoptó, además, la práctica de descargar un registro de prueba antes de cada extracción masiva para
descubrir los nombres normalizados de los campos.
Ante la imposibilidad de acceder a la información del RUP mediante mecanismos
convencionales (la plataforma carece de API pública documentada y está protegida por
reCAPTCHA), se diseñó e implementó un script de automatización con Playwright y CapSolver
que incorpora mecanismos de protección contra bloqueos. Esta solución técnica permitió obtener
datos financieros que de otro modo habrían sido inaccesibles para el proyecto.

Respecto a la variable objetivo de sobrecosto, al comprobarse su falta de confiabilidad se
descartó como target y se adoptó la variable «tiene extensión de plazo» como objetivo principal del
modelo, cuya prevalencia del 22,1 % y relación confirmada con múltiples predictores la convierten
en una alternativa más robusta y alineada con el objetivo del trabajo.
Finalmente, la complejidad de los problemas de calidad de datos motivó la elaboración de
un plan detallado de limpieza, transformación e imputación que documenta las técnicas específicas
a aplicar en cada etapa, diferenciando el tratamiento según el mecanismo de datos faltantes (MCAR,
MAR o MNAR). Este plan servirá como guía para la ejecución estructurada del pipeline de
preprocesamiento en las próximas semanas.
# Conclusiones
Reflexión sobre el estado actual del trabajo
El proyecto se encuentra en un estado de avance que puede calificarse como satisfactorio
dentro del contexto de la Fase I del plan de trabajo. Las actividades de extracción de datos, que
constituían el componente de mayor incertidumbre técnica — dado que implicaban la interacción
con múltiples APIs, el manejo de datasets de gran volumen y el desarrollo de herramientas de
scraping para fuentes no documentadas —, se completaron exitosamente. El repositorio de datos
construido supera el alcance originalmente previsto tanto en número de fuentes (siete datasets frente
a los cuatro planificados) como en la riqueza de la información obtenida, particularmente con la
incorporación de los datos financieros del RUP que no formaban parte del diseño inicial.
La exploración de las fuentes de datos ha permitido confirmar la viabilidad del modelo
predictivo que constituye el núcleo del trabajo. Se dispone de un volumen adecuado de datos
(48.331 contratos únicos de obra pública con aproximadamente diez años de historia), una variable
objetivo con desbalance manejable (22,1 % de prevalencia), y un conjunto de 66 variables
candidatas con señales predictivas identificadas empíricamente. Estos elementos proporcionan una
base sólida para las fases de modelado y evaluación.
No obstante, es necesario reconocer que la Fase I se encuentra aún en curso. La integración
completa de las fuentes en un dataset analítico unificado, la ejecución del pipeline de limpieza y
transformación, y la extracción de indicadores desde los documentos de pliegos de condiciones son
tareas pendientes cuya finalización es requisito previo para la transición hacia las fases de análisis
exploratorio formal y modelado predictivo. La complejidad de los problemas de calidad de datos —
significativamente mayor a la anticipada al inicio del proyecto — ha sido el factor principal que
explica la extensión del tiempo requerido para esta fase.

Sugerencias para mejorar el desarrollo del proyecto
A partir de la experiencia acumulada durante el periodo evaluado, se formulan las
siguientes recomendaciones orientadas a optimizar la ejecución de las fases restantes del proyecto.
En primer lugar, se recomienda priorizar la finalización del dataset analítico unificado como
actividad inmediata, ejecutando el pipeline de limpieza documentado en el plan de transformación e
imputación. La existencia de este plan detallado, que especifica las técnicas a aplicar en cada etapa
y para cada tipo de variable, permite abordar esta tarea de manera estructurada sin necesidad de
nuevas decisiones de diseño significativas.
En segundo lugar, se sugiere adoptar un enfoque de prototipado rápido para la fase de
modelado, entrenando un modelo baseline con las variables de alta prioridad antes de completar la
totalidad del feature engineering. Esta estrategia permitiría obtener una primera medición de
desempeño predictivo y una clasificación de importancia de variables que oriente el esfuerzo de
ingeniería de features de manera más eficiente, evitando invertir tiempo en la construcción de
variables que el modelo no considere relevantes.
En tercer lugar, se recomienda establecer puntos de corte claros para la extracción de
indicadores desde los pliegos de condiciones. Dado que esta actividad depende de la navegación
automatizada en un portal web protegido por reCAPTCHA y su procesamiento involucra técnicas
de extracción de texto sobre documentos PDF de estructura variable, se sugiere definir un alcance
acotado (por ejemplo, limitado a licitaciones públicas de obra) y evaluar su aporte predictivo
incremental antes de escalar la extracción a la totalidad del dataset.
Finalmente, se recomienda mantener la documentación técnica como práctica continua a lo
largo de las fases restantes. La documentación producida durante la Fase I — informes de
exploración, plan de limpieza, documento de variables candidatas — ha demostrado ser un activo
valioso para la toma de decisiones y la trazabilidad del proceso, y su continuidad facilitará la
redacción del informe final del trabajo dirigido.
Expectativas para el informe final.
El informe final del trabajo dirigido deberá reportar la ejecución completa de las cuatro
fases del proyecto. Se espera que, para su elaboración, se hayan alcanzado los siguientes resultados:
la consolidación del dataset analítico unificado con las variables seleccionadas y el
preprocesamiento aplicado (Fase I); la caracterización estadística del comportamiento histórico de
la contratación de obra pública mediante el análisis exploratorio formal (Fase II, correspondiente al
segundo objetivo específico); el entrenamiento, la evaluación y la validación de al menos dos
modelos predictivos basados en algoritmos supervisados, con métricas de desempeño comparativas

y análisis de interpretabilidad (Fase III, correspondiente al tercer objetivo específico); y la
implementación de un prototipo funcional de interfaz de consulta inteligente que permita interactuar
con las predicciones del modelo mediante lenguaje natural (Fase IV, correspondiente al cuarto
objetivo específico).
El informe final incluirá, además, un análisis retrospectivo de la metodología CRISP-DM
aplicada al dominio de la contratación pública colombiana, identificando las lecciones aprendidas,
las limitaciones del enfoque y las oportunidades de investigación futura. Se prevé que la
contribución principal del trabajo sea doble: por un lado, un pipeline documentado y reproducible
para la extracción, limpieza e integración de datos del SECOP orientado a obra pública; y por otro,
un modelo predictivo validado que demuestre la viabilidad de anticipar riesgos contractuales a partir
de información disponible en etapas tempranas del proceso de contratación..
Firmas del director y codirector del Trabajo dirigido
Firma del Codirector
Nelson Beltran Galvis
C.C. 79334324
Email: nelsonbeltran@ufps.edu.co

ANEXOS
Datos preliminares extraidos data
Definiciones de las tablas extraidas definciones
Notebook de jupyter preliminares notebooks
Scripts de extraccion de datos scripts de extraccion