# RESUMEN CONTROL — FASE 1 DEL INFORME FINAL DEL COMPANERO

## 0. Metadatos del resumen

- **Archivo fuente analizado:** `report/INFORME-FINAL.md`, limitado explicitamente a: portada/metadatos (lineas 1-11), Resumen ejecutivo (15-50), Introduccion (54-110) y **Seccion 1. Identificacion y extraccion de los datos crudos** (113-282). Las secciones 2 (analisis estadistico/EDA), 3 (modelado predictivo) y 4 (chatbot), asi como las Conclusiones y Anexos, quedan **fuera de alcance** de este resumen por instruccion explicita del usuario ("solo hasta la primera fase").
- **Fecha de generacion:** 2026-07-23
- **Tipo de documento:** Informe final de trabajo dirigido (no es un anteproyecto; es un reporte de cierre de un proyecto ya ejecutado). Autor: Angel Garcia (angeldev07). Codirector declarado en el documento: Nelson Beltran Galvis (C.C. 79.334.324, nelsonbeltran@ufps.edu.co).
- **Nivel de completitud de la Seccion 1:** Alto. Describe con precision las 6 fuentes de datos, la estrategia de extraccion (SoQL, paginacion, lotes, timeouts, scraping RUP, pipeline Docker de pliegos), el esquema relacional con coberturas de join medidas, los hallazgos de calidad de datos y el dataset consolidado final con dimensiones exactas por archivo.
- **Observaciones generales:** Esta seccion corresponde, dentro del esquema de fases del companero (`doc/contexto/tabla_fases_trabajo_dirigido.md`), a la **Fase I: Comprension del Negocio y Estructuracion de Datos**, ejecutada del 16 de febrero al 29 de marzo de 2026 segun esa tabla. Es la unica fase cuyo objeto de trabajo (extraccion e integracion de datos SECOP de obra publica) coincide tematicamente con los objetivos OE-01, OE-02 y OE-03 del anteproyecto de Andres (`InformesRev/AnteproyectoAndres.md`). Las fases posteriores del companero (modelado predictivo, chatbot) no tienen relacion con el alcance descriptivo de Andres y no se analizan aqui.
- **Discrepancia de rol del director detectada:** El documento llama a Nelson Beltran Galvis "**Codirector**" (linea 8), mientras que `InformesRev/AnteproyectoAndres.md` lo llama "**Director**" (sin codirector asignado). Esto sugiere que el companero podria tener un director principal distinto, no nombrado en la porcion analizada. **No verificable con la informacion disponible en Seccion 1** — se marca como pregunta pendiente (seccion 6 de este documento).

---

## 1. Resumen ejecutivo de la Fase 1 (traducido a lenguaje de control)

La Fase 1 del companero documenta la identificacion y extraccion de seis fuentes oficiales de datos SECOP (Contratos Electronicos, Procesos de Contratacion, Adiciones, Proveedores Registrados, Proponentes por Proceso, Registro Unico de Proponentes) mas un septimo insumo propio (pipeline de extraccion de indicadores financieros desde pliegos de condiciones, via scraping + Gemini). Declara una estrategia de extraccion con filtros SoQL, paginacion, descarga por lotes con reintentos, timeouts extendidos y persistencia en Parquet. Establece el esquema relacional entre las seis fuentes, con un hallazgo critico documentado (la llave correcta entre procesos y contratos es `id_del_portafolio`, no `id_del_proceso`, lo que elevo la cobertura del join de 0% a 99.9%). Documenta hallazgos de calidad de datos (sentinelas, duplicados masivos, tipos incorrectos, outliers extremos tratados con winsorizacion p1/p99). Cierra con un inventario de 9 archivos Parquet consolidados y la afirmacion de que 14 variables fueron excluidas por leakage temporal, documentadas en `cols_leakage.txt`.

Esta fase es, en esencia, la misma infraestructura tecnica que documenta `InformesRev/RESUMEN_CODIGO.md` de este repositorio bajo los notebooks `00` a `06` (mas el enriquecimiento RUP del notebook `08` y los scripts de `extractor-indicadores-docker/`), presentada aqui desde la perspectiva narrativa del companero como cumplimiento de su propio OE1 ("Estructurar un proceso de Ingenieria de Datos (ETL)... preparando el dataset para el modelado predictivo").

---

## 2. Objetivo que esta fase declara cumplir (segun el companero)

Segun la Introduccion del informe (lineas 75-78) y `doc/contexto/plan-trabajo-dirigido.md` (ya citado en `MATRIZ_OBJETIVOS_CODIGO.md`, seccion 6.2), esta seccion corresponde al OE1 del companero: *"Estructurar un proceso de Ingenieria de Datos (ETL) que permita la extraccion, limpieza y homologacion semantica de los registros de obras civiles provenientes del SECOP, resolviendo inconsistencias de formato y calidad."*

