"""Genera los notebooks 04-11 (zoológico 8 modelos) para modelo global v2."""
from pathlib import Path
import nbformat as nbf

RAIZ = Path(__file__).resolve().parent.parent
NB = RAIZ / 'notebooks'

PREAMBULO = """import sys, warnings
from pathlib import Path
warnings.filterwarnings('ignore')

RAIZ = Path('..').resolve()
sys.path.insert(0, str(RAIZ))

from src.preprocesamiento import preparar, RANDOM_STATE
from src.entrenamiento  import entrenar_y_evaluar

DATA = RAIZ / 'data'
"""

CARGA = """datos = preparar(DATA, aplicar_escalado={escalado})
print(f'Train: {{datos.n_train}} | Test: {{datos.n_test}} | Features: {{len(datos.cols_features)}}')
print(f'scale_pos_weight atraso: {{datos.scale_pos_weight[\"tuvo_atraso\"]:.4f}}')
"""

MODELOS = [
    ('04', 'lr', 'Logistic Regression', True,
     'from sklearn.linear_model import LogisticRegression\nfrom scipy.stats import loguniform',
     'LogisticRegression(max_iter=2000, random_state=RANDOM_STATE, n_jobs=-1)',
     {
        'C':             "loguniform(0.01, 100)",
        'penalty':       "['l2']",
        'solver':        "['lbfgs', 'liblinear']",
        'class_weight':  "['balanced', None]",
     }, 'Línea base lineal. Necesita escalado.', 40),

    ('05', 'knn', 'K-Nearest Neighbors', True,
     'from sklearn.neighbors import KNeighborsClassifier',
     'KNeighborsClassifier(n_jobs=-1)',
     {
        'n_neighbors': "[7, 11, 15, 21, 31, 51]",
        'weights':     "['uniform', 'distance']",
        'metric':      "['euclidean', 'manhattan']",
     }, 'Distancia. Necesita escalado. Sensible a cardinalidad.', 25),

    ('06', 'svm', 'Linear SVM', True,
     'from sklearn.svm import LinearSVC\nfrom sklearn.calibration import CalibratedClassifierCV\nfrom scipy.stats import loguniform',
     "CalibratedClassifierCV(LinearSVC(max_iter=2000, random_state=RANDOM_STATE, dual='auto'), method='sigmoid', cv=3)",
     {
        'estimator__C':            "loguniform(0.01, 10)",
        'estimator__class_weight': "['balanced', None]",
     }, 'SVM lineal (RBF inviable con 38k samples). CalibratedClassifierCV para predict_proba.', 15),

    ('07', 'rf', 'Random Forest', False,
     'from sklearn.ensemble import RandomForestClassifier',
     'RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1)',
     {
        'n_estimators':      "[200, 300, 500]",
        'max_depth':         "[None, 10, 20, 30]",
        'min_samples_split': "[2, 5, 10]",
        'min_samples_leaf':  "[1, 2, 4]",
        'max_features':      "['sqrt', 'log2']",
        'class_weight':      "['balanced', 'balanced_subsample', None]",
     }, 'Bagging. Sin escalado. Captura interacciones no-lineales.', 40),

    ('08', 'xgb', 'XGBoost', False,
     'from xgboost import XGBClassifier\nfrom scipy.stats import loguniform, uniform',
     ("XGBClassifier(objective='binary:logistic', eval_metric='logloss',\n"
      "    tree_method='hist', n_jobs=-1, random_state=RANDOM_STATE,\n"
      "    scale_pos_weight=datos.scale_pos_weight['tuvo_atraso'])"),
     {
        'n_estimators':     "[300, 500, 800]",
        'learning_rate':    "loguniform(0.01, 0.3)",
        'max_depth':        "[6, 8, 10, 12]",
        'subsample':        "uniform(0.6, 0.4)",
        'colsample_bytree': "uniform(0.6, 0.4)",
        'gamma':            "uniform(0, 5)",
        'reg_lambda':       "loguniform(0.1, 10)",
        'reg_alpha':        "loguniform(0.001, 1.0)",
     }, 'Gradient boosting SOTA tabular.', 50),

    ('09', 'lgbm', 'LightGBM', False,
     'from lightgbm import LGBMClassifier\nfrom scipy.stats import loguniform, uniform',
     ("LGBMClassifier(objective='binary', n_jobs=-1, random_state=RANDOM_STATE,\n"
      "    scale_pos_weight=datos.scale_pos_weight['tuvo_atraso'], verbose=-1)"),
     {
        'n_estimators':      "[300, 500, 800]",
        'learning_rate':     "loguniform(0.01, 0.3)",
        'num_leaves':        "[31, 63, 127]",
        'max_depth':         "[-1, 8, 10, 12]",
        'min_child_samples': "[10, 20, 50]",
        'subsample':         "uniform(0.6, 0.4)",
        'colsample_bytree':  "uniform(0.6, 0.4)",
     }, 'Variante eficiente de gradient boosting.', 50),

    ('10', 'nb', 'Gaussian Naive Bayes', True,
     'from sklearn.naive_bayes import GaussianNB\nfrom scipy.stats import loguniform',
     'GaussianNB()',
     {'var_smoothing': "loguniform(1e-12, 1e-6)"},
     'Probabilístico. Asume independencia condicional.', 20),

    ('11', 'mlp', 'Multi-Layer Perceptron', True,
     'from sklearn.neural_network import MLPClassifier\nfrom scipy.stats import loguniform',
     'MLPClassifier(max_iter=300, early_stopping=True, random_state=RANDOM_STATE)',
     {
        'hidden_layer_sizes': "[(100,), (50, 50), (100, 50), (100, 100), (150, 75)]",
        'alpha':              "loguniform(1e-5, 1e-2)",
        'learning_rate_init': "loguniform(1e-4, 1e-2)",
        'activation':         "['relu', 'tanh']",
     }, 'Red neuronal. Necesita escalado. Early stopping.', 20),
]


