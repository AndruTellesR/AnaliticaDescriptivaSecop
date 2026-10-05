# 08 — ¿Con qué frecuencia coinciden los problemas de un contrato?

**Notebook original:** `eda-extendido-integral/notebooks/08_alcance_y_coocurrencia.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **El problema a resolver.** El índice de alcance se construyó, desde el notebook 03 de la primera ronda, con una jerarquía de prioridad: si hay conclusión anticipada, se clasifica como "No entregado"; si no, pero hay suspensión o cesión, como "Entregado parcialmente"; en cualquier otro caso, "Entregado en su totalidad". Este notebook pone a prueba si esa jerarquía tiene sentido, revisando qué tanto se solapan en la práctica los distintos tipos de eventos.

2. **Construcción de una tabla de co-ocurrencia.** Se cruzan, dos a dos, las banderas binarias de suspensión, extensión de plazo, cesión y conclusión anticipada, contando cuántos contratos presentan cada combinación posible (por ejemplo, cuántos tienen suspensión y también extensión, cuántos tienen suspensión sin extensión, etc.).

3. **Hallazgo principal de co-ocurrencia.** Se encuentra que, de los contratos que tienen suspensión registrada, el 44,9% también tiene extensión de plazo, frente a solo el 17,4% entre los que no tienen suspensión. Esto confirma que estos eventos no son independientes entre sí: una suspensión suele venir acompañada de una extensión, lo cual tiene sentido operativo (si un contrato se detiene temporalmente, es razonable que después necesite más tiempo del pactado originalmente).

4. **Justificación de la jerarquía del índice de alcance.** Con esta evidencia de co-ocurrencia, se argumenta que agrupar suspensión y cesión bajo la misma categoría intermedia ("Entregado parcialmente") es razonable, porque ambos eventos tienden a presentarse junto con extensiones de plazo y representan una ejecución que se completó, pero no de forma continua ni sin contratiempos.

5. **Segmentación de la duración pactada.** Como análisis complementario, se discretiza el plazo pactado en rangos (menos de un mes, de un mes a un año, más de un año, más de dos años) y se calcula la tasa de retraso en cada rango, encontrando que aumenta de forma progresiva con la duración pactada (de 3,1% en contratos de menos de un mes a 51,2% en los de más de dos años) — un resultado que complementa, desde otro ángulo, el hallazgo de que la escala y complejidad del proyecto se asocia con mayor riesgo de desviación.

## Conclusión

**Qué se hizo, en palabras simples**

Se revisó qué tan seguido un mismo contrato presenta más de un problema al mismo tiempo — por ejemplo, si los contratos que se suspenden también suelen terminar con extensión de plazo. Esto sirvió para justificar el orden de prioridad que se usó al clasificar cada contrato como "entregado completo", "entregado a medias" o "no entregado".

**Por qué importa**

Da respaldo a la forma en que se construyó el indicador de alcance, mostrando que la clasificación no es arbitraria sino que refleja patrones reales de cómo ocurren los problemas en conjunto.
