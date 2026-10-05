# MATRIZ DE APROVECHAMIENTO — FASE 1 DEL COMPANERO PARA EL TRABAJO DE GRADO DE ANDRES

## 0. Metadatos

- **Fecha de generacion:** 2026-07-23
- **Archivos fuente cruzados:**
  - `InformesRev/AnalisisFase1Companero/RESUMEN_CONTROL_FASE1_INFORME_FINAL.md`
  - `InformesRev/AnalisisFase1Companero/RESUMEN_CODIGO_FASE1_INFORME_FINAL.md`
  - `InformesRev/RESUMEN_CONTROL.md` (objetivos de Andres)
  - `InformesRev/RESUMEN_CODIGO.md` (auditoria general de codigo)
  - `MATRIZ_OBJETIVOS_CODIGO.md` (matriz de cumplimiento y reglas de autoria ya establecidas)
- **Alcance de este documento:** unicamente la Fase 1 del companero (Seccion 1 de `report/INFORME-FINAL.md`: identificacion y extraccion de datos crudos). No se analiza aqui el modelado predictivo ni el chatbot del companero (Secciones 2-4), que quedan fuera del interes declarado por Andres para este ejercicio.
- **Proposito:** determinar, objetivo por objetivo, que partes de la Fase 1 del companero pueden servir como insumo, referencia o antecedente tecnico para el trabajo de grado de Andres, y bajo que condiciones.
- **Diferencia con `MATRIZ_OBJETIVOS_CODIGO.md`:** aquel documento evalua **cumplimiento** de los objetivos de Andres contra el codigo existente. Este documento evalua **aprovechamiento**: que tanto del trabajo ya documentado por el companero en su Fase 1 le ahorra esfuerzo a Andres, siempre que se resuelva la autoria y se mantenga el deslinde ya establecido.

---

## 1. Resumen ejecutivo

La Fase 1 del companero (`report/INFORME-FINAL.md`, Seccion 1) documenta con alto nivel de detalle y trazabilidad la misma infraestructura tecnica que ya fue auditada en `InformesRev/RESUMEN_CODIGO.md`: extraccion via API Socrata/OData de seis fuentes SECOP, resolucion de la llave de integracion `id_del_portafolio`, tratamiento de calidad de datos y consolidacion en Parquet. Esta fase es tecnicamente solida y en su mayoria verificable (`RESUMEN_CODIGO_FASE1_INFORME_FINAL.md`), con una unica contradiccion factual relevante: el conteo de variables de leakage (14 declaradas vs 45 reales).

Para Andres, esta fase es de **alto valor como antecedente tecnico y como posible insumo compartido** para OE-01 (extraccion), OE-02 (estructuracion) y OE-03 (normalizacion), bajo la condicion estricta de que el director confirme formalmente el estatus de autoria compartida del pipeline base (notebooks 00-06), tal como ya se establecio en `MATRIZ_OBJETIVOS_CODIGO.md`. Ningun elemento de esta fase sirve a OE-04 (dashboard), que no se trata en la Seccion 1.

El aporte mas citable sin ambiguedad de autoria es el **hallazgo documentado de la llave de integracion correcta** (`id_del_portafolio` vs `id_del_proceso`) y las **coberturas de join medidas**, dado que son hechos tecnicos sobre la estructura de los datos SECOP, no codigo ni texto propio del companero, y por tanto pueden citarse como antecedente de literatura tecnica/documental en la tesis de Andres, con atribucion explicita.

---

## 2. Tabla maestra de aprovechamiento

