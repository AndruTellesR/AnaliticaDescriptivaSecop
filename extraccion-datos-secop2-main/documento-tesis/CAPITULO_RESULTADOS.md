# Capítulo de resultados y discusión

## Nota preliminar

Este capítulo consolida los hallazgos verificados en `eda-extendido-integral/` (11 notebooks ejecutados sin errores, autoría de Camilo Andrés Telles Ramírez) y, como antecedente metodológico, en `analitica-descriptiva-andres/` (primera iteración del análisis). Toda cifra citada corresponde a la lectura **`universo_completo`** (48.331 contratos de obra pública), designada como oficial por instrucción del tutor en reunión de seguimiento, con el fin de mantener consistencia con el universo de datos trabajado por el compañero de tesis. Donde resulta pertinente para la robustez del hallazgo, se referencia adicionalmente la lectura `observable` (19.194 contratos, bajo el diseño metodológico original del anteproyecto: período 2018-2024 y estado de ejecución avanzado o finalizado) como análisis de sensibilidad.

El dataset integrado de entrada (procesos, contratos y proveedores de SECOP II) proviene de un pipeline de extracción compartido con el trabajo de grado del compañero, cuya autoría se encuentra pendiente de confirmación formal con el director. Todo el procesamiento, la estructuración, los indicadores y el análisis presentados en este capítulo son aporte propio e independiente: no se leyó, copió ni adaptó código del proyecto predictivo del compañero (`notebooks/07`, `notebooks/08`, `modelo_predictivo_global/`, `modelo-predictivo-preliminar/`).

---

## 1. Introducción del capítulo

El presente capítulo expone los resultados del análisis descriptivo de la contratación de obra pública en Colombia, organizados según los tres objetivos específicos que este componente del trabajo de grado atiende: la estructuración del dato analítico (OE-02), la normalización y calidad de los datos (OE-03), y la caracterización del desempeño contractual bajo el marco teórico de la restricción de hierro, que fundamenta adicionalmente el diseño del tablero interactivo (OE-04). Se presentan, en orden, la estructuración del universo de estudio, los indicadores de tiempo, costo y alcance, las segmentaciones exigidas por el instrumento RF-05, el análisis correlacional, y el contraste de las tres hipótesis formuladas en el anteproyecto (numeral 3.2). El capítulo cierra con la discusión teórica y las limitaciones declaradas del ejercicio.

---

## 2. Estructuración del dato analítico (OE-02)

Sobre el conjunto de contratos de obra pública integrados por el pipeline compartido (48.331 registros, deduplicados y con llave `id_contrato` única), se construyó un modelo dimensional simplificado, materializado sobre archivos Apache Parquet: una tabla de hechos con grano de un registro por contrato, y cinco tablas de dimensión que agrupan los atributos por tema (proceso, proveedor, entidad contratante, territorio y modalidad de contratación). La Tabla 1 resume la composición del modelo.

**Tabla 1.** *Modelo dimensional del dataset analítico*

| Tabla | Grano | Registros |
|---|---|---|
| Hechos (contratos) | 1 contrato de obra pública | 48.331 |
| Dimensión proceso | 1 proceso de compra | 43.451 |
| Dimensión proveedor | 1 proveedor único | 23.192 |
| Dimensión entidad | 1 entidad contratante única | 2.534 |
| Dimensión territorio | 1 combinación departamento-ciudad-orden | 848 |
| Dimensión modalidad | 1 modalidad de contratación única | 9 |

La integridad referencial entre la tabla de hechos y cada una de las dimensiones se verificó programáticamente, alcanzando una coincidencia del 100% en las cinco relaciones. El enriquecimiento del universo con las fuentes de procesos de contratación y de proveedores registrados —necesario para incorporar variables de competencia y de perfil de contratista, ausentes en el dataset integrado original— alcanzó una cobertura del 99,92% (48.293 de 48.331 contratos) para la fuente de procesos, tras deduplicar la llave de integración `id_del_portafolio` (que registraba 61.790 duplicados en la fuente cruda de procesos de contratación), y del 66,47% (32.126 de 48.331 contratos) para la fuente de proveedores registrados, medida a nivel de contrato.

