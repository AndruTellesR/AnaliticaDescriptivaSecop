# 09 — Todas las relaciones entre variables, en un solo lugar

**Notebook original:** `eda-extendido-integral/notebooks/09_asociaciones_extendido.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Recolección de todas las asociaciones ya calculadas.** Este notebook no inventa pruebas nuevas: reúne, en una sola tabla consolidada, los resultados de correlación de Spearman y de chi-cuadrado/V de Cramér calculados en distintos notebooks anteriores (06 de la primera ronda, 04 de competencia), agregando además nuevas combinaciones que no se habían probado todavía: cuantía contra los tres indicadores, territorio contra los tres indicadores, y tipo de contratista contra competencia.

2. **Verificación de asimetría extendida.** Se repite la verificación de asimetría (skewness) sobre las nuevas variables incorporadas en el EDA extendido (precio base, número de oferentes), confirmando que también presentan distribuciones muy asimétricas y que, por tanto, corresponde usar Spearman y no Pearson para todas ellas.

3. **Construcción de la tabla ordenada por tamaño de efecto.** A diferencia de una tabla de correlaciones convencional (que solo muestra el coeficiente y el p-valor), aquí se ordenan todas las asociaciones de mayor a menor tamaño de efecto, no de mayor a menor significancia estadística — una distinción importante, porque con casi 50.000 contratos casi cualquier asociación pequeña resulta "significativa", pero eso no significa que sea relevante en la práctica.

4. **Hallazgo destacado: la cuantía es la variable más asociada al retraso material.** Entre todas las variables categóricas evaluadas contra el deslizamiento del plazo, el rango de cuantía resulta ser el que tiene la mayor V de Cramér (0,351) de toda la tabla — más alto que modalidad de contratación o tipo de contratista. Este hallazgo, calculado aquí de forma sistemática, es el que se explica en detalle y se pone a prueba de forma dirigida en el notebook 10.

5. **Marcado de variables candidatas para un futuro modelo predictivo.** Como parte de la síntesis, se etiquetan explícitamente aquellas asociaciones que, aunque no se van a modelar en este trabajo (que es descriptivo, no predictivo), podrían ser insumo útil para el trabajo predictivo del compañero — dejando claro que esto es información sobre asociación, no una recomendación de modelado ni un resultado predictivo en sí mismo.

6. **Persistencia.** La tabla consolidada se guarda como un mapa de referencia que se usa como punto de partida narrativo antes de entrar al contraste formal de hipótesis del notebook 10.

## Conclusión

**Qué se hizo, en palabras simples**

Se armó una tabla completa con todas las relaciones entre variables que se habían ido explorando por separado (modalidad, tipo de contratista, cuantía, territorio, competencia) y se ordenaron según qué tan fuerte es cada relación. Esto permite ver de un vistazo cuáles son los factores que más se asocian con el desempeño de un contrato.

**Por qué importa**

Sirve como mapa general antes de entrar a las pruebas de hipótesis formales del notebook siguiente, y deja identificadas variables que podrían ser útiles para un futuro modelo predictivo (sin construir ese modelo, que no es el objetivo de este trabajo).
