

**Analítica descriptiva de la contratación de obra pública en Colombia**

**Camilo Andres Telles Ramirez​**  
**1151712**

**Universidad Francisco de Paula Santander**  
**Facultad de Ingeniería**  
**Ingeniería de Sistemas**  
**San José de Cúcuta**  
**2025**  
**Analítica descriptiva de la contratación de obra pública en Colombia**

**Proyecto de grado para optar al título de Ingeniero de Sistemas**

**Director**  
**Ing. Nelson Beltran Galvis**  
**Codirector**  
**Ing.**   
**​**

**Universidad Francisco de Paula Santander**  
**Facultad de Ingeniería**  
**Ingeniería de Sistemas**  
**San José de Cúcuta**  
**2025**

# **TABLA DE CONTENIDO**

INTRODUCCIÓN

1\. PRESENTACIÓN GENERAL DEL ANTEPROYECTO

    1.1 TÍTULO

    1.2 PLANTEAMIENTO DEL PROBLEMA

    1.3 JUSTIFICACIÓN

    1.4 OBJETIVOS

        1.4.1 Objetivo general

        1.4.2 Objetivos específicos

    1.5 ALCANCES Y DELIMITACIONES

        1.5.1 Alcance

        1.5.2 Limitaciones y delimitaciones

2\. MARCO TEÓRICO Y REFERENCIAL

    2.1 ANTECEDENTES EN LA SOLUCIÓN DEL PROBLEMA

    2.2 MARCO TEÓRICO

3\. DISEÑO METODOLÓGICO

    3.1 Tipo y enfoque de investigación

    3.2 Sistema de hipótesis

    3.3 Variables de investigación

    3.4 Relación lógica entre variables

    3.5 Fuentes y unidad de análisis

    3.6 Población y muestra

        3.6.1 Población

        3.6.2 Muestra

        3.6.3 Criterios de inclusión

        3.6.4 Criterios de exclusión

        3.6.5 Criterios de eliminación

    3.7 Instrumentos

        3.7.1 Estrategia de recolección de información

        3.7.2 Instrumentos de recolección (extracción)

        3.7.3 Instrumentos de organización (estructuración y depuración)

        3.7.4 Instrumentos de análisis (técnicos)

        3.7.5 Validez de los instrumentos

        3.7.6 Confiabilidad de los instrumentos

4\. CRONOGRAMA

5\. PRESUPUESTO

REFERENCIAS BIBLIOGRÁFICAS

# **LISTA DE TABLAS**

Tabla 1\. Antecedentes relevantes sobre SECOP, datos abiertos y analítica de contratación pública

Tabla 2\. Variables dependientes del estudio

Tabla 3\. Variables independientes del estudio

Tabla 4\. Presupuesto global del proyecto

Tabla 5\. Descripción de los gastos de personal

Tabla 6\. Descripción de los gastos de materiales y suministros

Tabla 7\. Descripción de los gastos de equipos e infraestructura

# **LISTA DE FIGURAS**

Figura 1\. Ciclo de vida del dato aplicado al proyecto

# **LISTA DE ANEXOS**

(Completar según anexos del proyecto)

# 

# **1\. PRESENTACIÓN GENERAL DEL ANTEPROYECTO**

## **1.1 TÍTULO**

Analítica descriptiva de la contratación de obra pública en Colombia

## **1.2 PLANTEAMIENTO DEL PROBLEMA**

La contratación de obra pública en Colombia representa uno de los componentes más relevantes de la inversión estatal y, por tanto, demanda mecanismos de análisis que permitan evaluar su desempeño y fortalecer la transparencia institucional. No obstante, la evidencia disponible revela que una proporción significativa de estos contratos no se ejecuta dentro de las condiciones originalmente pactadas. Estudios recientes basados en registros de SECOP muestran que aproximadamente 2 de cada 3 contratos de obra se ejecutan en un plazo mayor al inicialmente previsto, mientras que 1 de cada 4 termina costando más de lo presupuestado (Corporación Cívica de Caldas, 2025). En el nivel nacional, análisis de contratos licitados en períodos de ocho años evidencian que cerca del 38 % requirió prórrogas, de las cuales el 86 % presentaron retrasos clasificados como críticos (Corporación Cívica de Caldas, 2024). A esto se suman hallazgos de la Contraloría General de la República sobre irregularidades contractuales por montos superiores a $5 billones de pesos en los últimos cuatro años, que incluyen sobrecostos, dobles pagos y adiciones presupuestales sin sustento técnico suficiente (CGR, 2024). Estas cifras evidencian que el problema de la ineficiencia en la ejecución contractual no es marginal sino estructural, y que su análisis sistemático es una necesidad urgente para la política pública.

En el portal de datos abiertos datos.gov.co existe información disponible a través de SECOP, fuente que concentra mayor detalle para caracterizar procesos y contratos. Sin embargo, a pesar de que investigaciones previas han abordado la contratación pública en Colombia desde perspectivas descriptivas o analíticas, los avances existentes presentan limitaciones que justifican la presente investigación. Rodríguez Arévalo (2021) abordó la predicción de ineficiencias contractuales en Bogotá mediante modelos de aprendizaje automático aplicados a registros de SECOP I, utilizando variables de cuantía, modalidad de selección y tipo de entidad; sin embargo, su alcance se limitó al nivel distrital y no contempló los contratos de obra pública como categoría diferenciada ni empleó los registros de SECOP II. Por su parte, el DNP (2015) realizó un estudio descriptivo de la contratación pública nacional basado en estadísticas agregadas, sin llegar a un análisis de desempeño a nivel de contrato individual. En consecuencia, no existe hasta la fecha una metodología estandarizada, reproducible y orientada a datos abiertos que integre de forma sistemática la información del contrato, las características del proveedor y las evidencias de ejecución para evaluar el desempeño contractual bajo criterios cuantificables. Este vacío de conocimiento constituye el núcleo temático de la presente indagación.

El aprovechamiento analítico de los registros de SECOP se ve limitado, además, por tres factores técnicos principales: (i) el alto volumen de registros —del orden de millones en los conjuntos asociados a procesos y proveedores—, (ii) la presencia de inconsistencias, valores faltantes y heterogeneidad en variables clave, y (iii) la dependencia de información adicional contenida en URLs asociadas a los contratos, donde pueden aparecer datos relevantes para evaluar ejecución —modificaciones, avances o valores—, lo cual dificulta su integración de forma reproducible. En consecuencia, actualmente es complejo construir un dataset analítico confiable que relacione, de forma sistemática, las condiciones del contrato con sus resultados de ejecución, con el fin de determinar qué factores se asocian con resultados favorables en obra pública.

Para este proyecto, el éxito contractual se define mediante la "restricción de hierro", marco teórico proveniente del Project Management Body of Knowledge del Project Management Institute (PMI, 2021), que establece el tiempo, el costo y el alcance como las tres dimensiones fundamentales para evaluar el desempeño en la gestión de proyectos. Aplicadas al contexto de la contratación pública, estas dimensiones se operacionalizan como: tiempo (cumplimiento del cronograma sin prórrogas), costo (mantenimiento del presupuesto sin adiciones monetarias) y alcance (entrega completa del objeto sin reducciones ni terminaciones anticipadas). El problema se formula entonces como la necesidad de diseñar e implementar una metodología estandarizada que permita extraer automáticamente los datos de SECOP, estructurarlos, limpiarlos y transformarlos en variables e indicadores que operacionalicen esas tres dimensiones, habilitando análisis descriptivos, inferenciales y, como proyección, modelado predictivo del desempeño contractual.

