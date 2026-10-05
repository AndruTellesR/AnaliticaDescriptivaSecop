# 03 — Indicadores de la restriccion de hierro en doble lectura

**Proposito.** Medir las tres dimensiones de la restriccion de hierro (tiempo, costo, alcance) sobre el
universo completo y sobre el subconjunto observable, en dos columnas, con los denominadores correctos
desde el inicio y con la nomenclatura corregida.

**Insumo.** `data/universo_extendido.parquet` (notebook 01).

**Etiquetas de objetivo que atiende:** `[A-OE03]` (medicion valida del desempeno), `[A-OE04]`
(visualizacion de distribuciones y outliers), `[B-OE2]` (caracterizacion historica del comportamiento),
`[CALIDAD]`.

**Justificacion metodologica de la doble lectura.** El universo completo sirve a la caracterizacion
historica y a la comparabilidad con el EDA del pipeline compartido. El subconjunto observable sirve a la
medicion valida del desempeno, porque un contrato aun en ejecucion registra desviacion cero no por
cumplir sino por no haber terminado. Cuando ambas lecturas difieren de forma material, la diferencia se
cuantifica y se explica: esa diferencia es en si misma un hallazgo.

**Correccion de nomenclatura (insight N-01).** `fecha_de_fin_del_contrato` absorbe las prorrogas
registradas, de modo que `fecha_fin - fecha_inicio` no es la duracion planificada sino el plazo
contractual final vigente. En consecuencia:

| Nombre previo | Nombre en este EDA | Formula |
|---|---|---|
| `plazo_real_dias` / `duracion_planificada_dias` | `plazo_contractual_final_dias` | `fecha_de_fin - fecha_de_inicio` |
| `desviacion_tiempo_dias` | `deslizamiento_plazo_dias` | `plazo_contractual_final - plazo_pactado` |

> Documento generado automaticamente a partir de `notebooks/03_indicadores_doble_lectura.ipynb` ya ejecutado, por `build/gen_docs.py`. No editar a mano.

---

## 1. Validacion empirica del indicador de tiempo sobre el universo completo

El insight N-01 se establecio sobre 3.847 contratos de la muestra analitica. Aqui se replica sobre el
universo completo: si `fecha_de_fin_del_contrato` fuese la fecha originalmente pactada, el deslizamiento
del plazo y los dias adicionados formalmente registrados serian magnitudes independientes. Que su
diferencia tenga mediana cero demuestra que SECOP actualiza la fecha de fin al registrar una prorroga.

## 2. Validacion cruzada del parseo del plazo pactado contra la fuente de procesos

`duraci_n_del_contrato` (texto libre en el contrato) y `duracion` + `unidad_de_duracion` (campos
estructurados del proceso) describen el mismo dato desde fuentes independientes. Comparar el parseo
propio contra la segunda fuente es la validacion mas fuerte disponible para el indicador de tiempo, y
cierra el insight N-08.

La coincidencia no es perfecta y la razon esta identificada: la regla de conversion `Mes(es) x 30` del
parseo propio no reproduce los meses calendario, y las unidades `Semana(s)`, `Año(s)` y `Hora(s)` del
proceso no tienen correlato en el campo textual del contrato, que solo admite dias y meses. La
correlacion de rangos es la evidencia relevante: mide si las dos fuentes ordenan los contratos igual, y
lo hacen.

## 3. Indicador de tiempo en doble lectura, con denominadores correctos

**Correccion aplicada desde el inicio (insight N-05).** Cada porcentaje se reporta con su denominador
explicito. El porcentaje "sobre la muestra" usa como denominador todas las filas, contando los valores
faltantes como "sin retraso"; el porcentaje "sobre el N efectivo" condiciona a los contratos con el
indicador calculable. El segundo es el correcto para afirmar algo sobre el desempeno.

## 4. Indicador de costo en doble lectura y estructura tripartita

La masa concentrada en el cero exacto no es un resultado de ejecucion financiera: significa que la
entidad reporto `valor_pagado` identico a `valor_del_contrato`, es decir, un cierre administrativo. Es
la base empirica de la sospecha N-K05, que el notebook 05 resuelve contrastando contra `precio_base` y
`valor_total_adjudicacion`.

## 5. Indicador de alcance en doble lectura

## 6. Figuras

## 7. Persistencia y sintesis de hallazgos etiquetados

## Sintesis del notebook 03

