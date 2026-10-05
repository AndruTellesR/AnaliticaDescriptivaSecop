# Documentación del Proyecto — Modelo Predictivo SECOP II Obra Pública

> Metodología: CRISP-DM
> Filtro global: `tipo_de_contrato = "Obra"`

---

## Contexto general

- [Contexto del proyecto](contexto/CONTEXTO.md) — Fuentes de datos, esquema relacional, decisiones clave, estado actual

---

## Fases CRISP-DM

### Fase 1 — Comprensión del negocio
> Pendiente de documentar

### Fase 2 — Comprensión de los datos ✓
- [Diccionario de datos](fase2_comprension_datos/diccionario_datos.md) — Definición completa de los 7 datasets (316 columnas), contrastado con diccionario oficial SECOP, valores sentinela, esquema relacional
- [Informe Fase 2](fase2_comprension_datos/INFORME_FASE2_COMPRENSION_DATOS.md) — Exploración de las 4 fuentes, calidad de datos, features candidatos
- [Informe Integración Contratos + Adiciones](fase2_comprension_datos/INFORME_INTEGRACION_CONTRATOS_ADICIONES.md) — JOIN contratos/adiciones, targets viables, predictores fuertes

#### Enriquecimiento RUP
- [Investigación urlproceso + API RUP](fase2_comprension_datos/enriquecimiento_rup/investigacion_urlproceso_rup.md) — Viabilidad scraping SECOP, API RUP descubierta, K financiero del proveedor
- [Análisis K Residual — Viabilidad para el modelo](fase2_comprension_datos/enriquecimiento_rup/analisis_k_residual_viabilidad.md) — Limitaciones `urlproceso`, alternativa RUP, recomendación al director
- [Dataset Proponentes por Proceso](fase2_comprension_datos/enriquecimiento_rup/dataset_proponentes_por_proceso.md) — Fuente hgi6-6wh3, descarga por lotes, limpieza NITs, dataset unificado proveedores_rup.parquet
- [Documentación scripts extracción RUP](fase2_comprension_datos/enriquecimiento_rup/extraer_rup_documentacion.md) — Arquitectura CapSolver+Playwright, estrategia anti-bloqueo, estructura del parquet, índices financieros
- [Metodología de obtención de datos RUP](fase2_comprension_datos/enriquecimiento_rup/metodologia_obtencion_datos_rup.md) — Proceso completo: identificación de fuentes, obtención de NITs, desarrollo del scraper, resultados finales

### Fase 3 — Preparación de los datos
- [Plan de limpieza, transformación e imputación](fase3_preparacion_datos/plan_limpieza_transformacion_imputacion.md) — Inventario de calidad, pipeline de limpieza, ingeniería de features, estrategia de imputación por mecanismo (MCAR/MAR/MNAR), prevención de leakage
- [Variables candidatas para el modelo](fase3_preparacion_datos/variables_candidatas_modelo.md) — Targets (clasificación/regresión), ~66 features candidatas priorizadas, variables de leakage, esquema del dataset analítico

### Fase 4 — Modelado
> Pendiente

### Fase 5 — Evaluación
> Pendiente
