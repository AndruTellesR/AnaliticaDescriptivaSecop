# 01 — Universo enriquecido: integracion de las tres fuentes y marca de observabilidad

**Proposito.** Construir el dataset de trabajo de todo el EDA extendido: los 48.331 contratos de obra
del dataset integrado, enriquecidos con las variables de proceso (competencia, precio base, duracion
declarada) y de proveedor (tipo de empresa, antiguedad, PYME), mas la marca booleana `observable` que
identifica el subconjunto de 19.194 contratos cuyo desempeno final es medible.

**Insumos.**

| Fuente | Ruta | Dimensiones declaradas | Llave |
|---|---|---|---|
| Integrado (base) | `entregables/04-datasets/contratos_adiciones_obra.parquet` | 48.331 x 125 | `id_contrato` |
| Procesos | `entregables/04-datasets/procesos_contratacion_obra.parquet` | 138.112 x 57 | `id_del_portafolio` |
| Proveedores | `entregables/04-datasets/proveedores_obra.parquet` | 13.117 x 25 | `codigo` |

**Etiquetas de objetivo que atiende:** `[A-OE02]` (modelo de datos analitico y reglas de integracion),
`[A-OE03]` (normalizacion y criterios de calidad), `[B-OE2]` (base para la caracterizacion historica),
`[CALIDAD]`.

**Declaracion de procedencia y blindaje de autoria.** El dataset integrado de entrada proviene del
pipeline compartido (`notebooks/00-06`), cuya autoria sigue pendiente de confirmacion con el director
(`InformesRev/MATRIZ_OBJETIVOS_CODIGO.md`, tarea de prioridad 1). Las columnas producidas por el codigo
excluido del blindaje (`notebooks/07`, `notebooks/08` y scripts `pliego_*`) se eliminan fisicamente del
DataFrame en la primera celda y no se leen en ningun punto de este EDA. Las columnas derivadas del
pipeline compartido que este ejercicio re-deriva por cuenta propia tambien se eliminan, para garantizar
independencia analitica. La cadena de derivacion desde aqui en adelante es propia y auditable.

**Convencion de trazabilidad.** Las referencias `cNNN` que acompañan cada cifra corresponden al
`execution_count` de la celda que la produjo, tal como queda persistido en el `.ipynb` ejecutado.

**Nota de honestidad sobre el etiquetado dual.** La etiqueta `[B-OE2]` o `[B-OE3-insumo]` significa
"este hallazgo le seria util al compañero", no "este hallazgo es del compañero" ni "Andres trabajo para
el compañero". Todo el codigo y todos los hallazgos de este cuaderno son de autoria de Andres Telles.

> Documento generado automaticamente a partir de `notebooks/01_universo_enriquecido.ipynb` ya ejecutado, por `build/gen_docs.py`. No editar a mano.

---

## 1. Carga del dataset integrado y verificacion del blindaje de autoria

La verificacion devuelve cero columnas prohibidas y cero columnas no usadas presentes en el DataFrame de
trabajo. Las 14 columnas de agregacion de adiciones del pipeline compartido, explicitamente permitidas
por el numeral 4.3 del prompt, si estan disponibles y se usan.

## 2. Fuente de procesos: diagnostico de duplicados y deduplicacion

La advertencia del prompt se confirma en fuente: `id_del_proceso` tiene 25.221 duplicados y no sirve como
llave. `id_del_portafolio` tambien se repite (61.790 filas duplicadas sobre 138.112), de modo que la
deduplicacion previa al join no es opcional: sin ella el join inflaria las filas del universo.

## 3. Join contrato -> proceso y verificacion de que el conteo no crece

## 4. Join contrato -> proveedor: cobertura real por fila y por proveedor unico

## 5. Marca de observabilidad: criterios 3.6.3 y 3.6.4 sobre el universo completo

**Decision metodologica deliberada.** Se aplica el criterio conservador: cuando un contrato registra
`liquidaci_n = 'Si'` pero su `estado_contrato` sigue siendo activo, prevalece la exclusion por estado
activo (3.6.4) sobre la inclusion por liquidacion (3.6.3). Un contrato no puede estar liquidado y en
ejecucion a la vez; ante la contradiccion del dato fuente se opta por no incorporarlo, porque su
desempeno final podria no ser realmente observable.

## 6. Derivaciones propias sobre el universo completo

## 7. Deteccion de variables de competencia con varianza cero

Dos de las nueve variables de competencia que el prompt lista como candidatas
(`proveedores_que_manifestaron` y `conteo_de_respuestas_a_ofertas`) tienen un unico valor distinto
—cero en las 48.331 filas— y por tanto son inservibles. Es un hallazgo de calidad `[CALIDAD]` que
matiza la brecha 1 del documento comparativo: la brecha se cierra, pero no con las cinco variables
enunciadas sino con las que sobreviven al diagnostico. La variable de competencia efectiva del analisis
sera `proveedores_unicos_con` (numero de oferentes unicos con oferta), practicamente identica a
`respuestas_al_procedimiento`.

## 8. Persistencia del dataset extendido

## 9. Coberturas reales consolidadas

## 10. Sintesis de hallazgos etiquetados

## Sintesis del notebook 01

| ID | Hallazgo | Etiquetas |
|---|---|---|
| H01-01 | El join a procesos deduplicado por `id_del_portafolio` conserva el grano exacto (48.331, `id_contrato` unico) con cobertura del 99,92% | `[A-OE02]` `[B-OE2]` |
| H01-02 | La cobertura del registro de proveedores es 54,41% medida por proveedor unico y 66,47% medida por contrato | `[A-OE02]` `[CALIDAD]` |
| H01-03 | La marca `observable` reproduce exactamente los 19.194 contratos; el paso de mayor perdida es el filtro temporal | `[A-OE03]` `[CALIDAD]` |
| H01-04 | Dos de las nueve variables de competencia tienen varianza cero y son inservibles | `[CALIDAD]` `[B-OE2]` |
| H01-05 | Las variables de competencia son invariantes dentro del portafolio, lo que valida la regla de deduplicacion | `[A-OE02]` |
| H01-06 | `es_grupo` se rescata desde el contrato y sostiene `tipo_contratista` | `[A-OE03]` `[A-H2]` `[B-OE3-insumo]` |

