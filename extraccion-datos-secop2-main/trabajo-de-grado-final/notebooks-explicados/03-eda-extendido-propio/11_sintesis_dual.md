# 11 — El resumen final de todos los hallazgos

**Notebook original:** `eda-extendido-integral/notebooks/11_sintesis_dual.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Declaración de autoría y del sistema de etiquetado dual.** La primera celda de markdown deja escrito, de forma explícita, que todo el código de esta carpeta es de autoría exclusiva del estudiante, que el dato de entrada proviene de un pipeline compartido cuya autoría está pendiente de confirmación con el director, y que ninguna columna del código excluido del compañero se usó en ningún punto. A continuación se define el sistema de etiquetas: `[A-OE02]`, `[A-OE03]`, `[A-OE04]` (sirve a un objetivo específico propio), `[A-H1]`, `[A-H2]`, `[A-H3]` (aporta evidencia a una hipótesis propia), `[B-OE2]` (le sería útil al objetivo de EDA del compañero, sin que eso implique que el compañero lo produjo), `[B-OE3-insumo]` (identifica una variable candidata para un futuro modelo predictivo, sin construir ese modelo), y `[CALIDAD]` (hallazgo sobre la calidad del dato de SECOP en sí mismo, citable por cualquiera de los dos trabajos).

2. **Lectura de los archivos de hallazgos de cada notebook.** Cada uno de los notebooks 01 a 10 de esta carpeta, al ejecutarse, guarda un archivo `hallazgos_NN.csv` con los hallazgos que produjo, ya etiquetados. Este notebook 11 lee todos esos archivos con `glob` y los concatena en una sola tabla.

3. **Cálculo de la distribución de etiquetas.** Se cuenta cuántos hallazgos llevan cada etiqueta y se grafica, encontrando que la etiqueta más frecuente es `[B-OE2]` (36 hallazgos le serían útiles al objetivo de EDA del compañero), seguida de `[CALIDAD]` (28) y `[A-OE03]` (23).

4. **Construcción de la tabla maestra.** Se ensambla la tabla completa de más de 60 hallazgos, cada uno con su identificador (por ejemplo, H10-01), el notebook y la celda exacta de origen, la descripción del hallazgo, sus etiquetas, la evidencia numérica concreta, y una valoración de su importancia (alto/medio).

5. **Evaluación de cobertura de objetivos.** Se construye una tabla que cruza cada objetivo específico de ambos trabajos de grado (los cuatro de este trabajo, más el objetivo de EDA del compañero) contra el conjunto de hallazgos que lo respaldan, permitiendo evaluar de un vistazo qué tan cubierto queda cada objetivo por la evidencia generada.

6. **Verificación de contradicciones con el EDA previo.** Se comparan explícitamente los hallazgos de esta ronda extendida contra los de la primera ronda (`analitica-descriptiva-andres/`), documentando en una tabla separada (`contradicciones_con_eda_previo.csv`) los seis casos donde una cifra o una conclusión cambió entre una ronda y la otra, con la explicación de por qué cambió en cada caso.

7. **Generación del documento `HALLAZGOS_ETIQUETADOS.md`.** Con toda la información anterior ya calculada, el notebook escribe directamente, mediante código Python, el archivo Markdown que sirve como índice maestro de todo el trabajo analítico — el mismo mecanismo con el que este propio notebook fue generado a partir de un script (`build/gen_11.py`), de forma que el documento final nunca se edita a mano, sino que se reconstruye automáticamente cada vez que se vuelve a ejecutar el notebook.

8. **Verificación final de integridad del ejercicio.** Como última celda, se corre una comprobación programática de que ninguna de las 14 columnas prohibidas por el blindaje de autoría sigue presente en ningún DataFrame de trabajo, dejando esa verificación como evidencia final, no solo como una declaración de intenciones.

## Conclusión

**Qué se hizo, en palabras simples**

Este notebook no calcula nada nuevo: recopila, de todos los notebooks anteriores, cada hallazgo importante y lo etiqueta según a qué le sirve — si le aporta al objetivo de este trabajo de grado, si le sería útil al trabajo del compañero (sin que eso signifique que se hizo para él), o si es simplemente un hallazgo sobre la calidad de los datos del gobierno que cualquiera de los dos trabajos podría citar.

También genera un documento (`HALLAZGOS_ETIQUETADOS.md`) que sirve como el índice maestro de todo el trabajo analítico, con más de 60 hallazgos concretos, cada uno con su evidencia exacta (en qué notebook y en qué celda se puede verificar).

**Por qué importa**

Es el cierre ordenado de todo el proceso: convierte docenas de notebooks dispersos en una sola tabla clara de "esto se encontró, aquí está la prueba, y para qué sirve" — la base directa del capítulo de resultados de este trabajo de grado.
