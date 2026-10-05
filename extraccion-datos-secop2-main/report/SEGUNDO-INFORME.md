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
El presente informe parcial corresponde al periodo comprendido entre el 30 de marzo y el 7
de mayo de 2026, durante el cual se ha avanzado en la ejecución de la Fase II del proyecto,
denominada «Modelado Predictivo». Esta fase responde directamente al segundo objetivo
específico y comprende las actividades de selección de algoritmos candidatos y diseño
experimental, división estratificada del dataset en conjuntos de entrenamiento y prueba,
entrenamiento de modelos supervisados y calibración fina de hiperparámetros.
Si bien la Fase II se encuentra en estado avanzado de ejecución —dado que la calibración
fina de hiperparámetros mediante búsqueda aleatoria con validación cruzada se encuentra en
planeación inminente y la posterior evaluación detallada del modelo desde la perspectiva del
negocio corresponde a la Fase III—, los avances alcanzados hasta la fecha permiten reportar
resultados parciales sustantivos que se detallan en las secciones subsiguientes del presente
documento

# Avances del Proyecto
Descripción y cumplimiento de los objetivos y actividades realizadas
## Objetivos cumplidos
. Durante el periodo evaluado correspondiente al segundo informe de avance, el trabajo se ha
concentrado principalmente en el segundo objetivo específico del proyecto: desarrollar y validar
modelos predictivos basados en algoritmos supervisados, orientados a estimar la probabilidad de
ocurrencia de adiciones presupuestales o prórrogas en tiempo en los contratos de obra pública
analizados. De manera complementaria, se finalizaron las actividades pendientes del primer
objetivo específico —análisis exploratorio de datos y caracterización del comportamiento histórico
de la contratación de infraestructura— las cuales habían quedado en curso al cierre del informe
anterior, particularmente en lo relativo a la consolidación, depuración y validación final del dataset
analítico que sirve de insumo para la fase de modelado.
El segundo objetivo específico se encuentra en estado avanzado de ejecución, habiéndose
completado las actividades de selección de algoritmos candidatos, diseño experimental, división de
datos en conjuntos de entrenamiento y prueba, ingeniería y selección de variables, entrenamiento de
modelos supervisados de referencia y comparación cuantitativa entre ellos, mientras que la
calibración fina de hiperparámetros mediante búsqueda aleatoria, así como la evaluación de
desempeño desde la perspectiva del negocio y el análisis de errores, se encuentran planificadas para
las semanas inmediatamente siguientes dentro del cronograma original del proyecto. De forma
paralela y como esfuerzo complementario al modelado, se llevó a cabo el desarrollo y puesta en
producción de un pipeline automatizado de extracción de indicadores financieros habilitantes a
partir de los pliegos de condiciones publicados en el SECOP, el cual se ejecuta de manera
desatendida con el fin de enriquecer el conjunto de variables predictoras a medida que avanza el
proyecto. El tercer objetivo específico, relacionado con la implementación del prototipo de interfaz
de consulta inteligente basado en agentes RAG y Grandes Modelos de Lenguaje, no ha iniciado aún
por encontrarse fuera del alcance temporal del periodo reportado, conforme al cronograma original.

Actividades desarrolladas hasta el momento
Las actividades ejecutadas durante el periodo se corresponden, en su mayoría, con las
definidas en el plan de trabajo para la Fase II del proyecto, complementadas con el cierre de las
actividades aún pendientes de la Fase I. A continuación se describe el alcance de cada una.
En relación con el cierre de la validación del dataset estructurado para modelado (Actividad
1.5 de la Fase I), se consolidó la tabla analítica final mediante un proceso de depuración semántica e
ingeniería de variables que partió de la integración relacional entre las fuentes oficiales del SECOP.
El dataset resultante quedó constituido por 48.331 registros únicos de contratos de obra pública y 53
variables, entre las cuales se incluyen variables originales de la fuente, variables derivadas (como la
duración planificada del contrato, conteos de modificaciones por tipo, ventanas temporales de
adición e indicadores binarios de tipos de modificación), así como variables financieras
provenientes del Registro Único de Proponentes y los seis indicadores cuantitativos extraídos de los
pliegos de condiciones. Como parte de esta validación se identificaron y aislaron de manera
explícita catorce variables que, por su naturaleza post-contractual, constituyen riesgo de fuga de
información (data leakage) y que, por lo tanto, fueron excluidas del conjunto de predictores en todas
las fases subsecuentes del modelado.
Respecto a la selección de algoritmos candidatos y diseño experimental (Actividad 2.1), se
definió un conjunto inicial de cuatro modelos supervisados que cubre un espectro representativo de
aproximaciones a la clasificación binaria sobre datos tabulares: Regresión Logística como modelo
lineal interpretable utilizado como línea base de referencia; Random Forest como ensamble basado
en muestreo bootstrap y agregación de árboles; XGBoost como ensamble secuencial de gradient
boosting con manejo nativo de valores ausentes; y LightGBM como variante optimizada del
gradient boosting con eficiencia computacional superior. El diseño experimental se estructuró
considerando que el segundo objetivo específico del proyecto contempla la estimación de la
probabilidad de ocurrencia tanto de adiciones presupuestales como de prórrogas en tiempo, por lo
que se definieron dos variables objetivo binarias derivadas del dataset depurado: la variable
«tuvo_atraso», que indica si el contrato presentó al menos una extensión de plazo, con un balance
del 60,5 % positivos frente al 39,5 % negativos; y la variable «tuvo_sobrecosto», que indica si el
contrato presentó al menos una adición presupuestal, con una prevalencia del 83,4 % de positivos.
Esta dualidad de objetivos predictivos motivó posteriormente la adopción de una arquitectura
multi-target capaz de estimar ambas probabilidades de forma simultánea desde un único modelo.
Sobre la división de datos en conjuntos de entrenamiento y prueba (Actividad 2.2), se
aplicó un esquema de partición estratificada con una proporción 80 % para entrenamiento y 20 %
para prueba, utilizando una semilla aleatoria fija con el fin de garantizar la reproducibilidad de los
experimentos. Como resultado, el conjunto de entrenamiento quedó constituido por 38.664 registros

y el conjunto de prueba por 9.667 registros, conservando ambos la prevalencia de la clase positiva
en 60,48 % para la variable «tuvo_atraso», lo que confirma que el procedimiento de estratificación
fue exitoso. De manera previa al particionamiento, se ejecutó la fase de codificación de variables,
en la cual las variables categóricas de baja cardinalidad (con menos de veinte valores únicos) fueron
transformadas mediante codificación One-Hot, las variables categóricas de alta cardinalidad fueron
codificadas mediante Frequency Encoding por su capacidad de capturar la prevalencia relativa de
cada categoría sin introducir riesgo de fuga, y las variables numéricas con valores ausentes fueron
imputadas mediante la mediana, agregando un indicador binario por columna que preserva la
información de la ausencia original como predictor adicional. El resultado de este proceso es un
conjunto de entrada al modelado con 94 variables predictoras codificadas.
En cuanto al entrenamiento de modelos supervisados (Actividad 2.3), se entrenaron los
cuatro algoritmos seleccionados sobre el conjunto de entrenamiento utilizando configuraciones por
defecto ajustadas únicamente para compensar el desbalance de clases mediante los parámetros
«class_weight=balanced» en los modelos lineales y de bosque, y «scale_pos_weight» en los
modelos de gradient boosting. Para el target principal «tuvo_atraso», la evaluación inicial sobre el
conjunto de prueba arrojó valores del Área Bajo la Curva ROC (AUC-ROC) de 0,8301 para la
Regresión Logística, 0,8989 para Random Forest y 0,9015 para XGBoost, con valores de la métrica
F1 de 0,7862, 0,8457 y 0,8421 respectivamente. Estos resultados superan ampliamente el umbral
mínimo aceptable definido en el plan del proyecto (AUC-ROC ≥ 0,70) y permiten establecer una
línea base sólida sobre la cual se aplicarán las técnicas de calibración fina en la actividad
subsiguiente.
Como actividad complementaria al entrenamiento de la línea base, se aplicó un proceso
sistemático de selección de variables (feature selection) mediante una cascada de cuatro métodos:
filtrado por umbral de varianza, eliminación de redundancia por correlación entre pares de
variables, importancia por permutación sobre el modelo XGBoost previamente entrenado y
eliminación recursiva con validación cruzada. La intersección de las variables sobrevivientes a los
métodos de importancia por permutación y RFECV permitió reducir el conjunto de predictores de
94 a 30 variables, obteniéndose un modelo más parsimonioso que mantiene e incluso mejora
marginalmente todas las métricas de desempeño respecto a la versión completa, con un AUC-ROC
de 0,9036, un F1 de 0,8441 y una Precisión de 0,8808 sobre el conjunto de prueba. Este resultado
evidencia que aproximadamente dos terceras partes de las variables originalmente codificadas no
aportaban información útil para la tarea predictiva, y permite avanzar hacia la siguiente fase con un
modelo computacionalmente más eficiente y de mayor capacidad de generalización.
Con el fin de cubrir de manera integral el segundo objetivo específico del proyecto, que
demanda la predicción tanto de adiciones presupuestales como de prórrogas en tiempo, se desarrolló
posteriormente una arquitectura de modelado multi-target. Esta arquitectura permite que un único
modelo prediga simultáneamente las probabilidades de ambos eventos a partir del mismo vector de

