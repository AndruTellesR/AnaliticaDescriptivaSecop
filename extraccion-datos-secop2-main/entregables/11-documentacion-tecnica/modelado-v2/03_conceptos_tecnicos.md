# Documento 03 — Conceptos técnicos y decisiones de diseño

Compendio de definiciones y justificaciones de las decisiones técnicas
tomadas en el modelo predictivo global v2. Pensado como material de
sustentación académica.

## Índice

1. CRISP-DM
2. Train/test split y estratificación
3. K-Fold Cross Validation
4. Data leakage
5. Imputación de valores faltantes
6. Codificación de variables categóricas
7. Escalado de características
8. Métricas de clasificación
9. Class imbalance
10. Algoritmos del zoológico
11. Hyperparameter tuning
12. Feature importance
13. Overfitting y regularización
14. Threshold tuning y costo asimétrico
15. SHAP para explicabilidad

---

## 1. CRISP-DM

**Cross-Industry Standard Process for Data Mining**: metodología
de seis fases para proyectos de data science y machine learning,
publicada por el consorcio CRISP-DM en 1999 y vigente como referencia
industrial.

### Fases

1. **Business Understanding**: definir objetivos y criterios de éxito
   en términos del problema de negocio.
2. **Data Understanding**: recolección inicial, exploración y verificación
   de calidad de los datos.
3. **Data Preparation**: limpieza, transformación, integración y
   construcción del dataset analítico.
4. **Modeling**: selección de algoritmos, entrenamiento, ajuste.
5. **Evaluation**: validar que el modelo cumple los objetivos de negocio
   y revisar el proceso completo.
6. **Deployment**: integrar el modelo al flujo operativo y monitorear.

### Iteratividad

Las flechas entre fases son bidireccionales. Es esperable y deseable
volver a fases anteriores cuando un hallazgo lo amerite:
- Descubrir leakage en fase 4 → volver a fase 3 para depurar features.
- Comprobar baja capacidad predictiva → volver a fase 2 (explorar nuevas
  fuentes de datos).

### Justificación de uso

El proyecto sigue CRISP-DM porque (i) es la metodología estándar
documentada en la literatura académica de ML aplicado, (ii) cubre
explícitamente la articulación con objetivos de negocio (no solo
métricas), y (iii) permite documentar iteraciones, lo cual es relevante
para la trazabilidad de un trabajo de grado.

---

## 2. Train/Test Split y estratificación

### Definición

Dividir el dataset en dos subconjuntos disjuntos:
- **Train**: entrena el modelo (aprende parámetros internos).
- **Test**: evalúa el desempeño final sobre datos no vistos.

### Estratificación (`stratify=y`)

En clasificación con clases desbalanceadas, garantiza que la proporción
de positivos en train y test sea idéntica a la del dataset completo.
Sin estratificación, un split aleatorio puede producir conjuntos con
distribuciones distintas y métricas no comparables.

### Por qué 80/20 y `random_state = 42`

- **80/20**: convención estándar; maximiza datos de entrenamiento
  preservando un test set lo bastante grande (9.667 muestras) para
  métricas estables.
- **`random_state = 42`**: semilla fija → reproducibilidad. Cualquier
  re-ejecución del notebook produce el mismo split.