**Producto persistido:** `data/universo_extendido.parquet` (48.331 filas, marca `observable` con 19.194
contratos), `data/embudo_observabilidad.csv`, `data/coberturas_join.csv`.

**Limitacion declarada.** El dataset de entrada es producto del pipeline compartido; la autoria de ese
pipeline esta pendiente de confirmacion con el director. Todo lo derivado a partir de la celda 5 de este
cuaderno es propio.

---

## Figuras producidas por este cuaderno

- `figuras/01_embudo_observabilidad.png`

---

## Hallazgos etiquetados de este cuaderno

| ID | Celda | Hallazgo | Etiquetas | Evidencia | Valor |
|---|---|---|---|---|---|
| H01-01 | `c006` | El join a procesos por id_del_portafolio deduplicado conserva el grano exacto: 48.331 contratos, id_contrato unico | [A-OE02] [B-OE2] | Cobertura 99.92% (48,293/48.331) | Alto |
| H01-02 | `c008` | La cobertura del registro de proveedores es 54.41% por proveedor unico pero 66.47% por contrato | [A-OE02] [CALIDAD] | 54.41% de 23,192 proveedores; 66.47% de 48.331 contratos | Medio |
| H01-03 | `c009` | La marca `observable` reproduce exactamente los 19.194 contratos aplicando 3.6.3/3.6.4 sobre el universo completo | [A-OE03] [CALIDAD] | Embudo de 6 pasos, retencion final 39.71% | Alto |
| H01-04 | `c013` | Dos variables de competencia de la fuente de procesos tienen varianza cero: proveedores_que_manifestaron y conteo_de_respuestas_a_ofertas | [CALIDAD] [B-OE2] | 1 valor distinto en las 48.331 filas, todo en cero | Alto |
| H01-05 | `c005` | Las variables de competencia son practicamente invariantes dentro de un mismo portafolio | [A-OE02] | Promedio de valores distintos por portafolio entre 1.000 y 1.264 | Medio |
| H01-06 | `c011` | Se rescata `es_grupo` desde el contrato: en el registro de proveedores tiene varianza cero, en el contrato distingue 3 tipos de contratista | [A-OE03] [A-H2] [B-OE3-insumo] | tipo_contratista: 4 categorias sobre 48.331 | Alto |

---

## Apendice: salida literal de las celdas citadas como evidencia

Cada bloque reproduce la salida de la celda cuyo `execution_count` coincide con la referencia `cNNN` de la tabla anterior, tal como quedo persistida en el `.ipynb` ejecutado.

### Celda `c006`

```
Diagnostico de la fuente de proveedores:
  filas_originales: 13117
  dup_codigo: 499
  codigos_unicos: 12618
  varianza_cero: {'es_entidad': 2, 'esta_activa': 2, 'pais': 3, 'es_grupo': 1}
  filas_deduplicadas: 12618

Columnas descartadas por varianza cero documentada: ['es_entidad', 'esta_activa', 'pais', 'es_grupo']
Nota: `es_grupo` se descarta de ESTA fuente (100% 'No') y se usa el del contrato (insight N-07).
```

### Celda `c008`

```
                                                                                paso  contratos  retencion_pct  perdida_paso
                                0. Universo completo de contratos de obra integrados      48331       100.0000             0
                                       1. Fecha de firma dentro de 2018-2024 (3.6.3)      32175        66.5700        -16156
                           2. Campos minimos no nulos: valor, fechas, estado (3.6.3)      31610        65.4000          -565
                                        3. Excluidos valor_del_contrato <= 0 (3.6.4)      31544        65.2700           -66
                                 4. Excluidas fechas invertidas fin < inicio (3.6.4)      31543        65.2600            -1
5. Estado avanzado/finalizado excluyendo activos, criterio conservador (3.6.3/3.6.4)      19194        39.7100        -12349

Contratos observables: 19,194
VERIFICADO: la marca reproduce exactamente los 19,194 contratos del EDA previo.
```

### Celda `c009`

```
Figura persistida: 01_embudo_observabilidad.png
```

### Celda `c013`

```
Guardado: universo_extendido.parquet - (48331, 77)
Observables en el archivo persistido: 19194
VERIFICADO.
```

### Celda `c005`

```
Filas antes del join: 48,331
Filas despues del join: 48,331
VERIFICADO: el join no altero el grano. id_contrato sigue siendo unico.

Cobertura real del join a procesos: 99.92% (48,293 de 48,331)
Contratos sin proceso asociado: 38
```

### Celda `c011`

```
                      variable  no_nulos  cobertura_pct  valores_distintos
0                  n_oferentes     48293        99.9200                168
1                 n_respuestas     48293        99.9200                167
2                  n_invitados     48293        99.9200                500
3            n_visualizaciones     48293        99.9200                559
4              competencia_cat     48293        99.9200                  5
5                rango_cuantia     47635        98.5600                  5
6                   anio_firma     43181        89.3400                 11
7           plazo_proceso_dias     48293        99.9200                456
8                  precio_base     48293        99.9200              32617
9     valor_adjudicado_proceso     48293        99.9200              29535
10  antiguedad_proveedor_anios     28947        59.8900               3295
11          plazo_discretizado     42119        87.1500                  6
```
