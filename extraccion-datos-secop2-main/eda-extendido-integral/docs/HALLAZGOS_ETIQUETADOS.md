# HALLAZGOS ETIQUETADOS — EDA extendido integral sobre el universo completo

Documento generado por `notebooks/11_sintesis_dual.ipynb`. No editar a mano: se regenera al reejecutar el cuaderno.

Autoria del ejercicio: **Andres Telles**. Los archivos de evidencia estan en `eda-extendido-integral/data/` y las figuras en `eda-extendido-integral/figuras/`.


---


## 1. Que significa cada etiqueta

| Etiqueta | Significado exacto |
|---|---|
| `[A-OE02]` | Sirve al objetivo de estructuracion del modelo de datos analitico de Andres Telles |
| `[A-OE03]` | Sirve al objetivo de normalizacion y calidad de Andres Telles |
| `[A-OE04]` | Sirve al objetivo de visualizacion y segmentacion de Andres Telles |
| `[A-H1]` `[A-H2]` `[A-H3]` | Aporta evidencia a esa hipotesis de Andres Telles |
| `[B-OE2]` | **Le seria util** al objetivo de EDA del compañero |
| `[B-OE3-insumo]` | Variable con asociacion relevante que **seria** candidata predictora. Informacion, no modelado |
| `[CALIDAD]` | Hallazgo sobre la calidad del dato SECOP, citable por cualquiera de los dos trabajos |

**Regla de honestidad.** Una etiqueta `[B-*]` significa que el hallazgo le seria util al compañero. No significa que sea del compañero, ni que el compañero lo haya producido, ni que Andres Telles haya trabajado para el compañero. La utilidad cruzada no transfiere autoria. Ningun resultado de este EDA se produjo con codigo del compañero, y ninguno se atribuye al compañero.


---


## 2. Distribucion del etiquetado (61 hallazgos)

| Etiqueta | Hallazgos | % de los hallazgos | Bloque |
|---|---|---|---|
| `[B-OE2]` | 36 | 59.0% | Utilidad para el Trabajo B (compañero) |
| `[CALIDAD]` | 28 | 45.9% | Calidad del dato SECOP |
| `[A-OE03]` | 23 | 37.7% | Trabajo A (Andres Telles) |
| `[B-OE3-insumo]` | 20 | 32.8% | Utilidad para el Trabajo B (compañero) |
| `[A-H1]` | 8 | 13.1% | Trabajo A (Andres Telles) |
| `[A-OE04]` | 8 | 13.1% | Trabajo A (Andres Telles) |
| `[A-OE02]` | 4 | 6.6% | Trabajo A (Andres Telles) |
| `[A-H2]` | 4 | 6.6% | Trabajo A (Andres Telles) |
| `[A-H3]` | 1 | 1.6% | Trabajo A (Andres Telles) |

Promedio de etiquetas por hallazgo: 2.16. Un mismo hallazgo puede servir a varios objetivos simultaneamente.


---


## 3. Tabla maestra de hallazgos

Cada cifra citada es verificable abriendo el cuaderno indicado y localizando la celda cuyo `execution_count` coincide con la referencia `cNNN`.

