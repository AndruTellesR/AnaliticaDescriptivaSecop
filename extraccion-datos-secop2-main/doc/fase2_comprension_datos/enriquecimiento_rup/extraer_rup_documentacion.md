# Documentación: Scripts de extracción RUP

## Registro Único de Proponentes — Extracción de datos financieros

---

## Contexto

El RUP (Registro Único de Proponentes) es administrado por las Cámaras de Comercio de Colombia y contiene
información financiera que los proponentes deben reportar anualmente para participar en contratación pública.

La API del RUP (`ruppro.colombiacompra.gov.co`) requiere resolver un reCAPTCHA v2 para cada consulta.
Para escalar la extracción a miles de NITs, se desarrollaron 3 versiones del script:

| Script | Propósito | CAPTCHA | Estado |
|---|---|---|---|
| `extraer_rup.py` | Extracción manual, 1 CAPTCHA por NIT | Manual (usuario) | Funcional — para pruebas puntuales |
| `extraer_rup_v2.py` | Prueba de reutilización de token | Manual (usuario) | Funcional — confirmó que 1 token sirve para ~15-50 queries |
| `extraer_rup_auto.py` | **Extracción masiva automática** | CapSolver (API) | **Versión principal** |

---

## `extraer_rup_auto.py` — Versión principal

### Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│  1. Lee proveedores_rup.parquet                             │
│     → filtra: procesar=True AND procesado=False             │
│  2. Abre navegador Playwright (headless)                    │
│     → navega a ruppro.colombiacompra.gov.co                 │
│  3. Para cada NIT pendiente:                                │
│     a. Si no hay token → CapSolver resuelve reCAPTCHA v2    │
│     b. Llama API via page.evaluate(fetch()) — same-origin   │
│     c. Si 200 OK → escribe columnas rup_* en el DataFrame  │
│     d. Si 400/403 → token expiró, resuelve nuevo, reintenta│
│     e. Marca procesado=True                                 │
│     f. Delay aleatorio 2-4s entre peticiones                │
│  4. Cada 50 NITs → persiste parquet a disco                 │
│  5. Cada 500 NITs → cooldown de 5 min                      │
│  6. 3 errores seguidos → auto-brake 15 min                  │
│  7. Al terminar → reporte con costo CapSolver               │
└─────────────────────────────────────────────────────────────┘
```

### ¿Por qué Playwright en vez de `requests`?

La API del RUP está detrás de **Azure Application Gateway WAF**, que bloquea peticiones HTTP directas
desde Python (`requests`) con un 403 Forbidden. Al ejecutar `fetch()` desde dentro del navegador
Playwright, la petición se hace en contexto same-origin y el WAF la deja pasar.

### ¿Por qué CapSolver?

- Resuelve reCAPTCHA v2 automáticamente (sin intervención humana)
- Costo: **$0.80 USD / 1000 resoluciones**
- Un token se reutiliza para ~15-50 consultas antes de expirar
- No cobra si falla la resolución
- Tipo de tarea: `ReCaptchaV2TaskProxyLess`

### Estrategia anti-bloqueo

| Mecanismo | Valor | Configurable |
|---|---|---|
| Delay entre peticiones | 2-4s aleatorio | `DELAY_MIN`, `DELAY_MAX` |
| Cooldown periódico | 5 min cada 500 NITs | `--cooldown-every` |
| Auto-brake | 15 min tras 3 errores seguidos | `MAX_ERRORES_SEGUIDOS`, `BRAKE_PAUSE` |
| Persistencia incremental | Cada 50 NITs + cada cooldown | Automático |
| Resume automático | Solo procesa `procesado=False` | Automático |

### Uso

```bash
# Procesar todos los pendientes
python scripts/extraer_rup_auto.py

# Procesar solo 500 NITs en esta sesión
python scripts/extraer_rup_auto.py --limit 500

