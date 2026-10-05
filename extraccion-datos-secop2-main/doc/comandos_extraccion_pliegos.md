# Guía de comandos — Extracción de indicadores de pliegos

Workflow completo para procesar pliegos de condiciones de SECOP II y extraer los
6 indicadores habilitantes (liquidez, endeudamiento, cobertura, ROE, ROA, capital
de trabajo) usando Gemini.

> **Prerrequisitos**: `.env` con `GEMINI_API_KEY` y `CAPSOLVER_API_KEY`.
> Ejecutar siempre desde la raíz del proyecto: `extraccion-datos/`.

---

## 🗂️ Los tres scripts

| Script | Propósito | Modo |
|---|---|---|
| [`descargar_pliego.py`](../scripts/gemini/descargar_pliego.py) | Descargar PDFs de SECOP II | Interactivo |
| [`extraer_indicadores_gemini.py`](../scripts/gemini/extraer_indicadores_gemini.py) | Extraer indicadores 1 a 1 (síncrono) | Inmediato |
| [`extraer_indicadores_gemini_batch.py`](../scripts/gemini/extraer_indicadores_gemini_batch.py) | Extraer indicadores en lote (async) | Diferido, más barato |

---

## ⚡ Flujos comunes

### A) Flujo rápido (pocos contratos, ver resultado inmediato)

```bash
# 1. Descargar algunos PDFs
.venv/Scripts/python scripts/gemini/descargar_pliego.py

# 2. Extraer indicadores síncrono
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini.py --n 10
```

### B) Flujo masivo (cientos/miles, modo batch)

```bash
# 1. Descargar muchos PDFs (autoselección, sin supervisión)
.venv/Scripts/python scripts/gemini/descargar_pliego.py
# Dentro: da 1-50  (auto-descarga 50 sin preguntar)

# 2. Enviar batch de extracción
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py submit --n 400

# 3. Esperar y chequear
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py status

# 4. Cuando diga SUCCEEDED, recolectar
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py collect
```

---

## 📥 `descargar_pliego.py` — Descargador interactivo

### Abrir

```bash
.venv/Scripts/python scripts/gemini/descargar_pliego.py
.venv/Scripts/python scripts/gemini/descargar_pliego.py --page-size 30
```

### Comandos dentro del menú

| Comando | Qué hace |
|---|---|
| `l` / `list` | Listar candidatos de la página actual |
| `n` / `next` | Siguiente página |
| `p` / `prev` | Página anterior |
| `f <campo>=<valor>` | Filtrar (campos: `entidad`, `depto`, `proveedor`, `id`). Ej: `f entidad=INVIAS` |
| `c` / `clear` | Limpiar todos los filtros |
| `s` / `stats` | Estadísticas del conjunto filtrado (top entidades/departamentos) |
| `show <índice>` | Ver detalles completos de un candidato |
| `d <selección>` | **Descarga INTERACTIVA**: lista los documentos del contrato y te deja elegir manualmente (o Enter para usar la heurística) |
| `da <selección>` | **Descarga AUTO**: usa la heurística sin preguntar (útil para batches grandes) |
| `h` / `help` | Ayuda del menú |
| `q` / `quit` | Salir |

### Sintaxis de selección

```
d 1           # descargar el #1 de la tabla
d 1-5         # del 1 al 5
d 1,3,7       # los tres
d 1-5,8,10    # combinaciones
```

### Ejemplo de sesión

```
> f entidad=INVIAS
  filtros activos: entidad=INVIAS  →  406 candidatos

> d 1-3
Vas a descargar 3 PDF(s) en modo INTERACTIVO (eliges el doc):
  CO1.PCCNTR.1003010   INVIAS
  CO1.PCCNTR.1005023   INVIAS
  CO1.PCCNTR.1006217   INVIAS
confirmar? [s/N]: s

  [1/3] CO1.PCCNTR.1003010
    4 documentos disponibles:
      1  1. INVITACION PUBLICA IP-DT-BOY-011-2019.pdf ← recomendado
      2  2. ESTUDIOS PREVIOS.pdf
      ...
    Elegir # [Enter=1 (nivel 2), s=saltar]: [Enter]
    OK — 657.5 KB -> CO1.PCCNTR.1003010.pdf
```

---

## 🚀 `extraer_indicadores_gemini.py` — Extracción síncrona

Procesa los PDFs uno a uno, resultados en vivo. Úsalo para volúmenes chicos o testing.

### Uso básico

```bash
# Procesar 10 contratos pendientes (default cooldown 1.0s)
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini.py --n 10

# Ir más rápido (cooldown más corto)
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini.py --n 50 --cooldown 0.5

# Cambiar de modelo (p. ej. gemini-2.0-flash-lite o 3.1-preview)
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini.py --n 20 --modelo gemini-2.0-flash-lite

# Reintentar contratos con estado sin_match (usa fallback de texto completo)
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini.py --n 30 --retry-sin-match
```