**Pregunta de investigación principal:** ¿Qué condiciones de los contratos de obra pública registrados en SECOP se asocian estadísticamente con el cumplimiento de las dimensiones de tiempo, costo y alcance, y en qué medida una metodología basada en datos abiertos permite identificarlas y predecirlas de forma sistemática y reproducible?

**Delimitación:** El estudio se realizará con información de SECOP disponible en datos.gov.co, acotada a contratos de obra pública suscritos entre 2018 y 2024, período que corresponde a la etapa de consolidación operativa de la plataforma y que garantiza suficiente volumen de registros con estructura homogénea y nivel de completitud adecuado para el análisis propuesto.

## **1.3 JUSTIFICACIÓN**

La contratación de obra pública en Colombia constituye un componente estratégico para el desarrollo económico, social y territorial, en la medida en que materializa inversiones públicas orientadas a infraestructura vial, educativa, sanitaria, institucional y de servicios. En este sentido, su análisis no sólo resulta relevante desde la perspectiva administrativa y presupuestal, sino también desde el control social, la transparencia y la evaluación del desempeño estatal. La disponibilidad de datos abiertos asociados al Sistema Electrónico para la Contratación Pública, publicados a través del portal datos.gov.co, representa una oportunidad significativa para fortalecer los procesos de investigación aplicada, monitoreo institucional y generación de evidencia sobre el comportamiento de los contratos estatales (Colombia Compra Eficiente, 2024). No obstante, que la información sea abierta no implica automáticamente que sea fácil de aprovechar en términos analíticos, ya que su uso efectivo depende de capacidades técnicas para extraerla, estructurarla, depurarla y transformarla en conocimiento útil.

En la práctica, el análisis de la contratación pública basada en datos abiertos enfrenta diversas barreras. Entre ellas se encuentran el alto volumen de registros disponibles, la heterogeneidad en la calidad de los datos, la presencia de valores faltantes, inconsistencias de digitación, duplicidades y variaciones en la forma en que las entidades reportan la información contractual. A ello se suma que parte de la evidencia asociada a la ejecución de los contratos puede encontrarse distribuida en enlaces, documentos o campos complementarios que requieren integración y tratamiento adicional para poder ser incorporados en un análisis sistemático. Estas condiciones hacen necesario diseñar un proceso metodológico riguroso que permita convertir datos administrativos en un conjunto de información confiable, trazable y reutilizable para fines de evaluación y seguimiento (Sharifnia et al., 2025).

En ese contexto, el presente proyecto se justifica porque propone una metodología estandarizada y reproducible para el tratamiento del ciclo de vida de los datos abiertos aplicados a la contratación de obra pública. Dicha metodología comprende fases de extracción, estructuración, limpieza, análisis y visualización, con el propósito de construir un conjunto de datos analítico que permita evaluar el comportamiento contractual de manera más objetiva, comparable y escalable. La relevancia de esta propuesta radica en que supera las limitaciones de las revisiones manuales y fragmentadas de los procesos de contratación, sustituyéndolas por una estrategia técnica sustentada en procedimientos verificables y replicables, lo que fortalece la calidad del análisis y la posibilidad de reutilización futura en otros estudios o contextos institucionales.

Uno de los aportes conceptuales centrales del proyecto consiste en operacionalizar el desempeño contractual a partir de la llamada restricción de hierro en gestión de proyectos. Este enfoque sostiene que el éxito de un proyecto depende del equilibrio entre tres dimensiones esenciales: tiempo, costo y alcance. Desde la literatura clásica de la gestión de proyectos, esta relación ha sido reconocida como uno de los marcos más ampliamente utilizados para valorar el desempeño de una iniciativa, al considerar que las variaciones en una dimensión afectan necesariamente a las demás (Atkinson, 1999). De forma complementaria, autores como Meredith y Mantel explican que todo proyecto se desarrolla bajo restricciones interdependientes de programación, presupuesto y cumplimiento del trabajo definido, por lo que la evaluación de resultados debe considerar estas tres dimensiones de forma integrada (Meredith & Mantel, 2012).

Incorporar la restricción de hierro dentro del análisis de los datos de contratación pública permite dotar al estudio de una base teórica sólida y de una lógica de evaluación clara. En lugar de limitarse a describir procesos contractuales o a presentar estadísticas generales, la investigación busca construir una lectura analítica del "éxito contractual" a partir de variables que representen tiempo, costo y alcance. Esto ofrece una ventaja metodológica importante, pues transforma datos administrativos dispersos en un esquema interpretativo consistente que facilita la comparación entre contratos y la identificación de patrones asociados a mejores o peores desempeños.

Si no se desarrolla una investigación de esta naturaleza, el aprovechamiento de los datos abiertos de la contratación seguiría dependiendo en gran medida de consultas manuales, análisis exploratorios poco sistemáticos o lecturas parciales de la información disponible. Esta situación limita la comparabilidad entre procesos, dificulta la detección temprana de riesgos y reduce la posibilidad de construir conocimiento acumulativo sobre el comportamiento contractual. En consecuencia, el problema no radica únicamente en la disponibilidad de los datos, sino en la ausencia de mecanismos técnicos y analíticos que permitan convertirlos en evidencia útil para la toma de decisiones, la vigilancia y la investigación.

Los resultados esperados refuerzan la pertinencia del proyecto. En primer lugar, se espera demostrar la factibilidad técnica de extraer y procesar de manera automatizada datos abiertos de contratación pública a una escala significativa. En segundo lugar, se prevé construir un dataset analítico depurado que integre información contractual, variables de proceso, atributos del proveedor y elementos asociados a la ejecución. En tercer lugar, se busca generar productos de alto valor aplicado, tales como indicadores y visualizaciones, que faciliten la interpretación del desempeño contractual desde la lógica de tiempo, costo y alcance. Estos resultados benefician a entidades públicas, organismos de control, veedurías ciudadanas, el sector académico y la ciudadanía en general.

Finalmente, la pertinencia del proyecto es tanto nacional como regional. Es nacional porque se apoya en fuentes oficiales de datos abiertos de contratación pública y aborda un problema transversal al funcionamiento del Estado. Es regional porque la metodología propuesta puede adaptarse a estudios focalizados por territorios, sectores o tipos de entidad, permitiendo generar análisis comparables en distintos contextos. En este sentido, la investigación propone una ruta metodológica con potencial de réplica, escalamiento y aplicación en futuros ejercicios de analítica pública.

## **1.4 OBJETIVOS**

### **1.4.1 Objetivo general**

Analizar integralmente la contratación de obra pública en Colombia mediante el procesamiento de datos de SECOP, con el fin de determinar la eficiencia de los proyectos según su tiempo, costo y alcance, identificando las variables críticas que condicionan el éxito de la ejecución contractual.

### **1.4.2 Objetivos específicos**

* Implementar un mecanismo de extracción automatizada de los datos de SECOP (datos.gov.co), garantizando trazabilidad, actualización y reproducibilidad del conjunto de datos de estudio.  
* Estructurar los conjuntos de datos de SECOP relacionados con obra pública (procesos, contratos y proveedores), definiendo el modelo de datos analítico y las reglas de integración necesarias para su relacionamiento consistente.  
* Normalizar las variables del conjunto de datos analíticos, gestionando duplicados, valores faltantes, inconsistencias y tipificación, para garantizar la calidad de la información y la confiabilidad de los resultados de la analítica.  
* Diseñar visualizaciones y tableros interactivos que presenten resultados (distribuciones, outliers con box plots, segmentaciones por modalidad/entidad/territorio) para apoyar la interpretación, la transparencia y la toma de decisiones.

