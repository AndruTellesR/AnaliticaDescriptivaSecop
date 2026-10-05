# 04 — Competencia real en el proceso de seleccion

**Proposito.** Cerrar la brecha 1 del documento comparativo, la mas seria de las identificadas: A-H1 es
literalmente una hipotesis sobre competencia y hasta ahora se operacionalizaba unicamente mediante la
modalidad de contratacion como variable indirecta. Este cuaderno incorpora la medida directa —el numero
de oferentes que efectivamente presentaron oferta— y contrasta A-H1 con ella.

**Insumo.** `data/universo_extendido.parquet` (notebook 01), bloque de variables de proceso.

**Etiquetas de objetivo que atiende:** `[A-H1]` (evidencia directa sobre la hipotesis),
`[A-OE04]` (segmentaciones y visualizacion), `[B-OE2]` (variables criticas asociadas a la eficiencia),
`[B-OE3-insumo]` (variables con asociacion relevante que serian candidatas predictoras),
`[CALIDAD]`.

**Advertencia metodologica.** La modalidad de contratacion y el numero de oferentes no son la misma
variable. La hipotesis A-H1 esta formulada sobre modalidades ("licitacion publica frente a modalidades
de menor competencia"), lo que presupone que la modalidad determina la competencia. Ese presupuesto se
somete a prueba en la seccion 2 antes de usar la competencia como contraste.

> Documento generado automaticamente a partir de `notebooks/04_competencia.ipynb` ya ejecutado, por `build/gen_docs.py`. No editar a mano.

---

## 1. Distribucion de las variables de competencia en doble lectura

## 2. ¿La modalidad determina la competencia? Verificacion del presupuesto de A-H1

A-H1 opone la licitacion publica a "modalidades de menor competencia". Antes de aceptar esa
equivalencia hay que comprobarla en el dato: si la licitacion publica no concentrara mas oferentes que
las demas modalidades, la formulacion de la hipotesis seria invalida en su premisa.

## 3. Relacion entre competencia real y desempeno

## 4. Contraste de A-H1 con competencia real

**Formulacion operativa.** A-H1 sostiene que a mayor competencia menores desviaciones de costo y tiempo.
Se define competencia alta como cuatro o mas oferentes unicos con oferta y competencia baja como uno a
tres, **excluyendo del contraste los contratos con cero oferentes registrados**, porque el cero es
ausencia de reporte y no ausencia de competencia (seccion 1). Alfa declarado a priori: 0.05.

**Resultado central de este cuaderno.** El tamano de efecto de la modalidad sobre el deslizamiento del
plazo es de magnitud mediana, mientras que el de la competencia real es nulo. Es decir: la variable que
A-H1 presupone determinante —la intensidad de la competencia— no discrimina el desempeno de plazo, y la
que si lo discrimina es la modalidad, que ademas selecciona proyectos de otra escala. Esto reorienta la
interpretacion de A-H1: lo que el dato muestra no es un efecto de competencia sino un efecto de tipo de
proyecto. El notebook 10 lo verifica controlando por cuantia mediante estratificacion.

## 5. Sintesis de hallazgos etiquetados

## Sintesis del notebook 04

| ID | Hallazgo | Etiquetas |
|---|---|---|
| H04-01 | El nivel de competencia mas frecuente es cero oferentes registrados: brecha de reporte, no de competencia | `[CALIDAD]` `[B-OE2]` |
| H04-02 | La premisa de A-H1 se verifica: la licitacion publica concentra mas oferentes que el resto | `[A-H1]` `[B-OE2]` |
| H04-03 | **Medida con competencia real, A-H1 no se sostiene en tiempo: efecto nulo** | `[A-H1]` `[B-OE2]` `[B-OE3-insumo]` |
| H04-04 | En costo la competencia real si discrimina, con efecto pequeno y signo consistente con N-K01 | `[A-H1]` `[B-OE3-insumo]` |
| H04-05 | El numero de oferentes correlaciona con la cuantia: mecanismo de confusion entre modalidad y escala | `[A-H1]` `[B-OE3-insumo]` |
| H04-06 | `n_respuestas` y `n_oferentes` son redundantes entre si | `[B-OE3-insumo]` `[CALIDAD]` |

**Productos persistidos:** `data/correlaciones_competencia.csv`,
`data/h1_modalidad_vs_competencia.csv`, `figuras/04_distribucion_competencia.png`,
`figuras/04_h1_competencia_real.png`.

**Como responderlo ante un jurado.** La pregunta previsible es "¿entonces su hipotesis H1 es falsa?".
La respuesta honesta es que H1 se sostiene parcialmente y por una razon distinta a la enunciada: la
licitacion publica si difiere del resto en desempeno, pero medir la competencia directamente muestra que
la intensidad de la competencia no es el mecanismo. Reportar el contraste con la variable indirecta y con
la variable directa, y declarar cual de las dos sostiene la conclusion, es mas defendible que reportar
solo la que confirma la hipotesis.

---

## Figuras producidas por este cuaderno

- `figuras/04_distribucion_competencia.png`
- `figuras/04_h1_competencia_real.png`

---

## Hallazgos etiquetados de este cuaderno

| ID | Celda | Hallazgo | Etiquetas | Evidencia | Valor |
|---|---|---|---|---|---|
| H04-01 | `c005` | El nivel de competencia mas frecuente es el de cero oferentes registrados, que es ausencia de reporte y no ausencia de competencia | [CALIDAD] [B-OE2] | 29.67% del universo y 24.75% del observable | Alto |
| H04-02 | `c007` | La premisa de A-H1 se verifica: la licitacion publica si concentra significativamente mas oferentes que el resto de modalidades | [A-H1] [B-OE2] | Mann-Whitney U = 48,961,585.5 / p = < 1e-300 / rank-biserial = -0.593 (grande) | Alto |
| H04-03 | `c011` | CONTRASTE CENTRAL: medida con competencia real, A-H1 NO se sostiene en la dimension de tiempo — el tamano de efecto es nulo | [A-H1] [B-OE2] [B-OE3-insumo] | Ver tabla h1_modalidad_vs_competencia.csv: efecto de modalidad de magnitud mediana frente a efecto de competencia nulo | Alto |
| H04-04 | `c010` | En la dimension de costo la competencia real si discrimina, aunque con efecto pequeno: a mayor competencia, desviacion de costo mas negativa | [A-H1] [B-OE3-insumo] | Rank-biserial positivo en costo con N efectivo declarado en la tabla de contraste | Alto |
| H04-05 | `c008` | El numero de oferentes correlaciona positivamente con la cuantia del contrato | [A-H1] [B-OE3-insumo] | Spearman en la tabla de correlaciones de competencia | Alto |
| H04-06 | `c004` | `n_respuestas` y `n_oferentes` son practicamente la misma variable: usar ambas seria redundancia | [B-OE3-insumo] [CALIDAD] | Spearman rho = 0.9949 | Medio |

---

## Apendice: salida literal de las celdas citadas como evidencia

Cada bloque reproduce la salida de la celda cuyo `execution_count` coincide con la referencia `cNNN` de la tabla anterior, tal como quedo persistida en el `.ipynb` ejecutado.

### Celda `c005`

```
Figura persistida: 04_distribucion_competencia.png
```

### Celda `c007`

```
   variable_competencia        variable_desempeno            lectura  rho_spearman          p  N_efectivo tamano_efecto
0           n_oferentes  deslizamiento_plazo_dias  universo_completo        0.0511   7.18e-23       37123          nulo
1           n_oferentes  deslizamiento_plazo_dias         observable       -0.0004     0.9569       16309          nulo
2           n_oferentes      desviacion_costo_pct  universo_completo       -0.1845  3.89e-115       15020       pequeno
3           n_oferentes      desviacion_costo_pct         observable       -0.2032   2.10e-81        8667       pequeno
4           n_invitados  deslizamiento_plazo_dias  universo_completo       -0.0681   2.18e-39       37123          nulo
5           n_invitados  deslizamiento_plazo_dias         observable       -0.1362   2.17e-68       16309       pequeno
6           n_invitados      desviacion_costo_pct  universo_completo       -0.0281   5.82e-04       15020          nulo
7           n_invitados      desviacion_costo_pct         observable       -0.0359   8.35e-04        8667          nulo
8     n_visualizaciones  deslizamiento_plazo_dias  universo_completo        0.1079   1.28e-96       37123       pequeno
9     n_visualizaciones  deslizamiento_plazo_dias         observable        0.0503   1.29e-10       16309          nulo
10    n_visualizaciones      desviacion_costo_pct  universo_completo       -0.2371  6.14e-191       15020       pequeno
11    n_visualizaciones      desviacion_costo_pct         observable       -0.2533  5.55e-127        8667       pequeno
12          n_oferentes    n_modificaciones_total  universo_completo        0.2074   < 1e-300       48293       pequeno
13          n_oferentes    n_modificaciones_total         observable        0.1848  6.37e-147       19177       pequeno
14          n_oferentes        valor_del_contrato  universo_completo        0.2698   < 1e-300       48293       pequeno
15          n_oferentes        valor_del_contrato         observable        0.2521  7.04e-276       19177       pequeno
```

### Celda `c011`

```
Figura persistida: 04_h1_competencia_real.png
```

### Celda `c010`

```
             lectura dimension  efecto_MODALIDAD (proxy) interpretacion_modalidad  efecto_COMPETENCIA_REAL interpretacion_competencia  N_modalidad  \
0  universo_completo    Tiempo                   -0.3798                  mediano                  -0.1117                    pequeno        37155   
1  universo_completo     Costo                    0.4277                  mediano                   0.1158                    pequeno        15035   
2         observable    Tiempo                   -0.3862                  mediano                  -0.0907                       nulo        16326   
3         observable     Costo                    0.4079                  mediano                   0.0809                       nulo         8681   

   N_competencia  
0          25598  
1          10410  
2          11789  
3           6165
```

### Celda `c008`

```
                              n  mediana_deslizamiento  n_ef_tiempo  pct_retraso_mayor_30  mediana_costo  n_ef_costo  pct_no_entregado    mediana_valor
competencia_cat                                                                                                                                        
0 (sin oferta registrada)  4747                 4.0000         4520               37.1000         0.0000        2502           25.9000 150,000,000.0000
1 (oferente unico)         3620                 1.0000         3264               27.7000        -0.0000        1733           25.1000 210,993,996.0000
2-3 (baja)                 2692                 1.0000         2269               26.2000        -0.0000        1268           19.8000 202,605,787.0000
4-9 (media)                4252                 1.0000         3332               26.4000         0.0000        1757           21.0000 292,008,156.5000
10+ (alta)                 3866                12.0000         2924               41.8000        -0.1167        1407           19.4000 999,999,989.5000

Kruskal-Wallis, deslizamiento del plazo entre niveles de competencia:
  H = 311.87 | gl = 4 | p = 2.99e-66 | epsilon2 = 0.0189 (debil) | k = 5 grupos | N efectivo = 16,309

Kruskal-Wallis, desviacion de costo entre niveles de competencia:
  H = 425.52 | gl = 4 | p = 8.52e-91 | epsilon2 = 0.0487 (debil-moderado) | k = 5 grupos | N efectivo = 8,667

Chi-cuadrado, nivel de competencia x indice de alcance:
  chi2 = 338.81 | gl = 8 | p = 2.21e-68 | V de Cramer = 0.094 (nulo/insignificante) | N efectivo = 19,177 | minima frecuencia esperada = 548.6
  ADVERTENCIA: significancia estadistica con tamano de efecto nulo. Con N grande esto NO sostiene la hipotesis.
```

### Celda `c004`

```
                           universo_completo  observable  universo_pct  observable_pct  diferencia_pp
competencia_cat                                                                                      
0 (sin oferta registrada)              14330        4747       29.6700         24.7500        -4.9200
1 (oferente unico)                      9997        3620       20.7000         18.8800        -1.8200
2-3 (baja)                              7029        2692       14.5500         14.0400        -0.5100
4-9 (media)                             8880        4252       18.3900         22.1700         3.7800
10+ (alta)                              8057        3866       16.6800         20.1600         3.4800

Hallazgo de calidad: el nivel de competencia mas frecuente del universo es el de CERO oferentes
registrados. No significa que el proceso quedara desierto —todos estos contratos existen y se
firmaron— sino que SECOP no publico el conteo de ofertas para ese procedimiento. Es una brecha de
reporte, no de competencia, y obliga a tratar el cero como categoria propia y no como 'sin ofertas'.

Modalidades donde el conteo de oferentes es cero (top 6 por volumen):
                                      n_cero  total_modalidad  pct_sin_conteo
modalidad_de_contratacion                                                    
Contratación directa                    9961             9981         99.8000
Contratación régimen especial           2890             2905         99.5000
Selección Abreviada de Menor Cuantía     554            12932          4.3000
Mínima cuantía                           362             9747          3.7000
Contratación Directa (con ofertas)       235             1541         15.2000
Licitación pública Obra Publica          193             8575          2.3000
```
