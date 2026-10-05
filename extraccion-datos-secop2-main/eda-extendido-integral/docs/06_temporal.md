# 06 — Evolucion temporal de la contratacion y estabilidad de los indicadores

**Proposito.** Cerrar la brecha 4 del documento comparativo: el filtro 2018-2024 se aplico sin ninguna
figura que mostrara la distribucion de la muestra por anio. Este cuaderno responde tres preguntas que un
jurado formulara: cuantos contratos aporta cada anio, si el corte de 2024 trunca contratos largos, y si
los indicadores de desempeno son estables en el tiempo o si el resultado global esta dominado por un
periodo concreto.

**Insumo.** `data/universo_extendido.parquet` (notebook 01).

**Etiquetas de objetivo que atiende:** `[A-OE04]` (visualizacion y segmentacion temporal),
`[A-OE03]` (validez del criterio temporal de inclusion), `[B-OE2]` (caracterizacion del comportamiento
historico, que es literalmente el enunciado del objetivo), `[CALIDAD]`.

> Documento generado automaticamente a partir de `notebooks/06_temporal.ipynb` ya ejecutado, por `build/gen_docs.py`. No editar a mano.

---

## 1. Distribucion anual y efecto del criterio temporal de inclusion

## 2. Truncamiento del corte de 2024

Un contrato firmado a finales de 2024 con plazo largo no puede haber terminado. Si el filtro de
observabilidad retiene sistematicamente los contratos cortos de los ultimos anios, el subconjunto
observable esta sesgado hacia contratos de menor duracion en esos anios, y el indicador de tiempo lo
refleja. Se cuantifica.

## 3. Estabilidad de los indicadores de desempeno en el tiempo

## 4. Estacionalidad mensual de la firma de contratos

## 5. Momento de las modificaciones dentro del contrato

## 6. Sintesis de hallazgos etiquetados

## Sintesis del notebook 06

| ID | Hallazgo | Etiquetas |
|---|---|---|
| H06-01 | El criterio 2018-2024 excluye mayoritariamente contratacion posterior a 2024, no historia antigua | `[A-OE03]` `[CALIDAD]` `[B-OE2]` |
| H06-02 | La retencion del filtro de observabilidad cae en los anios recientes: efecto de truncamiento | `[A-OE03]` `[CALIDAD]` |
| H06-03 | Los indicadores de desempeno no son estables entre anios | `[A-OE04]` `[B-OE2]` `[B-OE3-insumo]` |
| H06-04 | La firma se concentra en el ultimo trimestre del anio | `[A-OE04]` `[B-OE2]` |
| H06-05 | La primera modificacion aparece cerca del final del plazo vigente | `[B-OE2]` `[B-OE3-insumo]` |

**Productos persistidos:** `data/indicadores_por_anio.csv`, `figuras/06_distribucion_anual.png`,
`figuras/06_estabilidad_indicadores.png`, `figuras/06_estacionalidad_mensual.png`.

---

## Figuras producidas por este cuaderno

- `figuras/06_distribucion_anual.png`
- `figuras/06_estabilidad_indicadores.png`
- `figuras/06_estacionalidad_mensual.png`

---

## Hallazgos etiquetados de este cuaderno

| ID | Celda | Hallazgo | Etiquetas | Evidencia | Valor |
|---|---|---|---|---|---|
| H06-01 | `c004` | El criterio temporal 2018-2024 excluye mayoritariamente contratacion POSTERIOR a 2024, no historia antigua | [A-OE03] [CALIDAD] [B-OE2] | 10,762 contratos posteriores a 2024 frente a 244 anteriores a 2018 | Alto |
| H06-02 | `c004` | La retencion del filtro de observabilidad cae fuertemente en los anios recientes | [A-OE03] [CALIDAD] | Columna retencion_pct de la tabla anual | Alto |
| H06-03 | `c007` | Los indicadores de desempeno NO son estables en el tiempo: el retraso material y la no entrega varian entre anios de forma significativa | [A-OE04] [B-OE2] [B-OE3-insumo] | Kruskal-Wallis entre anios con epsilon2 reportado sobre el subconjunto observable | Alto |
| H06-04 | `c009` | La firma de contratos de obra esta concentrada en el ultimo trimestre del anio | [A-OE04] [B-OE2] | Tabla de estacionalidad mensual sobre 2018-2024 | Medio |
| H06-05 | `c011` | La primera modificacion contractual aparece tipicamente cerca del final del plazo vigente | [B-OE2] [B-OE3-insumo] | Mediana de la fraccion del plazo transcurrida hasta la primera modificacion, en doble lectura | Medio |

---

## Apendice: salida literal de las celdas citadas como evidencia

Cada bloque reproduce la salida de la celda cuyo `execution_count` coincide con la referencia `cNNN` de la tabla anterior, tal como quedo persistida en el `.ipynb` ejecutado.

### Celda `c004`

```
Figura persistida: 06_distribucion_anual.png
```

### Celda `c007`

```
Figura persistida: 06_estabilidad_indicadores.png
```

### Celda `c009`

```
Figura persistida: 06_estacionalidad_mensual.png
```

### Celda `c011`

```
       id notebook celda                                           hallazgo                                          evidencia  \
0  H06-01       06  c004  El criterio temporal 2018-2024 excluye mayorit...  10,762 contratos posteriores a 2024 frente a 2...   
1  H06-02       06  c004  La retencion del filtro de observabilidad cae ...            Columna retencion_pct de la tabla anual   
2  H06-03       06  c007  Los indicadores de desempeno NO son estables e...  Kruskal-Wallis entre anios con epsilon2 report...   
3  H06-04       06  c009  La firma de contratos de obra esta concentrada...    Tabla de estacionalidad mensual sobre 2018-2024   
4  H06-05       06  c011  La primera modificacion contractual aparece ti...  Mediana de la fraccion del plazo transcurrida ...   

                         etiquetas  valor                                               nota  
0       [A-OE03] [CALIDAD] [B-OE2]   Alto  Responde a la objecion de que el filtro 'desca...  
1               [A-OE03] [CALIDAD]   Alto  Es el efecto de truncamiento esperado y debe d...  
2  [A-OE04] [B-OE2] [B-OE3-insumo]   Alto  El anio de firma es una variable con asociacio...  
3                 [A-OE04] [B-OE2]  Medio  Patron de ejecucion presupuestal de fin de vig...  
4           [B-OE2] [B-OE3-insumo]  Medio  Recupera un analisis del pipeline compartido c...
```