Se declara explícitamente que este modelo dimensional es una estructuración simplificada sobre archivos planos, no un modelo estrella formal materializado en un motor de base de datos relacional o analítico, decisión adoptada dado el alcance descriptivo del trabajo y la ausencia de un motor de almacenamiento especificado en el anteproyecto original.

---

## 3. Calidad de datos y delimitación de la muestra analítica (OE-03)

Se definieron umbrales cuantitativos propios de calidad de datos —una variable se considera apta para el análisis si su nulidad no supera el 20%, de uso restringido entre el 20% y el 50%, y no apta por encima de ese límite—, ausentes hasta este ejercicio en cualquier documento del proyecto. Las variables que alimentan los indicadores de desempeño contractual resultaron todas aptas bajo este criterio.

Durante la depuración se identificó una inconsistencia propia de los registros de SECOP: **7.382 contratos** (sobre el universo completo de 48.331) presentan simultáneamente el campo `liquidación = "Sí"` y un estado de ejecución que el propio sistema registra como activo (por ejemplo, "En ejecución" o "Suspendido"), una contradicción lógica que no puede resolver el dato fuente por sí mismo, dado que un contrato no puede estar formalmente liquidado y en ejecución activa al mismo tiempo. Se documenta como hallazgo de calidad de datos citable sobre el propio SECOP, no como un defecto introducido por este análisis.

Se verificó también la brecha de reporte del campo `valor_pagado`: contrastado contra el valor adjudicado del proceso de origen, se confirma que la adjudicación consta en el sistema mientras que el pago frecuentemente no se reporta, lo que se interpreta como una brecha de reporte administrativo y no como ausencia real de ejecución financiera.

Como parte del diseño metodológico original del anteproyecto, se había delimitado un subconjunto de 19.194 contratos (39,7% del universo) aplicando los criterios de inclusión y exclusión de los numerales 3.6.3 y 3.6.4 —período 2018-2024 y estado de ejecución avanzado o finalizado—. Por instrucción del tutor, este capítulo reporta como cifra oficial el universo completo de 48.331 contratos; el subconjunto filtrado se conserva como análisis de sensibilidad y se referencia donde resulta pertinente.

---

## 4. Caracterización descriptiva general del universo de estudio

El universo de estudio, tras el filtro por `tipo_de_contrato = "Obra"` y la deduplicación por `id_contrato`, comprende 48.331 contratos de obra pública. La modalidad de contratación más frecuente es la Selección Abreviada de Menor Cuantía, seguida de la Licitación Pública Obra Pública y la Mínima Cuantía. En cuanto al tipo de contratista, las personas jurídicas individuales concentran la mayor proporción de proveedores únicos (11.254 de 23.192), seguidas de los consorcios y uniones temporales (9.378) y, en menor medida, las personas naturales (2.461).

El valor del contrato y los plazos (pactado y de ejecución) presentan distribuciones fuertemente asimétricas, con valores atípicos extremos heredados de inconsistencias ya documentadas en el dato fuente de SECOP (duraciones y precios base con magnitudes no verosímiles). Por esta razón, todo estadístico de tendencia central que se reporta en este capítulo corresponde a la mediana, y las visualizaciones del tablero interactivo aplican una winsorización en los percentiles 1 y 99 únicamente con fines de representación gráfica, sin alterar los valores originales de los indicadores.

---

## 5. Indicadores de desempeño contractual bajo la restricción de hierro

Los tres indicadores exigidos por el anteproyecto (numeral 3.3) se derivaron de forma completamente independiente al código del proyecto predictivo del compañero, a partir de la definición textual del propio anteproyecto y de las columnas crudas del dataset integrado.

### 5.1 Desviación de tiempo (deslizamiento del plazo contractual)

Se define como la diferencia, en días, entre el plazo real de ejecución (fecha de fin menos fecha de inicio del contrato) y el plazo pactado (obtenido mediante un parseo propio del campo de texto libre de duración contractual de SECOP). El indicador se calculó para 37.155 contratos (76,9% del universo), quedando sin dato válido aquellos cuyo plazo pactado no pudo interpretarse (por ejemplo, registros marcados como "No definido").