### Decisión en este proyecto

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y['tuvo_atraso'], random_state=42,
)
```

Resultado: 38.664 train × 9.667 test. Tasa de positivos preservada en
60,48 % en ambos.

---

## 3. K-Fold Cross Validation

### Definición

Particionar el train set en `K` folds (partes) y entrenar `K` veces:
- Cada iteración usa `K-1` folds para entrenar y 1 fold para validar.
- Cada muestra del train aparece exactamente una vez como validación.
- Las K métricas se promedian → estimación más estable que una única
  validación holdout.

### Stratified K-Fold

Cada fold mantiene la proporción de clases del train original. Crítico
en clases desbalanceadas (sin esto, un fold podría quedar 90 % positivos
y otro 30 %, sesgando la métrica).

### Por qué `K = 5`

Compromiso estándar:
- `K = 3`: barato pero alto sesgo y varianza de estimación.
- `K = 5`: balance probado en literatura; cada fold con ~7.700 muestras
  (suficiente estabilidad).
- `K = 10`: mejor estimación pero 2× costo computacional.

### Decisión

`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` para todos
los algoritmos del zoológico.

---

## 4. Data Leakage

### Definición

Información del target o del futuro que entra en las features de
entrenamiento, inflando artificialmente las métricas y produciendo un
modelo que no generaliza fuera del laboratorio.

### Ejemplos en este proyecto

| Columna | Razón |
|---------|-------|
| `tiempo`, `presupuesto`, `alcance` | Son los binarios que construyen los targets — entrenar con ellos = predecir lo mismo |
| `dias_adicionados`, `dias_hasta_primera_adicion` | Eventos post-firma del contrato |
| `valor_pagado`, `valor_facturado` | Métricas de ejecución, no se conocen al inicio |
| `n_modif_general`, `n_extension`, `n_cesion` | Conteos post-contractuales |
| `fecha_fin_contrato`, `fecha_primera_adicion` | Fechas que solo existen tras la ejecución |
| `liquidaci_n`, `estado_contrato` | Estados terminales del contrato |

### Estrategia aplicada

Documentar todas las cols leakage en `data/cols_leakage.txt` y excluirlas
explícitamente al construir el set de features. Total: 36 columnas
prohibidas.

---

## 5. Imputación de valores faltantes

### Definición

Reemplazar valores `NaN` por estimaciones para que algoritmos que no
toleran NaN (LR, KNN, SVM, MLP, NB) puedan operar.

### Estrategias evaluadas

| Estrategia | Cómo funciona |
|------------|---------------|
| **Mediana + flag** | Reemplaza NaN por la mediana de la columna y agrega un binario `<col>_was_nan` que señala si era NaN originalmente |
| KNN Imputer | Usa los k vecinos más cercanos (en feature space) para promediar |
| MICE Bayesian Ridge | Itera: imputa una columna usando las demás como regresores; bayesiano |
| MICE Random Forest | Como MICE pero con RF en lugar de regresión lineal |

### Justificación de la elección

Validada en sub-sprint consorcios (10.629 contratos):

| Estrategia | AUC downstream | Tiempo |
|------------|---------------|--------|
| **mediana + flag** | **0,8542** | 0,02 s |
| knn (k=5) | 0,8093 | 6 s |
| mice_br | 0,8066 | 44 s |
| mice_rf | 0,8015 | 34 s |

**Hallazgo central**: el flag `_was_nan` añade información sobre el
**patrón de ausencia** que correlaciona con el target (qué procesos
no permitieron extraer el dato suele estar ligado a la modalidad o al
tipo de entidad). Los métodos sofisticados eliminan esa señal al
"tapar el hueco" con un valor plausible.

### Decisión

Mediana + flag `_was_nan` en todas las cols numéricas con NaN. Se
persiste `imputer_mediana.pkl` para reuso en inferencia.

---

## 6. Codificación de variables categóricas

Los algoritmos de ML requieren entradas numéricas. La elección del
encoding depende de la **cardinalidad** y de la naturaleza ordinal o
nominal de la variable.

### Estrategias estándar

| Encoding | Cuándo usarlo | Riesgos |
|----------|---------------|---------|
| **One-Hot Encoding** | Categóricas nominales con baja cardinalidad (< 20) | Explosión de dimensiones si cardinalidad alta |
| **Frequency Encoding** | Cardinalidad alta sin ordinalidad clara | Pierde info de identidad; colisiones (dos categorías con misma frecuencia) |
| **Label Encoding** | Categóricas ordinales (ej. tamaño: pequeño/mediano/grande) | Inyecta orden artificial si no es ordinal |
| Target Encoding | Cardinalidad alta + cuando se quiere preservar señal | Leakage si no se hace con CV interno |

### Decisión

Umbral cardinalidad = **20**:

```python
if X[col].nunique() < 20:
    aplicar OHE