Este OE1 del companero **no es identico** a ningun OE de Andres, pero se superpone parcialmente en objeto (extraccion e integracion de datos SECOP de obra publica) con OE-01 (extraccion), OE-02 (estructuracion/modelo de datos) y OE-03 (normalizacion) del anteproyecto de Andres. La diferencia de fondo es el proposito declarado: el companero construye este pipeline explicitamente "para el modelado predictivo" (frase literal usada en `doc/contexto/tabla_fases_trabajo_dirigido.md`, fila Fase I), mientras que Andres lo necesita para calcular indicadores descriptivos de tiempo/costo/alcance bajo el marco de restriccion de hierro.

---

## 3. Sintesis de las tablas y hallazgos clave de la Seccion 1

### 3.1 Fuentes de datos (tabla 1.1, linea 126-133)

| Fuente | Dataset ID | Volumen declarado |
|---|---|---|
| Contratos Electronicos | `jbjy-vk9h` | 51.353 registros de obra (87 columnas) |
| Procesos de Contratacion | `p6dx-8zbt` | 138.112 registros (59 columnas) |
| Adiciones contractuales | `cb9c-h8sn` | 249.037 registros (5 columnas) |
| Proveedores Registrados | `qmzu-gj57` | 13.117 proveedores (25 columnas) |
| Proponentes por Proceso | (SECOP II, sin ID citado) | 276.770 registros (9 columnas) |
| Registro Unico de Proponentes (RUP) | Camaras de Comercio (scraping) | 28.548 proveedores (22 columnas) |

Septimo insumo (no es fuente SECOP, es un pipeline propio): indicadores financieros de pliegos de condiciones (6 variables por contrato: indice de liquidez minimo, endeudamiento maximo, razon de cobertura de intereses, rentabilidad minima sobre patrimonio, rentabilidad minima sobre activo, capital de trabajo % presupuesto).

### 3.2 Estrategia de extraccion (1.2, lineas 145-187)

- Filtros SoQL por `tipo_de_contrato = "Obra"` para reducir volumen en origen.
- Paginacion `limit`/`offset` (limite de la API: 50.000 registros/consulta).
- Lotes de 150 IDs con clausula `WHERE IN`, con reintentos y retroceso exponencial.
- Timeout extendido a 120 segundos (default de `sodapy`: 10 segundos).
- Persistencia en Apache Parquet.
- RUP: scraping con Playwright + CapSolver (reCAPTCHA v2), 28.548 proveedores obtenidos.
- Pliegos: pipeline containerizado en Docker, navega el portal SECOP, descarga PDFs, extrae texto, envia a Gemini 2.5 Flash Lite con salida JSON estructurada. Publicado en Docker Hub (`angeldev07/extractor-indicadores-secop:v1.0.0`). Backup horario a Cloudflare R2. Notificaciones push via ntfy.sh. Resultado declarado: 7.994 contratos procesados, 4.276 con los 6 indicadores completos.

### 3.3 Esquema relacional y coberturas de join (1.3, lineas 189-227)

Hallazgo critico declarado: la llave correcta entre `procesosDeContratacion` y `contratosElectronicos` es `id_del_portafolio` (prefijo `CO1.BDOS.`), no `id_del_proceso` (prefijo `CO1.REQ.`) como se asumio inicialmente. Esta correccion elevo la cobertura del join de 0% a 99.9%.

| Relacion | Cobertura declarada |
|---|---|
| Procesos → Contratos | 99,9% |
| Adiciones → Contratos | 69,2% |
| Proveedores Registrados → Contratos | 54,4% |
| RUP → Proveedores Registrados | 63,5% |
| Proponentes → Procesos de Obra | 48,2% |
| Pliego → Contratos | 8,0% global / 36,5% en consorcios |

### 3.4 Hallazgos de calidad de datos (1.4, lineas 229-250)

- Valores sentinela: al menos 8 patrones distintos ("No Definido", "No Provisto", "No Defenido" [error ortografico], cadenas vacias, entre otros no listados explicitamente).
- Duplicados masivos: hasta 96.942 filas identicas en el dataset de adiciones.
- Tipos de datos incorrectos: campos numericos almacenados como texto.
- Outliers extremos: duraciones de hasta 27 millones de dias, precios base de hasta 11 cuatrillones de pesos, tratados con winsorizacion p1/p99.

### 3.5 Dataset analitico consolidado (1.5, lineas 252-281)

