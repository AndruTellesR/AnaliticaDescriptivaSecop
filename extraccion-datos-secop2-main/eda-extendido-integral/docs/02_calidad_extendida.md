# 02 — Calidad extendida sobre las columnas incorporadas

**Proposito.** Auditar la calidad de las columnas que este EDA incorpora por primera vez (proceso y
proveedor), no solo las diez columnas clave que audito el EDA descriptivo previo. Cubre umbrales de
nulidad, valores centinela, outliers de `precio_base`, el residuo de duplicados de la fuente de
adiciones y la caracterizacion completa de los contratos liquidados con estado activo sobre el universo
completo.

**Insumo.** `data/universo_extendido.parquet` (notebook 01) y, para el diagnostico de adiciones,
`entregables/04-datasets/adiciones_obra.parquet` en modo solo lectura.

**Etiquetas de objetivo que atiende:** `[A-OE03]` (normalizacion, calidad y confiabilidad),
`[CALIDAD]` (hallazgos sobre el dato SECOP citables por ambos trabajos), `[B-OE2]` (variables criticas
y su usabilidad real).

**Convencion de trazabilidad.** Las referencias `cNNN` corresponden al `execution_count` de la celda que
produjo la cifra, persistido en el `.ipynb` ejecutado.

> Documento generado automaticamente a partir de `notebooks/02_calidad_extendida.ipynb` ya ejecutado, por `build/gen_docs.py`. No editar a mano.

---

## 1. Umbrales de nulidad sobre todas las columnas del universo extendido

Se aplica el mismo criterio de clasificacion del EDA descriptivo previo, ahora sobre las 77 columnas del
dataset extendido y no sobre diez: nulidad <= 20% Apta, <= 50% Uso restringido, > 50% No apta sin
tratamiento adicional. Se separa el reporte por origen (contrato, proceso, proveedor, derivada propia)
porque el diagnostico de cada bloque es distinto.

## 2. Valores centinela: nulidad aparente frente a nulidad efectiva

SECOP usa valores centinela en lugar de nulos. Una columna con 0% de nulidad puede estar vacia en la
practica. Se evaluan dos familias: centinelas textuales (`No definido`, `No Definido`, `No aplica`,
cadena vacia) y ceros estructurales en variables donde el cero no es un valor legitimo.

## 3. Outliers y depuracion de `precio_base`

El documento comparativo advierte que `precio_base` contiene valores absurdos (minimo negativo y maximo
del orden de 1e16). Antes de usarlo como valor inicial alternativo (notebook 05) se declara y aplica una
regla de depuracion explicita.

**Regla declarada:** se considera `precio_base` utilizable si `precio_base > 0` y
`precio_base <= 1e13` (diez billones de pesos, cota superior generosa: el contrato de mayor valor del
universo esta un orden de magnitud por debajo). Los valores fuera de ese rango se marcan como no
utilizables, no se imputan y no se eliminan filas: la marca se propaga como `precio_base_valido`.

## 4. Residuo de duplicados en la fuente de adiciones

La agregacion de modificaciones por contrato (`n_modificaciones_total`, `dias_adicionados`, y las
banderas `tiene_*`) proviene de `adiciones_obra.parquet`. El documento comparativo señala un residuo de
duplicados no resuelto. Se reproduce el diagnostico en fuente porque afecta directamente a variables que
este EDA si utiliza.

## 5. Contratos liquidados con estado activo, sobre el universo completo

El insight N-K03 del EDA descriptivo previo cuantifico 3.538 contratos con `liquidaci_n = 'Si'` y estado
aun activo. Esa cifra corresponde al subconjunto que ya habia superado los cuatro primeros criterios del
embudo. Sobre el universo completo, sin filtrar, la contradiccion es mayor.

## 6. Coherencia de fechas y otros chequeos estructurales

## 7. Persistencia y sintesis de hallazgos etiquetados

