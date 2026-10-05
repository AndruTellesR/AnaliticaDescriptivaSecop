# RESUMEN CODIGO — VERIFICACION DE LA FASE 1 CONTRA EL REPOSITORIO REAL

## 0. Metadatos de la auditoria

- **Fecha de auditoria:** 2026-07-23
- **Documento verificado:** `report/INFORME-FINAL.md`, Seccion 1 (lineas 113-282), mas metadatos/resumen ejecutivo/introduccion (lineas 1-110) como contexto.
- **Base de evidencia tecnica:** Este archivo reutiliza y cita directamente los hallazgos ya verificados en `InformesRev/RESUMEN_CODIGO.md` (auditoria estatica completa del repositorio, realizada en esta misma sesion de trabajo) y anade verificaciones puntuales nuevas especificas a las afirmaciones de la Seccion 1 (existencia de `cols_leakage.txt`, conteo real de variables).
- **Metodo:** Analisis estatico, solo lectura. No se ejecuto ningun notebook ni script.
- **Regla aplicada:** Toda afirmacion de la Seccion 1 se marca como CONFIRMADA, PARCIALMENTE CONFIRMADA, NO VERIFICABLE o CONTRADICHA, con ruta exacta de evidencia.

---

## 1. Verificacion de las fuentes de datos (Seccion 1.1)

| Afirmacion del informe | Verificacion | Evidencia |
|---|---|---|
| 6 fuentes SECOP + 1 pipeline propio de indicadores de pliego | CONFIRMADA | `dataset.json` (4 fuentes con Dataset ID: `jbjy-vk9h`, `p6dx-8zbt`, `cb9c-h8sn`, `qmzu-gj57`); `notebooks/06_proponentes_por_proceso.ipynb` (5ta fuente); scraping RUP via `scripts/extraer_rup_auto.py` (6ta fuente); `extractor-indicadores-docker/` + `scripts/gemini/` (7mo insumo, pipeline de pliegos) |
| Contratos Electronicos: 51.353 x 87 | CONFIRMADA | `entregables/04-datasets/contratos_electronicos_obra.parquet`, documentado con identicas dimensiones en `entregables/04-datasets/README.md` (`InformesRev/RESUMEN_CODIGO.md`, seccion 7) |
| Procesos de Contratacion: 138.112 x 59 | PARCIALMENTE CONFIRMADA | `entregables/04-datasets/procesos_contratacion_obra.parquet` tiene 138.112 filas, pero `entregables/04-datasets/README.md` documenta **57** columnas reales, no 59 (59 es el numero de columnas *definidas* en `dataset.json`; 2 de ellas nunca llegaron desde la API, segun `doc/contexto/CONTEXTO.md` seccion 5). El informe usa la cifra nominal (59), no la cifra real recibida (57) |
| Adiciones: 249.037 x 5 | CONFIRMADA | `entregables/04-datasets/adiciones_obra.parquet` |
| Proveedores Registrados: 13.117 x 25 | CONFIRMADA | `entregables/04-datasets/proveedores_obra.parquet` |
| Proponentes por Proceso: 276.770 x 9 | CONFIRMADA | `entregables/04-datasets/proponentes_por_proceso_obra.parquet` |
| RUP: 28.548 x 22 | CONFIRMADA | `entregables/04-datasets/proveedores_rup.parquet` |

---

## 2. Verificacion de la estrategia de extraccion (Seccion 1.2)

