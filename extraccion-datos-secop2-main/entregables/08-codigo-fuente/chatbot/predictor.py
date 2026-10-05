"""
Predictor — wrapper sobre el modelo LightGBM ganador.

Recibe un dict crudo del usuario (features del contrato + perfil empresa),
aplica el pipeline completo de preprocesamiento (winsorización, OHE,
Frequency Encoding, imputación, flags _was_nan) y devuelve probabilidades
de atraso y sobrecosto + explicación local con SHAP.

El pipeline replica exactamente el flujo del notebook 02.
"""

from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, field
import re

import joblib
import numpy as np
import pandas as pd


RAIZ = Path(__file__).resolve().parent.parent
DATA = RAIZ / 'data'
IMP  = DATA / 'imputers'
MOD  = DATA / 'modelos'


# Columnas crudas esperadas (las 53 del consolidado_global excepto targets)
COLS_CRUDAS = [
    'departamento', 'ciudad', 'orden', 'sector', 'rama', 'entidad_centralizada',
    'modalidad_de_contratacion', 'condiciones_de_entrega', 'es_grupo', 'es_pyme',
    'habilita_pago_adelantado', 'obligaci_n_ambiental', 'origen_de_los_recursos',
    'destino_gasto', 'valor_del_contrato', 'valor_de_pago_adelantado', 'estado_bpin',
    'g_nero_representante_legal', 'presupuesto_general_de_la_nacion_pgn',
    'sistema_general_de_participaciones', 'sistema_general_de_regal_as',
    'recursos_propios_alcald_as_gobernaciones_y_resguardos_ind_genas_',
    'recursos_de_credito', 'recursos_propios', 'tipo_de_cuenta',
    'el_contrato_puede_ser_prorrogado', 'documentos_tipo',
    'duracion_planificada_dias',
    'rup_idx_endeudamiento', 'rup_idx_liquidez', 'rup_ingresos',
    'rup_utilidad_neta', 'rup_multas',
    'log_valor_contrato', 'nacionalidad_representante_legal',
    'obligaciones_postconsumo', 'espostconflicto',
    'pilares_del_acuerdo', 'puntos_del_acuerdo',
    'codigo_de_categoria_principal', 'localizaci_n', 'tipodocproveedor',
    'esta_activa', 'pais_proveedor', 'departamento_proveedor',
    'rup_tamano', 'rup_empleados', 'rup_sanciones', 'rup_inhabilidad',
    'rup_activo_total', 'rup_patrimonio',
    'anios_empresa', 'n_proponentes_por_proceso',
]


@dataclass
class Prediccion:
    proba_atraso: float
    proba_sobrecosto: float
    top_factores_atraso: list[dict] = field(default_factory=list)
    features_recibidas: dict = field(default_factory=dict)
    features_imputadas: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'proba_atraso':     round(self.proba_atraso, 4),
            'proba_sobrecosto': round(self.proba_sobrecosto, 4),
            'top_factores_atraso': self.top_factores_atraso,
            'features_imputadas': self.features_imputadas,
        }