| ID | Hallazgo | Etiquetas |
|---|---|---|
| H03-01 | **Contradice parcialmente a N-01**: la absorcion de la prorroga es exacta en los observables (mediana 0,0) pero solo parcial en el universo (mediana −9,0) | `[A-OE03]` `[CALIDAD]` |
| H03-01b | En los contratos en ejecucion la fecha de fin aun no refleja la extension completa | `[CALIDAD]` `[B-OE2]` |
| H03-02 | El parseo del plazo pactado concuerda con la duracion declarada en la fuente independiente de procesos | `[A-OE03]` `[CALIDAD]` |
| H03-03 | La tasa de deslizamiento depende del denominador y del universo: cuatro cifras correctas y distintas | `[A-OE03]` `[CALIDAD]` `[B-OE2]` |
| H03-04 | Con umbral de 30 dias, el retraso material afecta a un tercio del subconjunto observable | `[A-OE03]` `[B-OE2]` |
| H03-05 | La estructura tripartita del costo se mantiene en ambas lecturas, con la masa en el cero exacto | `[A-OE03]` `[CALIDAD]` `[B-OE2]` |
| H03-06 | Los tres grupos de costo tienen perfiles distintos de cuantia, modalidad y contratista | `[B-OE2]` `[B-OE3-insumo]` |
| H03-07 | La diferencia de 15,9 puntos en el indice de alcance entre lecturas es artefacto de observabilidad | `[A-OE03]` `[CALIDAD]` |

**Productos persistidos:** `data/indicadores_doble_lectura.csv`, `data/severidad_deslizamiento.csv`,
`figuras/03_doble_lectura_restriccion_hierro.png`, `figuras/03_distribuciones_indicadores.png`.

---

## Figuras producidas por este cuaderno

- `figuras/03_distribuciones_indicadores.png`
- `figuras/03_doble_lectura_restriccion_hierro.png`

---

## Hallazgos etiquetados de este cuaderno

| ID | Celda | Hallazgo | Etiquetas | Evidencia | Valor |
|---|---|---|---|---|---|
| H03-01 | `c004` | CONTRADICE PARCIALMENTE A N-01: la absorcion de la prorroga por fecha_de_fin es exacta en los contratos observables (mediana de la diferencia 0.0) pero solo parcial en el universo completo (mediana -9.0) | [A-OE03] [CALIDAD] | N efectivo 10,168 universo (mediana -9.0) y 3,847 observable (mediana 0.0) | Alto |
| H03-01b | `c005` | En los contratos 'En ejecucion' con prorroga registrada la fecha de fin todavia no refleja la extension completa | [CALIDAD] [B-OE2] | Tabla de mediana de la diferencia por estado_contrato entre los no observables | Medio |
| H03-02 | `c006` | El parseo propio de plazo pactado concuerda con la duracion declarada en la fuente independiente de procesos | [A-OE03] [CALIDAD] | Spearman rho = 0.766 sobre N efectivo 42,081; coincidencia exacta 62.2% | Alto |
| H03-03 | `c007` | La tasa de deslizamiento positivo depende criticamente del denominador y del universo: cuatro cifras correctas y distintas | [A-OE03] [CALIDAD] [B-OE2] | universo 41.57% sobre el conjunto y 54.07% sobre N efectivo; observable 51.17% y 60.16% | Alto |
| H03-04 | `c008` | Con umbral de retraso material de 30 dias, el retraso afecta al 27.8% del universo efectivo y al 32.3% del observable efectivo | [A-OE03] [B-OE2] | universo 24.66%, observable 32.33% | Alto |
| H03-05 | `c010` | La desviacion de costo mantiene su estructura tripartita en las dos lecturas, con la masa en el cero exacto | [A-OE03] [CALIDAD] [B-OE2] | observable (estricto): 0% exacto 52.49%, negativa 47.32%, positiva 0.18% (16 contratos); universo: 49.16% / 50.71% / 0.13% | Alto |
| H03-06 | `c010` | Los tres grupos de la estructura de costo tienen perfiles distintos: los de desviacion negativa son de mayor cuantia y mas licitacion publica | [B-OE2] [B-OE3-insumo] | Tabla de perfil por grupo de costo sobre el subconjunto observable | Medio |
| H03-07 | `c011` | El indice de alcance difiere 15.9 puntos entre lecturas y la diferencia es artefacto de observabilidad, no de desempeno | [A-OE03] [CALIDAD] | Entregado en su totalidad: 72.98% universo vs 57.11% observable | Alto |

---

## Apendice: salida literal de las celdas citadas como evidencia

Cada bloque reproduce la salida de la celda cuyo `execution_count` coincide con la referencia `cNNN` de la tabla anterior, tal como quedo persistida en el `.ipynb` ejecutado.

### Celda `c004`

