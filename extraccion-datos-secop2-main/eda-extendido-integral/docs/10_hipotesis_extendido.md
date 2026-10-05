# 10 — Contraste extendido de las hipotesis A-H1, A-H2 y A-H3

**Proposito.** Someter las tres hipotesis del numeral 3.2 del anteproyecto a un contraste mas exigente
que el del EDA descriptivo previo: A-H1 con competencia real y con control por cuantia mediante
estratificacion, A-H2 con perfil de contratista y control por cuantia, y A-H3 con analisis de
sensibilidad territorial con y sin el departamento dominante.

**Insumo.** `data/universo_extendido.parquet` (notebook 01), `data/sobrecosto_referencias.parquet`
(notebook 05).

**Etiquetas de objetivo que atiende:** `[A-H1]`, `[A-H2]`, `[A-H3]`, `[A-OE03]`, `[A-OE04]`,
`[B-OE2]`, `[B-OE3-insumo]`.

**Reglas estadisticas declaradas a priori.**

1. Alfa 0.05.
2. Asimetria verificada en el notebook 09: se usan pruebas de rangos (Mann-Whitney U, Kruskal-Wallis).
3. Todo p-valor se acompana de tamano de efecto (rank-biserial o epsilon-cuadrado) y de N efectivo.
4. Con N grande, un p-valor significativo con tamano de efecto nulo **no** sostiene la hipotesis, y asi
   se declara cuando ocurre.
5. El control por una tercera variable se hace por **estratificacion**, reportando el efecto dentro de
   cada estrato. No se usa regresion multivariada porque excede el alcance descriptivo del trabajo.
6. Signo del rank-biserial: se calcula como `1 - 2U/(n1*n2)` con el primer grupo en primera posicion.
   Un valor **negativo** significa que el primer grupo tiene rangos **mayores**.
7. Las hipotesis estaban preregistradas en el anteproyecto y no son exploracion masiva, de modo que no
   se aplica correccion por comparaciones multiples. Se declara explicitamente y se senala cuando un
   p-valor cae en zona de riesgo.

**Diseno.** Transversal, censal condicionado. Ninguna asociacion aqui reportada es causal.

> Documento generado automaticamente a partir de `notebooks/10_hipotesis_extendido.ipynb` ya ejecutado, por `build/gen_docs.py`. No editar a mano.

---

## 1. A-H1 — Formulacion original: licitacion publica frente al resto

> **A-H1.** Los contratos de obra publica adjudicados mediante licitacion publica presentan menores
> desviaciones de costo y tiempo que los adjudicados mediante modalidades de menor competencia.

Se reproduce primero el contraste tal como lo formulo el anteproyecto, en doble lectura, e incorporando
el indicador de sobrecosto redefinido en el notebook 05, que el EDA previo no tenia.

**Designacion de lectura oficial (instruccion del tutor, reunion de seguimiento).** El anteproyecto original delimitaba el analisis al periodo 2018-2024 (numeral 1.2) y a un subconjunto con estado de ejecucion avanzado/finalizado (numerales 3.6.3/3.6.4). En la reunion de seguimiento, el tutor instruyo unificar el universo de datos con el trabajo del companero (Angel) y usar el total de contratos disponibles para el analisis final, dejando de lado la restriccion temporal del anteproyecto.

En consecuencia: **`universo_completo` (48.331 contratos) es la lectura oficial para el documento de trabajo de grado.** La lectura `observable` (19.194 contratos, filtro 2018-2024 + estado avanzado/finalizado) se conserva como analisis de sensibilidad — permite verificar si el patron se sostiene tambien bajo el diseno metodologico originalmente declarado en el anteproyecto, pero no es la cifra a citar en el capitulo de resultados.

## 2. A-H1 con control por cuantia mediante estratificacion

El notebook 05 mostro que la licitacion publica se concentra en los rangos altos de cuantia y que el
desempeno de plazo empeora con la cuantia. Ambas condiciones definen una variable de confusion. Se
controla estratificando: se repite el contraste dentro de cada rango de cuantia. Si el efecto de la
modalidad persiste dentro de los estratos, es efecto de modalidad; si se desvanece, era efecto de escala.

## 3. A-H2 — Consorcios y uniones temporales

> **A-H2.** Los contratos ejecutados por consorcios o uniones temporales presentan un mayor indice de
> adiciones y modificaciones contractuales que los ejecutados por personas juridicas individuales.

