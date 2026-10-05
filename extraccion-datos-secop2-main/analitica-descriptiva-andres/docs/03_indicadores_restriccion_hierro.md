# 03 — Derivación independiente de los indicadores de tiempo, costo y alcance

**Objetivo específico que responde:** núcleo de OE-03 y de la restricción de hierro (`InformesRev/AnteproyectoAndres.md`, numerales 2.2.2 y 3.3).

**Regla de blindaje de autoría:** las fórmulas se derivan exclusivamente del texto del anteproyecto. No se leyó, copió ni parafraseó `notebooks/07_depuracion_variables_modelo.ipynb` ni `notebooks/08_integracion_rup_no_consorcios.ipynb` (código del compañero, excluido). Columnas ya presentes en el dataset pero deliberadamente no usadas: `tiempo`, `presupuesto`, `alcance`, `sobrecosto_ratio`, `duracion_planificada_dias`, `ratio_extension_duracion`, `dias_hasta_primera_adicion`, `ventana_adiciones_dias`, `log_valor_contrato`, `rup_*`, `pliego_*`.

## Fórmulas y resultados

| Indicador | Fórmula | N efectivo | Resultado |
|---|---|---|---|
| Desviación de tiempo (días) | plazo real (fin−inicio) − plazo pactado (parseado de `duraci_n_del_contrato`) | 16.326 (85.1%) | 51.2% de los contratos con dato válido presentan retraso (desviación > 0) |
| Desviación de costo (%) | (valor_pagado − valor_del_contrato) / valor_del_contrato × 100 | 8.681 (45.2%, solo con pago > 0) | Mediana 0%; solo 0.1% con sobrecosto positivo |
| Índice de cumplimiento de alcance | Categórico: No entregado (terminación anticipada) / Entregado parcialmente (suspensión o cesión) / Entregado en su totalidad | 19.194 (100%) | 57.1% total, 22.5% no entregado, 20.4% parcial |

## Hallazgo relevante para la discusión

La tasa de sobrecosto medida (0.1%) es sustancialmente menor a la cifra citada en el problema de investigación del anteproyecto (~25%). Hipótesis plausible (no verificada contra código excluido): `valor_del_contrato` en el dataset integrado podría reflejar el valor ya actualizado tras adiciones formales, no el valor originalmente pactado, subestimando el sobrecosto medido. Se declara como limitación metodológica y recomendación de trabajo futuro.

## Limitaciones declaradas

- Cobertura reducida del indicador de costo (45.2%) por brecha de reporte de `valor_pagado` en SECOP (54.8% de la muestra analítica registra pago en cero incluso en contratos finalizados).
- El índice de alcance no distingue "reducción del objeto contratado" por ausencia de variable cruda específica.
- Outliers extremos en desviación de tiempo (heredados del dato fuente), tratados en el notebook 04.

## Artefactos generados

- `analitica-descriptiva-andres/data/indicadores_restriccion_hierro.parquet` (19.194 × 28)