### Argumentos

| Flag | Default | Descripción |
|---|---|---|
| `--n N` | `5` | Máximo de contratos a procesar en esta corrida |
| `--cooldown S` | `1.0` | Segundos entre llamadas (Tier 1 soporta hasta ~0.015s) |
| `--modelo M` | `gemini-2.5-flash-lite` | Model ID de Gemini |
| `--retry-sin-match` | `False` | Reincluye contratos con estado `sin_match` (el fallback de texto completo intentará de nuevo) |

### Qué hace por dentro

Para cada contrato pendiente:
1. Abre el PDF con `pdfplumber`
2. Detecta la tabla de contenido (TOC) y la excluye
3. Busca páginas con keywords (`liquidez`, `endeudamiento`, `habilita`, etc.) y elige el cluster más denso
4. Si no encuentra match → **fallback**: todo el texto compactado (quita headers/footers, TOC, whitespace)
5. Envía a Gemini con schema JSON estructurado (temperatura 0)
6. Parsea los 6 indicadores
7. Guarda incremental en [`data/indicadores_pliegos_extraidos.json`](../data/indicadores_pliegos_extraidos.json)
8. Al final actualiza **ambos parquets** (`contratos_adiciones_obra.parquet` y `contratos_depurado_modelo.parquet`)

### Estados posibles del contrato

| Estado | Reintenta? | Significado |
|---|---|---|
| `ok` | No | Extrajo ≥1 indicador correctamente |
| `texto_sin_umbrales` | No | Gemini leyó el texto pero no encontró umbrales válidos |
| `sin_match` | No* | El filtro no encontró páginas; el fallback tampoco dio texto |
| `error_pdf` | No | PDF escaneado / corrupto (necesita OCR) |
| `error_api` | **Sí** | Error transitorio (5xx, ResourceExhausted, timeout) |
| `error_api_permanente` | No | Error 4xx (API mal usada, request inválido) |
| `error_parse` | **Sí** | Gemini devolvió JSON mal formado |
| `no_descargado` | - | Contrato sin PDF en carpeta |
| `no_pdf` | - | Archivo encontrado no es PDF |

\* `sin_match` se reintenta si pasas `--retry-sin-match`.

---

## 📦 `extraer_indicadores_gemini_batch.py` — Batch API (async)

Envía cientos/miles de PDFs en un solo job asíncrono. Tarda minutos a horas pero:
- ~50% más barato
- Aprovecha la cola de 10M tokens de Tier 1
- No consume tu rate limit síncrono

### Subcomandos

#### `submit` — enviar un nuevo batch

```bash
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py submit --n 400
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py submit --n 100 --modelo gemini-2.0-flash-lite
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py submit --n 50 --retry-sin-match
```

| Flag | Default | Descripción |
|---|---|---|
| `--n N` | `100` | Cuántos PDFs meter en el batch (máximo recomendado: 400) |
| `--modelo M` | `gemini-2.5-flash-lite` | Modelo |
| `--retry-sin-match` | `False` | Incluir contratos `sin_match` |

Qué pasa internamente:
1. Busca pendientes (ignora los que ya están en otros batches activos para evitar duplicados)
2. Extrae texto de cada PDF (paso lento)
3. PDFs escaneados / sin texto → se marcan `error_pdf` / `sin_match` **directamente** en el JSON (no gastan tokens)
4. Resto → arma JSONL, sube a Files API, crea el batch job
5. Registra el job en [`data/batch_jobs.json`](../data/batch_jobs.json)

#### `status` — ver progreso de los batches

```bash
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py status
```

Salida:
```
  #  display_name                n  estado      fase            stats
  1  pliegos_20260422_100642     4  COLLECTED   —               —
  2  pliegos_20260422_112520    73  RUNNING     corriendo 12m   45 ok / 2 err
```

Estados:
- `PENDING`: en cola (aún no arrancó)
- `RUNNING`: procesando
- `SUCCEEDED`: listo → correr `collect`
- `FAILED`: falló (ver el error)
- `COLLECTED`: ya se descargaron los resultados
- `CANCELLED`: cancelado

> ⚠️ **Google no expone progreso en %.** Los `completion_stats` solo aparecen al finalizar.

#### `collect` — descargar resultados

```bash
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py collect
```

Para cada batch en `SUCCEEDED`:
1. Descarga el archivo de resultados
2. Parsea cada respuesta JSON
3. Mergea al `indicadores_pliegos_extraidos.json`
4. Re-genera los parquets con todos los `ok` acumulados

