# 04 — ¿La competencia entre empresas realmente importa?

**Notebook original:** `eda-extendido-integral/notebooks/04_competencia.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Identificación de las variables de competencia disponibles.** Se parte de las columnas incorporadas en el notebook 01 desde la fuente de procesos: número de oferentes únicos con oferta, número de invitados, número de visualizaciones del proceso, número de respuestas al procedimiento. Se revisa la varianza de cada una y se descubre que dos de ellas (`proveedores_que_manifestaron` y `conteo_de_respuestas_a_ofertas`) tienen varianza cero o casi cero en la práctica — es decir, prácticamente no cambian de un proceso a otro y no sirven para diferenciar nada. Se documentan como inservibles y se descartan del análisis, quedándose con el número de oferentes como la variable de competencia principal.

2. **Verificación de la premisa de H1.** Antes de poner a prueba si la competencia influye en el desempeño, se verifica primero si es cierto que la licitación pública realmente concentra más competencia que las demás modalidades — la premisa implícita de la hipótesis H1 del anteproyecto. Se compara el número de oferentes entre licitación pública y el resto de modalidades con Mann-Whitney U, obteniendo un efecto grande (rank-biserial -0,593, p<1e-300): la premisa se confirma, la licitación pública sí atrae significativamente más competidores.

3. **El contraste central: competencia real contra deslizamiento del plazo.** Aquí está el paso decisivo del notebook. En lugar de usar la modalidad de contratación como un sustituto indirecto de "cuánta competencia hubo", se correlaciona directamente el número de oferentes (la competencia real, medida en cada contrato) contra el deslizamiento del plazo, usando Spearman por la asimetría ya conocida de ambas variables. El resultado es una correlación prácticamente nula (ρ = 0,051 en el universo completo, ρ = -0,0004 en el subconjunto observable), con un tamaño de efecto clasificado como nulo en ambos casos.

4. **Interpretación del resultado.** Esta combinación de hallazgos —la premisa se confirma (sí hay más competencia en licitación pública) pero el mecanismo no opera (la competencia no correlaciona con el desempeño)— es la evidencia central que permite, en el notebook 10, refutar formalmente el mecanismo que la hipótesis H1 atribuía a la disociación tiempo/costo, sin necesidad de rechazar el hallazgo en sí.

5. **Relación de la competencia con el costo.** Se repite el mismo cálculo para la desviación de costo, encontrando esta vez una correlación pequeña pero real y negativa (a mayor número de oferentes, ligeramente menor sobrecosto), lo que matiza el hallazgo: la competencia real sí discrimina algo en costo, aunque con un efecto mucho más modesto del que la hipótesis original sugería.

6. **Relación de la competencia con la cuantía.** Se identifica, de paso, que el número de oferentes correlaciona positivamente con el valor del contrato (ρ = 0,270, efecto pequeño): los contratos de mayor cuantía tienden a atraer más competidores, un dato que anticipa la variable de confusión (la escala del proyecto) que se desarrolla con más detalle en el notebook 10.

## Conclusión

**Qué se hizo, en palabras simples**

La primera hipótesis del trabajo suponía que la licitación pública es mejor porque genera más competencia entre empresas. Este notebook puso esa idea a prueba de forma directa: en lugar de asumir que "licitación pública = más competencia", se contó, contrato por contrato, cuántas empresas realmente se presentaron a competir.

Se confirmó que sí, la licitación pública efectivamente atrae más competidores que otras modalidades. Pero al comparar el número real de competidores contra los días de atraso, no se encontró ninguna relación: contratos con muchos competidores se demoran igual que contratos con pocos. Es decir, la competencia en sí misma no es lo que explica los retrasos.

**Por qué importa**

Este es uno de los hallazgos más importantes del trabajo: obliga a buscar la verdadera causa de los retrasos en otro lado (que resulta ser la cuantía del contrato, según se profundiza en el notebook 10).