variables de entrada. Se entrenaron dos variantes del modelo multi-target: la primera basada en
Random Forest con soporte nativo de salidas múltiples, y la segunda basada en XGBoost mediante
el envoltorio MultiOutputClassifier de scikit-learn, que entrena un estimador interno por cada
variable objetivo manteniendo una interfaz unificada. Los resultados sobre el conjunto de prueba
muestran que el Random Forest multi-target obtiene un AUC-ROC de 0,9047 para la predicción de
atrasos en plazo y de 0,8342 para la predicción de sobrecostos, mientras que XGBoost multi-target
obtiene 0,9035 y 0,8319 respectivamente. De manera notable, el desempeño del modelo multi-target
sobre la variable «tuvo_atraso» iguala o supera marginalmente al de los modelos especializados en
un único target del entrenamiento de línea base, lo que confirma que la arquitectura conjunta no
introduce penalización significativa en el desempeño y simplifica considerablemente el flujo de
despliegue posterior, al requerirse un único modelo en lugar de dos modelos independientes.
Respecto a la calibración de hiperparámetros mediante Grid Search o Random Search
(Actividad 2.4), esta actividad se encuentra en fase de planeación y ejecución inminente. El plan
contempla la aplicación de Random Search con ochenta iteraciones por modelo, sobre los dos
algoritmos con mejor desempeño en la línea base (Random Forest multi-target y XGBoost
multi-target), utilizando validación cruzada estratificada de cinco particiones. La selección de
Random Search sobre Grid Search responde a un criterio de eficiencia computacional, dado que el
espacio de búsqueda incluye variables continuas como la tasa de aprendizaje y la fracción de
submuestreo, donde una búsqueda exhaustiva resultaría prohibitiva sin garantizar mejoras
proporcionales al costo adicional.
Adicionalmente, y de forma paralela al desarrollo del modelado, se diseñó, construyó y
desplegó un pipeline automatizado de extracción de indicadores financieros habilitantes a partir de
los pliegos de condiciones publicados en el portal del SECOP. Este sistema fue containerizado
mediante Docker y publicado en Docker Hub para facilitar su despliegue en infraestructura de
servidor, y opera de manera desatendida iterando sobre los contratos pendientes mediante
navegación automatizada con Playwright, resolución de desafíos reCAPTCHA mediante el servicio
CapSolver y extracción de seis indicadores cuantitativos (índice de liquidez mínimo, nivel de
endeudamiento máximo, razón de cobertura de intereses, rentabilidad mínima sobre patrimonio y
sobre activo, y capital de trabajo como porcentaje del presupuesto) utilizando el modelo Gemini 2.5
Flash Lite. Los resultados se persisten de manera atómica en un archivo JSON local con copia de
seguridad automática hacia un bucket de Cloudflare R2 cada hora, y se envían notificaciones de
progreso y eventos críticos al dispositivo del estudiante mediante el servicio ntfy.sh. Al cierre del
periodo reportado, el pipeline ha procesado satisfactoriamente más de cuatro mil contratos y se
mantiene en ejecución continua para enriquecer progresivamente el dataset disponible para el
modelado predictivo a medida que avanza el proyecto.

Relación con los objetivos trazados en el plan de trabajo
El conjunto de actividades desarrolladas durante el periodo responde de forma directa y
completa al segundo objetivo específico del proyecto. La selección y entrenamiento de modelos
supervisados de clasificación, la división estratificada del dataset en conjuntos de entrenamiento y
prueba, la codificación e ingeniería de variables, la selección automatizada de predictores mediante
métodos de importancia por permutación y eliminación recursiva con validación cruzada, y la
construcción de la arquitectura multi-target capaz de estimar simultáneamente las probabilidades de
prórroga en plazo y de adición presupuestal constituyen el núcleo del proceso de modelado
predictivo que demanda dicho objetivo. Los resultados alcanzados al cierre del periodo —con
valores del Área Bajo la Curva ROC superiores a 0,90 para la predicción de atrasos y de 0,83 para
la predicción de sobrecostos— confirman que el modelo desarrollado cumple ambos componentes
del objetivo en una única arquitectura, simplificando el flujo de inferencia y reduciendo la
complejidad de mantenimiento que habría supuesto la operación de dos modelos independientes.
Es pertinente destacar que el cierre de la Actividad 1.5 de la Fase I, correspondiente a la
validación del dataset estructurado para modelado, se ejecutó como prerrequisito directo de la Fase
II, articulando de manera coherente las dos fases consecutivas del proyecto y consolidando un único
insumo analítico de 48.331 contratos y 53 variables sobre el cual se han apoyado todas las
experimentaciones posteriores. La identificación explícita de catorce variables con riesgo de fuga de
información, derivada del análisis exploratorio de la fase anterior, ha sido determinante para
asegurar la validez de los modelos entrenados y para descartar cualquier inflación artificial de las
métricas de desempeño obtenidas.
Adicionalmente, varias de las actividades ejecutadas durante el periodo trascienden el
alcance estricto del segundo objetivo específico y aportan insumos relevantes para fases futuras del
proyecto. El proceso de selección de variables redujo el conjunto de predictores de noventa y cuatro
a treinta variables sin pérdida de capacidad predictiva, lo que no solo mejora la eficiencia del
modelo, sino que aporta interpretabilidad al identificar qué atributos del contrato son
verdaderamente determinantes para la predicción de modificaciones, anticipando trabajo de
explicación y contextualización que será relevante para la implementación del prototipo RAG/LLM
contemplado en el tercer objetivo específico. De manera complementaria, el desarrollo del pipeline
automatizado de extracción de indicadores financieros habilitantes a partir de los pliegos de
condiciones del SECOP, además de enriquecer progresivamente el conjunto de variables disponibles
para el modelado, constituye un componente reutilizable que podrá integrarse al prototipo de
consulta inteligente del tercer objetivo específico, dado que los pliegos extraídos quedan
estructurados, persistidos y consultables como base de conocimiento auxiliar.

Finalmente, los hallazgos cuantitativos del entrenamiento de la línea base —tales como las
diferencias de capacidad predictiva entre modelos lineales y de ensamble, la confirmación de que
las variables relacionadas con la modalidad de contratación, el valor del contrato, la duración
planificada y la entidad contratante son las de mayor poder predictivo, y la verificación de que las
variables pliego_* aún no contribuyen significativamente al modelo debido a su baja cobertura
actual— constituyen evidencia empírica que orienta la siguiente fase de evaluación y refinamiento
del modelo, así como decisiones estratégicas sobre la priorización de esfuerzos de extracción de
datos en el periodo restante del proyecto.
Resultados parciales obtenidos
A continuación se presentan los entregables producidos durante el periodo evaluado, organizados
por tipo.
● Dataset analítico: Se consolidó el dataset definitivo para el modelado predictivo
(dataset_modelado.parquet), constituido por 48.331 registros únicos de contratos de obra
pública y 42 columnas que comprenden 39 variables predictoras y 3 variables objetivo
derivadas (tuvo_atraso_o_sobrecosto, tuvo_atraso y tuvo_sobrecosto). Este dataset es el
resultado del cierre de la Actividad 1.5 de la Fase I y representa la versión depurada y
validada del proceso de Ingeniería de Datos descrito en el informe anterior. Como
complemento al dataset principal, se generaron cuatro archivos derivados que materializan
la división estratificada del modelado: X_train.parquet (38.664 × 94) y X_test.parquet
(9.667 × 94) con la totalidad de variables codificadas, y los pares reducidos
X_train_reducido.parquet (38.664 × 30) y X_test_reducido.parquet (9.667 × 30) producto
del proceso de selección automatizada de variables. Adicionalmente, se persistió el archivo
freq_maps.pkl que documenta los mapas de codificación por frecuencia de las variables
categóricas de alta cardinalidad, requerido para garantizar la consistencia del proceso de
inferencia sobre datos nuevos.
● Modelos predictivos entrenados. Se entrenaron y persistieron seis modelos supervisados
que cubren el espectro de aproximaciones evaluadas durante el periodo. En la línea base de
modelado single-target sobre la variable «tuvo_atraso», se generaron tres modelos: una
Regresión Logística con escalado estándar incluido en el pipeline (lr.pkl), un Random
Forest con 300 árboles y compensación de clases (rf.pkl) y un XGBoost con 300
estimadores y profundidad máxima 6 (xgb.pkl). Posteriormente, en la fase de selección de
variables, se generó una versión reducida de XGBoost entrenada únicamente sobre las 30
variables seleccionadas (xgb_reducido.pkl). Finalmente, en la arquitectura multi-target
capaz de predecir simultáneamente atrasos y sobrecostos, se entrenaron dos modelos

