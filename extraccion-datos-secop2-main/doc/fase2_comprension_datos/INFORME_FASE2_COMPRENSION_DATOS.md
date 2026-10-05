# Informe Fase 2 — Comprensión de Datos
## Modelo Predictivo de Obra Pública SECOP II

> **Metodología**: CRISP-DM — Fase 2 completada
> **Fecha**: 2026-03-03
> **Alcance**: 4 fuentes de datos exploradas, 4 notebooks ejecutados
> **Filtro global**: `tipo_de_contrato = "Obra"`

---

## 1. Resumen ejecutivo

Se completó la exploración de las 4 fuentes de datos del SECOP II relevantes para
el modelo predictivo de contratos de Obra Pública. Se descargaron, perfilaron y
almacenaron **451,619 registros** distribuidos en 4 archivos Parquet.

| Fuente | Registros | Columnas | Cobertura | Archivo |
|---|---|---|---|---|
| contratosElectronicos | 51,353 | 87 | — (fuente madre) | `contratos_electronicos_obra.parquet` |
| procesosDeContratacion | 138,112 | 60 | 99.9% | `procesos_contratacion_obra.parquet` |
| adiciones | 249,037 | 5 | 69.2% | `adiciones_obra.parquet` |
| proveedoresRegistrados | 13,117 | 25 | 54.4% | `proveedores_obra.parquet` |

**Hallazgo principal**: Los datos son suficientes para construir un modelo predictivo,
pero requieren limpieza significativa (duplicados, sentinelas, conversión de tipos,
outliers) y un diseño cuidadoso del feature engineering para evitar data leakage.

---

## 2. Fuente madre: contratosElectronicos

### 2.1 Descripción

El contrato electrónico firmado es la **unidad de análisis** del proyecto. Cada fila
representa un contrato de Obra Pública en SECOP II, desde su firma hasta su liquidación.

- **Dataset ID**: jbjy-vk9h
- **Registros**: 51,353 (0.89% del total de 5.7M contratos en SECOP II)
- **Contratos únicos** (`id_contrato`): 48,331 (3,022 duplicados — 5.9%)
- **Periodo**: septiembre 2016 — febrero 2026
- **87 columnas** clasificadas en 8 categorías

### 2.2 Clasificación de columnas

| Rol | Cant. | Ejemplos |
|---|---|---|
| ID / Llave | 6 | `id_contrato`, `proceso_de_compra`, `codigo_proveedor` |
| Feature - Entidad | 8 | `departamento`, `sector`, `rama`, `orden` |
| Feature - Contractual | ~24 | `modalidad_de_contratacion`, `valor_del_contrato`, fechas |
| Feature - Presupuestal | 6 | `presupuesto_general_de_la_nacion_pgn`, `recursos_propios` |
| Feature - Proveedor | 5 | `es_pyme`, `es_grupo`, `proveedor_adjudicado` |
| **TARGET potencial** | **3** | `dias_adicionados`, `estado_contrato`, `liquidaci_n` |
| **LEAKAGE** | **15** | `valor_pagado`, `valor_facturado`, `saldo_cdp`, fechas de liquidación |
| Descartable | 18 | URLs, datos bancarios, nombres de personas |

### 2.3 Variables target identificadas

| Target | Tipo | Construcción | Distribución |
|---|---|---|---|
| `tiene_extension` | Binaria | `dias_adicionados > 0` | 22.5% positivo / 77.5% negativo (ratio 1:3.5) |
| `tiene_adicion_valor` | Binaria | Derivado de adiciones | Requiere join con adiciones |
| `sobrecosto_ratio` | Continua | `(valor_pagado - valor_contrato) / valor_contrato` | 67.5% tienen $0 pagado |
| `fue_liquidado` | Binaria | `liquidaci_n == 'Si'` | ~50% liquidados |
| `riesgo_contractual` | Multiclase | Combinación de los anteriores | Por definir |

El desbalance del target primario (`tiene_extension`, 1:3.5) es **manejable** con
técnicas estándar (SMOTE, class_weight, umbrales ajustados).

