# 03 — Recalcular los indicadores sobre todos los datos

**Notebook original:** `eda-extendido-integral/notebooks/03_indicadores_doble_lectura.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Recalculo del deslizamiento del plazo sobre el universo completo.** Se repite el mismo parseo del campo de texto de duración contractual y el mismo cálculo de plazo real menos plazo pactado, pero ahora sobre las 48.331 filas. El resultado se calcula para el 76,9% de los contratos (37.155 casos con dato válido), con una mediana de 1 día y un 54,1% de contratos con algún grado de retraso.

2. **La regla de "doble lectura", aplicada sistemáticamente.** Cada estadístico que se calcula en este notebook —y en todos los siguientes del EDA extendido— se reporta siempre en dos columnas paralelas: "universo completo" (las 48.331 filas, sin ningún filtro) y "observable" (las 19.194 filas marcadas con esa bandera en el notebook 01). Esto se implementa mediante una función auxiliar reutilizable que recibe cualquier cálculo y lo aplica automáticamente sobre ambos subconjuntos, en lugar de escribir el código duplicado cada vez.

3. **Recalculo de la desviación de costo sobre el universo completo.** Se repite el cálculo de desviación de costo (valor pagado frente a valor del contrato), obteniendo un N efectivo de 15.035 contratos (31,1% del universo completo) y una tasa de sobrecosto de apenas 0,13% — más baja incluso que el 0,1% ya bajo encontrado en la primera ronda sobre el subconjunto filtrado, lo que refuerza la sospecha, investigada a fondo en el notebook 05, de que esta definición del indicador subestima el sobrecosto real.

4. **Recalculo del índice de alcance sobre el universo completo.** Sobre las 48.331 filas, la distribución del índice de alcance cambia notablemente respecto al subconjunto filtrado: 73,0% "Entregado en su totalidad", 16,5% "Entregado parcialmente", 10,5% "No entregado" — porcentajes más favorables que en el subconjunto observable, precisamente porque el universo completo incluye contratos todavía en ejecución que aún no han tenido oportunidad de fallar.

5. **Corrección explícita de los denominadores.** A diferencia de la primera ronda, aquí se reporta siempre, junto a cada porcentaje titular, el porcentaje condicionado al N efectivo (es decir, calculado solo sobre los contratos con dato válido, no sobre el total de la muestra incluyendo los que no tienen ese dato). Esta corrección de denominadores, identificada como una precisión editorial necesaria durante la revisión del asesor de tesis, evita que un porcentaje parezca más bajo de lo que realmente es solo porque se está dividiendo entre un número más grande del que corresponde.

6. **Persistencia.** Los tres indicadores, calculados en ambas lecturas y guardados junto con la bandera `observable`, quedan disponibles en `indicadores_restriccion_hierro.parquet` para todos los notebooks siguientes del EDA extendido.

## Conclusión

**Qué se hizo, en palabras simples**

Se recalcularon los mismos tres indicadores de siempre (demora, sobrecosto, entrega completa) pero ahora reportando siempre dos números: uno sobre todos los contratos, y otro solo sobre los que ya se pueden evaluar completamente. Esto permite mostrar con transparencia que la decisión de usar el grupo completo de datos no cambia las conclusiones principales, solo cambia un poco la cifra exacta.

**Por qué importa**

Es la manera más honesta de manejar la instrucción del director de "usar todos los datos": en vez de esconder el análisis anterior, se muestran los dos resultados lado a lado.
