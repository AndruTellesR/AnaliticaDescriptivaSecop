# 06 — Proponentes por proceso (quiénes compitieron por cada contrato)

**Notebook original:** `notebooks/06_proponentes_por_proceso.ipynb` (fase compartida, coautoría)

## Explicación técnica paso a paso

1. **Por qué hace falta un notebook aparte.** Los datos de "número de oferentes" que ya aparecen en la fuente de procesos (notebook 02) son conteos agregados que el propio SECOP calcula, pero no siempre coinciden con el detalle real de quién se presentó. Para verificar y enriquecer esa información, se descarga por separado el listado detallado de proponentes (empresas que efectivamente radicaron oferta) por cada proceso de contratación.

2. **Descarga por lotes.** Al igual que en el notebook 03, esta fuente se descarga filtrando por los identificadores de proceso ya conocidos (los asociados a los 48.331 contratos de obra pública), en lugar de descargar el listado completo de proponentes de todos los procesos de SECOP (que incluiría procesos de servicios, compras, consultorías, etc., irrelevantes para este trabajo). Se obtienen 276.770 registros de proponentes.

3. **Conteo por proceso.** Se agrupa la tabla de proponentes por identificador de proceso y se cuenta cuántas empresas distintas aparecen en cada uno, generando así un número de oferentes reales por proceso, calculado directamente desde el detalle y no desde un agregado previo del sistema.

4. **Persistencia.** Esta tabla de conteo de proponentes por proceso se guarda para ser cruzada más adelante, en el notebook 01 del EDA extendido, contra el identificador de portafolio de cada contrato — permitiendo así construir la variable de "competencia real" que se usa para poner a prueba la hipótesis H1.

## Conclusión

**Qué se hizo, en palabras simples**

Se descargó, para cada proceso de contratación, la lista de empresas que se presentaron a competir (no solo la que ganó). Esto permite calcular, para cada contrato, cuántos oferentes reales hubo — un dato distinto y más preciso que solo mirar la modalidad de contratación.

**Por qué importa**

Este dato terminó siendo clave para poner a prueba, con evidencia directa, si la competencia entre empresas realmente influye en que un contrato se demore más o menos — uno de los hallazgos más importantes de este trabajo (ver sección 6.3.1 del documento principal).