definitivos: un Random Forest multi-output nativo (rf_multi.pkl) y un XGBoost envuelto
mediante MultiOutputClassifier (xgb_multi.pkl). Todos los modelos se persistieron en
formato joblib y constituyen artefactos reutilizables tanto para el ajuste fino de
hiperparámetros previsto para la siguiente actividad, como para la fase posterior de
evaluación.
● Métricas de desempeño. Se documentaron los resultados de evaluación de todos los
modelos sobre el conjunto de prueba en archivos CSV reproducibles. Para los modelos
single-target sobre «tuvo_atraso», las métricas obtenidas fueron de un Área Bajo la Curva
ROC de 0,8301 (Regresión Logística), 0,8989 (Random Forest) y 0,9015 (XGBoost), con
valores de F1 de 0,7862, 0,8457 y 0,8421 respectivamente. La versión reducida del
XGBoost con 30 variables registró un AUC-ROC de 0,9036 y un F1 de 0,8441, ligeramente
superior a su contraparte completa. La arquitectura multi-target alcanzó valores de
AUC-ROC de 0,9047 sobre «tuvo_atraso» y 0,8342 sobre «tuvo_sobrecosto» en el caso del
Random Forest, y de 0,9035 y 0,8319 respectivamente en el caso de XGBoost, confirmando
que la unificación de targets no degrada el desempeño respecto a los modelos
especializados. Las matrices de confusión, curvas ROC y desglose de Precisión y Recall por
clase se documentaron en archivos gráficos asociados a cada experimento.
● Selección automatizada de variables: Como entregable independiente, se documentó el
proceso de selección de variables mediante el archivo features_seleccionadas.csv, que
enumera las 30 variables sobrevivientes a la cascada de cuatro métodos aplicados (varianza,
correlación, importancia por permutación y RFECV) junto con un indicador binario por
método que documenta su trazabilidad. La comparativa cuantitativa entre el modelo
completo y el reducido se persistió en comparativa_feature_selection.csv, evidenciando que
la reducción del 68 % del conjunto de predictores no comprometió el desempeño y aportó
beneficios en eficiencia computacional y capacidad de generalización.
● Pipeline automatizado de extracción de indicadores pliego_*. Como entregable
adicional al modelado, se materializó un sub-proyecto containerizado de extracción de
indicadores financieros habilitantes a partir de los pliegos de condiciones del SECOP. El
pipeline fue construido en Python sobre la imagen base oficial de Microsoft Playwright para
Python, integra los servicios de CapSolver para resolución de reCAPTCHA y de Cloudflare
R2 para respaldo automático en la nube, y utiliza el modelo Gemini 2.5 Flash Lite para la
extracción semántica estructurada de los seis indicadores definidos. La imagen Docker
resultante (angeldev07/extractor-indicadores-secop:v1.0.0) fue publicada en Docker Hub
para facilitar su despliegue en infraestructura de servidor, e incorpora un mecanismo de
siembra de datos que permite reanudar el procesamiento desde el último estado guardado.
Al cierre del periodo, el sistema ha procesado satisfactoriamente más de setecientos
contratos y se mantiene en operación continua. La documentación operativa del pipeline
(DEPLOY_SERVER.md y OPERACION.md) acompaña la imagen como entregable
autónomo.

● Notebooks de experimentación. Se desarrollaron y ejecutaron cinco notebooks de
experimentación en formato Jupyter, organizados secuencialmente para garantizar la
reproducibilidad del proceso de modelado: 01_definicion_target_eda.ipynb (definición del
target y análisis exploratorio), 02_feature_engineering.ipynb (codificación, imputación y
división), 03_baselines.ipynb (entrenamiento de los tres modelos de línea base),
04b_feature_selection.ipynb (selección automatizada de variables) y
05_modelo_multi_target.ipynb (arquitectura multi-target). Cada notebook documenta sus
decisiones técnicas, resultados intermedios y conclusiones, y produce los artefactos
persistentes correspondientes (datasets, modelos y figuras). Adicionalmente, se generaron
resúmenes ejecutivos por día (dia_01_resumen.md a dia_04b_resumen.md) que sintetizan
los hallazgos y decisiones tomadas en cada etapa.
# Metodología Aplicada
Enfoque metodológico seguido en el trabajo
El desarrollo del presente trabajo dirigido continúa fundamentándose en la metodología
CRISP-DM (Cross-Industry Standard Process for Data Mining), conservando la estructura de seis
fases iterativas agrupadas en las cuatro fases operativas definidas en el plan de trabajo del proyecto.
Durante el periodo evaluado correspondiente al segundo informe de avance, el trabajo se ha situado
en las fases tercera y cuarta del ciclo CRISP-DM —preparación de los datos y modelado—, las
cuales convergen operativamente en la Fase II del plan de trabajo, con un cierre concurrente de la
fase tercera mediante la consolidación definitiva del dataset analítico requerido como insumo para
la modelación.
La fase de preparación de los datos, iniciada en el periodo anterior, se llevó a su cierre
durante este periodo mediante la ejecución de las tareas de codificación de variables categóricas,
imputación de valores ausentes con preservación de información mediante indicadores binarios,
identificación y exclusión explícita de variables con riesgo de fuga de información temporal, y
división estratificada de los datos en conjuntos de entrenamiento y prueba. La codificación se
diseñó atendiendo a la naturaleza de cada variable: One-Hot Encoding para variables categóricas de
baja cardinalidad y Frequency Encoding para variables de alta cardinalidad, criterio que respondió a
la necesidad de evitar la inflación dimensional propia de One-Hot sobre atributos como la entidad
contratante, el departamento o la ciudad, sin introducir riesgo de fuga propio de técnicas como
Target Encoding cuando se aplican sin validación cruzada.
La fase de modelado se ejecutó conforme a los principios de CRISP-DM mediante un
enfoque iterativo que partió de modelos sencillos hacia configuraciones progresivamente más
sofisticadas, validando los resultados intermedios antes de avanzar a la siguiente iteración. En
primera instancia, se entrenaron tres modelos de línea base con configuraciones por defecto y
compensación del desbalance de clases mediante los parámetros class_weight=balanced o

scale_pos_weight: una Regresión Logística como referencia interpretable, un Random Forest como
ensamble robusto, y un XGBoost como ensamble secuencial de gradient boosting. Posteriormente,
en una segunda iteración, se aplicó un proceso sistemático de selección automatizada de variables
que combina cuatro métodos complementarios (umbral de varianza, filtro por correlación,
importancia por permutación y eliminación recursiva con validación cruzada), permitiendo
retroceder a la fase de preparación de datos para refinar el conjunto de predictores. En una tercera
iteración se construyó la arquitectura multi-target que aprovecha el soporte nativo de Random
Forest para salidas múltiples y el envoltorio MultiOutputClassifier de scikit-learn para XGBoost,
configuración que permite predecir simultáneamente las probabilidades de prórroga en plazo y de
adición presupuestal manteniendo un único pipeline de entrenamiento e inferencia.
La aplicación de la metodología CRISP-DM en esta fase se evidencia particularmente en la
decisión de retroceder a la fase tercera tras observar los resultados iniciales del modelado: el análisis
de importancia por permutación reveló que aproximadamente dos terceras partes de las variables
originalmente codificadas no aportaban información útil al modelo, lo que motivó una reingeniería
del conjunto de predictores antes de avanzar a la fase de calibración fina. Este ciclo de
retroalimentación entre preparación y modelado es uno de los rasgos centrales del enfoque
CRISP-DM, y se ha respetado en lugar de avanzar de forma lineal hacia la calibración con un
dataset subóptimo.
Adicionalmente, todo el proceso de experimentación se ha desarrollado bajo principios
estrictos de reproducibilidad, fundamentales para la validez científica del proyecto. Cada notebook
utiliza una semilla aleatoria fija (random_state=42) en todos los procesos estocásticos —división de
datos, inicialización de modelos basados en bosques y validación cruzada—, los datasets
intermedios se persisten en formato Apache Parquet y los modelos entrenados en formato joblib con
versionado explícito por etapa, y los espacios de búsqueda de hiperparámetros, las métricas de
evaluación y las decisiones tomadas en cada iteración se documentan en archivos Markdown
asociados al sprint. Esta rigurosidad permite que cualquier resultado pueda ser reproducido y
auditado a posteriori, y constituye una buena práctica heredada del marco CRISP-DM cuando se
aplica en contextos académicos.
Como complemento al modelado predictivo, durante el periodo se aplicó una metodología
de ingeniería de software para la construcción del pipeline desatendido de extracción de indicadores
pliego_*, fundamentada en principios de containerización (Docker), idempotencia del estado
(escritura atómica de archivos JSON con respaldo automático en la nube), tolerancia a fallos
(reanudación automática tras crashes, mecanismo de marcas de intento y skip automático tras
múltiples fallos consecutivos sobre el mismo contrato) y observabilidad (notificaciones push al
dispositivo del estudiante mediante el servicio ntfy.sh). Esta metodología responde al requerimiento
operativo de ejecutar el pipeline en infraestructura de servidor remota durante varios días sin
intervención del estudiante, y materializa principios de buenas prácticas de despliegue de sistemas