La mediana de la desviación de tiempo en el universo completo es de 1 día, y el 54,1% de los contratos con dato válido presenta un plazo real mayor al pactado (retraso). Restringiendo el análisis a los retrasos de magnitud material —superiores a 30 días—, la proporción es del 24,7%, cifra que se considera más defendible como indicador de incumplimiento de cronograma que el porcentaje bruto de cualquier desviación positiva, dado que desviaciones de pocos días pueden atribuirse al margen de imprecisión del parseo del plazo pactado.

### 5.2 Desviación de costo y el hallazgo sobre el valor inicialmente pactado

Aplicando literalmente la fórmula del anteproyecto —diferencia entre el valor pagado y el valor del contrato, como porcentaje del valor del contrato—, el indicador arroja una tasa de sobrecosto prácticamente nula: apenas el 0,13% de los 15.035 contratos con dato válido (31,1% del universo) presenta un valor pagado superior al valor del contrato. Esta cifra contrasta radicalmente con la magnitud citada en el planteamiento del problema del anteproyecto (aproximadamente uno de cada cuatro contratos con sobrecosto, según fuentes de control social).

La investigación de esta discrepancia constituye uno de los hallazgos analíticos más relevantes de este trabajo. Se contrastó el campo `valor_del_contrato` contra el `precio_base` del proceso de contratación de origen —la única aproximación disponible en los datos integrados al valor inicialmente estimado antes de la adjudicación—, restringiendo la comparación a procesos con un único contrato asociado para evitar ambigüedad de asignación. Sobre 39.938 procesos comparables, **el 23,63% de los contratos registra un valor superior al precio base en más de un 1%**, cifra que sí es consistente con la magnitud citada en el planteamiento del problema. Se verificó además el mecanismo que explica la diferencia: los contratos con al menos una adición de valor registrada presentan un exceso mediano del 17,05% sobre el precio base, frente al 0,00% de los contratos sin adiciones registradas. La interpretación que se sostiene, sin haber inspeccionado el código excluido del proyecto predictivo del compañero, es que el campo `valor_del_contrato` en el dataset de SECOP II refleja el valor **vigente al momento de la extracción**, ya actualizado tras las adiciones formales de valor, y no el valor originalmente pactado en la firma del contrato. Por esa razón, contrastarlo contra el valor pagado subestima sistemáticamente el sobrecosto real, mientras que contrastarlo contra el precio base del proceso lo revela.

Esta limitación se declara de forma explícita: `precio_base` no es estrictamente idéntico al "valor inicialmente pactado" que exige el anteproyecto, y no fue posible reconstruir dicho valor por diferencia de adiciones, dado que el dataset de adiciones de SECOP no incluye una columna de monto. El indicador sobre `precio_base` se adopta, en consecuencia, como la mejor aproximación disponible dentro de los datos ya integrados.

### 5.3 Índice de cumplimiento de alcance

Operacionalizado como una variable categórica de tres niveles —entregado en su totalidad, entregado parcialmente y no entregado—, a partir de las banderas de terminación anticipada, suspensión y cesión ya agregadas por el pipeline compartido de extracción. Sobre el universo completo, el 73,0% de los contratos se clasifica como entregado en su totalidad, el 16,5% como entregado parcialmente y el 10,5% como no entregado. Se declara como limitación que el indicador no distingue la categoría de "reducción del objeto contratado" mencionada en el marco teórico del anteproyecto, por ausencia de una variable cruda que la identifique de forma independiente.

---

## 6. Segmentación por modalidad, tipo de contratista y territorio

La segmentación de los indicadores de desempeño por las variables independientes declaradas en el anteproyecto (modalidad de contratación, tipo de contratista y territorio) revela patrones no uniformes entre categorías, insumo directo del tablero interactivo desarrollado para OE-04.

Por modalidad, la Licitación Pública Obra Pública presenta la mediana de desviación de tiempo más alta de todas las modalidades evaluadas, muy por encima de modalidades de menor competencia como la Selección Abreviada de Menor Cuantía o la Mínima Cuantía. Este patrón, contraintuitivo respecto a la hipótesis H0, se desarrolla en detalle en la sección 8.1.