## Sintesis del notebook 02

| ID | Hallazgo | Etiquetas |
|---|---|---|
| H02-01 | Sobre el universo completo hay 7.382 contratos liquidados con estado activo, no 3.538 | `[CALIDAD]` `[A-OE03]` `[B-OE2]` |
| H02-02 | La inconsistencia se concentra en pocas entidades: practica de reporte, no error aleatorio | `[CALIDAD]` `[B-OE2]` |
| H02-03 | `precio_base` exige depuracion declarada antes de usarse como valor inicial alternativo | `[CALIDAD]` `[A-OE03]` |
| H02-04 | Residuo de 8.894 identificadores duplicados en adiciones, no resuelto por el pipeline | `[CALIDAD]` |
| H02-05 | 68,9% de pagos en cero sobre el universo; 54,8% tras el filtro de observabilidad | `[CALIDAD]` `[A-OE03]` `[B-OE2]` |
| H02-06 | Las columnas de proceso llegan completas; el bloque de proveedor tiene nulidad estructural | `[A-OE03]` `[B-OE2]` |

**Productos persistidos:** `data/calidad_umbrales_extendido.csv`, `data/calidad_centinelas.csv`,
`data/marcas_calidad.parquet`, `figuras/02_precio_base_vs_valor.png`,
`figuras/02_liquidados_estado_activo_por_anio.png`.

**Como responder a un jurado.** La objecion previsible es "¿por que el numero de contratos liquidados con
estado activo cambio respecto del EDA anterior?". La respuesta es que no cambio el dato sino el
denominador: 3.538 es el conteo dentro del subconjunto ya filtrado por fecha, campos minimos, valor y
coherencia de fechas; 7.382 es el conteo sobre el universo completo. Ambas cifras son correctas en su
contexto y aqui se reportan las dos.

---

## Figuras producidas por este cuaderno

- `figuras/02_liquidados_estado_activo_por_anio.png`
- `figuras/02_precio_base_vs_valor.png`

---

## Hallazgos etiquetados de este cuaderno

| ID | Celda | Hallazgo | Etiquetas | Evidencia | Valor |
|---|---|---|---|---|---|
| H02-01 | `c009` | Sobre el universo completo hay 7.382 contratos con liquidacion registrada y estado aun activo, mas del doble de los 3.538 reportados por el EDA previo | [CALIDAD] [A-OE03] [B-OE2] | 7,382 sobre 48.331 (15.27%); 3,538 sobre el subconjunto filtrado | Alto |
| H02-02 | `c010` | La inconsistencia liquidado-activo no esta distribuida al azar: se concentra en pocas entidades y crece en los anios recientes | [CALIDAD] [B-OE2] | Las 10 entidades con mas casos acumulan 32.2% del total | Alto |
| H02-03 | `c006` | `precio_base` requiere depuracion previa: contiene valores negativos y magnitudes absurdas | [CALIDAD] [A-OE03] | minimo -397,166,484; maximo 13,212,285,859,000; utilizables 47,704 (98.70%) | Alto |
| H02-04 | `c008` | La fuente de adiciones arrastra 8.894 identificadores repetidos con contenido distinto que la eliminacion de filas identicas no resuelve | [CALIDAD] | 249,037 registros; 96,942 filas identicas; residuo 8,894 | Alto |
| H02-05 | `c012` | El 68.9% del universo registra valor_pagado en cero; el filtro de observabilidad lo reduce a 54.8% pero no lo resuelve | [CALIDAD] [A-OE03] [B-OE2] | 33,296 de 48.331 en el universo | Alto |
| H02-06 | `c004` | Ninguna columna de proceso incorporada supera el umbral de nulidad: la cobertura del join es del 99.92% y las variables llegan completas | [A-OE03] [B-OE2] | Clasificacion de nulidad por origen en la tabla de umbrales | Medio |

---

## Apendice: salida literal de las celdas citadas como evidencia