| ID | Notebook | Celda | Hallazgo | Etiquetas | Evidencia | Valor |
|---|---|---|---|---|---|---|
| H01-01 | 01 | `c006` | El join a procesos por id_del_portafolio deduplicado conserva el grano exacto: 48.331 contratos, id_contrato unico | [A-OE02] [B-OE2] | Cobertura 99.92% (48,293/48.331) | Alto |
| H01-02 | 01 | `c008` | La cobertura del registro de proveedores es 54.41% por proveedor unico pero 66.47% por contrato | [A-OE02] [CALIDAD] | 54.41% de 23,192 proveedores; 66.47% de 48.331 contratos | Medio |
| H01-03 | 01 | `c009` | La marca `observable` reproduce exactamente los 19.194 contratos aplicando 3.6.3/3.6.4 sobre el universo completo | [A-OE03] [CALIDAD] | Embudo de 6 pasos, retencion final 39.71% | Alto |
| H01-04 | 01 | `c013` | Dos variables de competencia de la fuente de procesos tienen varianza cero: proveedores_que_manifestaron y conteo_de_respuestas_a_ofertas | [CALIDAD] [B-OE2] | 1 valor distinto en las 48.331 filas, todo en cero | Alto |
| H01-05 | 01 | `c005` | Las variables de competencia son practicamente invariantes dentro de un mismo portafolio | [A-OE02] | Promedio de valores distintos por portafolio entre 1.000 y 1.264 | Medio |
| H01-06 | 01 | `c011` | Se rescata `es_grupo` desde el contrato: en el registro de proveedores tiene varianza cero, en el contrato distingue 3 tipos de contratista | [A-OE03] [A-H2] [B-OE3-insumo] | tipo_contratista: 4 categorias sobre 48.331 | Alto |
| H02-01 | 02 | `c009` | Sobre el universo completo hay 7.382 contratos con liquidacion registrada y estado aun activo, mas del doble de los 3.538 reportados por el EDA previo | [CALIDAD] [A-OE03] [B-OE2] | 7,382 sobre 48.331 (15.27%); 3,538 sobre el subconjunto filtrado | Alto |
| H02-02 | 02 | `c010` | La inconsistencia liquidado-activo no esta distribuida al azar: se concentra en pocas entidades y crece en los anios recientes | [CALIDAD] [B-OE2] | Las 10 entidades con mas casos acumulan 32.2% del total | Alto |
| H02-03 | 02 | `c006` | `precio_base` requiere depuracion previa: contiene valores negativos y magnitudes absurdas | [CALIDAD] [A-OE03] | minimo -397,166,484; maximo 13,212,285,859,000; utilizables 47,704 (98.70%) | Alto |
| H02-04 | 02 | `c008` | La fuente de adiciones arrastra 8.894 identificadores repetidos con contenido distinto que la eliminacion de filas identicas no resuelve | [CALIDAD] | 249,037 registros; 96,942 filas identicas; residuo 8,894 | Alto |
| H02-05 | 02 | `c012` | El 68.9% del universo registra valor_pagado en cero; el filtro de observabilidad lo reduce a 54.8% pero no lo resuelve | [CALIDAD] [A-OE03] [B-OE2] | 33,296 de 48.331 en el universo | Alto |
| H02-06 | 02 | `c004` | Ninguna columna de proceso incorporada supera el umbral de nulidad: la cobertura del join es del 99.92% y las variables llegan completas | [A-OE03] [B-OE2] | Clasificacion de nulidad por origen en la tabla de umbrales | Medio |
| H03-01 | 03 | `c004` | CONTRADICE PARCIALMENTE A N-01: la absorcion de la prorroga por fecha_de_fin es exacta en los contratos observables (mediana de la diferencia 0.0) pero solo parcial en el universo completo (mediana -9.0) | [A-OE03] [CALIDAD] | N efectivo 10,168 universo (mediana -9.0) y 3,847 observable (mediana 0.0) | Alto |
| H03-01b | 03 | `c005` | En los contratos 'En ejecucion' con prorroga registrada la fecha de fin todavia no refleja la extension completa | [CALIDAD] [B-OE2] | Tabla de mediana de la diferencia por estado_contrato entre los no observables | Medio |
| H03-02 | 03 | `c006` | El parseo propio de plazo pactado concuerda con la duracion declarada en la fuente independiente de procesos | [A-OE03] [CALIDAD] | Spearman rho = 0.766 sobre N efectivo 42,081; coincidencia exacta 62.2% | Alto |
| H03-03 | 03 | `c007` | La tasa de deslizamiento positivo depende criticamente del denominador y del universo: cuatro cifras correctas y distintas | [A-OE03] [CALIDAD] [B-OE2] | universo 41.57% sobre el conjunto y 54.07% sobre N efectivo; observable 51.17% y 60.16% | Alto |
| H03-04 | 03 | `c008` | Con umbral de retraso material de 30 dias, el retraso afecta al 27.8% del universo efectivo y al 32.3% del observable efectivo | [A-OE03] [B-OE2] | universo 24.66%, observable 32.33% | Alto |
| H03-05 | 03 | `c010` | La desviacion de costo mantiene su estructura tripartita en las dos lecturas, con la masa en el cero exacto | [A-OE03] [CALIDAD] [B-OE2] | observable (estricto): 0% exacto 52.49%, negativa 47.32%, positiva 0.18% (16 contratos); universo: 49.16% / 50.71% / 0.13% | Alto |
| H03-06 | 03 | `c010` | Los tres grupos de la estructura de costo tienen perfiles distintos: los de desviacion negativa son de mayor cuantia y mas licitacion publica | [B-OE2] [B-OE3-insumo] | Tabla de perfil por grupo de costo sobre el subconjunto observable | Medio |
| H03-07 | 03 | `c011` | El indice de alcance difiere 15.9 puntos entre lecturas y la diferencia es artefacto de observabilidad, no de desempeno | [A-OE03] [CALIDAD] | Entregado en su totalidad: 72.98% universo vs 57.11% observable | Alto |
| H04-01 | 04 | `c005` | El nivel de competencia mas frecuente es el de cero oferentes registrados, que es ausencia de reporte y no ausencia de competencia | [CALIDAD] [B-OE2] | 29.67% del universo y 24.75% del observable | Alto |
| H04-02 | 04 | `c007` | La premisa de A-H1 se verifica: la licitacion publica si concentra significativamente mas oferentes que el resto de modalidades | [A-H1] [B-OE2] | Mann-Whitney U = 48,961,585.5 / p = < 1e-300 / rank-biserial = -0.593 (grande) | Alto |
| H04-03 | 04 | `c011` | CONTRASTE CENTRAL: medida con competencia real, A-H1 NO se sostiene en la dimension de tiempo — el tamano de efecto es nulo | [A-H1] [B-OE2] [B-OE3-insumo] | Ver tabla h1_modalidad_vs_competencia.csv: efecto de modalidad de magnitud mediana frente a efecto de competencia nulo | Alto |
| H04-04 | 04 | `c010` | En la dimension de costo la competencia real si discrimina, aunque con efecto pequeno: a mayor competencia, desviacion de costo mas negativa | [A-H1] [B-OE3-insumo] | Rank-biserial positivo en costo con N efectivo declarado en la tabla de contraste | Alto |
| H04-05 | 04 | `c008` | El numero de oferentes correlaciona positivamente con la cuantia del contrato | [A-H1] [B-OE3-insumo] | Spearman en la tabla de correlaciones de competencia | Alto |
| H04-06 | 04 | `c004` | `n_respuestas` y `n_oferentes` son practicamente la misma variable: usar ambas seria redundancia | [B-OE3-insumo] [CALIDAD] | Spearman rho = 0.9949 | Medio |
| H05-01 | 05 | `c007` | N-K05 RESUELTO: el sobrecosto contra el presupuesto oficial del proceso es del orden del 24%, frente al 0.1% medido contra valor_del_contrato | [A-OE03] [B-OE2] [CALIDAD] | 1 contrato por proceso: 23.60% supera precio_base en mas del 1%; 34.66% supera el valor adjudicado; 0.04% con la definicion previa | Alto |
| H05-02 | 05 | `c007` | El exceso sobre el precio base es mayor en los contratos con adicion de valor registrada, lo que confirma el mecanismo propuesto | [A-OE03] [B-OE3-insumo] | Mann-Whitney con tamano de efecto reportado en la celda de veredicto | Alto |
| H05-03 | 05 | `c009` | Los contratos con pago en cero tienen valor adjudicado positivo en el proceso: la brecha es de reporte de ejecucion financiera | [CALIDAD] [B-OE2] | Tabla de contraste pago frente a valor adjudicado, en doble lectura | Alto |
| H05-04 | 05 | `c011` | El retraso material crece monotonicamente con la cuantia, pero la NO ENTREGA se comporta al reves: decrece al subir la cuantia | [A-OE04] [A-H1] [B-OE2] [B-OE3-insumo] | Perfil por rango de cuantia en doble lectura: retraso > 30 dias sube del rango bajo al alto; alcance 'No entregado' baja | Alto |
| H05-05 | 05 | `c010` | La cuantia y la modalidad estan fuertemente asociadas: la licitacion publica se concentra en los rangos altos | [A-H1] [B-OE2] | Columna pct_licitacion del perfil por cuantia | Alto |
| H05-06 | 05 | `c005` | `precio_base` y `valor_del_contrato` correlacionan fuerte pero no perfectamente, lo que hace del primero una referencia inicial utilizable | [A-OE03] [B-OE3-insumo] | Matriz de Spearman entre las cuatro magnitudes monetarias | Medio |
| H06-01 | 06 | `c004` | El criterio temporal 2018-2024 excluye mayoritariamente contratacion POSTERIOR a 2024, no historia antigua | [A-OE03] [CALIDAD] [B-OE2] | 10,762 contratos posteriores a 2024 frente a 244 anteriores a 2018 | Alto |
| H06-02 | 06 | `c004` | La retencion del filtro de observabilidad cae fuertemente en los anios recientes | [A-OE03] [CALIDAD] | Columna retencion_pct de la tabla anual | Alto |
| H06-03 | 06 | `c007` | Los indicadores de desempeno NO son estables en el tiempo: el retraso material y la no entrega varian entre anios de forma significativa | [A-OE04] [B-OE2] [B-OE3-insumo] | Kruskal-Wallis entre anios con epsilon2 reportado sobre el subconjunto observable | Alto |
| H06-04 | 06 | `c009` | La firma de contratos de obra esta concentrada en el ultimo trimestre del anio | [A-OE04] [B-OE2] | Tabla de estacionalidad mensual sobre 2018-2024 | Medio |
| H06-05 | 06 | `c011` | La primera modificacion contractual aparece tipicamente cerca del final del plazo vigente | [B-OE2] [B-OE3-insumo] | Mediana de la fraccion del plazo transcurrida hasta la primera modificacion, en doble lectura | Medio |
| H07-01 | 07 | `c004` | `es_pyme` discrimina el desempeno de plazo: los contratos de PYME presentan menor deslizamiento que los de no PYME | [A-OE04] [B-OE2] [B-OE3-insumo] | Mann-Whitney U = 24,323,628.0 / p = 8.42e-157 / rank-biserial = +0.245 (pequeno) / N efectivo = 9,649 (PYME) vs 6,677 (No PYME) / medianas 1.00 vs 9.00 | Alto |
| H07-02 | 07 | `c005` | `es_pyme` del contrato y `espyme` del registro concuerdan al 100%: son la misma variable con coberturas distintas | [CALIDAD] [A-OE02] | Concordancia del 100.00% sobre N efectivo 32,126 | Medio |
| H07-02b | 07 | `c005` | La antiguedad del proveedor no es calculable para consorcios y uniones temporales: no figuran en el registro externo | [CALIDAD] | Tabla de cobertura de antiguedad por tipo de contratista | Alto |
| H07-03 | 07 | `c009` | El mercado de obra publica tiene cola larga: la mayoria de los proveedores tiene un unico contrato y no hay contratistas dominantes | [B-OE2] [A-OE04] | 16,299 proveedores con un solo contrato (70.3%); top 10 acumula 2.73% de los contratos | Alto |
| H07-04 | 07 | `c010` | La reincidencia del contratista se asocia al desempeno: los proveedores con mas contratos muestran mayor retraso material | [B-OE2] [B-OE3-insumo] [A-OE04] | Kruskal-Wallis y chi-cuadrado con tamano de efecto reportados | Alto |
| H07-05 | 07 | `c008` | La antiguedad del proveedor mide antiguedad de la CUENTA en SECOP, no antiguedad empresarial | [CALIDAD] | N efectivo 28,947; maximo observado en torno a 11 anios, coherente con la vida de la plataforma | Alto |
| H07-06 | 07 | `c007` | El tipo de empresa del registro discrimina el desempeno de plazo entre las formas societarias principales | [B-OE2] [B-OE3-insumo] | Kruskal-Wallis entre los 8 tipos de empresa mas frecuentes, con N efectivo declarado | Medio |
| H08-01 | 08 | `c005` | La suspension y la extension de plazo co-ocurren muy por encima de lo esperado por azar | [B-OE2] [B-OE3-insumo] | Matriz de co-ocurrencia y chi-cuadrado con V de Cramer reportado | Alto |
| H08-02 | 08 | `c008` | El indice de alcance es robusto al orden de precedencia: invertir la jerarquia reclasifica menos del 1% de los contratos | [A-OE03] | 564 contratos observables tienen mas de una de las tres banderas (2.94%) | Alto |
| H08-03 | 08 | `c009` | La tasa de extension crece monotonicamente con la duracion pactada, del rango mas corto al mas largo | [A-OE04] [B-OE2] [B-OE3-insumo] | Gradiente por duracion discretizada en doble lectura, con chi-cuadrado y Kruskal-Wallis | Alto |
| H08-04 | 08 | `c011` | El numero de modificaciones se asocia al deslizamiento del plazo y a la cuantia del contrato | [B-OE3-insumo] [B-OE2] | Spearman con N efectivo declarado sobre el subconjunto observable | Medio |
| H09-01 | 09 | `c008` | La variable categorica con mayor asociacion al desempeno es `rango_cuantia` frente a retraso_material_mayor_30d | [B-OE2] [B-OE3-insumo] [A-OE04] | V de Cramer = 0.351, N efectivo = 16,326, moderado | Alto |
| H09-02 | 09 | `c004` | Todas las variables continuas del analisis presentan asimetria severa, lo que descarta Pearson por verificacion y no por supuesto | [A-OE03] | 14 de 16 variables con /skew/ > 1 | Medio |
| H09-03 | 09 | `c007` | Frente a los tres indicadores de la restriccion de hierro ninguna variable anticipatoria supera el tamano de efecto mediano; solo el numero de modificaciones alcanza efecto grande con la cuantia | [B-OE2] [B-OE3-insumo] | maximo /rho/ anticipatorio: valor_del_contrato ~ deslizamiento_plazo_dias = 0.3794 (mediano, N efectivo 16,326) | Alto |
| H09-04 | 09 | `c010` | Las variables con mayor asociacion al desempeno son mayoritariamente NO anticipatorias: se conocen durante o despues de la ejecucion | [B-OE3-insumo] [CALIDAD] | Tabla de variables candidatas con su momento de disponibilidad | Alto |
| H09-05 | 09 | `c005` | El sobrecosto sobre el precio base se comporta como un indicador distinto de la desviacion de costo previa, con su propio patron de asociaciones | [A-OE03] [B-OE2] | Fila correspondiente en la matriz de Spearman extendida | Alto |
| H10-01 | 10 | `c004` | A-H1 se invierte en tiempo y se sostiene en costo, en el universo completo (lectura oficial) y de forma consistente en el subconjunto observable, con el indicador de sobrecosto redefinido | [A-H1] [B-OE2] | Universo completo (lectura oficial), deslizamiento: rank-biserial -0.3798; observable (sensibilidad): -0.3862; costo: positivo con efecto mediano en ambas lecturas | Alto |
| H10-02 | 10 | `c006` | El efecto de la modalidad sobre el deslizamiento del plazo se reduce sustancialmente al estratificar por cuantia | [A-H1] [A-OE03] [B-OE2] | efecto bruto 0.3798 frente a magnitud media dentro de estratos 0.1113 | Alto |
| H10-03 | 10 | `c008` | A-H2 se sostiene en modificaciones totales, NO se sostiene en adiciones de valor pese al p-valor significativo, y se invierte en alcance | [A-H2] [B-OE2] | Tabla de contraste de A-H2 en doble lectura, con tamano de efecto por variable | Alto |
| H10-04 | 10 | `c009` | El efecto de A-H2 tambien se reduce al controlar por cuantia, aunque menos que el de A-H1 | [A-H2] [A-OE03] | reduccion del 73.6% al estratificar | Alto |
| H10-05 | 10 | `c012` | CONTRADICE AL EDA PREVIO: la heterogeneidad territorial en TIEMPO se desvanece al excluir el departamento dominante; en COSTO se refuerza | [A-H3] [B-OE2] [CALIDAD] | epsilon2 en tiempo (observable) pasa de 0.0577 a 0.0098; en costo de 0.0303 a 0.0522 | Alto |
| H10-06 | 10 | `c011` | El peso del departamento dominante aumenta tras el filtro de observabilidad | [CALIDAD] [A-OE03] | Comparacion de la participacion del departamento dominante entre universo y observable | Alto |
| H10-07 | 10 | `c010` | El perfil de proveedor del registro externo no puede usarse para caracterizar A-H2 sin sesgo, porque su cobertura difiere fuertemente entre consorcios y personas juridicas | [CALIDAD] [A-H2] | Columna cobertura_registro_pct del perfil comparado | Alto |
| H10-08 | 10 | `c008` | `n_extension` del pipeline compartido es una bandera binaria, no un conteo: no puede sostener una prueba de 'mayor indice de extensiones' | [CALIDAD] | 2 valores distintos (0 y 1) en las 48.331 filas; la prueba de A-H2 sobre esa variable devuelve p = 1.0 y efecto exactamente 0 | Medio |