## **1.5 ALCANCES Y DELIMITACIONES**

### **1.5.1 Alcance**

La presente investigación se delimita al análisis de la contratación de obra pública a partir de los datos abiertos asociados a SECOP, en tanto fuente oficial de información sobre los procesos contractuales del Estado colombiano. El alcance del proyecto es fundamentalmente analítico y metodológico. En primer lugar, busca demostrar la factibilidad de construir un flujo de trabajo reproducible para el tratamiento de datos abiertos de contratación pública, desde la extracción hasta la generación de indicadores y visualizaciones. En segundo lugar, pretende consolidar un conjunto de datos analítico enfocado en contratos de obra pública, integrando variables útiles para examinar su comportamiento desde criterios de tiempo, costo y alcance. En tercer lugar, el estudio aspira a ofrecer una base empírica que permita interpretar el desempeño contractual a partir de una lógica comparable, apoyada en la restricción de hierro como marco de referencia para la evaluación del éxito de los proyectos (Atkinson, 1999; Meredith & Mantel, 2012).

Desde el punto de vista temático, el estudio se restringe a la contratación de obra pública, por lo que sus resultados no pretenden generalizarse automáticamente a otras tipologías contractuales como prestación de servicios, suministro, consultoría o convenios. Igualmente, el estudio no pretende auditar jurídicamente los contratos ni emitir juicios de responsabilidad fiscal, disciplinaria o penal sobre las entidades, contratistas o supervisores. Su propósito es eminentemente analítico y metodológico: identificar patrones, construir indicadores y demostrar la factibilidad de utilizar datos abiertos de contratación pública como insumo para estudios de desempeño contractual.

### **1.5.2 Limitaciones y delimitaciones**

**Limitaciones**

Las principales limitaciones del proyecto están asociadas a factores externos al investigador y al contexto tecnológico disponible:

* Disponibilidad y calidad de los datos: la cobertura y precisión de los resultados dependen de la completitud, consistencia y actualización de las variables publicadas en SECOP; la existencia de campos vacíos o inconsistentes puede restringir el nivel de detalle alcanzable en la estructuración y depuración del dataset.  
* Acceso a información complementaria mediante enlaces: parte de la información relevante sobre los contratos puede encontrarse en URLs asociadas en los registros de SECOP; algunos enlaces pueden estar caídos, requerir autenticación o no contener información estructurable.  
* Recursos tecnológicos y de infraestructura: el procesamiento de grandes volúmenes de datos puede verse restringido por la capacidad de cómputo disponible (memoria, CPU, almacenamiento), condicionando la complejidad de los procesos de depuración.  
* Tiempo disponible dentro del calendario académico: el cronograma institucional acota el número de iteraciones sobre el diseño del modelo de datos, los procesos de depuración y la refinación de los tableros interactivos.  
* Imposibilidad de verificación externa caso a caso: dado que se trabaja exclusivamente con datos abiertos, no siempre será posible contrastar cada contrato con fuentes internas o expedientes completos para validar eventos como prórrogas, adiciones o modificaciones de alcance.

**Delimitaciones**

La investigación se delimita temática, espacial, temporal y metodológicamente al análisis de la contratación de obra pública en Colombia a partir de los datos abiertos de SECOP. Temáticamente, se concentra en contratos de obra pública debido a que esta tipología presenta características particulares de planeación, ejecución, seguimiento y modificación que la hacen especialmente adecuada para ser examinada desde la lógica de la restricción de hierro (Atkinson, 1999; Meredith & Mantel, 2012). En términos espaciales, la investigación se circunscribe al contexto colombiano y no incluye ejercicios comparativos con sistemas internacionales de contratación. Desde la dimensión temporal, el estudio se limita al período 2018–2024, que corresponde a la etapa de consolidación operativa de SECOP (Colombia Compra Eficiente, 2024). Metodológicamente, la investigación se delimita al uso de datos secundarios estructurados y al desarrollo de procedimientos automatizados de extracción, estructuración, limpieza, análisis y visualización, sin contemplar técnicas primarias de recolección de información.

# **2\. MARCO TEÓRICO Y REFERENCIAL**

## **2.1 ANTECEDENTES EN LA SOLUCIÓN DEL PROBLEMA**

En los últimos años, los gobiernos han impulsado estrategias de datos abiertos como mecanismo para fortalecer la transparencia, promover el control ciudadano y mejorar la eficiencia de la administración pública. En el ámbito de la contratación estatal, esta transformación ha permitido que grandes volúmenes de información sobre procesos contractuales, oferentes, adjudicaciones y ejecución se encuentren disponibles para su consulta y reutilización, generando nuevas oportunidades de análisis empírico, vigilancia institucional e investigación aplicada.

En Colombia, el Sistema Electrónico para la Contratación Pública, a través de los datos abiertos asociados a SECOP, ha consolidado una fuente oficial de información reutilizable para entidades estatales, ciudadanía, organismos de control y academia. Colombia Compra Eficiente señala que el SECOP constituye el punto de ingreso de información de la compra pública y que sus datos abiertos se ofrecen precisamente para facilitar análisis de mercado, ejercicios académicos y actividades de control (Colombia Compra Eficiente, 2024).

No obstante, la disponibilidad abierta de la información no resuelve por sí sola los retos analíticos. La literatura y los trabajos aplicados muestran que el aprovechamiento de datos de contratación pública enfrenta problemas asociados al gran volumen de registros, la heterogeneidad de las variables, la existencia de datos faltantes y la necesidad de complementar o interpretar la información contractual a partir de documentos y soportes adicionales.

**Antecedentes sobre SECOP**

Dentro de los antecedentes nacionales, se identifican trabajos que estudian el SECOP desde perspectivas jurídicas, de transparencia, datos abiertos y evaluación de resultados. Un referente importante es el trabajo "Datos abiertos y su beneficio en la contratación pública", que analiza el desarrollo del gobierno abierto y el uso de información contractual publicada en SECOP, mostrando el potencial de los datos abiertos para el análisis de inversiones públicas y la toma de decisiones basadas en evidencia (Universidad Distrital, 2018).

En el campo de la evaluación de la contratación pública, el trabajo "Predicción de ineficiencias en la contratación pública de Bogotá" constituye un antecedente particularmente relevante, ya que utiliza información pública contractual y modelos de inteligencia artificial para predecir contratos con resultados ineficientes, identificando además la importancia relativa de las variables explicativas. Rodríguez Arévalo (2021) reporta una precisión superior al 90 % para predecir contratos con prórrogas o sobrecostos, lo que demuestra que los datos de contratación pública pueden usarse en esquemas predictivos y de priorización de control.

Asimismo, se encontraron investigaciones que abordan el comportamiento del SECOP desde un enfoque de implementación y desempeño institucional. El estudio sobre el impacto en la participación de oferentes por la migración de SECOP I a SECOP II en obras civiles de Risaralda examina cómo los cambios en el sistema afectan la dinámica competitiva del mercado de obra pública (Pulgarín Gómez & Yepes Gómez, 2024). Por su parte, el artículo "Eficacia del Sistema Electrónico de Contratación Pública SECOP I y II" reporta falencias como faltantes en bases de datos, ausencia de documentos del proceso y debilidades en el registro de información contractual, hallazgo que respalda la necesidad de incorporar procesos de limpieza, validación e interpretación crítica de los datos (Unaciencia, 2021).

**Tabla 1\.**

*Antecedentes relevantes sobre SECOP, datos abiertos y analítica de contratación pública*