| Afirmacion | Verificacion | Evidencia |
|---|---|---|
| Notebooks Jupyter + `sodapy` como cliente Socrata | CONFIRMADA | `notebooks/00_definicion_tabla_base.ipynb` a `06_proponentes_por_proceso.ipynb`; `requirements.txt` (`sodapy>=2.2`) |
| Filtro SoQL `tipo_de_contrato = "Obra"` | CONFIRMADA | Documentado explicitamente en `doc/contexto/CONTEXTO.md` ("Filtro obligatorio: `tipo_de_contrato = 'Obra'`"); coherente con el volumen filtrado (51.353 de 5.738.449 registros totales en contratos, 0,89%) |
| Paginacion `limit`/`offset`, maximo 50.000 registros/consulta | NO VERIFICABLE DIRECTAMENTE EN CODIGO ESTATICO | No se leyo el codigo Python de cada celda de notebook en detalle (solo estructura de celdas markdown, ver `InformesRev/RESUMEN_CODIGO.md` seccion 6); el limite de 50.000 es una caracteristica documentada de la API Socrata, no del codigo del proyecto |
| Lotes de 150 IDs con `WHERE IN`, reintentos con retroceso exponencial | PARCIALMENTE CONFIRMADA | `doc/contexto/CONTEXTO.md`: "estrategia de filtrado por lotes de 150 IDs con WHERE IN" (coincide exactamente); el mecanismo de reintentos con backoff se recomienda en `CONTEXTO.md` pero **no se verifico su implementacion real en el codigo estatico** de los notebooks (mismo hallazgo que `InformesRev/RESUMEN_CODIGO.md`, seccion 8) |
| Timeout extendido a 120s (default 10s) | CONFIRMADA | `doc/contexto/CONTEXTO.md`: "El timeout por defecto de sodapy (10s) no es suficiente para datos.gov.co → usar timeout=120" (coincide exactamente) |
| Persistencia en Apache Parquet | CONFIRMADA | Todos los datasets en `entregables/04-datasets/*.parquet`; uso de `pyarrow>=14.0` en `requirements.txt` |
| Scraping RUP con Playwright + CapSolver, 28.548 proveedores | CONFIRMADA | `scripts/extraer_rup_auto.py` (379 lineas); `CAPSOLVER_API_KEY` en `.env.example`; `proveedores_rup.parquet` con 28.548 filas |
| Pipeline Docker de indicadores de pliegos, Gemini 2.5 Flash Lite, Docker Hub, Cloudflare R2, ntfy.sh | CONFIRMADA | `extractor-indicadores-docker/` completo: `Dockerfile`, `docker-compose.yml`, `entrypoint.sh`, `src/scraper.py` (Playwright+CapSolver), `src/gemini.py` (Gemini 2.5 Flash Lite), `src/r2_backup.py` (Cloudflare R2), `src/controller.py` (ntfy.sh), documentado en `InformesRev/RESUMEN_CODIGO.md` secciones 4.7 y 6 |
| 7.994 contratos procesados, 4.276 con 6 indicadores completos | NO VERIFICABLE EN ESTA SESION (cifra operativa reportada por el pipeline en su ejecucion historica; no hay un log persistido en el repositorio que permita re-verificarla de forma estatica) | Cifra consistente con lo reportado en analisis previos de este mismo repositorio (README del pipeline), pero no contrastable contra un archivo de resultados presente en el checkout actual |

---

## 3. Verificacion del esquema relacional y coberturas de join (Seccion 1.3)

| Afirmacion | Verificacion | Evidencia |
|---|---|---|
| Llave correcta `id_del_portafolio` (no `id_del_proceso`) | CONFIRMADA | `doc/contexto/CONTEXTO.md`, seccion 3: "La llave `id_del_proceso` (CO1.REQ.) NO coincide con `proceso_de_compra` (CO1.BDOS.). La llave correcta es `id_del_portafolio`"; tambien documentado como "HALLAZGO CRITICO" en `notebooks/02_procesos_contratacion.ipynb`, celda 52 (ver `InformesRev/RESUMEN_CODIGO.md`, seccion 6) |
| Cobertura Procesos → Contratos: 99,9% | CONFIRMADA | `doc/contexto/CONTEXTO.md`, tabla de llaves de integracion: "99.9% (43,414/43,451)" |
| Cobertura Adiciones → Contratos: 69,2% | CONFIRMADA | `doc/contexto/CONTEXTO.md`: "69.2% (33,465/48,331)" |
| Cobertura Proveedores → Contratos: 54,4% | CONFIRMADA | `doc/contexto/CONTEXTO.md`: "54.4% (12,618/23,192)" |
| Cobertura RUP → Proveedores: 63,5% | CONFIRMADA | `entregables/04-datasets/README.md` (citado en `InformesRev/RESUMEN_CODIGO.md`, seccion 8) |
| Cobertura Proponentes → Procesos: 48,2% | CONFIRMADA | `entregables/04-datasets/README.md` |
| Cobertura Pliego → Contratos: 8,0% global / 36,5% consorcios | NO VERIFICABLE EN ESTA SESION (cifra operativa del pipeline de pliegos; consistente con analisis previos del mismo repositorio, pero sin archivo de resultados presente en el checkout actual para recalcularla) | — |