que serán reutilizables en la Fase IV del proyecto cuando se desarrolle el prototipo de interfaz de
consulta inteligente.
Finalmente, la transición hacia la cuarta fase de CRISP-DM —evaluación— y hacia la Fase
III del plan de trabajo se encuentra programada para el periodo inmediatamente siguiente al cierre
del presente informe. Las actividades previstas incluyen la calibración fina de hiperparámetros
mediante Random Search con validación cruzada estratificada, la evaluación detallada del modelo
desde la perspectiva del negocio (curvas de ganancia, lift por decil, ajuste de umbral según costo
asimétrico de errores), y el análisis de falsos positivos y falsos negativos para identificar segmentos
del dataset donde el modelo presenta dificultades específicas y orientar futuras iteraciones de
ingeniería de variables.
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
del ciclo CRISP-DM, y durante el periodo evaluado se ha extendido el segundo nivel
correspondiente a la validación de modelos predictivos, que no había sido aplicable hasta ahora.
A nivel de datos, correspondiente a la fase de preparación, la validación se ha continuado
realizando mediante el contraste sistemático entre los registros consolidados y las estadísticas
reportadas por las fuentes originales, la verificación de integridad referencial entre tablas
(porcentajes de cobertura en los joins), el diagnóstico de duplicados y valores atípicos, y la
documentación de cada hallazgo en los informes de exploración. La aplicación de esta estrategia
durante el cierre de la Actividad 1.5 permitió, por ejemplo, validar que la integración final entre
contratos y modificaciones contractuales preserva la cardinalidad esperada (48.331 contratos
únicos) y que los conteos de modificaciones por tipo (variables n_modif_general, tiene_cesion,
tiene_suspension, entre otras) se corresponden con las observaciones individuales de la tabla de
adiciones a través de procedimientos de comprobación cruzada.
A nivel de modelo, correspondiente a la fase de modelado, se ha aplicado una estrategia
multifacética de validación que combina mecanismos preventivos contra el sobreajuste,
validaciones cuantitativas de desempeño y verificaciones empíricas de no-trivialidad. El primer
mecanismo, de carácter preventivo, consiste en la división estratificada del dataset en conjuntos de
entrenamiento (38.664 contratos, 80 %) y de prueba (9.667 contratos, 20 %) con preservación
exacta de la proporción de la clase positiva en ambos subconjuntos —60,48 % en cada caso para la
variable tuvo_atraso—, garantizando que las métricas reportadas se evalúan sobre datos que el
modelo nunca ha visto durante el entrenamiento y que ambos subconjuntos son comparables en
términos de balance de clases. El uso de una semilla aleatoria fija (random_state=42) asegura que
esta partición es reproducible entre ejecuciones.
El segundo mecanismo, de carácter cuantitativo, consiste en la evaluación simultánea de los
modelos mediante un conjunto de cinco métricas complementarias: el Área Bajo la Curva ROC
(AUC-ROC) como métrica principal de capacidad de ordenamiento independiente del umbral de
clasificación, la métrica F1 como medida balanceada entre precisión y exhaustividad, los valores
individuales de Precisión y Exhaustividad (Recall) para identificar trade-offs específicos según el

caso de uso, y la Exactitud (Accuracy) como referencia complementaria. La consideración de
múltiples métricas en lugar de una sola es deliberada: en problemas con desbalance leve a moderado
como el del presente proyecto, la Exactitud por sí sola puede resultar engañosa, por lo cual el
AUC-ROC y el F1 se priorizan como criterios principales de selección del modelo.
El tercer mecanismo, de carácter empírico, consiste en la verificación explícita de
no-trivialidad de los resultados mediante tres comprobaciones independientes. En primer lugar, se
verificó que los resultados no fueran producto de fuga de información temporal, mediante la
inspección de las variables más importantes según la importancia por permutación: ninguna de las
catorce variables identificadas como leakage en la fase de preparación (variables relacionadas con
conteos de modificaciones, ratios de extensión y ventanas temporales post-firma) aparece entre las
treinta variables seleccionadas como predictoras del modelo final. En segundo lugar, se verificó que
el desempeño obtenido es consistente entre algoritmos independientes: tanto Random Forest como
XGBoost convergen a valores de AUC-ROC en torno a 0,90 sobre la variable «tuvo_atraso», lo que
sugiere que la señal capturada es real y no atribuible a un artefacto específico de un algoritmo. En
tercer lugar, se contrastó el modelo entrenado contra una línea base trivial consistente en predecir
siempre la clase mayoritaria; mientras que dicho clasificador trivial obtendría una Exactitud del
60,5 % y un valor de F1 de 0,7547 sobre el target principal, los modelos entrenados superan
ampliamente estos umbrales, alcanzando F1 superiores a 0,84 y Exactitud por encima del 81 %, lo
que confirma que el modelo aporta valor predictivo sustancial respecto a la línea base trivial.
Adicionalmente, en la arquitectura multi-target se incorporó una estrategia de validación
específica consistente en la evaluación independiente de cada target sobre el mismo conjunto de
prueba, lo que permite identificar si el modelo conjunto compromete el desempeño en alguno de los
targets respecto a un modelo single-target equivalente. La comparación cuantitativa entre el
Random Forest multi-output y el Random Forest single-target sobre la variable tuvo_atraso arrojó
un AUC-ROC de 0,9047 frente a 0,8989 respectivamente, evidenciando que la unificación de
targets no degrada el desempeño y, en este caso particular, lo mejora marginalmente, lo cual
constituye un argumento empírico a favor de la arquitectura conjunta.
Para la siguiente fase del proyecto, correspondiente a la calibración de hiperparámetros, se
ha planificado complementar la validación actual con una estrategia de validación cruzada
estratificada de cinco particiones (5-fold Stratified Cross-Validation), que permitirá obtener
estimaciones más robustas del desempeño y reducir la sensibilidad de las métricas reportadas a la
partición específica de entrenamiento y prueba utilizada hasta el momento. Asimismo, en la fase de
evaluación correspondiente a la Fase III del plan de trabajo, se incorporarán estrategias de
validación desde la perspectiva del negocio mediante el análisis de la calibración de probabilidades
(Brier score, curva de calibración), el cálculo del lift por decil para evaluar la utilidad práctica del
modelo en escenarios de priorización, y el análisis detallado de falsos positivos y falsos negativos
para caracterizar los segmentos del dataset donde el modelo presenta dificultades específicas.