Cada bloque reproduce la salida de la celda cuyo `execution_count` coincide con la referencia `cNNN` de la tabla anterior, tal como quedo persistida en el `.ipynb` ejecutado.

### Celda `c009`

```
=== Por modalidad de contratacion ===
                                             contratos_liq_activos  total_universo  tasa_pct
modalidad_de_contratacion                                                                   
Contratación directa                                          2480            9981   24.8500
Selección Abreviada de Menor Cuantía                          1509           12932   11.6700
Mínima cuantía                                                1321            9747   13.5500
Licitación pública Obra Publica                               1074            8575   12.5200
Contratación régimen especial                                  399            2905   13.7300
Contratación régimen especial (con ofertas)                    328            1932   16.9800
Contratación Directa (con ofertas)                             173            1541   11.2300
Licitación pública                                              58             421   13.7800

=== Por anio de firma ===
            contratos_liq_activos  total_universo  tasa_pct
anio_firma                                                 
2,016.0000                      1               7   14.2900
2,017.0000                     30             237   12.6600
2,018.0000                    132            1282   10.3000
2,019.0000                    278            2292   12.1300
2,020.0000                    182            2764    6.5800
2,021.0000                    247            5406    4.5700
2,022.0000                    574            5962    9.6300
2,023.0000                   1372            7966   17.2200
2,024.0000                    888            6503   13.6600
2,025.0000                   2532            9731   26.0200
2,026.0000                    566            1031   54.9000

=== Por departamento (top 8) ===
                            contratos_liq_activos  total_universo  tasa_pct
departamento                                                               
Distrito Capital de Bogotá                   2427           14338   16.9300
Antioquia                                     768            5330   14.4100
Cundinamarca                                  383            2412   15.8800
Meta                                          326            1155   28.2300
Boyacá                                        300            2070   14.4900
Valle del Cauca                               295            2569   11.4800
Caldas                                        272            1938   14.0400
Santander                                     262            1744   15.0200

=== Entidades que mas los reportan (top 10) ===
                                                              contratos_liq_activos  total_entidad  tasa_pct
nombre_entidad                                                                                              
INSTITUTO DE CAMINOS Y CONSTRUCCIONES DE CUNDINAMARCA - ICCU                   1123           2684   41.8000
INVIAS                                                                          387           3655   10.6000
AEROCIVIL                                                                       204           1364   15.0000
AGENCIA PARA LA INFRAESTRUCTURA DEL META                                        199            395   50.4000
EDUNA (COMPRADOR)                                                               100            181   55.2000
GOBERNACION DE CALDAS                                                            86            635   13.5000
CORPORACION NASA KIWE                                                            82            214   38.3000
MUNICIPIO DE MANIZALES                                                           69            426   16.2000
GOBERNACIÓN DE BOLÍVAR//                                                         63            156   40.4000
MUNICIPIO DE PIEDECUESTA                                                         61            212   28.8000

Concentracion: las 10 entidades listadas acumulan 32.2% de los casos.

Mediana de valor_del_contrato — liquidados-activos vs resto del universo:
  liquidados-activos: 110,000,000
  resto:              221,265,546
```

### Celda `c010`

```
Figura persistida: 02_liquidados_estado_activo_por_anio.png
```

### Celda `c006`

```
Figura persistida: 02_precio_base_vs_valor.png
```

### Celda `c008`

```
Sobre el UNIVERSO COMPLETO (N = 48,331): 7,382 contratos (15.27%)
Sobre el subconjunto que supera los 4 primeros criterios (N = 31,543): 3,538 contratos

La cifra de 3.538 del EDA previo corresponde a la segunda lectura. Sobre el universo completo
la inconsistencia afecta a mas del doble de contratos.

Distribucion por estado_contrato registrado:
estado_contrato
En ejecución         4955
Aprobado             1191
Suspendido            651
enviado Proveedor     174
Borrador              170
Cancelado             154
En aprobación          87
```

