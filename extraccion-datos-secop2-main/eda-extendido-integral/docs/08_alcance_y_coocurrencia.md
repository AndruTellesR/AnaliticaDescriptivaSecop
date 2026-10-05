# 08 — Co-ocurrencia de modificaciones, jerarquia del indice de alcance y duracion discretizada

**Proposito.** Cerrar las brechas 5 y 6 del documento comparativo. El indice de alcance colapsa
conclusion, suspension y cesion en una jerarquia excluyente; mostrar cuanto se solapan justifica —o
cuestiona— el orden de precedencia elegido. La duracion discretizada hace comunicable en un tablero lo
que la correlacion de Spearman expresa como coeficiente.

**Insumo.** `data/universo_extendido.parquet` (notebook 01).

**Etiquetas de objetivo que atiende:** `[A-OE03]` (justificacion de la construccion del indicador),
`[A-OE04]` (segmentacion y visualizacion), `[B-OE2]` (patrones de modificacion contractual),
`[B-OE3-insumo]`.

**Jerarquia sometida a examen.** `indice_alcance` se construye con la precedencia:
conclusion anticipada > (suspension o cesion) > entrega total. La justificacion semantica es que una
conclusion anticipada implica que el objeto no se entrego, mientras que una suspension o una cesion
indican entrega interrumpida o transferida. Este cuaderno comprueba si el orden es consistente con el
comportamiento observado de las tres banderas.

> Documento generado automaticamente a partir de `notebooks/08_alcance_y_coocurrencia.ipynb` ya ejecutado, por `build/gen_docs.py`. No editar a mano.

---

## 1. Matriz de co-ocurrencia entre banderas de modificacion

## 2. Solapamiento real entre las tres banderas del indice de alcance

## 3. Duracion discretizada y gradiente de extension

## 4. Estructura del numero de modificaciones

## 5. Sintesis de hallazgos etiquetados

## Sintesis del notebook 08

| ID | Hallazgo | Etiquetas |
|---|---|---|
| H08-01 | Suspension y extension co-ocurren muy por encima de lo esperado por azar | `[B-OE2]` `[B-OE3-insumo]` |
| H08-02 | El indice de alcance es robusto al orden de precedencia de su jerarquia | `[A-OE03]` |
| H08-03 | La tasa de extension crece monotonicamente con la duracion pactada | `[A-OE04]` `[B-OE2]` `[B-OE3-insumo]` |
| H08-04 | El numero de modificaciones se asocia al deslizamiento del plazo y a la cuantia | `[B-OE3-insumo]` `[B-OE2]` |

**Productos persistidos:** `data/coocurrencia_modificaciones_observable.csv`,
`data/gradiente_por_duracion_observable.csv`, `figuras/08_coocurrencia_modificaciones.png`,
`figuras/08_gradiente_por_duracion.png`.

**Advertencia de causalidad.** Ninguna de estas asociaciones es causal. En particular, el numero de
modificaciones y el deslizamiento del plazo son en parte la misma cosa medida de dos maneras: una
prorroga registrada es simultaneamente una modificacion y un desplazamiento de la fecha de fin. La
asociacion entre ambas no es un hallazgo sustantivo sino una consecuencia de como SECOP registra el
evento, y asi debe presentarse.

---

## Figuras producidas por este cuaderno

- `figuras/08_coocurrencia_modificaciones.png`
- `figuras/08_gradiente_por_duracion.png`

---

## Hallazgos etiquetados de este cuaderno

| ID | Celda | Hallazgo | Etiquetas | Evidencia | Valor |
|---|---|---|---|---|---|
| H08-01 | `c005` | La suspension y la extension de plazo co-ocurren muy por encima de lo esperado por azar | [B-OE2] [B-OE3-insumo] | Matriz de co-ocurrencia y chi-cuadrado con V de Cramer reportado | Alto |
| H08-02 | `c008` | El indice de alcance es robusto al orden de precedencia: invertir la jerarquia reclasifica menos del 1% de los contratos | [A-OE03] | 564 contratos observables tienen mas de una de las tres banderas (2.94%) | Alto |
| H08-03 | `c009` | La tasa de extension crece monotonicamente con la duracion pactada, del rango mas corto al mas largo | [A-OE04] [B-OE2] [B-OE3-insumo] | Gradiente por duracion discretizada en doble lectura, con chi-cuadrado y Kruskal-Wallis | Alto |
| H08-04 | `c011` | El numero de modificaciones se asocia al deslizamiento del plazo y a la cuantia del contrato | [B-OE3-insumo] [B-OE2] | Spearman con N efectivo declarado sobre el subconjunto observable | Medio |