| OE de Andres | Elemento de la Fase 1 del companero | Aprovechable | Condicion de uso | Autoria | Recomendacion |
|---|---|---|---|---|---|
| OE-01 (Extraccion) | Estrategia de extraccion (SoQL, paginacion, lotes de 150 IDs, timeout 120s, persistencia Parquet) | Si, como referencia tecnica y posible base de codigo | Confirmar autoria del pipeline base con el director antes de reutilizar el codigo | AUTORIA A CONFIRMAR CON DIRECTOR | Citar como antecedente tecnico; reutilizar el codigo solo si se confirma coautoria |
| OE-01 (Extraccion) | 6 fuentes de datos identificadas (Dataset IDs Socrata) | Si, directamente | Los Dataset IDs son informacion publica de datos.gov.co, no autoria de nadie | INSUMO EXTERNO (publico) | Reutilizar libremente, citando `dataset.json` y el portal oficial |
| OE-01 (Extraccion) | Pipeline de indicadores financieros de pliegos (scraping + Gemini + Docker) | No aplica al alcance de Andres | El anteproyecto de Andres no contempla RUP ni pliegos | CODIGO DEL COMPANERO - EXCLUIR | No usar; fuera del alcance declarado |
| OE-02 (Estructuracion) | Esquema relacional entre las 6 fuentes + hallazgo de la llave `id_del_portafolio` | Si, como hecho tecnico documentado | Ninguna — es un hallazgo sobre la estructura publica de los datos SECOP | INSUMO EXTERNO (hallazgo tecnico, citable) | Citar directamente con atribucion al trabajo del companero como antecedente |
| OE-02 (Estructuracion) | Coberturas de join medidas (99.9%, 69.2%, 54.4%, etc.) | Si, como referencia, con verificacion propia recomendada | Recalcular con el propio dataset de Andres si se construye de forma independiente | INSUMO EXTERNO (cifras, con verificacion propia recomendada) | Usar como valor esperado de referencia; no asumir identicas sin recalculo |
| OE-02 (Estructuracion) | Modelo estrella / modelo dimensional | No aplica — el companero **tampoco** materializo un modelo estrella formal | N/A | N/A | Ninguna: esta brecha ya fue identificada en `MATRIZ_OBJETIVOS_CODIGO.md` (OE-02) como ausente en todo el repositorio, incluyendo la Fase 1 del companero |
| OE-03 (Normalizacion) | Hallazgos de calidad de datos (sentinelas, duplicados, tipos, outliers) | Si, como referencia y posible base de codigo | Confirmar autoria del pipeline base | AUTORIA A CONFIRMAR CON DIRECTOR | Citar los hallazgos; reutilizar el tratamiento (winsorizacion, homologacion de sentinelas) solo si se confirma coautoria |
| OE-03 (Normalizacion) | `cols_leakage.txt` (variables de leakage) | Parcialmente aplicable, con correccion | El companero subestima el conteo (14 vs 45 reales); Andres debe definir su propia lista de variables no utilizables segun su propio marco de indicadores continuos | CODIGO DEL COMPANERO - EXCLUIR (el archivo en si) | No copiar el archivo; el concepto de excluir variables post-ejecucion si es aplicable y debe rehacerse con criterio propio |
| OE-04 (Dashboard) | No hay elementos de la Fase 1 relacionados con visualizacion | No aplica | — | — | Ningun aprovechamiento posible desde esta fase; ver Seccion 3.4 de `MATRIZ_OBJETIVOS_CODIGO.md` para la brecha de OE-04 |

---

## 3. Analisis detallado por objetivo

### OE-01: Extraccion automatizada de SECOP

**Que aporta la Fase 1 del companero:** Una estrategia de extraccion completa y probada (filtros SoQL, paginacion, lotes con reintentos, timeout extendido, persistencia Parquet), documentada con precision suficiente para ser replicada. El companero declara explicitamente en su Seccion 1.2 el mismo conjunto de decisiones tecnicas que `InformesRev/RESUMEN_CODIGO.md` ya identifico en `notebooks/00-06` como la implementacion real (verificado en `RESUMEN_CODIGO_FASE1_INFORME_FINAL.md`, seccion 2).

**Lo que Andres puede tomar sin reservas:** los Dataset IDs de las fuentes SECOP (`jbjy-vk9h`, `p6dx-8zbt`, `cb9c-h8sn`, `qmzu-gj57`), que son informacion publica del portal datos.gov.co, no propiedad intelectual de nadie.