# Análisis de Resultados Parciales
Evaluación de los avances logrados frente a los objetivos iniciales.
La evaluación del progreso del proyecto al cierre del periodo evaluado se realiza objetivo
por objetivo, contrastando los entregables comprometidos en el plan de trabajo con los entregables
efectivamente producidos hasta la fecha.
Respecto al primer objetivo específico, relacionado con la realización de un análisis
exploratorio de datos para caracterizar el comportamiento histórico de la contratación de
infraestructura, identificando patrones, correlaciones y variables críticas asociadas a la eficiencia o
ineficiencia administrativa, el avance puede considerarse completo. Las actividades de extracción,
perfilado, integración y caracterización de las fuentes oficiales del SECOP, iniciadas durante el
periodo del primer informe, fueron cerradas durante el presente periodo con la consolidación del
dataset analítico final de 48.331 contratos y 53 variables. La caracterización del comportamiento
histórico se materializó tanto en los notebooks de exploración por fuente desarrollados en el periodo
anterior, como en los hallazgos cuantitativos del análisis exploratorio del notebook de definición de
target, que documentaron la prevalencia de cada tipo de modificación contractual en la población de
contratos de obra (89,1 % de contratos con al menos una modificación, 60,5 % con extensión de
plazo y 83,4 % con adición presupuestal), las correlaciones entre variables predictoras y variables
objetivo, y la variabilidad geográfica y por modalidad de contratación de la tasa de incidencia de
modificaciones. Adicionalmente, la identificación explícita de las variables críticas asociadas a las
modificaciones contractuales —modalidad de contratación, valor del contrato, duración planificada,
entidad contratante y origen de los recursos— se cuantificó mediante los métodos de importancia
por permutación aplicados durante la fase de selección de variables, ofreciendo evidencia empírica
sustentable sobre cuáles son los factores realmente determinantes en el comportamiento histórico de
la contratación.
En cuanto al segundo objetivo específico, relacionado con el desarrollo y validación de
modelos predictivos basados en algoritmos supervisados orientados a estimar la probabilidad de
ocurrencia de adiciones presupuestales o prórrogas en tiempo, el avance puede considerarse en
estado avanzado de ejecución, con cumplimiento total de la dimensión de desarrollo y
cumplimiento parcial de la dimensión de validación. La dimensión de desarrollo se cubre
íntegramente: se entrenaron seis modelos en total (Regresión Logística, Random Forest, XGBoost,
XGBoost reducido, Random Forest multi-target y XGBoost multi-target), abarcando tanto modelos
lineales como ensambles de árboles, y se construyó una arquitectura multi-target capaz de predecir
simultáneamente las dos variables objetivo del proyecto desde un único pipeline, lo cual cubre
integralmente los dos componentes mencionados explícitamente en el enunciado del objetivo. La
dimensión de validación se cumple parcialmente: las métricas estadísticas básicas (Área Bajo la
Curva ROC, F1, Precisión, Recall, Exactitud) fueron calculadas y documentadas para todos los
modelos sobre el conjunto de prueba, las verificaciones empíricas de no-trivialidad y ausencia de

fuga de información se ejecutaron mediante la importancia por permutación, y los resultados
confirman valores de AUC-ROC superiores a 0,90 para la predicción de atrasos y de 0,83 para la
predicción de sobrecostos, todos por encima del umbral mínimo aceptable definido en el plan del
sprint y en zona de "muy buena calidad" según la literatura de aprendizaje automático para
clasificación binaria. Sin embargo, las actividades de calibración fina de hiperparámetros mediante
búsqueda aleatoria con validación cruzada, así como la evaluación del desempeño desde la
perspectiva del negocio (lift por decil, ajuste de umbral, calibración de probabilidades) y el análisis
detallado de falsos positivos y falsos negativos por segmento del dataset, se encuentran en
planeación inminente y son las actividades que materializarán el cierre completo de la dimensión de
validación durante las semanas inmediatamente siguientes al cierre del presente informe, conforme
al cronograma original.
Respecto al tercer objetivo específico, relacionado con la implementación de un prototipo
de interfaz de consulta inteligente utilizando técnicas de agentes RAG y Grandes Modelos de
Lenguaje, el avance al cierre del periodo es nulo en términos de entregables formales del objetivo,
lo cual es consistente con el cronograma del proyecto que ubica esta fase entre las semanas 13 y 16.
No obstante, durante el periodo evaluado se desarrollaron componentes técnicos auxiliares que
sentarán las bases para la ejecución de este objetivo. En particular, el pipeline automatizado de
extracción de indicadores pliego_* constituye una primera experiencia operativa con modelos de
lenguaje de gran tamaño aplicados al dominio del proyecto (utilizando Gemini 2.5 Flash Lite para
extracción semántica estructurada de información financiera), y deja como subproducto un
repositorio de pliegos de condiciones procesados y persistidos que podrá utilizarse como base de
conocimiento del sistema RAG cuando se inicie formalmente esta fase. Asimismo, el modelo
predictivo entrenado durante el periodo será uno de los componentes que el agente inteligente del
prototipo final podrá consultar para responder preguntas en lenguaje natural sobre la probabilidad
de modificaciones contractuales en contratos específicos, articulando coherentemente los productos
de los tres objetivos específicos en una solución integrada.
En síntesis, el balance global del proyecto al cierre del periodo evaluado es favorable. El
primer objetivo específico se encuentra cumplido, el segundo objetivo se encuentra en estado
avanzado con la totalidad del desarrollo del modelo realizado y la validación parcialmente
ejecutada, y el tercer objetivo aún no inicia conforme al cronograma original. El cumplimiento del
cronograma del proyecto se mantiene dentro de los márgenes establecidos en el plan de trabajo, sin
atrasos significativos respecto a las fechas comprometidas, y los entregables producidos hasta el
momento exceden en algunos aspectos lo originalmente planificado, particularmente en lo relativo
al desarrollo del pipeline containerizado de extracción de indicadores que no estaba contemplado
explícitamente en el cronograma inicial pero que aporta valor al modelado y al despliegue posterior.

Identificación de Logros, Dificultades y Desviaciones del Plan
Logros: Durante el periodo evaluado se materializaron logros en cuatro dimensiones del
proyecto. En la dimensión de modelado, el principal logro fue el desarrollo de una arquitectura
multi-target que predice simultáneamente las dos variables objetivo definidas en el segundo objetivo
específico (atrasos en plazo y adiciones presupuestales), con valores del Área Bajo la Curva ROC
de 0,9047 y 0,8342 respectivamente, todos por encima del umbral mínimo aceptable establecido en
el plan del proyecto. La obtención de estas métricas en la línea base, sin haber aplicado todavía
calibración fina de hiperparámetros, constituye un indicador favorable sobre la calidad del dataset
construido durante la Fase I y sobre la pertinencia de las decisiones de modelado tomadas. En la
dimensión de ingeniería de variables, la aplicación sistemática de un pipeline de selección
automatizada de predictores permitió reducir el conjunto de variables del modelo de 94 a 30, sin
pérdida de capacidad predictiva y con mejoras marginales en todas las métricas evaluadas, lo que
evidencia que el modelo final es más eficiente computacionalmente y de mayor capacidad de
generalización que la versión inicial. En la dimensión de ingeniería de software, el desarrollo y
despliegue del pipeline desatendido de extracción de indicadores financieros habilitantes constituye
un logro adicional al alcance original del periodo, dado que aporta una herramienta operativa que
continuará enriqueciendo el dataset a lo largo de las semanas siguientes y cuya imagen Docker fue
publicada en Docker Hub para facilitar la reproducibilidad por parte de terceros. En la dimensión de
reproducibilidad y rigor científico, la persistencia de todos los artefactos del modelado (datasets
intermedios en formato Parquet, modelos serializados en joblib, mapas de codificación, métricas en
formato CSV y figuras en formato PNG) bajo una estructura de directorios consistente y con uso de
semillas aleatorias fijas garantiza que cualquier resultado pueda ser auditado y reproducido con
facilidad por evaluadores externos.
Dificultades:La ejecución del periodo presentó dificultades de tres tipos. La primera
dificultad, de naturaleza metodológica, consistió en la selección apropiada de la variable objetivo
principal del modelo. Durante el análisis exploratorio de los targets candidatos, se identificó que la
variable más amplia que combinaba ambos tipos de modificación contractual
(tuvo_atraso_o_sobrecosto) presentaba un balance del 89,1 % de positivos, lo cual habría
trivializado la tarea predictiva al permitir que un clasificador constante alcanzara 89 % de exactitud
sin aportar información útil. Esta observación motivó el descarte de la variable combinada como
target principal y la selección de la variable «tuvo_atraso» como objetivo de la línea base, decisión
que, si bien se considera correcta a posteriori, no estaba explícitamente prevista en el diseño
experimental inicial. La cobertura del segundo target («tuvo_sobrecosto») mediante una
arquitectura multi-target en lugar de un modelo separado fue la respuesta natural a esta limitación
inicial.