Por tipo de contratista, los consorcios y uniones temporales presentan una mediana de desviación de tiempo superior a la de las personas jurídicas individuales y las personas naturales, pero una tasa de contratos "no entregados" inferior a la de las personas jurídicas —un patrón mixto que se desarrolla en la sección 8.2.

Por territorio, se observa heterogeneidad entre departamentos, con Bogotá D.C. —el departamento de mayor volumen de contratación de obra pública— concentrando además la mediana de desviación de tiempo más alta entre los departamentos de mayor volumen. La sección 8.3 examina si esta heterogeneidad territorial es generalizable o atribuible a la concentración de un único departamento.

La asociación entre modalidad de contratación e índice de cumplimiento de alcance resulta de magnitud moderada (V de Cramér), y la asociación entre tipo de contratista e índice de alcance, de magnitud débil a moderada, ambas estadísticamente significativas con un nivel de significancia de 0,05 declarado a priori.

---

## 7. Análisis correlacional y de asociación

Dada la asimetría severa verificada en las variables continuas (coeficientes de asimetría muy superiores a la unidad en el valor del contrato y en los plazos pactados), se empleó el coeficiente de correlación de Spearman, no paramétrico y robusto a valores atípicos, para las asociaciones entre variables continuas. Entre las relaciones evaluadas, la correlación entre el plazo pactado y el plazo contractual final resultó la más alta de la matriz, lo que respalda la fiabilidad del parseo propio del campo de texto libre de duración contractual, a pesar de la pérdida de información en aproximadamente una cuarta parte de los registros no interpretables.

Para las asociaciones entre variables categóricas y el índice de cumplimiento de alcance se empleó la prueba de chi-cuadrado de independencia, reportando en todos los casos el tamaño de efecto mediante la V de Cramér, no solo la significancia estadística. Ninguna de las asociaciones reportadas en este capítulo se interpreta en términos causales: el diseño del estudio es transversal y censal condicionado, no experimental.

---

## 8. Contraste de las hipótesis de investigación

Las tres hipótesis formuladas en el numeral 3.2 del anteproyecto se sometieron a pruebas estadísticas no paramétricas (Mann-Whitney U para comparaciones de dos grupos, Kruskal-Wallis para más de dos grupos), con un nivel de significancia declarado a priori de 0,05, reportando en todos los casos el tamaño de efecto —no únicamente el p-valor— y el tamaño de muestra efectivo de cada prueba. Se declara explícitamente que estas hipótesis fueron preregistradas en el anteproyecto y no constituyen exploración masiva de datos, por lo que no se aplicó corrección por comparaciones múltiples; en cualquier caso, los p-valores obtenidos se encuentran en órdenes de magnitud muy inferiores a cualquier corrección concebible.

### 8.1 Hipótesis H0 — Licitación pública y desviaciones de costo y tiempo

La hipótesis H0 planteó que los contratos adjudicados mediante licitación pública presentarían menores desviaciones de costo y tiempo que los adjudicados mediante modalidades de menor competencia, tales como la contratación directa o la selección abreviada, atribuyendo implícitamente esta diferencia a la mayor intensidad de competencia asociada a la licitación pública.

El contraste produce un resultado disociado por dimensión. En la dimensión de costo, la hipótesis se sostiene: la licitación pública presenta una desviación de costo significativamente menor (rank-biserial = +0,428, tamaño de efecto mediano; mediana de -9,18% frente a 0,00% en las modalidades de menor competencia; N = 2.793 frente a 12.242). En la dimensión de tiempo, la hipótesis se invierte: la licitación pública presenta un deslizamiento del plazo significativamente mayor (rank-biserial = -0,380, tamaño de efecto mediano; mediana de 26 días frente a 0 días; N = 6.611 frente a 30.544).

La premisa implícita del enunciado —que el mecanismo explicativo es la intensidad de la competencia— se verificó de forma independiente y se refuta. Se confirmó primero que la licitación pública efectivamente concentra un número de oferentes significativamente mayor que el resto de modalidades (rank-biserial = -0,593, tamaño de efecto grande). Sin embargo, al medir la competencia de forma directa mediante el número de oferentes únicos con oferta, su correlación con el deslizamiento del plazo resulta nula (ρ de Spearman = 0,051 en el universo completo, tamaño de efecto nulo) y su asociación con la desviación de costo es de magnitud pequeña. Es decir, la competencia por sí misma no explica el desempeño de plazo ni, en la magnitud observada, el de costo.

