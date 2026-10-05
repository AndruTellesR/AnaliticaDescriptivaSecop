# Análisis Técnico: K Residual y Capacidad Financiera del Proveedor
## Viabilidad para el Modelo Predictivo SECOP II — Obra Pública

> Documento técnico para presentar al director del proyecto
> Fecha: marzo 2026
> Estado: Fase 2 — Comprensión de datos

---

## 1. ¿Qué es el K Residual?

El **K residual** (también llamado **Capacidad Residual de Contratación**) es el saldo de capacidad de contratación que le queda a un proponente después de descontar los contratos que ya tiene en ejecución.

### Fórmula oficial (Decreto 1082/2015, Art. 2.2.1.1.1.6.1)

```
K_residual = CO × [(E + CT + CF) / 100] − SCE
```

| Variable | Significado |
|---|---|
| CO | Capacidad Organizacional (patrimonio neto registrado en RUP) |
| E  | Experiencia (puntaje de contratos ejecutados, según pliego) |
| CT | Capacidad Técnica (equipos/personal, según pliego) |
| CF | Capacidad Financiera (índices financieros, según pliego) |
| SCE | Saldo de Contratos en Ejecución (contratos vigentes del proponente) |

### Implicación clave

El K residual **no es un número fijo**. Varía en cada licitación porque:
- E, CT, CF son pesos definidos por cada entidad en sus pliegos
- SCE cambia con cada contrato nuevo o terminado
- No existe un repositorio centralizado y actualizado de K residual

---

## 2. ¿El K Residual está disponible en alguna fuente pública?

### Fuentes investigadas

| Fuente | ¿Contiene K residual? | Observación |
|---|---|---|
| SECOP II — `urlproceso` (página del proceso) | No directamente | Está en el **Informe de Evaluación** (PDF) |
| RUP (ruppro.colombiacompra.gov.co) | **No** | Solo certificado financiero; CO y CF extraíbles |
| datos.gov.co / SODA API | **No** | No existe dataset de K residual en datos abiertos |
| Cámara de Comercio (RUES) | **No** | Solo matrícula, objeto social, socios — no financiero |
| CHIP / SIIF (entes territoriales) | **No** | Solo sector público |

**Conclusión: el K residual NO está almacenado ni disponible como dato estructurado en ninguna fuente pública.**

---

## 3. Limitaciones de `urlproceso` (SECOP Community)

La columna `urlproceso` en `contratosElectronicos` apunta a:
```
https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.XXXXXXX
```

### Barreras técnicas identificadas

| Barrera | Severidad | Detalle |
|---|---|---|
| **reCAPTCHA Enterprise** | 🔴 Alta | Se activa por sesión; no bypasseable automáticamente sin servicio de terceros de pago |
| **`mkey` de sesión efímero** | 🔴 Alta | Token en URLs de descarga de documentos; expira al navegar entre páginas; no reutilizable |
| **K financiero en PDF** | 🔴 Alta | El Informe de Evaluación (único lugar con datos de K) es un PDF no estructurado; requeriría LLM/OCR para parsear |
| **Heterogeneidad de PDFs** | 🟡 Media | Cada entidad usa su propio formato de informe; no hay esquema estándar |
| **Volumen** | 🟡 Media | 51,353 URLs × tiempo de scraping + CAPTCHA = semanas de procesamiento manual |
| **Disponibilidad** | 🟡 Media | No todos los procesos tienen informe de evaluación publicado |

### Viabilidad de scraping de `urlproceso`

```
OBJETIVO           → Extraer K residual de oferentes por proceso
VIABILIDAD         → ❌ NO VIABLE a escala
ALTERNATIVA MANUAL → 🟡 Posible para muestra pequeña (< 50 procesos)
```

---

## 4. Alternativa viable: API del RUP

### ¿Qué es el RUP?

El **Registro Único de Proponentes** es el registro oficial de habilitación financiera, técnica y jurídica que toda empresa debe tener vigente para contratar con el Estado en Colombia.
Portal: `https://ruppro.colombiacompra.gov.co/`

### API descubierta

```
POST https://ruppro.colombiacompra.gov.co/msrup/api/v1/consultas/nit/completo
Body: { "nit": "830038225", "recaptchaToken": "<token_v2>" }
```

### Variables financieras extraíbles del RUP

| Variable | Uso en modelo |
|---|---|
| `activo_corriente` | Base para liquidez |
| `activo_total` | Base para endeudamiento y rentabilidad |
| `pasivo_corriente` | Base para liquidez |
| `pasivo_total` | Base para endeudamiento |
| `patrimonio_neto` | Base para rentabilidad + CO del K |
| `ingresos_ordinarios` | Proxy de tamaño/actividad |
| `utilidad_perdida_operacional` | Base para cobertura de intereses |
| `resultado_del_periodo` | Base para rentabilidades |

### Índices calculables (componente CF del K financiero)

