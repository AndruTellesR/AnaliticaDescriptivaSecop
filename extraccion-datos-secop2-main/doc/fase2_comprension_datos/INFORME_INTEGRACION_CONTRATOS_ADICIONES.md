# Informe: Integración Contratos + Adiciones
## Comportamiento de los contratos de Obra Pública en SECOP II

> **Notebook**: `05_integracion_contratos_adiciones.ipynb`
> **Fecha**: 2026-03-04
> **Base**: 48,331 contratos únicos de Obra (deduplicados)
> **Tabla generada**: `data/contratos_adiciones_obra.parquet` (111 columnas)

---

## 1. Panorama general

Tras deduplicar contratos (3,022 eliminados) y adiciones (96,942 filas idénticas eliminadas),
se realizó un LEFT JOIN entre la fuente madre y las adiciones agregadas a nivel contrato.

| Indicador | Valor | % |
|---|---|---|
| Contratos únicos de Obra | 48,331 | 100% |
| Con al menos una modificación | 33,465 | 69.2% |
| Con extensión de plazo (días adicionados > 0) | 10,699 | 22.1% |
| Con adición en valor ($) | 4,465 | 9.2% |
| Con suspensión | 8,275 | 17.1% |
| Con conclusión formal | 5,087 | 10.5% |
| Con cesión (cambio de contratista) | 496 | 1.0% |
| Sin ninguna modificación | 14,866 | 30.8% |

**Hallazgo principal**: Casi 7 de cada 10 contratos de Obra sufren algún tipo de modificación
durante su ejecución. Las extensiones de plazo son las más frecuentes (22.1%), seguidas de
suspensiones (17.1%) y conclusiones (10.5%). Las adiciones en valor (9.2%) son menos frecuentes
de lo esperado.

---

## 2. Extensiones de plazo (días adicionados)

### 2.1 Distribución

De los 10,699 contratos con extensión:

| Estadística | Días |
|---|---|
| Media | 77.6 |
| Mediana | 46 |
| P25 | 25 |
| P75 | 91 |
| P90 | 181 |
| P95 | 264 |
| P99 | 367 |
| Máximo | 2,934 (~8 años) |

La distribución es fuertemente sesgada a la derecha: la mayoría de extensiones son
de 1-3 meses, pero hay una cola larga con extensiones extremas.

### 2.2 Ratio extensión / duración planificada

La duración planificada mediana es de **115 días**. Entre los contratos con extensión,
la extensión representa en promedio un **10% de la duración original**. Sin embargo,
hay contratos donde la extensión supera la duración original.

Correlación entre duración planificada y días adicionados: **0.521** (moderada-positiva).
Los contratos más largos tienden a recibir más días adicionales.

### 2.3 Extensiones por modalidad de contratación

| Modalidad | Contratos | % con extensión |
|---|---|---|
| Licitación pública Obra Pública | 8,575 | **33.5%** |
| Selección Abreviada Menor Cuantía (sin manif.) | 297 | 29.3% |
| Contratación directa | 9,981 | 23.6% |
| Selección Abreviada de Menor Cuantía | 12,932 | 23.4% |
| Contratación Directa (con ofertas) | 1,541 | 21.1% |
| Régimen especial (con ofertas) | 1,932 | 21.1% |
| Régimen especial | 2,905 | 19.4% |
| Licitación pública (genérica) | 421 | 18.5% |
| Mínima cuantía | 9,747 | 12.1% |

**Hallazgo**: La **Licitación pública de Obra Pública** tiene la tasa más alta de extensiones
(33.5%), casi 3 veces más que Mínima cuantía (12.1%). Esto sugiere que los contratos de
mayor complejidad y envergadura (que usan licitación) son más propensos a atrasos.

### 2.4 Extensiones por estado del contrato

| Estado | Contratos | % extensión | % adición valor | % suspensión |
|---|---|---|---|---|
| **Modificado** | 15,248 | **68.4%** | 14.2% | 27.9% |
| Terminado | 11,259 | 0.4% | 13.9% | 19.9% |
| En ejecución | 9,805 | 0.1% | 1.4% | 9.9% |
| Cerrado | 3,072 | 0.2% | 15.9% | 6.2% |
| Suspendido | 1,181 | 16.7% | 3.7% | **44.6%** |
| Cancelado | 1,681 | 0.0% | 0.1% | 0.1% |

**Hallazgo clave**: Los contratos en estado "Modificado" concentran casi todas las extensiones
(68.4%). Los contratos terminados o cerrados reportan ~0% de extensiones, lo cual tiene sentido
porque la extensión ocurre durante la ejecución, no después. Los contratos "Suspendidos"
tienen alta tasa de suspensión (44.6%) como era esperado.

---

## 3. Adiciones en valor (dinero)

### 3.1 Distribución

- **4,465 contratos** (9.2%) recibieron al menos una adición en valor
- La mayoría (81.6%) recibieron solo 1 adición; 14% recibieron 2; el resto hasta 10

### 3.2 Relación con el valor del contrato

