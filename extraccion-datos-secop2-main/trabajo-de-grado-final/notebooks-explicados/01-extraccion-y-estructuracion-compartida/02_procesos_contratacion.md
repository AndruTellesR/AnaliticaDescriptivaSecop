# 02 — Procesos de contratación (lo que pasa antes de firmar el contrato)

**Notebook original:** `notebooks/02_procesos_contratacion.ipynb` (fase compartida, coautoría)

## Explicación técnica paso a paso

1. **Descarga.** Se descarga el dataset `p6dx-8zbt` de `datos.gov.co` (Procesos de Contratación), aplicando el mismo patrón de filtrado en origen y paginación explicado en el notebook 01. El resultado es una tabla de 138.112 procesos de contratación de obra pública, con 57 de las 59 columnas definidas por la fuente (dos columnas no traían datos utilizables y se descartaron).

2. **Primer intento de conexión — y su fracaso.** El plan inicial era unir esta tabla con la de contratos electrónicos usando el campo `id_del_proceso`, que por su nombre parecía ser la llave obvia. Al calcular cuántos valores de ese campo, en la tabla de procesos, aparecen también en la tabla de contratos, el resultado fue una coincidencia del 0%. Es decir: ese campo, a pesar del nombre, no sirve para conectar las dos tablas.

3. **Diagnóstico del error.** Se investigó por qué fallaba: `id_del_proceso` en la fuente de procesos no corresponde al mismo tipo de identificador que usa la fuente de contratos para referenciar su proceso de origen. Revisando el diccionario de datos de la API y probando otros campos disponibles, se identificó que el campo correcto para conectar era `id_del_portafolio`.

4. **Verificación de la llave correcta.** Al repetir el cálculo de coincidencia usando `id_del_portafolio` (procesos) contra `proceso_de_compra` (contratos), la coincidencia sube al 99,9% — prácticamente todos los contratos encuentran su proceso de origen. Esta corrección se documenta como el hallazgo más importante de este notebook, porque sin ella ninguna de las variables de proceso (precio base, número de oferentes, modalidad detallada) podría incorporarse al análisis.

5. **Deduplicación de la llave.** Se detecta que `id_del_portafolio` tiene 61.790 registros duplicados en la fuente de procesos (un mismo proceso puede aparecer varias veces por actualizaciones del sistema). Antes de usarlo como llave de unión, se deduplica conservando un solo registro por valor de la llave, para evitar que la futura unión infle el número de filas de la tabla de contratos.

6. **Identificación de variables de competencia.** Se revisan las columnas de la fuente y se identifican varias que registran directamente cuántas empresas participaron en cada proceso: número de invitados, número de proveedores con invitación, número de oferentes únicos con oferta, número de respuestas al procedimiento. Estas columnas quedan marcadas como candidatas para medir la competencia real de un proceso, en lugar de usar la modalidad de contratación como un sustituto indirecto.

7. **Persistencia.** La tabla de procesos, ya con la llave correcta identificada y verificada, se guarda para su uso en la integración del notebook 05 y en el enriquecimiento posterior del notebook 01 del EDA extendido.

## Conclusión

**Qué se hizo, en palabras simples**

Antes de que se firme un contrato, hay todo un proceso previo: la entidad publica que necesita contratar una obra, varias empresas se presentan a competir, y finalmente se elige una. Este notebook descargó esa información — 138.112 procesos de contratación de obra pública — para poder conectarla, más adelante, con el contrato ya firmado.

El hallazgo más importante de este notebook fue detectar un error de conexión: inicialmente se pensó que un campo llamado "identificador del proceso" era el que permitía unir esta tabla con la de contratos, pero al probarlo, ninguno de los datos coincidía. Se investigó y se encontró que el campo correcto tenía otro nombre ("identificador del portafolio"), y al usar ese, la conexión funcionó casi perfectamente (coincidió en 999 de cada 1.000 casos). También se descubrió que muchos procesos guardan cuántas empresas se presentaron a competir por el contrato — un dato que resultó clave más adelante para poner a prueba una de las hipótesis de este trabajo.

**Por qué importa**

Sin corregir ese error de conexión, no habría sido posible saber, para cada contrato, qué tan competido fue el proceso que lo originó — información que se usa en varias partes del análisis final.
