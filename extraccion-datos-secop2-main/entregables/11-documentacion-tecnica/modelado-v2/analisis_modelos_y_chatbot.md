# Análisis completo — Modelos v2, ganador, variables clave e interacción con el chatbot

Documento complementario que explica en detalle:
- Los 8 modelos entrenados
- El modelo ganador (LightGBM)
- Variables que aportan valor predictivo
- Diseño de interacción con el chatbot conversacional

---

## 1. Los 8 modelos del zoológico

Cada uno representa una familia distinta de Machine Learning. La idea:
cubrir todo el espectro para tener evidencia empírica de cuál algoritmo
aprende mejor el patrón del problema.

### 1.1 Logistic Regression (LR) — AUC 0,840

- **Familia**: lineal.
- **Cómo funciona**: combina las 154 features con pesos lineales, pasa
  por sigmoide → probabilidad. Cada feature aporta un coeficiente fijo.
- **Cuándo brilla**: cuando la frontera entre clases es aproximadamente
  lineal.
- **Por qué quedó 5º**: el problema tiene interacciones no-lineales
  (ej. duración × modalidad, depto × valor) que un modelo lineal no
  captura. Aún así, AUC 0,84 no es malo como baseline.
- **Mejor params**: `C=0,53` (regularización media), `class_weight='balanced'`.

### 1.2 K-Nearest Neighbors (KNN) — AUC 0,833

- **Familia**: distancia (lazy learning).
- **Cómo funciona**: para predecir un contrato nuevo, encuentra los k
  contratos más parecidos en el dataset de entrenamiento y vota por
  mayoría.
- **Cuándo brilla**: datasets pequeños con geometría natural.
- **Por qué quedó 7º**: 154 features con muchas dummies binarias →
  "curse of dimensionality" (todos los vecinos se ven igual de lejos).
  El mejor `k=51` confirma que vecindarios pequeños son puro ruido.
- **Mejor params**: `n_neighbors=51`, `metric='manhattan'`, `weights='distance'`.

### 1.3 SVM lineal calibrado (SVM) — AUC 0,838

- **Familia**: margen máximo.
- **Cómo funciona**: encuentra el hiperplano que separa mejor las dos
  clases maximizando el margen.
- **Por qué lineal y no RBF**: con 38.664 muestras + 154 features, SVM
  RBF tiene complejidad cuadrática → tomaría horas y memoria explota.
  Linear es factible.
- **Calibrado**: se agrega `CalibratedClassifierCV` porque LinearSVC
  nativamente no da probabilidades, solo distancia al hiperplano.
  Necesitamos `predict_proba` para el chatbot.
- **Por qué quedó 6º**: similar a LR (modelo lineal); empata casi
  exactamente.

### 1.4 Random Forest (RF) — AUC 0,900

- **Familia**: bagging (ensemble paralelo).
- **Cómo funciona**: entrena 300 árboles independientes; cada uno ve
  un bootstrap aleatorio del train + subconjunto aleatorio de features.
  La predicción final = voto mayoritario.
- **Por qué quedó 3º**: los árboles capturan interacciones no-lineales,
  pero al ser independientes no se especializan en errores ajenos.
- **Mejor params**: `n_estimators=300`, `max_depth=30`,
  `min_samples_split=5`, `max_features='sqrt'`.

### 1.5 XGBoost (XGB) — AUC 0,907

- **Familia**: gradient boosting (ensemble secuencial).
- **Cómo funciona**: árboles uno tras otro, cada uno corrige los errores
  que el anterior cometió. Es como un equipo donde cada miembro se
  especializa en los casos difíciles que dejó el anterior.
- **Por qué quedó 2º**: state-of-the-art para tabular. Empata
  virtualmente con LGBM.
- **Mejor params**: `n_estimators=300`, `max_depth=10`,
  `learning_rate=0,024`, `gamma=1,18`, `reg_lambda=0,17`,
  `subsample=0,776`, `colsample_bytree=0,889`.

