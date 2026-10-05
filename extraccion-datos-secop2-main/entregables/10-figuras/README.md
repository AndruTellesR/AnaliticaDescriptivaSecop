# 10 — Figuras del proyecto

Esta carpeta agrupa todas las figuras producidas durante el proyecto,
distribuidas en cuatro grupos según la etapa que ilustran.

## Estructura

| Subcarpeta o archivos | Cantidad | Rol |
|-----------------------|----------|-----|
| Archivos PNG en la raíz | 26 | Figuras embebidas en el informe final (referenciadas desde el documento LaTeX) |
| `modelado-v1/` | 21 | Figuras del sprint principal de modelado (sprint padre) |
| `modelado-v2/` | 6 | Figuras del modelado v2 con variables estructurales |
| `consorcios/` | 13 | Figuras del sub-sprint específico de consorcios |

## Figuras del informe final (raíz)

Las 26 figuras de la raíz se referencian en el informe final, numeradas
secuencialmente del 01 al 26. Las más representativas son:

| Archivo | Capítulo del informe | Contenido |
|---------|----------------------|-----------|
| `01_balance_target.png` | Cap. 2 | Distribución de la variable objetivo `tuvo_atraso` |
| `02_tasa_por_depto.png` | Cap. 2 | Tasa de atraso por departamento (top 15) |
| `04_balance_split.png` | Cap. 3 | Preservación del balance tras la división train/test |
| `09_permutation_importance.png` | Cap. 3 | Importancia por permutación de features |
| `10_rfecv_curve.png` | Cap. 3 | Curva de RFECV con estabilización en 30 variables |
| `11_comparativa_reduccion.png` | Cap. 3 | Comparativa con y sin selección de variables |
| `15_valor_duracion.png` | Cap. 2 | Relación valor/duración con riesgo de modificación |
| `22_permutation_top30.png` | Cap. 2 | Top 30 features por importancia (modelo v2) |
| `23_comparativa_auc.png` | Cap. 3 | AUC test del zoológico de 8 algoritmos |
| `24_curvas_roc.png` | Cap. 3 | Curvas ROC superpuestas |
| `25_heatmap_metricas.png` | Cap. 3 | Mapa de calor de métricas por modelo |
| `26_matriz_confusion_lgbm.png` | Cap. 3 | Matriz de confusión del modelo ganador |

## Figuras del sub-sprint consorcios

Las 13 figuras de `consorcios/` profundizan el análisis del sub-universo de
contratos suscritos por consorcios. Incluyen distribuciones de los
indicadores de pliego, correlaciones con los targets, heatmaps por
departamento y modalidad, y comparativa de modelos sobre ese subconjunto.

## Formato

Todas las figuras están en formato PNG con resolución de 120 DPI, generadas
con `matplotlib` y `seaborn` desde los notebooks Jupyter que las producen.

## Reproducibilidad

Cada figura puede regenerarse ejecutando el notebook correspondiente:

| Figura | Notebook que la produce |
|--------|-------------------------|
| `01–13` (algunas) | Notebooks del sprint padre en `../07-notebooks/modelado-v1/` |
| `21–26` | Notebooks del modelo final en `../07-notebooks/modelado-v2/` |
| `consorcios/*` | Notebooks del sub-sprint consorcios |