### 2.4 Distribuciones relevantes

**Estado del contrato**:
- Modificado: 32%, Terminado: 23%, En ejecución: 20%, Cerrado: 6%, Aprobado: 5%

**Modalidad de contratación**:
- Selección Abreviada: ~40%, Contratación Directa: ~25%, Licitación Pública: ~18%

**Valor del contrato (COP)**:
- Mediana: $201M, Media: $3,023M (sesgada por outliers extremos)
- Percentil 5: $12M, Percentil 95: $9,034M
- 705 contratos con valor = $0
- 5 contratos con valor > $1 billón

**Días adicionados** (solo los >0):
- Mediana: 14 días, P75: 30 días, P90: 90 días, P95: 180 días

**Geografía**:
- Bogotá lidera, seguido de Antioquia, Valle del Cauca, Cundinamarca

### 2.5 Problemas de calidad

| Problema | Detalle | Impacto |
|---|---|---|
| Duplicados | 3,022 en `id_contrato` | Inflación de métricas |
| Tipos de dato | Todos los numéricos llegan como texto | Requiere conversión |
| Sentinela "No Definido" | En ~14 columnas con >50% frecuencia | Nulidad oculta |
| Duración como texto | "143 Dia(s)", "3 Mes(es)" — 3,196 "No definido" | Requiere parsing |
| Outliers financieros | Máximo $7.1 billones, 182 contratos > $100MM | Sesgan estadísticas |
| Fechas anómalas | Inicio en 1899, fin en 2047, 23 duraciones negativas | Datos corruptos |
| Nulidad en fechas | Firma 10.5%, Inicio 12.4%, Actualización 35.2% | Reduce muestra |
| Leakage | 15 columnas de ejecución financiera y liquidación | Excluir de features |

---

## 3. Fuente complementaria: procesosDeContratacion

### 3.1 Descripción

Cada fila representa un **proceso de compra** (licitación, selección, etc.) que
precede al contrato. Contiene información que existe **antes de la firma**, lo que
la convierte en fuente libre de leakage.

- **Dataset ID**: p6dx-8zbt
- **Registros**: 138,112 de tipo Obra
- **Columnas recibidas**: 60 (de 59 definidas + 1 extra)
- **Duplicados** en `id_del_proceso`: 25,221

### 3.2 Llave de integración

> **Lección crítica**: `id_del_proceso` (prefijo CO1.REQ.) **NO** coincide con
> `proceso_de_compra` (prefijo CO1.BDOS.). La llave correcta es `id_del_portafolio`,
> que logra un **99.9% de match** (43,414 de 43,451 contratos).

### 3.3 Features de competencia (los más valiosos)

Estos campos caracterizan el **nivel de competencia** del proceso y son predictores
intuitivamente fuertes de riesgo contractual:

| Campo | Descripción | Valor predictivo |
|---|---|---|
| `proveedores_invitados` | Cuántos proveedores fueron invitados | Más invitados → más competencia |
| `proveedores_que_manifestaron` | Cuántos mostraron interés | Interés real en el proceso |
| `proveedores_unicos_con` | Cuántos presentaron oferta | Competencia efectiva |
| `visualizaciones_del` | Vistas del proceso | Transparencia/visibilidad |

**Importancia**: Estas variables existen **antes** de firmar el contrato, por lo que
no generan leakage temporal.

### 3.4 Distribuciones relevantes

**Adjudicación**: 40.5% adjudicados, 59.5% no adjudicados

**Modalidades**:
- Selección Abreviada: 33.8%, Licitación pública: 23.4%
- Régimen especial: 20.2%, Mínima cuantía: 9.7%

**Precio base**: Mediana $300M COP, con outliers absurdos (máx $11 cuatrillones)

**Orden territorial**: 63.9% Territorial, 34.7% Nacional

### 3.5 Problemas de calidad

