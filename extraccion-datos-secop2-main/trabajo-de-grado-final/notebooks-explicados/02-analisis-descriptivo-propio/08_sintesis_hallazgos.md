# 08 — Resumen de la primera ronda de hallazgos

**Notebook original:** `analitica-descriptiva-andres/notebooks/08_sintesis_hallazgos.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Naturaleza del notebook.** A diferencia de los siete anteriores, este no contiene celdas de código que calculen algo nuevo sobre los datos; está compuesto casi en su totalidad por celdas de markdown que resumen, en prosa, lo obtenido en los notebooks 01 a 07.

2. **Organización por objetivo específico.** El resumen se estructura siguiendo los objetivos específicos del anteproyecto: primero lo relativo a OE-02 (modelo dimensional), luego OE-03 (calidad, normalización, indicadores, hipótesis), citando en cada punto de qué notebook proviene la cifra correspondiente.

3. **Consolidación del embudo de calidad.** Se repite, en una sola tabla resumen, el recorrido completo de 48.331 a 19.194 contratos (39,7%), con el detalle de cuántos contratos se perdieron en cada criterio de inclusión/exclusión aplicado en el notebook 02.

4. **Consolidación de los hallazgos de hipótesis.** Se transcriben las conclusiones de H1, H2 y H3 del notebook 07, ya en lenguaje de resultado final: la disociación tiempo/costo en H1, el patrón mixto de H2, y la declaración de no validez de H3.

5. **Relación explícita con el marco teórico.** Se incluye un párrafo que conecta los hallazgos anteriores con la restricción de hierro (Atkinson, 1999; Meredith y Mantel, 2012): el hecho de que la licitación pública mejore el costo pero empeore el tiempo se interpreta como el tipo de disociación entre dimensiones que ese marco teórico anticipa.

6. **Lista explícita de siete limitaciones.** Se enumeran, sin suavizarlas, las limitaciones detectadas durante todo el proceso: el sesgo de la muestra hacia contratos con ejecución avanzada, la baja cobertura del indicador de costo, la incapacidad del índice de alcance para distinguir "reducción del objeto contratado", la ausencia de datos de NBI para H3, las variables extrañas no controladas, la imposibilidad de inferir causalidad, y la autoría pendiente de confirmación del pipeline compartido.

7. **Función de puente hacia el trabajo posterior.** Al cierre, se señala explícitamente qué preguntas quedan abiertas — en particular, la discrepancia entre el sobrecosto casi nulo medido aquí y la cifra mucho más alta citada en el planteamiento del problema del anteproyecto — dejando planteada la pregunta que el EDA extendido (`eda-extendido-integral/`) resolvería más adelante.

## Conclusión

**Qué se hizo, en palabras simples**

Este notebook no calcula nada nuevo: junta en un solo lugar, en lenguaje de conclusión (no de código), todo lo que se encontró en los siete notebooks anteriores de esta primera ronda de análisis. Sirve como borrador inicial del capítulo de resultados de la tesis.

**Por qué importa**

Es el antecedente directo del análisis mucho más completo desarrollado después en `eda-extendido-integral/`, que retoma estos mismos hallazgos, corrige algunos detalles y profundiza en varios puntos (por ejemplo, por qué el sobrecosto medido parecía casi inexistente).
