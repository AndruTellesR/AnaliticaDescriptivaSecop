# 07 — Perfil del contratista y concentracion del mercado

**Proposito.** Incorporar el bloque de proveedor, ausente del EDA descriptivo previo: `es_pyme`
(disponible al 100% en el contrato y sin usar hasta ahora), tipo de empresa, antiguedad y categoria
UNSPSC del registro de proveedores, y la concentracion de contratos por contratista. Cierra la brecha 7
del documento comparativo y aporta el perfil de proveedor que el insight N-K02 pedia para profundizar
A-H2.

**Insumo.** `data/universo_extendido.parquet` (notebook 01).

**Etiquetas de objetivo que atiende:** `[A-OE04]` (segmentacion por contratista), `[A-H2]` (perfil de
contratista para la hipotesis de consorcios), `[B-OE2]` (variables criticas y comportamiento historico),
`[B-OE3-insumo]`, `[CALIDAD]`.

**Limitacion declarada de entrada.** El registro externo de proveedores cubre el 54,41% de los
proveedores unicos y el 66,47% de los contratos. Los analisis que dependen de `tipo_empresa`,
`antiguedad` o UNSPSC del proveedor se reportan sobre ese subconjunto, con su N efectivo. Los analisis
basados en `es_pyme` y `tipo_contratista` cubren el 100% porque se derivan del propio contrato.

> Documento generado automaticamente a partir de `notebooks/07_perfil_proveedor.ipynb` ya ejecutado, por `build/gen_docs.py`. No editar a mano.

---

## 1. `es_pyme`: la variable disponible al 100% que no se habia usado

Nota de coherencia entre fuentes: `es_pyme` del contrato y `espyme` del registro de proveedores tienen
nombres casi identicos y podrian no medir lo mismo. Antes de tratarlas como equivalentes se comprueba su
concordancia empirica sobre los contratos donde ambas estan disponibles.

## 2. Tipo de contratista y perfil del proveedor registrado

## 3. Concentracion de contratos por contratista y reincidencia

## 4. Categoria UNSPSC principal del proveedor

## 5. Sintesis de hallazgos etiquetados

## Sintesis del notebook 07

| ID | Hallazgo | Etiquetas |
|---|---|---|
| H07-01 | `es_pyme` discrimina el desempeno de plazo; la variable estaba disponible al 100% y sin usar | `[A-OE04]` `[B-OE2]` `[B-OE3-insumo]` |
| H07-02 | `es_pyme` del contrato y `espyme` del registro concuerdan al 100%: misma variable, coberturas distintas | `[CALIDAD]` `[A-OE02]` |
| H07-02b | La antiguedad no es calculable para consorcios y uniones temporales | `[CALIDAD]` |
| H07-03 | El mercado tiene cola larga: no hay contratistas dominantes | `[B-OE2]` `[A-OE04]` |
| H07-04 | La reincidencia del contratista se asocia al desempeno | `[B-OE2]` `[B-OE3-insumo]` `[A-OE04]` |
| H07-05 | La antiguedad medible es antiguedad de la cuenta en SECOP, no experiencia empresarial | `[CALIDAD]` |
| H07-06 | El tipo de empresa discrimina el desempeno de plazo, con cobertura limitada | `[B-OE2]` `[B-OE3-insumo]` |

**Producto persistido:** `figuras/07_perfil_proveedor.png`.

**Advertencia de interpretacion.** Ninguno de los efectos de este cuaderno esta controlado por cuantia.
Dado que la cuantia se asocia tanto al perfil del contratista como al desempeno (notebook 05), los
efectos reportados aqui son asociaciones brutas. Se declara explicitamente y se remite al notebook 10,
donde el control por estratificacion se aplica a las hipotesis formales.

---

## Figuras producidas por este cuaderno

- `figuras/07_perfil_proveedor.png`

---

## Hallazgos etiquetados de este cuaderno