class Predictor:
    """Carga modelo + artifacts y expone .predict(input_dict)."""

    def __init__(self):
        self.modelo = joblib.load(MOD / 'lgbm.pkl')
        self.winsor = joblib.load(IMP / 'winsor_limits.pkl')
        self.freq_maps = joblib.load(IMP / 'freq_maps.pkl')
        self.imputer = joblib.load(IMP / 'imputer_mediana.pkl')

        # Recuperar cols esperadas por el modelo en el orden correcto
        ref = pd.read_parquet(DATA / 'consolidado_imputado.parquet').drop(
            columns=['tuvo_atraso', 'tuvo_sobrecosto'])
        self.cols_modelo = ref.columns.tolist()

        # Cols que requieren sanitización para LGBM (mismo patrón que notebook 09)
        self.cols_modelo_sanitized = [self._sanitize(c) for c in self.cols_modelo]

        # Identificar cols con flag _was_nan (las 9 con NaN del notebook 02)
        self.cols_con_was_nan = [
            c.replace('_was_nan', '')
            for c in self.cols_modelo if c.endswith('_was_nan')
        ]

        # SHAP explainer (lazy, se inicializa al primer uso)
        self._explainer = None

    @staticmethod
    def _sanitize(name: str) -> str:
        return re.sub(r'[^A-Za-z0-9_]+', '_', str(name))

    # ------------------------------------------------------------------ #
    # Pipeline de transformación                                          #
    # ------------------------------------------------------------------ #

    def _normalizar_input(self, raw: dict) -> dict:
        """Limpia y completa input crudo. NaN para no provistas."""
        out = {c: np.nan for c in COLS_CRUDAS}
        for k, v in raw.items():
            if k in out:
                out[k] = v
        # Derivar log_valor_contrato si solo se dio valor_del_contrato
        if not np.isnan_safe(out.get('log_valor_contrato', np.nan)):
            pass
        elif out.get('valor_del_contrato') and not pd.isna(out.get('valor_del_contrato')):
            v = float(out['valor_del_contrato'])
            if v > 0:
                out['log_valor_contrato'] = float(np.log10(v))
        return out

    def _aplicar_winsor(self, df: pd.DataFrame) -> pd.DataFrame:
        # Solo a cols que estaban en winsor_limits (numéricas continuas)
        for c, (p1, p99) in self.winsor.items():
            if c in df.columns:
                try:
                    df[c] = pd.to_numeric(df[c], errors='coerce').clip(p1, p99)
                except Exception:
                    pass
        return df

    def _aplicar_encoding(self, df: pd.DataFrame) -> pd.DataFrame:
        """Replica encoding del notebook 02 sobre 1 fila."""
        cols_freq = list(self.freq_maps.keys())
        # Cols que pasaron por winsor son numéricas
        cols_winsor = set(self.winsor.keys())
        # Categóricas = NO en winsor AND NO en freq_maps AND no son derivadas
        cols_cat_todas = [c for c in df.columns
                          if c not in cols_winsor and c not in cols_freq
                          and not c.startswith('_')]
        cols_ohe = [c for c in cols_cat_todas if c in COLS_CRUDAS]

        # OHE: rellenar NaN cat con 'desconocido'
        df_ohe = pd.DataFrame(index=df.index)
        if cols_ohe:
            tmp = df[cols_ohe].copy()
            for c in cols_ohe:
                tmp[c] = tmp[c].fillna('desconocido').astype(str)
            df_ohe = pd.get_dummies(tmp, drop_first=False, dtype=np.int8)

        # Freq encoding
        df_freq = pd.DataFrame(index=df.index)
        for c in cols_freq:
            if c not in df.columns:
                df_freq[c + '_freq'] = 0.0
                continue
            valor = df[c].iloc[0]
            if pd.isna(valor):
                df_freq[c + '_freq'] = 0.0
            else:
                fmap = self.freq_maps[c]
                df_freq[c + '_freq'] = fmap.get(str(valor), 0.0)
            df_freq[c + '_freq'] = df_freq[c + '_freq'].astype(np.float32)

        # Numéricas continuas (las que winsor procesa)
        df_num = pd.DataFrame(index=df.index)
        for c in cols_winsor:
            if c in df.columns:
                df_num[c] = pd.to_numeric(df[c], errors='coerce').astype(np.float32)

        return pd.concat([df_num, df_ohe, df_freq], axis=1)

    def _alinear_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        """Asegura mismo orden y cols que el modelo entrenó.

        Cols faltantes (ej. OHE de categorías no vistas) → 0.
        Cols extra (categorías nuevas) → drop.
        """
        # Identificar cols con NaN ANTES de imputar (para los flags)
        cols_imputables = [c for c in df.columns
                           if c in self.cols_modelo
                           and c not in [x + '_was_nan' for x in self.cols_con_was_nan]]
        # Construir flags
        flags = {}
        for c in self.cols_con_was_nan:
            if c in df.columns:
                flags[c + '_was_nan'] = int(pd.isna(df[c].iloc[0]))
            else:
                flags[c + '_was_nan'] = 1  # no provisto → was_nan

        # Imputar (rellenar NaN antes de alinear)
        # Solo cols numéricas con NaN
        for c in df.columns:
            if pd.api.types.is_numeric_dtype(df[c]):
                df[c] = df[c].fillna(self.imputer.statistics_[
                    list(self.cols_modelo).index(c)
                ] if c in self.cols_modelo else df[c].median())

        # Construir DataFrame final con orden exacto del modelo
        out = pd.DataFrame(0, index=df.index, columns=self.cols_modelo, dtype=np.float32)
        for c in df.columns:
            if c in out.columns:
                out[c] = df[c].astype(np.float32)
        # Aplicar flags
        for fcol, fval in flags.items():
            if fcol in out.columns:
                out[fcol] = np.float32(fval)

        return out

    def preprocess(self, raw_input: dict) -> tuple[pd.DataFrame, list[str]]:
        """Pipeline completo. Devuelve X listo para predict + lista de
        features imputadas (no provistas por el usuario)."""
        normalizado = self._normalizar_input(raw_input)
        imputadas = [c for c, v in normalizado.items()
                     if pd.isna(v) and c in raw_input.keys() is False]
        # Mejor lista: cols crudas no provistas explícitamente por el usuario
        imputadas = [c for c in COLS_CRUDAS if c not in raw_input]

        df_raw = pd.DataFrame([normalizado])
        df_w   = self._aplicar_winsor(df_raw)
        df_enc = self._aplicar_encoding(df_w)
        df_ok  = self._alinear_cols(df_enc)
        return df_ok, imputadas

    # ------------------------------------------------------------------ #
    # Predicción                                                          #
    # ------------------------------------------------------------------ #

    def predict(self, raw_input: dict) -> Prediccion:
        X, imputadas = self.preprocess(raw_input)
        # LGBM exige nombres sanitizados
        X_lgbm = X.copy()
        X_lgbm.columns = self.cols_modelo_sanitized

        proba_atraso = float(self.modelo.predict_proba(X_lgbm)[:, 1][0])

        # Sobrecosto: usar mismo modelo (entrenado para atraso) NO sirve;
        # como tenemos solo lgbm.pkl (target atraso), aproximamos con el
        # modelo XGB del sprint padre o devolvemos None. Para el prototipo,
        # entrenamos sobrecosto on-the-fly al cargar el predictor (cacheado).
        if not hasattr(self, '_modelo_sobrecosto'):
            self._modelo_sobrecosto = self._entrenar_sobrecosto()
        X_lgbm_sc = X_lgbm.copy()
        proba_sobrecosto = float(self._modelo_sobrecosto.predict_proba(X_lgbm_sc)[:, 1][0])

        # SHAP top factores
        top_factores = self._top_factores_shap(X_lgbm)

        return Prediccion(
            proba_atraso=proba_atraso,
            proba_sobrecosto=proba_sobrecosto,
            top_factores_atraso=top_factores,
            features_recibidas=raw_input,
            features_imputadas=imputadas,
        )

    def _entrenar_sobrecosto(self):
        """Carga el modelo de sobrecosto entrenado en notebook 12. Si no
        existe (porque ganador no fue lgbm), reentrena rápido."""
        path_sc = MOD / 'lgbm_sobrecosto.pkl'
        if path_sc.exists():
            return joblib.load(path_sc)

        # Entrenar rápido y persistir
        from lightgbm import LGBMClassifier
        from sklearn.model_selection import train_test_split

        df = pd.read_parquet(DATA / 'consolidado_imputado.parquet')
        y = df['tuvo_sobrecosto']
        X = df.drop(columns=['tuvo_atraso', 'tuvo_sobrecosto'])
        X_train, _, y_train, _ = train_test_split(
            X, y, test_size=0.20, stratify=y, random_state=42,
        )
        X_train.columns = [self._sanitize(c) for c in X_train.columns]

        # Mismos params que el ganador
        params = {
            'n_estimators': 800, 'num_leaves': 127, 'learning_rate': 0.020,
            'max_depth': -1, 'min_child_samples': 50,
            'subsample': 0.6645, 'colsample_bytree': 0.8159,
        }
        scale_pos = (y_train == 0).sum() / (y_train == 1).sum()
        mod_sc = LGBMClassifier(
            objective='binary', n_jobs=-1, random_state=42,
            scale_pos_weight=float(scale_pos), verbose=-1, **params,
        )
        mod_sc.fit(X_train, y_train)
        joblib.dump(mod_sc, path_sc)
        return mod_sc

    def _top_factores_shap(self, X_lgbm: pd.DataFrame, top_k: int = 3) -> list[dict]:
        """SHAP local. Top features que más empujan probabilidad."""
        try:
            import shap
            if self._explainer is None:
                self._explainer = shap.TreeExplainer(self.modelo)
            sv = self._explainer.shap_values(X_lgbm)
            # LGBM binario devuelve array 1D o tupla
            if isinstance(sv, list):
                sv_arr = sv[1][0] if len(sv) == 2 else sv[0][0]
            else:
                sv_arr = sv[0]
            df = pd.DataFrame({
                'feature': self.cols_modelo,
                'shap':    sv_arr,
                'valor':   X_lgbm.iloc[0].values,
            })
            df['abs'] = df['shap'].abs()
            df = df.sort_values('abs', ascending=False).head(top_k)
            return [
                {
                    'feature': r['feature'],
                    'contribucion': round(float(r['shap']), 4),
                    'direccion': 'aumenta_riesgo' if r['shap'] > 0 else 'reduce_riesgo',
                    'valor':   round(float(r['valor']), 4),
                }
                for _, r in df.iterrows()
            ]
        except Exception as e:
            return [{'error': str(e)}]


# Helper porque numpy.isnan no acepta strings
def _isnan_safe(x):
    try:
        return pd.isna(x)
    except Exception:
        return False
np.isnan_safe = _isnan_safe


if __name__ == '__main__':
    # Smoke test
    p = Predictor()
    caso = {
        'departamento': 'Distrito Capital de Bogotá',
        'ciudad': 'Bogotá',
        'modalidad_de_contratacion': 'Licitación pública Obra Publica',
        'valor_del_contrato': 2_000_000_000,
        'duracion_planificada_dias': 365,
        'es_pyme': 'Si',
        'es_grupo': 'No',
        'sector': 'Vivienda Ciudad y Territorio',
        'orden': 'Territorial',
    }
    pred = p.predict(caso)
    import json
    print(json.dumps(pred.to_dict(), indent=2, ensure_ascii=False))