**Lo que requiere confirmacion del director:** el codigo real de extraccion (`notebooks/00-06`), ya que fue escrito con el proposito declarado de alimentar el modelado predictivo del companero (`doc/contexto/CONTEXTO.md`, linea 10, ya citado en `MATRIZ_OBJETIVOS_CODIGO.md`). Si el director confirma que este pipeline es insumo compartido, Andres puede reutilizarlo directamente, anadiendo unicamente el filtro de fecha 2018-2024 y los logs que le faltan (brecha ya identificada en `MATRIZ_OBJETIVOS_CODIGO.md`, seccion 3, OE-01).

**Ahorro de tiempo estimado si se confirma la coautoria:** el pipeline de extraccion ya esta escrito y probado (51.353 a 276.770 registros por fuente, segun tabla de la Fase 1); Andres se ahorraria practicamente la totalidad del desarrollo de OE-01, reduciendo su propia tarea a las brechas puntuales (filtro de fecha, logging, script reutilizable) ya presupuestadas en 1-1.5 semanas en `MATRIZ_OBJETIVOS_CODIGO.md`.

**Riesgo si no se confirma la coautoria:** Andres tendria que reconstruir la extraccion de forma independiente para evitar cualquier ambiguedad de autoria, lo que anadiria aproximadamente un tiempo similar al de aprender y validar la estrategia ya documentada (estimado adicional: 1-2 semanas).

### OE-02: Modelo de datos analitico (estructuracion)

**Que aporta la Fase 1 del companero:** El hallazgo tecnico mas valioso de toda la fase: la correccion de la llave de integracion entre procesos y contratos (`id_del_portafolio` en lugar de `id_del_proceso`), que elevo la cobertura del join de 0% a 99.9%. Este es un hecho sobre la estructura de los datos publicos de SECOP II, no una obra de autoria original del companero en el sentido de propiedad intelectual — es un descubrimiento tecnico documentable y citable como antecedente, similar a como se citaria un hallazgo publicado en un articulo.

**Importante — brecha compartida:** ni la Fase 1 del companero ni ningun otro punto del repositorio materializan un modelo estrella formal (tabla de hechos + dimensiones en un motor de base de datos). Esto ya fue establecido como ausente de forma transversal en `MATRIZ_OBJETIVOS_CODIGO.md` (seccion 3, OE-02, Camino B recomendado: modelo dimensional simplificado). Es decir, **la Fase 1 del companero no resuelve esta brecha de Andres**; solo resuelve la integracion via joins de pandas, que es la misma tecnica (no un modelo estrella) que Andres tendria que documentar de cualquier forma bajo su Camino B ya recomendado.

**Recomendacion:** Andres puede citar el hallazgo de la llave de integracion como antecedente tecnico (con atribucion), y usar las coberturas de join reportadas como valores de referencia esperados, pero debe recalcularlas sobre su propio dataset si construye la integracion de forma independiente, y debe construir su propio modelo dimensional simplificado (diagrama + convenciones) de cualquier forma, ya que esa pieza no existe en ningun punto del repositorio compartido.

### OE-03: Normalizacion de variables

**Que aporta la Fase 1 del companero:** Un inventario de hallazgos de calidad de datos (sentinelas, duplicados masivos, tipos incorrectos, outliers extremos) y su tratamiento (winsorizacion p1/p99). Estos hallazgos son consistentes con lo ya documentado independientemente en `doc/contexto/CONTEXTO.md` y verificado en `InformesRev/RESUMEN_CODIGO.md` (seccion 9).