---


## 4. Notas de cada hallazgo

| ID | Nota |
|---|---|
| H01-01 | Sin deduplicar, id_del_portafolio repite 61.790 filas y el join inflaria el universo |
| H01-02 | El EDA previo cito 54.4% sin declarar la unidad; los proveedores registrados concentran mas contratos |
| H01-03 | El paso de mayor perdida es el filtro temporal 2018-2024: 16.156 contratos |
| H01-04 | Matiza la brecha 1 del documento comparativo: la brecha se cierra con menos variables de las enunciadas |
| H01-05 | Justifica que la regla de deduplicacion no sesga la distribucion de competencia |
| H01-06 | Extension del insight N-07 |
| H02-01 | La cifra previa se calculo despues de cuatro filtros; la cifra sobre el universo es la correcta para caracterizar la fuente |
| H02-02 | Sugiere practica de reporte de entidad, no error aleatorio de captura |
| H02-03 | Regla declarada: 0 < precio_base <= 1e13; no se imputa ni se eliminan filas, se marca |
| H02-04 | Afecta a las agregaciones de modificaciones por contrato que este EDA si utiliza |
| H02-05 | Extension de N-K04 al universo completo |
| H02-06 | El bloque de proveedor si tiene nulidad estructural del 33.5% por cobertura del registro |
| H03-01 | N-01 se sostiene donde fue formulado pero no se generaliza al universo; la absorcion se completa al cierre del contrato |
| H03-01b | Refina N-01: la actualizacion de fecha_de_fin es progresiva, no instantanea |
| H03-02 | Cierra N-08 con una fuente externa al contrato, no con coherencia interna |
| H03-03 | Aplica la correccion N-05 desde el inicio; ninguna cifra se reporta sin denominador |
| H03-04 | Cifra defendible ante escrutinio: separa retraso material de ruido de calendario |
| H03-05 | La masa en cero exacto es cierre administrativo, no ejecucion financiera |
| H03-06 | Caracteriza quien esta en cada grupo, no solo cuantos son |
| H03-07 | Es el argumento empirico que justifica el filtro de observabilidad |
| H04-01 | Obliga a excluir el cero del contraste de A-H1 en lugar de tratarlo como competencia minima |
| H04-02 | Sin esta verificacion, usar la modalidad como variable indirecta de competencia seria injustificado |
| H04-03 | El efecto atribuido a la competencia era en realidad efecto de la modalidad, confundida con la escala del proyecto |
| H04-04 | Replica la disociacion tiempo/costo de N-K01 con la medida directa en lugar de la indirecta |
| H04-05 | Es el mecanismo que confunde el efecto modalidad con el efecto escala; se controla en el notebook 10 |
| H04-06 | Relevante para cualquier seleccion posterior de variables |
| H05-01 | Confirma que `valor_del_contrato` es el valor vigente tras adiciones y no el inicial pactado; concilia la medicion con el planteamiento del problema |
| H05-02 | Evidencia de mecanismo, no solo de magnitud |
| H05-03 | Cierra N-K04 con evidencia de una segunda fuente |
| H05-04 | Cierra la brecha 3. El gradiente opuesto de las dos dimensiones desaconseja hablar de 'peor desempeno' sin especificar la dimension |
| H05-05 | Es la confusion que obliga a estratificar A-H1 por cuantia en el notebook 10 |
| H05-06 | Si la correlacion fuese 1 el contraste de N-K05 seria vacuo |
| H06-01 | Responde a la objecion de que el filtro 'descarta datos': descarta contratacion reciente aun no observable |
| H06-02 | Es el efecto de truncamiento esperado y debe declararse como limitacion del corte |
| H06-03 | El anio de firma es una variable con asociacion no trivial; conviene reportarlo junto a cualquier tasa global |
| H06-04 | Patron de ejecucion presupuestal de fin de vigencia; relevante para la interpretacion de la planeacion |
| H06-05 | Recupera un analisis del pipeline compartido con derivacion propia; util como variable temporal |
| H07-01 | Cierra la brecha 7: la variable estaba disponible al 100% y sin usar. El efecto puede estar confundido con la cuantia |
| H07-02 | Valida la homologacion semantica entre las dos fuentes y justifica usar la version de cobertura completa |
| H07-02b | Sesga por construccion cualquier analisis de antiguedad hacia personas juridicas y naturales; afecta a A-H2 |
| H07-03 | Contradice la expectativa de captura del mercado por pocos contratistas |
| H07-04 | Variable derivable sin fuentes externas; candidata a informar cualquier priorizacion de vigilancia |
| H07-05 | Impide interpretarla como experiencia del contratista; corrige una lectura probable del campo |
| H07-06 | Cobertura limitada al 54% de los proveedores; se reporta con su N efectivo |
| H08-01 | Replica con derivacion propia el dato del pipeline compartido (44.9% frente a 17.4%) |
| H08-02 | Responde por anticipado a la objecion de que la jerarquia es arbitraria |
| H08-03 | Cierra la brecha 6 y hace comunicable en tablero lo que la correlacion expresa como coeficiente |
| H08-04 | Variable de proceso interno, disponible solo despues de que las modificaciones ocurran |
| H09-01 | Extiende a 11 variables la matriz de dos tablas de contingencia del EDA previo |
| H09-02 | El criterio de eleccion de la prueba queda documentado y es auditable |
| H09-03 | Resultado honesto: las asociaciones anticipatorias son de magnitud pequena a mediana. Se excluye del calculo el plazo contractual final por relacion definicional con el deslizamiento |
| H09-04 | Distincion imprescindible antes de usar cualquiera de estas variables en un ejercicio predictivo |
| H09-05 | Confirma que la redefinicion del notebook 05 aporta informacion y no replica la medicion anterior |
| H10-01 | Replica y extiende N-K01 al universo completo y al indicador de sobrecosto sobre precio base |
| H10-02 | Confirma la confusion modalidad-escala anticipada por el documento comparativo; control por estratificacion, no por regresion |
| H10-03 | Rechazo explicito de un resultado significativo por tamano de efecto nulo |
| H10-04 | Los consorcios se concentran en contratos de mayor cuantia, que acumulan mas modificaciones |
| H10-05 | Analisis de sensibilidad ausente en el EDA previo. El resultado territorial en tiempo del EDA previo es artefacto de un solo departamento y no debe presentarse como heterogeneidad general |
| H10-06 | Extension del insight N-06; debe declararse como limitacion junto al resultado territorial |
| H10-07 | Limitacion detectada y declarada antes de usar la variable, no despues |
| H10-08 | Impide usarla como magnitud; para el volumen de prorrogas debe usarse `dias_adicionados` |