## 4. A-H3 — Heterogeneidad territorial y sensibilidad al departamento dominante

> **A-H3.** Los contratos de obra publica en municipios con mayores indices de necesidades basicas
> insatisfechas presentan mayores desviaciones en tiempo y costo.

**Declaracion previa al resultado, no posterior.** A-H3 **no puede probarse** con los datos disponibles.
El indice de necesidades basicas insatisfechas no existe en SECOP y no se ha incorporado ninguna fuente
externa del DANE. Lo que sigue es un analisis exploratorio de heterogeneidad territorial usando el
departamento como aproximacion imperfecta. El departamento no es NBI y no debe presentarse como tal.
La contribucion propia de este cuaderno respecto del EDA previo es el analisis de sensibilidad: verificar
si la heterogeneidad territorial detectada sobrevive a la exclusion del departamento dominante.

## 5. Cuadro consolidado de veredictos

## 6. Sintesis de hallazgos etiquetados

## Sintesis del notebook 10

| ID | Hallazgo | Etiquetas |
|---|---|---|
| H10-01 | A-H1 se invierte en tiempo y se sostiene en costo, en el universo completo (lectura oficial, 48.331) y de forma consistente en el subconjunto observable (19.194) | `[A-H1]` `[B-OE2]` |
| H10-02 | El efecto de la modalidad sobre el plazo se reduce al estratificar por cuantia | `[A-H1]` `[A-OE03]` `[B-OE2]` |
| H10-03 | A-H2 se sostiene en modificaciones, no en adiciones de valor, y se invierte en alcance | `[A-H2]` `[B-OE2]` |
| H10-04 | El efecto de A-H2 tambien se reduce al controlar por cuantia | `[A-H2]` `[A-OE03]` |
| H10-05 | **Contradice al EDA previo**: la heterogeneidad territorial en tiempo se desvanece sin el departamento dominante; en costo se refuerza | `[A-H3]` `[B-OE2]` `[CALIDAD]` |
| H10-06 | El peso del departamento dominante aumenta tras el filtro de observabilidad | `[CALIDAD]` `[A-OE03]` |
| H10-07 | El perfil del registro externo no puede caracterizar A-H2 sin sesgo de cobertura | `[CALIDAD]` `[A-H2]` |
| H10-08 | `n_extension` es una bandera binaria, no un conteo | `[CALIDAD]` |

**Productos persistidos:** `data/h1_contraste_base.csv`, `data/h1_estratificado_por_cuantia.csv`,
`data/h2_contraste_base.csv`, `data/h2_estratificado_por_cuantia.csv`,
`data/h3_perfil_territorial.csv`, `data/h3_sensibilidad_territorial.csv`,
`data/veredictos_hipotesis.csv`, `figuras/10_h1_estratificado.png`, `figuras/10_h3_territorial.png`.

**Lo que un jurado cuestionara y como responderlo.**

| Cuestionamiento | Respuesta preparada |
|---|---|
| "¿Su hipotesis H1 se cumple o no?" | Se cumple en costo y se invierte en tiempo. Esa disociacion es el hallazgo, no un fracaso. Ademas se identifico que el mecanismo enunciado (la competencia) no es el que opera: medida con el numero real de oferentes, la competencia tiene efecto nulo sobre el plazo. |
| "¿Por que estratificacion y no regresion?" | Porque el alcance del trabajo es descriptivo-analitico. La estratificacion responde la misma pregunta de confusion sin asumir forma funcional ni requerir supuestos de residuos, y el efecto dentro de cada estrato es directamente interpretable. |
| "Diez pruebas sin correccion por comparaciones multiples" | Las hipotesis estaban preregistradas en el numeral 3.2 del anteproyecto, no son exploracion masiva. Los p-valores relevantes estan en ordenes muy inferiores a cualquier correccion concebible. La unica prueba en zona de riesgo ya fue descartada por tamano de efecto nulo. |
| "¿H3 esta probada?" | No, y se declara antes del resultado, no despues. El departamento no es NBI. El analisis de sensibilidad ademas muestra que la heterogeneidad territorial en tiempo depende casi por completo del departamento dominante, mientras que en costo es robusta. Presentar ambas cosas es mas defendible que presentar solo el estadistico global. Incorporar NBI del DANE es trabajo futuro inmediato. |

---

## Figuras producidas por este cuaderno

- `figuras/10_h1_estratificado.png`
- `figuras/10_h3_territorial.png`

