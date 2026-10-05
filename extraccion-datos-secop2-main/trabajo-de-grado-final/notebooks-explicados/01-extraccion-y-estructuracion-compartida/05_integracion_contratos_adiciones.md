# 05 — Integración de contratos y adiciones (unir todo en una sola tabla)

**Notebook original:** `notebooks/05_integracion_contratos_adiciones.ipynb` (fase compartida, coautoría)

## Explicación técnica paso a paso

1. **Deduplicación final de contratos.** Se parte de los 51.353 contratos del notebook 01 y se eliminan 3.022 registros duplicados por `id_contrato`, conservando en cada caso el registro más reciente (el que tiene la fecha de última actualización más nueva, bajo el supuesto de que refleja el estado más al día del contrato). El resultado es 48.331 contratos únicos.

2. **Agregación de adiciones por contrato.** La tabla de adiciones del notebook 03 está a nivel de evento (una fila por modificación), no a nivel de contrato. Aquí se hace un `groupby` por el identificador del contrato, construyendo, para cada uno, contadores: cuántas extensiones de plazo tuvo, cuántas adiciones de valor, cuántas suspensiones, cuántas cesiones, cuántas conclusiones anticipadas, y un total de modificaciones sumando todos los tipos. Este paso convierte 249.037 filas de eventos individuales en columnas resumidas sobre 48.331 filas de contratos.

3. **Eliminación de duplicados en adiciones antes de agregar.** Antes de sumar, se eliminan las 96.942 filas 100% idénticas detectadas en el notebook 03, para no contar dos veces el mismo evento y así inflar artificialmente los contadores de modificaciones (por ejemplo, que un contrato aparezca con 6 extensiones de plazo cuando en realidad tuvo 3, solo porque cada una estaba duplicada en el sistema origen).

4. **Unión (join) de las tablas.** Se cruza la tabla de contratos (ya deduplicada) con la tabla de adiciones agregadas, usando `id_contrato` como llave; y por separado se deja preparada la unión con procesos (usando la llave corregida `id_del_portafolio` del notebook 02) y con proveedores (usando el código de proveedor del notebook 04). El resultado de este proceso de unión es una única tabla ancha, con 48.331 filas (una por contrato) y más de cien columnas que combinan datos de la firma del contrato, sus modificaciones agregadas, y campos de referencia hacia proceso y proveedor.

5. **Verificación de integridad.** Se comprueba que la unión no haya cambiado el número de filas (debe seguir siendo 48.331; si aumentara, significaría que alguna llave tiene duplicados sin resolver y se estaría multiplicando información por error) y que los contadores de modificaciones agregados coincidan, en una muestra de verificación manual, con lo que se ve directamente en la tabla de eventos sin agregar.

6. **Persistencia del archivo central.** Esta tabla integrada de 48.331 contratos se guarda en formato Parquet y se convierte en el punto de partida único a partir del cual se construyen, de forma completamente separada, tanto el trabajo predictivo del compañero como el trabajo descriptivo de este documento (`analitica-descriptiva-andres/` y `eda-extendido-integral/`).

## Conclusión

**Qué se hizo, en palabras simples**

Hasta aquí se tenían varias tablas por separado: contratos, adiciones, procesos, proveedores. Este notebook las juntó en una sola tabla, donde cada fila es un contrato de obra pública con toda su información resumida: cuántas veces se le hicieron adiciones, si tuvo suspensiones, si terminó antes de tiempo, cuánto dinero se le agregó, etc.

El resultado es el archivo central de todo el proyecto: 48.331 contratos únicos de obra pública, con más de cien columnas de información cada uno.

**Por qué importa**

Es la tabla que tanto este trabajo como el del compañero de tesis usan como punto de partida — cada uno construye su propio análisis a partir de aquí, sin depender del código del otro.