def grid_str(g): return '{\n' + '\n'.join(f"        '{k}': {v}," for k,v in g.items()) + '\n    }'


def construir(num, corto, etiqueta, escalado, imports, clf, grid, obs, n_iter):
    nb = nbf.v4.new_notebook()
    cells = [
        nbf.v4.new_markdown_cell(
            f"# Notebook {num} — {etiqueta}\n\n"
            f"Algoritmo: {etiqueta}. Escalado: {'sí' if escalado else 'no'}. "
            f"n_iter = {n_iter}, CV=5, scoring='roc_auc'.\n\n"
            f"Observaciones: {obs}"
        ),
        nbf.v4.new_markdown_cell("## 1. Setup"),
        nbf.v4.new_code_cell(PREAMBULO + '\n' + imports),
        nbf.v4.new_markdown_cell("## 2. Cargar y preparar datos"),
        nbf.v4.new_code_cell(CARGA.format(escalado=escalado)),
        nbf.v4.new_markdown_cell("## 3. Clasificador + grid"),
        nbf.v4.new_code_cell(f"clf = {clf}\n\nparam_distributions = {grid_str(grid)}"),
        nbf.v4.new_markdown_cell(f"## 4. RandomizedSearchCV ({n_iter} iters × CV 5)"),
        nbf.v4.new_code_cell(
            f"resultado = entrenar_y_evaluar(\n"
            f"    nombre='{corto}',\n"
            f"    estimador=clf,\n"
            f"    param_distributions=param_distributions,\n"
            f"    datos=datos,\n"
            f"    data_dir=DATA,\n"
            f"    n_iter={n_iter},\n"
            f"    target='tuvo_atraso',\n"
            f")\n"
            f"resultado"
        ),
    ]
    nb['cells'] = cells
    nb['metadata'] = {
        'kernelspec': {'display_name':'Python 3','language':'python','name':'python3'},
        'language_info': {'name':'python','version':'3.12.10'},
    }
    return nb


def main():
    for spec in MODELOS:
        num, corto = spec[0], spec[1]
        nb = construir(*spec)
        out = NB / f'{num}_modelo_{corto}.ipynb'
        with open(out, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print(f'Escrito {out.name}')


if __name__ == '__main__':
    main()
