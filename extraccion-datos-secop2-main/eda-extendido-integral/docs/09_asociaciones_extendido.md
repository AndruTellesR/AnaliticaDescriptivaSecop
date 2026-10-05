# 09 — Matriz extendida de asociaciones

**Proposito.** Extender la matriz de correlaciones y asociaciones del EDA descriptivo previo (5 variables
continuas y 2 tablas de contingencia) a todas las variables incorporadas por este ejercicio, y ordenar
el resultado por tamano de efecto. La tabla ordenada es el insumo `[B-OE3-insumo]`: identifica que
variables muestran asociacion relevante con el desempeno y por tanto **serian** candidatas predictoras
en un ejercicio de modelado posterior. Este cuaderno no entrena ningun modelo ni reporta metrica alguna
de clasificacion.

**Insumo.** `data/universo_extendido.parquet` (notebook 01) y `data/sobrecosto_referencias.parquet`
(notebook 05).

**Etiquetas de objetivo que atiende:** `[A-OE04]`, `[B-OE2]` (correlaciones y variables criticas),
`[B-OE3-insumo]`, `[A-H1]`, `[A-H2]`.

**Rigor declarado.** Alfa a priori de 0.05. Todas las variables continuas presentan asimetria severa
(se verifica en la seccion 1), de modo que se usa Spearman y no Pearson. Cada coeficiente se reporta con
su N efectivo. Con N del orden de las decenas de miles, la significancia estadistica es casi automatica:
la lectura correcta es el tamano de efecto, no el p-valor.

> Documento generado automaticamente a partir de `notebooks/09_asociaciones_extendido.ipynb` ya ejecutado, por `build/gen_docs.py`. No editar a mano.

---

## 1. Verificacion de supuestos antes de elegir el coeficiente

## 2. Matriz de Spearman extendida

## 3. Pares continuos ordenados por tamano de efecto

**Advertencia sobre relaciones definicionales.** Tres pares de la tabla anterior no son hallazgos
sustantivos sino consecuencias de como se construyen los indicadores: `plazo_contractual_final_dias`
frente a `deslizamiento_plazo_dias` (el segundo se calcula restando el plazo pactado al primero),
`dias_adicionados` frente a `deslizamiento_plazo_dias` (SECOP actualiza la fecha de fin al registrar la
prorroga, notebook 03) y `valor_pagado` frente a `desviacion_costo_pct`. Se dejan en la matriz por
completitud pero no deben leerse como asociacion empirica.

## 4. Asociaciones entre variables categoricas y desempeno

## 5. Tabla consolidada de variables con asociacion relevante

La tabla siguiente es el insumo `[B-OE3-insumo]`. Enumera las variables que muestran asociacion no
trivial con alguna dimension del desempeno y clasifica cada una segun **cuando** esta disponible en el
ciclo del contrato. Esa distincion es la que hace utilizable o no una variable en un ejercicio
predictivo posterior: una variable que solo existe una vez ocurrida la modificacion no puede anticiparla.
Este cuaderno se limita a senalar la distincion; no construye ningun modelo.

## 6. Sintesis de hallazgos etiquetados

## Sintesis del notebook 09

| ID | Hallazgo | Etiquetas |
|---|---|---|
| H09-01 | La variable categorica de mayor asociacion al desempeno se identifica con V de Cramer y N efectivo | `[B-OE2]` `[B-OE3-insumo]` `[A-OE04]` |
| H09-02 | Toda la matriz usa Spearman por asimetria verificada, no por supuesto | `[A-OE03]` |
| H09-03 | Ninguna variable anticipatoria supera el efecto mediano frente a la restriccion de hierro | `[B-OE2]` `[B-OE3-insumo]` |
| H09-04 | Las variables de mayor asociacion son mayoritariamente no anticipatorias | `[B-OE3-insumo]` `[CALIDAD]` |
| H09-05 | El sobrecosto sobre precio base es un indicador distinto y no redundante | `[A-OE03]` `[B-OE2]` |