---


## 5. Cobertura de los objetivos de ambos trabajos

| Trabajo | Objetivo | Enunciado | Estado | Que aporta este EDA | Evidencia |
|---|---|---|---|---|---|
| A | A-OE01 | Extraccion automatizada de SECOP con trazabilidad y reproducibilidad | **No cubierto** | Fuera del alcance de este EDA. Corresponde al pipeline de extraccion, no a este ejercicio analitico |  |
| A | A-OE02 | Estructurar los conjuntos de datos: modelo de datos analitico y reglas de integracion | **Cubierto** | Integracion verificada de tres fuentes con llaves, deduplicacion declarada y grano preservado | nb 01 |
| A | A-OE03 | Normalizar variables para garantizar calidad y confiabilidad | **Cubierto** | Umbrales sobre 77 columnas, centinelas, depuracion declarada de precio_base, marca de observabilidad reproducible, validacion cruzada del parseo de plazo | nb 01, 02, 03, 05 |
| A | A-OE04 | Disenar visualizaciones: distribuciones, outliers, segmentaciones | **Cubierto** | 20 figuras persistidas cubriendo distribuciones, doble lectura, segmentacion por modalidad, cuantia, territorio, competencia, contratista y tiempo | nb 03-11 |
| A | A-H1 | Licitacion publica presenta menores desviaciones de costo y tiempo | **Contrastada, resultado mixto** | Se sostiene en costo, se invierte en tiempo. El mecanismo enunciado (competencia) no opera: efecto nulo con oferentes reales. El efecto de modalidad cae al estratificar por cuantia | nb 04, 10 |
| A | A-H2 | Consorcios presentan mayor indice de adiciones y modificaciones | **Contrastada, resultado mixto** | Se sostiene en modificaciones totales, no se sostiene en adiciones de valor (efecto nulo pese al p-valor) y se invierte en alcance | nb 07, 10 |
| A | A-H3 | Municipios con mayor NBI presentan mayores desviaciones | **No probada, declarado a priori** | No existe NBI municipal en el dataset. El analisis territorial exploratorio muestra que la heterogeneidad en tiempo depende del departamento dominante y en costo no | nb 10 |
| B | B-OE1 | Proceso de Ingenieria de Datos (ETL) con limpieza y homologacion semantica | **Parcialmente util** | Este EDA no construye el ETL del compañero, pero documenta reglas de homologacion verificables: concordancia es_pyme/espyme, deduplicacion de procesos por portafolio, residuo de duplicados en adiciones | nb 01, 02, 07 |
| B | B-OE2 | EDA para caracterizar el comportamiento historico, patrones, correlaciones y variables criticas | **Ampliamente util** | Es el objetivo al que mas sirve este ejercicio: caracterizacion en doble lectura, evolucion temporal, competencia, cuantia, perfil de contratista, matriz extendida de asociaciones | nb 03-10 |
| B | B-OE3 | Desarrollar y validar modelos predictivos supervisados | **Insumo, no cubierto** | Este EDA no entrena ningun modelo por diseno. Aporta la tabla de variables candidatas con su momento de disponibilidad en el ciclo del contrato, que es informacion previa al modelado | nb 09 |
| B | B-OE4 | Prototipo de interfaz de consulta inteligente (RAG + LLM) | **No cubierto** | Fuera del alcance de un EDA |  |