| Autor(es) / Institución | Año | Tipo | Objetivo | Metodología | Principales hallazgos | Aporte |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Rodríguez Arévalo, S. | 2021 | Tesis de maestría | Predecir ineficiencias en contratación pública de Bogotá | Aprendizaje automático sobre datos de SECOP I | Precisión \>90% en predicción de prórrogas y sobrecostos | Valida viabilidad de modelos predictivos con datos abiertos |
| Universidad Distrital | 2018 | Trabajo académico | Analizar relación entre gobierno abierto y contratación pública en Colombia | Revisión conceptual y análisis de inversiones TIC desde SECOP | Evidencia el potencial de datos abiertos para toma de decisiones | Sustenta pertinencia de SECOP como fuente oficial |
| Pulgarín Gómez & Yepes Gómez | 2024 | Tesis de pregrado | Analizar participación de oferentes en obras civiles de Risaralda tras migración SECOP I→II | Recolección de procesos en base de datos y análisis de brechas | Impacto positivo en pluralidad de proponentes; brechas en completitud del registro | Evidencia que datos de SECOP permiten estudiar competencia y calidad del sistema |
| Unaciencia | 2021 | Artículo científico | Analizar SECOP I y II desde principio de transparencia | Metodología descriptiva y revisión documental | Falencias en bases de datos, ausencia de documentos y debilidades de conectividad | Justifica necesidad de procesos de limpieza y validación crítica |
| Pontificia Universidad Javeriana | 2018 | Documento técnico | Desarrollar plataforma de datos abiertos para contratación de obras públicas | Enfoque aplicado de apertura y explotación de datos | Datos de obra pública organizables en plataformas para consulta y seguimiento | Antecedente directo para construcción de productos analíticos y visualizaciones |

*Nota. Elaboración propia.*

Como se observa en la Tabla 1, los antecedentes revisados muestran que el estudio de la contratación pública a partir de datos abiertos ha sido abordado desde perspectivas institucionales, jurídicas, descriptivas y analíticas. Sin embargo, persiste un vacío en la formulación de metodologías reproducibles orientadas específicamente a la construcción de datasets analíticos de obra pública y a la evaluación del desempeño contractual mediante criterios de tiempo, costo y alcance, aspecto en el cual se inscribe la presente investigación.

**Estado del arte técnico**

Desde el punto de vista técnico, la literatura reciente muestra que la analítica de contratación pública ha evolucionado desde enfoques descriptivos hacia modelos de automatización, análisis predictivo y evaluación de riesgo. Distintos trabajos internacionales muestran que los datos abiertos de contratación son usados para perfilar patrones de gasto, examinar dinámicas de competencia, estudiar el éxito de proveedores y construir índices o señales asociadas a integridad y corrupción (Welch et al., 2023). Esta tendencia confirma que la contratación pública ya no se analiza únicamente como un asunto normativo o procedimental, sino también como un problema de datos, modelado y generación de indicadores (Birks et al., 2024).

En esa línea, algunos estudios han incorporado machine learning para predecir resultados contractuales o apoyar la priorización del control. Un ejemplo es el trabajo de Feigenbaum et al. (2024), quienes proponen un esquema de priorización de la supervisión de la contratación pública mediante aprendizaje automático, agrupando contratos según sobrecostos o retrasos y modelando variables asociadas a desviaciones de costo y tiempo. De forma complementaria, investigaciones sobre predicción del desempeño de proyectos muestran que enfoques de aprendizaje automático pueden mejorar la identificación de variables que influyen en sobrecostos y retrasos (Sharifnia et al., 2025).

Otra línea del estado del arte se enfoca en la automatización del análisis de contratos. La literatura más reciente sobre analítica contractual asistida por inteligencia artificial describe sistemas capaces de extraer cláusulas, detectar riesgos, evaluar cumplimiento normativo y generar señales de gestión a partir de grandes volúmenes de documentos (Patel et al., 2025). Estos enfoques combinan procesamiento de lenguaje natural, detección de anomalías y analítica predictiva para transformar texto contractual en variables estructuradas.

De igual forma, la evolución de la IA aplicada a procurement se ha orientado hacia la extracción automatizada de variables contractuales, la comparación con históricos o estándares, y la construcción de scores o calificaciones para apoyar decisiones de seguimiento y control (Aboelazm & Dganni, 2025). La adopción de IA en procurement público también ha sido documentada a nivel global por la OCDE, que estima que la contratación pública representa aproximadamente el 13 % del PIB en países miembros (OECD, 2025).

A partir de los antecedentes revisados, se observa que existe producción académica sobre SECOP en temas de transparencia, implementación institucional, datos abiertos, participación de oferentes y predicción de ineficiencias (Rodríguez Arévalo, 2021; Pulgarín Gómez & Yepes Gómez, 2024). Sin embargo, se identifica un espacio de investigación específico en la construcción de una metodología reproducible de analítica de datos para contratación de obra pública, orientada a operacionalizar el desempeño contractual mediante criterios de tiempo, costo y alcance (Atkinson, 1999; Meredith & Mantel, 2012). El presente proyecto se ubica en la intersección entre tres líneas: datos abiertos de contratación pública, ingeniería de datos para integración y limpieza de información, y evaluación del desempeño contractual.

## **2.2 MARCO TEÓRICO**

El marco teórico presenta los fundamentos conceptuales y técnicos que sustentan el desarrollo de la solución analítica para la contratación de obra pública con datos abiertos de SECOP. Se estructura en conceptos fundamentales, marcos normativos, teoría de gestión de proyectos y tecnologías de implementación.

### **2.2.1 Datos abiertos y contratación pública**

Los datos abiertos se definen como aquellos que son accesibles en línea, en formato legible por máquina, libres de uso con atribución y permitidos para su reutilización (Open Definition, 2021). En Colombia, la Ley 1712 de 2014 establece el derecho de acceso a datos públicos en formato abierto, promoviendo la transparencia y la participación ciudadana. SECOP, como plataforma de contratación electrónica, publica sus registros en datos.gov.co mediante API Socrata/OData, habilitando extracción automatizada con trazabilidad (Colombia Compra Eficiente, 2024).

### **2.2.2 Restricción de hierro en gestión de proyectos**

La denominada restricción de hierro (Iron Triangle) constituye uno de los marcos conceptuales más consolidados en la literatura de gestión de proyectos. Este enfoque postula que todo proyecto está delimitado por tres variables interdependientes: alcance (qué se entrega), tiempo (cronograma de ejecución) y costo (presupuesto comprometido), de tal forma que cualquier variación en una de ellas afecta necesariamente a las demás (Atkinson, 1999). Meredith y Mantel (2012) refuerzan esta postura al señalar que la gestión efectiva de proyectos implica administrar de forma simultánea estas tres restricciones a lo largo de todo el ciclo de vida de la iniciativa.

En el contexto de la contratación de obra pública, este marco resulta especialmente pertinente porque permite operacionalizar el concepto de éxito contractual a partir de variables observables en los registros administrativos de SECOP. El tiempo se evalúa mediante el cumplimiento del cronograma contractual, identificando prórrogas o modificaciones injustificadas; el costo, a través de la comparación entre el valor inicial y el valor final del contrato; y el alcance, mediante indicadores asociados a terminaciones anticipadas, suspensiones prolongadas o reducciones del objeto contratado (Atkinson, 1999; Colombia Compra Eficiente, 2024).

### **2.2.3 Ciclo de vida del dato (Data Lifecycle)**