**Productos persistidos:** `data/spearman_matriz_observable.csv`, `data/spearman_matriz_universo.csv`,
`data/pares_spearman_ordenados.csv`, `data/asociaciones_categoricas.csv`,
`data/insumo_variables_candidatas.csv`, `figuras/09_matriz_spearman_extendida.png`,
`figuras/09_asociaciones_categoricas.png`.

**Declaracion de alcance.** La tabla de variables candidatas es informacion sobre asociacion, no un
ejercicio de seleccion de variables ni un modelo. No se importa ninguna libreria de aprendizaje
automatico en este cuaderno ni en ningun otro de este EDA, y no se reporta ninguna metrica de
clasificacion.

---

## Figuras producidas por este cuaderno

- `figuras/09_asociaciones_categoricas.png`
- `figuras/09_matriz_spearman_extendida.png`

---

## Hallazgos etiquetados de este cuaderno

| ID | Celda | Hallazgo | Etiquetas | Evidencia | Valor |
|---|---|---|---|---|---|
| H09-01 | `c008` | La variable categorica con mayor asociacion al desempeno es `rango_cuantia` frente a retraso_material_mayor_30d | [B-OE2] [B-OE3-insumo] [A-OE04] | V de Cramer = 0.351, N efectivo = 16,326, moderado | Alto |
| H09-02 | `c004` | Todas las variables continuas del analisis presentan asimetria severa, lo que descarta Pearson por verificacion y no por supuesto | [A-OE03] | 14 de 16 variables con /skew/ > 1 | Medio |
| H09-03 | `c007` | Frente a los tres indicadores de la restriccion de hierro ninguna variable anticipatoria supera el tamano de efecto mediano; solo el numero de modificaciones alcanza efecto grande con la cuantia | [B-OE2] [B-OE3-insumo] | maximo /rho/ anticipatorio: valor_del_contrato ~ deslizamiento_plazo_dias = 0.3794 (mediano, N efectivo 16,326) | Alto |
| H09-04 | `c010` | Las variables con mayor asociacion al desempeno son mayoritariamente NO anticipatorias: se conocen durante o despues de la ejecucion | [B-OE3-insumo] [CALIDAD] | Tabla de variables candidatas con su momento de disponibilidad | Alto |
| H09-05 | `c005` | El sobrecosto sobre el precio base se comporta como un indicador distinto de la desviacion de costo previa, con su propio patron de asociaciones | [A-OE03] [B-OE2] | Fila correspondiente en la matriz de Spearman extendida | Alto |

---

## Apendice: salida literal de las celdas citadas como evidencia

Cada bloque reproduce la salida de la celda cuyo `execution_count` coincide con la referencia `cNNN` de la tabla anterior, tal como quedo persistida en el `.ipynb` ejecutado.

### Celda `c008`

```
Figura persistida: 09_asociaciones_categoricas.png
```

### Celda `c004`