---


## 6. Estado de los 16 insights del documento comparativo

| ID | Insight | Estado | Que se hizo | Evidencia |
|---|---|---|---|---|
| N-K01 | Disociacion tiempo/costo en H1 | **Profundizado** | Contrastado con competencia real (oferentes) y con control por cuantia. El mecanismo de competencia no opera | nb 04, 10 |
| N-K02 | Patron mixto en consorcios (H2) | **Profundizado** | Anadido perfil de contratista, control por cuantia y concentracion de mercado. Detectado sesgo de cobertura del registro para consorcios | nb 07, 10 |
| N-K03 | Contratos liquidados con estado activo | **Ampliado** | 7.382 sobre el universo completo frente a 3.538 sobre el filtrado. Caracterizados por entidad, anio, modalidad y territorio | nb 02 |
| N-K04 | Pagos en cero | **Cerrado** | Contrastado contra el valor adjudicado del proceso: la adjudicacion consta y el pago no se reporta. Es brecha de reporte | nb 05 |
| N-K05 | Sospecha sobre valor_del_contrato | **RESUELTO** | El sobrecosto contra el presupuesto oficial del proceso es del orden del 24%, no del 0.1%. Confirmada la hipotesis de que valor_del_contrato es el valor vigente tras adiciones | nb 05 |
| N-K06 | Tamanos de efecto de asociacion | **Extendido** | Matriz ampliada a 11 variables categoricas y 13 continuas, en doble lectura, ordenada por tamano de efecto | nb 09 |
| N-K07 | Heterogeneidad territorial | **Matizado** | La heterogeneidad en tiempo se desvanece al excluir el departamento dominante; en costo se refuerza | nb 10 |
| N-K08 | Embudo de calidad | **Recalculado** | Embudo de 6 pasos sobre el universo completo, con la marca observable reproduciendo exactamente 19.194 | nb 01 |
| N-01 | fecha_de_fin absorbe prorrogas | **Matizado** | La absorcion es exacta en los observables (mediana 0) pero solo parcial en el universo (mediana -9). Se completa al cierre del contrato | nb 03 |
| N-02 | Filtros no neutrales por modalidad | **Cuantificado** | Retencion por anio, cuantia, modalidad y territorio reportada en doble lectura | nb 05, 06, 10 |
| N-03 | Estructura tripartita del costo | **Caracterizado** | Los tres grupos perfilados por cuantia, modalidad, contratista y alcance, en definicion estricta y con tolerancia | nb 03 |
| N-04 | Retraso material frente a ruido de calendario | **Establecido** | Umbral de 30 dias declarado y justificado; distribucion completa en cinco tramos y en doble lectura | nb 03 |
| N-05 | Denominadores de las cifras titulares | **Aplicado desde el inicio** | Todo porcentaje se reporta con su denominador y con el N efectivo de cada indicador | nb 03 y todos |
| N-06 | Concentracion del departamento dominante | **Ampliado** | Peso del 29.7% en el universo frente al 38.3% en el observable, con analisis de sensibilidad de la prueba territorial | nb 10 |
| N-07 | Rescate de es_grupo | **Extendido** | Ademas de es_grupo se examinaron las restantes variables descartadas por varianza cero; dos variables de competencia resultaron inservibles | nb 01 |
| N-08 | Coherencia plazo pactado y plazo final | **Validado con fuente independiente** | El parseo propio se contrasta contra duracion y unidad_de_duracion del proceso, no contra coherencia interna | nb 03 |

