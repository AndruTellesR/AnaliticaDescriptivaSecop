# 05 — Comparación por grupos (modalidad, tipo de contratista, territorio)

**Notebook original:** `analitica-descriptiva-andres/notebooks/05_eda_segmentado.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Segmentación por modalidad de contratación.** Se agrupa la muestra analítica (19.194 contratos) por modalidad y se calcula, para cada una, la mediana del deslizamiento del plazo y de la desviación de costo, junto con el número de contratos en cada grupo. El resultado muestra que "Licitación pública Obra Pública" tiene la mediana de desviación de tiempo más alta de todas las modalidades (50 días), muy por encima de "Selección Abreviada de Menor Cuantía" (1 día) y "Mínima cuantía" (0 días) — un resultado contraintuitivo respecto a lo que la hipótesis H1 anticipaba, y que se marca explícitamente para ser contrastado formalmente en el notebook 07.

2. **Segmentación por tipo de contratista.** Se repite el mismo cálculo agrupando por tipo de contratista (Persona Natural, Persona Jurídica, Consorcio/Unión Temporal). Los consorcios muestran una mediana de desviación de tiempo de 27 días, frente a 1 día en personas jurídicas y 0 días en personas naturales. Al cruzar el tipo de contratista contra el índice de alcance, se encuentra un patrón que parece contradictorio a primera vista: los consorcios tienen, a la vez, más días de atraso y una tasa de "no entregado" (12,4%) menor que las personas jurídicas individuales (26,4%) — es decir, se demoran más pero terminan entregando con más frecuencia. Este patrón mixto se documenta explícitamente, sin forzar una única lectura simple.

3. **Segmentación por territorio.** Se agrupa por orden de la entidad contratante (nacional/territorial) y por departamento. Las entidades de orden territorial muestran una mediana de 3 días de desviación frente a 1 día en las de orden nacional. Al desagregar por departamento entre los de mayor volumen de contratación, Bogotá D.C. (el de mayor volumen, con 7.345 contratos en la muestra) presenta la mediana más alta (15 días).

4. **Generación de las figuras.** Se producen tres gráficos de box plot segmentado (uno por cada variable de agrupación: modalidad, tipo de contratista, territorio), usando el mismo patrón de winsorización P1-P99 solo para visualización explicado en el notebook 04, y se guardan como archivos PNG independientes.

5. **Redacción de la síntesis con base en los números reales.** La celda de conclusión de este notebook se redactó después de ver los resultados calculados, no antes: inicialmente se esperaba (siguiendo la hipótesis H1 del anteproyecto) que la licitación pública tuviera mejor desempeño de tiempo por ser una modalidad más competitiva, y al encontrar lo contrario, la síntesis se corrigió para reflejar el hallazgo real en lugar de la expectativa original.

## Conclusión

**Qué se hizo, en palabras simples**

Aquí se compararon los tres indicadores entre distintos grupos: ¿los contratos por licitación pública se demoran más o menos que los de contratación directa? ¿Los consorcios se comportan distinto a las empresas individuales? ¿Hay departamentos donde las obras se retrasan sistemáticamente más que en otros?

El hallazgo más llamativo de este notebook fue que la licitación pública —que en teoría debería ser el mecanismo más "cuidadoso" para elegir contratista— resultó ser la modalidad con más días de atraso, contrario a lo que se esperaba.

**Por qué importa**

Estos resultados son la base directa de las hipótesis que se ponen a prueba formalmente más adelante, y también alimentan las segmentaciones que el tablero interactivo le muestra al usuario final.
