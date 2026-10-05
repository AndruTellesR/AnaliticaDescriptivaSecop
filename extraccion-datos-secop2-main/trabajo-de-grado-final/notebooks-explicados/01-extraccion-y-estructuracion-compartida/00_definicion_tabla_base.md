# 00 — Definición de la tabla base

**Notebook original:** `notebooks/00_definicion_tabla_base.ipynb` (fase compartida, coautoría)

## Explicación técnica paso a paso

1. **Punto de partida.** El proyecto tiene acceso a cuatro fuentes de datos abiertos publicadas por el Estado colombiano en el portal `datos.gov.co`, todas relacionadas con el Sistema Electrónico para la Contratación Pública (SECOP): "Contratos Electrónicos", "Procesos de Contratación", "Adiciones" (modificaciones contractuales) y "Proveedores Registrados". Cada una vive como un dataset independiente en la plataforma Socrata, con su propio identificador y su propia estructura de columnas.

2. **Inspección de cada fuente.** El notebook consulta la API de cada una de las cuatro fuentes (solo para ver su forma, no para descargarla completa todavía) y revisa: cuántas columnas tiene, qué tipo de información contiene cada columna, y qué volumen aproximado de registros existe. Esto se hace antes de comprometerse a descargar nada, porque descargar sin saber qué se va a encontrar sería ineficiente y arriesgado dado el volumen (algunas fuentes tienen decenas de millones de registros si no se filtran).

3. **Búsqueda de llaves candidatas.** Para que cuatro tablas separadas puedan convertirse en un solo conjunto de datos analítico, tiene que existir al menos un campo compartido entre ellas que sirva de "llave" de conexión (algo parecido a un número de cédula que permite cruzar dos bases de datos distintas de la misma persona). El notebook identifica varios candidatos: el identificador del contrato, el identificador del proceso de contratación, y el código del proveedor.

4. **Decisión sobre la fuente madre.** De las cuatro, se elige `contratosElectronicos` como la tabla base ("fuente madre") del análisis. La razón técnica es que esta es la única fuente donde aparecen, en un mismo registro, tanto los datos de firma del contrato (fecha, valor, modalidad) como los datos de su ejecución final (fecha de terminación, estado). Las otras tres fuentes aportan información complementaria (quién compitió, qué modificaciones tuvo, quién es el proveedor), pero ninguna de ellas por sí sola permite medir si un contrato cumplió su plazo y su presupuesto.

5. **Resultado de este notebook.** No se descarga ningún dato masivo todavía: el resultado es una decisión documentada (cuál es la fuente madre y cuáles son las llaves de integración candidatas) que guía el diseño de los notebooks 01 a 06 siguientes.

## Conclusión

**Qué se hizo, en palabras simples**

Antes de descargar un solo dato, había que responder una pregunta básica: de las cuatro fuentes de información que publica el Estado sobre contratación pública (contratos, procesos de compra, adiciones/modificaciones, y proveedores), ¿cuál de ellas es la más importante, la que sirve de "columna vertebral" para conectar todo lo demás?

Este notebook resuelve esa pregunta. Se revisó qué información trae cada una de las cuatro fuentes, se identificó qué campos podrían servir para conectarlas entre sí (por ejemplo, un número de contrato o un código de proceso que aparezca en más de una fuente), y se concluyó que la fuente de "Contratos Electrónicos" debía ser la base principal, porque es donde están registrados los eventos que realmente importan para este trabajo: cuándo se firmó el contrato, cuánto costó, cuándo debía terminar y cuándo terminó realmente.

**Por qué importa**

Es el paso de planeación que evita construir la casa por el techo: si se hubiera elegido mal la fuente base, toda la integración posterior habría quedado mal armada.
