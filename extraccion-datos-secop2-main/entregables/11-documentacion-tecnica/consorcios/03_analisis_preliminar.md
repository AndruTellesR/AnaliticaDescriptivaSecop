# Documento 03 — Análisis preliminar

**Notebook**: `notebooks/03_analisis_preliminar.ipynb`
**Inputs**: `consorcios_base.parquet`, `consorcios_imputado.parquet`
**Outputs**: 6 figuras + 4 CSVs en `data/`

## Pregunta del director

> A partir de la información de departamento y municipio de la entidad
> que abre el proceso, validar cuáles serían los indicadores financieros
> mínimos exigidos por tipo de contrato, y la probabilidad de éxito de
> un consorcio que los cumple.

El análisis se estructura en cinco frentes: distribución de los
indicadores extraídos, correlación con los targets, perfil por modalidad
de contratación, perfil por departamento, e importancia mutua (MI) sobre
el dataset imputado.

## 1. Distribución de los indicadores `pliego_*`

Subset: 3.877 consorcios con pliego extraído (36,5 %).

Las distribuciones son altamente sesgadas, incluso después de la
winsorización p1–p99 aplicada en el notebook 02. Las medianas indican
los umbrales típicos exigidos en los pliegos:

| Indicador | Mediana exigida (aprox.) |
|-----------|--------------------------|
| `liquidez_min` | ~1,5 |
| `endeudamiento_max_pct` | ~60 % |
| `cobertura_intereses_min` | ~3 |
| `rentabilidad_activo_min_pct` | ~3 % |
| `rentabilidad_patrimonio_min_pct` | ~5 % |
| `capital_trabajo_min_pct_presupuesto` | ~30 % |

Figura: `dia_03_distribucion_pliego.png`.

## 2. Correlación `pliego_*` ↔ targets

| Indicador | r vs atraso | r vs sobrecosto |
|-----------|-------------|-----------------|
| capital_trabajo_min_pct_presupuesto | 0,033 | 0,016 |
| cobertura_intereses_min | 0,036 | 0,012 |
| endeudamiento_max_pct | −0,013 | −0,032 |
| liquidez_min | 0,017 | 0,041 |
| rentabilidad_activo_min_pct | 0,029 | −0,008 |
| rentabilidad_patrimonio_min_pct | 0,034 | 0,000 |

**Todas las correlaciones lineales son menores a 0,05 en valor absoluto.**
Los umbrales exigidos por el pliego no discriminan de manera lineal el
resultado final del contrato. Tres lecturas posibles:

1. **Validación de un sistema funcional**: si el pliego efectivamente
   filtra a los proponentes incapaces, todos los que llegan a firmar
   contrato ya cumplen un mínimo común, comprimiendo la varianza relevante.
2. **Heterogeneidad del cumplimiento**: el valor mínimo exigido por el
   pliego no se observa en el dataset; solo se sabe que el adjudicatario
   lo cumple "al menos hasta" ese umbral. La señal verdadera es la
   diferencia entre lo exigido y lo aportado, que no está disponible.
3. **Otras dimensiones dominan**: variables como duración, valor y
   contexto geográfico tienen más peso que el filtro financiero.

Figura: `dia_03_corr_pliego_target.png`.

## 3. Indicadores típicos por modalidad

Top 5 modalidades en consorcios y mediana del indicador en sus pliegos
(`data/03_indicadores_por_modalidad.csv`). Permite responder
operativamente: «¿qué nivel de capacidad financiera debe demostrar un
consorcio para competir bajo modalidad X?».

La modalidad **Licitación pública Obra Pública** concentra los pliegos
con umbrales más estrictos en liquidez y cobertura de intereses. Las
modalidades de menor cuantía (Selección abreviada, Mínima cuantía)
exigen umbrales notablemente más laxos.

## 4. Tasas de éxito por modalidad

Tasa observada de atraso y sobrecosto en los 8 modalidades con más
contratos de consorcio:

| Modalidad | n | atraso | sobrecosto |
|-----------|---|--------|------------|
| Licitación pública Obra Pública | ~5.700 | ~0,46 | ~0,82 |
| Selección abreviada Obra | ~2.100 | ~0,42 | ~0,77 |
| Concurso de méritos | ~1.200 | ~0,38 | ~0,68 |
| Contratación directa | ~600 | ~0,33 | ~0,55 |

La tasa de sobrecosto se mueve más entre modalidades que la de atraso.
La modalidad Licitación pública concentra el mayor riesgo en ambas
dimensiones, mientras que las contrataciones directas son
significativamente menos riesgosas.

Figura: `dia_03_tasas_por_modalidad.png`.

## 5. Capacidad por departamento

Top 15 departamentos por número de contratos de consorcio
(`data/03_capacidad_por_depto.csv`):

| Departamento | n | atraso | sobrecosto | valor mediano |
|--------------|---|--------|------------|----------------|
| Bogotá D.C. | 3.585 | 0,42 | 0,76 | $2,24 B |
| Valle del Cauca | 751 | 0,40 | 0,75 | $1,12 B |
| Cundinamarca | 529 | 0,38 | 0,85 | $878 M |
| Antioquia | 517 | 0,43 | 0,77 | $3,00 B |
| Santander | 410 | 0,48 | 0,64 | $1,66 B |
| Tolima | 363 | 0,49 | 0,83 | $1,12 B |
| Bolívar | 361 | 0,48 | 0,75 | $2,20 B |
| Caldas | 337 | **0,29** | 0,81 | $852 M |
| Boyacá | 333 | 0,44 | 0,78 | $519 M |
| Norte de Santander | 303 | 0,52 | 0,76 | $808 M |
| Huila | 296 | **0,58** | 0,74 | $955 M |
| Meta | 273 | 0,39 | 0,79 | $1,62 B |
| Cesar | 267 | 0,45 | 0,79 | $1,80 B |
| Atlántico | 258 | 0,47 | 0,77 | $3,28 B |
| No Definido | 224 | 0,70 | 0,85 | $1,77 B |