La segunda dificultad, de naturaleza relacionada con la calidad de los datos, consistió en la
elevada proporción de valores ausentes en algunas familias de variables. En particular, las seis
variables pliego_* provenientes de la extracción de los pliegos de condiciones presentaron una
cobertura inicial del orden del 2 al 3 %, dado que el pipeline de extracción se encontraba todavía en
etapa temprana de ejecución durante el periodo. De manera similar, las variables del Registro Único
de Proponentes (rup_*) presentaron tasas de valores ausentes del orden del 60 %. Esta dificultad se
abordó mediante una estrategia dual: por un lado, la imputación con la mediana acompañada de un
indicador binario que preserva la información de la ausencia original como predictor adicional; y
por otro, la verificación cuantitativa, mediante el análisis de importancia por permutación, de cuáles
de estas variables aportan o no señal predictiva al modelo. El resultado mostró que las variables
pliego_* aún no contribuyen significativamente al modelo en su estado actual de cobertura, por lo
cual quedó documentada la necesidad de revisar este punto cuando la cobertura aumente con el
avance del pipeline de extracción.
La tercera dificultad, de naturaleza técnica, surgió durante la operación del pipeline
desatendido de extracción de indicadores. Se identificaron y resolvieron incidentes operativos de
diversa naturaleza: errores de permisos sobre el sistema de archivos al ejecutar el contenedor con un
usuario no privilegiado, formatos heterogéneos de los documentos publicados en el SECOP
(algunos contratos publican únicamente archivos .doc o .docx en lugar de PDF), errores transitorios
de servicio del proveedor de modelos de lenguaje (códigos HTTP 503 por alta demanda en horas
pico), y casos de contratos específicos que generaban bloqueos del proceso de extracción en los
cuales el navegador automatizado quedaba en estado inconsistente. Cada uno de estos incidentes fue
abordado mediante mecanismos correctivos: ajustes de permisos en la imagen Docker, filtrado por
tipo de archivo, reintentos con retroceso exponencial sobre errores transitorios de la API, y un
mecanismo de marcas de intento con auto-skip tras dos fallos consecutivos sobre el mismo contrato
para evitar bucles infinitos. La acumulación de estas correcciones produjo una imagen final estable
y auto-recuperable, capaz de operar de manera desatendida durante días sin intervención de alguien.
Desviaciones del plan: Las desviaciones del plan original durante el periodo son de
naturaleza aditiva y no comprometen el cumplimiento de los objetivos del proyecto. La primera
desviación consiste en la incorporación, no contemplada explícitamente en el cronograma inicial, de
un proceso sistemático de selección automatizada de variables mediante una cascada de cuatro
métodos. Esta desviación se justifica por los hallazgos del entrenamiento de la línea base, que
sugerían la presencia de variables redundantes o de baja contribución predictiva, y por el principio
iterativo de CRISP-DM que motiva retroceder a la fase de preparación de datos cuando los
resultados del modelado lo requieren. La segunda desviación consiste en la adopción de una
arquitectura multi-target capaz de predecir simultáneamente ambas variables objetivo, en lugar de
entrenar dos modelos separados como se contemplaba inicialmente. Esta desviación se justifica por
las ventajas operativas de mantener un único pipeline de inferencia y por la verificación empírica de
que la arquitectura conjunta no introduce penalización en el desempeño respecto a los modelos

especializados. La tercera desviación, ya mencionada, es el desarrollo paralelo del pipeline
desatendido de extracción de indicadores pliego_*, esfuerzo no contemplado en el plan original
pero que constituye un componente reutilizable para fases posteriores del proyecto.
Adicionalmente, durante el periodo se reordenó el orden de prioridad de algunas actividades
planificadas internamente. En particular, la incorporación del modelo LightGBM como cuarto
algoritmo baseline, prevista en el diseño experimental original, fue desarrollada en formato de
notebook pero su ejecución completa se difirió en favor de avanzar con la arquitectura multi-target
sobre los dos algoritmos con mejor desempeño en la línea base (Random Forest y XGBoost), por
considerarse de mayor impacto para el cumplimiento del objetivo. La ejecución del notebook de
LightGBM se mantiene como tarea opcional para el periodo siguiente si las restricciones de tiempo
lo permiten.
En síntesis, las desviaciones identificadas no representan retrasos en el cronograma, sino
enriquecimientos del alcance original que aportan valor adicional al proyecto y materializan en
mayor profundidad los objetivos específicos comprometidos.
Medidas correctivas adoptadas en caso de ser necesarias.
Las medidas correctivas adoptadas durante el periodo evaluado responden a las dificultades
identificadas en la sección anterior y se aplicaron en tres ámbitos diferenciados: el modelado
predictivo, la calidad y completitud de los datos, y la operación del pipeline desatendido de
extracción de indicadores. A continuación se describe cada conjunto de medidas.
Medidas correctivas en el ámbito del modelado
La primera medida correctiva en este ámbito consistió en la reformulación de la variable
objetivo principal del modelo. Una vez detectado, durante el análisis exploratorio inicial, que la
variable combinada tuvo_atraso_o_sobrecosto presentaba un balance de clases del 89,1 % de
positivos —prevalencia que habría trivializado la tarea predictiva—, se decidió reorientar la línea
base hacia la variable tuvo_atraso, con un balance del 60,5 % positivos, mucho más apropiado para
tareas de clasificación binaria sin requerir técnicas adicionales de remuestreo. La cobertura del
segundo target (tuvo_sobrecosto), inicialmente postergada como objetivo secundario por su
desbalance del 83,4 %, se incorporó posteriormente al modelo mediante la adopción de la
arquitectura multi-target ya descrita, lo que permitió cumplir íntegramente el segundo objetivo
específico del proyecto sin sacrificar la calidad del modelo en ninguno de los dos targets.
La segunda medida correctiva consistió en la incorporación, no prevista inicialmente, de un
proceso sistemático de selección automatizada de variables. Tras el entrenamiento de la línea base,
la inspección del análisis de importancia por permutación y de la curva de eliminación recursiva con
validación cruzada evidenció que aproximadamente dos terceras partes de las variables

originalmente codificadas no aportaban información útil al modelo. La medida correctiva consistió
en aplicar una cascada de cuatro métodos complementarios (umbral de varianza, filtro por
correlación, importancia por permutación y eliminación recursiva con validación cruzada) y
conservar únicamente la intersección de las variables sobrevivientes a los dos métodos más
rigurosos. El resultado fue un dataset reducido de 30 variables que mantuvo e incluso mejoró
marginalmente todas las métricas de desempeño respecto a la versión completa, evidenciando que la
simplificación del modelo era pertinente y no comprometía sus capacidades predictivas.
Medidas correctivas en el ámbito de los datos
La principal dificultad relacionada con los datos fue la elevada proporción de valores
ausentes en algunas familias de variables, particularmente en las variables pliego_* (con cobertura
del 2-3 % al inicio del periodo) y en las variables rup_* (con cerca del 60 % de valores ausentes).
La medida correctiva adoptada consistió en una estrategia dual: por un lado, la imputación con la
mediana de cada columna acompañada de un indicador binario adicional (_was_nan) que preserva
como predictor la información de la ausencia original, lo que permite a los modelos basados en
árboles aprovechar la propia ausencia como una señal predictiva; y por otro, la verificación
cuantitativa de la utilidad de estas variables mediante la importancia por permutación, lo que
permitió documentar con evidencia empírica que las variables pliego_* aún no contribuyen
significativamente al modelo en su estado actual de cobertura, sin descartarlas definitivamente del
pipeline para que puedan reincorporarse cuando la cobertura aumente. Esta medida transforma una
limitación de los datos en información explotable y deja abierta la puerta a futuras mejoras del
modelo a medida que avance el pipeline de extracción.
Como medida correctiva complementaria al problema de cobertura de las variables
pliego_*, se priorizó la operación continua y desatendida del pipeline de extracción containerizado,
con el objetivo de incrementar la cobertura de estas variables a lo largo del periodo restante del
proyecto. El sistema fue diseñado para operar de forma autónoma durante días sin intervención del
estudiante, lo que permite que la cobertura crezca progresivamente y posibilita la reapertura del
análisis de la utilidad de estas variables en una iteración posterior del modelado.
Medidas correctivas en el ámbito operativo del pipeline desatendido
Durante la operación del pipeline desatendido de extracción de indicadores se identificaron
y corrigieron incidentes técnicos de diversa naturaleza, cada uno de los cuales motivó una medida
correctiva específica que quedó incorporada al diseño definitivo del sistema.
Frente al problema de errores de permisos sobre el sistema de archivos del contenedor,
derivado de la combinación entre la ejecución del proceso bajo un usuario no privilegiado y el
montaje de volúmenes temporales tipo tmpfs propiedad del usuario root, se adoptó la medida
correctiva de reubicar el directorio de archivos temporales a una ruta interna del contenedor