| Problema | Detalle |
|---|---|
| Duplicados masivos | 25,221 (18.3%) — algunos IDs repetidos hasta 1,296 veces |
| Subtipo contrato | 100% "No Definido" → campo inútil |
| Valor adjudicación | 59.6% son ceros → poco útil |
| Nulidad en fechas | publicación (89.8%), adjudicación (63.1%) |
| Outliers extremos | Duración máx 27M días, precio máx $11 cuatrillones |

---

## 4. Fuente complementaria: adiciones

### 4.1 Descripción

Cada fila representa un **evento de modificación** a un contrato: adiciones en valor,
prórrogas, suspensiones, cesiones, etc. La relación es N:1 con contratos (un contrato
puede tener múltiples adiciones).

- **Dataset ID**: cb9c-h8sn
- **Registros**: 249,037
- **Columnas**: 5 (`identificador`, `id_contrato`, `tipo`, `descripcion`, `fecharegistro`)
- **Contratos con adiciones**: 33,465 (69.2% de 48,331 contratos de Obra)
- **Nulidad**: 0% en todas las columnas

### 4.2 Tipos de modificación

| Tipo | Frecuencia | Relevancia para el modelo |
|---|---|---|
| MODIFICACION GENERAL | 76.4% de contratos con adiciones | Demasiado genérico |
| No definido | 55.4% | Sentinela |
| REACTIVACIoN | 27.4% | Indica contrato suspendido previamente |
| SUSPENSIoN | ~24.7% | Feature: contrato fue suspendido |
| CONCLUSION | 15.2% | Indica cierre formal |
| ADICION EN EL VALOR | 13.3% | **TARGET directo** |
| CESION | 1.5% | Cambio de contratista (riesgo) |
| EXTENSION | 0.006% (2 registros) | Target, pero casi vacío |

### 4.3 Variables derivadas propuestas

| Variable | Tipo | Descripción | Rol |
|---|---|---|---|
| `n_modificaciones_total` | Numérica | Total de eventos por contrato | Feature / Target |
| `n_tipos_distintos` | Numérica | Diversidad de modificaciones | Feature |
| `n_adiciones_valor` | Numérica | Adiciones en valor | Target |
| `tiene_adicion_valor` | Binaria | Al menos una adición en valor | Target |
| `tiene_suspension` | Binaria | Fue suspendido alguna vez | Feature / Target |
| `tiene_cesion` | Binaria | Cambió de contratista | Feature / Target |
| `tiene_conclusion` | Binaria | Fue concluido formalmente | Feature |

### 4.4 Consideración de leakage

Las adiciones ocurren **durante** la ejecución del contrato. Esto significa que:

- **Como TARGET**: Usarlas libremente (es lo que queremos predecir)
- **Como FEATURE**: Solo si se aplica un **corte temporal** (ej: usar solo adiciones
  de los primeros N días para predecir adiciones futuras), lo cual es complejo y
  reduce la muestra significativamente.

**Recomendación**: Usar adiciones exclusivamente para construir targets.

### 4.5 Problemas de calidad

| Problema | Detalle |
|---|---|
| Duplicados masivos | 105,836 en `identificador`, 96,942 filas idénticas |
| Sentinela en `tipo` | 55.4% "No definido" |
| Sin campo de valor | No indica el monto de la adición, solo el tipo |

---

## 5. Fuente complementaria: proveedoresRegistrados

### 5.1 Descripción

Cada fila representa el **perfil** de un proveedor registrado en SECOP II: tipo de
empresa, ubicación, clasificación UNSPSC, si es Pyme, etc.

- **Dataset ID**: qmzu-gj57
- **Registros**: 13,117 (12,618 proveedores únicos)
- **Columnas**: 25
- **Cobertura**: 54.4% (12,618 de 23,192 proveedores de Obra)
- **Nulidad técnica**: 0% (pero sentinela "No Provisto" frecuente)

### 5.2 Cobertura y diagnóstico

La cobertura de 54.4% **no es un error de join**. Se verificó directamente contra
la API: los 10,574 proveedores faltantes simplemente no existen en el dataset de
datos.gov.co. Posibles causas:

