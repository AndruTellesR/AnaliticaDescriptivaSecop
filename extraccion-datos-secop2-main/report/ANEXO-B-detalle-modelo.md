# Anexo B — Detalle técnico del modelo final

Documento complementario al Informe Final del Trabajo Dirigido. Reúne
los detalles técnicos del modelo predictivo final, los hiperparámetros
óptimos de los ocho algoritmos evaluados y la justificación detallada
de las decisiones técnicas tomadas durante la fase de modelado.

---

## B.1. Modelo seleccionado

El modelo final del proyecto es un **LightGBM** con calibración fina de
hiperparámetros, entrenado sobre el dataset enriquecido v2 (152 features
predictoras tras encoding e imputación). Se persiste en
`modelo_predictivo_global/data/modelos/lgbm.pkl` y se acompaña de los
artefactos de preprocesamiento necesarios para la inferencia.

### Hiperparámetros óptimos

| Hiperparámetro | Valor | Justificación |
|----------------|-------|---------------|
| `n_estimators` | 800 | Mayor número de árboles permite refinar la estimación gradualmente con learning_rate bajo |
| `num_leaves` | 127 | Permite árboles asimétricos amplios que capturan combinaciones específicas de features |
| `max_depth` | −1 (sin límite) | El control de complejidad se delega a `num_leaves` y `min_child_samples` |
| `learning_rate` | 0,020 | Tasa baja para reducir overfitting con muchos árboles |
| `min_child_samples` | 50 | Requiere al menos 50 muestras por hoja, evita hojas con poca evidencia |
| `subsample` | 0,664 | Bagging del 66 % de las muestras por iteración |
| `colsample_bytree` | 0,816 | Cada árbol usa un 82 % aleatorio de las features |
| `scale_pos_weight` | (calculado por target) | Compensa el desbalance de clases por target |

### Métricas finales sobre el conjunto de prueba

| Target | AUC | F1 | Precisión | Recall | Exactitud |
|--------|-----|------|-----------|--------|-----------|
| `tuvo_atraso` | 0,9091 | 0,8503 | 0,8672 | 0,8341 | 0,8268 |
| `tuvo_sobrecosto` | 0,8338 | 0,8731 | 0,8896 | 0,8572 | 0,8071 |

## B.2. Resultados completos del zoológico

Resultados de los ocho algoritmos sobre el target principal `tuvo_atraso`:

| Modelo | CV AUC | Test AUC | F1 | Precisión | Recall | Exactitud | n_iter | Tiempo |
|--------|--------|----------|------|-----------|--------|-----------|--------|--------|
| LightGBM | 0,9094 | **0,9091** | 0,8503 | 0,8672 | 0,8341 | 0,8268 | 50 | 380 s |
| XGBoost | 0,9085 | 0,9069 | 0,8500 | 0,8765 | 0,8250 | 0,8238 | 50 | 186 s |
| Random Forest | 0,8982 | 0,8996 | 0,8489 | 0,8262 | 0,8729 | 0,8120 | 40 | 368 s |
| MLP | 0,8700 | 0,8630 | 0,8263 | 0,8147 | 0,8382 | 0,7868 | 20 | 86 s |
| Logistic Regression | 0,8424 | 0,8402 | 0,7982 | 0,8243 | 0,7737 | 0,7634 | 40 | 93 s |
| SVM lineal | 0,8397 | 0,8381 | 0,8144 | 0,7705 | 0,8635 | 0,7619 | 15 | 223 s |
| KNN | 0,8258 | 0,8333 | 0,8077 | 0,7565 | 0,8663 | 0,7505 | 25 | 176 s |
| Naive Bayes | 0,7492 | 0,7519 | 0,3482 | 0,9952 | 0,2110 | 0,5222 | 20 | 8 s |

## B.3. Hiperparámetros óptimos de cada algoritmo

### B.3.1. Logistic Regression

- `C`: 0,5343
- `penalty`: `l2`
- `solver`: `lbfgs`
- `class_weight`: `balanced`
- `max_iter`: 2000

### B.3.2. K-Nearest Neighbors

