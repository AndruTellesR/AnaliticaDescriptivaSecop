# Dataset: Proponentes por Proceso SECOP II

## Fuente de datos para enriquecimiento con información financiera del RUP

---

## Resumen

Se descubrió y descargó el dataset **Proponentes por Proceso SECOP II** (`hgi6-6wh3`) de datos.gov.co,
que contiene la lista de proveedores que presentaron oferta en cada proceso de contratación pública.

Este dataset se usa para obtener los NITs de todos los participantes en procesos de Obra,
no solo los ganadores (que ya están en contratosElectronicos).

---

## Fuente

| Atributo | Valor |
|---|---|
| Nombre | Proponentes por Proceso SECOP II |
| Dataset ID | `hgi6-6wh3` |
| API SODA | `https://www.datos.gov.co/resource/hgi6-6wh3.json` |
| Registros totales | ~2.25 millones (todos los tipos de contrato) |
| Granularidad | 1 fila = 1 proponente en 1 proceso |

## Columnas (9)

| Campo API | Tipo | Descripción |
|---|---|---|
| `id_procedimiento` | Texto | Identificador del procedimiento (CO1.REQ.XXX) |
| `fecha_publicaci_n` | Timestamp | Fecha de publicación del proceso |
| `nombre_procedimiento` | Texto | Nombre del proceso |
| `nit_entidad` | Número | NIT de la entidad contratante |
| `codigo_entidad` | Número | Código de la entidad contratante |
| `entidad_compradora` | Texto | Nombre de la entidad compradora |
| `proveedor` | Texto | Nombre del proveedor/proponente |
| `nit_proveedor` | Texto | NIT del proveedor |
| `codigo_proveedor` | Número | Código SECOP II del proveedor |

---

## Llave de integración

```
procesosDeContratacion.id_del_proceso  (CO1.REQ.XXX)
              ↕ match
proponentesporProceso.id_procedimiento (CO1.REQ.XXX)
```

**Importante**: Este dataset NO se cruza directamente con `contratosElectronicos`.
Los contratos electrónicos son un caso especial de procesos que se firmaron electrónicamente
y no aparecen en `procesosDeContratacion` ni en este dataset.

---

## Descarga (Notebook 06)

### Estrategia

El dataset completo tiene ~2.25M registros de todos los tipos de contrato. Para obtener solo los
de Obra, se filtró desde la API usando los 112,891 `id_del_proceso` únicos del parquet
`procesos_contratacion_obra.parquet`.

### Método

- Consulta por lotes de 150 IDs usando `WHERE id_procedimiento IN (...)`
- 753 lotes con paginación de 50,000 registros
- Reintentos con backoff exponencial (10s, 20s, 30s...)

### Resultados

| Métrica | Valor |
|---|---|
| Registros descargados | 276,770 |
| Procesos con proponentes | 33,171 de 112,891 (29.4%) |
| Procesos sin proponentes | 79,720 (70.6%) |
| Proponentes únicos (NIT) | 23,759 |
| Entidades únicas | 2,264 |
| `nit_proveedor` = "No Definido" | 93,103 (33.6%) |

### Proponentes por proceso

| Estadístico | Valor |
|---|---|
| Media | 8.3 |
| Mediana | 3 |
| P75 | 8 |
| Máximo | 255 |

---

## Calidad de datos — NITs

### Problemas encontrados

| Problema | Registros | Únicos |
|---|---|---|
| "No Definido" | 93,103 | 1 |
| No numérico (texto, consorcios) | 1,770 | 644 |
| Muy corto (< 6 dígitos) | 1,091 | 145 |
| Muy largo (> 10 dígitos) | 406 | 240 |
| Todo ceros | 1,279 | 20 |
| **NITs limpios (6-10 dígitos)** | **179,699** | **22,724** |

### Limpieza aplicada

1. NITs con dígito verificador (`XXXXXXXXX-D`): se extrajo la parte antes del guion (111 recuperados)
2. Filtro: solo dígitos puros, longitud 6-10
3. Consorcios y Uniones Temporales: marcados como `procesar=False` en el dataset unificado

---

## Dataset unificado: `proveedores_rup.parquet`

Se combinaron los NITs limpios de ambas fuentes en un solo dataset a nivel NIT:

| Fuente | NITs únicos |
|---|---|
| Solo procesos | 10,020 |
| Solo electrónicos | 5,768 |
| Ambas fuentes | 12,760 |
| **Total** | **28,548** |
| A procesar (sin consorcios/UT) | **21,164** |

Este parquet es la fuente única de verdad para el scraper RUP (`extraer_rup_auto.py`).
Ver [documentación del scraper](extraer_rup_documentacion.md) para detalles de la extracción.

---

## Archivos generados

| Archivo | Descripción |
|---|---|
| `data/proponentes_por_proceso_obra.parquet` | Descarga cruda: 276,770 registros, 9 columnas |
| `data/proveedores_rup.parquet` | Dataset unificado: 28,548 NITs, 22 columnas (incluye columnas RUP vacías) |
| `notebooks/06_proponentes_por_proceso.ipynb` | Notebook con descarga, perfilado, limpieza y creación del dataset unificado |