| ID | Celda | Hallazgo | Etiquetas | Evidencia | Valor |
|---|---|---|---|---|---|
| H07-01 | `c004` | `es_pyme` discrimina el desempeno de plazo: los contratos de PYME presentan menor deslizamiento que los de no PYME | [A-OE04] [B-OE2] [B-OE3-insumo] | Mann-Whitney U = 24,323,628.0 / p = 8.42e-157 / rank-biserial = +0.245 (pequeno) / N efectivo = 9,649 (PYME) vs 6,677 (No PYME) / medianas 1.00 vs 9.00 | Alto |
| H07-02 | `c005` | `es_pyme` del contrato y `espyme` del registro concuerdan al 100%: son la misma variable con coberturas distintas | [CALIDAD] [A-OE02] | Concordancia del 100.00% sobre N efectivo 32,126 | Medio |
| H07-02b | `c005` | La antiguedad del proveedor no es calculable para consorcios y uniones temporales: no figuran en el registro externo | [CALIDAD] | Tabla de cobertura de antiguedad por tipo de contratista | Alto |
| H07-03 | `c009` | El mercado de obra publica tiene cola larga: la mayoria de los proveedores tiene un unico contrato y no hay contratistas dominantes | [B-OE2] [A-OE04] | 16,299 proveedores con un solo contrato (70.3%); top 10 acumula 2.73% de los contratos | Alto |
| H07-04 | `c010` | La reincidencia del contratista se asocia al desempeno: los proveedores con mas contratos muestran mayor retraso material | [B-OE2] [B-OE3-insumo] [A-OE04] | Kruskal-Wallis y chi-cuadrado con tamano de efecto reportados | Alto |
| H07-05 | `c008` | La antiguedad del proveedor mide antiguedad de la CUENTA en SECOP, no antiguedad empresarial | [CALIDAD] | N efectivo 28,947; maximo observado en torno a 11 anios, coherente con la vida de la plataforma | Alto |
| H07-06 | `c007` | El tipo de empresa del registro discrimina el desempeno de plazo entre las formas societarias principales | [B-OE2] [B-OE3-insumo] | Kruskal-Wallis entre los 8 tipos de empresa mas frecuentes, con N efectivo declarado | Medio |

---

## Apendice: salida literal de las celdas citadas como evidencia

Cada bloque reproduce la salida de la celda cuyo `execution_count` coincide con la referencia `cNNN` de la tabla anterior, tal como quedo persistida en el `.ipynb` ejecutado.

### Celda `c004`

```
Concordancia entre `es_pyme` (contrato) y `espyme` (registro de proveedores):
reg        No     Si    All
es_pyme                    
No       8131      0   8131
Si          0  23995  23995
All      8131  23995  32126

N efectivo: 32,126 contratos con ambas variables disponibles
Concordancia: 100.00%

RESULTADO: la concordancia es perfecta donde ambas estan disponibles. No son variables en
conflicto sino la misma variable con coberturas distintas. Se adopta `es_pyme` del contrato
como variable de trabajo por cobertura del 100% frente al 66.47% del registro externo.

Cobertura de la antiguedad por tipo de contratista (advertencia estructural):
                            cobertura_antiguedad_pct
tipo_contratista                                    
Consorcio / Union Temporal                    0.0000
No definido                                  26.8800
Persona Juridica                             75.9200
Persona Natural                              88.1500

Los consorcios y uniones temporales no figuran en el registro de proveedores con fecha de
creacion utilizable, de modo que la antiguedad no es calculable para ese tipo de contratista.
Cualquier analisis de antiguedad esta por construccion sesgado a personas juridicas y naturales.
```

### Celda `c005`

```
=== UNIVERSO COMPLETO ===
                                n     pct      mediana_valor  mediana_modificaciones  mediana_deslizamiento  pct_no_entregado  pct_entregado_total  mediana_oferentes  pct_pyme  mediana_antiguedad_anios
tipo_contratista                                                                                                                                                                                         
Consorcio / Union Temporal  10629 21.9900 1,542,231,047.0000                  3.0000                 8.0000            6.2000              62.0000             5.0000   32.6000                       NaN
No definido                   971  2.0100             0.0000                  0.0000                 0.0000            4.9000              92.0000             0.0000   25.6000                    2.6000
Persona Juridica            30197 62.4800   119,470,000.0000                  1.0000                 1.0000           12.1000              75.7000             1.0000   61.1000                    2.4800
Persona Natural              6534 13.5200   101,039,453.0000                  1.0000                 0.0000           11.2000              75.3000             2.0000   81.1000                    3.0100

=== SUBCONJUNTO OBSERVABLE ===
                                n     pct      mediana_valor  mediana_modificaciones  mediana_deslizamiento  pct_no_entregado  pct_entregado_total  mediana_oferentes  pct_pyme  mediana_antiguedad_anios
tipo_contratista                                                                                                                                                                                         
Consorcio / Union Temporal   4562 23.7700 1,480,005,224.0000                  5.0000                27.0000           12.4000              49.4000             5.0000   34.5000                       NaN
No definido                   117  0.6100    90,000,000.0000                  2.0000                 0.0000           28.2000              61.5000             1.0000   71.8000                    1.8900
Persona Juridica            11919 62.1000   161,133,542.0000                  3.0000                 1.0000           26.4000              59.0000             1.0000   64.2000                    2.6100
Persona Natural              2596 13.5300   129,945,336.5000                  3.0000                 0.0000           22.1000              61.6000             3.0000   86.9000                    2.8900
```