El ciclo de vida del dato constituye un marco metodológico que describe las etapas secuenciales a través de las cuales transita la información desde su origen hasta su uso final. De acuerdo con el National Institute of Standards and Technology, este ciclo comprende las fases de colección y extracción, procesamiento y estructuración, limpieza y normalización, análisis, y visualización o comunicación de resultados (NIST, 2015). En el presente proyecto, cada objetivo específico se articula directamente con una fase del ciclo de vida del dato, lo que dota al diseño metodológico de una estructura ordenada y reproducible.

*Figura 1\. Ciclo de vida del dato aplicado al proyecto. Adaptado de Data Management (NIST, 2015).* 

![][image1]*Elaboración propia.*  
*Nota. Cada etapa del ciclo se corresponde con un objetivo específico del proyecto: la colección con la extracción automatizada vía API Socrata/OData de SECOP; el procesamiento con la estructuración en modelo estrella; la limpieza con la detección y tratamiento de inconsistencias bajo criterios ISO 8000; el análisis con la construcción de indicadores de tiempo, costo y alcance; y la visualización con los tableros interactivos.*

### **2.2.4 Marco normativo**

El desarrollo de la presente investigación se enmarca en un conjunto de disposiciones normativas que regulan tanto el acceso y reutilización de datos públicos en Colombia como la publicación y gestión de la información contractual del Estado.

La Ley 1712 de 2014, conocida como la Ley de Transparencia y del Derecho de Acceso a la Información Pública Nacional, establece el derecho de toda persona a acceder a información pública en formatos abiertos y reutilizables, obliga a las entidades del Estado a publicar activamente sus datos en línea y define los principios de transparencia, máxima publicidad y facilitación del acceso como ejes rectores de la gestión de información pública (Ley 1712, 2014). Esta norma sustenta legalmente la extracción y reutilización de los datos de contratación disponibles en datos.gov.co.

El Decreto 1082 de 2015 regula la obligatoriedad de las entidades estatales de publicar sus procesos y contratos en el SECOP, así como los estándares mínimos de información que deben registrar a lo largo del ciclo contractual (Decreto 1082, 2015). Este decreto define qué variables contractuales deben estar disponibles en el sistema, lo cual incide directamente en la cobertura y completitud del conjunto de datos analítico que se pretende construir.

El Manual de Datos Abiertos del SECOP emitido por Colombia Compra Eficiente establece los estándares técnicos para la extracción de información mediante la API Socrata/OData, los criterios de calidad de los registros publicados y las condiciones de reutilización de los datos (Colombia Compra Eficiente, 2024).

En materia de calidad de datos, la norma ISO 8000 establece los criterios internacionales para la gestión de la calidad de datos maestros e información de intercambio, incluyendo dimensiones como exactitud, completitud, consistencia y accesibilidad (ISO, 2011). Su adopción como referente metodológico en la fase de depuración permite alinear el proyecto con estándares internacionales reconocidos (Sharifnia et al., 2025).

### **2.2.5 Tecnologías de implementación**

La implementación de la solución analítica propuesta requiere la articulación de un conjunto de herramientas tecnológicas que cubren las diferentes etapas del ciclo de vida del dato. La selección de estas tecnologías responde a criterios de accesibilidad, escalabilidad, reproducibilidad y compatibilidad con entornos de análisis de datos abiertos, privilegiando en todos los casos herramientas de código abierto.

**Extracción automatizada (API Socrata/OData)**

La extracción de los datos de contratación pública se realiza mediante la API Socrata/OData disponible en datos.gov.co, la cual permite realizar consultas estructuradas con sentencias tipo SQL que habilitan la selección, filtrado y paginación de registros a gran escala (Colombia Compra Eficiente, 2024). Un ejemplo de consulta aplicada al dominio del proyecto sería: SELECT \* FROM dataset WHERE tipo\_contrato LIKE '%obra%' LIMIT 1000\.

**Estructuración y modelado de datos**

Una vez extraídos los registros, la fase de estructuración transforma los datos brutos en un modelo analítico organizado. Para el procesamiento de grandes volúmenes se utilizan las bibliotecas Pandas y PySpark, que permiten construir DataFrames y realizar operaciones de transformación, combinación y agregación de manera eficiente (Feigenbaum et al., 2024). El modelo de datos adopta una arquitectura de modelo estrella (Kimball & Ross, 2013), en el que una tabla de hechos central —correspondiente a los contratos— se conecta con tablas de dimensiones que contienen información sobre proveedores, entidades contratantes y modalidades de contratación.

**Depuración y calidad de datos**

La fase de depuración se apoya en técnicas de análisis exploratorio de datos (EDA) para perfilar las variables, detectar valores atípicos mediante diagramas de caja (box plots) y distribuciones de frecuencia, identificar duplicidades e imputar valores faltantes. Los criterios de calidad adoptados se alinean con la norma ISO 8000 (ISO, 2011; Sharifnia et al., 2025).

**Visualización y tableros interactivos**

Para la visualización se utilizan las bibliotecas Streamlit y Plotly, que permiten construir interfaces web interactivas con filtros dinámicos, gráficos configurables y mapas coropléticos organizados por territorio o modalidad de contratación (OECD, 2025). Estas herramientas permiten que los resultados del análisis sean comprensibles, navegables y útiles para la toma de decisiones y el fortalecimiento del control social (Welch et al., 2023).

# **3\. DISEÑO METODOLÓGICO**

## **3.1 Tipo y enfoque de investigación**

La presente investigación adopta un enfoque cuantitativo de carácter descriptivo-analítico, sustentado en el procesamiento de datos administrativos secundarios provenientes de los registros abiertos de contratación pública disponibles en SECOP. Es descriptivo en tanto busca caracterizar el comportamiento de los contratos de obra pública mediante indicadores de desempeño asociados a tiempo, costo y alcance; y es analítico en la medida en que examina posibles asociaciones entre factores contractuales, institucionales y territoriales con los resultados observados (Hernández et al., 2014). El diseño es de tipo transversal, dado que el análisis se realiza sobre un corte temporal definido por la disponibilidad y calidad de los registros en SECOP.

El marco epistémico desde el cual se aborda la investigación es empírico-analítico, coherente con el uso de datos estructurados, operacionalización de variables y generación de evidencia cuantificable sobre el desempeño contractual. Este enfoque permite que los resultados sean replicables, verificables y susceptibles de ser utilizados como insumo para investigaciones posteriores o ejercicios de monitoreo institucional (Rodríguez Arévalo, 2021; Feigenbaum et al., 2024).

## **3.2 Sistema de hipótesis**

Con base en la revisión de la literatura y en la conceptualización de la restricción de hierro como marco de evaluación del desempeño contractual, se plantean las siguientes hipótesis de trabajo:

* H₁: Los contratos de obra pública adjudicados mediante licitación pública presentan menores desviaciones de costo y tiempo que los adjudicados mediante modalidades de menor competencia, como la contratación directa o la selección abreviada.  
* H₂: Los contratos ejecutados por consorcios o uniones temporales presentan un mayor índice de adiciones y modificaciones contractuales que los ejecutados por personas jurídicas individuales.  
* H₃: Los contratos de obra pública en municipios con mayores índices de necesidades básicas insatisfechas presentan mayores desviaciones en tiempo y costo respecto al valor y plazo inicialmente pactados.

Estas hipótesis se plantean como orientadoras del análisis exploratorio y descriptivo, por lo que su contrastación no implica necesariamente inferencia estadística formal, sino la identificación de patrones y tendencias en el conjunto de datos analítico construido (Atkinson, 1999; Meredith & Mantel, 2012).

## **3.3 Variables de investigación**

**Variables dependientes — El desempeño contractual**