Lecturas:

- **Caldas** tiene la menor tasa de atraso (28,8 %).
- **Huila** tiene la mayor tasa de atraso (58,4 %) entre departamentos
  con n suficiente, casi al doble de Caldas.
- Los contratos con `departamento = "No Definido"` son atípicamente
  riesgosos (70 % atraso). Este es un sentinela del dataset y conviene
  tratarlo como categoría informativa, no como dato faltante.
- El valor mediano del contrato varía un orden de magnitud entre
  departamentos (de $519 M en Boyacá a $3,28 B en Atlántico), pero el
  riesgo no escala monotónicamente con el valor.

Figura: `dia_03_riesgo_por_depto.png`.

## 6. Cruce departamento × modalidad

Heatmap (`dia_03_heatmap_atraso.png`) sobre los 10 deptos × 4 modalidades
con mayor frecuencia. La interacción entre geografía y modalidad concentra
celdas de alto riesgo (>0,55) y celdas de bajo riesgo (<0,35), lo que
justifica que el modelo trate ambas variables como predictores
independientes y permita capturar la interacción mediante árboles.

## 7. Valor del contrato vs riesgo

Por cuartiles de `valor_del_contrato`:

| Cuartil | Valor mediano | atraso | sobrecosto |
|---------|---------------|--------|------------|
| Q1 (bajo) | ~95 M | ~0,38 | ~0,72 |
| Q2 | ~480 M | ~0,42 | ~0,77 |
| Q3 | ~1,5 B | ~0,47 | ~0,80 |
| Q4 (alto) | ~5 B | ~0,49 | ~0,83 |

La relación es monotónica creciente: los contratos más grandes son más
riesgosos en ambas dimensiones. Esto refuerza el uso de `valor_del_contrato`
como predictor (y no solo como variable de exposición).

Figura: `dia_03_valor_vs_riesgo.png`.

## 8. Mutual Information — top 20 features

Sobre el dataset imputado (79 features). MI no asume linealidad y permite
identificar qué variables contienen información discriminativa para los
targets.

| Posición | Feature | MI atraso | MI sobrecosto |
|---|---|---|---|
| 1 | **`duracion_planificada_dias`** | **0,214** | 0,044 |
| 2 | `duracion_planificada_dias_was_nan` | 0,102 | 0,033 |
| 3 | `valor_del_contrato` | 0,039 | 0,011 |
| 4 | `ciudad_freq` | 0,025 | 0,018 |
| 5 | `condiciones_de_entrega_No Definido` | 0,020 | 0,012 |
| 6 | `presupuesto_general_de_la_nacion_pgn_freq` | 0,015 | 0,007 |
| 7 | `el_contrato_puede_ser_prorrogado_Si` | 0,012 | 0,009 |
| 8 | `departamento_freq` | 0,014 | 0,006 |
| 9 | `obligaci_n_ambiental_No` | 0,013 | 0,004 |
| 10 | `entidad_centralizada_Centralizada` | 0,008 | 0,009 |

**Hallazgos relevantes**:

1. `duracion_planificada_dias` es **cinco veces más informativa** que la
   segunda variable. El hecho de que su flag `_was_nan` también esté en
   el top 2 sugiere que tanto la duración planificada como la ausencia
   de información sobre ella son señales fuertes del comportamiento del
   contrato.
2. `valor_del_contrato`, `ciudad_freq` y `departamento_freq` confirman la
   importancia del contexto geográfico y de exposición.
3. **Ningún indicador `pliego_*` está en el top 20**. Los más altos son
   los flags `pliego_*_was_nan` (MI ≤ 0,015), confirmando que la
   presencia del dato pesa más que su valor.
4. Variables categóricas codificadas como OHE aparecen distribuidas en
   el top, lo que justifica mantener el encoding tal cual.

Figura: `dia_03_mi_top20.png`.

## Implicaciones para el modelado (notebooks 04–11)

1. **Variable más importante**: `duracion_planificada_dias` debe estar
   siempre presente. Modelos que la imputen mal degradarán fuerte.
2. **Flags `_was_nan`**: aportan señal, validando la elección de la
   estrategia de imputación por mediana.
3. **Geografía como predictor**: `departamento_freq` y `ciudad_freq`
   capturan diferencias regionales. Mantener en todos los modelos.
4. **Indicadores `pliego_*`**: aportan poco como variables continuas
   pero sus flags de ausencia sí aportan. La decisión de mantenerlos
   en el set de features es defendible por interpretabilidad y por
   completar la trazabilidad académica, aun cuando su impacto sea bajo.
5. **Modalidad**: las categóricas OHE de modalidad están presentes en
   top, así que se mantienen. No reducir a `modalidad_freq`.

## Próximo paso

Notebook 04 — primer modelo del zoológico: Logistic Regression con
`RandomizedSearchCV` siguiendo `pasos.md`.