---


## 7. Estado de las 7 brechas del documento comparativo

| Prioridad | Brecha | Estado | Que se hizo | Evidencia |
|---|---|---|---|---|
| 1 | Variables de competencia | **CERRADA con matiz** | Incorporadas desde procesos. Dos de las nueve variables enunciadas tienen varianza cero y son inservibles. A-H1 contrastada con oferentes reales | nb 01, 04 |
| 2 | precio_base | **CERRADA** | Depurado con regla declarada y usado como referencia inicial. Resuelve N-K05 | nb 02, 05 |
| 3 | Segmentacion por cuantia | **CERRADA** | Perfil completo por rango de cuantia en doble lectura y usada como variable de control por estratificacion | nb 05, 10 |
| 4 | Evolucion temporal | **CERRADA** | Distribucion anual, retencion por anio, estacionalidad mensual, estabilidad de los indicadores y momento de las modificaciones | nb 06 |
| 5 | Co-ocurrencia de modificaciones | **CERRADA** | Matriz de co-ocurrencia y analisis de sensibilidad de la jerarquia del indice de alcance | nb 08 |
| 6 | Duracion discretizada | **CERRADA** | Gradiente de extension, adicion y suspension por rango de plazo pactado, en doble lectura | nb 08 |
| 7 | es_pyme | **CERRADA** | Incorporada, contrastada y validada contra el registro externo de proveedores | nb 07 |