Representan el resultado observable del contrato en función de las tres dimensiones de la restricción de hierro. Son las variables que el proyecto busca medir y explicar: desviación de tiempo (diferencia entre plazo pactado y plazo real de ejecución), desviación de costo (diferencia entre valor inicial y valor final del contrato, expresada como porcentaje de adición presupuestal) e índice de cumplimiento del alcance (indicador binario o categórico que señala si el objeto contractual fue entregado en su totalidad, parcialmente o no fue entregado).

**Variables independientes — Los factores explicativos**

Son las características del contrato, el proveedor, la entidad y el contexto territorial que se hipotetiza pueden influir en el desempeño contractual. Entre ellas se incluyen: modalidad de selección, tipo de contratista (persona natural, jurídica, consorcio o unión temporal), cuantía inicial del contrato, sector de inversión, nivel territorial de la entidad contratante y región geográfica.

**Variables extrañas**

Se reconocen como variables extrañas aquellas condiciones que pueden incidir en el desempeño contractual sin ser controladas directamente en el análisis, tales como fenómenos climáticos o de orden público que generen suspensiones justificadas, cambios normativos durante la ejecución del contrato, o variaciones macroeconómicas que afecten los costos de materiales e insumos. Aunque estas variables no serán medidas directamente, su existencia se reconoce como una limitación del estudio y justifica la interpretación cautelosa de los resultados (Sharifnia et al., 2025).

## **3.4 Relación lógica entre variables**

La estructura analítica del proyecto puede representarse de la siguiente forma:

**Desempeño contractual (Vc, Vt) \= f (Modalidad \+ Tipo de contratista \+ Región \+ Cuantía \+ Sector)**

Esta relación no implica necesariamente la estimación de un modelo de regresión formal, sino que orienta la construcción de indicadores, tablas de contingencia y visualizaciones comparativas que permitan identificar patrones de desempeño asociados a los factores independientes definidos (Feigenbaum et al., 2024; Rodríguez Arévalo, 2021).

## **3.5 Fuentes y unidad de análisis**

La fuente principal de información es el conjunto de datos abiertos de contratación pública disponibles en el portal datos.gov.co, extraídos mediante la API Socrata/OData de SECOP (Colombia Compra Eficiente, 2024). La unidad de análisis es el contrato de obra pública individual, con sus atributos asociados de proceso, proveedor, entidad y ejecución. No se contemplan fuentes primarias de recolección de información, como encuestas o entrevistas, dado que la investigación se basa exclusivamente en datos administrativos secundarios de carácter público.

## **3.6 Población y muestra**

### **3.6.1 Población**

La población objeto de estudio está constituida por la totalidad de los contratos de obra pública registrados en SECOP con disponibilidad en el portal de datos abiertos datos.gov.co, suscritos por entidades estatales colombianas de cualquier nivel territorial —nacional, departamental y municipal— durante el período analítico definido según disponibilidad y calidad de los registros. Esta población incluye contratos de obra civil en todos sus sectores de aplicación: infraestructura vial, construcción de edificaciones, obras de saneamiento, infraestructura educativa, entre otros, siempre que el tipo contractual esté clasificado como obra pública en los registros de SECOP (Colombia Compra Eficiente, 2024).

Dado el volumen potencialmente masivo de registros disponibles en la plataforma, la población se delimita operacionalmente mediante criterios técnicos de inclusión, exclusión y eliminación que garantizan la coherencia y la calidad analítica del conjunto de datos resultante (DNP, 2015; Rodríguez Arévalo, 2021).

### **3.6.2 Muestra**

Dado que el proyecto trabaja con datos abiertos de acceso masivo y emplea procesos automatizados de extracción mediante API Socrata/OData, se contempla el procesamiento del universo completo de registros que cumplan los criterios de inclusión definidos, sin reducción muestral probabilística. Esta decisión responde a un criterio censal condicionado, en el que el universo de análisis está determinado no por un muestreo estadístico, sino por los criterios técnicos de calidad y completitud de los registros (Feigenbaum et al., 2024; Colombia Compra Eficiente, 2024).

No obstante, en caso de que restricciones técnicas de procesamiento o de calidad de los datos hagan necesario reducir el conjunto de registros, se aplicará un muestreo aleatorio estratificado por nivel territorial y modalidad de contratación. En cualquier escenario, el tamaño mínimo de la muestra respetará el umbral del 10 % de la población total identificada (Hernández et al., 2014).

Es importante precisar que la población analizada corresponde exclusivamente a los contratos registrados en SECOP, lo cual no equivale a la totalidad de la contratación pública en Colombia. Existen entidades con regímenes especiales de contratación que pueden no estar completamente integrados en SECOP o que presentan niveles de detalle insuficientes para el análisis propuesto (Colombia Compra Eficiente, 2024; Sharifnia et al., 2025).

### **3.6.3 Criterios de inclusión**

Se incluirán en el conjunto de datos analítico los registros contractuales que cumplan simultáneamente las siguientes condiciones:

* Clasificados como contrato de obra pública en el campo de tipo de contrato o en la codificación UNSPSC correspondiente a obras civiles dentro de los registros de SECOP.  
* Con fecha de suscripción comprendida en el período 2018–2024.  
* Con información disponible en los campos mínimos requeridos para calcular los indicadores de desempeño: valor adjudicado, fecha de inicio, fecha pactada de terminación y estado del contrato.  
* Contratos que registren un estado de ejecución avanzado o finalizado (liquidado, terminado o con acta de liquidación disponible).  
* Registrados por entidades estatales colombianas de cualquier nivel territorial sujetas al Estatuto General de Contratación.

### **3.6.4 Criterios de exclusión**

Serán excluidos del análisis los registros que presenten alguna de las siguientes condiciones:

* Contratos cuyo tipo contractual no corresponda a obra pública, tales como prestación de servicios, suministro, consultoría, interventoría o convenios.  
* Registros con valores adjudicados iguales a cero o negativos, que sugieren errores de digitación o registros incompletos.  
* Contratos con fechas de inicio o terminación inválidas, incluyendo fechas anteriores a la creación de SECOP o con inversión lógica entre fecha de inicio y fecha de terminación.  
* Registros de entidades con regímenes especiales de contratación cuya estructura de reporte sea incompatible con las variables de análisis definidas.  
* Contratos en estado de ejecución activa al momento de la extracción de datos, dado que sus variables de desempeño final no son aún observables.

### **3.6.5 Criterios de eliminación**

Durante el proceso de depuración y análisis, serán eliminados los registros que, habiendo cumplido inicialmente los criterios de inclusión, presenten alguna de las siguientes condiciones:

* Duplicidades detectadas durante la fase de limpieza, conservando únicamente el registro más completo o el más reciente en caso de actualizaciones.  
* Contratos que modifiquen su tipo contractual durante el proceso de análisis como resultado de correcciones retroactivas en SECOP.  
* Registros cuya información de ejecución resulte internamente inconsistente de manera irrecuperable mediante técnicas estándar de imputación (Sharifnia et al., 2025).

## **3.7 Instrumentos**

### **3.7.1 Estrategia de recolección de información**

El presente proyecto emplea como estrategia principal la revisión documental y el análisis de registros administrativos secundarios, dado que la naturaleza del objeto de estudio son los contratos de obra pública consignados en SECOP. A diferencia de la investigación social tradicional basada en encuestas o entrevistas, los instrumentos aquí empleados no son cuestionarios sino herramientas y protocolos de procesamiento, dado que la información ya existe en forma de registros institucionales producidos y publicados por Colombia Compra Eficiente a través del portal datos.gov.co (Hernández et al., 2014; Corral, 2009). Los instrumentos se clasifican en tres categorías según su función en el proceso investigativo: recolección, organización y análisis.

