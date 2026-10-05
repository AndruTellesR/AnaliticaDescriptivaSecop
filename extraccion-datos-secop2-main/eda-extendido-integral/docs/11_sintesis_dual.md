# 11 — Sintesis dual: consolidacion de hallazgos y cobertura de objetivos

**Proposito.** Consolidar los hallazgos de los diez cuadernos anteriores en una tabla maestra con
etiquetado dual, cuantificar la distribucion de etiquetas, evaluar que objetivo de cada uno de los dos
trabajos de grado queda cubierto por este EDA, y generar el documento
`docs/HALLAZGOS_ETIQUETADOS.md`.

**Insumo.** Los archivos `data/hallazgos_NN.csv` producidos por cada cuaderno.

**Etiquetas de objetivo que atiende:** todas.

---

## Declaracion de autoria y significado del etiquetado dual

Este EDA es un unico ejercicio tecnico de autoria de **Andres Telles**. Todo el codigo de
`eda-extendido-integral/` es propio. El dataset integrado de entrada proviene del pipeline compartido
(`notebooks/00-06`), cuya autoria sigue pendiente de confirmacion con el director
(`InformesRev/MATRIZ_OBJETIVOS_CODIGO.md`, tarea de prioridad 1), y asi se declara en el notebook 01.
Las columnas producidas por el codigo excluido del blindaje se eliminan fisicamente del DataFrame de
trabajo antes de cualquier analisis y no se leen en ningun punto.

El etiquetado dual clasifica cada hallazgo segun **a que objetivo sirve**, incluidos los objetivos del
compañero:

| Etiqueta | Significado exacto |
|---|---|
| `[A-OE02]` `[A-OE03]` `[A-OE04]` | Sirve a ese objetivo especifico de Andres Telles |
| `[A-H1]` `[A-H2]` `[A-H3]` | Aporta evidencia a esa hipotesis de Andres Telles |
| `[B-OE2]` | **Le seria util** al objetivo de EDA del compañero (Angel Garcia) |
| `[B-OE3-insumo]` | Identifica una variable con asociacion relevante que **seria** candidata predictora. Es informacion sobre asociacion, no modelado |
| `[CALIDAD]` | Hallazgo sobre la calidad del dato SECOP en si mismo, citable por cualquiera de los dos trabajos |

**Regla de honestidad, escrita de forma explicita.** Una etiqueta `[B-*]` significa "este hallazgo le
seria util al compañero". **No** significa "este hallazgo es del compañero", **no** significa que el
compañero lo haya producido, y **no** significa que Andres Telles haya trabajado para el compañero. La
utilidad cruzada de un hallazgo no transfiere su autoria. Ningun resultado de este EDA se ha producido
con codigo del compañero, y ningun resultado de este EDA se atribuye al compañero.

> Documento generado automaticamente a partir de `notebooks/11_sintesis_dual.ipynb` ya ejecutado, por `build/gen_docs.py`. No editar a mano.

---

## 1. Distribucion de etiquetas

## 2. Tabla maestra de hallazgos

## 3. Cobertura de los objetivos de ambos trabajos

## 4. Insights y brechas del documento comparativo: estado tras este EDA

## 5. Contradicciones detectadas respecto del EDA descriptivo previo

## 6. Generacion del documento `docs/HALLAZGOS_ETIQUETADOS.md`

## 7. Verificacion final de integridad del ejercicio

## Sintesis del notebook 11

Este cuaderno no produce hallazgos nuevos: consolida los de los diez anteriores, cuantifica la
distribucion del etiquetado dual, evalua la cobertura de los objetivos de ambos trabajos de grado y
genera `docs/HALLAZGOS_ETIQUETADOS.md`.

**Lectura del resultado del etiquetado.** Una proporcion alta de los hallazgos lleva simultaneamente una
etiqueta `[A-*]` y una `[B-OE2]`. Eso no es una anomalia: B-OE2 es literalmente un objetivo de analisis
exploratorio sobre el mismo dominio, y un EDA riguroso sobre el universo completo sirve a ese objetivo
del mismo modo que sirve a A-OE03 y A-OE04. La coincidencia de utilidad es consecuencia de que los dos
trabajos comparten dominio y fuente, no de que compartan trabajo.

**Productos persistidos:** `data/hallazgos_maestra.csv`, `data/cobertura_objetivos.csv`,
`data/estado_insights.csv`, `data/estado_brechas.csv`, `data/contradicciones_con_eda_previo.csv`,
`figuras/11_distribucion_etiquetas.png`, `docs/HALLAZGOS_ETIQUETADOS.md`.

---

## Figuras producidas por este cuaderno

- `figuras/11_distribucion_etiquetas.png`
