# 07 — Contraste exploratorio de las hipótesis H0, H1 y H2

**Objetivo específico que responde:** `InformesRev/AnteproyectoAndres.md`, numeral 3.2. Alfa declarado a priori: 0.05. Pruebas no paramétricas (Mann-Whitney U, Kruskal-Wallis) justificadas por la asimetría verificada en el notebook 06.

> **Nota (actualizada tras reunión con el tutor):** las cifras de este documento se calcularon sobre el subconjunto filtrado por fecha (2018-2024) y estado avanzado/finalizado (19.194 contratos), conforme al anteproyecto original. El tutor instruyó posteriormente usar el total de datos disponibles (48.331, sin filtro temporal) como universo oficial del análisis final, para mantener consistencia con el trabajo del compañero. La lectura oficial actualizada de H0 está en `eda-extendido-integral/docs/10_hipotesis_extendido.md`: rank-biserial -0.3798 en tiempo (mediana 26 vs. 0 días) y +0.4277 en costo, sobre el universo completo de 48.331 contratos. La conclusión (H0 se invierte en tiempo, se sostiene en costo) es la misma en ambas lecturas; lo que cambia es la magnitud exacta. Las cifras de este documento (19.194) se conservan como análisis de sensibilidad bajo el diseño metodológico originalmente declarado en el anteproyecto.

## H0 — Licitación pública vs. modalidades de menor competencia

| Variable | Mediana licitación | Mediana menor competencia | p-valor | Efecto (rank-biserial) |
|---|---|---|---|---|
| Desviación de tiempo (días) | 49.0 | 2.0 | 5.7e-156 | **-0.316** |
| Desviación de costo (%) | -2.44 | 0.0 | 1.0e-136 | **0.383** |

**Conclusión: mixta.** No se sostiene para tiempo (sentido contrario — licitación con mayor desviación). Sí se sostiene para costo (licitación con menor desviación). N=4.069 (licitación) vs. 9.974 (menor competencia); 5.151 contratos excluidos por modalidad no clasificable.

## H1 — Consorcios/UT vs. personas jurídicas individuales

| Variable | Mediana consorcio/UT | Mediana persona jurídica | p-valor | Efecto (rank-biserial) |
|---|---|---|---|---|
| N. total de modificaciones | 5.0 | 3.0 | 4.0e-306 | **-0.372** |
| N. de adiciones en valor | 0.0 | 0.0 | 0.004 | -0.017 (nulo) |

**Conclusión: parcial.** Se sostiene para modificaciones totales (efecto moderado). No se sostiene para adiciones en valor específicamente (p-valor significativo pero efecto prácticamente nulo — ejemplo de significancia estadística sin relevancia práctica).

## H2 — NBI territorial vs. tiempo/costo

**Limitación crítica:** no existe columna de NBI municipal en el dataset integrado disponible. Esta sección **no es una prueba válida de H2**. Se reporta, solo con fines exploratorios, Kruskal-Wallis de desviación de tiempo/costo entre los 8 departamentos de mayor volumen (proxy geográfico, no NBI):

- Desviación de tiempo: H=670.67, p=1.45e-140 (heterogeneidad significativa).
- Desviación de costo: H=190.32, p=1.28e-37 (heterogeneidad significativa).

**Recomendación de trabajo futuro:** incorporar el índice NBI oficial del DANE por municipio antes de reformular esta prueba con validez plena.