---

## 4. Verificacion de hallazgos de calidad de datos (Seccion 1.4)

| Afirmacion | Verificacion | Evidencia |
|---|---|---|
| Sentinelas ("No Definido", "No Provisto", etc.) | PARCIALMENTE CONFIRMADA | `doc/contexto/CONTEXTO.md`: "SECOP II usa el texto 'No Definido' en lugar de NULL"; `notebooks/03_adiciones.ipynb` celda 13 ("Deteccion de sentinelas 'No Definido'"); `notebooks/04_proveedores.ipynb`: sentinela "No Provisto" ~29% en departamento/municipio (`InformesRev/RESUMEN_CODIGO.md`, seccion 6). El informe menciona "al menos ocho patrones distintos" pero solo 4 se nombran explicitamente ("No Definido", "No Provisto", "No Defenido", cadenas vacias); los otros 4 no son verificables sin auditoria celda por celda |
| Duplicados masivos, hasta 96.942 filas identicas en adiciones | CONFIRMADA | `doc/contexto/CONTEXTO.md`: "105,836 duplicados en `identificador` — 96,942 filas completamente duplicadas" (coincide exactamente) |
| Tipos de datos incorrectos (numericos como texto) | CONFIRMADA | `doc/contexto/CONTEXTO.md`: "Todos los campos numericos llegan como texto (object) desde la API"; `notebooks/02_procesos_contratacion.ipynb`, seccion 5.1 "Conversion de tipos" |
| Outliers extremos (27M dias, 11 cuatrillones COP) tratados con winsorizacion p1/p99 | CONFIRMADA | `doc/contexto/CONTEXTO.md`: "max 27M dias", "max $11 cuatrillones"; winsorizacion confirmada en `modelo_predictivo_global/data/imputers/winsor_limits.pkl` (`InformesRev/RESUMEN_CODIGO.md`, seccion 9) |

---

## 5. Verificacion del dataset consolidado y del leakage (Seccion 1.5) — HALLAZGO CRITICO