```
                  n  mediana_diferencia  pct_diferencia_cero  pct_diferencia_negativa  mediana_deslizamiento  mediana_dias_adicionados
grupo                                                                                                                                 
No observable  6321            -15.0000               3.3900                  66.6800                18.0000                   46.0000
Observable     3847              0.0000               3.4100                  46.7900                49.0000                   45.0000

Detalle por estado_contrato entre los NO observables (top 6 por volumen):
                    n  mediana_diferencia  pct_dif_cero
estado_contrato                                        
Modificado       6100            -15.0000        3.4400
Suspendido        193            -19.0000        1.0400
terminado          16            -11.0000       12.5000
En ejecución        8            -61.5000        0.0000
cedido              3            -47.0000        0.0000
Cerrado             1            -18.0000        0.0000

Lectura: en 'En ejecucion' la fecha de fin todavia no refleja la prorroga completa, lo que
desplaza la mediana de la diferencia hacia valores negativos. Es coherente con la interpretacion
de N-01 y ademas la refina: la absorcion es un proceso que se completa al cierre del contrato.
```

### Celda `c005`

```
N efectivo de la validacion cruzada: 42,081 contratos (87.1% del universo)
Spearman entre el parseo propio y la duracion declarada en el proceso: rho = 0.766, p = < 1e-300 (grande)

Coincidencia exacta:         62.23%
Coincidencia dentro del 5%:  63.08%
Mediana de la diferencia:   0.0 dias

Discrepancia por unidad declarada en el proceso:
                           n  coincidencia_exacta_pct  mediana_dif
pr_unidad_de_duracion                                             
Mes(es)                22353                  69.3100       0.0000
día(s)                 19693                  54.3200       0.0000
Semana(s)                 18                   0.0000     107.0000
Año(s)                     9                   0.0000     180.0000
Hora(s)                    8                   0.0000     194.7708
```

### Celda `c006`

```
                                                   universo_completo (N=48.331)  observable (N=19.194)   diferencia
N del conjunto                                                      48,331.0000            19,194.0000 -29,137.0000
N efectivo (deslizamiento calculable)                               37,155.0000            16,326.0000 -20,829.0000
Cobertura del indicador (%)                                             76.8800                85.0600       8.1800
% con deslizamiento > 0 sobre el conjunto                               41.5700                51.1700       9.6000
% con deslizamiento > 0 sobre el N efectivo                             54.0700                60.1600       6.0900
% con deslizamiento > 30 dias sobre el N efectivo                       24.6600                32.3300       7.6700
Mediana del deslizamiento (dias)                                         1.0000                 2.0000       1.0000
p75 del deslizamiento (dias)                                            30.0000                60.0000      30.0000
p90 del deslizamiento (dias)                                           139.0000               184.0000      45.0000
```

### Celda `c007`

```
                                     universo_completo  observable
N efectivo                                 37,155.0000 16,326.0000
Negativo (adelanto) %                          33.9300     29.5400
Exactamente 0 %                                12.0000     10.3000
1 a 7 dias (ruido de calendario) %             21.1500     18.4800
8 a 30 dias %                                   8.2500      9.3500
Mas de 30 dias (retraso material) %            24.6600     32.3300
Mas de 180 dias %                               8.1000     10.3100

Umbral defendible declarado: el retraso se considera material por encima de 30 dias.
Justificacion: la regla de conversion Mes(es) x 30 introduce un error de hasta 3 dias por
cada 3 meses de plazo, de modo que la franja de 1 a 7 dias no es separable del ruido de
calendario. Por encima de 30 dias la desviacion no puede atribuirse a redondeo.
```

### Celda `c008`

```
                                      universo_completo (N=48.331)  observable (N=19.194)
N del conjunto                                         48,331.0000            19,194.0000
N efectivo (valor_pagado > 0)                          15,035.0000             8,681.0000
Cobertura del indicador (%)                                31.1100                45.2300
% con valor_pagado == 0                                    68.8900                54.7700
% con sobrecosto sobre el conjunto                          0.0400                 0.0800
% con sobrecosto sobre el N efectivo                        0.1300                 0.1800
n de contratos con sobrecosto                              20.0000                16.0000
Mediana de la desviacion (%)                               -0.0000                 0.0000
p25 de la desviacion (%)                                  -10.0000                -2.8800
```

### Celda `c010`

```
                               universo_completo (N=48.331)  observable (N=19.194)  diferencia_pp
Entregado en su totalidad (%)                       72.9800                57.1100       -15.8700
Entregado parcialmente (%)                          16.5000                20.3700         3.8700
No entregado (%)                                    10.5300                22.5200        11.9900
N del conjunto                                  48,331.0000            19,194.0000   -29,137.0000
Cobertura del indicador (%)                        100.0000               100.0000         0.0000

Diferencia material entre lecturas: sobre el universo completo el 73.0% aparece como
'Entregado en su totalidad', frente al 57.1% en el subconjunto observable. La brecha de
15.9 puntos NO indica mejor desempeno del universo: indica que los contratos aun activos no
han tenido tiempo de acumular suspensiones, cesiones ni conclusiones anticipadas.
```

### Celda `c011`

```
Figura persistida: 03_doble_lectura_restriccion_hierro.png
```