| Índice | Fórmula | Relevancia para modelo |
|---|---|---|
| Liquidez | activo_corriente / pasivo_corriente | Capacidad de pago de corto plazo |
| Endeudamiento | pasivo_total / activo_total | Apalancamiento financiero |
| Cobertura de intereses | utilidad_operacional / gastos_intereses | Sostenibilidad financiera |
| Rentabilidad patrimonio | utilidad_neta / patrimonio_neto | Retorno a propietarios |
| Rentabilidad activo | utilidad_neta / activo_total | Eficiencia de activos |

### Limitaciones del RUP

| Factor | Impacto |
|---|---|
| **reCAPTCHA v2 por consulta** | Token de un solo uso — una resolución manual por cada NIT |
| **Cobertura parcial** | No todos los proveedores de `contratosElectronicos` están inscritos en RUP |
| `documento_proveedor = "No Definido"` | ~30% de registros sin NIT válido — no consultables |
| **Dato histórico** | La API devuelve el último año registrado; el RUP se actualiza anualmente |
| **Indices pre-calculados en cero** | `capacidad_organizacional` de la API muestra 0 en muchas empresas; hay que calcular desde los datos crudos |

---

## 5. ¿Qué aporta el K financiero al modelo predictivo?

### Hipótesis de valor

Un proveedor con **baja liquidez** o **alto endeudamiento** tiene mayor probabilidad de:
- Solicitar adiciones de plazo por falta de capital de trabajo
- Incumplir cronograma por problemas de flujo de caja
- Abandonar el contrato (rescisión unilateral)

### Variables derivables del RUP para el modelo

```
Nivel 1 — Features directas (disponibles en RUP):
  • tamano_empresa  →  correlacionado con capacidad de gestión
  • patrimonio_neto  →  CO del K (capacidad organizacional base)
  • es_pyme  →  ya disponible en proveedoresRegistrados

Nivel 2 — Índices financieros calculados (requieren RUP):
  • idx_liquidez
  • idx_endeudamiento
  • idx_cobertura_intereses
  • rent_patrimonio
  • rent_activo

Nivel 3 — K residual (NO disponible automáticamente):
  • Requiere E, CT, CF ponderados por pliego (variables per-proceso)
  • Requiere SCE en tiempo real (contratos activos del proponente al momento de licitar)
  • → Solo estimable con supuestos; no calculable con certeza
```

### Comparación con alternativa disponible

| Feature | Fuente | Disponibilidad | Costo |
|---|---|---|---|
| `es_pyme` | proveedoresRegistrados | Ya en dataset | $0 |
| `codigo_tamano_empresa` | proveedoresRegistrados | Ya en dataset | $0 |
| Índices financieros RUP | RUP API | Extracción semiautomática | Tiempo humano (CAPTCHA) |
| K residual | Cálculo por proceso | No disponible | No viable |

---

## 6. Recomendación al director del proyecto

### Sobre el K residual

> **No incluir el K residual como variable del modelo.** Es un número dinámico calculado per-proceso que no existe como dato almacenado en ninguna fuente pública. Intentar reconstruirlo requeriría parsear PDFs heterogéneos de 51K procesos + datos de contratos en ejecución de cada oferente al momento de licitar — inviable en el marco de este trabajo de grado.

### Sobre los índices financieros del RUP (K financiero)

> **Extracción parcial recomendada.** Priorizar los top-N proveedores por frecuencia de contratos. Con el script `extraer_rup.py` y resolución manual de CAPTCHA, es factible obtener datos financieros para los 200-500 proveedores más activos en obra pública, que representan una fracción desproporcionada del valor total contratado.

```python
# Proveedores únicos válidos en el dataset
df[df['documento_proveedor'] != 'No Definido']['documento_proveedor'].nunique()
# → ~19,000 NITs únicos

# Top 200 proveedores por frecuencia de contratos
conteos = df['documento_proveedor'].value_counts()
top_200 = conteos.head(200)
# → Estrategia pragmática: ~1-2 horas de resolución manual de CAPTCHA
```

### Sobre el poder predictivo esperado

Los índices financieros del RUP son un proxy razonable del riesgo financiero del contratista, pero **no reemplazan** la riqueza predictiva que ya existe en el dataset:

- El historial de `dias_adicionados`, `tipo_modificacion`, y `estado_contrato` del mismo proveedor (feature engineering sobre contratos históricos) probablemente tendrá mayor poder predictivo que los índices RUP.
- Las variables de SECOP II (`plazo_de_ejec_del_contrato`, `valor_del_contrato`, `modalidad_de_contratacion`) son directas y sin costo adicional de extracción.

---

## 7. Próximos pasos sugeridos

1. **Estimar cobertura real del RUP**: ejecutar muestra de 100 NITs frecuentes y medir % de match
2. **Definir N prioritario**: acordar con director cuántos proveedores extraer (100, 200, 500)
3. **Extraer con script**: `python scripts/extraer_rup.py --generar data/contratos_electronicos_obra.parquet --top 200`
4. **Feature engineering de historial**: crear features de comportamiento histórico por proveedor (adiciones previas, proyectos terminados, etc.)
5. **Evaluar importancia**: en el modelo final, comparar feature importance de índices RUP vs features históricas
