# PROMPT — EDA EXTENSO E INDEPENDIENTE PARA OE-02 Y OE-03 (ANALITICA DESCRIPTIVA)

## Como usar este archivo

Este es un prompt completo, listo para pegarse en una nueva sesion de Claude Code (o continuar en esta) con acceso al repositorio `/home/william-telles/Documentos/extraccion-datos-secop2-main (1)/extraccion-datos-secop2-main/`. No ha sido ejecutado todavia. Especifica con precision que construir, con que datos, bajo que reglas de autoria, y con que nivel de rigor academico, para producir un Analisis Exploratorio de Datos (EDA) extenso, propio e independiente, orientado a cerrar las brechas de OE-02 y OE-03 identificadas en `MATRIZ_OBJETIVOS_CODIGO.md`.

---

## 1. Rol y encuadre

Actua como analista de datos senior con perfil de asesor de trabajo de grado en Ingenieria de Sistemas y evaluador de jurado de proyectos de analitica descriptiva. El proyecto es de caracter **analitico-descriptivo**, no predictivo: no se entrenan modelos de clasificacion/regresion supervisada, no se reporta AUC/F1/accuracy de ningun clasificador, y no se usa `scikit-learn`, `xgboost` ni `lightgbm` para nada en este ejercicio. El criterio de exito no es la capacidad predictiva de un modelo, sino la calidad, profundidad y rigor estadistico de la caracterizacion descriptiva e inferencial exploratoria del comportamiento contractual, bajo el marco teorico de la restriccion de hierro (tiempo, costo, alcance).

---

## 2. Contexto y objetivo del ejercicio

Este repositorio contiene, en paralelo, el trabajo de grado descriptivo de Andres Telles (`InformesRev/AnteproyectoAndres.md`) y un proyecto predictivo de un companero de tesis (Angel Garcia, bajo el mismo director), documentados y diferenciados en `InformesRev/RESUMEN_CONTROL.md`, `InformesRev/RESUMEN_CODIGO.md` y `MATRIZ_OBJETIVOS_CODIGO.md` (todos ya existentes en `InformesRev/`, leerlos primero completos antes de escribir una sola linea de codigo).

`MATRIZ_OBJETIVOS_CODIGO.md` establecio que:
- OE-02 (modelo de datos analitico) esta en estado **Parcial**, sin modelo estrella formal, recomendando como Camino B un **modelo dimensional simplificado** (tabla de hechos + dimensiones sobre Parquet, con diagrama y diccionario de convenciones).
- OE-03 (normalizacion) esta en estado **Parcial**, con deteccion de calidad de datos ya hecha mas arriba en el pipeline compartido, pero **sin umbrales cuantitativos de calidad** y **sin los indicadores continuos de tiempo/costo/alcance** que exige el anteproyecto (numeral 3.3): los unicos indicadores existentes en el repositorio son flags binarios (`tiempo`, `presupuesto`, `alcance`) construidos en `notebooks/07_depuracion_variables_modelo.ipynb` para el modelado predictivo del companero, y son **codigo excluido** (no se puede usar ni como referencia de logica de calculo).

El objetivo de este ejercicio es **construir de cero, de forma independiente**, una serie de notebooks que: (a) reestructuren el dataset integrado en un modelo dimensional simplificado (cierra brecha de OE-02); (b) definan y apliquen umbrales cuantitativos de calidad (cierra parte de la brecha de OE-03); (c) deriven los indicadores continuos/categoricos de tiempo, costo y alcance directamente desde la definicion del propio anteproyecto, sin ninguna dependencia del notebook 07; y (d) realicen un EDA extenso, riguroso y con contrastacion de hipotesis, que produzca conclusiones e insights citables en el capitulo de resultados de la tesis.

---

## 3. Reglas de blindaje de autoria (obligatorias, no negociables)