---


## 8. Contradicciones con el EDA descriptivo previo

Se reportan tal cual, con su evidencia.

| Tema | Lectura previa | Lectura de este EDA | Interpretacion | Evidencia |
|---|---|---|---|---|
| N-01 se generaliza al universo completo | La mediana de (deslizamiento - dias adicionados) es 0 en cualquier universo | Es 0.0 en el subconjunto observable pero -9.0 en el universo completo | La absorcion de la prorroga por fecha_de_fin se completa al cierre del contrato, no antes | nb 03 |
| Heterogeneidad territorial de A-H3 en tiempo | Kruskal-Wallis H = 670.67 sostiene heterogeneidad territorial en el deslizamiento | Al excluir el departamento dominante el tamano de efecto cae de 0.0577 a 0.0098 (categoria nula) | El resultado territorial en tiempo esta dominado por un solo departamento; en costo si es robusto | nb 10 |
| Numero de contratos liquidados con estado activo | 3.538 contratos | 7.382 sobre el universo completo; 3.538 es el conteo despues de cuatro filtros previos | Ambas cifras son correctas en su contexto; la del universo es la que caracteriza la fuente | nb 02 |
| Sobrecosto practicamente inexistente | 0.1% de los contratos presenta sobrecosto | 23.6% supera el presupuesto oficial del proceso en mas del 1%; 34.7% supera el valor adjudicado | La cifra previa es correcta para su definicion, pero esa definicion no puede detectar sobrecosto | nb 05 |
| Cobertura del registro de proveedores | 54.4% | 54.41% por proveedor unico y 66.47% por contrato | La cifra previa no declaraba la unidad; ambas son correctas | nb 01 |
| es_pyme frente a espyme del registro | No comparadas | Concordancia del 100% donde ambas existen | Son la misma variable con coberturas distintas; se adopta la de cobertura completa | nb 07 |