- Proveedores que nunca completaron su perfil
- Registros eliminados o desactivados
- Dataset que no incluye históricos completos

**Implicación**: En el JOIN final, ~45% de los contratos tendrán nulos en las
columnas de proveedor.

### 5.3 Clasificación de columnas

| Categoría | Cant. | Columnas |
|---|---|---|
| ID / Llave | 2 | `codigo`, `nit` |
| Feature candidato | 12 | `espyme`, `tipo_empresa`, `departamento`, `municipio`, `codigo_categoria_principal`, `fecha_creacion`, etc. |
| Dato de contacto (descartar) | 6 | `nombre`, `telefono`, `correo`, `direccion`, `fax`, `sitio_web` |
| Representante legal (descartar) | 5 | `nombre_representante_legal`, documentos, teléfono, correo |

### 5.4 Variables con varianza cero (descartar)

| Variable | Distribución | Decisión |
|---|---|---|
| `es_grupo` | 100% No | Descartar |
| `es_entidad` | 99.98% No | Descartar |
| `esta_activa` | 99.99% Si | Descartar |
| `pais` | 99.98% CO | Descartar (o binaria) |

### 5.5 Features útiles

| Variable | Distribución | Potencial |
|---|---|---|
| `espyme` | 60% Si / 40% No | Alto — buena discriminación |
| `tipo_empresa` | SAS domina, 9+ tipos | Medio — cardinalidad baja |
| `departamento` | 34 departamentos (29% "No Provisto") | Medio — con limpieza |
| `municipio` | 708 municipios (29% "No Provisto") | Medio — alta cardinalidad |
| `codigo_categoria_principal` | UNSPSC, múltiples categorías | Medio — requiere agrupación |
| `fecha_creacion` | 2015–2026 | Alto — antigüedad del proveedor |

### 5.6 Problemas de calidad

| Problema | Detalle |
|---|---|
| Cobertura parcial | 54.4% — la más baja de las 4 fuentes |
| Sentinela "No Provisto" | ~29% en departamento y municipio |
| 499 duplicados | 100% filas idénticas (trivial de limpiar) |
| 4 columnas constantes | Varianza ~0, no aportan información |

---

## 6. Esquema relacional confirmado

```
procesosDeContratacion ──────(1:N)──────► contratosElectronicos (FUENTE MADRE)
  id_del_portafolio            =           proceso_de_compra
  Cobertura: 99.9%                         48,331 contratos únicos

proveedoresRegistrados ──────(1:N)──────► contratosElectronicos
  codigo                       =           codigo_proveedor
  Cobertura: 54.4%                         12,618 proveedores encontrados

adiciones ───────────────────(N:1)──────► contratosElectronicos
  id_contrato                  =           id_contrato
  Cobertura: 69.2%                         33,465 contratos con adiciones
```

### Estrategia de JOIN

El JOIN se realizará con `contratosElectronicos` como tabla central:

1. **LEFT JOIN** con `procesosDeContratacion` vía `proceso_de_compra` = `id_del_portafolio`
   - Esperado: ~99.9% de match
   - Aporta: features de competencia, modalidad detallada, precios base

2. **LEFT JOIN** con agregado de `adiciones` vía `id_contrato`
   - Primero agregar adiciones a nivel contrato (pivot/groupby)
   - Esperado: 69.2% con datos, 30.8% con ceros/nulos
   - Aporta: variables target y features de modificación

3. **LEFT JOIN** con `proveedoresRegistrados` vía `codigo_proveedor` = `codigo`
   - Esperado: 54.4% con datos, 45.6% con nulos
   - Aporta: perfil del proveedor (pyme, tipo empresa, ubicación, UNSPSC)

---

## 7. Problemas de calidad transversales

### 7.1 Duplicados

