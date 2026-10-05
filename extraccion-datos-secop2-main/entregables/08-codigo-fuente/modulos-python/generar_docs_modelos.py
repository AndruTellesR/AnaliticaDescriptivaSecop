"""Genera docs por modelo y doc 12 comparativa a partir de resultados_modelos.json."""
from pathlib import Path
import json

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / 'docs' / 'modelos'
DOCS.mkdir(parents=True, exist_ok=True)

META = {
    'lr': {
        'familia':   'Lineal',
        'algoritmo': 'Logistic Regression',
        'escalado':  'sí',
        'descripcion': 'Modelo lineal con sigmoide. Línea base interpretable. Penalización L2.',
    },
    'knn': {
        'familia':   'Distancia',
        'algoritmo': 'K-Nearest Neighbors',
        'escalado':  'sí',
        'descripcion': 'Clasifica por mayoría entre k vecinos más cercanos.',
    },
    'svm': {
        'familia':   'Margen',
        'algoritmo': 'Linear SVM (calibrado)',
        'escalado':  'sí',
        'descripcion': 'SVM lineal con CalibratedClassifierCV para predict_proba. RBF inviable a 38k samples.',
    },
    'rf': {
        'familia':   'Bagging',
        'algoritmo': 'Random Forest',
        'escalado':  'no',
        'descripcion': 'Ensemble paralelo de árboles sobre muestras bootstrap.',
    },
    'xgb': {
        'familia':   'Boosting',
        'algoritmo': 'XGBoost',
        'escalado':  'no',
        'descripcion': 'Gradient boosting SOTA tabular. tree_method=hist.',
    },
    'lgbm': {
        'familia':   'Boosting',
        'algoritmo': 'LightGBM',
        'escalado':  'no',
        'descripcion': 'Gradient boosting con leaf-wise growth e histogramas.',
    },
    'nb': {
        'familia':   'Probabilístico',
        'algoritmo': 'Gaussian Naive Bayes',
        'escalado':  'sí',
        'descripcion': 'Asume independencia condicional y distribuciones gaussianas por clase.',
    },
    'mlp': {
        'familia':   'Red neuronal',
        'algoritmo': 'Multi-Layer Perceptron',
        'escalado':  'sí',
        'descripcion': 'Red feed-forward con backpropagation. Early stopping para evitar overfitting.',
    },
}

NUM = {'lr':'04','knn':'05','svm':'06','rf':'07','xgb':'08','lgbm':'09','nb':'10','mlp':'11'}


def render(nombre, r):
    m = META[nombre]
    num = NUM[nombre]
    bp = '\n'.join(f'- `{k}`: `{v}`' for k, v in r['best_params'].items())
    return f"""# Modelo {num} — {m['algoritmo']}

**Notebook**: `notebooks/{num}_modelo_{nombre}.ipynb`
**Modelo persistido**: `data/modelos/{nombre}.pkl`

## Configuración

- **Familia**: {m['familia']}
- **Escalado**: {m['escalado']}
- **Estrategia**: `RandomizedSearchCV` con `n_iter = {r['n_iter']}`,
  `cv = StratifiedKFold({r['cv_folds']})`, `scoring = 'roc_auc'`
- **Tiempo de búsqueda**: {r['tiempo_search_seg']} s

## Descripción

{m['descripcion']}

## Resultados (test set, target `tuvo_atraso`)

| Métrica | Valor |
|---------|-------|
| CV AUC | {r['best_cv_auc']:.4f} |
| Test AUC | **{r['AUC']:.4f}** |
| F1 | {r['F1']:.4f} |
| Precision | {r['Precision']:.4f} |
| Recall | {r['Recall']:.4f} |
| Accuracy | {r['Accuracy']:.4f} |

## Mejores hiperparámetros

{bp}
"""


def main():
    p = RAIZ / 'data' / 'resultados_modelos.json'
    resultados = json.loads(p.read_text(encoding='utf-8'))
    for nombre, r in resultados.items():
        out = DOCS / f'{NUM[nombre]}_{nombre}.md'
        out.write_text(render(nombre, r), encoding='utf-8')
        print(f'Escrito {out.name}')


if __name__ == '__main__':
    main()
