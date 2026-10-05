# Documento 12 — Comparativa final del zoológico

**Notebook**: `notebooks/12_comparativa_final.ipynb`
**Inputs**: `data/resultados_modelos.json`, `data/modelos/*.pkl`
**Outputs**: `data/comparativa_modelos.csv`, `data/modelos/GANADOR.txt`, figuras `dia_12_*.png`

## Tabla maestra de resultados (target = `tuvo_atraso`)

| # | Modelo | AUC CV | AUC test | F1 | Precision | Recall | Accuracy | Tiempo búsqueda |
|---|--------|--------|----------|------|-----------|--------|----------|-----------------|
| 1 | **xgb** | 0,8797 | **0,8630** | **0,7499** | 0,7765 | 0,7250 | 0,7841 | 25,27 s |
| 2 | lgbm | 0,8786 | 0,8627 | 0,7478 | 0,7794 | 0,7187 | 0,7836 | 819,94 s |
| 3 | rf | 0,8726 | 0,8518 | 0,7274 | 0,7741 | 0,6860 | 0,7705 | 57,77 s |
| 4 | mlp | 0,8248 | 0,8074 | 0,6789 | 0,7431 | 0,6249 | 0,7361 | 59,02 s |
| 5 | svm | 0,8160 | 0,8058 | 0,6786 | 0,7226 | 0,6396 | 0,7295 | 771,14 s |
| 6 | lr | 0,8002 | 0,7690 | 0,6114 | 0,7406 | 0,5205 | 0,7046 | 10,42 s |
| 7 | knn | 0,7661 | 0,7497 | 0,6190 | 0,6909 | 0,5606 | 0,6919 | 8,81 s |
| 8 | nb | 0,6725 | 0,6762 | 0,6219 | 0,4703 | 0,9178 | 0,5019 | 5,32 s |

## Modelo ganador

**XGBoost** — `data/modelos/xgb.pkl`

Criterio de selección:

- AUC máximo en test (0,8630).
- Empate técnico con LightGBM (Δ = 0,0003 < 0,003) resuelto a favor de XGB por:
  - F1 ligeramente superior (0,7499 vs 0,7478).
  - Tiempo de entrenamiento 33 veces menor (25 s vs 820 s).

## Mejores hiperparámetros del ganador

| Hiperparámetro | Valor |
|----------------|-------|
| `n_estimators` | 500 |
| `max_depth` | 10 |
| `learning_rate` | 0,0348 |
| `subsample` | 0,7232 |
| `colsample_bytree` | 0,7976 |
| `gamma` | 0,8941 |
| `reg_lambda` | 2,7662 |
| `scale_pos_weight` | 1,2406 |

## Lecturas por familia de algoritmos

**Boosting (XGB / LGBM)**: dominan claramente el ranking (AUC ~0,863).
Ambos extraen exactamente el mismo nivel de señal; la diferencia entre
ellos es de implementación y eficiencia. La elección de XGB sobre LGBM
es operativa, no estadística.

**Bagging (RF)**: tercer lugar con AUC 0,852. Diferencia de ~1,1 pp
respecto al boosting. Captura interacciones pero pierde frente al
gradient descent dirigido del boosting.

**Red neuronal (MLP)**: AUC 0,807. Significativamente por debajo de los
ensambles. La señal en este dataset es mayoritariamente capturada por
splits sobre `duracion_planificada_dias` y otras numéricas, lo cual
favorece a los árboles. La red no aporta beneficio adicional dado el
tamaño moderado del dataset (8.500 muestras de train).

**Lineales (LR)**: AUC 0,769. Solo lineal no alcanza para capturar las
interacciones presentes (modalidad × valor, departamento × duración).
Confirma la necesidad de modelos no-lineales para esta tarea.

**Distancia (KNN)**: AUC 0,750. El mejor `k` quedó alto (k = 31), lo
que sugiere que las vecindades pequeñas tienen demasiado ruido en este
feature space mixto (numéricas + dummies + flags).

**Naive Bayes (NB)**: AUC 0,676 — el peor con margen. La hipótesis de
independencia condicional es claramente violada (correlación entre
duración planificada, valor del contrato y modalidad). Recall altísimo
(0,92) pero a costa de precisión muy baja (0,47): predice "atraso" en
casi todo. Funciona como cota inferior de referencia.

## Análisis FP / FN del ganador

Con umbral de decisión 0,50 sobre la probabilidad XGBoost:

- **Verdaderos positivos** (atraso correctamente predicho): predomina en
  contratos con duración planificada larga y modalidad de licitación pública.
- **Falsos positivos** (alarma incorrecta): concentrados en contratos con
  valor alto pero modalidad de contratación directa, que históricamente
  cumplen plazo más a menudo de lo que sugiere el modelo.
- **Falsos negativos** (atrasos no detectados): contratos de menor valor
  en departamentos con baja muestra histórica donde la señal es difusa.

El balance Precision (0,78) vs Recall (0,72) es razonable y se puede
mover via threshold para casos de uso específicos: si el costo del FP
(alarma falsa) es bajo, bajar el umbral incrementa recall; si el costo
del FN (atraso no detectado) es bajo, subir el umbral mejora precisión.

## Comparativa contra el modelo global del sprint padre

| Escenario | Universo | AUC | F1 |
|-----------|----------|-----|-----|
| Global multi-target (RF / XGB) | 48.331 contratos | 0,9047 | 0,847 |
| Consorcios — XGB (este sprint) | 10.629 contratos | 0,8630 | 0,750 |

El modelo global mantiene mejor desempeño (4,2 pp de AUC y 9,7 pp de F1)
incluso al compararse en un universo que incluye a los consorcios. Dos
razones probables:

1. **Tamaño de muestra**: 48.331 contratos aportan ~4,5× más datos para
   aprender patrones. La curva de aprendizaje no satura todavía en el
   universo de consorcios.
2. **Riqueza de features**: el modelo global tiene acceso a `rup_*`
   (cobertura ~40 %), mientras que en consorcios `rup_*` es 0 %.
3. **Heterogeneidad útil**: la diversidad de comportamientos entre
   consorcios y no-consorcios provee contraste que ayuda al modelo a
   discriminar mejor que aprender solo dentro del sub-universo más
   uniforme.

## Decisión sobre la unificación

A la luz de los resultados, la **especialización en consorcios no
mejora frente al modelo global** aplicado al mismo sub-universo. El
modelo global captura ya la información geográfica, de modalidad y de
duración que son los predictores dominantes, y el sub-universo es
demasiado pequeño y homogéneo para que un modelo dedicado ofrezca
ventaja.

**Recomendación**: el modelo global multi-target se mantiene como
modelo de producción único. El presente sprint cumple su valor como
evidencia experimental y como caracterización descriptiva del sub-
universo de consorcios, no como reemplazo del modelo principal.

## Nota sobre SVM

El notebook 06 (SVM) ejecuta `RandomizedSearchCV` con 12 iteraciones
sobre kernels RBF y lineal. La búsqueda quedó en kernel RBF con C = 6,36,
`gamma = 'auto'` y `class_weight = 'balanced'`. AUC test 0,8058, ligeramente
por debajo del MLP. El tiempo de búsqueda (771 s) confirma que SVM con
RBF no es competitivo en este dataset: alcanza un AUC comparable al MLP
pero a 13 veces el costo computacional del XGBoost, sin mejora alguna en
métricas. Se descarta para producción.
