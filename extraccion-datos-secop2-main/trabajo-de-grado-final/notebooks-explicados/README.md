# Notebooks explicados en lenguaje no técnico

Este índice acompaña al Anexo A del trabajo de grado (`../TRABAJO_DE_GRADO.md`). Cada archivo `.md` explica uno de los notebooks reales del proyecto, referenciando su ruta original, y sigue siempre la misma estructura en dos partes:

1. **Explicación técnica paso a paso** — un recorrido extendido y explícito por lo que hace el notebook, celda por celda o etapa por etapa, con las cifras exactas que produce. Más detallado que una simple traducción a lenguaje llano, pero sin jerga innecesaria.
2. **Conclusión** — el resumen condensado en dos apartados ("Qué se hizo, en palabras simples" y "Por qué importa"), pensado para quien solo quiere la idea general sin entrar en el detalle técnico.

Ningún archivo aquí modifica, ejecuta ni reemplaza el notebook original: son una traducción y ampliación explicativa, pensada para que el autor revise y decida cuáles conservar como evidencia en la sustentación.

## 01 — Extracción y estructuración compartida (coautoría con Ángel García Rangel)

Notebooks originales en `notebooks/00` a `06` de la raíz del repositorio.

| Archivo | Notebook original | Qué hace, en una frase |
|---|---|---|
| `00_definicion_tabla_base.md` | `notebooks/00_definicion_tabla_base.ipynb` | Decide cuál de las cuatro fuentes de SECOP es la base principal del análisis |
| `01_contratos_electronicos.md` | `notebooks/01_contratos_electronicos.ipynb` | Descarga y perfila los 51.353 contratos de obra pública |
| `02_procesos_contratacion.md` | `notebooks/02_procesos_contratacion.ipynb` | Descarga los procesos de compra y corrige la llave de integración |
| `03_adiciones.md` | `notebooks/03_adiciones.ipynb` | Descarga los cambios y modificaciones contractuales |
| `04_proveedores.md` | `notebooks/04_proveedores.ipynb` | Descarga el registro de proveedores |
| `05_integracion_contratos_adiciones.md` | `notebooks/05_integracion_contratos_adiciones.ipynb` | Une todo en la tabla central de 48.331 contratos |
| `06_proponentes_por_proceso.md` | `notebooks/06_proponentes_por_proceso.ipynb` | Descarga quiénes compitieron por cada contrato |

## 02 — Análisis descriptivo propio, primera versión

Notebooks originales en `analitica-descriptiva-andres/notebooks/`.

| Archivo | Notebook original | Qué hace, en una frase |
|---|---|---|
| `01_modelo_dimensional.md` | `01_modelo_dimensional.ipynb` | Reorganiza la tabla central en un esquema más ordenado |
| `02_calidad_umbrales.md` | `02_calidad_umbrales.ipynb` | Decide qué contratos se pueden evaluar y cuáles no |
| `03_indicadores_restriccion_hierro.md` | `03_indicadores_restriccion_hierro.ipynb` | Construye los tres indicadores de tiempo, costo y alcance |
| `04_eda_univariado.md` | `04_eda_univariado.ipynb` | Grafica cómo se distribuyen esos indicadores |
| `05_eda_segmentado.md` | `05_eda_segmentado.ipynb` | Compara los indicadores entre modalidad, contratista y territorio |
| `06_correlaciones_asociaciones.md` | `06_correlaciones_asociaciones.ipynb` | Mide qué variables se relacionan entre sí |
| `07_contraste_hipotesis.md` | `07_contraste_hipotesis.ipynb` | Primera prueba formal de las tres hipótesis |
| `08_sintesis_hallazgos.md` | `08_sintesis_hallazgos.ipynb` | Resume los hallazgos de esta primera ronda |

## 03 — EDA extendido propio (universo completo, 48.331 contratos)

Notebooks originales en `eda-extendido-integral/notebooks/`.

| Archivo | Notebook original | Qué hace, en una frase |
|---|---|---|
| `01_universo_enriquecido.md` | `01_universo_enriquecido.ipynb` | Amplía el análisis a todos los contratos y añade datos de competencia |
| `02_calidad_extendida.md` | `02_calidad_extendida.ipynb` | Repite la revisión de calidad sobre el universo completo |
| `03_indicadores_doble_lectura.md` | `03_indicadores_doble_lectura.ipynb` | Recalcula los indicadores mostrando siempre las dos lecturas |
| `04_competencia.md` | `04_competencia.ipynb` | Prueba si la competencia real explica los retrasos (no lo hace) |
| `05_valor_precio_base_cuantia.md` | `05_valor_precio_base_cuantia.ipynb` | Resuelve el misterio del sobrecosto casi nulo |
| `06_temporal.md` | `06_temporal.ipynb` | Revisa la evolución de los datos año a año |
| `07_perfil_proveedor.md` | `07_perfil_proveedor.ipynb` | Compara el perfil de consorcios y empresas individuales |
| `08_alcance_y_coocurrencia.md` | `08_alcance_y_coocurrencia.ipynb` | Justifica cómo se clasifica el cumplimiento de alcance |
| `09_asociaciones_extendido.md` | `09_asociaciones_extendido.ipynb` | Consolida todas las relaciones entre variables |
| `10_hipotesis_extendido.md` | `10_hipotesis_extendido.ipynb` | Prueba a fondo las tres hipótesis, con controles adicionales |
| `11_sintesis_dual.md` | `11_sintesis_dual.ipynb` | Resume y etiqueta todos los hallazgos del proyecto |

## Cómo usar esta carpeta

Al preparar la sustentación, revisa cada archivo y decide cuáles incluir como Anexo A del trabajo de grado. Se recomienda conservar, como mínimo, los que sustentan directamente los cambios frente al anteproyecto: `02_procesos_contratacion.md` (corrección de la llave), `05_valor_precio_base_cuantia.md` (el hallazgo del sobrecosto) y `10_hipotesis_extendido.md` (el contraste final de las tres hipótesis).