1. **No leer, no copiar, no parafrasear la logica de** `notebooks/07_depuracion_variables_modelo.ipynb` ni `notebooks/08_integracion_rup_no_consorcios.ipynb`. Estos notebooks estan clasificados como "CODIGO DEL COMPANERO - EXCLUIR" en `MATRIZ_OBJETIVOS_CODIGO.md`, seccion 4. Cualquier formula de indicador debe derivarse **exclusivamente** de la definicion textual del anteproyecto (`InformesRev/AnteproyectoAndres.md`, numeral 3.3), no de inspeccionar como el companero los calculo.
2. **No usar, copiar ni citar** `modelo_predictivo_global/`, `modelo-predictivo-preliminar/`, `extractor-indicadores-docker/`, `entregables/05-modelos/`, `entregables/07-notebooks/modelado-v1/` y `modelado-v2/`, `entregables/08-codigo-fuente/`, `report/`, `scripts/gemini/`, `scripts/extraer_rup_auto.py`, `scripts/extraer_indicadores_pliegos.py`, ni `modelo_predictivo_global/data/cols_leakage.txt`. Ninguno de estos aporta a OE-02/OE-03 de Andres.
3. **No modificar ni ejecutar** `notebooks/00` a `06` ni `scripts/generar_diccionario_datos.py`/`generar_diccionario_md.py`. Estos siguen con autoria "A CONFIRMAR CON DIRECTOR" (mismo pipeline compartido); este EDA los trata como **fuente de datos de solo lectura**, no como codigo a extender ni a modificar.
4. **Advertencia de dependencia de datos que debe quedar escrita en el primer notebook, en una celda markdown, sin excepcion:** el dataset de entrada (`entregables/04-datasets/contratos_adiciones_obra.parquet`) fue producido por el pipeline compartido (notebooks 00-06), cuya autoria aun no ha sido confirmada por el director (ver `MATRIZ_OBJETIVOS_CODIGO.md`, tarea prioridad 1). Este EDA es independiente en **codigo y logica analitica**, pero **no elimina** la necesidad de esa confirmacion respecto al **dato crudo integrado**. Documentar esto explicitamente evita cualquier ambiguedad ante el jurado.
5. Todo notebook nuevo debe crearse en una carpeta **nueva y separada**, nunca dentro de `notebooks/` (que es del pipeline compartido) ni dentro de ninguna carpeta ya clasificada como del companero.

---

## 4. Fuente de datos a usar

- **Dataset base:** `entregables/04-datasets/contratos_adiciones_obra.parquet` (48.331 filas x 125 columnas segun `entregables/04-datasets/README.md` — verificar la dimension real al cargarlo, no asumirla).
- Enriquecer unicamente si faltan columnas necesarias con `entregables/04-datasets/contratos_electronicos_obra.parquet` (87 columnas, fuente madre) y `entregables/04-datasets/proveedores_obra.parquet` (25 columnas, para tipo de contratista/tamano de empresa), usando las mismas llaves de integracion ya documentadas y verificadas (`proceso_de_compra` = `id_del_portafolio`, `codigo_proveedor` = `codigo`) — citar `doc/contexto/CONTEXTO.md` como referencia de las llaves, no como codigo a ejecutar.
- **No usar** `consolidado_global.parquet` ni `consolidado_imputado.parquet` (son productos del pipeline de modelado del companero: winsorizados, codificados e imputados con criterios de ML, no aptos como insumo de un EDA descriptivo independiente).
- Antes de cualquier calculo, imprimir y documentar en una celda markdown: numero real de filas/columnas cargadas, lista de columnas disponibles relevantes para tiempo/costo/alcance y para las variables independientes de la seccion 3.3 del anteproyecto (modalidad de seleccion, tipo de contratista, cuantia inicial, sector, nivel territorial, region geografica). Si alguna columna esperada no existe con ese nombre exacto, buscar el nombre real (los campos SECOP llegan con normalizacion de Socrata, por ejemplo `duraci_n_del_contrato`, `liquidaci_n`) y dejarlo documentado, no asumirlo.

---

## 5. Notebooks a crear (carpeta nueva, ej. `analitica-descriptiva-andres/notebooks/`)