(/app/pdfs_tmp) propiedad del usuario operativo, eliminando la dependencia de tmpfs y resolviendo
definitivamente el conflicto de permisos.
Frente al problema de los formatos heterogéneos de los documentos publicados en el
SECOP (algunos contratos solo cuentan con archivos .doc o .docx en lugar de PDF), se adoptó la
medida correctiva de filtrar de antemano los documentos por extensión, procesando únicamente
archivos PDF y marcando como sin_pdfs los contratos cuya documentación no incluye este
formato, evitando así el desperdicio de recursos en intentos de procesamiento que invariablemente
fallarían.
Frente al problema de errores transitorios del servicio del modelo de lenguaje (códigos
HTTP 503 por alta demanda), se adoptó una medida correctiva basada en reintentos con retroceso
exponencial mediante la librería tenacity, configurando hasta cuatro intentos consecutivos con
tiempos de espera crecientes entre 4 y 60 segundos, y diferenciando entre errores transitorios
reintentables (error_api) y errores permanentes (error_api_permanente) que no se reintentan.
Frente al problema de contratos específicos que dejaban el navegador automatizado en
estado inconsistente, generando bucles potencialmente infinitos al reanudarse el contenedor, se
adoptaron tres medidas correctivas complementarias: la incorporación de un timeout global de 180
segundos por contrato que cancela el procesamiento en caso de que se exceda el tiempo razonable
para completarlo; la implementación de un mecanismo de marca de intentos persistido en el estado
de cada contrato, que incrementa un contador en cada inicio de procesamiento; y la implementación
de una lógica de auto-skip que descarta automáticamente como error irrecuperable cualquier
contrato que acumule dos o más intentos sin completarse, lo cual garantiza que el sistema se
autosane sin intervención del estudiante. Adicionalmente, se identificó que tras la resolución del
desafío reCAPTCHA la página del SECOP renueva los identificadores de los enlaces de descarga,
lo cual invalida las referencias previas; la medida correctiva consistió en re-navegar a la URL del
proceso después de cada resolución de reCAPTCHA para refrescar los identificadores antes de
intentar las descargas.
Medidas correctivas para la persistencia y recuperación de datos
Considerando que el pipeline desatendido produce resultados que deben preservarse a lo
largo de varios días de operación, se adoptaron medidas correctivas adicionales para garantizar la
integridad y disponibilidad de los datos producidos. La primera medida fue la implementación de
escritura atómica del archivo de resultados mediante el patrón de archivo temporal con renombrado
y sincronización al disco (tempfile + rename + fsync), de forma que cualquier interrupción abrupta
del proceso (apagón, kill del contenedor, fallo de hardware) no pueda corromper el archivo de
resultados. La segunda medida fue la implementación de un respaldo automático periódico del
archivo de resultados hacia un bucket en Cloudflare R2, sobrescribiendo el mismo objeto cada hora
para garantizar disponibilidad ante un eventual fallo del disco local sin saturar el almacenamiento

en la nube. La tercera medida fue la incorporación de copias rotatorias locales del archivo de
resultados cada 25 escrituras, manteniendo las últimas diez versiones en una subcarpeta de
respaldos, lo que ofrece una capa adicional de protección ante errores accidentales de manipulación
del archivo principal.
En síntesis, las medidas correctivas adoptadas durante el periodo evaluado han sido eficaces
para resolver los incidentes identificados y han contribuido a consolidar un sistema más robusto,
reproducible y operativamente estable de cara a las fases posteriores del proyecto.
# Conclusiones
Reflexión sobre el estado actual del trabajo
El periodo evaluado representa el cierre operativo de la Fase I del plan de trabajo y el
avance sustancial sobre la Fase II, articulando dos etapas que metodológicamente son inseparables:
la calidad y rigurosidad del proceso de Ingeniería de Datos ejecutado durante el periodo anterior se
ha visto reflejada de manera directa en la solidez de los resultados obtenidos en la fase de
modelado. La obtención, sin haber aplicado todavía calibración fina de hiperparámetros, de valores
del Área Bajo la Curva ROC superiores a 0,90 sobre la línea base de modelos para la predicción de
atrasos, y de 0,83 para la predicción de sobrecostos mediante la arquitectura multi-target, constituye
evidencia empírica de que las decisiones tomadas durante el primer informe sobre selección de
fuentes, ingeniería de variables, identificación de variables de leakage y construcción del esquema
relacional fueron acertadas, y que el dataset analítico producido captura efectivamente los factores
históricos asociados a las modificaciones contractuales en la contratación de obra pública en
Colombia.
Desde una perspectiva metodológica, el trabajo desarrollado durante el periodo confirma la
pertinencia del marco CRISP-DM como hilo conductor del proyecto. La iteratividad inherente a
esta metodología se manifestó concretamente en el retroceso desde la fase de modelado hacia la fase
de preparación de datos para refinar el conjunto de variables predictoras tras observar los resultados
de la línea base, en la reformulación del target principal tras detectar el desbalance trivial de la
variable inicialmente propuesta, y en la consolidación de la arquitectura multi-target tras reconocer
que el segundo objetivo específico del proyecto demandaba la cobertura simultánea de dos variables
predictivas. Estas iteraciones, lejos de constituir desviaciones del plan, son la materialización del
ciclo virtuoso de retroalimentación que CRISP-DM propone como principio fundamental para
proyectos de minería de datos.
Desde una perspectiva técnica, los resultados obtenidos posicionan al proyecto en una
situación favorable para enfrentar las fases restantes del plan de trabajo. El modelo predictivo

desarrollado se encuentra en niveles de desempeño calificados como muy buenos según la literatura
del aprendizaje automático para clasificación binaria con balance moderado, lo que ofrece un
margen amplio para que la calibración fina de hiperparámetros prevista para la siguiente actividad
permita refinamientos adicionales en lugar de tener que compensar deficiencias estructurales del
modelo. Asimismo, la verificación empírica de ausencia de fuga de información temporal mediante
el análisis de importancia por permutación, y la consistencia de resultados entre algoritmos
independientes, otorgan confianza sobre la validez de las métricas reportadas, descartando que sean
producto de artefactos del proceso de modelado.
Desde una perspectiva operativa, el desarrollo del pipeline desatendido de extracción de
indicadores constituye un aprendizaje técnico significativo del periodo. La construcción de un
sistema containerizado capaz de operar de manera autónoma durante días, recuperarse
automáticamente de fallos transitorios, persistir su estado de manera atómica y notificar incidentes
en tiempo real al estudiante representa una práctica de ingeniería de software de nivel profesional
aplicada a un contexto académico, y deja como aprendizaje la importancia de incorporar principios
de tolerancia a fallos, idempotencia y observabilidad en cualquier proceso de larga duración.
Adicionalmente, la publicación de la imagen Docker en un registro público constituye un primer
ejercicio de despliegue reproducible que será directamente reutilizable en la cuarta fase del
proyecto, cuando se desarrolle el prototipo de interfaz de consulta inteligente.
Como aspectos abiertos al cierre del periodo, conviene reconocer que la cobertura de las
variables pliego_* aún no es suficiente para que estas contribuyan significativamente al modelo, y
que el pipeline de extracción debe continuar operando para que esta limitación se resuelva
progresivamente; que la arquitectura multi-target con XGBoost, al utilizar un envoltorio de
scikit-learn, comparte hiperparámetros entre los dos targets internos, lo cual constituye un
compromiso aceptable pero perfectible si en alguna iteración futura las métricas de uno de los
targets se quedan rezagadas; y que la evaluación desde la perspectiva del negocio (lift por decil,
ajuste de umbral según costos asimétricos, calibración de probabilidades) y el análisis detallado de
falsos positivos y falsos negativos por segmento del dataset son tareas que materializarán el cierre
completo de la dimensión de validación del segundo objetivo específico durante las semanas
inmediatamente siguientes.
En cuanto a la proyección hacia las fases restantes, el cumplimiento sostenido del
cronograma original, la solidez de los entregables producidos hasta el momento y la articulación
coherente entre las tres fases ya en curso permiten afirmar con confianza razonable que el proyecto
se encuentra en condiciones de cumplir el alcance comprometido en el plan de trabajo dentro de los
plazos establecidos. La transición hacia la Fase III (evaluación) se realizará sin discontinuidades,
dado que los modelos entrenados, los conjuntos de datos persistidos y los marcos de medición ya
implementados durante el presente periodo constituyen los insumos directos de la fase siguiente. La
transición posterior hacia la Fase IV (despliegue del prototipo RAG/LLM) contará con varios