**Advertencia especifica sobre `cols_leakage.txt`:** el companero declara 14 variables de leakage, pero el archivo real tiene 45 (verificado en `RESUMEN_CODIGO_FASE1_INFORME_FINAL.md`, seccion 5). Andres **no debe** citar la cifra de "14" si hace referencia a este archivo, y **no debe** copiar el archivo tal cual, porque esas 45 variables fueron definidas especificamente para excluir informacion post-ejecucion en el contexto de un modelo de clasificacion binaria (`tiempo`, `presupuesto`, `alcance`, `tuvo_atraso`, `tuvo_sobrecosto`), no en el contexto de indicadores descriptivos continuos que Andres necesita construir. El concepto (excluir variables que solo se conocen despues de la ejecucion del contrato) si es aplicable y debe reconstruirse con una lista propia, adaptada a los indicadores continuos de tiempo/costo/alcance que exige el anteproyecto de Andres.

**Recomendacion:** Andres debe construir su propia lista de "variables no disponibles al momento de la firma" a partir de las mismas fuentes de datos, con criterio propio y documentado, sin heredar directamente `cols_leakage.txt` del companero.

---

## 4. Diferenciacion de autoria especifica a los elementos de la Fase 1

| Elemento de la Fase 1 | Clasificacion | Justificacion |
|---|---|---|
| Dataset IDs de Socrata (`jbjy-vk9h`, `p6dx-8zbt`, `cb9c-h8sn`, `qmzu-gj57`) | INSUMO EXTERNO | Informacion publica del portal datos.gov.co, no propiedad de ningun estudiante |
| Hallazgo de la llave `id_del_portafolio` | INSUMO EXTERNO (hallazgo tecnico citable) | Es un hecho sobre la estructura de los datos SECOP II, documentado independientemente en `doc/contexto/CONTEXTO.md`; citable como antecedente con atribucion |
| Codigo de extraccion (`notebooks/00-06`) | AUTORIA A CONFIRMAR CON DIRECTOR | Mismo estatus que en `MATRIZ_OBJETIVOS_CODIGO.md`, seccion 4 |
| Coberturas de join (cifras porcentuales) | INSUMO EXTERNO (cifras de referencia, con verificacion propia recomendada) | Son resultados numericos sobre datos publicos; citables como antecedente, no como aporte propio de Andres sin recalculo |
| Estrategia de scraping RUP (Playwright + CapSolver) | CODIGO DEL COMPANERO - EXCLUIR | Ya establecido en `MATRIZ_OBJETIVOS_CODIGO.md`; no aplica al alcance de Andres |
| Pipeline Docker de indicadores de pliegos | CODIGO DEL COMPANERO - EXCLUIR | Idem |
| `cols_leakage.txt` (el archivo en si) | CODIGO DEL COMPANERO - EXCLUIR | Construido para el modelado predictivo binario, con la imprecision documental ya senalada (14 vs 45); no debe copiarse tal cual |
| Narrativa de hallazgos de calidad de datos (sentinelas, duplicados, outliers) | AUTORIA A CONFIRMAR CON DIRECTOR (si se reutiliza el texto) / INSUMO EXTERNO (si se cita como hallazgo, con atribucion) | El hallazgo en si (que existen sentinelas, duplicados, outliers en SECOP) es objetivo y verificable; el texto narrativo especifico del informe es propiedad intelectual del companero y no debe copiarse literalmente |

---

## 5. Recomendaciones concretas de aprovechamiento

1. **Citar como antecedente tecnico documentado** (con atribucion explicita al trabajo del companero, dirigido por el mismo tutor): el hallazgo de la llave de integracion `id_del_portafolio` y las coberturas de join medidas. Esto ahorra a Andres el tiempo de re-descubrir estos hechos de forma independiente y le da respaldo documental adicional a su propio marco de integracion.
2. **Usar como lista de verificacion de calidad de datos, no como fuente de codigo:** los hallazgos de sentinelas, duplicados y outliers reportados en la Fase 1 sirven como checklist de que buscar al auditar la calidad de sus propios datasets, pero el codigo de tratamiento debe ser propio o confirmado como insumo compartido con el director.
3. **No reutilizar `cols_leakage.txt` tal cual.** Construir una lista propia de variables no disponibles al momento de la firma, adaptada a los indicadores continuos que exige el anteproyecto, y evitar citar la cifra de "14" sin verificarla (el archivo real tiene 45 entradas).
4. **Priorizar la reunion con el director** (ya recomendada en `MATRIZ_OBJETIVOS_CODIGO.md`, tarea 1 del plan de accion) precisamente porque esta Fase 1 confirma que el pipeline compartido es sustancial y bien documentado: si se confirma la coautoria, el ahorro de tiempo para Andres en OE-01 y parte de OE-03 es significativo (varias semanas); si no se confirma, Andres debe presupuestar tiempo adicional para reconstruir esa infraestructura de forma independiente.
5. **No aprovechar nada de esta fase para OE-04**, dado que la Seccion 1 no contiene ningun elemento de visualizacion o dashboard.