```
Matriz de Spearman — subconjunto observable:
                  Valor contrato  Precio base  Plazo pactado  Plazo final  Deslizamiento  Desv. costo  Sobrecosto vs PB  Oferentes  Invitados  Visualizaciones  Modificaciones  Dias adicionados  Anio firma
Valor contrato            1.0000       0.9690         0.6040       0.6570         0.3790      -0.3590            0.1670     0.2520     0.0350           0.4600          0.5060            0.2530     -0.0490
Precio base               0.9690       1.0000         0.5980       0.6470         0.3690      -0.3510            0.0320     0.2880     0.0160           0.4660          0.4790            0.2380     -0.0640
Plazo pactado             0.6040       0.5980         1.0000       0.8770         0.3000      -0.2400            0.1830     0.0250    -0.1110           0.1010          0.3590            0.2910     -0.1640
Plazo final               0.6570       0.6470         0.8770       1.0000         0.6310      -0.2740            0.1700     0.0560    -0.1270           0.1250          0.5410            0.3490     -0.1410
Deslizamiento             0.3790       0.3690         0.3000       0.6310         1.0000      -0.1380            0.1320    -0.0000    -0.1360           0.0500          0.5100            0.3450     -0.1100
Desv. costo              -0.3590      -0.3510        -0.2400      -0.2740        -0.1380       1.0000           -0.1120    -0.2030    -0.0360          -0.2530         -0.2580           -0.2050     -0.0130
Sobrecosto vs PB          0.1670       0.0320         0.1830       0.1700         0.1320      -0.1120            1.0000    -0.2630     0.0740          -0.0940          0.1650            0.0950      0.1070
Oferentes                 0.2520       0.2880         0.0250       0.0560        -0.0000      -0.2030           -0.2630     1.0000     0.1340           0.7460          0.1850           -0.0160     -0.1550
Invitados                 0.0350       0.0160        -0.1110      -0.1270        -0.1360      -0.0360            0.0740     0.1340     1.0000           0.4420         -0.0440           -0.0820     -0.0050
Visualizaciones           0.4600       0.4660         0.1010       0.1250         0.0500      -0.2530           -0.0940     0.7460     0.4420           1.0000          0.2580            0.0260     -0.1160
Modificaciones            0.5060       0.4790         0.3590       0.5410         0.5100      -0.2580            0.1650     0.1850    -0.0440           0.2580          1.0000            0.1430     -0.0950
Dias adicionados          0.2530       0.2380         0.2910       0.3490         0.3450      -0.2050            0.0950    -0.0160    -0.0820           0.0260          0.1430            1.0000      0.1540
Anio firma               -0.0490      -0.0640        -0.1640      -0.1410        -0.1100      -0.0130            0.1070    -0.1550    -0.0050          -0.1160         -0.0950            0.1540      1.0000
```

### Celda `c007`

```
Asociaciones categoricas ordenadas por V de Cramer (todas las lecturas):
      variable_categorica                   objetivo           lectura       chi2  gl         p  V_cramer       tamano_efecto  N_efectivo  min_frecuencia_esperada
            rango_cuantia retraso_material_mayor_30d        observable 2,011.6700   4  < 1e-300    0.3510            moderado       16326                 242.8000
modalidad_de_contratacion retraso_material_mayor_30d        observable 2,009.5700   8  < 1e-300    0.3508            moderado       16326                  18.1000
            rango_cuantia retraso_material_mayor_30d universo_completo 4,211.1100   4  < 1e-300    0.3370            moderado       37077                 421.4000
modalidad_de_contratacion retraso_material_mayor_30d universo_completo 3,313.8700   8  < 1e-300    0.2986      debil-moderado       37155                  26.9000
       plazo_discretizado retraso_material_mayor_30d        observable 1,308.6800   5 8.41e-281    0.2831      debil-moderado       16326                  97.3000
modalidad_de_contratacion             indice_alcance        observable 2,763.3500  16  < 1e-300    0.2683      debil-moderado       19194                  24.9000
       plazo_discretizado retraso_material_mayor_30d universo_completo 2,511.7900   5  < 1e-300    0.2600      debil-moderado       37155                 164.5000
            rango_cuantia             indice_alcance        observable 2,301.8100   8  < 1e-300    0.2449      debil-moderado       19194                 176.4000
modalidad_de_contratacion             indice_alcance universo_completo 4,805.5200  16  < 1e-300    0.2230      debil-moderado       48331                  31.3000
             departamento retraso_material_mayor_30d        observable   803.0700  33 1.89e-147    0.2218      debil-moderado       16326                   0.6000
                  es_pyme retraso_material_mayor_30d        observable   682.2300   1 2.18e-150    0.2044      debil-moderado       16326               2,159.0000
         tipo_contratista retraso_material_mayor_30d        observable   675.2000   3 5.00e-146    0.2034      debil-moderado       16326                  34.3000
         tipo_contratista retraso_material_mayor_30d universo_completo 1,462.1200   3  < 1e-300    0.1984               debil       37155                  59.7000
            rango_cuantia             indice_alcance universo_completo 3,548.5400   8  < 1e-300    0.1930               debil       47635                 236.9000
             departamento retraso_material_mayor_30d universo_completo 1,305.5600  33 2.67e-253    0.1875               debil       37155                   0.7000
         tipo_contratista             indice_alcance        observable 1,300.5600   6 8.18e-278    0.1841               debil       19194                  23.8000
             departamento             indice_alcance        observable 1,119.2100  66 3.20e-191    0.1707               debil       19194                   0.4000
         tipo_contratista             indice_alcance universo_completo 2,534.9300   6  < 1e-300    0.1619               debil       48331                 102.2000
             departamento             indice_alcance universo_completo 2,274.9400  66  < 1e-300    0.1534               debil       48331                   0.3000
       plazo_discretizado             indice_alcance        observable   736.6700  10 8.39e-152    0.1502               debil       16326                  57.9000
          competencia_cat retraso_material_mayor_30d        observable   291.5100   4  7.35e-62    0.1337               debil       16309                 733.9000
       plazo_discretizado             indice_alcance universo_completo 1,481.3200  10  < 1e-300    0.1326               debil       42119                  64.0000
                  es_pyme retraso_material_mayor_30d universo_completo   627.9400   1 1.40e-138    0.1300               debil       37155               3,955.3000
        prov_tipo_empresa retraso_material_mayor_30d        observable   144.2700  25  9.53e-19    0.1173               debil       10488                   0.2000
        prov_tipo_empresa             indice_alcance        observable   337.8700  50  2.35e-44    0.1161               debil       12527                   0.3000
          competencia_cat retraso_material_mayor_30d universo_completo   494.0700   4 1.29e-105    0.1154               debil       37123               1,322.3000
                    orden             indice_alcance        observable   413.4100   4  3.51e-88    0.1038               debil       19194                  65.0000
                  es_pyme             indice_alcance        observable   201.6100   2  1.66e-44    0.1025               debil       19194               1,552.3000
        prov_tipo_empresa retraso_material_mayor_30d universo_completo   226.8300  29  1.49e-32    0.0961 nulo/insignificante       24557                   0.2000
          competencia_cat             indice_alcance universo_completo   854.5400   8 3.60e-179    0.0941 nulo/insignificante       48293                 739.4000
          competencia_cat             indice_alcance        observable   338.8100   8  2.21e-68    0.0940 nulo/insignificante       19177                 548.6000
                    orden             indice_alcance universo_completo   833.2800   4 4.74e-179    0.0928 nulo/insignificante       48331                  68.2000
        prov_tipo_empresa             indice_alcance universo_completo   373.8600  58  1.03e-47    0.0763 nulo/insignificante       32126                   0.1000
                    orden retraso_material_mayor_30d        observable    38.1000   2  5.34e-09    0.0483 nulo/insignificante       16326                  92.5000
                  es_pyme             indice_alcance universo_completo    84.1000   2  5.46e-19    0.0417 nulo/insignificante       48331               2,195.8000
     entidad_centralizada retraso_material_mayor_30d       
[...salida truncada en el documento; completa en el .ipynb...]
```

