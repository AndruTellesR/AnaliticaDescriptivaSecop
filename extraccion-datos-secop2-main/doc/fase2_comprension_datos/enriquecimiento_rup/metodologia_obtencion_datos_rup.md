# Metodología de obtención de datos financieros del RUP

## Enriquecimiento del dataset de contratación pública con información financiera de proponentes

---

## 1. Objetivo

Enriquecer el dataset de contratos de Obra Pública de SECOP II con información financiera de los proponentes
extraída del Registro Único de Proponentes (RUP), administrado por las Cámaras de Comercio de Colombia.

**Hipótesis**: La capacidad financiera del proponente (liquidez, endeudamiento, tamaño, historial de sanciones)
es un predictor relevante de problemas contractuales como atrasos, adiciones presupuestales y sobrecostos.

---

## 2. Identificación de la fuente

### 2.1 El RUP como fuente de datos financieros

El RUP es el registro obligatorio para participar en contratación pública en Colombia. Los proponentes deben
reportar anualmente su información financiera, que incluye:

- Estados financieros (activos, patrimonio, ingresos, utilidad neta)
- Indicadores calculados (liquidez, endeudamiento, cobertura de intereses, rentabilidad)
- Información de perfil (tamaño empresa, empleados, municipio)
- Historial de sanciones, multas e inhabilidades

### 2.2 API descubierta

Se identificó que el portal `ruppro.colombiacompra.gov.co` expone una API interna de consulta por NIT:

```
GET https://ruppro.colombiacompra.gov.co/api/buscarProponente/{NIT}
```

**Restricciones de acceso**:
- Requiere reCAPTCHA v2 (token válido como header de autorización)
- Protegida por Azure Application Gateway WAF (bloquea peticiones HTTP directas)
- Sin documentación pública ni rate limits declarados

---

## 3. Obtención de NITs a consultar

Para maximizar la cobertura, se obtuvieron NITs de dos fuentes complementarias:

### 3.1 Fuente 1: Proponentes por Proceso SECOP II (`hgi6-6wh3`)

Dataset público en datos.gov.co que lista todos los proveedores que presentaron oferta en cada proceso
de contratación. Contiene ~2.25 millones de registros (todos los tipos de contrato).

**Llave de integración**:
```
procesosDeContratacion.id_del_proceso (CO1.REQ.XXX)
                    ↕
proponentesporProceso.id_procedimiento (CO1.REQ.XXX)
```

**Proceso de descarga** (Notebook `06_proponentes_por_proceso.ipynb`):
1. Se extrajeron 112,891 IDs de procesos únicos de Obra desde `procesos_contratacion_obra.parquet`
2. Consulta a la API SODA por lotes de 150 IDs usando `WHERE id_procedimiento IN (...)`
3. 753 lotes con paginación de 50,000 registros y reintentos con backoff exponencial
4. Resultado: **276,770 registros** en `proponentes_por_proceso_obra.parquet`

**Cobertura**: Solo 33,171 de 112,891 procesos de Obra (29.4%) tienen proponentes registrados en este dataset.

### 3.2 Fuente 2: Contratos Electrónicos (`jbjy-vk9h`)

Los contratos electrónicos son un caso especial que **no aparece** en `procesosDeContratacion`
ni en `proponentesporProceso`. Los NITs de estos proveedores se obtuvieron directamente del campo
`codigo_proveedor` del dataset `contratos_electronicos_obra.parquet` (descargado en Notebook 01).

### 3.3 Limpieza y unificación de NITs

Se aplicaron los siguientes filtros de calidad a los NITs de ambas fuentes:

| Paso | Descripción | Resultado |
|---|---|---|
| 1 | Eliminar "No Definido" y cadenas vacías | Descarta sentinelas |
| 2 | Remover dígito verificador (`846002422-3` → `846002422`) | 111 NITs recuperados |
| 3 | Filtrar solo dígitos puros, longitud 6-10 | Descarta texto libre y códigos cortos/largos |
| 4 | Marcar consorcios y uniones temporales como `procesar=False` | No tienen registro RUP propio |
| 5 | Deduplicar y clasificar origen (`procesos`, `electronicos`, `ambos`) | Un NIT puede venir de ambas fuentes |

**Dataset unificado resultante** (`proveedores_rup.parquet`):

| Origen | NITs |
|---|---|
| Solo procesos | 10,020 |
| Solo electrónicos | 5,768 |
| Ambas fuentes | 12,760 |
| **Total** | **28,548** |
| A procesar (sin consorcios/UT) | **21,164** |
| No procesar (consorcios/UT) | 7,384 |

---

## 4. Desarrollo del scraper

### 4.1 Desafíos técnicos

| Desafío | Solución |
|---|---|
| reCAPTCHA v2 en cada consulta | **CapSolver** — servicio de resolución automática ($0.80/1000 tokens) |
| Azure WAF bloquea `requests` de Python | **Playwright** — ejecuta `fetch()` desde el navegador en contexto same-origin |
| Riesgo de bloqueo por IP | Estrategia de throttling progresiva (delay, cooldown, auto-brake) |
| 21K+ NITs a consultar | Persistencia incremental en parquet + resume automático |

