# 04 — EDA univariado: distribuciones y outliers

**Objetivo específico que responde:** contenido analítico base de OE-04 (RF-05: distribuciones, box plots, segmentaciones).

## Hallazgos

- Desviación de tiempo, desviación de costo y valor del contrato presentan distribuciones fuertemente asimétricas (skew verificado en el notebook 06: 20.1, -36.5 y -2.8 respectivamente) con outliers extremos heredados de inconsistencias ya documentadas del dato fuente SECOP. Se reportan mediana y RIC además de media/desviación estándar, y se aplicó winsorización P1-P99 solo para visualización.
- Modalidad más frecuente en la muestra analítica: Selección Abreviada de Menor Cuantía (6.026 contratos, 31.4%), seguida de Licitación pública Obra Pública (3.947) y Mínima cuantía (3.865).
- Tipo de contratista: Persona Jurídica (11.919), Consorcio/UT (4.562), Persona Natural (2.596).
- Índice de alcance: 57.1% "Entregado en su totalidad", 22.5% "No entregado", 20.4% "Entregado parcialmente".

## Figuras generadas

`analitica-descriptiva-andres/figuras/04_desviacion_tiempo.png`, `04_desviacion_costo.png`, `04_valor_y_plazos.png`, `04_variables_categoricas.png`, `04_indice_alcance.png`.
