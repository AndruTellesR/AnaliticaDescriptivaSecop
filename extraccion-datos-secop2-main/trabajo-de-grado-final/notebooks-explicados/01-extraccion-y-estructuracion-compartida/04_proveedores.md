# 04 — Proveedores registrados (quién ejecuta las obras)

**Notebook original:** `notebooks/04_proveedores.ipynb` (fase compartida, coautoría)

## Explicación técnica paso a paso

1. **Descarga.** Se descarga el dataset `qmzu-gj57` (Proveedores Registrados) de `datos.gov.co`, obteniendo 13.117 registros con 25 columnas: código del proveedor, nombre, tipo de documento, si es persona natural o jurídica, si es un grupo (consorcio/unión temporal), tipo de empresa, categoría UNSPSC principal, departamento y municipio, fecha de creación del registro, y si está clasificado como PYME.

2. **Deduplicación.** Se detectan 499 registros duplicados (filas 100% idénticas, el 3,8% del total), que se eliminan conservando un único registro por proveedor, dejando 12.618 proveedores únicos.

3. **Detección de valores centinela y varianza cero.** Se revisa cada columna categórica para ver si realmente aporta información. Se encuentra que el campo `pais` es "CO" en el 99,98% de los registros (no discrimina nada, porque prácticamente todos los proveedores son colombianos); `es_entidad` es "No" en el 100%; `esta_activa` es "Sí" en el 99,99%. Estas tres columnas se marcan como candidatas a descartar por varianza cero — no sirven para diferenciar un proveedor de otro.

4. **El campo `es_grupo` y su limitación.** Se revisa el campo que debería indicar si un proveedor es un consorcio o unión temporal (`es_grupo`), y se encuentra que en esta fuente específica es "No" en el 100% de los registros — es decir, esta fuente en particular no permite distinguir consorcios de empresas individuales, a pesar de que el campo existe. Se documenta esta limitación en lugar de descartar la variable por completo, porque el mismo concepto (`es_grupo`) sí está disponible con variación real en la fuente de contratos electrónicos (notebook 01), lo cual se aprovecha después en el EDA propio (notebook 01 del EDA extendido, sección de rescate de variables descartadas).

5. **Cálculo de cobertura frente a los contratos.** Se cruza el código de proveedor de esta fuente contra el campo de proveedor de la tabla de contratos, y se calcula qué porcentaje de los proveedores que efectivamente aparecen en contratos de obra pública tienen también un registro en esta fuente. El resultado es una cobertura del 54,4% — es decir, prácticamente la mitad de los proveedores que ejecutan obra pública no tienen perfil completo en el registro de proveedores. Esto se documenta explícitamente como una limitación de los datos abiertos del Estado, no como un error introducido por este trabajo.

6. **Persistencia.** La tabla de proveedores, con sus columnas de varianza cero identificadas (para descartarlas más adelante) y su cobertura documentada, se guarda para su uso en la integración y en el perfil de proveedor del EDA extendido (notebook 07).

## Conclusión

**Qué se hizo, en palabras simples**

Se descargó el registro de las empresas y personas que aparecen como proveedoras en el sistema (13.117 registros), con información como el tipo de empresa, su tamaño, su ubicación y hace cuánto existe. La idea era poder responder, más adelante, preguntas como: ¿los consorcios se comportan distinto a las empresas individuales?

Se encontró que esta fuente solo cubre a poco más de la mitad de los proveedores que realmente aparecen en los contratos de obra pública — es una limitación real de los datos abiertos del Estado, no un error de este trabajo, y se documentó como tal.

**Por qué importa**

Es la fuente que permite distinguir, por ejemplo, si un contrato lo ejecuta una persona natural, una empresa o un consorcio (unión de varias empresas) — variable central para una de las hipótesis de este trabajo.