else:
    aplicar Frequency Encoding (persistir freq_map.pkl)
```

Esto resulta en:
- ~15 cols OHE → ~110 dummies generadas
- ~7 cols Frequency → 7 features continuas

NaN en categóricas se trata como categoría `'desconocido'` antes del
OHE para evitar pérdida de filas.

### Justificación

- OHE preserva la independencia entre categorías y permite que árboles
  hagan splits exactos.
- Frequency Encoding evita la explosión de dummies en variables como
  `ciudad` (1.000+ valores) o `codigo_de_categoria_principal` (1.506
  UNSPSC) y captura una señal débil pero estable: ciudades/categorías
  con más contratos tienen comportamientos más predecibles.
- Target Encoding se descartó por riesgo de leakage; queda como upgrade
  si el modelo no llega a métricas objetivo.

---

## 7. Escalado de características

### Definición

Transformar todas las features numéricas a una escala común (típicamente
media 0, desviación 1) para que ninguna domine por magnitud.

### Algoritmos que lo requieren

- **Logistic Regression**: la regularización L2 penaliza coeficientes
  con norma alta; sin escalado, features grandes se sobre-penalizan.
- **KNN**: las distancias euclídeas se dominan por features con escala
  mayor.
- **SVM**: el kernel y los márgenes dependen de la geometría del espacio.
- **MLP**: la convergencia de SGD se beneficia de inputs estandarizados.
- **NB (Gaussiano)**: las distribuciones asumidas son sensibles a escalas
  muy distintas.

### Algoritmos que NO lo requieren

- **Random Forest, XGBoost, LightGBM**: los árboles hacen splits por
  umbral; no dependen de la escala.

### Estrategia

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)   # sin volver a fit
```

Crítico: `fit` solo sobre train para no filtrar info del test
(forma de leakage).

---

## 8. Métricas de clasificación

### Definiciones

Para clasificación binaria con clases positiva (1) y negativa (0):

|  | Pred 0 | Pred 1 |
|---|---|---|
| Real 0 | TN | FP |
| Real 1 | FN | TP |

### Métricas

- **Accuracy** = (TP + TN) / (TP + TN + FP + FN) — engañosa en
  desbalance: predecir siempre la mayoritaria da accuracy alto.
- **Precision** = TP / (TP + FP) — calidad de las alertas positivas.
- **Recall (sensibilidad)** = TP / (TP + FN) — cobertura de positivos
  reales.
- **F1** = media armónica de Precision y Recall — penaliza si una de
  las dos cae mucho.
- **F-beta** = generalización de F1 con peso `β` al Recall.
- **AUC-ROC** = área bajo la curva Receiver Operating Characteristic
  (TPR vs FPR a distintos umbrales). Métrica **independiente del umbral**.
- **Brier Score** = MSE entre probabilidad predicha y label. Mide
  calibración.

### Priorización

**Métrica principal: AUC-ROC**
- Es independiente del umbral de decisión.
- Es robusta al desbalance.
- Es la métrica estándar reportada en literatura tabular.

**Desempate: F1**
- Cuando dos modelos empatan en AUC, el F1 mide cuál de los dos
  funciona mejor en el umbral operativo 0,5.

**Precision/Recall**: se reportan por completitud y para análisis FP/FN.

---

## 9. Class imbalance

### Definición

Cuando una clase aparece mucho más que la otra (ej. 60 % positivos vs
40 % negativos). El modelo tiende a sesgar predicciones hacia la
mayoritaria, perdiendo recall en la minoritaria.

### Soluciones