---

## Hallazgos etiquetados de este cuaderno

| ID | Celda | Hallazgo | Etiquetas | Evidencia | Valor |
|---|---|---|---|---|---|
| H10-01 | `c004` | A-H1 se invierte en tiempo y se sostiene en costo, en el universo completo (lectura oficial) y de forma consistente en el subconjunto observable, con el indicador de sobrecosto redefinido | [A-H1] [B-OE2] | Universo completo (lectura oficial), deslizamiento: rank-biserial -0.3798; observable (sensibilidad): -0.3862; costo: positivo con efecto mediano en ambas lecturas | Alto |
| H10-02 | `c006` | El efecto de la modalidad sobre el deslizamiento del plazo se reduce sustancialmente al estratificar por cuantia | [A-H1] [A-OE03] [B-OE2] | efecto bruto 0.3798 frente a magnitud media dentro de estratos 0.1113 | Alto |
| H10-03 | `c008` | A-H2 se sostiene en modificaciones totales, NO se sostiene en adiciones de valor pese al p-valor significativo, y se invierte en alcance | [A-H2] [B-OE2] | Tabla de contraste de A-H2 en doble lectura, con tamano de efecto por variable | Alto |
| H10-04 | `c009` | El efecto de A-H2 tambien se reduce al controlar por cuantia, aunque menos que el de A-H1 | [A-H2] [A-OE03] | reduccion del 73.6% al estratificar | Alto |
| H10-05 | `c012` | CONTRADICE AL EDA PREVIO: la heterogeneidad territorial en TIEMPO se desvanece al excluir el departamento dominante; en COSTO se refuerza | [A-H3] [B-OE2] [CALIDAD] | epsilon2 en tiempo (observable) pasa de 0.0577 a 0.0098; en costo de 0.0303 a 0.0522 | Alto |
| H10-08 | `c008` | `n_extension` del pipeline compartido es una bandera binaria, no un conteo: no puede sostener una prueba de 'mayor indice de extensiones' | [CALIDAD] | 2 valores distintos (0 y 1) en las 48.331 filas; la prueba de A-H2 sobre esa variable devuelve p = 1.0 y efecto exactamente 0 | Medio |
| H10-06 | `c011` | El peso del departamento dominante aumenta tras el filtro de observabilidad | [CALIDAD] [A-OE03] | Comparacion de la participacion del departamento dominante entre universo y observable | Alto |
| H10-07 | `c010` | El perfil de proveedor del registro externo no puede usarse para caracterizar A-H2 sin sesgo, porque su cobertura difiere fuertemente entre consorcios y personas juridicas | [CALIDAD] [A-H2] | Columna cobertura_registro_pct del perfil comparado | Alto |

---

## Apendice: salida literal de las celdas citadas como evidencia

Cada bloque reproduce la salida de la celda cuyo `execution_count` coincide con la referencia `cNNN` de la tabla anterior, tal como quedo persistida en el `.ipynb` ejecutado.

### Celda `c004`

```
=== A-H1, DESLIZAMIENTO DEL PLAZO, estratificado por rango de cuantia ===
          lectura  rango_cuantia  N_licitacion  N_otras  mediana_licitacion  mediana_otras              p  rank_biserial tamano_efecto
universo_completo           <50M             2     8279                 NaN            NaN N insuficiente            NaN  no evaluable
universo_completo       50M-200M             8    10002                 NaN            NaN N insuficiente            NaN  no evaluable
universo_completo    200M-1.000M          1355     9033              3.0000         1.0000       1.15e-13        -0.1247       pequeno
universo_completo 1.000M-10.000M          3872     2819             32.0000         6.0000       3.76e-18        -0.1241       pequeno
universo_completo       >10.000M          1371      336             50.0000        18.5000         0.0155        -0.0851          nulo
       observable           <50M             0     3202                 NaN            NaN N insuficiente            NaN  no evaluable
       observable       50M-200M             4     4203                 NaN            NaN N insuficiente            NaN  no evaluable
       observable    200M-1.000M           690     4213             12.0000         3.0000       3.03e-06        -0.1106       pequeno
       observable 1.000M-10.000M          1927     1336             55.0000        19.5000       4.10e-12        -0.1425       pequeno
       observable       >10.000M           614      137            113.0000        89.0000         0.2649        -0.0609          nulo

=== A-H1, DESVIACION DE COSTO, estratificado por rango de cuantia ===
          lectura  rango_cuantia  N_licitacion  N_otras  mediana_licitacion  mediana_otras              p  rank_biserial tamano_efecto
universo_completo           <50M             0     3711                 NaN            NaN N insuficiente            NaN  no evaluable
universo_completo       50M-200M             7     3888                 NaN            NaN N insuficiente            NaN  no evaluable
universo_completo    200M-1.000M           651     3502             -0.8700        -0.0000       1.37e-15         0.1899       pequeno
universo_completo 1.000M-10.000M          1695     1038             -6.5800        -0.4400       2.36e-07         0.1167       pequeno
universo_completo       >10.000M           439      102            -25.6200       -38.3900         0.3067        -0.0649          nulo
       observable           <50M             0     1911                 NaN            NaN N insuficiente            NaN  no evaluable
       observable       50M-200M             4     2225                 NaN            NaN N insuficiente            NaN  no evaluable
       observable    200M-1.000M           404     2114             -0.0900         0.0000       5.92e-15         0.2320       pequeno
       observable 1.000M-10.000M          1043      677             -1.3500        -0.0100       4.06e-05         0.1153       pequeno
       observable       >10.000M           241       62            -13.7700       -17.9200         0.8243         0.0183          nulo
```