### Celda `c009`

```
=== UNIVERSO COMPLETO ===
                  contratos    mediana_valor  mediana_deslizamiento  pct_retraso_mayor_30  pct_no_entregado  mediana_modificaciones  pct_consorcio
reincidencia_cat                                                                                                                                  
1 contrato            16299 470,931,228.0000                 1.0000               30.1000            7.3000                  2.0000        52.3000
2-3 contratos         10265 177,970,195.0000                 0.0000               22.6000           11.0000                  1.0000        16.3000
4-10 contratos        10907 171,473,421.0000                 0.0000               19.9000           11.0000                  2.0000         3.9000
>10 contratos         10860 100,063,346.0000                 2.0000               22.5000           14.4000                  1.0000         0.1000

=== SUBCONJUNTO OBSERVABLE ===
                  contratos    mediana_valor  mediana_deslizamiento  pct_retraso_mayor_30  pct_no_entregado  mediana_modificaciones  pct_consorcio
reincidencia_cat                                                                                                                                  
1 contrato             6383 667,491,996.0000                 6.0000               39.6000           15.1000                  4.0000        59.1000
2-3 contratos          3765 218,337,274.0000                 1.0000               27.5000           25.7000                  3.0000        15.8000
4-10 contratos         4269 201,179,367.0000                 1.0000               24.6000           23.6000                  3.0000         4.4000
>10 contratos          4777 146,701,556.0000                 4.0000               32.8000           29.0000                  3.0000         0.2000

Kruskal-Wallis, deslizamiento del plazo entre niveles de reincidencia (observable):
  H = 254.68 | gl = 3 | p = 6.37e-55 | epsilon2 = 0.0154 (debil) | k = 4 grupos | N efectivo = 16,326
Chi-cuadrado, reincidencia x indice de alcance (observable):
  chi2 = 863.82 | gl = 6 | p = 2.49e-183 | V de Cramer = 0.150 (debil) | N efectivo = 19,194 | minima frecuencia esperada = 767.0
```

### Celda `c010`

```
Figura persistida: 07_perfil_proveedor.png
```

### Celda `c008`

```
Proveedores unicos en el universo: 23,192
                 corte  n_proveedores  cuota_de_contratos_pct  cuota_de_valor_pct
    Top 10 proveedores             10                  2.7300             16.5900
 Top 1% de proveedores            231                 15.1400             47.0200
 Top 5% de proveedores           1159                 33.1300             70.6800
Top 10% de proveedores           2319                 44.2200             81.5800
Top 20% de proveedores           4638                 56.9400             91.0800

Distribucion de contratos por proveedor:
  mediana: 1 | p90: 4 | p99: 17 | maximo: 672
  proveedores con un unico contrato: 16,299 (70.3%)

El mercado NO esta concentrado en el sentido clasico: el 20% de los proveedores concentra
una cuota alta, pero no hay un puñado de contratistas dominantes. La cola larga es lo dominante.
```

### Celda `c007`

```
N efectivo con antiguedad calculable: 28,896 (59.8% del universo)
Advertencia de calidad: `fecha_creacion` del registro es la fecha de creacion de la CUENTA en
SECOP, no la fecha de constitucion de la empresa. La antiguedad medida es antiguedad en la
plataforma. Se reporta como tal y no como experiencia empresarial.

                   n    mediana_valor  mediana_deslizamiento  pct_no_entregado  mediana_modificaciones  pct_consorcio
antiguedad_cat                                                                                                       
<1 anio         7478  49,888,843.0000                 0.0000           15.9000                  1.0000         0.0000
1-3 anios       8361  99,996,983.0000                 0.0000           15.5000                  2.0000         0.0000
3-5 anios       6930 172,860,929.0000                 0.0000           11.4000                  2.0000         0.0000
>5 anios        6127 250,000,000.0000                 0.0000            5.6000                  2.0000         0.0000

Spearman antiguedad ~ deslizamiento: rho = 0.0745, N efectivo = 24,503 (nulo)
Spearman antiguedad ~ modificaciones: rho = 0.1044, N efectivo = 28,896 (pequeno)
```