| Segmento | Mediana valor contrato (COP) |
|---|---|
| Sin adición en valor | $199,921,893 |
| **Con adición en valor** | **$345,000,000** |
| Sin extensión | $157,925,189 |
| **Con extensión** | **$521,940,758** |

**Hallazgo**: Los contratos que reciben adiciones en valor o extensiones tienden a ser
significativamente más grandes. Los contratos con extensión tienen un valor mediano
**3.3x mayor** que los que no tienen extensión.

### 3.3 Sobrecostos (ratio valor pagado / valor contratado)

Solo 15,033 contratos (31%) tienen tanto valor contratado como valor pagado > 0.

| Categoría | Contratos | % |
|---|---|---|
| Sin sobrecosto (~0%) | 10,033 | 66.7% |
| Subejecutado leve (1-50% menos) | 3,561 | 23.7% |
| Subejecutado severo (>50% menos) | 1,433 | 9.5% |
| Sobrecosto leve (1-10%) | 4 | 0.0% |
| Sobrecosto moderado-alto | 2 | 0.0% |
| Sobrecosto extremo (>100%) | 0 | 0.0% |

**Hallazgo sorprendente**: Los sobrecostos son casi inexistentes en el dato crudo.
La gran mayoría de contratos o no tiene sobrecosto o está **sub-ejecutado** (se pagó menos
de lo contratado). Esto puede deberse a:
1. Las adiciones en valor actualizan el campo `valor_del_contrato`, ocultando el incremento real
2. Muchos contratos aún están en ejecución (67.5% tienen $0 pagado)
3. El valor pagado se registra gradualmente y aún no refleja el total final

**Conclusión**: El campo `sobrecosto_ratio` calculado desde `valor_pagado` / `valor_del_contrato`
**no es confiable como target**. El verdadero indicador de adición presupuestal es
`tiene_adicion_valor` (del dataset de adiciones).

---

## 4. Suspensiones y cesiones

### 4.1 Suspensiones vs extensiones

| | Sin extensión | Con extensión |
|---|---|---|
| Sin suspensión | 82.6% | 17.4% |
| **Con suspensión** | **55.1%** | **44.9%** |

**Hallazgo**: Los contratos suspendidos tienen **2.6x más probabilidad** de recibir
extensiones (44.9% vs 17.4%). La suspensión es un predictor fuerte de extensión.

### 4.2 Suspensiones vs adiciones en valor

| | Sin adición valor | Con adición valor |
|---|---|---|
| Sin suspensión | 91.3% | 8.7% |
| Con suspensión | 88.1% | 11.9% |

La relación suspensión → adición en valor es más débil, pero aún positiva.

### 4.3 Cesiones

Los 496 contratos con cesión (cambio de contratista) muestran tasas elevadas:
- 39.9% con extensión (vs 22.1% general)
- 13.9% con adición en valor (vs 9.2% general)

La cesión es un indicador de problemas contractuales.

---

## 5. Co-ocurrencia de modificaciones

### 5.1 Diversidad de tipos

De los 33,465 contratos con alguna modificación:

| Tipos distintos | Contratos |
|---|---|
| 1 tipo | 12,802 (38.3%) |
| 2 tipos | 9,615 (28.7%) |
| 3 tipos | 5,762 (17.2%) |
| 4 tipos | 4,245 (12.7%) |
| 5 tipos | 941 (2.8%) |
| 6-7 tipos | 100 (0.3%) |

**Hallazgo**: El 62% de los contratos modificados tienen 2 o más tipos distintos de
modificación. Las modificaciones tienden a acumularse: un contrato que ya fue modificado
una vez tiene alta probabilidad de recibir más modificaciones.

### 5.2 Correlaciones entre tipos

Las correlaciones más fuertes entre tipos de modificación (binarias):
- **Suspensión ↔ Extensión**: Correlación positiva fuerte (los contratos suspendidos luego reciben extensiones)
- **Adición valor ↔ Extensión**: Correlación positiva moderada
- **Cesión ↔ resto**: Correlaciones débiles (la cesión es un evento relativamente independiente)

---

## 6. Análisis temporal

### 6.1 Tiempo hasta primera modificación

De los contratos con fecha de primera adición y firma disponibles:

| Estadística | Días |
|---|---|
| Media | 199 |
| Mediana | 91 |
| P25 | 36 |
| P75 | 231 |

**Hallazgo**: La primera modificación ocurre en promedio a los **3 meses** de la firma.
El 25% de las modificaciones ocurren en el primer mes, lo que sugiere que algunos
problemas contractuales se manifiestan muy temprano.

---

## 7. Factores de riesgo: ¿qué contratos tienen más problemas?

### 7.1 Por rango de valor del contrato

| Rango (COP) | Contratos | % extensión | % adición valor | % suspensión | Días adic. media | Modif. media |
|---|---|---|---|---|---|---|
| <50M | 10,800 | 11.1% | 6.5% | 7.4% | 5.5 | 1.4 |
| 50M-200M | 12,743 | 17.7% | 8.6% | 10.1% | 11.2 | 1.9 |
| 200M-1B | 13,051 | 26.2% | 10.9% | 20.1% | 19.4 | 3.4 |
| 1B-10B | 8,818 | **33.8%** | 11.6% | **32.5%** | 30.7 | 5.9 |
| >10B | 2,223 | **37.3%** | 10.2% | **31.8%** | 44.8 | **7.4** |