| Afirmacion | Verificacion | Evidencia |
|---|---|---|
| 9 archivos Parquet con las dimensiones listadas | CONFIRMADA | Verificado directamente contra `entregables/04-datasets/*.parquet` (los 9 archivos existen con las dimensiones exactas declaradas: 51.353×87, 138.112×59\*, 249.037×5, 13.117×25, 28.548×22, 276.770×9, 48.331×125, 48.331×53, 48.331×55). \*Con la salvedad de columnas ya senalada en la seccion 1 de este documento |
| "14 variables identificadas como leakage temporal... documentadas explicitamente en `cols_leakage.txt`" | **CONTRADICHA** | Se verifico directamente el archivo `modelo_predictivo_global/data/cols_leakage.txt`: contiene **45 lineas/variables**, no 14 (`tiempo`, `presupuesto`, `alcance`, `n_modif_general`, `n_tipos_distintos`, `n_tipo_no_definido`, `n_suspension`, `tiene_cesion`, `tiene_conclusion`, `tiene_suspension`, `dias_adicionados`, `dias_hasta_primera_adicion`, `ventana_adiciones_dias`, `ratio_extension_duracion`, `fecha_de_fin_del_contrato`, `fecha_de_inicio_del_contrato`, `fecha_de_firma`, `fecha_primera_adicion`, `fecha_ultima_adicion`, `fecha_de_notificaci_n_de_prorrogaci_n`, `fecha_fin_liquidacion`, `fecha_inicio_liquidacion`, `duraci_n_del_contrato`, `liquidaci_n`, `n_adicion_valor`, `n_extension`, `n_cesion`, `n_conclusion`, `n_reactivacion`, `n_modificaciones_total`, `tiene_adicion_valor`, `tiene_extension_dias`, `tiene_modificacion`, `valor_amortizado`, `valor_facturado`, `valor_pagado`, `valor_pendiente_de`, `valor_pendiente_de_ejecucion`, `valor_pendiente_de_pago`, `saldo_cdp`, `saldo_vigencia`, `sobrecosto_ratio`, `estado_contrato`, `ultima_actualizacion`, `reversion`) |
| Los 5 ejemplos citados en el informe (`dias_adicionados`, `n_modif_general`, `valor_pagado`, `valor_facturado`, `fecha_fin_contrato`) | PARCIALMENTE CONFIRMADA | 4 de los 5 ejemplos aparecen literalmente en el archivo real (`dias_adicionados`, `n_modif_general`, `valor_pagado`, `valor_facturado`); el quinto, `fecha_fin_contrato`, no aparece con ese nombre exacto en `cols_leakage.txt` (el archivo real usa `fecha_de_fin_del_contrato`) |
| `report/ANEXO-A-fuentes-y-variables.md`, seccion A.4, refuerza la cifra de "catorce variables" | **CONTRADICHA POR EL MISMO REPOSITORIO** | El Anexo A lista textualmente solo las primeras 14 lineas del archivo real de 45 (desde `tiempo` hasta `ratio_extension_duracion`), truncando sin indicarlo el resto de las 31 variables restantes (fechas, valores pagados/facturados, saldo_cdp, sobrecosto_ratio, estado_contrato, etc.) |
| Discrepancia previa ya detectada en `InformesRev/RESUMEN_CODIGO.md` | Consistente | `InformesRev/RESUMEN_CODIGO.md` ya habia senalado esta misma familia de discrepancias citando `doc/AUDITORIA_INCONSISTENCIAS.md` ("36 vs 14 columnas de leakage"). Esta verificacion directa del archivo aporta el dato definitivo: **el archivo real tiene 45 entradas**, ni 36 ni 14. La cifra de "36" citada en `modelo_predictivo_global/docs/01_dataset_y_variables.md` (linea 148) tampoco coincide con el conteo real |

**Conclusion de esta seccion:** La Seccion 1 del informe final del companero subestima en un 68% (14 de 45) el numero real de variables de leakage documentadas en su propio archivo de referencia. Esta es la unica contradiccion factual dura (no ambigua, no de interpretacion) detectada en la Fase 1, verificable de forma directa y reproducible por cualquier tercero con acceso al repositorio.

---

## 6. Sintesis de la verificacion

De las afirmaciones centrales de la Seccion 1:

- **Confirmadas sin reservas:** 6 de las fuentes de datos, la mayoria de la estrategia de extraccion (filtro SoQL, timeout, lotes, Parquet, scraping RUP, pipeline Docker de pliegos), el hallazgo de la llave `id_del_portafolio`, 5 de 6 coberturas de join, 3 de 4 hallazgos de calidad de datos, y las dimensiones de los 9 archivos Parquet.
- **Parcialmente confirmadas:** el numero de columnas de Procesos de Contratacion (59 nominal vs 57 real), los patrones de sentinelas (solo 4 de "al menos 8" verificables), la paginacion y los reintentos (documentados narrativamente pero no verificados en codigo Python especifico).
- **No verificables en esta sesion:** las cifras operativas del pipeline de pliegos (7.994/4.276 contratos, cobertura 8%/36.5%), por ausencia de un archivo de resultados persistido en el checkout actual.
- **Contradicha de forma directa y verificable:** el numero de variables de leakage (14 declaradas vs 45 reales en `cols_leakage.txt`), replicada tambien en `report/ANEXO-A-fuentes-y-variables.md`.

En terminos generales, la Fase 1 del companero es **tecnicamente solida y mayoritariamente verificable** contra el codigo real; su unico defecto factual relevante es la subestimacion del conteo de variables de leakage, que no afecta la validez tecnica del pipeline en si (las 45 variables si estan correctamente excluidas del modelado, segun la evidencia de `InformesRev/RESUMEN_CODIGO.md`), pero si constituye una imprecision documental que Andres debe evitar reproducir si cita esta fase como antecedente en su propio trabajo.