| Archivo | Dimensiones | Rol declarado |
|---|---|---|
| `contratos_electronicos_obra.parquet` | 51.353 × 87 | Fuente madre cruda |
| `procesos_contratacion_obra.parquet` | 138.112 × 59 | Pre-contrato crudo |
| `adiciones_obra.parquet` | 249.037 × 5 | Modificaciones crudas |
| `proveedores_obra.parquet` | 13.117 × 25 | Proveedores crudos |
| `proveedores_rup.parquet` | 28.548 × 22 | RUP extraido por scraping |
| `proponentes_por_proceso_obra.parquet` | 276.770 × 9 | Oferentes por proceso |
| `contratos_adiciones_obra.parquet` | 48.331 × 125 | Integracion primaria |
| `contratos_depurado_modelo.parquet` | 48.331 × 53 | Dataset depurado para modelado v1 |
| `consolidado_global.parquet` | 48.331 × 55 | Dataset enriquecido para modelado v2 |

Declara ademas: "14 variables identificadas como leakage temporal... documentadas explicitamente en `cols_leakage.txt`", citando como ejemplos `dias_adicionados`, `n_modif_general`, `valor_pagado`, `valor_facturado`, `fecha_fin_contrato`.

---

## 4. Inconsistencias y vacios detectados en la Seccion 1 (control documental, sin cruzar aun contra codigo)

- **Vacio 1:** El documento (linea 11) declara el repositorio como `extraccion-datos/`, mientras que el repositorio real analizado se llama `extraccion-datos-secop2-main`. Posible renombramiento posterior o referencia a un clon/checkout distinto. Impacto bajo, pero debe aclararse si se cita este informe en la tesis de Andres.
- **Vacio 2:** "Proponentes por Proceso" (tabla 1.1) no tiene un Dataset ID de Socrata citado, a diferencia de las otras cinco fuentes SECOP. No se puede verificar contra `dataset.json` sin abrir ese archivo (fuera del alcance de este control documental; se aborda en el archivo de verificacion de codigo).
- **Ambiguedad 1:** El documento afirma "14 variables identificadas como leakage temporal" en `cols_leakage.txt`, pero solo cita 5 ejemplos textualmente y no reproduce la lista completa dentro de la Seccion 1. Esta cifra de "14" debe verificarse directamente contra el archivo real (ver `RESUMEN_CODIGO_FASE1_INFORME_FINAL.md`, seccion 4, donde se documenta una discrepancia significativa).
- **Discrepancia de rol de direccion:** "Codirector" en este documento vs. "Director" (sin codirector) en `AnteproyectoAndres.md`. Sugiere una estructura de direccion distinta entre ambos trabajos que no queda resuelta en la Seccion 1.
- **Vacio 3:** Los "al menos ocho patrones distintos" de valores sentinela solo se listan parcialmente (4 de 8 mencionados explicitamente). No se puede verificar la lista completa de 8 patrones sin auditar el codigo fuente de cada notebook celda por celda (fuera del alcance de este control documental).

---

## 5. Informacion clave para el cruce contra el codigo real

Para verificar esta fase contra el codigo, deben confirmarse:

1. Existencia y contenido real de `cols_leakage.txt` (numero exacto de variables).
2. Existencia real de los 9 archivos Parquet listados en 3.5, con las dimensiones exactamente declaradas.
3. Evidencia en codigo de: filtros SoQL, paginacion `limit`/`offset`, lotes de 150 IDs con `WHERE IN`, timeout de 120s, persistencia en Parquet.
4. Evidencia en codigo del scraping RUP (Playwright + CapSolver) y del pipeline Docker de indicadores de pliegos (Gemini 2.5 Flash Lite, Docker Hub, Cloudflare R2, ntfy.sh).
5. Evidencia en codigo del hallazgo de la llave `id_del_portafolio` vs `id_del_proceso` y de las coberturas de join declaradas.
6. Evidencia en codigo de las tecnicas de tratamiento de calidad de datos (sentinelas, deduplicacion, winsorizacion).

Este cruce se realiza en `RESUMEN_CODIGO_FASE1_INFORME_FINAL.md` dentro de esta misma carpeta.

---

## 6. Preguntas pendientes derivadas de esta fase (relevantes para Andres)

- ¿Quien es el director principal del companero, si Nelson Beltran Galvis aparece como "Codirector" en este informe? ¿Existe un director distinto no mencionado en la Seccion 1?
- ¿El repositorio `extraccion-datos/` mencionado en la portada es el mismo que `extraccion-datos-secop2-main`, o una version anterior/distinta?
- ¿Los 9 datasets Parquet listados en la seccion 1.5 estan disponibles integros en este repositorio para que Andres los use como insumo (previa autorizacion), o deben regenerarse?
- ¿El pipeline de extraccion de indicadores de pliegos (RUP financiero) tiene algun valor para el alcance descriptivo de Andres, dado que su anteproyecto no menciona RUP ni pliegos en absoluto?
- ¿El hallazgo de la llave correcta `id_del_portafolio` y las coberturas de join medidas pueden citarse directamente por Andres como antecedente tecnico documentado, sin necesidad de re-descubrirlas el mismo?

Estas preguntas se retoman con recomendaciones concretas en `MATRIZ_APROVECHAMIENTO_FASE1.md`.