---

## Apendice: salida literal de las celdas citadas como evidencia

Cada bloque reproduce la salida de la celda cuyo `execution_count` coincide con la referencia `cNNN` de la tabla anterior, tal como quedo persistida en el `.ipynb` ejecutado.

### Celda `c005`

```
Figura persistida: 08_coocurrencia_modificaciones.png
```

### Celda `c008`

```
=== UNIVERSO COMPLETO ===
                        n  pct_con_extension  pct_con_adicion_valor  pct_con_suspension  n_ef_tiempo  mediana_deslizamiento  pct_retraso_mayor_30  pct_no_entregado       mediana_valor
plazo_discretizado                                                                                                                                                                     
<=1 mes              8019             9.2000                 6.0000              9.9000         6790                -1.0000               11.5000            9.8000     39,023,726.0000
1-3 meses           14218            19.9000                 9.1000             13.8000        12392                 0.0000               17.2000            8.5000    134,793,816.0000
3-6 meses            9186            30.9000                10.0000             22.5000         8101                 2.0000               28.4000            7.3000    494,417,160.5000
6-12 meses           7728            31.6000                 6.9000             23.8000         7132                 4.0000               36.2000           12.0000    712,246,582.5000
1-2 anios            2248            44.5000                 7.6000             33.6000         2073                34.0000               50.8000            6.1000  4,754,760,994.5000
>2 anios              720            43.9000                 9.0000             25.6000          667                19.0000               46.8000            1.9000 11,906,947,599.0000

=== SUBCONJUNTO OBSERVABLE ===
                       n  pct_con_extension  pct_con_adicion_valor  pct_con_suspension  n_ef_tiempo  mediana_deslizamiento  pct_retraso_mayor_30  pct_no_entregado      mediana_valor
plazo_discretizado                                                                                                                                                                   
<=1 mes             2512             7.2000                 9.2000             12.7000         2512                -1.0000               15.4000           24.7000    37,640,350.5000
1-3 meses           5113            16.5000                13.8000             17.0000         5113                 1.0000               21.9000           19.0000   142,441,867.0000
3-6 meses           3779            25.1000                14.8000             26.9000         3779                 2.0000               34.5000           15.2000   509,486,298.0000
6-12 meses          3534            34.6000                 9.2000             29.1000         3534                30.5000               50.0000           23.5000   727,873,593.5000
1-2 anios           1087            47.4000                 9.6000             38.9000         1087                36.0000               51.7000           11.9000 3,311,389,672.0000
>2 anios             301            43.5000                12.6000             32.6000          301                16.0000               46.5000            4.0000 8,494,918,036.0000

Cifra de referencia del pipeline compartido: la tasa de extension pasa de 3.1% en contratos de
menos de un mes a 51.2% en contratos de mas de dos anios.

Chi-cuadrado, duracion discretizada x extension (observable):
  chi2 = 1,164.51 | gl = 5 | p = 1.43e-249 | V de Cramer = 0.267 (debil-moderado) | N efectivo = 16,326 | minima frecuencia esperada = 70.9
Kruskal-Wallis, deslizamiento del plazo entre rangos de duracion (observable):
  H = 1,462.80 | gl = 5 | p = < 1e-300 | epsilon2 = 0.0893 (debil-moderado) | k = 6 grupos | N efectivo = 16,326
```

### Celda `c009`

```
Figura persistida: 08_gradiente_por_duracion.png
```

### Celda `c011`

```
       id notebook celda                                           hallazgo                                          evidencia  \
0  H08-01       08  c005  La suspension y la extension de plazo co-ocurr...  Matriz de co-ocurrencia y chi-cuadrado con V d...   
1  H08-02       08  c008  El indice de alcance es robusto al orden de pr...  564 contratos observables tienen mas de una de...   
2  H08-03       08  c009  La tasa de extension crece monotonicamente con...  Gradiente por duracion discretizada en doble l...   
3  H08-04       08  c011  El numero de modificaciones se asocia al desli...  Spearman con N efectivo declarado sobre el sub...   

                         etiquetas  valor                                               nota  
0           [B-OE2] [B-OE3-insumo]   Alto  Replica con derivacion propia el dato del pipe...  
1                         [A-OE03]   Alto  Responde por anticipado a la objecion de que l...  
2  [A-OE04] [B-OE2] [B-OE3-insumo]   Alto  Cierra la brecha 6 y hace comunicable en table...  
3           [B-OE3-insumo] [B-OE2]  Medio  Variable de proceso interno, disponible solo d...
```
