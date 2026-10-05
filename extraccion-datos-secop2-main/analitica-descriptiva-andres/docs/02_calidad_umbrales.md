# 02 — Calidad de datos: umbrales cuantitativos y muestra analítica

**Objetivo específico que responde:** OE-03. **Brecha que cierra:** ausencia de umbrales cuantitativos de calidad y de filtro de fecha 2018-2024 verificable (`MATRIZ_OBJETIVOS_CODIGO.md`, sección 5).

## Umbrales de calidad definidos (propios)

Apta ≤20% nulidad | Uso restringido 20-50% | No apta >50%. Las 10 columnas clave evaluadas (fechas, valor, duración, estado, liquidación) resultaron todas "Aptas" (nulidad máxima 12.6% en `fecha_de_inicio_del_contrato`).

## Criterios de inclusión/exclusión del anteproyecto (numerales 3.6.3/3.6.4), aplicados por primera vez de forma verificable

Embudo de filtrado (funnel), sobre 48.331 contratos de partida:

| Paso | Contratos restantes | Retención |
|---|---|---|
| Total contratos de Obra integrados | 48.331 | 100.0% |
| Fecha de firma en 2018-2024 | 32.175 | 66.6% |
| Campos mínimos no nulos | 31.610 | 65.4% |
| Excluidos valor_del_contrato ≤ 0 | 31.544 | 65.3% |
| Excluidas fechas invertidas | 31.543 | 65.3% |
| Estado avanzado/finalizado (conservador) | **19.194** | **39.7%** |

## Hallazgo de calidad de datos propio

Se detectaron 3.538 contratos con `liquidaci_n='Si'` pero `estado_contrato` aún activo (En ejecución: 2.800, Aprobado: 443, Suspendido: 290, Cancelado: 5) — inconsistencia del propio dato fuente SECOP. Se resolvió con el criterio más conservador: la exclusión por estado activo (3.6.4) tiene prioridad sobre la inclusión por liquidación (3.6.3).

## Muestra analítica final

**19.194 contratos** (39.7% del universo integrado). Distribución de `estado_contrato`: terminado (10.378), Modificado (5.897), Cerrado (2.894), cedido (25).

## Artefactos generados

- `analitica-descriptiva-andres/data/muestra_analitica.parquet` (19.194 × 29)
- `analitica-descriptiva-andres/data/reporte_calidad_funnel.csv`
- `analitica-descriptiva-andres/data/reporte_calidad_umbrales.csv`
