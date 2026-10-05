"""
Módulo compartido de preprocesamiento — modelo predictivo global v2.

Operaciones:
- Cargar dataset imputado.
- Train/test split estratificado.
- Escalado opcional (para LR, KNN, SVM, NB, MLP).
- Construcción de `scale_pos_weight` por target.

Convenciones:
- `random_state = 42`
- `test_size = 0.20`
- target principal = `tuvo_atraso`
"""

from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42
TEST_SIZE = 0.20
TARGETS = ['tuvo_atraso', 'tuvo_sobrecosto']
TARGET_PRINCIPAL = 'tuvo_atraso'


@dataclass
class Datos:
    X_train: pd.DataFrame
    X_test:  pd.DataFrame
    y_train: pd.DataFrame
    y_test:  pd.DataFrame
    scaler:  Optional[StandardScaler]
    scale_pos_weight: dict[str, float]
    cols_features: list[str]

    @property
    def n_train(self) -> int: return len(self.X_train)

    @property
    def n_test(self) -> int: return len(self.X_test)


def cargar_dataset(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_parquet(data_dir / 'consolidado_imputado.parquet')
    y = df[TARGETS].copy()
    X = df.drop(columns=TARGETS).copy()
    return X, y


def dividir(X: pd.DataFrame, y: pd.DataFrame,
            target_principal: str = TARGET_PRINCIPAL):
    return train_test_split(
        X, y,
        test_size=TEST_SIZE,
        stratify=y[target_principal],
        random_state=RANDOM_STATE,
    )


def construir_scale_pos_weight(y_train: pd.DataFrame) -> dict[str, float]:
    return {
        c: ((y_train[c] == 0).sum() / (y_train[c] == 1).sum())
        for c in TARGETS
    }


def preparar(data_dir: Path,
             aplicar_escalado: bool = False,
             target_principal: str = TARGET_PRINCIPAL) -> Datos:
    X, y = cargar_dataset(data_dir)
    X_train, X_test, y_train, y_test = dividir(X, y, target_principal)

    scaler = None
    if aplicar_escalado:
        scaler = StandardScaler()
        Xt = scaler.fit_transform(X_train.values)
        Xe = scaler.transform(X_test.values)
        X_train = pd.DataFrame(Xt, columns=X_train.columns, index=X_train.index)
        X_test  = pd.DataFrame(Xe, columns=X_test.columns,  index=X_test.index)

    return Datos(
        X_train=X_train, X_test=X_test,
        y_train=y_train, y_test=y_test,
        scaler=scaler,
        scale_pos_weight=construir_scale_pos_weight(y_train),
        cols_features=X_train.columns.tolist(),
    )


def metricas_clasificacion(y_true, y_pred, y_proba) -> dict:
    from sklearn.metrics import (
        roc_auc_score, f1_score, precision_score, recall_score, accuracy_score
    )
    return {
        'AUC':       round(roc_auc_score(y_true, y_proba), 4),
        'F1':        round(f1_score(y_true, y_pred), 4),
        'Precision': round(precision_score(y_true, y_pred), 4),
        'Recall':    round(recall_score(y_true, y_pred), 4),
        'Accuracy':  round(accuracy_score(y_true, y_pred), 4),
    }


__all__ = [
    'RANDOM_STATE', 'TEST_SIZE', 'TARGETS', 'TARGET_PRINCIPAL',
    'Datos', 'preparar', 'metricas_clasificacion',
    'construir_scale_pos_weight',
]
