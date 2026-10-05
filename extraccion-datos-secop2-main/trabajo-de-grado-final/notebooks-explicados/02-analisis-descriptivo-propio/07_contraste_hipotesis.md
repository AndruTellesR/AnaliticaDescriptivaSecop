# 07 — Poniendo a prueba las tres hipótesis (primera versión)

**Notebook original:** `analitica-descriptiva-andres/notebooks/07_contraste_hipotesis.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Declaración de las hipótesis y del criterio de significancia.** Se transcriben las tres hipótesis del anteproyecto (H1 sobre licitación pública, H2 sobre consorcios, H3 sobre necesidades básicas insatisfechas) y se declara, antes de calcular nada, el nivel de significancia que se usará para decidir si un resultado se considera estadísticamente significativo: alfa = 0,05.

2. **Justificación de la prueba elegida para H1 y H2.** Como ambas hipótesis comparan dos grupos (licitación pública contra el resto; consorcios contra personas jurídicas) sobre variables continuas con la asimetría severa ya verificada en el notebook 06, se elige la prueba de Mann-Whitney U, que compara los rangos (posiciones relativas) de los valores entre dos grupos, en lugar de una prueba t de Student, que asumiría una distribución aproximadamente normal.

3. **Contraste de H1.** Se comparan las medianas de deslizamiento del plazo y de desviación de costo entre los contratos de licitación pública (N=4.069) y los de modalidades de menor competencia agrupadas (N=9.974). Resultado: en tiempo, la mediana de licitación pública es 49 días frente a 2 días del resto (p = 5,7e-156, efecto rank-biserial -0,316, tamaño de efecto mediano) — la hipótesis se invierte, la licitación pública se demora más, no menos. En costo, la mediana de licitación pública es -2,44% frente a 0,00% (p = 1,0e-136, efecto +0,383, mediano) — aquí sí se sostiene, la licitación pública tiene menor sobrecosto.

4. **Contraste de H2.** Se comparan consorcios/uniones temporales contra personas jurídicas individuales en dos variables: número total de modificaciones (mediana 5 frente a 3, p<0,001, efecto -0,372, mediano — se sostiene) y número de adiciones de valor específicamente (mediana 0 frente a 0 en ambos grupos, p=0,004 mayormente por el gran tamaño de muestra, pero con efecto de solo -0,017 — prácticamente nulo). Se declara explícitamente que este segundo resultado, aunque técnicamente "significativo" por el p-valor, no se considera evidencia sustantiva de nada, precisamente por su tamaño de efecto nulo — un ejemplo concreto de significancia estadística sin relevancia práctica.

5. **Intento de contraste de H3 — y su límite honesto.** Al buscar el índice de necesidades básicas insatisfechas (NBI) por municipio en el dataset disponible, no se encuentra ninguna columna que lo contenga: SECOP no publica ese dato. En lugar de fabricar un sustituto poco riguroso o de omitir la hipótesis en silencio, se declara explícitamente, antes de mostrar cualquier resultado, que esta prueba no es válida para H3 tal como fue formulada. Como ejercicio exploratorio adicional, se usa el departamento como aproximación geográfica y se aplica la prueba de Kruskal-Wallis (apropiada para comparar más de dos grupos a la vez) entre los ocho departamentos de mayor volumen, encontrando heterogeneidad significativa tanto en tiempo (H=670,67, p=1,45e-140) como en costo (H=190,32, p=1,28e-37) — pero se insiste en que esto es un proxy geográfico, no una prueba de NBI.

6. **Persistencia y trazabilidad.** Todos los resultados numéricos (medianas, N por grupo, p-valores, tamaños de efecto) quedan impresos en las celdas de salida del notebook y documentados en su archivo `.md` de acompañamiento, de forma que cualquier cifra citada en el documento de tesis pueda verificarse de vuelta en la celda exacta que la produjo.

## Conclusión

**Qué se hizo, en palabras simples**

El anteproyecto de este trabajo planteó tres apuestas (hipótesis) antes de ver los datos:

1. Los contratos por licitación pública deberían demorarse y costar menos que los de modalidades con menos competencia.
2. Los consorcios deberían tener más cambios y modificaciones que las empresas individuales.
3. Los contratos en zonas más pobres deberían tener peor desempeño.

Este notebook puso a prueba cada una con pruebas estadísticas formales (no solo "a ojo"), sobre el subconjunto de contratos ya terminados. El resultado fue mixto: la primera apuesta se cumplió a medias (mejor en costo, peor en tiempo), la segunda se cumplió a medias (más cambios, pero no necesariamente peor entrega), y la tercera no se pudo comprobar porque el gobierno no publica el dato de pobreza por municipio que se necesitaba.

**Por qué importa**

Este fue el primer intento de estas pruebas; la versión más completa y con más variables de control está en `eda-extendido-integral/notebooks/10_hipotesis_extendido.ipynb`, que retoma exactamente este mismo trabajo y lo profundiza.
