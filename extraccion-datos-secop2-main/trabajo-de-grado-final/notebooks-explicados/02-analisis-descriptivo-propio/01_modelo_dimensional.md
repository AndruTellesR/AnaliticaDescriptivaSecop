# 01 — Modelo dimensional (ordenar la información en carpetas lógicas)

**Notebook original:** `analitica-descriptiva-andres/notebooks/01_modelo_dimensional.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Punto de partida.** Se carga el archivo `contratos_adiciones_obra.parquet` (48.331 filas, 125 columnas), producto final del notebook 05 compartido. Antes de tocar cualquier columna, se eliminan físicamente del DataFrame las 14 columnas prohibidas por el blindaje de autoría (`tiempo`, `presupuesto`, `alcance`, las cinco variables `rup_*` y las seis `pliego_*`), producidas por el código excluido del compañero. Esto se hace en la primera celda del notebook, antes de cualquier análisis, y se deja constancia escrita de qué columnas se eliminaron y por qué.

2. **Diseño del esquema.** Se decide un modelo dimensional simplificado: una tabla de hechos (`hechos_contratos`), con un registro por contrato, que conserva las columnas numéricas y de fecha directamente relevantes para medir desempeño; y cinco tablas de dimensión que agrupan atributos descriptivos por tema.

3. **Construcción de `dim_proceso`.** Se extraen las columnas relativas al proceso de contratación (modalidad detallada, fechas de publicación, identificador de portafolio) y se genera una tabla con un registro por proceso único, resultando en 43.451 filas.

4. **Construcción de `dim_proveedor`.** Se extraen las columnas de proveedor y se deriva la variable `tipo_contratista` combinando el campo `es_grupo` (proveniente de la fuente de contratos electrónicos, no de proveedores registrados, por la limitación de esta última descrita en el notebook 04 compartido) con el tipo de documento del proveedor, clasificando cada uno en Persona Natural, Persona Jurídica, o Consorcio/Unión Temporal. Resultan 23.192 proveedores únicos.

5. **Construcción de `dim_entidad`.** Se agrupan las columnas de la entidad contratante (nombre, NIT, sector) en una tabla de 2.534 entidades únicas.

6. **Construcción de `dim_territorio`.** Se genera una llave subrogada (un identificador propio, no proveniente de SECOP) combinando departamento, ciudad y orden de la entidad (nacional/territorial), resultando en 848 combinaciones únicas de territorio.

7. **Construcción de `dim_modalidad`.** Se listan las modalidades de contratación distintas presentes en los datos, resultando en 9 modalidades únicas.

8. **Verificación de integridad referencial.** Para cada una de las cinco dimensiones, se comprueba de forma programática que el 100% de los registros de la tabla de hechos tengan una llave que exista en la dimensión correspondiente (es decir, que no haya contratos "huérfanos" apuntando a un proceso, proveedor, entidad, territorio o modalidad que no esté en su tabla de dimensión). El resultado es una coincidencia del 100% en las cinco relaciones.

9. **Documentación del diagrama.** Se incluye un diagrama tipo entidad-relación (formato Mermaid) que representa visualmente la tabla de hechos en el centro y las cinco dimensiones alrededor, para dejar constancia del diseño.

10. **Persistencia.** Las seis tablas (hechos + cinco dimensiones) se guardan como archivos Parquet independientes en `data/modelo_dimensional/`, listas para ser consultadas por los notebooks siguientes sin necesidad de repetir esta reorganización.

## Conclusión

**Qué se hizo, en palabras simples**

La tabla de 48.331 contratos con más de cien columnas es difícil de manejar tal cual. Este notebook la reorganizó en un esquema más ordenado: una tabla principal con los datos de cada contrato (fechas, valor, cuántas veces se modificó), y cinco tablas más pequeñas y separadas para agrupar la información sobre el proceso, el proveedor, la entidad que contrata, el territorio y la modalidad de contratación — como tener carpetas separadas por tema en lugar de un solo archivo desordenado.

También se verificó, de forma automática, que todas las conexiones entre la tabla principal y esas cinco carpetas funcionaran perfectamente (sin ningún dato "huérfano" que no encajara en ningún lado).

**Por qué importa**

Esta reorganización es la base técnica que permite, en los notebooks siguientes, consultar la información de forma rápida y confiable — por ejemplo, "muéstrame todos los contratos de la modalidad X" sin tener que revisar manualmente cien columnas cada vez.
