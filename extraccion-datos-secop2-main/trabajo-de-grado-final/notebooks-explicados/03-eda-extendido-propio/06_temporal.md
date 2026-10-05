# 06 — ¿Cómo ha cambiado esto con los años?

**Notebook original:** `eda-extendido-integral/notebooks/06_temporal.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Extracción de año y mes de firma.** A partir del campo `fecha_de_firma` ya disponible en el universo extendido, se derivan dos columnas nuevas: `anio_firma` y `mes_firma`, usando las funciones de manejo de fechas de pandas.

2. **Distribución anual del volumen de contratación.** Se cuenta cuántos contratos del universo completo (48.331) se firmaron en cada año, y se grafica en un gráfico de barras. Esto permite ver en qué años se concentra la mayor parte de la actividad contractual de obra pública registrada en SECOP II.

3. **Distribución mensual dentro de cada año.** Se repite el conteo a nivel de mes, para detectar si existe algún patrón de estacionalidad (por ejemplo, si se firman más contratos hacia el cierre del año fiscal).

4. **Verificación de estabilidad de los indicadores en el tiempo.** Se calcula, año por año, la mediana del deslizamiento del plazo y de la desviación de costo, para comprobar que los hallazgos centrales del trabajo (por ejemplo, que la licitación pública tiende a demorarse más) no dependen de un solo año atípico sino que se repiten de forma razonablemente consistente a lo largo del periodo disponible.

5. **Verificación del truncamiento por el corte temporal.** Se revisa cuántos contratos firmados en los últimos años del rango disponible todavía no muestran fecha de fin registrada, para advertir sobre el riesgo de que el análisis truncado por año de firma subestime el desempeño de los contratos más recientes (que, por definición, han tenido menos tiempo para completarse o para acumular retrasos observables).

6. **Persistencia de las figuras.** Se guardan los gráficos de evolución anual y mensual como archivos PNG, disponibles para ser usados como evidencia visual en el documento de tesis si se requiere justificar el periodo analizado.

## Conclusión

**Qué se hizo, en palabras simples**

Se revisó cómo se distribuyen los contratos y sus modificaciones a lo largo del tiempo (por año y por mes), para entender si hay años con más volumen de contratación o con patrones distintos de comportamiento.

**Por qué importa**

Ayuda a verificar que las conclusiones del trabajo no dependen de un solo año atípico, y le da al lector una idea de en qué periodo se concentra la información analizada.