# Cooldown más frecuente (cada 200 NITs)
python scripts/extraer_rup_auto.py --limit 1000 --cooldown-every 200
```

### Reutilización de token CAPTCHA

El script no impone un límite artificial al uso del token. Lo usa hasta que la API responde
400 o 403 (token expirado), momento en el que:

1. Solicita un nuevo token a CapSolver
2. Reintenta el NIT que falló con el nuevo token
3. Continúa con los NITs restantes

En pruebas, un token dura entre 15 y 50+ consultas.

---

## Dataset: `proveedores_rup.parquet`

El scraper lee y escribe directamente este parquet. Es la fuente única de verdad.

### Estructura (22 columnas)

| Columna | Tipo | Descripción |
|---|---|---|
| `nit` | str | NIT del proveedor (llave única) |
| `nombre_proveedor` | str | Nombre del proveedor/proponente |
| `origen` | str | `procesos`, `electronicos`, o `ambos` |
| **— Perfil RUP —** | | |
| `rup_estado` | str | Estado matrícula: ACTIVA, SUSPENDIDA, etc. |
| `rup_tamano` | str | 01=Micro, 02=Pequeña, 03=Mediana, 04=Grande |
| `rup_empleados` | num | Número de empleados declarados |
| `rup_municipio` | str | Municipio comercial |
| `rup_sanciones` | int | Cantidad de sanciones registradas |
| `rup_multas` | int | Cantidad de multas registradas |
| `rup_inhabilidad` | str | Inhabilidad vigente (si aplica) |
| **— Financiero RUP —** | | |
| `rup_ano_financiero` | str | Año de la información financiera |
| `rup_activo_total` | num | Activo total (COP) |
| `rup_patrimonio` | num | Patrimonio neto (COP) |
| `rup_ingresos` | num | Ingresos actividad ordinaria (COP) |
| `rup_utilidad_neta` | num | Resultado del período (COP) |
| **— Índices calculados —** | | |
| `rup_idx_liquidez` | float | AC / PC — capacidad de pago a corto plazo |
| `rup_idx_endeudamiento` | float | PT / AT — proporción de deuda |
| `rup_idx_cobertura` | float | UO / GI — cobertura de intereses |
| `rup_rent_patrimonio` | float | UN / PN — rentabilidad sobre patrimonio |
| `rup_rent_activo` | float | UN / AT — rentabilidad sobre activos |
| **— Control —** | | |
| `procesado` | bool | ¿Se consultó la API? |
| `procesar` | bool | ¿Debe procesarse? (False = consorcios/UT) |

### Origen de los NITs

| Origen | NITs | Descripción |
|---|---|---|
| `procesos` | 10,020 | Proponentes que solo aparecen en procesosDeContratacion |
| `electronicos` | 5,768 | Proveedores que solo aparecen en contratosElectronicos |
| `ambos` | 12,760 | Aparecen en ambas fuentes |
| **Total** | **28,548** | |
| `procesar=True` | 21,164 | NITs reales para consultar en RUP |
| `procesar=False` | 7,384 | Consorcios/UT — no tienen RUP propio |

### Limpieza aplicada a los NITs

- Dígito verificador removido: `846002422-3` → `846002422`
- Filtro de longitud: solo 6-10 dígitos
- Descartados: "No Definido", texto libre, todo ceros, NITs < 6 dígitos
- Consorcios y Uniones Temporales: marcados `procesar=False` (no tienen registro RUP)

---

## Índices financieros — Interpretación

### Liquidez (AC / PC)

| Rango | Interpretación |
|---|---|
| < 1.0 | No puede cubrir deudas de corto plazo — riesgo de iliquidez |
| 1.0 – 2.0 | Rango normal para constructoras |
| > 3.0 | Posibles activos ociosos |
| **Umbral pliegos**: ≥ 1.0 | |

### Endeudamiento (PT / AT)

| Rango | Interpretación |
|---|---|
| 0.0 – 0.40 | Poco apalancada, sólida |
| 0.40 – 0.70 | Normal, aceptable en pliegos |
| > 0.70 | Muy endeudada, alto riesgo |
| **Umbral pliegos**: ≤ 0.70 | |

### Cobertura de intereses (UO / GI)

| Rango | Interpretación |
|---|---|
| < 1.0 | No genera suficiente utilidad para pagar intereses |
| 1.0 – 3.0 | Ajustado |
| > 3.0 | Buena holgura financiera |
| **Umbral pliegos**: ≥ 1.0 | |

### Rentabilidades (referencial)

- Valores negativos = pérdida en el período
- Se usan comparativamente entre proveedores, no como filtro de habilitación

---

## Dependencias

| Librería | Uso |
|---|---|
| `playwright` | Navegador Chromium para bypass WAF |
| `pandas` | Lectura/escritura parquet |
| `requests` | Comunicación con API CapSolver |
| `rich` | Tabla formateada en consola |

```bash
pip install playwright pandas requests rich
python -m playwright install chromium
```

---

## Configuración requerida

| Variable | Valor |
|---|---|
| `CAPSOLVER_API_KEY` | Clave API de CapSolver (en el script) |
| `RUP_SITE_KEY` | `6LfssZMrAAAAAEHbwOrGkKzKR9TFnmZFBwkQqw73` |
| `PARQUET` | `data/proveedores_rup.parquet` |