### 1.6 LightGBM (LGBM) — AUC 0,9091 ⭐ GANADOR

- **Familia**: gradient boosting (variante eficiente).
- **Cómo funciona**: similar a XGBoost pero con dos diferencias clave:
  - **Leaf-wise growth**: en lugar de expandir el árbol nivel por nivel
    (level-wise), expande la hoja con mayor ganancia. Captura patrones
    complejos con menos árboles.
  - **Histogramas**: agrupa valores continuos en bins para acelerar splits.
- **Por qué ganó**: la combinación `num_leaves=127` + `learning_rate=0,02`
  + `min_child_samples=50` encontró un balance que aprovecha mejor el
  feature space ampliado de v2.
- **Mejor params**: `n_estimators=800`, `num_leaves=127`,
  `learning_rate=0,020`, `max_depth=-1` (sin límite),
  `min_child_samples=50`, `subsample=0,664`, `colsample_bytree=0,816`.

### 1.7 Multi-Layer Perceptron (MLP) — AUC 0,863

- **Familia**: red neuronal feed-forward.
- **Cómo funciona**: dos capas ocultas de 100 + 100 neuronas con
  activación ReLU; entrenamiento por backpropagation.
- **Por qué quedó 4º**: dataset moderado (38k muestras) no es suficiente
  para que la red supere a los árboles. Además, las features categóricas
  (OHE) no son el dominio natural de las redes densas.
- **Mejor params**: `hidden_layer_sizes=(100, 100)`, `activation='relu'`,
  `alpha=0,003`, `learning_rate_init=0,008`.

### 1.8 Gaussian Naive Bayes (NB) — AUC 0,752 ❌

- **Familia**: probabilístico.
- **Cómo funciona**: asume que las features son condicionalmente
  independientes dada la clase y modela cada una como Gaussiana.
- **Por qué quedó último**: la asunción de independencia se viola
  severamente. `duracion_planificada_dias` está correlacionada con
  `valor_del_contrato`, modalidad, sector. NB no puede modelar esa
  estructura.
- **Resultado patológico**: Precision 0,995 / Recall 0,211 → el modelo
  casi nunca predice positivo, pero cuando lo hace acierta. Inútil para
  producción.

---

## 2. El ganador: LightGBM

### 2.1 ¿Por qué LGBM y no XGB?

Diferencia muy pequeña (Δ AUC = 0,0022), pero LGBM gana en F1 (0,8503
vs 0,8500). Razones técnicas:

| Aspecto | XGB | LGBM |
|---|---|---|
| Estrategia árbol | level-wise (balanceado) | leaf-wise (greedy en mejor hoja) |
| Hojas | `max_depth` controla | `num_leaves` controla directamente |
| Velocidad | rápido | ~2× más rápido por iteración |
| Memoria | mayor | menor (histogramas comprimidos) |