**Hallazgo clave**: Existe una **relación monótona creciente** entre el valor del contrato
y la probabilidad de problemas. Los contratos de >10B tienen:
- 3.4x más extensiones que los de <50M
- 4.3x más suspensiones
- 8.2x más días adicionados en promedio
- 5.3x más modificaciones totales

El valor del contrato es un **predictor fuerte** de riesgo contractual.

### 7.2 Por duración planificada

| Duración | Contratos | % extensión | % adición valor | Días adic. media | Ratio ext/dur |
|---|---|---|---|---|---|
| <1 mes | 6,462 | 3.1% | 7.3% | 0.4 | 0.021 |
| 1-3 meses | 11,022 | 16.2% | 10.8% | 4.8 | 0.073 |
| 3-6 meses | 9,569 | **31.5%** | **12.4%** | 15.6 | 0.121 |
| 6-12 meses | 8,914 | 30.8% | 10.2% | 23.3 | 0.090 |
| 1-2 años | 4,082 | **47.2%** | 9.3% | 52.4 | 0.105 |
| >2 años | 1,983 | **51.2%** | **16.0%** | 102.4 | 0.100 |

**Hallazgo**: Los contratos más largos tienen **mucha** más probabilidad de extensión
(51.2% para >2 años vs 3.1% para <1 mes). La duración planificada es otro
**predictor fuerte**.

El ratio extensión/duración se estabiliza alrededor del **10%** para contratos de
3+ meses: independientemente de la duración, la extensión típica es ~10% del plazo
original.

### 7.3 Por geografía (departamento)

Los departamentos con mayor tasa de extensión (mínimo 50 contratos):

| Departamento | Contratos | % extensión |
|---|---|---|
| Sucre | 349 | 32.4% |
| Quindío | 573 | 32.1% |
| Magdalena | 648 | 29.9% |
| Risaralda | 855 | 29.4% |
| Bolívar | 1,254 | 28.3% |
| Caldas | 1,938 | 28.2% |
| Cundinamarca | 2,412 | 27.3% |
| Amazonas | 144 | 27.1% |
| Cauca | 1,328 | 26.9% |

Bogotá (14,338 contratos) tiene 23.6% de extensiones, cerca del promedio nacional.

---

## 8. Conclusiones principales

### 8.1 Sobre el comportamiento de los contratos

1. **Las modificaciones son la norma, no la excepción**: 69.2% de los contratos de Obra
   sufren alguna modificación. Solo 3 de cada 10 contratos se ejecutan sin cambios.

2. **Las extensiones son el problema más visible**: 22.1% de contratos reciben días
   adicionales, con una mediana de 46 días.

3. **El dinero y el tiempo están correlacionados con el riesgo**: Contratos más grandes
   y más largos tienen sistemáticamente más problemas.

4. **Las suspensiones son predictores fuertes de extensiones**: Un contrato suspendido
   tiene 2.6x más probabilidad de recibir extensión.

5. **Las adiciones en valor son relativamente infrecuentes** (9.2%), pero se concentran
   en contratos de mayor valor.

6. **El sobrecosto calculado (pagado vs contratado) no es confiable**: Probablemente
   porque el valor del contrato se actualiza con las adiciones, ocultando el delta real.

### 8.2 Para el modelo predictivo

**Targets viables**:
- `tiene_extension_dias` (22.1% positivo, ratio 1:3.5) — **TARGET PRINCIPAL**
- `tiene_adicion_valor` (9.2% positivo, ratio 1:10) — más desbalanceado
- `tiene_suspension` (17.1% positivo, ratio 1:5) — viable
- `tiene_modificacion` (69.2% positivo) — demasiado común, poco discriminante

**Predictores fuertes identificados**:
- `valor_del_contrato` — relación monótona con riesgo
- `duracion_planificada_dias` — relación monótona con extensiones
- `modalidad_de_contratacion` — Licitación pública = mayor riesgo
- `departamento` — variación geográfica significativa
- `estado_contrato` — los "Modificados" concentran las extensiones

**Variables nuevas generadas** (24 columnas):
- 8 conteos por tipo de modificación
- 2 totales (n_modificaciones_total, n_tipos_distintos)
- 2 fechas (primera/última adición)
- 6 targets binarios
- 4 features derivados (sobrecosto_ratio, duracion_planificada, ratio_extension, dias_hasta_primera_adicion)
- 2 auxiliares (ventana_adiciones, log_valor)

---

## 9. Siguiente paso

Este análisis confirma que el modelo predictivo es viable. Los siguientes pasos son:

1. **Integrar procesosDeContratacion** (features de competencia: proveedores invitados, oferentes)
2. **Integrar proveedoresRegistrados** (perfil del proveedor: pyme, tipo empresa, ubicación)
3. **Feature engineering final** (encoding de categóricas, imputación, escalado)
4. **Modelado** (clasificación binaria para `tiene_extension_dias`)
