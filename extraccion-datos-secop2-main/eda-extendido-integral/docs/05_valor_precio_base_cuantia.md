# 05 — Valor del contrato, precio base y segmentacion por cuantia

**Proposito.** Resolver o cerrar el insight N-K05, objetivo analitico numero uno de este EDA: por que el
sobrecosto medido con `valor_pagado` es del 0,1% cuando el planteamiento del problema del anteproyecto
afirma que aproximadamente uno de cada cuatro contratos termina costando mas de lo presupuestado. Y
cerrar la brecha 3: la cuantia inicial es variable independiente declarada en el numeral 3.3 del
anteproyecto y hasta ahora no se habia segmentado.

**Insumo.** `data/universo_extendido.parquet` (notebook 01) y `data/marcas_calidad.parquet` (notebook 02,
marca `precio_base_valido`).

**Etiquetas de objetivo que atiende:** `[A-OE03]`, `[A-OE04]`, `[A-H1]`, `[B-OE2]`,
`[B-OE3-insumo]`, `[CALIDAD]`.

**Las cuatro magnitudes monetarias disponibles y lo que significa cada una.**

| Campo | Fuente | Momento del ciclo | Interpretacion |
|---|---|---|---|
| `precio_base` | proceso | antes de la adjudicacion | presupuesto oficial estimado por la entidad |
| `valor_total_adjudicacion` | proceso | en la adjudicacion | valor por el que se adjudico el proceso |
| `valor_del_contrato` | contrato | vigente al momento de la extraccion | valor contractual actual |
| `valor_pagado` | contrato | ejecucion | pagos reportados |

La hipotesis N-K05 sostiene que `valor_del_contrato` no es el valor inicial pactado sino el valor
actualizado tras adiciones. Si es cierta, comparar `valor_pagado` contra `valor_del_contrato` no puede
detectar sobrecosto por construccion, y el sobrecosto real debe aparecer al comparar
`valor_del_contrato` contra `precio_base` o contra `valor_total_adjudicacion`.

> Documento generado automaticamente a partir de `notebooks/05_valor_precio_base_cuantia.ipynb` ya ejecutado, por `build/gen_docs.py`. No editar a mano.

---

## 1. Depuracion de las magnitudes del proceso

## 2. Correlacion entre las cuatro magnitudes

## 3. Resolucion de N-K05: `valor_del_contrato` frente a `precio_base` y al valor adjudicado

**Diseno del contraste.** El sobrecosto se redefine como el exceso del valor contractual vigente sobre
el valor de referencia inicial. Se calculan dos versiones:

- `sobrecosto_vs_precio_base_pct` = `(valor_del_contrato - precio_base) / precio_base x 100`
- `sobrecosto_vs_adjudicado_pct` = `(valor_del_contrato - valor_total_adjudicacion) / valor_total_adjudicacion x 100`

Se aplica ademas una **tolerancia del 1%** para no contar como sobrecosto diferencias de redondeo, y se
reporta una version restringida a los procesos con **un unico contrato**, porque cuando un portafolio
agrupa varios contratos el valor adjudicado del proceso no es comparable con el valor de un solo
contrato. Esa restriccion es la lectura limpia.

## 4. Brecha de reporte de pagos frente al valor adjudicado (N-K04)

## 5. Segmentacion por rango de cuantia (brecha 3)

## 6. Persistencia y sintesis de hallazgos etiquetados

## Sintesis del notebook 05

| ID | Hallazgo | Etiquetas |
|---|---|---|
| H05-01 | **N-K05 resuelto**: el sobrecosto contra el presupuesto oficial del proceso es del orden del 24%, no del 0,1% | `[A-OE03]` `[B-OE2]` `[CALIDAD]` |
| H05-02 | El exceso sobre el precio base es mayor donde hay adicion de valor registrada: evidencia de mecanismo | `[A-OE03]` `[B-OE3-insumo]` |
| H05-03 | Los contratos con pago en cero tienen valor adjudicado positivo: brecha de reporte financiero | `[CALIDAD]` `[B-OE2]` |
| H05-04 | El retraso material crece con la cuantia pero la no entrega decrece: gradientes opuestos por dimension | `[A-OE04]` `[A-H1]` `[B-OE2]` `[B-OE3-insumo]` |
| H05-05 | Cuantia y modalidad estan fuertemente asociadas: obliga a estratificar A-H1 | `[A-H1]` `[B-OE2]` |
| H05-06 | `precio_base` correlaciona fuerte pero no perfectamente con `valor_del_contrato` | `[A-OE03]` `[B-OE3-insumo]` |