---


## 9. Limitaciones declaradas del conjunto del ejercicio

1. El dataset integrado de entrada proviene del pipeline compartido (`notebooks/00-06`), cuya autoria sigue pendiente de confirmacion con el director. Toda la cadena de derivacion a partir del notebook 01 de este EDA es propia y auditable.
2. Diseno transversal y censal condicionado. Ninguna asociacion reportada es causal.
3. El control por terceras variables se hace por estratificacion, no por regresion multivariada, por coherencia con el alcance descriptivo del trabajo. La estratificacion no controla simultaneamente por mas de una variable.
4. A-H3 no puede probarse: no existe NBI municipal en el dataset y no se incorporo fuente externa del DANE.
5. El registro externo de proveedores cubre el 54,41% de los proveedores unicos, y su cobertura es practicamente nula para consorcios y uniones temporales, lo que impide usarlo para caracterizar A-H2 sin sesgo.
6. Ninguna magnitud monetaria esta deflactada. Las comparaciones entre presupuesto, adjudicacion y valor contractual son validas porque pertenecen al mismo proceso; las comparaciones de cuantia entre anios distintos no lo serian.
7. Este ejercicio es descriptivo-analitico. No se entrena ningun modelo supervisado, no se importa ninguna libreria de aprendizaje automatico y no se reporta ninguna metrica de clasificacion.
