# 05 — Resolviendo el misterio del sobrecosto

**Notebook original:** `eda-extendido-integral/notebooks/05_valor_precio_base_cuantia.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Punto de partida: la cifra que no cuadraba.** Se retoma el resultado del notebook 03 —una tasa de sobrecosto de apenas 0,13%, calculada como (valor pagado − valor del contrato) / valor del contrato— y se confronta explícitamente contra la cifra citada en el planteamiento del problema del anteproyecto (aproximadamente uno de cada cuatro contratos con sobrecosto). La discrepancia es demasiado grande para ignorarla, así que este notebook se dedica por completo a investigar la causa.

2. **Formulación de la hipótesis explicativa.** Se plantea que el campo `valor_del_contrato` de SECOP II podría no representar el valor original pactado en la firma, sino el valor vigente al momento en que se hizo la extracción de datos — es decir, un valor que ya incorporaría las adiciones de dinero (otrosíes) hechas durante la ejecución. Si esto fuera cierto, comparar el pago contra ese valor ya actualizado subestimaría el sobrecosto real por diseño, sin importar qué tan preciso sea el resto del cálculo.

3. **Prueba directa de la hipótesis.** Para probarlo sin necesidad de inspeccionar el dato interno del sistema, se usa una fuente independiente: el `precio_base` del proceso de contratación (el valor que la entidad estimó antes de adjudicar, disponible desde el notebook 01). Se convierte a tipo numérico (llega como texto) y se filtra a los procesos con un solo contrato asociado (para que la comparación sea 1 a 1, sin ambigüedad de a cuál contrato corresponde el precio base), obteniendo 39.938 casos comparables.

4. **Cálculo del exceso sobre precio base.** Se calcula la diferencia porcentual entre `valor_del_contrato` y `precio_base`. El resultado: 23,63% de esos 39.938 procesos muestran un valor del contrato superior al precio base en más de un 1% — una cifra muy cercana al "uno de cada cuatro" citado en el planteamiento del problema, y radicalmente distinta del 0,13% obtenido con la fórmula original.

5. **Verificación del mecanismo, no solo del número.** No basta con tener una cifra distinta; hay que demostrar que el mecanismo propuesto es el correcto. Se segmenta a los mismos 39.938 procesos según si el contrato tuvo o no al menos una adición de valor registrada (variable ya disponible desde la fase compartida). El exceso mediano sobre precio base es 17,05% en los contratos con adición registrada, frente a 0,00% en los que no la tienen — una diferencia que confirma que el mecanismo propuesto (el campo se actualiza tras las adiciones) es efectivamente el que opera.

6. **Segmentación por rango de cuantía.** Aprovechando que ya se tiene el valor del contrato depurado, se construye la variable `rango_cuantia` (menos de 50 millones, 50-200 millones, 200 millones a 1.000 millones, 1.000 a 10.000 millones, más de 10.000 millones de pesos), que se usará en el notebook 10 para el análisis estratificado de las hipótesis H1 y H2.

7. **Declaración explícita de la limitación.** Se deja escrito, sin suavizarlo, que `precio_base` no es exactamente lo mismo que "el valor inicialmente pactado" que pide el anteproyecto, y que no fue posible reconstruir ese valor original por diferencia de adiciones porque el dataset de adiciones de SECOP no tiene ninguna columna de monto (solo registra el tipo de evento, no la cifra). Se verifica esto explícitamente revisando las columnas disponibles en esa fuente, para poder responder con evidencia si un jurado pregunta por qué no se hizo de esa forma alternativa.

## Conclusión

**Qué se hizo, en palabras simples**

Este es, probablemente, el notebook con el hallazgo más importante de todo el trabajo. Al principio, comparando "lo que se pagó" contra "lo que se contrató", el sobrecosto medido era casi cero (0,1%) — un número que no encajaba con lo que dicen las noticias y los informes de control (que hablan de uno de cada cuatro contratos con sobrecosto).

Se investigó por qué, y se encontró la explicación: el campo que el sistema del gobierno llama "valor del contrato" no es el valor con el que se firmó originalmente, sino el valor ya actualizado después de sumarle los "otrosíes" (adiciones de dinero que se le hacen a un contrato mientras se ejecuta). Es decir, comparar el pago contra ese valor "ya actualizado" siempre iba a dar un sobrecosto cercano a cero, porque el número de comparación ya incluía el sobrecosto.

Se resolvió comparando, en cambio, contra el "precio base" — el valor que la entidad había estimado antes de siquiera abrir el proceso de contratación. Con esa comparación, el sobrecosto real resultó ser del 23,63%, coincidiendo con lo que dicen las fuentes externas.

**Por qué importa**

Sin este hallazgo, el trabajo habría llegado a una conclusión equivocada (que casi no hay sobrecostos), cuando en realidad el problema era que se estaba comparando contra el número equivocado.
