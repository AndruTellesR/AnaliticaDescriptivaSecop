# Síntesis de hallazgos e insights — capítulo de resultados (OE-02 y OE-03)

**Alcance:** este documento consolida los notebooks 01 a 08 de `analitica-descriptiva-andres/`, construidos de forma independiente al proyecto predictivo del compañero, según `PROMPT_EDA_EXTENSO_OE02_OE03.md`. Cubre OE-02 (modelo dimensional) y OE-03 (normalización, indicadores, EDA e hipótesis). No cubre OE-01 (ya evaluado en `InformesRev/RESUMEN_CODIGO.md`) ni la construcción del tablero interactivo de OE-04 (fase posterior).

> **Nota (actualizada tras reunión con el tutor):** este documento fue elaborado bajo el diseño del anteproyecto original, que restringía el análisis a 2018-2024 y a contratos con ejecución avanzada/finalizada (19.194 de 48.331 contratos). En reunión de seguimiento, el tutor instruyó unificar el universo de datos con el trabajo del compañero y usar el total de contratos disponibles (48.331, sin restricción temporal) como base oficial del análisis final. El EDA extendido en `eda-extendido-integral/` retoma estos mismos hallazgos sobre el universo completo, en doble lectura (universo completo + este subconjunto como sensibilidad). La síntesis oficial y actualizada está en `eda-extendido-integral/docs/11_sintesis_dual.md` y `HALLAZGOS_ETIQUETADOS.md`; este documento se conserva como la primera iteración del análisis y sigue siendo válido como verificación de sensibilidad bajo el diseño metodológico original.

## 1. Modelo dimensional (OE-02)

Modelo dimensional simplificado sobre Parquet: 1 tabla de hechos (48.331 contratos) + 5 dimensiones (proceso, proveedor, entidad, territorio, modalidad), integridad referencial 100%. Cierra la brecha de `MATRIZ_OBJETIVOS_CODIGO.md` (Camino B de OE-02).

## 2. Calidad de datos y muestra analítica (OE-03)

Umbrales de calidad propios definidos (apta ≤20% nulidad). Criterios de inclusión/exclusión 3.6.3/3.6.4 del anteproyecto aplicados por primera vez de forma verificable, incluido el filtro 2018-2024. Muestra analítica final: **19.194 de 48.331 contratos (39.7%)**. Hallazgo de calidad propio: 3.538 contratos con inconsistencia liquidación/estado, resuelta conservadoramente.

## 3. Indicadores de la restricción de hierro

Derivados de forma completamente independiente al código excluido del compañero (`notebooks/07`, `08`): desviación de tiempo (días, N=16.326), desviación de costo (%, N=8.681, limitado por cobertura de `valor_pagado`), índice de alcance categórico (N=19.194). **Limitación crítica:** la tasa de sobrecosto medida (0.1%) contrasta con la cifra del problema de investigación (~25%); hipótesis explicativa declarada sin inspeccionar código excluido.

## 4. EDA e hipótesis — hallazgos principales

- 51.2% de contratos con retraso (desviación de tiempo > 0).
- **H0 (mixta):** licitación pública con peor tiempo (mediana 26 vs. 0 días, efecto -0.3798, universo completo de 48.331 — lectura oficial; mediana 49 vs. 2, efecto -0.316/-0.386 en el subconjunto de 19.194, sensibilidad) pero mejor costo (-9.18% vs. 0%, efecto 0.4277 universo; -2.44% vs. 0%, efecto 0.383 subconjunto) que modalidades de menor competencia. Disociación tiempo/costo relevante para la discusión teórica, consistente en ambas lecturas. Ver además `eda-extendido-integral/docs/10_hipotesis_extendido.md`: al estratificar por cuantía el efecto de la modalidad cae 70.7% (universo) / 72.9% (subconjunto), y medido con competencia real (número de oferentes) el efecto sobre el tiempo es nulo — la escala del proyecto, no la competencia, es lo que discrimina.
- **H1 (parcial):** consorcios/UT con más modificaciones totales (efecto -0.372) pero no más adiciones en valor específicamente (efecto nulo).
- **H2 (no probada):** sin datos de NBI municipal; proxy departamental muestra heterogeneidad significativa, pero no valida la hipótesis tal como fue formulada.
- Asociación modalidad↔alcance: V de Cramér 0.268 (moderada). Asociación tipo de contratista↔alcance: V de Cramér 0.184 (débil-moderada).

## 5. Relación con el marco teórico

Consistente con la restricción de hierro (Atkinson, 1999; Meredith & Mantel, 2012): el mecanismo que más disciplina el costo (licitación, mayor competencia) no necesariamente mejora el cronograma, sugiriendo un trade-off entre dimensiones más que una mejora simultánea — coherente con antecedentes citados (Rodríguez Arévalo, 2021; Feigenbaum et al., 2024).

## 6. Limitaciones declaradas

1. Muestra analítica sesgada a contratos con ejecución avanzada/finalizada (39.7% del universo).
2. Indicador de costo cubre solo 45.2% de la muestra (brecha de reporte SECOP, no atribuible a este análisis).
3. Índice de alcance no distingue "reducción del objeto contratado".
4. H2 sin datos reales de NBI municipal.
5. Variables extrañas (numeral 3.3 del anteproyecto) no controladas.
6. Ninguna asociación implica causalidad (diseño transversal, censal condicionado).
7. Autoría del dato de entrada (pipeline compartido) pendiente de confirmación con el director.

## 7. Siguiente paso

Este material queda listo para conectarse a un tablero Streamlit + Plotly (OE-04, decisión ya aprobada en `MATRIZ_OBJETIVOS_CODIGO.md`), y para redactarse directamente como capítulo de resultados de la tesis.