| Fuente | Duplicados | % del total | Tipo |
|---|---|---|---|
| contratosElectronicos | 3,022 en `id_contrato` | 5.9% | Requiere investigación |
| procesosDeContratacion | 25,221 en `id_del_proceso` | 18.3% | Algunos IDs x1,296 |
| adiciones | 96,942 filas idénticas | 38.9% | Deduplicar directamente |
| proveedoresRegistrados | 499 filas idénticas | 3.8% | Deduplicar directamente |

**Acción requerida**: Deduplicar en todas las fuentes antes del JOIN. Para contratos
y procesos, investigar si los duplicados representan versiones diferentes del mismo
registro (por actualización) o errores de carga.

### 7.2 Sentinelas como nulos ocultos

SECOP II usa cadenas de texto en lugar de NULL real:

| Sentinela | Fuentes afectadas | Ejemplo de campo |
|---|---|---|
| `"No Definido"` | contratosElectronicos, procesosDeContratacion | subtipo_contrato, c_digo_bpin |
| `"No Provisto"` | proveedoresRegistrados | departamento, municipio, teléfono |
| `"No definido"` | adiciones | tipo de modificación |
| `""` (cadena vacía) | Todas | Varios |
| `"0"` | contratosElectronicos | codigo_proveedor (677 registros) |

**Acción requerida**: Reemplazar todos los sentinelas por `NaN` antes de cualquier
análisis estadístico o modelado.

### 7.3 Tipos de datos incorrectos

- **Todos los campos numéricos** de contratosElectronicos llegan como texto (`object`)
- **Fechas** llegan como strings ISO 8601
- **`duraci_n_del_contrato`** es texto libre ("143 Dia(s)", "3 Mes(es)")
- **Booleanos** codificados como "Si"/"No" en texto

**Acción requerida**: Pipeline de conversión de tipos en el notebook de integración.

### 7.4 Nulidad real significativa

| Campo | Fuente | % Nulidad | Impacto |
|---|---|---|---|
| `fecha_de_publicacion` | procesos | 89.8% | Descartar campo |
| `fecha_de_publicacion_fase_2` | procesos | 82.9% | Descartar campo |
| `nombre_ordenador_de_pago` | contratos | 94.9% | Descartar campo |
| `datos bancarios` | contratos | ~76% | Descartar campos |
| `fecha_adjudicacion` | procesos | 63.1% | Imputar o descartar |
| `fecha_inicio_liquidacion` | contratos | 50.0% | LEAKAGE — descartar |
| `ultima_actualizacion` | contratos | 35.2% | LEAKAGE — descartar |
| `departamento` (proveedor) | proveedores | ~29% "No Provisto" | Imputar como "Desconocido" |

### 7.5 Outliers extremos

| Campo | Fuente | Valor extremo | Acción |
|---|---|---|---|
| `valor_del_contrato` | contratos | Máx $7.1 billones | Winsorizar o filtrar |
| `precio_base` | procesos | Máx $11 cuatrillones | Claramente erróneo — filtrar |
| `duracion_estimada` | procesos | Máx 27M días (~74,000 años) | Filtrar |
| `dias_adicionados` | contratos | Máx 2,934 días (~8 años) | Evaluar caso por caso |
| Fechas de inicio | contratos | 1899-11-24 | Dato corrupto — NaN |
| Fechas de fin | contratos | 2047-07-31 | Sospechoso — investigar |

---

## 8. Inventario de features candidatos

### 8.1 Features directos (sin transformación)

| Feature | Fuente | Tipo | Notas |
|---|---|---|---|
| `modalidad_de_contratacion` | contratos | Categórica | 5 modalidades principales |
| `departamento` | contratos | Categórica | Geográfico de la entidad |
| `sector` | contratos | Categórica | Sector económico |
| `orden` | contratos | Categórica | Nacional/Territorial |
| `es_pyme` | contratos | Binaria | Del contrato |
| `es_grupo` | contratos | Binaria | Del contrato |
| `valor_del_contrato` | contratos | Numérica | Requiere conversión + outliers |
| `habilita_pago_adelantado` | contratos | Binaria | Si/No |
| `espostconflicto` | contratos | Binaria | Indicador de posconflicto |
| `origen_de_los_recursos` | contratos | Categórica | Fuente de financiamiento |
| `destino_gasto` | contratos | Categórica | Destino presupuestal |

