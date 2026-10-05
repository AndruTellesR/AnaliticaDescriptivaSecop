# 04 — Distribuciones y valores atípicos

**Notebook original:** `analitica-descriptiva-andres/notebooks/04_eda_univariado.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Ajuste técnico del entorno gráfico.** Antes de graficar nada, se configura matplotlib con el backend `Agg` (en lugar del modo interactivo habitual `%matplotlib inline`, que en este entorno de ejecución producía un error de compatibilidad de versiones). Cada gráfico se guarda como archivo PNG en la carpeta `figuras/` y luego se muestra dentro del notebook usando `IPython.display.Image`, lo que permite tanto verlo en el momento como reutilizarlo después en el documento de tesis o en el tablero.

2. **Histogramas de las variables continuas.** Se grafica la distribución del deslizamiento del plazo y de la desviación de costo. Ambas distribuciones resultan fuertemente asimétricas: la mayoría de los contratos se agrupan cerca de cero (poco o ningún atraso, poco o ningún sobrecosto), pero existe una cola larga de casos extremos hacia valores muy altos.

3. **Winsorización solo para visualizar.** Para que un histograma no quede aplastado por dos o tres valores extremos (por ejemplo, un contrato con miles de días de atraso, probablemente un error de digitación), se aplica winsorización en los percentiles 1 y 99: los valores por debajo del percentil 1 se recortan visualmente al percentil 1, y los que superan el percentil 99 se recortan al percentil 99. Se deja explícito que esto solo afecta el gráfico — el dato original, sin recortar, es el que se sigue usando en todos los cálculos estadísticos posteriores.

4. **Diagramas de caja (box plots).** Se construyen box plots de las mismas variables, que muestran de forma visual la mediana, los cuartiles y los valores atípicos (los puntos que quedan fuera de los "bigotes" de la caja). Esto permite ver de un vistazo cuántos casos extremos hay y qué tan lejos están del comportamiento típico.

5. **Distribución de variables categóricas.** Se grafican las proporciones de modalidad de contratación, tipo de contratista y estado del contrato dentro de la muestra analítica de 19.194 contratos, para tener una fotografía general de su composición antes de empezar a segmentar por grupos en el notebook siguiente.

6. **Distribución del índice de alcance.** Se grafica, en un gráfico de barras, la proporción de contratos en cada una de las tres categorías del índice de alcance (entregado en su totalidad, entregado parcialmente, no entregado), como referencia general antes de cruzarlo con otras variables.

7. **Reporte de estadísticos robustos.** Junto a cada gráfico, se imprime la mediana y el rango intercuartílico (en lugar de solo la media y la desviación estándar), porque estas medidas son más apropiadas para variables con la asimetría severa detectada (coeficientes de asimetría muy superiores a 1, hasta 34,64 en el caso del plazo pactado).

## Conclusión

**Qué se hizo, en palabras simples**

Con los tres indicadores ya calculados, este notebook los grafica para ver cómo se distribuyen: ¿la mayoría de los contratos se demoran poco o mucho? ¿Hay casos extremos (por ejemplo, un contrato que aparece con miles de días de atraso, que probablemente es un error de digitación del sistema del gobierno)?

Se usaron histogramas (barras que muestran cuántos contratos caen en cada rango de valores) y diagramas de caja (una forma visual de detectar esos casos extremos de un vistazo).

**Por qué importa**

Antes de comparar grupos o sacar conclusiones, hay que entender cómo se comportan los datos en general y qué tan confiables son los valores extremos — de lo contrario, un solo dato mal digitado en el sistema del gobierno podría distorsionar todo el análisis.
