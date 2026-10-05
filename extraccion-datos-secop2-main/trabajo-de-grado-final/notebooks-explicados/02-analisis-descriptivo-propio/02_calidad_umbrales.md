# 02 — Calidad y umbrales (decidir qué contratos sí se pueden analizar)

**Notebook original:** `analitica-descriptiva-andres/notebooks/02_calidad_umbrales.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Definición de umbrales cuantitativos de calidad.** Se establece una regla propia, ausente hasta este punto en cualquier documento del proyecto: una variable se considera "apta" para el análisis si su nulidad (porcentaje de datos vacíos) no supera el 20%; "de uso restringido" entre el 20% y el 50%; y "no apta" por encima del 50%. Esta regla se justifica con el estándar internacional de calidad de datos ISO 8000.

2. **Aplicación de los umbrales.** Se evalúan diez columnas clave que alimentarán los indicadores de desempeño (fechas de inicio y fin, valor del contrato, valor pagado, estado, campo de duración en texto). Todas resultan "aptas", con la nulidad máxima observada en la fecha de inicio del contrato (12,6%).

3. **Aplicación del criterio 3.6.3 del anteproyecto — fecha de firma.** Se filtra el universo de 48.331 contratos dejando solo los firmados entre 2018 y 2024, reduciendo el conjunto a 32.175 contratos (66,6%).

4. **Aplicación del criterio — campos mínimos completos.** Sobre ese subconjunto, se exige que estén presentes los campos mínimos necesarios para calcular los indicadores (valor, fecha de inicio, fecha pactada de terminación, estado), reduciendo a 31.610 contratos (65,4%).

5. **Aplicación del criterio — valor y fechas coherentes.** Se excluyen los contratos con valor menor o igual a cero y con fechas invertidas (fecha de fin anterior a la fecha de inicio), quedando 31.543 contratos (65,3%).

6. **Aplicación del criterio 3.6.4 — estado de ejecución avanzado o finalizado.** Este es el paso que más reduce el universo. Se decide qué estados de SECOP se consideran "avanzados o finalizados" (terminado, cerrado, cedido, entre otros con acta de liquidación) y cuáles se consideran "activos" y por tanto se excluyen (en ejecución, suspendido, cancelado, borrador, aprobado, en aprobación, enviado a proveedor). Aplicando este filtro, el universo baja a 19.194 contratos (39,7% del total).

7. **El hallazgo de calidad: la contradicción liquidación/estado.** Durante este paso se detecta que 3.538 contratos tienen simultáneamente el campo `liquidación = "Sí"` (que sugiere cierre formal) y un estado que el propio sistema clasifica como activo (en ejecución, suspendido, cancelado, aprobado). Se decide, de forma conservadora, que el estado de ejecución activo tiene prioridad sobre la bandera de liquidación al momento de decidir si un contrato se excluye — es decir, se excluyen estos 3.538 casos aunque digan estar liquidados, porque su estado contradice esa liquidación y no se puede confiar en el dato sin evidencia adicional. Esta decisión, junto con el número exacto de casos afectados, queda documentada explícitamente.

8. **Persistencia de la muestra analítica y del reporte de calidad.** Se guardan dos archivos: `muestra_analitica.parquet` (los 19.194 contratos que superaron todos los filtros) y `reporte_calidad_funnel.csv` (una tabla paso a paso mostrando cuántos contratos se perdieron en cada uno de los criterios anteriores, para que el proceso completo sea auditable).

## Conclusión

**Qué se hizo, en palabras simples**

No todos los 48.331 contratos sirven para medir "qué tan bien se ejecutó una obra": si un contrato todavía está en construcción, todavía no se puede saber si se demoró o no. Este notebook definió reglas claras para decidir qué contratos sí tienen la información necesaria para ser evaluados (fecha de firma entre 2018 y 2024, datos completos, y que el contrato ya haya terminado o esté en una etapa avanzada), y aplicó esas reglas paso a paso, documentando cuántos contratos se descartaban en cada paso.

De paso, se descubrió algo curioso en los propios datos del gobierno: 3.538 contratos aparecían marcados como "ya liquidados" (es decir, cerrados formalmente) pero al mismo tiempo su estado decía que seguían "en ejecución" — una contradicción que no tiene sentido, y que se decidió resolver de la forma más cuidadosa posible (tratándolos como no confiables para este análisis).

**Por qué importa**

Evita sacar conclusiones sobre contratos que todavía no han terminado, lo cual daría una imagen falsamente positiva del desempeño contractual.