### 4.2 Evolución del script

| Versión | Descripción |
|---|---|
| `extraer_rup.py` | Prueba de concepto — CAPTCHA manual, 1 NIT a la vez |
| `extraer_rup_v2.py` | Validación de reutilización de token — confirmó ~15-50 consultas por token |
| `extraer_rup_auto.py` | **Versión final** — CapSolver + Playwright, masivo, resiliente |

### 4.3 Arquitectura del scraper final

```
proveedores_rup.parquet ──→ filtrar (procesar=True, procesado=False)
         │
         ▼
   CapSolver API ──→ resuelve reCAPTCHA v2 ──→ token
         │
         ▼
   Playwright (Chromium headless)
   └─ navega a ruppro.colombiacompra.gov.co
   └─ page.evaluate(fetch("/api/buscarProponente/{NIT}", token))
         │
         ▼
   Clasificación de respuesta:
   ├─ 200 + datos    → guarda 18 campos RUP, marca procesado=True
   ├─ 200 sin datos  → marca procesado=True (no registrado)
   ├─ "No se encontró" → marca procesado=True (NIT no existe en RUP)
   ├─ 400/403        → token expirado → nuevo CAPTCHA → reintenta
   └─ Otro error     → NO marca procesado → se reintenta en siguiente ejecución
         │
         ▼
   Persistencia cada 50 NITs ──→ proveedores_rup.parquet
```

### 4.4 Estrategia anti-bloqueo

| Mecanismo | Configuración | Propósito |
|---|---|---|
| Delay entre peticiones | 2.5 – 4.0 s aleatorio | Simular comportamiento humano |
| Cooldown periódico | 3 min cada 500 NITs | Dar descanso al servidor |
| Auto-brake | 15 min tras 3 errores consecutivos reales | Detectar bloqueo temporal |
| Reutilización de token | 1 CAPTCHA → ~50 consultas | Minimizar costo CapSolver |
| Resume automático | Solo procesa `procesado=False` | Tolerante a interrupciones (Ctrl+C) |

**Nota**: Los NITs no encontrados en el RUP (respuesta válida de la API) no se cuentan como error para el auto-brake. Solo errores de red, HTTP 503, o WAF blocks cuentan como errores reales.

### 4.5 Manejo de errores

| Tipo de respuesta | Acción | ¿Marca procesado? | ¿Cuenta como error? |
|---|---|---|---|
| 200 + datos RUP | Guarda 18 campos financieros | Sí | No |
| 200 + success, sin data | Marca "no registrado" | Sí | No |
| 200 + "No se encontró" | Marca "no encontrado" | Sí | No |
| 400 / 403 | Token expirado → resuelve nuevo CAPTCHA | No (reintenta) | No |
| 503 / otro HTTP | Error real del servidor | **No** | **Sí** |

---

## 5. Ejecución y resultados

### 5.1 Proceso de ejecución

La extracción se realizó en múltiples sesiones a lo largo de 3 días, ejecutando el script con:

```bash
python scripts/extraer_rup_auto.py
```

El diseño de resume automático permitió detener y reiniciar el script sin pérdida de progreso.
El parquet se actualizó incrementalmente en cada sesión.

### 5.2 Resultados finales

| Métrica | Valor |
|---|---|
| **NITs totales en dataset** | **28,548** |
| NITs procesables (sin consorcios) | 21,164 |
| **NITs procesados** | **21,164 (100%)** |
| NITs con datos RUP | 13,438 (63.5%) |
| NITs sin datos en RUP | 7,726 (36.5%) |
| Consorcios/UT (no procesados) | 7,384 |

### 5.3 Cobertura por origen

| Origen | Procesados | Con datos RUP | Tasa de éxito |
|---|---|---|---|
| Ambas fuentes | 8,399 | 6,612 | 78.7% |
| Solo procesos | 7,470 | 5,863 | 78.5% |
| Solo electrónicos | 5,295 | 963 | 18.2% |

**Observación**: Los proveedores exclusivos de contratos electrónicos tienen una tasa de registro RUP
significativamente menor (18.2% vs ~78.5%). Esto puede deberse a que muchos son personas naturales
o empresas que participan en contratación directa sin necesidad de inscripción RUP vigente.

### 5.4 Estado de inscripción RUP

| Estado | Cantidad | % |
|---|---|---|
| ACTIVA | 11,802 | 87.8% |
| CANCELADA | 1,452 | 10.8% |
| Matrícula nueva / traslado | 176 | 1.3% |
| Cancelada por traslado / Ley 1429 | 18 | 0.1% |

### 5.5 Distribución por tamaño de empresa

| Código | Tamaño | Cantidad | % |
|---|---|---|---|
| 01 | Microempresa | 8,195 | 61.0% |
| 02 | Pequeña | 2,949 | 21.9% |
| 03 | Mediana | 1,196 | 8.9% |
| 00 | No clasificada | 555 | 4.1% |
| 04 | Grande | 488 | 3.6% |

---

## 6. Variables extraídas del RUP

### 6.1 Información de perfil