Numerar y nombrar de forma clara. Cada notebook debe iniciar con una celda markdown de proposito, insumos, y a que OE responde, y cerrar con una celda markdown de sintesis de hallazgos de esa etapa (no dejar el analisis sin conclusion parcial).

### 01 — Reestructuracion en modelo dimensional simplificado (cierra brecha OE-02)
- Cargar el dataset base y separarlo explicitamente en una **tabla de hechos** (`hechos_contratos`: llaves foraneas + medidas: valor del contrato, duracion planificada, valor pagado si esta disponible sin ser leakage para este proposito descriptivo) y **tablas de dimension** (`dim_proceso`, `dim_proveedor`, `dim_entidad`, `dim_modalidad`, `dim_territorio`), persistidas como Parquet independientes en una subcarpeta `data/modelo_dimensional/`.
- Producir un diagrama (Mermaid o imagen) del esquema de hechos/dimensiones y un diccionario de convenciones (nombre de cada tabla, grano, llaves).
- Documentar explicitamente que esto es un modelo dimensional **simplificado sobre archivos Parquet**, no un motor relacional formal (segun lo aprobado en `MATRIZ_OBJETIVOS_CODIGO.md`, seccion 7, Camino B de OE-02), dejando la limitacion redactada tal como se sugirio alli.

### 02 — Calidad de datos con umbrales cuantitativos (cierra parte de brecha OE-03)
- Definir explicitamente, con justificacion, umbrales cuantitativos propios (ejemplo: nulidad maxima aceptable por variable, cobertura minima de cada join heredado). No copiar umbrales de ningun documento del companero.
- Aplicar los umbrales sobre el dataset base y reportar, por columna, si pasa o no el umbral, con una tabla resumen.
- Documentar el criterio de deduplicacion aplicado (cual registro se conserva y por que), de forma independiente a lo que haga el pipeline compartido.

### 03 — Derivacion independiente de los indicadores de tiempo, costo y alcance (nucleo de OE-03 y de la restriccion de hierro)
- **Desviacion de tiempo:** derivar la diferencia entre plazo pactado y plazo real de ejecucion, en dias, siguiendo literalmente la definicion del numeral 3.3 del anteproyecto. Documentar la formula exacta usada y las columnas fuente reales (verificadas en el paso 4).
- **Desviacion de costo:** derivar el porcentaje de adicion presupuestal (diferencia entre valor inicial y valor final del contrato, como % del valor inicial), tambien segun el numeral 3.3.
- **Indice de cumplimiento de alcance:** derivar un indicador **categorico** (entregado en su totalidad / parcialmente / no entregado), no binario, segun la definicion del anteproyecto — no el binario `alcance` del companero.
- Cada formula debe quedar documentada en una celda markdown citando explicitamente "Anteproyecto, numeral 3.3" como fuente, no ningun notebook del companero.
- Guardar el resultado como un nuevo dataset propio (ej. `data/indicadores_restriccion_hierro.parquet`), separado de cualquier artefacto del companero.

### 04 — EDA univariado: distribuciones y outliers
- Distribuciones de los tres indicadores continuos/categoricos recien creados y de las variables independientes clave (modalidad, tipo de contratista, cuantia, sector, nivel territorial, region).
- Box plots de outliers para las variables continuas (duracion, valor del contrato, desviacion de tiempo, desviacion de costo), siguiendo la exigencia explicita de OE-04/RF-05 del anteproyecto (aunque el dashboard interactivo se construya despues, el contenido analitico de estos box plots debe quedar listo aqui).
- Reportar medidas de tendencia central y dispersion apropiadas segun la forma de la distribucion (mediana/RIC si hay asimetria, no solo media/desviacion estandar).

### 05 — EDA segmentado: modalidad, entidad y territorio
- Segmentar los tres indicadores por modalidad de contratacion, tipo de contratista, nivel territorial (orden) y region/departamento, tal como exige el anteproyecto (numeral 1.4.2, OE-04, y modulo de indicadores de la tabla de la seccion 14 de `RESUMEN_CONTROL.md`).
- Tablas de contingencia y visualizaciones comparativas (no solo texto) para cada segmentacion.