- `n_neighbors`: 51
- `weights`: `distance`
- `metric`: `manhattan`
- `n_jobs`: −1

### B.3.3. SVM lineal calibrado

- `estimator__C`: 1,3311
- `estimator__class_weight`: None
- Calibración: `CalibratedClassifierCV` con método sigmoide y CV=3

### B.3.4. Random Forest

- `n_estimators`: 300
- `max_depth`: 30
- `min_samples_split`: 5
- `min_samples_leaf`: 1
- `max_features`: `sqrt`
- `class_weight`: None

### B.3.5. XGBoost

- `n_estimators`: 300
- `max_depth`: 10
- `learning_rate`: 0,0239
- `colsample_bytree`: 0,8887
- `gamma`: 1,1799
- `reg_alpha`: 0,1355
- `reg_lambda`: 0,1666
- `subsample`: 0,7757

### B.3.6. LightGBM (modelo final)

- `n_estimators`: 800
- `num_leaves`: 127
- `max_depth`: −1
- `learning_rate`: 0,0200
- `min_child_samples`: 50
- `subsample`: 0,6645
- `colsample_bytree`: 0,8159

### B.3.7. Gaussian Naive Bayes

- `var_smoothing`: 5,06e−07

### B.3.8. Multi-Layer Perceptron

- `hidden_layer_sizes`: (100, 100)
- `activation`: `relu`
- `alpha`: 0,0034
- `learning_rate_init`: 0,0076
- `early_stopping`: True
- `max_iter`: 300

## B.4. Experimento de estrategias de tuning

Resultados del experimento adicional comparando cuatro estrategias de
búsqueda de hiperparámetros sobre XGBoost:

| Estrategia | CV AUC | Desv. estándar | Tiempo | Iteraciones efectivas |
|------------|--------|----------------|--------|------------------------|
| Grid Search reducido | 0,9101 | 0,0026 | 435 s | 288 |
| Bayesian Optimization (Optuna TPE) | 0,9103 | 0,0026 | 329 s | 80 trials |
| Random Search | 0,9089 | 0,0027 | 88 s | 80 |
| Halving Random Search | 0,8293 | 0,0234 | 10 s | 119 |

Conclusión: Grid Search y Bayesian Optimization empatan virtualmente,
Random Search ofrece compromiso aceptable de tiempo, Halving Random
Search fracasa por descartes prematuros.

## B.5. Variables seleccionadas y su importancia

Las 30 variables sobrevivientes a la cascada de selección, ordenadas por
importancia por permutación:

| Pos | Feature | MI | Permutación |
|---|---|---|---|
| 1 | `duracion_planificada_dias` | 0,217 | 0,230 |
| 2 | `duracion_planificada_dias_was_nan` | 0,069 | 0,122 |
| 3 | `valor_del_contrato` | 0,086 | 0,012 |
| 4 | `estado_bpin_No Válido` | 0,006 | 0,009 |
| 5 | `ciudad_freq` | 0,025 | 0,007 |
| 6 | `sector_freq` | 0,009 | 0,006 |
| 7 | `log_valor_contrato` | 0,085 | 0,006 |
| 8 | `localizaci_n_freq` | 0,032 | 0,006 |
| 9 | `departamento_freq` | 0,014 | 0,005 |
| 10 | `codigo_de_categoria_principal_freq` | 0,016 | 0,005 |
| 11 | `anios_empresa` | 0,015 | 0,004 |
| 12 | `modalidad_de_contratacion_Mínima cuantía` | 0,014 | 0,003 |
| 13 | `recursos_propios_alcald_as_freq` | 0,008 | 0,003 |
| 14 | `recursos_propios_freq` | 0,010 | 0,003 |
| 15 | `modalidad_de_contratacion_Contratación directa` | 0,001 | 0,003 |
| 16–30 | Variables adicionales con permutación < 0,003 | — | — |

## B.6. Decisiones técnicas justificadas

### Por qué se descartó la variable `tuvo_atraso_o_sobrecosto`

La variable combinada presentaba prevalencia del 89,1 %, lo cual la
convertía en un objetivo trivial. Un clasificador que siempre predice 1
alcanzaría exactitud del 89 % sin aportar valor predictivo. La elección
de `tuvo_atraso` (60,5 % positivos) como target principal garantiza que
el modelo deba aprender genuinamente la señal del problema.

