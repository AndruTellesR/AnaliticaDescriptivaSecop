# 05 — EDA segmentado: modalidad, entidad y territorio

**Objetivo específico que responde:** OE-04 (RF-05: segmentaciones por modalidad/entidad/territorio).

> **Nota (actualizada tras reunión con el tutor):** las medianas por modalidad de este documento se calcularon sobre el subconjunto filtrado (19.194 contratos, 2018-2024 + estado avanzado/finalizado). El tutor instruyó usar el universo completo (48.331 contratos, sin filtro temporal) como base oficial del análisis final. Ver `eda-extendido-integral/docs/05_valor_precio_base_cuantia.md` y `10_hipotesis_extendido.md` para las cifras recalculadas sobre el universo completo. Estas cifras se conservan como referencia del primer EDA y como análisis de sensibilidad.

## Hallazgos clave

- **Modalidad:** "Licitación pública Obra Pública" presenta la mediana de desviación de tiempo más alta (50 días) de todas las modalidades, frente a 1 día en "Selección Abreviada de Menor Cuantía" y 0 días en "Mínima cuantía" — hallazgo contraintuitivo respecto a H0, contrastado formalmente en el notebook 07.
- **Tipo de contratista:** Consorcio/UT con mediana de desviación de tiempo de 27 días frente a 1 día (Persona Jurídica) y 0 días (Persona Natural); pero con **menor** tasa de "No entregado" (12.4%) que Persona Jurídica (26.4%) — patrón mixto.
- **Territorio:** entidades de orden Territorial con mediana de 3 días frente a 1 día en orden Nacional. Bogotá D.C. (mayor volumen, 7.345 contratos) presenta la mediana más alta entre los departamentos de mayor volumen (15 días).

## Figuras generadas

`05_tiempo_por_modalidad.png`, `05_segmentado_tipo_contratista.png`, `05_segmentado_territorio.png`.
