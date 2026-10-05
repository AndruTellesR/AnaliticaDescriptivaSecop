# 01 — Contratos electrónicos (la fuente principal)

**Notebook original:** `notebooks/01_contratos_electronicos.ipynb` (fase compartida, coautoría)

## Explicación técnica paso a paso

1. **Conexión a la API.** Se abre una conexión programática al dataset `jbjy-vk9h` de `datos.gov.co` usando la biblioteca `sodapy`, que es un cliente de Python para la API Socrata (el sistema que usa el gobierno para publicar sus datos abiertos). Esta conexión permite enviar consultas parecidas a SQL sin tener que descargar el archivo completo primero.

2. **Filtro en el origen.** En lugar de descargar los más de 5 millones de contratos electrónicos que existen en total y filtrar después en la computadora local, se envía el filtro directamente en la consulta a la API: `tipo_de_contrato = 'Obra'`. Esto reduce drásticamente lo que hay que transferir y procesar, y es más eficiente que descargar todo y filtrar después.

3. **Paginación.** La API de Socrata solo entrega un máximo de 50.000 registros por consulta. Como el resultado filtrado (51.353 contratos de obra) supera ese límite, el notebook hace varias consultas seguidas, cada una pidiendo un bloque distinto de registros (usando parámetros de "salto" y "límite"), hasta reunir el total completo.

4. **Ensamblaje en una tabla.** Cada bloque descargado se convierte en un DataFrame de pandas (una tabla en memoria) y todos los bloques se concatenan en una sola tabla de 51.353 filas y 87 columnas.

5. **Perfilado de calidad.** Sobre esa tabla ya completa, se revisa: cuántos valores nulos tiene cada columna, cuántas filas están duplicadas exactamente (mismo `id_contrato` repetido), y si hay fechas que no tienen sentido lógico (por ejemplo, fecha de fin anterior a la fecha de inicio). Se detectan 23 contratos con fechas invertidas y una cantidad de registros con el campo de valor pagado en cero.

6. **Identificación de la variable de plazo.** Se localiza el campo que registra cuántos días de más se le dieron a un contrato (extensión de plazo), porque será uno de los insumos para calcular, más adelante, el indicador de desviación de tiempo.

7. **Persistencia.** El resultado —51.353 contratos limpios de duplicados exactos, en formato Parquet— queda guardado para que los notebooks siguientes lo usen sin tener que repetir la descarga.

## Conclusión

**Qué se hizo, en palabras simples**

Aquí se conectó por primera vez al portal de datos abiertos del gobierno colombiano (`datos.gov.co`) y se descargaron todos los contratos registrados como "obra pública" — es decir, se dejaron fuera contratos de servicios, compras, consultorías, etc., y solo se trajeron los que corresponden a construcción de infraestructura. En total se descargaron 51.353 contratos de este tipo.

Una vez descargados, se revisó la calidad de la información: cuántos contratos estaban duplicados (aparecían dos veces por error del sistema), qué tan completos estaban los datos de fechas y valores, y si había datos que no tenían sentido (por ejemplo, un contrato que terminó antes de empezar). También se identificó cuál sería la variable clave para medir si un contrato tuvo problemas de plazo: los días que se le agregaron de más al plazo original.

**Por qué importa**

Este es el conjunto de datos que contiene, para cada contrato, el dato más importante de todos: cuánto costó y cuánto tiempo tomó. Sin esta fuente no habría nada que medir.