### Celda `c010`

```
       id notebook celda                                           hallazgo                                          evidencia  \
0  H09-01       09  c008  La variable categorica con mayor asociacion al...  V de Cramer = 0.351, N efectivo = 16,326, mode...   
1  H09-02       09  c004  Todas las variables continuas del analisis pre...                  14 de 16 variables con |skew| > 1   
2  H09-03       09  c007  Frente a los tres indicadores de la restriccio...  maximo |rho| anticipatorio: valor_del_contrato...   
3  H09-04       09  c010  Las variables con mayor asociacion al desempen...  Tabla de variables candidatas con su momento d...   
4  H09-05       09  c005  El sobrecosto sobre el precio base se comporta...  Fila correspondiente en la matriz de Spearman ...   

                         etiquetas  valor                                               nota  
0  [B-OE2] [B-OE3-insumo] [A-OE04]   Alto  Extiende a 11 variables la matriz de dos tabla...  
1                         [A-OE03]  Medio  El criterio de eleccion de la prueba queda doc...  
2           [B-OE2] [B-OE3-insumo]   Alto  Resultado honesto: las asociaciones anticipato...  
3         [B-OE3-insumo] [CALIDAD]   Alto  Distincion imprescindible antes de usar cualqu...  
4                 [A-OE03] [B-OE2]   Alto  Confirma que la redefinicion del notebook 05 a...
```

### Celda `c005`

```
Figura persistida: 09_matriz_spearman_extendida.png
```