### **3.7.2 Instrumentos de recolección (extracción)**

**a) Interfaz de programación de aplicaciones (API) Socrata/OData**

La extracción automatizada de los registros contractuales se realiza mediante consultas programáticas a la API pública del portal datos.gov.co, utilizando el protocolo OData y el lenguaje de consulta SoQL (Socrata Query Language). Este mecanismo constituye el instrumento principal de conexión entre el código del proyecto y los servidores del Estado colombiano, permitiendo recuperar registros de manera estructurada, reproducible y auditada.

**b) Scripts de extracción y filtrado inicial en Python**

Complementariamente, se emplean scripts desarrollados en Python que aplican filtros parametrizados sobre los registros descargados, seleccionando únicamente los contratos de obra pública que cumplen los criterios de inclusión definidos. Estos scripts operacionalizan directamente dichos criterios y garantizan que el proceso de selección sea replicable bajo las mismas condiciones (Feigenbaum et al., 2024).

### **3.7.3 Instrumentos de organización (estructuración y depuración)**

**a) Matriz de operacionalización de variables**

Consiste en una tabla estructurada que define para cada variable: su nombre, definición conceptual, tipo de dato (numérica o categórica), rango válido de valores esperados y la columna exacta del conjunto de datos de SECOP de la que proviene. Este instrumento garantiza la validez de contenido del análisis (Corral, 2009).

**b) Protocolo de limpieza y transformación (ETL)**

Conjunto de reglas lógicas documentadas para el tratamiento de valores nulos, registros duplicados, errores de digitación en fechas y valores atípicos extremos presentes en los registros de SECOP. Este protocolo actúa como instrumento de trazabilidad, haciendo auditable cada decisión de transformación o eliminación de registros (Sharifnia et al., 2025).

**c) Diccionario de datos**

Documento complementario que describe el significado operativo de cada campo empleado en el análisis, incluyendo las categorías válidas de variables cualitativas, las unidades de medida de las variables cuantitativas y las convenciones de codificación utilizadas por SECOP (Colombia Compra Eficiente, 2024).

### **3.7.4 Instrumentos de análisis (técnicos)**

**a) Módulo analítico en Python**

El procesamiento, transformación y análisis de los datos se realiza mediante un módulo de software implementado en Python, utilizando las bibliotecas pandas para la manipulación de datos tabulares, scikit-learn para la construcción de modelos de clasificación supervisada, y matplotlib/plotly para la generación de visualizaciones. Su lógica de procesamiento queda documentada en el código fuente del proyecto, garantizando la reproducibilidad completa de los resultados (Hernández et al., 2014).

**b) Tablero de visualización interactivo (dashboard)**

Tablero interactivo construido con las bibliotecas Dash y Plotly de Python que permite la exploración dinámica de los indicadores de desempeño contractual calculados —desviación de costo, desviación de tiempo e índice de adiciones—, facilitando la consulta e interpretación de los hallazgos por parte de usuarios no especializados en análisis de datos (Colombia Compra Eficiente, 2024).

### **3.7.5 Validez de los instrumentos**

La validez hace referencia al grado en que un instrumento realmente mide la variable que pretende medir (Corral, 2009). En esta investigación se distinguen dos dimensiones:

* Validez de contenido: las variables extraídas de SECOP corresponden directamente a los constructos definidos en el marco conceptual —valor adjudicado, plazo contractual, adiciones y estado de ejecución.  
* Validez de criterio: los indicadores calculados han sido utilizados en estudios previos de analítica de contratación pública como proxies válidos del desempeño en la ejecución contractual (Feigenbaum et al., 2024; Rodríguez Arévalo, 2021).

### **3.7.6 Confiabilidad de los instrumentos**

La confiabilidad se entiende como el grado en que el instrumento produce resultados consistentes ante condiciones similares de aplicación (Corral, 2009). En este proyecto se garantiza mediante tres mecanismos:

* Reproducibilidad: la extracción vía API con parámetros fijos y el procesamiento mediante código Python documentado permiten replicar exactamente el mismo conjunto de datos bajo las mismas condiciones de consulta.  
* Trazabilidad: el protocolo ETL y el diccionario de datos documentan cada transformación aplicada, haciendo auditable el proceso completo de limpieza.  
* Consistencia interna: las fórmulas de cálculo de los indicadores de desempeño se aplican de manera uniforme a todos los registros, eliminando la variabilidad subjetiva propia de instrumentos aplicados por personas (Sharifnia et al., 2025).

# **4\. CRONOGRAMA**

La siguiente tabla presenta el cronograma de actividades propuesto para el desarrollo del proyecto, distribuido en semanas a lo largo del semestre académico.

**Tabla 2\.**

*Cronograma de actividades del proyecto*

| Actividad / Fase | Mar S1 | Mar S2 | Mar S3 | Mar S4 | Abr S1 | Abr S2 | Abr S3 | Abr S4 | May S1 | May S2 | May S3 | May S4 | Jun S1 | Jun S2 | Jun S3 | Jun S4 | Jul S1 | Jul S2 | Jul S3 | Jul S4 | Ago S1 | Ago S2 | Ago S3 | Ago S4 |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| 1\. Revisión de literatura y ajuste del marco teórico | X | X | X | X |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 2\. Definición del modelo de datos y variables |  |  | X | X | X | X |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 3\. Extracción automatizada vía API Socrata/OData |  |  |  |  | X | X | X | X | X |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 4\. Estructuración del dataset (modelo estrella) |  |  |  |  |  |  |  | X | X | X | X |  |  |  |  |  |  |  |  |  |  |  |  |  |
| 5\. Depuración y limpieza de datos (ETL) |  |  |  |  |  |  |  |  |  | X | X | X | X |  |  |  |  |  |  |  |  |  |  |  |
| 6\. Construcción de indicadores (tiempo, costo, alcance) |  |  |  |  |  |  |  |  |  |  |  | X | X | X | X |  |  |  |  |  |  |  |  |  |
| 7\. Análisis descriptivo e inferencial |  |  |  |  |  |  |  |  |  |  |  |  |  | X | X | X | X |  |  |  |  |  |  |  |
| 8\. Diseño de visualizaciones y tablero interactivo |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | X | X | X | X |  |  |  |  |  |
| 9\. Validación de resultados y ajustes |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | X | X | X | X |  |  |  |
| 10\. Redacción del informe final |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | X | X | X | X | X |  |
| 11\. Revisión por el director de tesis |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | X | X | X | X |
| 12\. Correcciones y entrega final |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | X | X |

*Nota. S \= Semana. X indica semana de trabajo activo en la actividad. Elaboración propia.*

# **5\. PRESUPUESTO**

A continuación se presenta la estimación del presupuesto global del proyecto, desglosado por rubros principales: personal, materiales y suministros, y equipos e infraestructura tecnológica. Los valores expresados corresponden a pesos colombianos (COP).

**Tabla 3\.**

*Presupuesto global del proyecto*

| Rubro | Fuente Universidad | Fuente Propia | Otras Fuentes | Total (COP) |
| :---- | :---- | :---- | :---- | :---- |
| Personal (investigador principal) | $0 | $3.600.000 | $0 | $3.600.000 |
| Materiales y suministros | $0 | $150.000 | $0 | $150.000 |
| Equipos e infraestructura tecnológica | $0 | $500.000 | $0 | $500.000 |
| Difusión y divulgación | $0 | $200.000 | $0 | $200.000 |
| Imprevistos (5 %) | $0 | $222.500 | $0 | $222.500 |
| **TOTAL** | **$0** | **$4.672.500** | **$0** | **$4.672.500** |