| Técnica | Cómo funciona | Cuándo usar |
|---------|---------------|-------------|
| **`class_weight='balanced'`** | LR/RF: penaliza más los errores en la clase minoritaria | Estándar para sklearn |
| **`scale_pos_weight`** | XGB/LGBM: ratio negativos/positivos en la pérdida | Estándar para gradient boosting |
| Oversampling (SMOTE) | Genera muestras sintéticas de la minoritaria | Cuidado: puede introducir ruido |
| Undersampling | Descartar muestras de la mayoritaria | Pierde información |

### Decisión

`tuvo_atraso` tiene 60,5 % positivos, 39,5 % negativos. Desbalance leve
pero suficiente para aplicar `class_weight='balanced'` (LR, RF) y
`scale_pos_weight = neg / pos = 0,653` (XGB, LGBM). Se evita SMOTE
porque introduce ruido en datasets categóricos con OHE.

---

## 10. Algoritmos del zoológico

Selección de 8 representantes de familias distintas, siguiendo
`pasos.md` del líder.

### 10.1 Logistic Regression (LR)

- **Familia**: lineal.
- **Idea**: combinación lineal de features + sigmoide → probabilidad.
- **Hiperparámetros**: `C` (inverso de regularización), `penalty` (L1/L2).
- **Cuándo usar**: línea base interpretable; cuando interesa el efecto
  marginal de cada feature.
- **Limitación**: no captura interacciones no-lineales.

### 10.2 K-Nearest Neighbors (KNN)

- **Familia**: lazy / basado en distancia.
- **Idea**: clasificar por mayoría entre los k vecinos más cercanos.
- **Hiperparámetros**: `n_neighbors`, `weights` (uniform/distance),
  `metric` (euclidean/manhattan).
- **Cuándo usar**: si los datos están en un espacio geométrico
  significativo.
- **Limitación**: lento en inferencia con muchos datos; sensible a
  curse of dimensionality.

### 10.3 Support Vector Machine (SVM)

- **Familia**: margen máximo.
- **Idea**: encontrar hiperplano que maximice el margen entre clases;
  puede usar kernel para mapear a espacio no-lineal.
- **Hiperparámetros**: `C`, `kernel` (linear/rbf), `gamma`.
- **Cuándo usar**: datasets pequeños/medianos con frontera de decisión
  compleja.
- **Limitación**: SVM RBF escala mal con muchos datos (complejidad
  cuadrática). En este proyecto se usó `LinearSVC` para 38k muestras.

### 10.4 Random Forest (RF)

- **Familia**: bagging (ensemble paralelo de árboles).
- **Idea**: entrenar muchos árboles independientes sobre muestras
  bootstrap + subconjuntos aleatorios de features; promediar votos.
- **Hiperparámetros**: `n_estimators`, `max_depth`, `min_samples_split`,
  `min_samples_leaf`, `max_features`.
- **Cuándo usar**: default robusto para tabular; baja varianza.
- **Limitación**: tiende a sobreajustar con `max_depth=None` si no se
  regulariza.

### 10.5 XGBoost (XGB)

- **Familia**: boosting (ensemble secuencial).
- **Idea**: entrena árboles uno a uno, cada uno corrigiendo errores del
  anterior; gradient descent en el espacio de funciones.
- **Hiperparámetros**: `n_estimators`, `learning_rate`, `max_depth`,
  `subsample`, `colsample_bytree`, `gamma`, `reg_lambda`, `reg_alpha`.
- **Cuándo usar**: SOTA tabular; cuando se busca máxima capacidad
  predictiva.
- **Ventajas**: manejo nativo de NaN (no usado aquí porque se imputa
  antes), `scale_pos_weight` para imbalance.

### 10.6 LightGBM (LGBM)

- **Familia**: boosting.
- **Idea**: similar a XGB pero usa histogramas y leaf-wise growth →
  más rápido en datasets medianos/grandes.
- **Hiperparámetros**: `n_estimators`, `learning_rate`, `num_leaves`,
  `max_depth`, `min_child_samples`.