### 06 — Analisis correlacional y de asociacion
- Correlaciones entre variables continuas (valor del contrato, duracion planificada, desviacion de tiempo, desviacion de costo), eligiendo el coeficiente apropiado segun la escala y la forma de la distribucion (Pearson si hay linealidad y normalidad razonable, Spearman si no).
- Asociacion entre variables categoricas (modalidad, tipo de contratista) y el indice de alcance categorico, usando tablas de contingencia con la prueba apropiada (ver seccion 6 de este prompt).
- Explicitar siempre que correlacion/asociacion no implica causalidad, dado el caracter descriptivo-analitico (no causal) del proyecto.

### 07 — Contraste exploratorio de las hipotesis H1, H2 y H3 del anteproyecto
Ver seccion 6 de este prompt para el detalle metodologico exigido. Debe quedar un notebook dedicado exclusivamente a esto, con una subseccion por hipotesis (H1: modalidad de seleccion vs. desviaciones de costo/tiempo; H2: consorcios/UT vs. adiciones y modificaciones; H3: NBI territorial vs. desviaciones de tiempo/costo).

### 08 — Sintesis de hallazgos e insights (capitulo de resultados)
- Consolidar, en lenguaje de tesis (no de notebook tecnico), los hallazgos de los notebooks 04 a 07.
- Relacionar cada hallazgo explicitamente con el marco teorico de la restriccion de hierro (Atkinson, 1999; Meredith & Mantel, 2012) y, cuando aplique, con los antecedentes citados en el anteproyecto (Rodriguez Arevalo, 2021; Feigenbaum et al., 2024).
- Declarar explicitamente las limitaciones del analisis (cobertura parcial de joins ya documentada, variables extranas no controladas segun numeral 3.3 del anteproyecto, naturaleza exploratoria no causal de las pruebas de hipotesis).
- Este notebook (o un `.md` derivado de el) es el que debe alimentar directamente el capitulo de resultados/discusion de la tesis y, mas adelante, el contenido del dashboard de OE-04.

---

## 6. Rigor estadistico exigido para el analisis inferencial (notebooks 06 y 07)

No reportar unicamente un p-valor. Para cada prueba:
1. Justificar por que se elige esa prueba (tipo de variable, supuestos aplicables).
2. Verificar supuestos antes de aplicar pruebas parametricas (normalidad con Shapiro-Wilk o inspeccion grafica sobre muestras grandes, homogeneidad de varianzas con Levene) y usar la alternativa no parametrica si no se cumplen (Mann-Whitney U o Kruskal-Wallis en lugar de t-test/ANOVA cuando corresponda).
3. Para variables categoricas vs. categoricas (ej. modalidad vs. cumplimiento de alcance categorico): prueba chi-cuadrado de independencia, reportando tambien un tamano de efecto (V de Cramer), no solo el p-valor.
4. Para diferencias de medianas/medias entre grupos (ej. H2: consorcios vs. personas juridicas individuales en numero de adiciones): Mann-Whitney U (2 grupos) o Kruskal-Wallis (mas de 2 grupos), con tamano de efecto correspondiente.
5. Declarar el nivel de significancia usado (ejemplo, alfa = 0.05) antes de las pruebas, no despues.
6. Mantener explicito en todo momento, tal como el propio anteproyecto lo aclara (numeral 3.2), que estas pruebas son **orientadoras/exploratorias** y no constituyen inferencia causal ni generalizacion poblacional formal mas alla de lo que permite el diseno censal condicionado del estudio.
7. Reportar los resultados en una tabla resumen por hipotesis: variable(s) involucradas, prueba usada, estadistico, p-valor, tamano de efecto, conclusion en lenguaje llano.

---

## 7. Estandar de documentacion exigido (nivel de rigor de jurado de tesis)

