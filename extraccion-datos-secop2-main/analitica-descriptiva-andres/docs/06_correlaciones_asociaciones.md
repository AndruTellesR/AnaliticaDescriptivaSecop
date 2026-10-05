# 06 — Análisis correlacional y de asociación

**Objetivo específico que responde:** OE-03/OE-04, numeral 3.4 del anteproyecto ("Relación lógica entre variables").

## Justificación estadística

Skewness verificado: `valor_del_contrato` (20.1), `plazo_pactado_dias` (34.6), `plazo_real_dias` (3.8), `desviacion_tiempo_dias` (-36.5), `desviacion_costo_pct` (-2.8). Todas descartan el supuesto de normalidad de Pearson; se usa correlación de **Spearman**.

## Asociaciones categóricas (chi-cuadrado + V de Cramér)

| Prueba | Chi² | gl | p-valor | V de Cramér | Interpretación |
|---|---|---|---|---|---|
| Modalidad de contratación vs. índice de alcance | 2763.35 | 16 | ~0 | **0.268** | Efecto moderado |
| Tipo de contratista vs. índice de alcance | 1300.56 | 6 | ~0 | **0.184** | Efecto débil-moderado |

## Advertencia metodológica

Correlación/asociación no implica causalidad. Diseño transversal, censal condicionado (numeral 3.1 y 3.6.2 del anteproyecto).

## Figuras generadas

`06_correlacion_spearman.png`