- **Cuándo usar**: alternativa a XGB cuando el tiempo es crítico.

### 10.7 Gaussian Naive Bayes (NB)

- **Familia**: probabilístico.
- **Idea**: asume independencia condicional entre features dadas la
  clase; modela cada feature como distribución gaussiana por clase.
- **Hiperparámetros**: `var_smoothing`.
- **Cuándo usar**: línea base muy rápida; benchmark inferior.
- **Limitación**: la asunción de independencia se viola en la mayoría
  de problemas reales.

### 10.8 Multi-Layer Perceptron (MLP)

- **Familia**: red neuronal feed-forward.
- **Idea**: capas densas con activaciones no-lineales; entrenamiento
  por backpropagation.
- **Hiperparámetros**: `hidden_layer_sizes`, `alpha`, `learning_rate_init`,
  `activation`.
- **Cuándo usar**: cuando hay mucha data y la frontera es altamente
  no-lineal.
- **Limitación**: en tabular suele perder frente a boosting por la
  dificultad de capturar interacciones discretas con redes densas.

### Justificación de incluir 8

`pasos.md` exige cubrir el espectro de familias para tener evidencia
empírica robusta sobre cuál algoritmo es óptimo para este problema. Una
sola familia (ej. solo boosting) puede sesgar la conclusión.

---

## 11. Hyperparameter Tuning

### Definición

Hiperparámetros = parámetros del algoritmo que NO se aprenden de los
datos; se eligen antes del entrenamiento (ej. profundidad de árbol,
tasa de aprendizaje).

### Estrategias

| Estrategia | Idea | Costo | Cuándo |
|------------|------|-------|--------|
| **Grid Search** | Probar todas las combinaciones de una rejilla discreta | Alto (exponencial) | Pocas dimensiones, grid pequeño |
| **Random Search** | Muestrear N combinaciones aleatorias del espacio | Bajo (lineal en N) | Default eficiente; converge similar a Grid |
| **Halving Random** | Empezar con muchos candidatos y pocos recursos; descartar y promover | Muy bajo | Cuando recursos importan y HP no escalan con n_samples |
| **Bayesian (TPE)** | Aprende del histórico de trials, sugiere combos prometedores | Bajo | Espacios grandes y costosos |

### Decisión

`RandomizedSearchCV` con `n_iter = 40-50` para cada algoritmo:
- Más eficiente que Grid en alta dimensión.
- Convergencia comparable según literatura (Bergstra & Bengio 2012).
- Sin dependencias externas (sklearn nativo).

`scoring='roc_auc'`, `cv=StratifiedKFold(5)`, `refit=True` para que
sklearn entrene el mejor estimador automáticamente al final.

---

## 12. Feature Importance

### 12.1 Mutual Information (MI)

- **Definición**: medida de información compartida entre dos variables,
  basada en entropía. Captura dependencia (lineal o no) sin asumir
  forma funcional.
- **Pro**: rápido, simple, marginal univariado.
- **Contra**: no captura interacciones; trata cada feature aislada.

### 12.2 Permutation Importance

- **Definición**: entrena el modelo una vez. Para cada feature, permuta
  aleatoriamente sus valores en el test set, mide cuánto cae la métrica
  (AUC). Una caída grande → feature importante para ese modelo.
- **Pro**: modelo-específico, captura uso real.
- **Contra**: si dos features están correlacionadas, permutar una sola
  puede no caer la métrica (la info la sustituye la otra).

### Decisión

Se usan los **dos** en el notebook 03 para tener evidencia complementaria:
- MI muestra qué features tienen *potencial* informativo.
- Permutation Importance muestra qué features el modelo XGB realmente
  *usa* para predecir.

Las features que aparecen en ambos rankings son las más confiables.

---

## 13. Overfitting y regularización

### Definición

**Overfitting**: el modelo memoriza el train (incluyendo ruido) y
pierde capacidad de generalizar al test.

### Síntomas

