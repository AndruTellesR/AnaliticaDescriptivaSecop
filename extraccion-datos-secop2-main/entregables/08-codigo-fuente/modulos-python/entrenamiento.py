"""Entrenamiento + RandomizedSearchCV + persistencia consolidada."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import time, json

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold

from .preprocesamiento import Datos, metricas_clasificacion, RANDOM_STATE

CV_FOLDS = 5
N_ITER_DEFAULT = 40


def entrenar_y_evaluar(
    nombre: str,
    estimador,
    param_distributions: dict[str, Any],
    datos: Datos,
    data_dir: Path,
    n_iter: int = N_ITER_DEFAULT,
    target: str = 'tuvo_atraso',
    n_jobs: int = -1,
) -> dict:
    cv = StratifiedKFold(n_splits=CV_FOLDS, shuffle=True, random_state=RANDOM_STATE)

    search = RandomizedSearchCV(
        estimator=estimador,
        param_distributions=param_distributions,
        n_iter=n_iter,
        cv=cv, scoring='roc_auc',
        n_jobs=n_jobs, random_state=RANDOM_STATE,
        refit=True, return_train_score=False, verbose=0,
    )

    y_train = datos.y_train[target]
    y_test  = datos.y_test[target]

    t0 = time.time()
    search.fit(datos.X_train, y_train)
    t_search = time.time() - t0

    mejor = search.best_estimator_

    if hasattr(mejor, 'predict_proba'):
        proba = mejor.predict_proba(datos.X_test)[:, 1]
    else:
        proba = mejor.decision_function(datos.X_test)
        proba = (proba - proba.min()) / (proba.max() - proba.min())
    pred = (proba >= 0.5).astype(int)

    metricas = metricas_clasificacion(y_test, pred, proba)

    salida = {
        'nombre':        nombre,
        'target':        target,
        'n_iter':        n_iter,
        'cv_folds':      CV_FOLDS,
        'tiempo_search_seg': round(t_search, 2),
        'best_params':   _to_native(search.best_params_),
        'best_cv_auc':   round(float(search.best_score_), 4),
        **metricas,
    }

    mod_dir = data_dir / 'modelos'
    mod_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(mejor, mod_dir / f'{nombre}.pkl')

    out_json = data_dir / 'resultados_modelos.json'
    consolidado = json.loads(out_json.read_text(encoding='utf-8')) if out_json.exists() else {}
    consolidado[nombre] = salida
    out_json.write_text(json.dumps(consolidado, indent=2, ensure_ascii=False, default=str),
                        encoding='utf-8')

    print(f'\n=== {nombre.upper()} ===')
    print(f'CV AUC:          {salida["best_cv_auc"]}')
    print(f'Test AUC:        {salida["AUC"]}')
    print(f'Test F1:         {salida["F1"]}')
    print(f'Test Precision:  {salida["Precision"]}')
    print(f'Test Recall:     {salida["Recall"]}')
    print(f'Test Accuracy:   {salida["Accuracy"]}')
    print(f'Tiempo search:   {salida["tiempo_search_seg"]} s')
    print(f'Best params:     {salida["best_params"]}')

    return salida


def _to_native(d):
    out = {}
    for k, v in d.items():
        if isinstance(v, np.integer):     out[k] = int(v)
        elif isinstance(v, np.floating):  out[k] = float(v)
        elif isinstance(v, np.ndarray):   out[k] = v.tolist()
        else:                              out[k] = v
    return out


__all__ = ['entrenar_y_evaluar', 'CV_FOLDS', 'N_ITER_DEFAULT']