### 8.2 Features de competencia (desde procesos)

| Feature | Tipo | Descripción |
|---|---|---|
| `proveedores_invitados` | Numérica | Total invitados al proceso |
| `proveedores_que_manifestaron` | Numérica | Interesados reales |
| `proveedores_unicos_con` | Numérica | Oferentes efectivos |
| `visualizaciones_del` | Numérica | Visibilidad pública |
| `precio_base` | Numérica | Estimación inicial (con limpieza) |
| `modalidad_de_contratacion` (procesos) | Categórica | Detalle de modalidad |

### 8.3 Features derivados (requieren cálculo)

| Feature | Fuente | Tipo | Construcción |
|---|---|---|---|
| `duracion_dias` | contratos | Numérica | Parsing de "143 Dia(s)" a número |
| `duracion_planificada` | contratos | Numérica | `fecha_fin - fecha_inicio` |
| `ratio_competencia` | procesos | Numérica | `oferentes / invitados` |
| `log_valor_contrato` | contratos | Numérica | Transformación logarítmica |
| `proveedor_es_pyme` | proveedores | Binaria | Desde registro del proveedor |
| `proveedor_tipo_empresa` | proveedores | Categórica | SAS, LTDA, etc. |
| `proveedor_departamento` | proveedores | Categórica | Ubicación del proveedor |
| `proveedor_antiguedad_dias` | proveedores | Numérica | `fecha_firma - fecha_creacion` |
| `proveedor_categoria_unspsc` | proveedores | Categórica | Agrupación UNSPSC |
| `tiene_registro_proveedor` | proveedores | Binaria | 1 si existe en proveedoresRegistrados |
| `mes_firma` | contratos | Numérica | Estacionalidad |
| `anio_firma` | contratos | Numérica | Tendencia temporal |
| `fuente_recursos_pgn` | contratos | Numérica | % financiado con PGN |

### 8.4 Resumen cuantitativo

| Categoría | Features estimados |
|---|---|
| Entidad (geográficos, sectoriales) | ~8 |
| Contractuales (valor, duración, modalidad) | ~12 |
| Competencia (del proceso) | ~6 |
| Proveedor (perfil) | ~8 |
| Presupuestales (fuente recursos) | ~6 |
| Temporales (estacionalidad, tendencia) | ~4 |
| **Total features candidatos** | **~44** |

Tras selección de features (correlación, importancia, varianza), se espera un
conjunto final de **20-30 features** para modelado.

---

## 9. Conclusiones

### 9.1 Fortalezas del dataset

1. **Volumen adecuado**: 48,331 contratos únicos de Obra con ~10 años de historia
2. **Target bien definido**: `tiene_extension` tiene un desbalance manejable (22.5% positivo)
3. **Features pre-contrato disponibles**: Variables de competencia del proceso (sin leakage)
4. **Múltiples perspectivas**: Entidad, proceso, contrato, proveedor, modificaciones
5. **Datos abiertos**: API pública con acceso completo via SODA v3

### 9.2 Debilidades y riesgos

1. **Calidad de datos irregular**: Sentinelas, duplicados, tipos incorrectos en todas las fuentes
2. **Cobertura parcial de proveedores (54.4%)**: Genera nulos masivos en el JOIN
3. **Leakage potencial**: 15+ columnas de ejecución financiera que deben excluirse estrictamente
4. **Duplicados sin explicación**: 3,022 contratos duplicados — pueden ser versiones o errores
5. **Campo `tipo` de adiciones**: 55% "No definido" limita la utilidad de esta variable
6. **Outliers extremos**: Valores financieros y duraciones absurdas requieren tratamiento
7. **Duración como texto**: Parsing no trivial con múltiples formatos

### 9.3 Viabilidad del modelo