*Nota. Los valores son estimados con base en dedicación horaria del investigador y costos de herramientas tecnológicas requeridas. Elaboración propia.*

**Tabla 4\.**

*Descripción de los gastos de personal*

| Nombre / Rol | Formación | Dedicación (h/semana) | Semanas | Valor hora (COP) | Total (COP) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Andres Telles / Investigador principal | Pregrado (en curso) | 10 | 36 | $10.000 | $3.600.000 |
| Director de tesis / Asesor metodológico | Doctorado / Maestría | 1 | 16 | $0 (institucional) | $0 |
| TOTAL |  |  |  |  | $3.600.000 |

*Nota. Elaboración propia.*

**Tabla 5\.**

*Descripción de los gastos de materiales y suministros*

| Ítem | Unidad | Cantidad | Valor unitario (COP) | Total (COP) |
| :---- | :---- | :---- | :---- | :---- |
| Papelería e impresión de informes | Global | 1 | $80.000 | $80.000 |
| Almacenamiento externo (USB/HDD) | Unidad | 1 | $70.000 | $70.000 |
| TOTAL |  |  |  | $150.000 |

*Nota. Elaboración propia.*

**Tabla 6\.**

*Descripción de los gastos de equipos e infraestructura tecnológica*

| Ítem | Justificación | Valor estimado (COP) |
| :---- | :---- | :---- |
| Computador portátil (uso compartido) | Procesamiento, programación y análisis de datos | $200.000 (depreciación estimada) |
| Acceso a internet de banda ancha | Extracción de datos y revisión bibliográfica | $180.000 (4 meses) |
| Servicios en la nube (Google Colab Pro o equivalente) | Procesamiento de grandes volúmenes de datos | $120.000 |
| TOTAL |  | $500.000 |

*Nota. Elaboración propia.*

# **REFERENCIAS BIBLIOGRÁFICAS**

Aboelazm, K. S., & Dganni, K. M. (2025). Public procurement contracts futurity: Using of artificial intelligence in a tender process. Corporate Law & Governance Review, 7(1), 60–72. https://doi.org/10.22495/clgrv7i1p6

Atkinson, R. (1999). Project management: Cost, time and quality, two best guesses and a phenomenon, its time to accept other success criteria. International Journal of Project Management, 17(6), 337–342. https://doi.org/10.1016/S0263-7863(98)00069-6

Birks, D., Masucci, M., Tompson, L., & Ignatans, D. (2024). \[Completar con datos completos del artículo — pendiente de verificación en base de datos institucional\].

Colombia Compra Eficiente. (2024). Manual para el uso de datos abiertos del SECOP. https://www.colombiacompra.gov.co

Contraloría General de la República \[CGR\]. (2024). Hallazgos en contratos ejecutados por la UNGRD 2021–2024. https://laotracara.co/destacados/la-contraloria-encontro-irregularidades-en-contratos-ejecutados-por-la-ungrd-por-cerca-de-5-billones

Corral, Y. (2009). Validez y confiabilidad de los instrumentos de investigación para la recolección de datos. Revista Ciencias de la Educación, 19(33), 228–247. http://servicio.bc.uc.edu.ve/educacion/revista/n33/art12.pdf

Corporación Cívica de Caldas. (2024, febrero 18). En los últimos 8 años casi la mitad de los contratos por licitación en Caldas han tenido retrasos y adiciones. https://www.corporacioncivicadecaldas.com/2024/02/en-los-ultimos-8-anos-casi-la-mitad-de-los-contratos-por-licitacion-en-caldas

Corporación Cívica de Caldas. (2025, junio 1). Prórrogas y adiciones en contratos de la Gobernación de Caldas entre 2024 y 2025\. https://www.corporacioncivicadecaldas.com/2025/06/prorrogas-y-adiciones-en-contratos-de-la-gobernacion-de-caldas-entre-2024-y-2025

Decreto 1082 de 2015 \[Gobierno de Colombia\]. Por medio del cual se expide el Decreto Único Reglamentario del sector administrativo de planeación nacional. 26 de mayo de 2015\. https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=61307

Departamento Nacional de Planeación \[DNP\]. (2015). Estudio descriptivo de la contratación pública 2011–2015. https://colaboracion.dnp.gov.co/CDT/Sinergia/Documentos/Estudio\_descriptivo\_Contratacion\_Publica\_Ficha.pdf

Feigenbaum, J., Luco, F., & Tintelnot, F. (2024). VigIA: Prioritizing public procurement oversight with machine learning models and risk indices. Data & Policy, 6, e83. https://doi.org/10.1017/dap.2024.83

Hernández Sampieri, R., Fernández Collado, C., & Baptista Lucio, P. (2014). Metodología de la investigación (6.ª ed.). McGraw-Hill.

IBM Corporation. (2021). CRISP-DM: A standard process for data mining. https://www.ibm.com/docs/en/spss-modeler/18.4?topic=dm-crisp-overview

International Organization for Standardization \[ISO\]. (2011). ISO 8000-2:2011 — Data quality. ISO. https://www.iso.org/standard/50798.html

Kimball, R., & Ross, M. (2013). The data warehouse toolkit: The definitive guide to dimensional modeling (3rd ed.). Wiley.

Ley 1712 de 2014 \[Congreso de Colombia\]. Por medio de la cual se crea la Ley de Transparencia y del Derecho de Acceso a la Información Pública Nacional y se dictan otras disposiciones. 6 de marzo de 2014\. https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=56882

Meredith, J. R., & Mantel, S. J. (2012). Project management: A managerial approach (8th ed.). Wiley.

National Institute of Standards and Technology \[NIST\]. (2015). NIST big data interoperability framework: Volume 1, definitions. NIST. https://doi.org/10.6028/NIST.SP.1500-1

Organization for Economic Co-operation and Development \[OECD\]. (2025). Governing with artificial intelligence: AI in public procurement. https://www.oecd.org/en/publications/governing-with-artificial-intelligence\_795de142-en/full-report/ai-in-public-procurement

Patel, R., Kumar, A., & Singh, M. (2025). Agentic AI in contract analytics: Harnessing machine learning for risk assessment and compliance in government procurement contracts. Open Journal of Applied Sciences, 15(3). https://doi.org/10.4236/ojapps.2025.153048

Project Management Institute \[PMI\]. (2021). A guide to the project management body of knowledge (PMBOK® Guide) (7th ed.). PMI.

Pulgarín Gómez, L., & Yepes Gómez, M. (2024). Análisis de la participación de oferentes en la contratación pública de obras civiles en Risaralda a partir de la migración entre plataformas del SECOP \[Tesis de pregrado\]. Repositorio Colombia Compra Eficiente.

Rodríguez Arévalo, S. (2021). Predicción de ineficiencias en la contratación pública de Bogotá \[Tesis de maestría, Universidad del Rosario\]. https://repository.urosario.edu.co/handle/10336/30915

Sharifnia, A., Griffiths, P., & Richardson, A. (2025). A primer of data cleaning in quantitative research. Journal of Advanced Nursing. https://pubmed.ncbi.nlm.nih.gov/40145308/

Unaciencia, Revista de Estudios e Investigaciones. (2021). Eficacia del Sistema Electrónico de Contratación Pública SECOP I y II. Unaciencia, 14(27). https://www.colombiacompra.gov.co

Welch, E., Rimes, H., & Bhullar, A. (2023). Open contracting data and procurement analytics: Trends and applications. Government Information Quarterly, 40(2). https://doi.org/10.1016/j.giq.2022.101800

[image1]: <data:image/png;base64,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>