### Por qué se eligió arquitectura multi-target en lugar de dos modelos separados

La verificación empírica mostró que la arquitectura multi-target no
degrada el desempeño respecto a modelos especializados (de hecho lo
mejora marginalmente en el caso del Random Forest). Las ventajas
operativas adicionales son: un solo pipeline de inferencia, una sola
versión a mantener, garantía de consistencia entre los dos targets
sobre el mismo vector de entrada.

### Por qué se eligió Random Search por defecto y luego Grid Search final

Random Search es eficiente para espacios de búsqueda amplios con
variables continuas (learning rate, subsample), donde una búsqueda
exhaustiva sería prohibitiva. Una vez identificada una región
prometedora del espacio mediante Random Search, se aplicó Grid Search
sobre un grid manual centrado en esa región para encontrar el óptimo
fino. Esta combinación equilibra eficiencia computacional y precisión.

### Por qué se descartó SVM RBF

SVM con kernel RBF tiene complejidad cuadrática en el número de muestras.
Con 38.664 muestras de entrenamiento, el tiempo de cómputo sería
prohibitivo (orden de horas por entrenamiento, miles de horas para una
búsqueda completa de hiperparámetros). Se adoptó la variante lineal
(LinearSVC) con calibración posterior mediante `CalibratedClassifierCV`,
que es factible computacionalmente y se desempeñó comparablemente.

### Por qué se eligió Frequency Encoding sobre Target Encoding

Target Encoding (reemplazar cada categoría por la media del target en
esa categoría) es más potente que Frequency Encoding pero introduce
riesgo de fuga de información si no se calcula con validación cruzada
interna. Frequency Encoding ofrece un compromiso favorable: captura una
señal estadística estable (categorías más frecuentes suelen
corresponder a flujos operativos más maduros) sin riesgo de leakage.
Target Encoding queda como mejora opcional si las métricas no llegan al
objetivo en futuras iteraciones.

### Por qué se aplicó winsorización p1/p99 en lugar de p5/p95

Recortar el 2 % extremo (p1/p99) preserva el 98 % de la masa de datos y
neutraliza solo los valores manifiestamente erróneos. Recortar el 10 %
(p5/p95) sería demasiado destructivo y eliminaría observaciones legítimas
con valores genuinamente altos o bajos. La elección se confirma porque
los outliers detectados en el dataset (duraciones de millones de días,
valores de 10¹³ pesos) son claramente errores de carga, no
observaciones reales.

## B.7. Reproducibilidad

Toda la fase de modelado utiliza una semilla aleatoria fija
(`random_state = 42`) en todos los procesos estocásticos: división
train/test, bootstrap en Random Forest, inicialización de XGBoost y
LightGBM, validación cruzada estratificada, Random Search.

Los datasets intermedios se persisten en formato Apache Parquet, los
modelos en formato joblib, los mapas de codificación y los hiperparámetros
óptimos en pickle. Cualquier resultado del informe puede ser auditado o
reproducido ejecutando los notebooks numerados en orden.

## B.8. Comparativa entre las dos versiones del modelo

| Métrica | v1 (XGBoost tuneado, dataset depurado) | v2 (LightGBM, dataset enriquecido) |
|---------|----------------------------------------|-------------------------------------|
| Features predictoras | 94 (30 seleccionadas) | 152 (30 seleccionadas) |
| AUC test atraso | 0,9088 | 0,9091 |
| F1 test atraso | 0,8522 | 0,8503 |
| AUC test sobrecosto | 0,8358 | 0,8338 |
| F1 test sobrecosto | 0,8508 | 0,8731 |
| Tiempo entrenamiento | 65 s | 380 s |

La versión v2 se selecciona como modelo final por completitud
metodológica y mejor F1 en sobrecosto, a pesar de la mejora marginal en
AUC. Las variables estructurales adicionales aportan información
limitada (Δ AUC atraso = +0,0003), confirmando que el dataset v1 ya
capturaba la mayor parte de la señal predictiva accesible.