---

## 6. Riesgos especificos derivados de usar la Fase 1 del companero como insumo

| Riesgo | Severidad | Mitigacion |
|---|---|---|
| Citar la cifra de "14 variables de leakage" sin verificarla, replicando el error del companero | Media | Verificar siempre contra el archivo real (`modelo_predictivo_global/data/cols_leakage.txt`, 45 entradas) antes de citar cualquier cifra de este documento |
| Asumir que el codigo de extraccion es de libre uso sin confirmar autoria | Alta | No usar el codigo de `notebooks/00-06` en el entregable de Andres hasta tener confirmacion escrita del director (ya establecido en `MATRIZ_OBJETIVOS_CODIGO.md`) |
| Citar cifras de cobertura de join sin recalculo propio, presentandolas como resultado propio | Media | Citar siempre con atribucion explicita al trabajo del companero si no se recalculan de forma independiente |
| Confundir el alcance de la Fase 1 (ETL para modelado predictivo) con el alcance de OE-02 de Andres (modelo estrella descriptivo) | Media | Dejar explicito en el capitulo de metodologia que la integracion de datos es insumo compartido, pero el modelo dimensional y los indicadores son aporte propio e independiente |

---

## 7. Version ultracompacta

La Fase 1 del companero (`report/INFORME-FINAL.md`, Seccion 1) es tecnicamente solida y mayoritariamente verificable contra el codigo real (`RESUMEN_CODIGO_FASE1_INFORME_FINAL.md`), con una sola contradiccion factual dura: declara 14 variables de leakage cuando el archivo real (`modelo_predictivo_global/data/cols_leakage.txt`) tiene 45. Para Andres, esta fase aporta valor real a OE-01 (estrategia de extraccion ya probada) y OE-02 (hallazgo de la llave `id_del_portafolio` y coberturas de join, citables como antecedente tecnico), y aporta un checklist util para OE-03 (calidad de datos), pero no resuelve la brecha de modelo estrella formal (que tampoco existe en la Fase 1 del companero) ni aporta nada a OE-04 (dashboard, fuera de esta seccion). El uso del codigo real de extraccion (`notebooks/00-06`) sigue sujeto a la misma condicion ya establecida en `MATRIZ_OBJETIVOS_CODIGO.md`: confirmacion formal de autoria compartida por parte del director. No debe reutilizarse `cols_leakage.txt` tal cual, ni citarse la cifra de "14" sin verificacion.

---

## 8. Checklist de siguientes pasos especificos a esta fase

- [ ] Verificar con el director el estatus de autoria de `notebooks/00-06` (misma tarea que en `MATRIZ_OBJETIVOS_CODIGO.md`).
- [ ] Si se confirma coautoria, incorporar el codigo de extraccion a `tesis-andres/` con las brechas de OE-01 ya identificadas (filtro fecha, logs, script reutilizable).
- [ ] Citar el hallazgo de la llave `id_del_portafolio` y las coberturas de join como antecedente tecnico, con atribucion.
- [ ] Construir una lista propia de variables no disponibles al momento de la firma (no copiar `cols_leakage.txt`).
- [ ] Verificar cualquier cifra citada de `report/INFORME-FINAL.md` antes de reutilizarla (ya se detecto al menos un error de conteo).
- [ ] No extraer ningun elemento de esta fase para OE-04 (no aplica).
