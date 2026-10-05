# 01 — Ampliar el universo de datos (versión extendida)

**Notebook original:** `eda-extendido-integral/notebooks/01_universo_enriquecido.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Punto de partida: el universo completo, no el filtrado.** Se carga de nuevo `contratos_adiciones_obra.parquet` (48.331 filas), pero esta vez sin aplicar los criterios de inclusión/exclusión del notebook 02 de la primera ronda. La primera celda elimina físicamente, otra vez, las 14 columnas prohibidas por blindaje de autoría, y deja constancia programática de esa eliminación (una verificación que se guarda como evidencia de que el blindaje se aplicó).

2. **Enriquecimiento con procesos.** Se carga `procesos_contratacion_obra.parquet` (138.112 filas) y, antes de cruzarlo, se deduplica por la llave `id_del_portafolio` (eliminando 61.790 filas repetidas). Se hace el cruce (`merge`) contra los 48.331 contratos usando esa llave corregida, y se verifica de inmediato que el número de filas del resultado siga siendo exactamente 48.331 — si hubiera aumentado, sería señal de que la deduplicación previa falló y se estarían multiplicando contratos por error. La cobertura obtenida es del 99,92% (48.293 de 48.331 contratos encuentran su proceso de origen).

3. **Incorporación de variables de competencia.** Del cruce con procesos se traen las columnas de número de oferentes, invitados, visualizaciones del proceso y número de lotes — variables que no estaban disponibles en el dataset integrado original y que resultan indispensables para el notebook 04 (poner a prueba si la competencia real, y no solo la modalidad, influye en el desempeño).

4. **Incorporación de precio base.** También del cruce con procesos se trae el campo `precio_base`, convertido explícitamente a tipo numérico (llega como texto desde la API, un problema conocido de SECOP), lo que habilita, más adelante, el notebook 05 y su resolución del misterio del sobrecosto.

5. **Enriquecimiento con proveedores.** Se cruza además contra `proveedores_obra.parquet`, alcanzando una cobertura del 66,47% de los contratos con perfil de proveedor disponible (tipo de empresa, antigüedad, si es PYME).

6. **Construcción de la variable `observable`.** Se aplican, sobre el universo completo, los mismos criterios de inclusión/exclusión definidos en el anteproyecto (fecha 2018-2024, campos completos, valor y fechas coherentes, estado avanzado o finalizado), pero en lugar de eliminar los contratos que no cumplen, se marca cada contrato con una bandera booleana `observable = Verdadero/Falso`. Esto permite conservar todo el universo (48.331) y, al mismo tiempo, saber exactamente cuáles de esos contratos son comparables con el subconjunto usado en la primera ronda de análisis (19.194, que corresponde exactamente a `observable = Verdadero`).

7. **Rescate de la variable `es_grupo`.** Retomando la limitación detectada en el notebook 04 de la fase compartida (donde `es_grupo` resultaba inútil por tener varianza cero en la fuente de proveedores), se reconstruye esta variable a partir de la fuente de contratos electrónicos, donde sí tiene variación real (11.078 casos "Sí" sobre 51.353), y se combina con el tipo de documento del proveedor para construir `tipo_contratista` de forma más confiable que en la primera ronda.

8. **Persistencia.** El resultado, `universo_extendido.parquet` (48.331 filas, con las columnas de competencia, precio base, perfil de proveedor y la bandera `observable`), queda guardado como la base sobre la que se construyen todos los notebooks siguientes del EDA extendido.

## Conclusión

**Qué se hizo, en palabras simples**

Por instrucción del director de tesis, se decidió trabajar con todos los contratos disponibles (48.331), no solo con el subconjunto más pequeño y filtrado que se había usado antes (19.194). Este notebook retoma la tabla de contratos y le agrega información adicional que antes no se estaba usando: cuántas empresas compitieron por cada contrato, cuál era el precio estimado antes de adjudicarlo, y algunos datos del proveedor ganador.

También se creó una marca especial en cada contrato indicando si "sí se puede medir su desempeño final" o no (por ejemplo, si todavía está en ejecución, no se puede saber si terminará bien o mal). Esto permite analizar los datos de dos maneras: con todos los contratos, y solo con los que ya se pueden evaluar completamente — y comparar si las conclusiones cambian entre una forma y otra.

**Por qué importa**

Es el punto de partida de todo el análisis más profundo y extenso que sigue; sin este enriquecimiento no habría sido posible investigar, por ejemplo, si la competencia real entre empresas influye en los retrasos.
