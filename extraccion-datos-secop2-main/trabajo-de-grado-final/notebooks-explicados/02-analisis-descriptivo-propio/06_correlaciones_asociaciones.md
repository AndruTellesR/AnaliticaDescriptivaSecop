# 06 — ¿Qué variables se mueven juntas?

**Notebook original:** `analitica-descriptiva-andres/notebooks/06_correlaciones_asociaciones.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Verificación de la asimetría antes de elegir la prueba.** Antes de calcular ninguna correlación, se calcula el coeficiente de asimetría (skewness) de cada variable continua. Los resultados confirman una asimetría severa: 20,13 para el valor del contrato y 34,64 para el plazo pactado en días (valores muy por encima de lo que se consideraría una distribución razonablemente simétrica). Esta verificación es la que justifica, más adelante, no usar la correlación de Pearson (que asume relaciones lineales sobre datos aproximadamente normales) y usar en su lugar Spearman.

2. **Matriz de correlación de Spearman.** Se calcula la correlación de Spearman —basada en el orden de los valores, no en su magnitud exacta, y por tanto más robusta ante valores atípicos y distribuciones asimétricas— entre todas las parejas de variables continuas relevantes: plazo pactado, plazo real, deslizamiento del plazo, valor del contrato, desviación de costo. Se genera un mapa de calor (heatmap) que visualiza toda la matriz de una vez.

3. **Lectura de la matriz.** La correlación más alta de toda la matriz aparece entre el plazo pactado y el plazo real (0,88), lo cual se interpreta como una señal de que el parseo propio del campo de texto de duración contractual (hecho en el notebook 03) es confiable, a pesar de que no logró interpretar el 14,9% de los registros.

4. **Prueba de chi-cuadrado para variables categóricas.** Para medir si dos variables categóricas están asociadas (por ejemplo, modalidad de contratación e índice de alcance), no se puede usar una correlación numérica; se usa en su lugar la prueba de chi-cuadrado de independencia, que compara las frecuencias observadas contra las que se esperarían si las dos variables fueran independientes entre sí.

5. **Cálculo de la V de Cramér.** El chi-cuadrado por sí solo solo indica si la asociación es estadísticamente significativa, pero no dice qué tan fuerte es esa asociación — con un número de contratos tan grande (miles), casi cualquier asociación pequeña resulta "significativa". Por eso se calcula además la V de Cramér, una medida de tamaño de efecto que sí indica la magnitud real de la asociación, independientemente del tamaño de la muestra. Se obtiene V=0,268 (moderada) entre modalidad e índice de alcance, y V=0,184 (débil-moderada) entre tipo de contratista e índice de alcance.

6. **Declaración explícita de no causalidad.** Se deja escrito, como parte de la síntesis del notebook, que ninguna de estas asociaciones implica causalidad: el diseño del estudio es transversal (una fotografía en el tiempo, no un experimento controlado), por lo que solo se puede hablar de relación, no de causa y efecto.

## Conclusión

**Qué se hizo, en palabras simples**

Este notebook midió, de forma más formal (con pruebas estadísticas, no solo mirando gráficos), qué tan relacionadas están unas variables con otras. Por ejemplo: ¿el valor del contrato tiene relación con cuánto se demora? ¿La modalidad de contratación tiene relación con que el contrato se entregue completo o no?

Se usaron pruebas estadísticas apropiadas para datos que no siguen una distribución "normal" (es decir, no en forma de campana), porque los datos de contratación pública casi nunca la siguen — tienen muchos valores bajos y pocos casos extremos muy altos.

**Por qué importa**

Aclarar qué variables están relacionadas (sin llegar a decir que una causa la otra) ayuda a entender mejor el panorama antes de las pruebas de hipótesis formales del notebook siguiente.