El análisis estratificado por rango de cuantía del contrato identifica la variable que sí opera: al repetir el contraste dentro de cada rango de valor, el efecto bruto de la modalidad sobre el deslizamiento del plazo (-0,380) se reduce a una magnitud media de 0,111 dentro de los estratos evaluables, una disminución del 70,7% (72,9% en el análisis de sensibilidad sobre el subconjunto observable). La licitación pública se concentra sistemáticamente en los contratos de mayor cuantía, de modo que buena parte del efecto atribuido a la modalidad es, en realidad, efecto de la escala y complejidad del proyecto, con la que la modalidad covaría.

En consecuencia, se propone como resultado de esta investigación la siguiente reformulación de H0, conservando el enunciado original como referencia: *los contratos de obra pública de mayor cuantía —entre los que la licitación pública es la modalidad predominante— presentan mayores deslizamientos del plazo contractual y menores desviaciones de costo que los de menor cuantía; la intensidad de la competencia, medida por el número de oferentes, no discrimina el desempeño de plazo*. La hipótesis original queda contrastada y su mecanismo explicativo, corregido con evidencia.

### 8.2 Hipótesis H1 — Consorcios y uniones temporales

La hipótesis H1 planteó que los contratos ejecutados por consorcios o uniones temporales presentarían un mayor índice de adiciones y modificaciones contractuales que los ejecutados por personas jurídicas individuales.

El contraste sostiene la hipótesis para el número total de modificaciones contractuales (mediana de 3 frente a 1, rank-biserial = -0,285, tamaño de efecto pequeño; N = 10.629 frente a 30.197), pero no la sostiene para las adiciones de valor monetario específicamente: aunque la diferencia resulta estadísticamente significativa por el gran tamaño de muestra, el tamaño de efecto es prácticamente nulo (-0,015) y las medianas de ambos grupos son idénticas (0,0), de modo que se rechaza explícitamente este resultado como evidencia sustantiva pese a su significancia. Al estratificar por rango de cuantía, el efecto sobre el número de modificaciones se reduce en un 70,6% dentro de los estratos, indicando que también aquí la cuantía del contrato explica una parte sustancial del patrón observado.

Un hallazgo adicional matiza la hipótesis en su dimensión de alcance: los consorcios y uniones temporales presentan, contra lo que H1 sugeriría, una tasa de contratos "no entregados" **menor** que la de las personas jurídicas individuales. El patrón que emerge es, por tanto, mixto: los consorcios acumulan más modificaciones contractuales durante la ejecución, pero no presentan peor desempeño de alcance final. Se declara además una limitación relevante para la caracterización del perfil de estos contratistas: la cobertura del registro externo de proveedores difiere fuertemente entre consorcios y personas jurídicas, por lo que las variables de perfil de proveedor (tipo de empresa, antigüedad) no se emplearon para caracterizar esta hipótesis sin ese sesgo declarado.

### 8.3 Hipótesis H2 — Heterogeneidad territorial

La hipótesis H2 planteó que los contratos de obra pública en municipios con mayores índices de necesidades básicas insatisfechas presentarían mayores desviaciones en tiempo y costo. Se declara, antes de presentar cualquier resultado, que **esta hipótesis no puede probarse con los datos disponibles**: el dataset integrado no contiene un índice de necesidades básicas insatisfechas por municipio, y su incorporación desde una fuente externa del DANE excede el alcance de este ejercicio de análisis sobre datos ya integrados.

Como aproximación exploratoria, no válida como prueba de H2, se evaluó la heterogeneidad territorial usando el departamento como proxy geográfico mediante la prueba de Kruskal-Wallis entre los ocho departamentos de mayor volumen de contratación. Se detectó heterogeneidad estadísticamente significativa tanto en tiempo como en costo. Sin embargo, un análisis de sensibilidad adicional —ausente en la primera iteración de este trabajo— revela que dicha heterogeneidad no es igualmente robusta en ambas dimensiones: al excluir el departamento de mayor volumen (Bogotá D.C.) del contraste, el tamaño de efecto en la dimensión de tiempo se reduce a una categoría nula o insignificante, mientras que en la dimensión de costo el tamaño de efecto se refuerza. Esto indica que la heterogeneidad territorial detectada en tiempo depende en gran medida de un único departamento dominante y no debe presentarse como evidencia de heterogeneidad territorial generalizada, mientras que en costo la heterogeneidad sí parece ser un fenómeno multidepartamental.