componentes técnicos auxiliares ya desarrollados durante este periodo —el modelo predictivo
entrenado, el repositorio de pliegos procesados, la experiencia operativa con modelos de lenguaje de
gran tamaño y la imagen Docker reutilizable— lo cual reduce significativamente el riesgo de
retrasos en la fase final del proyecto.
En síntesis, el estado actual del trabajo es satisfactorio. Los objetivos comprometidos para
el periodo evaluado se han cumplido, los entregables superan en algunos aspectos lo originalmente
planificado, las dificultades encontradas se han resuelto mediante medidas correctivas eficaces y el
proyecto se proyecta hacia las fases restantes con buenas perspectivas de cumplimiento integral del
alcance comprometido.
Sugerencias para mejorar el desarrollo del proyecto
Si bien el avance del proyecto al cierre del presente periodo se considera satisfactorio, la
experiencia acumulada permite formular un conjunto de sugerencias orientadas a optimizar el
desarrollo restante y a fortalecer la calidad de los entregables finales. Estas sugerencias se agrupan
en cinco ámbitos: enriquecimiento del conjunto de variables predictoras, exploración de algoritmos
adicionales, refinamiento de la metodología de validación, ampliación de la documentación
reproducible y consolidación de los aspectos operativos del despliegue final.
En el ámbito del enriquecimiento de variables, se sugiere mantener la operación continua
del pipeline desatendido de extracción de indicadores pliego_* durante el mayor tiempo posible del
periodo restante, con el objetivo de que la cobertura de estas seis variables alcance niveles que
permitan reincorporarlas como predictores significativos del modelo. Adicionalmente, podría
explorarse la incorporación de variables derivadas del historial de la entidad contratante (tasas de
adición y prórroga acumuladas en periodos anteriores), del historial del proveedor adjudicado
(cuando exista en el Registro Único de Proponentes) y de variables temporales asociadas al
momento de la firma del contrato (mes, año fiscal, ciclo electoral local), todas ellas candidatas
naturales para capturar dinámicas predictivas adicionales que el modelo actual no aprovecha.
En el ámbito de los algoritmos, se sugiere completar la ejecución del notebook de
LightGBM ya escrito, dado que su evaluación quedó pendiente en favor de avanzar con la
arquitectura multi-target, y se recomienda explorar de manera complementaria el algoritmo
CatBoost, que tiene un manejo nativo destacado de variables categóricas de alta cardinalidad y
podría ofrecer mejoras adicionales en este tipo de datos. En el caso de que la calibración fina de
hiperparámetros del Random Forest y XGBoost multi-target no produzca incrementos significativos
en las métricas, podría considerarse una breve exploración de modelos de redes neuronales
tabulares como FT-Transformer o TabNet, aunque esta exploración debe condicionarse al tiempo
disponible y al beneficio incremental esperado.

En el ámbito de la validación, se sugiere complementar la validación cruzada estratificada
prevista para la calibración de hiperparámetros con un esquema de validación temporal (time-aware
split), en el cual el conjunto de entrenamiento se construye con contratos firmados antes de una
fecha de corte y el conjunto de prueba con contratos posteriores. Esta validación adicional
permitiría verificar que el modelo no se basa en patrones específicos de un periodo histórico cerrado
y que conserva su capacidad predictiva sobre contratos nuevos, lo cual resulta especialmente
relevante para un sistema cuyo uso real implicaría predecir el comportamiento de contratos
firmados después del entrenamiento. Asimismo, se sugiere incorporar análisis de calibración
isotónica o sigmoide de las probabilidades predichas, que permita transformar las salidas del
modelo en estimaciones de probabilidad estadísticamente confiables y facilite su interpretación en
escenarios de toma de decisiones.
En el ámbito de la documentación, se sugiere consolidar al cierre del proyecto un
documento técnico unificado que integre las decisiones de modelado, los resultados experimentales
y las medidas correctivas adoptadas durante el sprint, en formato adecuado para acompañar el
repositorio de código en GitHub que constituye uno de los entregables comprometidos para la Fase
IV. Esta documentación complementaría los resúmenes ejecutivos por día generados durante el
sprint y facilitaría la comprensión integral del proyecto por parte de evaluadores externos y futuros
investigadores que deseen reproducir o extender el trabajo.
Finalmente, en el ámbito operativo, se sugiere planificar con anticipación la articulación
entre el modelo predictivo y el prototipo de interfaz inteligente que se desarrollará en la Fase IV,
definiendo desde ahora los contratos de interfaz (formato del payload de entrada, esquema de
respuesta, manejo de errores) que el agente RAG utilizará para consultar el modelo, y
documentando los criterios mediante los cuales el prototipo determinará si una pregunta del usuario
amerita invocar el modelo predictivo o si puede responderse exclusivamente desde la base
documental de pliegos. Esta planificación temprana reducirá la fricción en la fase final del proyecto
y permitirá una integración más fluida entre los productos de los tres objetivos específicos.
Expectativas para el informe final.
El informe final del proyecto, programado para el cierre de la Fase IV en la semana 16 del
cronograma, está concebido como un documento de síntesis que integrará los resultados
acumulados de las cuatro fases del trabajo dirigido bajo la metodología CRISP-DM. Las
expectativas sobre el contenido y los entregables que acompañarán dicho informe se organizan en
cuatro bloques.
En el bloque correspondiente a la metodología y los datos, se espera consolidar y actualizar
el diccionario de variables del proyecto con la versión final de los predictores efectivamente
utilizados por el modelo, documentar de manera definitiva las variables descartadas y las razones de
su descarte (incluyendo las catorce variables de leakage y las sesenta y cuatro variables eliminadas

durante la selección automatizada), y publicar el dataset analítico final en formato Apache Parquet
como insumo reproducible para futuros investigadores que deseen extender el trabajo. Se espera
asimismo que la cobertura de las variables pliego_* haya crecido significativamente respecto al
estado actual, gracias a la operación continua del pipeline desatendido, y que esta mejora pueda
traducirse en una nueva iteración del modelo que aproveche estas variables adicionales.
En el bloque correspondiente al modelado, se espera presentar el modelo final calibrado tras
la ejecución de la búsqueda aleatoria de hiperparámetros con validación cruzada estratificada,
acompañado de las métricas finales de desempeño tanto desde la perspectiva estadística (Área Bajo
la Curva ROC, F1, Precisión, Recall, Brier score, calibración) como desde la perspectiva del
negocio (lift por decil, curva de ganancia, recomendación de umbral según costos asimétricos). Se
espera que las métricas finales sobre la variable tuvo_atraso se ubiquen en valores de Área Bajo la
Curva ROC superiores a 0,91 y que las métricas sobre tuvo_sobrecosto superen 0,84, conforme al
margen de mejora esperable de la calibración fina sobre la línea base actual. Asimismo, se espera
entregar un análisis detallado de los segmentos del dataset donde el modelo presenta mayores
dificultades, identificando características de los contratos asociados a falsos positivos y falsos
negativos, lo que permitirá orientar futuras iteraciones del trabajo y servirá de insumo cualitativo
para el prototipo RAG de la Fase IV.
En el bloque correspondiente al prototipo de interfaz de consulta inteligente, se espera
materializar el tercer objetivo específico mediante un sistema funcional desplegado localmente que
permita al usuario formular preguntas en lenguaje natural sobre los contratos analizados (por
ejemplo, sobre la probabilidad de modificación de un contrato específico, sobre los factores de
mayor riesgo en una entidad o departamento determinado, o sobre las disposiciones financieras
habilitantes contenidas en un pliego en particular) y que produzca respuestas fundamentadas tanto
en el modelo predictivo entrenado como en la base documental de pliegos extraídos. Se espera que
este prototipo se construya sobre tecnologías de tipo LangChain o equivalente para la orquestación
del agente RAG, sobre Streamlit u otra alternativa para la interfaz de usuario, y que utilice un
modelo de lenguaje de gran tamaño (por ejemplo Gemini 2.5, Claude Sonnet o un modelo
open-source desplegable localmente) para la generación de respuestas. La integración de los tres
componentes —modelo predictivo, base documental y agente conversacional— constituirá la
culminación funcional del proyecto.
En el bloque correspondiente a la documentación y el cierre académico, se espera entregar
el repositorio de código completo del proyecto en GitHub bajo una estructura organizada por fases y
con instrucciones claras de instalación y reproducción de cada experimento, así como el documento
final del trabajo dirigido con la metodología completa documentada. Este documento final cubrirá
la justificación del problema, el marco teórico de los métodos utilizados, la descripción exhaustiva
del proceso desarrollado fase por fase, los resultados cuantitativos y cualitativos obtenidos, una
discusión crítica de las limitaciones encontradas y las consideraciones éticas asociadas al uso del

modelo en contextos de fiscalización pública. Se espera que el conjunto de entregables del informe
final permita evaluar de manera integral el cumplimiento de los tres objetivos específicos del
proyecto y demostrar que la combinación entre análisis exploratorio, modelado predictivo y agentes
conversacionales basados en grandes modelos de lenguaje constituye una aproximación viable y útil
para el análisis de riesgo de la contratación pública en Colombia.
Firmas del director y codirector del Trabajo dirigido
Firma del Codirector
Nelson Beltran Galvis
C.C. 79334324
Email: nelsonbeltran@ufps.edu.co

ANEXOS
Modelos preliminares entrenados data
Datasets definciones
Notebooks de experimentación notebooks
Pipeline Docker scripts de extraccion