| Aspecto | Evaluación |
|---|---|
| Suficiencia de datos | **Alta** — 48K contratos es suficiente |
| Balance del target | **Aceptable** — 1:3.5 es manejable |
| Features disponibles | **Alta** — ~44 candidatos de 4 fuentes |
| Riesgo de leakage | **Medio** — requiere disciplina estricta |
| Calidad de datos | **Media** — limpieza significativa necesaria |
| Viabilidad general | **Alta** — el proyecto es factible |

---

## 10. Siguientes pasos

### Paso 1: Notebook de integración y limpieza

**Objetivo**: Construir la tabla analítica base (una fila = un contrato con todos sus features).

**Tareas**:
1. Deduplicar las 4 fuentes (estrategia por definir para contratos y procesos)
2. Reemplazar sentinelas por `NaN` ("No Definido", "No Provisto", "0", cadenas vacías)
3. Convertir tipos de datos (numéricos, fechas, booleanos)
4. Parsear `duraci_n_del_contrato` (texto → número de días)
5. Agregar adiciones a nivel contrato (pivot: columnas por tipo de modificación)
6. Ejecutar los 3 LEFT JOINs (procesos, adiciones agregadas, proveedores)
7. Crear variable binaria `tiene_registro_proveedor`
8. Calcular features derivados (antigüedad proveedor, ratio competencia, etc.)
9. Tratar outliers (winsorización o filtrado en campos financieros y duración)
10. Guardar tabla integrada como `data/tabla_analitica_obra.parquet`

### Paso 2: Análisis exploratorio integrado

**Objetivo**: Entender relaciones entre features y targets en la tabla unificada.

**Tareas**:
1. Matriz de correlación entre features numéricos y target
2. Análisis bivariado: cada feature vs `tiene_extension`
3. Identificar features con alta correlación entre sí (multicolinealidad)
4. Evaluar cardinalidad de categóricas y decidir encoding
5. Evaluar impacto de nulidad por fuente (¿los nulos de proveedores son informativos?)
6. Documentar decisiones de feature selection

### Paso 3: Preparación final para modelado (CRISP-DM Fase 3)

**Objetivo**: Dataset listo para entrenar modelos.

**Tareas**:
1. Selección final de features (basada en importancia, varianza, correlación)
2. Encoding de categóricas (one-hot, target encoding, ordinal)
3. Imputación de nulos (estrategia por feature)
4. Escalado de numéricos si es necesario (dependiendo del modelo)
5. Split train/test (temporal o aleatorio — decidir)
6. Guardar splits como Parquet

### Paso 4: Modelado predictivo (CRISP-DM Fase 4)

**Objetivo**: Entrenar y evaluar modelos de clasificación.

**Posibles modelos a evaluar**:
- Baseline: Regresión Logística
- Gradient Boosting: XGBoost, LightGBM
- Random Forest
- (Opcional) Redes neuronales si los anteriores no son suficientes

**Métricas**: ROC-AUC, Precision, Recall, F1-Score (priorizando según el caso de uso)

---

## Anexo: Archivos del proyecto

```
extraccion-datos/
├── dataset.json                                # Definiciones de fuentes
├── CONTEXTO.md                                 # Memoria del proyecto
├── INFORME_FASE2_COMPRENSION_DATOS.md          # ← ESTE DOCUMENTO
├── data/
│   ├── contratos_electronicos_obra.parquet     # 51,353 registros
│   ├── procesos_contratacion_obra.parquet      # 138,112 registros
│   ├── adiciones_obra.parquet                  # 249,037 registros
│   └── proveedores_obra.parquet                # 13,117 registros
└── notebooks/
    ├── 00_definicion_tabla_base.ipynb           # Clasificación columnas y esquema
    ├── 01_contratos_electronicos.ipynb          # Exploración fuente madre
    ├── 02_procesos_contratacion.ipynb           # Exploración procesos
    ├── 03_adiciones.ipynb                       # Exploración adiciones
    └── 04_proveedores.ipynb                     # Exploración proveedores
```