**Productos persistidos:** `data/nk05_sobrecosto_referencias.csv`,
`data/sobrecosto_referencias.parquet`, `data/perfil_por_cuantia_universo.csv`,
`data/perfil_por_cuantia_observable.csv`, `figuras/05_nk05_referencias_de_valor.png`,
`figuras/05_gradiente_por_cuantia.png`.

**Limitaciones declaradas del contraste de N-K05.**

1. `precio_base` es un presupuesto estimado, no un valor pactado. Un exceso sobre el presupuesto puede
   deberse a una adjudicacion por encima del estimado y no a una adicion posterior. La lectura contra
   `valor_total_adjudicacion` corrige ese sesgo y arroja una magnitud aun mayor.
2. Cuando un portafolio agrupa varios contratos, el valor adjudicado del proceso no es comparable con
   el valor de un contrato individual. Por eso la lectura titular se restringe a procesos con un unico
   contrato, y se reportan las cuatro lecturas para que el sesgo sea auditable.
3. Ninguna de las magnitudes esta deflactada. Las comparaciones son en pesos corrientes dentro de cada
   contrato, lo que es correcto porque el presupuesto, la adjudicacion y el valor contractual pertenecen
   al mismo proceso; no lo seria para comparar cuantias entre anios.

---

## Figuras producidas por este cuaderno

- `figuras/05_gradiente_por_cuantia.png`
- `figuras/05_nk05_referencias_de_valor.png`

---

## Hallazgos etiquetados de este cuaderno

| ID | Celda | Hallazgo | Etiquetas | Evidencia | Valor |
|---|---|---|---|---|---|
| H05-01 | `c007` | N-K05 RESUELTO: el sobrecosto contra el presupuesto oficial del proceso es del orden del 24%, frente al 0.1% medido contra valor_del_contrato | [A-OE03] [B-OE2] [CALIDAD] | 1 contrato por proceso: 23.60% supera precio_base en mas del 1%; 34.66% supera el valor adjudicado; 0.04% con la definicion previa | Alto |
| H05-02 | `c007` | El exceso sobre el precio base es mayor en los contratos con adicion de valor registrada, lo que confirma el mecanismo propuesto | [A-OE03] [B-OE3-insumo] | Mann-Whitney con tamano de efecto reportado en la celda de veredicto | Alto |
| H05-03 | `c009` | Los contratos con pago en cero tienen valor adjudicado positivo en el proceso: la brecha es de reporte de ejecucion financiera | [CALIDAD] [B-OE2] | Tabla de contraste pago frente a valor adjudicado, en doble lectura | Alto |
| H05-04 | `c011` | El retraso material crece monotonicamente con la cuantia, pero la NO ENTREGA se comporta al reves: decrece al subir la cuantia | [A-OE04] [A-H1] [B-OE2] [B-OE3-insumo] | Perfil por rango de cuantia en doble lectura: retraso > 30 dias sube del rango bajo al alto; alcance 'No entregado' baja | Alto |
| H05-05 | `c010` | La cuantia y la modalidad estan fuertemente asociadas: la licitacion publica se concentra en los rangos altos | [A-H1] [B-OE2] | Columna pct_licitacion del perfil por cuantia | Alto |
| H05-06 | `c005` | `precio_base` y `valor_del_contrato` correlacionan fuerte pero no perfectamente, lo que hace del primero una referencia inicial utilizable | [A-OE03] [B-OE3-insumo] | Matriz de Spearman entre las cuatro magnitudes monetarias | Medio |

---

## Apendice: salida literal de las celdas citadas como evidencia

Cada bloque reproduce la salida de la celda cuyo `execution_count` coincide con la referencia `cNNN` de la tabla anterior, tal como quedo persistida en el `.ipynb` ejecutado.

### Celda `c007`

```
Figura persistida: 05_nk05_referencias_de_valor.png
```

### Celda `c009`