- Cada notebook debe combinar codigo con celdas markdown narrativas que expliquen el **porque** de cada decision tecnica (no solo el que), siguiendo el mismo estandar narrativo ya usado en `notebooks/00-06` (con markdown headers `##`/`###` por seccion), pero en la carpeta nueva e independiente.
- Ademas de los notebooks, generar un documento `.md` de sintesis por notebook (o uno consolidado final) dentro de una carpeta `analitica-descriptiva-andres/docs/`, en el mismo espiritu que `doc/fase2_comprension_datos/` y `doc/fase3_preparacion_datos/` ya existentes en el repositorio, pero **en una carpeta propia y separada** para no mezclarse documentalmente con las fases del companero.
- Todas las cifras, tablas y graficos deben ser reproducibles desde el propio notebook (no copiar cifras de otros documentos sin recalcularlas).
- Citar el anteproyecto (`InformesRev/AnteproyectoAndres.md`) por numeral exacto cada vez que se derive una definicion de el (indicadores, hipotesis, variables).

---

## 8. Reglas de calidad academica transversales

1. No usar en ningun momento terminologia ni metricas de modelado predictivo (no "accuracy", no "AUC", no "features", no "target" en el sentido de ML) — usar terminologia de analitica descriptiva/inferencial (indicador, variable dependiente/independiente, distribucion, asociacion).
2. No ejecutar ni importar `scikit-learn`, `xgboost`, `lightgbm` ni ninguna libreria de modelado supervisado en ninguno de estos notebooks.
3. Declarar siempre el tamano de muestra efectivo usado en cada analisis (despues de excluir nulos), no solo el tamano del dataset completo.
4. Si una cobertura de datos es baja para alguna variable (ej. proveedores con 54.4% de cobertura segun hallazgos ya documentados), declarar explicitamente el posible sesgo de exclusion antes de interpretar resultados sobre esa variable.
5. Ningun hallazgo debe presentarse como conclusion definitiva sin matizar con las limitaciones del numeral 3.3 y 1.5.2 del anteproyecto (variables extranas no controladas, imposibilidad de verificacion externa caso a caso).

---

## 9. Ubicacion de archivos de salida

```
extraccion-datos-secop2-main/
└── analitica-descriptiva-andres/
    ├── notebooks/
    │   ├── 01_modelo_dimensional.ipynb
    │   ├── 02_calidad_umbrales.ipynb
    │   ├── 03_indicadores_restriccion_hierro.ipynb
    │   ├── 04_eda_univariado.ipynb
    │   ├── 05_eda_segmentado.ipynb
    │   ├── 06_correlaciones_asociaciones.ipynb
    │   ├── 07_contraste_hipotesis.ipynb
    │   └── 08_sintesis_hallazgos.ipynb
    ├── data/
    │   ├── modelo_dimensional/   (hechos_contratos.parquet, dim_*.parquet)
    │   └── indicadores_restriccion_hierro.parquet
    └── docs/
        ├── 01_modelo_dimensional.md
        ├── 02_calidad_umbrales.md
        ├── ...
        └── sintesis_hallazgos_finales.md
```

Esta carpeta debe quedar completamente separada de `notebooks/`, `modelo_predictivo_global/`, `modelo-predictivo-preliminar/`, `entregables/` y `report/`.

---

## 10. Que reportar al finalizar la ejecucion de este prompt

Al completar los 8 notebooks y su documentacion, reportar en maximo 25 lineas:
- Resumen del modelo dimensional construido (tablas de hechos/dimensiones, con conteo de filas de cada una).
- Umbrales de calidad definidos y cuantas variables/filas quedaron dentro/fuera de ellos.
- Formulas finales usadas para los tres indicadores (tiempo, costo, alcance), con su fuente citada (numeral 3.3 del anteproyecto).
- Principales hallazgos de la segmentacion por modalidad/entidad/territorio (2-3 hallazgos mas relevantes).
- Resultado resumido de H1, H2 y H3 (soportada / no soportada / parcial, con el estadistico y p-valor de cada una).
- Limitaciones declaradas explicitamente.
- Confirmacion de que ningun archivo de `modelo_predictivo_global/`, `modelo-predictivo-preliminar/`, `entregables/05-11`, `report/`, `scripts/gemini/` ni `notebooks/07-08` fue leido, copiado o modificado durante el ejercicio.
