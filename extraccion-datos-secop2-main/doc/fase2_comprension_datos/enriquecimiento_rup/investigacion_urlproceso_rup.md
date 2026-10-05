# Investigación: urlproceso + API RUP-SECOP

## Contexto
El director de proyecto solicitó explorar si la columna `urlproceso` (presente en `contratosElectronicos` y `procesosDeContratacion`) permite extraer el **K financiero** de los proveedores que concursan por contratos de obra pública.

---

## 1. ¿Qué es `urlproceso`?

Todas las URLs tienen el formato:
```
https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.XXXXXXX
```
- 51,353 registros con URL en `contratosElectronicos_obra.parquet`
- Apuntan al portal público SECOP II Community (Colombia Compra Eficiente)

---

## 2. Contenido de la página de proceso

La página del proceso contiene las secciones:

| Sección | Contenido relevante |
|---|---|
| Información | Precio estimado, número proceso, estado |
| Datos del contrato | Tipo, modalidad, duración, UNSPSC |
| Configuración financiera | Requisitos de garantías (% del contrato) |
| **Lista de respuesta de proveedores** | Oferentes, posición, fecha, documentos oferta |
| **Información de la selección** | Informe de evaluación (PDF), adjudicatario |
| Documentación | Pliegos, estudios previos (PDFs) |

### Hallazgo clave: el K financiero NO está en campos estructurados
Está dentro del **Informe de Evaluación** (PDF), descargable desde:
```
GET /Public/Tendering/OpportunityDetail/DownloadDocumentReport?documentId=XXX&mkey=YYY
```

---

## 3. Barreras de `urlproceso` (scraping directo)

| Barrera | Severidad |
|---|---|
| reCAPTCHA Enterprise por sesión | Alta — no bypasseable automáticamente |
| `mkey` de sesión expira al navegar | Alta — token de un solo uso por sesión |
| K financiero en PDF (no estructurado) | Alta — requiere LLM para extracción |
| 51K URLs a procesar | Muy alto volumen |

**Conclusión: scraping directo de `urlproceso` → NO VIABLE para obtener K financiero.**

---

## 4. Alternativa identificada: API RUP-SECOP

Portal: `https://ruppro.colombiacompra.gov.co/`
API descubierta: `POST https://ruppro.colombiacompra.gov.co/msrup/api/v1/consultas/nit/completo`

### Request
```json
{
  "nit": "830038225",
  "recaptchaToken": "<token_recaptcha_v2>"
}
```

### Response exitosa (VISUAR SAS, NIT 830038225)
```json
{
  "success": true,
  "data": {
    "informacionBasica": {
      "razon_social": "VISUAR S A S",
      "estado_matricula": "ACTIVA",
      "desc_ciiu_act_econ_pri": "Construcción de otras obras de ingeniería civil",
      "numero_empleados": "8",
      "codigo_tamano_empresa": "03",
      "informacionFinanciera": [{
        "ano_informacion_financiera": "2025",
        "activo_corriente": "2736512948",
        "activo_total": "7288252942",
        "pasivo_corriente": "662816950",
        "pasivo_total": "3440565871",
        "patrimonio_neto": "3847687071",
        "ingresos_actividad_ordinaria": "8754686872",
        "utilidad_perdida_operacional": "923210016",
        "resultado_del_periodo": "221963082"
      }]
    },
    "informacionDetalle": {
      "capacidad_organizacional": {
        "indice_liquidez": "...",
        "indice_endeudamiento": "...",
        "razon_cobertura_intereses": "...",
        "rentabilidad_patrimonio": "...",
        "rentabilidad_activo": "..."
      },
      "desc_tamano_empresa": "PEQUEÑA"
    }
  }
}
```

### Variables financieras extraíbles
Con los datos del RUP se pueden calcular los índices del K financiero:
- **Índice de liquidez** = activo_corriente / pasivo_corriente
- **Índice de endeudamiento** = pasivo_total / activo_total
- **Razón cobertura intereses** = utilidad_operacional / gastos_intereses
- **Rentabilidad patrimonio** = utilidad_neta / patrimonio_neto
- **Rentabilidad activo** = utilidad_neta / activo_total

> ⚠️ **Hallazgo importante**: los índices pre-calculados en `capacidad_organizacional`
> aparecen en 0 para muchas empresas (incluida VISUAR SAS), aunque los datos crudos
> en `informacionFinanciera` sí tienen valores reales. Los índices deben calcularse
> manualmente a partir de los valores crudos. El K de contratación (capacidad residual)
> requiere además experiencia y capacidad técnica declarada — puede estar incompleto.

---

## 5. Limitaciones del API RUP

| Factor | Detalle |
|---|---|
| reCAPTCHA v2 por llamada | Token de **un solo uso** — necesario por cada NIT |
| Cobertura del RUP | No todos los proveedores están inscritos |
| `documento_proveedor` | Muchos registros con "No Definido" |
| Enlace NIT | Usar `documento_proveedor`, NO `codigo_proveedor` (es ID interno SECOP) |

---

## 6. Opciones para automatización

### Opción A: Servicio de resolución CAPTCHA (recomendada)
- **2captcha** o **Anti-Captcha**: ~$1-2 por 1,000 tokens
- Integración: Python `requests` + API 2captcha → token → llamada RUP
- Costo estimado: **$20-40 USD** para ~19K NITs únicos válidos (estimado)
- Es práctica aceptada para datos públicos en contextos de investigación

### Opción B: Solicitud de acceso bulk a CCE
- Colombia Compra Eficiente tiene convenios de datos para investigación académica
- Evitaría CAPTCHA completamente

---

## 7. Pasos siguientes recomendados

1. **Estimar cobertura real**: `df[df['documento_proveedor'] != 'No Definido']['documento_proveedor'].nunique()`
2. **Verificar tasa de match con RUP**: tomar muestra de 100 NITs y ver % encontrados
3. **Decidir estrategia**: 2captcha vs solicitud formal a CCE
4. **Implementar**: notebook `06_enriquecimiento_rup.ipynb`

---

## 8. Esquema de integración propuesto

```
contratosElectronicos.documento_proveedor (NIT)
        ↓
API RUP: /msrup/api/v1/consultas/nit/completo
        ↓
informacionFinanciera → activos, pasivos, patrimonio, utilidades
capacidad_organizacional → índices calculados
        ↓
JOIN con dataset principal por NIT
→ Nuevas features: liquidez, endeudamiento, rentabilidad, tamaño_empresa
```