```
=== UNIVERSO COMPLETO ===
                    n  n_ef_tiempo  mediana_deslizamiento  pct_retraso_mayor_30  n_ef_costo  mediana_costo  pct_no_entregado  pct_con_extension  mediana_oferentes  pct_licitacion  pct_consorcio
rango_cuantia                                                                                                                                                                                    
<50M            10800         8281                -1.0000                6.7000        3711         0.0000           14.5000            11.1000             1.0000          0.2000         1.9000
50M-200M        12743        10010                 1.0000               16.6000        3895         0.0000           13.7000            17.7000             1.0000          1.2000         7.6000
200M-1.000M     13051        10388                 1.0000               28.5000        4153        -0.0007            9.3000            26.2000             2.0000         14.3000        24.0000
1.000M-10.000M   8818         6691                18.0000               45.9000        2733        -5.0000            5.7000            33.8000             4.0000         59.4000        51.3000
>10.000M         2223         1707                44.0000               52.8000         541       -27.6442            2.4000            37.3000             5.0000         76.7000        79.6000

=== SUBCONJUNTO OBSERVABLE ===
                   n  n_ef_tiempo  mediana_deslizamiento  pct_retraso_mayor_30  n_ef_costo  mediana_costo  pct_no_entregado  pct_con_extension  mediana_oferentes  pct_licitacion  pct_consorcio
rango_cuantia                                                                                                                                                                                   
<50M            3617         3202                 0.0000                7.8000        1911         0.0000           35.2000             6.3000             1.0000          0.0000         2.3000
50M-200M        4998         4207                 1.0000               25.9000        2229         0.0000           30.4000            19.3000             1.0000          1.2000         8.1000
200M-1.000M     5750         4903                 4.0000               34.8000        2518        -0.0000           18.2000            21.7000             2.0000         14.6000        24.2000
1.000M-10.000M  3963         3263                36.0000               53.3000        1720        -0.3249           11.2000            32.8000             6.0000         62.1000        49.7000
>10.000M         866          751               109.0000               65.8000         303       -14.0979            5.0000            49.7000             6.0000         81.9000        82.7000
```

### Celda `c011`

```
Figura persistida: 05_gradiente_por_cuantia.png
```

### Celda `c010`

```
Kruskal-Wallis, deslizamiento del plazo entre rangos de cuantia (observable):
  H = 2,272.15 | gl = 4 | p = < 1e-300 | epsilon2 = 0.1390 (moderado) | k = 5 grupos | N efectivo = 16,326

Kruskal-Wallis, desviacion de costo entre rangos de cuantia (observable):
  H = 1,225.28 | gl = 4 | p = 5.26e-264 | epsilon2 = 0.1408 (moderado) | k = 5 grupos | N efectivo = 8,681

Chi-cuadrado, rango de cuantia x indice de alcance (observable):
  chi2 = 2,301.81 | gl = 8 | p = < 1e-300 | V de Cramer = 0.245 (debil-moderado) | N efectivo = 19,194 | minima frecuencia esperada = 176.4

Spearman valor ~ deslizamiento (observable): rho = 0.379, N efectivo = 16,326 (mediano)
Spearman valor ~ desviacion de costo (observable): rho = -0.359, N efectivo = 8,681 (mediano)
```

### Celda `c005`

```
                           lectura                                referencia  N_efectivo  % con exceso > 0  % con exceso > 1% (tolerancia)  % con exceso > 10%  mediana %   p75 %   p90 %
                 universo completo      vs precio_base (presupuesto oficial)       47147           22.1400                         21.2500             17.6100     0.0000  0.0000 31.5300
                 universo completo           vs valor adjudicado del proceso       35319           35.6500                         34.8900             29.4500     0.0000 17.8400 48.7400
                 universo completo vs valor_del_contrato (definicion previa)       15035            0.1300                          0.0500              0.0300    -0.0000  0.0000  0.0000
                        observable      vs precio_base (presupuesto oficial)       19065           32.2400                         31.1100             26.0000     0.0000 11.9600 41.4700
                        observable           vs valor adjudicado del proceso       15142           48.0600                         47.5100             40.7100     0.0000 32.4900 49.9400
                        observable vs valor_del_contrato (definicion previa)        8681            0.1800                          0.0600              0.0200     0.0000  0.0000  0.0000
  universo, 1 contrato por proceso      vs precio_base (presupuesto oficial)       39941           24.5600                         23.6000             19.5700     0.0000  0.0000 34.6500
  universo, 1 contrato por proceso           vs valor adjudicado del proceso       28715           34.9600                         34.6600             29.3400     0.0000 17.4400 47.8100
  universo, 1 contrato por proceso vs valor_del_contrato (definicion previa)       13849            0.1200                          0.0400              0.0100     0.0000  0.0000  0.0000
observable, 1 contrato por proceso      vs precio_base (presupuesto oficial)       16774           34.6800                         33.4800             28.0100     0.0000 15.0600 42.6300
observable, 1 contrato por proceso           vs valor adjudicado del proceso       12997           46.1500                         45.7700             38.9500     0.0000 29.2800 49.7200
observable, 1 contrato por proceso vs valor_del_contrato (definicion previa)        7933            0.1800                          0.0400              0.0100     0.0000  0.0000  0.0000
```