Es idempotente — si corres varias veces seguidas solo procesa los nuevos.

#### `list-all` — ver todos los batches en Google

```bash
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py list-all
```

Lista TODOS los batches del proyecto en Google (aunque no los hayas creado con este script).

#### `list-files` — ver archivos JSONL subidos

```bash
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py list-files
```

Lista los archivos subidos a Files API (input JSONL + output JSONL de cada batch).

#### `clean-files` — borrar archivos viejos

```bash
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py clean-files
```

Borra todos los JSONL cuyos nombres empiecen con `batch_pliegos_*`. Útil si te acercas al límite de 20 GB de Files API.

#### `cancel` — cancelar un batch en curso

```bash
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini_batch.py cancel pliegos_20260422_112520
```

---

## 🔍 `inspeccionar_prompt.py` — Ver qué le llega a Gemini

Útil para debugging: muestra el prompt exacto que se enviaría (sin consumir cuota).

```bash
# Ver el prompt completo (instrucciones + texto filtrado)
.venv/Scripts/python scripts/gemini/inspeccionar_prompt.py CO1.PCCNTR.1005228

# Ver solo el texto filtrado del PDF
.venv/Scripts/python scripts/gemini/inspeccionar_prompt.py CO1.PCCNTR.1005228 --solo-texto

# Guardar a disco para inspeccionar con editor
.venv/Scripts/python scripts/gemini/inspeccionar_prompt.py CO1.PCCNTR.1005228 --guardar
```

Los prompts guardados van a [`data/prompts_inspeccion/`](../data/prompts_inspeccion/).

---

## 🗄️ Archivos generados

| Archivo | Qué contiene |
|---|---|
| `data/indicadores_pliegos_extraidos.json` | **Registro maestro**: todos los resultados (ok, errors, estados) — idempotente |
| `data/batch_jobs.json` | Registro local de batches enviados (job_name, ids, meta) |
| `data/contratos_adiciones_obra.parquet` | Dataset completo con `pliego_*` merged |
| `data/contratos_depurado_modelo.parquet` | Dataset depurado con `pliego_*` merged |
| `secop-scraper/storage/pliegos/*.pdf` | PDFs descargados (naming: `{id_contrato}.pdf`) |

---

## 🚨 Troubleshooting

### "ERROR: falta GEMINI_API_KEY en .env"
Asegúrate de tener el `.env` en la raíz con:
```
GEMINI_API_KEY=AIza...
CAPSOLVER_API_KEY=CAP-...
```

### El descargador no encuentra "pliego" en los documentos
La heurística busca en este orden:
1. "pliego de condiciones definitivo"
2. "invitacion publica" (INVIAS)
3. "pliego" (cualquier mención)
4. "condiciones definitivas" / "bases definitivas"
5. "términos de referencia"
6. "proyecto de pliego" (borrador, último recurso)

Si ninguno matchea, **usa el modo interactivo (`d` en vez de `da`)** para elegir manualmente el documento correcto.

### El batch lleva horas en PENDING
Normal. Los batches de Gemini pueden esperar desde minutos hasta 24h en cola. No hay forma de acelerar. Si necesitas urgencia → `extraer_indicadores_gemini.py` síncrono.

### Muchos `error_api` en el JSON
Se reintentan solos en la siguiente corrida. No hagas nada, solo vuelve a correr:
```bash
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini.py --n 50
```

### PDFs "escaneados" (sin texto)
Marcados como `error_pdf`. No se resuelven sin OCR — sáltalos por ahora.

### Necesito reintentar los `sin_match` con el fallback
```bash
.venv/Scripts/python scripts/gemini/extraer_indicadores_gemini.py --n 50 --retry-sin-match
```

---

## 📊 Límites Tier 1 (Google AI Studio)

| Modelo | RPM | TPM | RPD |
|---|---|---|---|
| gemini-2.5-flash-lite | 4,000 | 4M | **ilimitado** |
| gemini-2.0-flash-lite | 4,000 | 4M | ilimitado |
| gemini-2.0-flash | 2,000 | 4M | ilimitado |
| gemini-3.1-flash-lite-preview | 4,000 | 4M | 150k |

**Batch API** (tokens en cola por modelo):
| Modelo | Tokens en cola |
|---|---|
| gemini-2.5-flash-lite | 10M |
| gemini-2.0-flash-lite | 10M |
| gemini-3.1-flash-lite-preview | 10M |

---

## 📌 Dashboard web

- **Batches (UI visual)**: https://aistudio.google.com/app/batch-mode
- **API keys y uso**: https://aistudio.google.com/app/apikey
- **Ajustes**: https://aistudio.google.com/app/settings