Se recomienda como trabajo futuro inmediato la incorporación del índice de necesidades básicas insatisfechas del DANE a nivel municipal, condición necesaria para una prueba válida de H2 tal como fue formulada.

---

## 9. Discusión: relación con el marco teórico de la restricción de hierro

Los resultados se interpretan bajo el marco de la restricción de hierro (Atkinson, 1999; Meredith & Mantel, 2012; PMI, 2021), que postula que tiempo, costo y alcance son dimensiones interdependientes del éxito de un proyecto, de modo que una intervención sobre una de ellas puede afectar a las demás. El hallazgo central de la hipótesis H0 —que la modalidad con mayor competencia mejora el desempeño de costo pero empeora el de tiempo— es consistente con esa interdependencia: el mecanismo que disciplina el costo (mayor escrutinio y competencia en la selección) no opera de la misma manera sobre el cronograma, y ambos efectos parecen mediados por una tercera variable, la escala del proyecto, con la que la modalidad de contratación covaría fuertemente en el marco normativo colombiano. Este hallazgo es coherente con la literatura de antecedentes citada en el anteproyecto (Rodríguez Arévalo, 2021; Feigenbaum et al., 2024), que documenta que los factores asociados a sobrecostos y a retrasos no siempre coinciden ni actúan en la misma dirección.

---

## 10. Limitaciones del análisis

1. El indicador de desviación de costo bajo la definición literal del anteproyecto (valor pagado frente a valor del contrato) subestima sistemáticamente el sobrecosto real, según se estableció en la sección 5.2; el indicador sobre `precio_base` se adopta como mejor aproximación disponible, con la salvedad de que no es idéntico al valor inicialmente pactado.
2. El índice de cumplimiento de alcance no distingue la "reducción del objeto contratado" por ausencia de una variable cruda específica en el dataset integrado.
3. La hipótesis H2 no pudo probarse por ausencia de datos de necesidades básicas insatisfechas a nivel municipal; el proxy departamental empleado no es NBI y así se declaró antes de presentar el resultado.
4. El análisis estratificado de H0 y H1 se realiza mediante estratificación univariada, no mediante regresión multivariada, decisión coherente con el alcance descriptivo del trabajo, pero que no descarta la existencia de otras variables de confusión no evaluadas.
5. Las variables extrañas reconocidas en el anteproyecto (fenómenos climáticos, orden público, cambios normativos, variaciones macroeconómicas) no fueron medidas ni controladas.
6. Ninguna asociación o diferencia reportada en este capítulo implica causalidad; el diseño del estudio es transversal y censal condicionado.
7. La autoría del pipeline compartido de extracción e integración de datos de entrada continúa pendiente de confirmación formal por parte del director de tesis.

---

## 11. Síntesis del capítulo

El análisis descriptivo del universo completo de 48.331 contratos de obra pública de SECOP II permitió estructurar un modelo de datos analítico con integridad referencial verificada, definir y aplicar por primera vez criterios cuantitativos de calidad de datos, y derivar de forma independiente los tres indicadores de la restricción de hierro exigidos por el anteproyecto. El hallazgo más relevante en términos de aporte metodológico es la resolución de la aparente contradicción entre la tasa de sobrecosto medida (prácticamente nula bajo la definición literal del anteproyecto) y la cifra citada en el planteamiento del problema, mediante el contraste independiente contra el precio base del proceso de origen, que confirma una tasa de sobrecosto del 23,63%, consistente con dicho planteamiento. En cuanto a las hipótesis de investigación, H0 resulta contrastada con un mecanismo explicativo distinto al enunciado (la escala del proyecto, no la competencia), H1 se sostiene parcialmente con un patrón mixto en la dimensión de alcance, y H2 se declara no probable con los datos disponibles, dejando explícita la vía para su contrastación futura.