### Celda `c006`

```
Figura persistida: 10_h1_estratificado.png
```

### Celda `c008`

```
=== A-H2, MODIFICACIONES TOTALES, estratificado por rango de cuantia ===
          lectura  rango_cuantia  N_consorcio  N_persona_juridica  mediana_consorcio  mediana_persona_juridica        p  rank_biserial tamano_efecto
universo_completo           <50M          206                8243             1.0000                    1.0000   0.0174        -0.0925          nulo
universo_completo       50M-200M          965                9698             2.0000                    1.0000 3.40e-11        -0.1253       pequeno
universo_completo    200M-1.000M         3128                7908             3.0000                    2.0000 3.17e-16        -0.0985          nulo
universo_completo 1.000M-10.000M         4528                3813             4.0000                    4.0000 1.50e-07        -0.0663          nulo
universo_completo       >10.000M         1770                 400             5.0000                    5.0000   0.2401        -0.0373          nulo
       observable           <50M           83                2756             2.0000                    2.0000   0.0133        -0.1524       pequeno
       observable       50M-200M          405                3776             3.0000                    2.0000 3.00e-06        -0.1378       pequeno
       observable    200M-1.000M         1390                3467             4.0000                    3.0000 8.83e-10        -0.1113       pequeno
       observable 1.000M-10.000M         1968                1778             7.0000                    6.0000 1.51e-04        -0.0714          nulo
       observable       >10.000M          716                 142             8.0000                    8.0000   0.7281         0.0184          nulo

Efecto bruto (observable): -0.3721
Magnitud media dentro de estratos: 0.0983
Reduccion al controlar por cuantia: 73.6%
```

### Celda `c009`

```
Distribucion del indice de alcance por tipo de contratista (observable):
indice_alcance              Entregado en su totalidad  Entregado parcialmente  No entregado
tipo_contratista                                                                           
Consorcio / Union Temporal                    49.4000                 38.3000       12.4000
Persona Juridica                              59.0000                 14.5000       26.4000

Chi-cuadrado, tipo de contratista x indice de alcance:
  chi2 = 1,225.57 | gl = 2 | p = 7.41e-267 | V de Cramer = 0.273 (debil-moderado) | N efectivo = 16,481 | minima frecuencia esperada = 961.9

PATRON MIXTO (extension del insight N-K02). Los consorcios acumulan mas modificaciones pero
presentan MENOR tasa de no entrega que las personas juridicas. A-H2 acierta en el volumen de
modificaciones y no implica peor desempeno de alcance.

Perfil comparado de los dos grupos:
                                n      mediana_valor  mediana_oferentes  pct_pyme  pct_licitacion  mediana_deslizamiento  pct_retraso_mayor_30  cobertura_registro_pct
tipo_contratista                                                                                                                                                      
Consorcio / Union Temporal   4562 1,480,005,224.0000             5.0000   34.5000         55.4000                27.0000               48.7000                  0.0000
Persona Juridica            11919   161,133,542.0000             1.0000   64.2000         11.3000                 1.0000               28.5000                 82.4000

Limitacion declarada: el perfil de proveedor procedente del registro externo esta disponible para
una fraccion mucho menor de los consorcios, de modo que `tipo_empresa`, antiguedad y UNSPSC no
pueden usarse para caracterizar A-H2 sin sesgo. Se declara y no se usa para el contraste.
```