### Celda `c012`

```
       id notebook celda                                           hallazgo                                          evidencia                   etiquetas  \
0  H02-01       02  c009  Sobre el universo completo hay 7.382 contratos...  7,382 sobre 48.331 (15.27%); 3,538 sobre el su...  [CALIDAD] [A-OE03] [B-OE2]   
1  H02-02       02  c010  La inconsistencia liquidado-activo no esta dis...  Las 10 entidades con mas casos acumulan 32.2% ...           [CALIDAD] [B-OE2]   
2  H02-03       02  c006  `precio_base` requiere depuracion previa: cont...  minimo -397,166,484; maximo 13,212,285,859,000...          [CALIDAD] [A-OE03]   
3  H02-04       02  c008  La fuente de adiciones arrastra 8.894 identifi...  249,037 registros; 96,942 filas identicas; res...                   [CALIDAD]   
4  H02-05       02  c012  El 68.9% del universo registra valor_pagado en...                    33,296 de 48.331 en el universo  [CALIDAD] [A-OE03] [B-OE2]   
5  H02-06       02  c004  Ninguna columna de proceso incorporada supera ...  Clasificacion de nulidad por origen en la tabl...            [A-OE03] [B-OE2]   

   valor                                               nota  
0   Alto  La cifra previa se calculo despues de cuatro f...  
1   Alto  Sugiere practica de reporte de entidad, no err...  
2   Alto  Regla declarada: 0 < precio_base <= 1e13; no s...  
3   Alto  Afecta a las agregaciones de modificaciones po...  
4   Alto            Extension de N-K04 al universo completo  
5  Medio  El bloque de proveedor si tiene nulidad estruc...
```

### Celda `c004`

```
                            columna           origen               tipo      n     pct  nulidad_declarada_pct  nulidad_efectiva_pct
0   prov_codigo_categoria_principal        proveedor  centinela textual  46958 97.1600                33.5300              130.6900
1                       n_invitados          proceso   cero estructural  33833 70.0000                 0.0800               70.0800
2                      valor_pagado         contrato   cero estructural  33296 68.8900                 0.0000               68.8900
3                   valor_facturado         contrato   cero estructural  29677 61.4000                 0.0000               61.4000
4                       prov_codigo        proveedor  centinela textual  16205 33.5300                33.5300               67.0600
5                 prov_tipo_empresa        proveedor  centinela textual  16205 33.5300                33.5300               67.0600
6                    prov_municipio        proveedor  centinela textual  16205 33.5300                33.5300               67.0600
7                 prov_departamento        proveedor  centinela textual  16205 33.5300                33.5300               67.0600
8                       prov_espyme        proveedor  centinela textual  16205 33.5300                33.5300               67.0600
9                       n_oferentes          proceso   cero estructural  14330 29.6500                 0.0800               29.7300
10         valor_adjudicado_proceso          proceso   cero estructural  12932 26.7600                 0.0800               26.8400
11                n_visualizaciones          proceso   cero estructural  12921 26.7300                 0.0800               26.8100
12                           ciudad         contrato  centinela textual   8433 17.4500                 0.0000               17.4500
13               plazo_discretizado  derivada propia  centinela textual   6212 12.8500                12.8500               25.7000
14               plazo_proceso_dias          proceso   cero estructural   4272  8.8400                 0.0800                8.9200
15                 tipodocproveedor         contrato  centinela textual   3469  7.1800                 0.0000                7.1800
16            duraci_n_del_contrato         contrato  centinela textual   3056  6.3200                 0.0000                6.3200
17                     departamento         contrato  centinela textual   1599  3.3100                 0.0000                3.3100
18                 tipo_contratista  derivada propia  centinela textual    971  2.0100                 0.0000                2.0100
19                    rango_cuantia  derivada propia  centinela textual    696  1.4400                 1.4400                2.8800
```