| Variable | Descripción | Uso potencial en modelo |
|---|---|---|
| `rup_estado` | Estado de la matrícula RUP | Feature categórica: matrícula activa vs cancelada |
| `rup_tamano` | Tamaño de empresa (micro/pequeña/mediana/grande) | Proxy de capacidad operativa |
| `rup_empleados` | Número de empleados | Capacidad de ejecución |
| `rup_municipio` | Municipio del domicilio comercial | Feature geográfica |
| `rup_sanciones` | Cantidad de sanciones | Historial de incumplimiento |
| `rup_multas` | Cantidad de multas | Historial de incumplimiento |
| `rup_inhabilidad` | Inhabilidad vigente | Indicador de riesgo legal |

### 6.2 Información financiera

| Variable | Descripción |
|---|---|
| `rup_ano_financiero` | Año fiscal de los estados financieros reportados |
| `rup_activo_total` | Activo total (COP) |
| `rup_patrimonio` | Patrimonio neto (COP) |
| `rup_ingresos` | Ingresos por actividad ordinaria (COP) |
| `rup_utilidad_neta` | Resultado del período (COP) |

### 6.3 Indicadores financieros calculados por el RUP

| Indicador | Fórmula | Interpretación |
|---|---|---|
| `rup_idx_liquidez` | Activo corriente / Pasivo corriente | Capacidad de pago a corto plazo (umbral pliegos: ≥ 1.0) |
| `rup_idx_endeudamiento` | Pasivo total / Activo total | Proporción de deuda (umbral pliegos: ≤ 0.70) |
| `rup_idx_cobertura` | Utilidad operacional / Gastos intereses | Capacidad de servicio de deuda (umbral pliegos: ≥ 1.0) |
| `rup_rent_patrimonio` | Utilidad neta / Patrimonio | Rentabilidad sobre recursos propios |
| `rup_rent_activo` | Utilidad neta / Activo total | Eficiencia en uso de activos |

---

## 7. Estructura del dataset final

El archivo `data/proveedores_rup.parquet` contiene 28,548 registros y 22 columnas:

| Grupo | Columnas |
|---|---|
| Identificación | `nit`, `nombre_proveedor`, `origen` |
| Perfil RUP | `rup_estado`, `rup_tamano`, `rup_empleados`, `rup_municipio`, `rup_sanciones`, `rup_multas`, `rup_inhabilidad` |
| Financiero RUP | `rup_ano_financiero`, `rup_activo_total`, `rup_patrimonio`, `rup_ingresos`, `rup_utilidad_neta` |
| Índices RUP | `rup_idx_liquidez`, `rup_idx_endeudamiento`, `rup_idx_cobertura`, `rup_rent_patrimonio`, `rup_rent_activo` |
| Control | `procesado`, `procesar` |

---

## 8. Integración con el modelo predictivo

Este dataset se vincula con las fuentes principales del proyecto mediante:

```
contratosElectronicos.codigo_proveedor ──→ proveedores_rup.nit
procesosDeContratacion.id_del_proceso  ──→ proponentesporProceso.id_procedimiento
                                            └─→ proponentesporProceso.nit_proveedor ──→ proveedores_rup.nit
```

En la Fase 3 (Preparación de datos), las variables del RUP se incorporarán como features del proponente/contratista
al dataset de contratos, mediante LEFT JOIN por NIT.

---

## 9. Limitaciones y consideraciones

1. **Cobertura parcial (63.5%)**: No todos los NITs tienen registro RUP. Los JOINs con contratos generarán nulos que deberán tratarse (imputación o indicador de ausencia).

2. **Temporalidad de datos financieros**: El RUP reporta el último año fiscal declarado. No hay histórico — un contrato de 2020 se enriquece con la información financiera más reciente del proveedor, no necesariamente la de 2020.

3. **Consorcios y Uniones Temporales (26%)**: 7,384 NITs corresponden a consorcios/UT que no tienen registro RUP propio. Para estos, la información financiera debería obtenerse de los integrantes individuales, lo cual está fuera del alcance de esta fase.

4. **Proveedores exclusivos de electrónicos**: Tasa de registro RUP muy baja (18.2%), posiblemente por tratarse de contratación directa donde el RUP no es requisito.

5. **Acceso a la API**: La API del RUP no es pública ni documentada. La extracción se realizó respetando tiempos de espera entre consultas para no impactar el servicio.

---

## 10. Archivos generados

| Archivo | Descripción |
|---|---|
| `data/proponentes_por_proceso_obra.parquet` | Descarga cruda de proponentes: 276,770 registros, 9 columnas |
| `data/proveedores_rup.parquet` | Dataset unificado con datos RUP: 28,548 NITs, 22 columnas |
| `notebooks/06_proponentes_por_proceso.ipynb` | Descarga, perfilado, limpieza NITs, creación dataset unificado |
| `scripts/extraer_rup_auto.py` | Scraper masivo con CapSolver + Playwright |
| `scripts/extraer_rup.py` | Script original (CAPTCHA manual) |
| `scripts/extraer_rup_v2.py` | Validación de reutilización de token |