### Celda `c012`

```
Figura persistida: 10_h3_territorial.png
```

### Celda `c011`

```
          lectura               indicador                     escenario          H  gl         p  epsilon2       tamano_efecto  N_efectivo  k_departamentos
universo_completo Deslizamiento del plazo CON el departamento dominante 1,346.7500   7 1.28e-286    0.0559      debil-moderado       23972                8
universo_completo Deslizamiento del plazo SIN el departamento dominante   101.4200   7  5.50e-19    0.0061 nulo/insignificante       15409                8
universo_completo     Desviacion de costo CON el departamento dominante   156.1300   7  2.09e-30    0.0159               debil        9401                8
universo_completo     Desviacion de costo SIN el departamento dominante   147.5200   7  1.35e-28    0.0232               debil        6062                8
       observable Deslizamiento del plazo CON el departamento dominante   670.6700   7 1.45e-140    0.0577      debil-moderado       11512                8
       observable Deslizamiento del plazo SIN el departamento dominante    70.7400   7  1.05e-12    0.0098 nulo/insignificante        6541                8
       observable     Desviacion de costo CON el departamento dominante   190.3200   7  1.28e-37    0.0303               debil        6048                8
       observable     Desviacion de costo SIN el departamento dominante   205.8800   7  6.53e-41    0.0522      debil-moderado        3817                8

VEREDICTO SOBRE A-H3
==============================================================================
A-H3 NO SE PRUEBA: no hay NBI municipal en el dataset y el departamento no es NBI.

universo_completo  | Deslizamiento del plazo  epsilon2 0.0559 -> 0.0061 (-89%)
universo_completo  | Desviacion de costo      epsilon2 0.0159 -> 0.0232 (+46%)
observable         | Deslizamiento del plazo  epsilon2 0.0577 -> 0.0098 (-83%)
observable         | Desviacion de costo      epsilon2 0.0303 -> 0.0522 (+72%)

RESULTADO QUE CONTRADICE LA EXPECTATIVA Y SE REPORTA IGUAL:
la heterogeneidad territorial en TIEMPO NO sobrevive a excluir el departamento dominante: el
tamano de efecto cae a la categoria nula. En COSTO ocurre lo contrario: el efecto AUMENTA al
excluirlo, de modo que ahi la heterogeneidad si es genuinamente multi-departamental.

Consecuencia para la sustentacion: el resultado territorial en tiempo del EDA descriptivo previo
(Kruskal-Wallis H = 670.67) esta dominado por un solo departamento y no debe presentarse como
evidencia de heterogeneidad territorial general. El resultado en costo si es robusto.
```

### Celda `c010`

```
Departamento dominante: Distrito Capital de Bogotá
  7,345 contratos observables (38.3% del subconjunto)
  14,338 contratos en el universo (29.7%)

Concentracion tras el filtro de observabilidad: el peso del departamento dominante pasa de 29.7% a 38.3% (extension del insight N-06).

                               n  n_ef_tiempo  mediana_deslizamiento  pct_retraso_mayor_30  n_ef_costo  mediana_costo  pct_no_entregado    mediana_valor
departamento                                                                                                                                            
Distrito Capital de Bogotá  7345         5365                15.0000               45.0000        2618         0.0000           26.7000 359,940,995.0000
Antioquia                   2062         1936                 1.0000               17.3000        1179        -0.0000           26.3000 166,431,773.0000
Valle del Cauca              919          854                 3.0000               34.0000         144         0.0000           15.8000 439,337,686.0000
Boyacá                       841          820                 1.0000               26.6000         394        -0.0000           10.8000  95,189,183.0000
Caldas                       793          733                 1.0000               28.5000         305       -10.0125           41.9000 159,998,523.0000
Cundinamarca                 745          685                 1.0000               27.9000         460        -0.0000           10.9000 220,316,110.0000
Santander                    654          618                 1.0000               28.2000         484         0.0000           17.1000 198,219,907.5000
Norte de Santander           521          501                 1.0000               21.4000         464         0.0000           12.3000 299,107,156.0000
Huila                        466          394                 0.0000               25.1000         387         0.0000           21.9000 227,037,842.5000
No Definido                  436          364                 1.0000               25.5000         217         0.0000           31.7000 116,723,580.0000
```