En este caso LGBM con `num_leaves=127` permite árboles asimétricos que
capturan combinaciones específicas de features (ej. "duración > 365 días
AND modalidad = licitación pública AND depto = Bogotá") con más libertad
que XGB con `max_depth=10`.

### 2.2 Capacidad real del modelo ganador

Sobre el test set (9.667 contratos no vistos):

**Target `tuvo_atraso`** (60,5 % positivos):
- **AUC 0,9091** → discrimina muy bien
- **F1 0,8503** → balance Precision/Recall sólido
- **Precision 0,8672** → de cada 100 alertas, ~87 son atrasos reales
- **Recall 0,8341** → captura 83 % de los atrasos reales

**Target `tuvo_sobrecosto`** (83,4 % positivos):
- **AUC 0,8338** → discrimina menos bien (más difícil)
- **F1 0,8731** → muy alto por la alta prevalencia
- **Precision 0,8896** / **Recall 0,8572**

### 2.3 Comparativa contra el sprint padre v1

| Versión | Target | AUC | F1 |
|---|---|---|---|
| v1 XGB tuned (Grid) | atraso | 0,9088 | **0,8522** |
| **v2 LGBM** | atraso | **0,9091** | 0,8503 |
| v1 XGB tuned (Grid) | sobrecosto | **0,8358** | 0,8508 |
| **v2 LGBM** | sobrecosto | 0,8338 | **0,8731** |

**Lectura**: v2 empata o supera marginalmente. La mejora real está en
F1 de sobrecosto (+0,022). El modelo v2 es **más balanceado** (mejor
Recall, peor Precision en sobrecosto).

---

## 3. Variables que aportan valor

Análisis combinado de **Mutual Information** (informativa marginal) +
**Permutation Importance** (uso real del modelo).

### 3.1 Top 10 features dominantes

| # | Feature | MI atraso | Permutation | Origen | Nueva v2 |
|---|---|---|---|---|---|
| 1 | **`duracion_planificada_dias`** | **0,217** | **0,230** | Contrato | No |
| 2 | `duracion_planificada_dias_was_nan` | 0,069 | 0,122 | Flag derivado | No |
| 3 | `valor_del_contrato` | 0,086 | 0,012 | Contrato | No |
| 4 | `estado_bpin_No Válido` | 0,006 | 0,009 | Categórico OHE | No |
| 5 | `ciudad_freq` | 0,025 | 0,007 | Geografía | No |
| 6 | `sector_freq` | 0,009 | 0,006 | Entidad | No |
| 7 | **`log_valor_contrato`** | 0,085 | 0,006 | Contrato (transf) | **Sí** ⭐ |
| 8 | **`localizaci_n_freq`** | 0,032 | 0,006 | Geografía fina | **Sí** ⭐ |
| 9 | `departamento_freq` | 0,014 | 0,005 | Geografía | No |
| 10 | **`codigo_de_categoria_principal_freq`** | 0,016 | 0,005 | UNSPSC contrato | **Sí** ⭐ |

### 3.2 Interpretación de las variables clave

#### `duracion_planificada_dias` (dominante absoluta)

Es 5× más informativa que cualquier otra feature. **Contratos más
largos = más probabilidad de atraso**. Razón: a más tiempo, más
exposición a imprevistos (clima, modificaciones, problemas legales).

El flag `_was_nan` es el 2º predictor más fuerte. Esto significa que
**el hecho de que el dataset no tenga duración registrada es señal**
— los contratos sin fecha planificada suelen ser irregulares y se
atrasan más.

#### `valor_del_contrato` y `log_valor_contrato`

Ambos en top 10. Captura el mismo fenómeno pero con escala distinta:
- **Bruto**: lineal — un contrato de $10B aporta 10× más que uno de $1B.
- **Log**: comprime escala — diferencia entre $1B y $10B es la misma
  que entre $100M y $1B.

XGB/LGBM usan splits, así que la versión log no añade nada nuevo a
árboles, pero **sí aporta a modelos lineales** (LR, SVM) que sí ven
la escala.

**Patrón**: contratos más grandes → más riesgo (Q4 > Q1).

#### `ciudad_freq` / `departamento_freq` / `localizaci_n_freq`

Tres niveles de granularidad geográfica:
- Departamento: 32 valores (Bogotá D.C., Antioquia, …)
- Ciudad: ~1.000 valores
- Localización: 737 valores (subdivisión territorial fina)

**Frequency encoding** convierte cada categoría en su % de aparición.
Captura una señal estable: territorios con más contratos suelen tener
flujos operativos más maduros → menor riesgo.

**Caldas tiene atraso 28,8 %** vs **Huila 58,4 %**. Diferencia gigante.

#### `codigo_de_categoria_principal_freq` (UNSPSC)

Clasificación estándar internacional de bienes y servicios. 1.506
valores. Captura el **tipo de obra**: pavimentación vs construcción
de escuela vs alcantarillado. Algunos tipos son históricamente más
conflictivos.

#### `estado_bpin_No Válido` (OHE dummy)

Flag de que el código BPIN (Banco de Proyectos de Inversión Nacional)
no es válido. Aparece en top porque **señala procesos con problemas
administrativos** → mayor probabilidad de atraso. Es un proxy de
"documentación sucia".

### 3.3 Variables que NO aportaron lo esperado

Hipótesis fallidas del experimento v2:

| Feature | Cobertura | MI atraso | Por qué no aportó |
|---|---|---|---|
| `rup_tamano` | 49 % | < 0,003 | Cobertura limitada + categórica casi binaria (micro/pyme) |
| `rup_empleados` | 49 % | < 0,005 | Idem cobertura + colineal con `rup_tamano` |
| `rup_sanciones` | 49 % | < 0,002 | Sanciones formales muy raras |
| `rup_inhabilidad` | 49 % | < 0,002 | Inhabilitados son excepción |
| `rup_activo_total`, `rup_patrimonio` | 48 % | < 0,008 | Útiles pero redundantes con `valor_del_contrato` |
| `n_proponentes_por_proceso` | 48 % | 0,002 | Sorpresa — competencia NO predice atraso |
| `anios_empresa` | 67 % | 0,015 | Top 11; sí aporta marginal |
| `espostconflicto` | 100 % | < 0,001 | Casi todos `No` |
| `obligaciones_postconsumo` | 100 % | < 0,001 | Sin variación útil |

**Conclusión**: las variables estructurales del proveedor (capacidad,
tamaño, sanciones) tienen valor descriptivo pero **no aportan capacidad
predictiva** sobre el target en este dataset. Razones:

1. Cobertura limitada (49 %) divide la señal.
2. Las variables de contrato (duración, valor, geografía) ya capturan
   ~99 % de la varianza explicable.
3. Las sanciones e inhabilidades son tan raras que casi no varían
   entre observaciones.

---

## 4. Interacción con el chatbot

### 4.1 Arquitectura propuesta

```
┌─────────────────────────────────────────────────────────┐
│ Usuario (empresario)                                      │
│ "Microempresa de construcción, quiero participar en       │
│  licitación de obra en Bogotá por $2B, 12 meses"          │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│ Gemini 2.5 Flash (LLM)                                    │
│ • Extrae features del texto natural                       │
│ • Decide cuándo llamar al modelo predictivo               │
│ • Humaniza la respuesta                                   │
└─────────────────────┬───────────────────────────────────┘
                      ↓ function call: predecir_riesgo(features)
┌─────────────────────────────────────────────────────────┐
│ Predictor (wrapper Python)                                │
│ • Recibe dict crudo del usuario                           │
│ • Aplica winsor + OHE + Freq encoding + impute (idéntico  │
│   al pipeline de entrenamiento)                           │
│ • Llama lgbm.pkl                                          │
│ • Devuelve {atraso: 0.62, sobrecosto: 0.78,               │
│             top_factores: [...]}                          │
└─────────────────────┬───────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────────┐
│ Respuesta humanizada al usuario                           │
│ "Contratos como el que describes históricamente:          │
│  • 62 % de probabilidad de atrasarse                      │
│  • 78 % de probabilidad de adición presupuestal           │
│  Factores principales:                                    │
│  1. Duración planificada larga (12 meses) ↑               │
│  2. Valor alto del contrato ↑                             │
│  3. Localización Bogotá: depto con riesgo medio"          │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Mapeo input usuario → features del modelo

El usuario describe en lenguaje natural. Gemini extrae estructuradamente:

| Usuario dice | Feature del modelo | Cómo se procesa |
|---|---|---|
| "Bogotá" | `departamento`, `ciudad`, `localizaci_n` | Match contra freq_maps; sin match → freq=0 |
| "obra de pavimentación" | `codigo_de_categoria_principal` | LLM clasifica al UNSPSC más cercano + freq encode |
| "$2.000 millones" | `valor_del_contrato`, `log_valor_contrato` | Directo + log10 |
| "12 meses" | `duracion_planificada_dias` | Convertir a días (×30,4) |
| "microempresa" | `es_pyme=Si` | OHE |
| "no me asocio con otros" | `es_grupo=No` | OHE |
| "licitación pública" | `modalidad_de_contratacion` | Match exacto |
| (no mencionado) | `n_proponentes_por_proceso` | NaN → mediana + flag_was_nan=1 |
| (no mencionado) | `rup_*`, `anios_empresa` | NaN → mediana + flag_was_nan=1 |

**Clave**: features no mencionadas se imputan con mediana + el flag
`_was_nan=1` envía al modelo la señal "no se conoce este dato", que
en sí ya es informativo.

### 4.3 Explicabilidad con SHAP

Después de la predicción, calcular SHAP local sobre el caso:

```python
import shap
explainer = shap.TreeExplainer(lgbm)
shap_values = explainer.shap_values(X_caso)
# top-3 features que empujaron probabilidad hacia atraso/no-atraso
```

Esto permite al chatbot decir:

> "Los factores que más aumentan tu riesgo de atraso en este caso son:
> 1. Duración de 12 meses (+0,18 a la probabilidad)
> 2. Modalidad licitación pública (+0,04)
> 3. Valor alto del contrato (+0,03)
>
> Lo que reduce tu riesgo:
> 1. Sector de obras civiles (-0,02)"

### 4.4 Recomendaciones accionables

Con conocimiento del modelo + datos históricos, el chatbot puede
sugerir mitigaciones:

| Situación | Recomendación |
|---|---|
| Riesgo atraso alto (>60%) | "Considera formar consorcio: en consorcios la tasa baja de 60,5% a 44,6%" |
| Departamento Huila / Norte Santander | "Estos deptos tienen tasa atraso > 50%. Refuerza cronograma" |
| Pyme + valor alto | "Pymes en contratos Q4 tienen 49% atraso. Buffer financiero recomendado" |
| Modalidad licitación pública | "Modalidad más rigurosa. Asegura documentación completa" |

### 4.5 Limitaciones que el bot DEBE comunicar

El modelo NO sabe:
- Si tu empresa será adjudicada
- Tu capacidad técnica real (experiencia previa, equipo)
- Calidad del proyecto (planos, BIM, estudios previos)
- Contexto político local

Solo proyecta: **comportamiento histórico de contratos similares**.

Decir esto explícitamente protege la integridad del chatbot y evita
expectativas erróneas.

### 4.6 Stack técnico recomendado

| Componente | Tecnología | Por qué |
|---|---|---|
| Frontend | Streamlit | Python nativo, demo académica rápida |
| LLM | Gemini 2.5 Flash (Tier 1 que ya tienes) | Function calling soportado, free tier |
| Modelo | `lgbm.pkl` cargado en memoria | Inferencia < 50 ms por caso |
| Wrapper | Clase `Predictor` con freq_maps + imputer + winsor | Replica pipeline 02 |
| Explicabilidad | SHAP TreeExplainer | Eficiente sobre árboles |
| Persistencia sesión | `st.session_state` | Histórico conversación |

Tiempo estimado de implementación: 4-6 horas.

---

## 5. Resumen ejecutivo

| Pregunta | Respuesta |
|---|---|
| ¿Cuál modelo gana? | LightGBM (AUC 0,9091 atraso, 0,8338 sobrecosto) |
| ¿Aportan las features estructurales nuevas? | Solo marginalmente. 3 nuevas en top 10 pero impacto AUC < 0,001 |
| ¿Qué predice el modelo? | Riesgo histórico de atraso y sobrecosto de contratos similares |
| ¿Qué features dominan? | `duracion_planificada_dias` (5× más fuerte), `valor`, geografía |
| ¿Qué features fallaron como predictoras? | RUP estructurales (`rup_tamano`, `rup_empleados`, `rup_sanciones`), `n_proponentes_por_proceso`, `espostconflicto` |
| ¿Es útil para el chatbot? | Sí. Stack: Streamlit + Gemini + LGBM + SHAP |
| ¿Qué NO puede hacer el bot? | Predecir adjudicación, evaluar capacidad técnica, contexto político |