- Métricas train >> métricas test.
- Modelo sensible a perturbaciones pequeñas.
- Alta varianza entre folds del CV.

### Técnicas de regularización aplicadas

| Algoritmo | Mecanismo |
|-----------|-----------|
| LR | Penalización L2 (`C` controla intensidad) |
| RF | Limitar `max_depth`, `min_samples_leaf` ≥ 2; bagging |
| XGB | `reg_lambda` (L2), `reg_alpha` (L1), `gamma` (mínima ganancia para split), `subsample`, `colsample_bytree` |
| LGBM | Análogo a XGB + `num_leaves` controla complejidad |
| MLP | `alpha` (L2 sobre pesos), `early_stopping` (detener antes que sobreajuste) |

### Validación

Stratified K-Fold CV es el control empírico. Si la métrica CV está
cercana a la métrica test → no hay overfitting catastrófico.

---

## 14. Threshold tuning y costo asimétrico

### Definición

Un clasificador devuelve probabilidad `p ∈ [0, 1]`. La decisión binaria
`pred = 1 if p ≥ τ` depende del umbral `τ` (default 0,5).

Mover `τ` mueve el trade-off Precision ↔ Recall:
- `τ` bajo → más alertas, más recall, menos precision.
- `τ` alto → menos alertas, más precision, menos recall.

### Por qué importa

En negocio el costo de un FP suele ser distinto al de un FN:
- En auditoría contractual: un FN (atraso no detectado) puede costar
  millones; un FP (auditoría innecesaria) cuesta horas-humano.
- → `τ` óptimo NO es 0,5; se elige minimizando el costo esperado.

### Cómo elegirlo

1. **F1-óptimo**: barrer `τ` de 0 a 1, elegir el que maximiza F1.
2. **Costo asimétrico**: definir `c_fp` y `c_fn`, minimizar
   `E[c_fp · FP + c_fn · FN]`.
3. **Constraint operativo**: ej. "no más de X% de alertas" → `τ`
   correspondiente al percentil.

### Decisión

Se reporta `τ = 0,5` como baseline. El análisis de threshold queda para
la fase de evaluación (Día 7 / Fase 5 CRISP-DM).

---

## 15. SHAP para explicabilidad

### Definición

**SHapley Additive exPlanations**: atribuye a cada feature una
contribución numérica a la predicción de un caso específico, basado en
valores de Shapley de teoría de juegos cooperativa.

### Propiedades

- **Aditividad**: la suma de las contribuciones SHAP iguala la predicción
  del modelo menos el valor base.
- **Local**: explica predicciones individuales.
- **Global**: agregando muchas explicaciones locales se obtienen
  importancias globales fieles.

### Outputs

- **Summary plot**: importancia global ranqueada.
- **Force plot / Waterfall**: para un caso específico, cómo cada feature
  empuja la probabilidad.
- **Dependence plot**: relación entre valor de feature y su contribución
  (captura no-linealidades).

### Por qué importa para el proyecto

- Cumple requerimiento de **explicabilidad** del OE3 (prototipo
  conversacional).
- Permite que el chatbot final responda "por qué este contrato tiene
  X % de riesgo".
- Detecta sesgos o features problemáticas que el modelo está usando.

### Implementación

`shap.TreeExplainer` para XGB/RF (eficiente, exacto en árboles).
Se aplica en la fase de evaluación final.

---

## Referencias rápidas

- Pedregosa et al. (2011). Scikit-learn: Machine Learning in Python.
- Chen & Guestrin (2016). XGBoost: A Scalable Tree Boosting System.
- Ke et al. (2017). LightGBM: A Highly Efficient Gradient Boosting
  Decision Tree.
- Bergstra & Bengio (2012). Random Search for Hyper-Parameter Optimization.
- Lundberg & Lee (2017). A Unified Approach to Interpreting Model
  Predictions (SHAP).
- Wirth & Hipp (2000). CRISP-DM: Towards a Standard Process Model for
  Data Mining.
