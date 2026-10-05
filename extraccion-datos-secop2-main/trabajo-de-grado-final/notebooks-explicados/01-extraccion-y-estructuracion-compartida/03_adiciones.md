# 03 — Adiciones (los cambios que sufre un contrato mientras se ejecuta)

**Notebook original:** `notebooks/03_adiciones.ipynb` (fase compartida, coautoría)

## Explicación técnica paso a paso

1. **Naturaleza de la fuente.** El dataset `cb9c-h8sn` (Adiciones) no registra contratos, sino *eventos*: cada fila es una modificación puntual hecha sobre un contrato ya firmado — una extensión de plazo, una adición de dinero, una suspensión, una cesión a otro contratista, una reactivación, etc. Un mismo contrato puede tener cero, una o decenas de estos eventos.

2. **Estrategia de descarga por lotes.** Esta fuente es demasiado grande para descargarla completa y filtrarla después por tipo de contrato, porque el campo de tipo de contrato no está disponible directamente en esta tabla (solo el identificador del contrato). En cambio, se toma la lista de los 51.353 identificadores de contratos de obra ya descargados en el notebook 01, y se descargan las adiciones en lotes, consultando la API con cláusulas `WHERE identificador IN (...)` para cada bloque de identificadores. Esta estrategia evita descargar los cientos de miles de adiciones de contratos que no son de obra pública.

3. **Resultado bruto.** Tras descargar todos los lotes y concatenarlos, se obtienen 249.037 registros de modificaciones asociadas específicamente a contratos de obra pública.

4. **Detección de duplicados.** Se encuentra que 105.836 de esos registros están duplicados en el campo `identificador` (el 42,5% del total), de los cuales 96.942 son filas completamente idénticas en todas sus columnas — es decir, el mismo evento reportado dos o más veces por el sistema de origen, sin ninguna diferencia entre las copias.

5. **Homologación de nombres de columnas.** Los nombres de columnas que llegan desde la API no siempre coinciden con los que se esperaban según la documentación pública del dataset (algo frecuente en fuentes de datos gubernamentales, donde el nombre técnico del campo puede diferir del nombre visible en el portal). Se revisan y homologan los nombres antes de continuar, para que el resto del proceso pueda referirse a ellos de forma consistente.

6. **Clasificación por tipo de evento.** Se identifica, para cada registro, a qué tipo de modificación corresponde (extensión de plazo, adición de valor, suspensión, cesión, conclusión anticipada, reactivación, u otro tipo no clasificado), preparando el terreno para que el notebook 05 pueda contar, por contrato, cuántos eventos de cada tipo tuvo.

7. **Persistencia parcial.** En este punto solo se elimina la duplicación exacta (filas 100% idénticas); los 8.894 registros restantes con `identificador` repetido pero contenido distinto se dejan sin resolver aquí, y quedan documentados como un residuo de calidad pendiente (se retoma en la fase de identificación del EDA extendido, notebook 02).

## Conclusión

**Qué se hizo, en palabras simples**

Un contrato de obra pública casi nunca se ejecuta exactamente como se firmó: se le agregan días, se le agrega dinero, se suspende temporalmente, o incluso se termina antes de tiempo. Este notebook descargó el registro de todos esos cambios — 249.037 eventos de modificación — y los organizó por tipo (extensión de plazo, adición de dinero, suspensión, cesión a otro contratista, etc.).

Se encontró que una parte grande de estos registros estaban duplicados (repetidos exactamente igual), por lo que se limpiaron antes de seguir. También se detectó que el sistema de origen tenía nombres de columnas distintos a los que se esperaban, algo común al trabajar con datos que vienen directamente del gobierno.

**Por qué importa**

Este archivo es la base para calcular, más adelante, cuántas veces se modificó cada contrato y de qué tipo fueron esos cambios — insumo directo para medir el desempeño en tiempo y costo.
