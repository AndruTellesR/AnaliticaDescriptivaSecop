"""
eda_comun.py — Modulo de apoyo del EDA EXTENDIDO INTEGRAL sobre el universo completo.

Autoria: Andres Telles. Codigo propio, escrito para este ejercicio.

Contiene: rutas, reglas de blindaje de autoria, carga y deduplicacion de las tres
fuentes, derivacion propia de los indicadores de la restriccion de hierro, marca de
observabilidad segun los criterios 3.6.3/3.6.4 del anteproyecto, helpers estadisticos
con tamano de efecto y utilidades de figura.

Ninguna funcion de este modulo lee las columnas prohibidas declaradas en el numeral 4
del prompt (producidas por codigo excluido del blindaje de autoria).
"""

from __future__ import annotations

import re
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
SRC_DIR = Path(__file__).resolve().parent
BASE_DIR = SRC_DIR.parent                      # eda-extendido-integral/
REPO = BASE_DIR.parent                         # raiz del repositorio
DATASETS = REPO / "entregables" / "04-datasets"

DIR_DATA = BASE_DIR / "data"
DIR_FIG = BASE_DIR / "figuras"
DIR_DOCS = BASE_DIR / "docs"
for _d in (DIR_DATA, DIR_FIG, DIR_DOCS):
    _d.mkdir(parents=True, exist_ok=True)

P_CONTRATOS = DATASETS / "contratos_adiciones_obra.parquet"
P_PROCESOS = DATASETS / "procesos_contratacion_obra.parquet"
P_PROVEEDORES = DATASETS / "proveedores_obra.parquet"

# ---------------------------------------------------------------------------
# Parametros metodologicos declarados a priori
# ---------------------------------------------------------------------------
ALFA = 0.05
N_UNIVERSO_ESPERADO = 48331
N_OBSERVABLE_ESPERADO = 19194

# ---------------------------------------------------------------------------
# Blindaje de autoria (numeral 4 del prompt)
# ---------------------------------------------------------------------------
COLUMNAS_PROHIBIDAS = [
    # notebooks/07 (excluido)
    "tiempo", "presupuesto", "alcance",
    # notebooks/08 (excluido)
    "rup_idx_endeudamiento", "rup_idx_liquidez", "rup_ingresos",
    "rup_utilidad_neta", "rup_multas",
    # scripts excluidos
    "pliego_liquidez_min", "pliego_endeudamiento_max_pct",
    "pliego_cobertura_intereses_min", "pliego_rentabilidad_patrimonio_min_pct",
    "pliego_rentabilidad_activo_min_pct", "pliego_capital_trabajo_min_pct_presupuesto",
]

COLUMNAS_NO_USADAS = [
    # derivadas del pipeline compartido; se re-derivan por cuenta propia
    "sobrecosto_ratio", "duracion_planificada_dias", "ratio_extension_duracion",
    "dias_hasta_primera_adicion", "ventana_adiciones_dias", "log_valor_contrato",
]

COLUMNAS_PIPELINE_PERMITIDAS = [
    "dias_adicionados", "n_adicion_valor", "n_cesion", "n_conclusion", "n_extension",
    "n_modificaciones_total", "n_suspension", "n_tipos_distintos",
    "tiene_conclusion", "tiene_suspension", "tiene_cesion", "tiene_extension_dias",
    "tiene_adicion_valor", "tiene_modificacion",
]


def verificar_blindaje(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve el estado del blindaje: ninguna columna prohibida ni no-usada presente."""
    presentes_prohibidas = [c for c in COLUMNAS_PROHIBIDAS if c in df.columns]
    presentes_no_usadas = [c for c in COLUMNAS_NO_USADAS if c in df.columns]
    return pd.DataFrame(
        {
            "regla": [
                "Columnas prohibidas (codigo excluido) presentes",
                "Columnas del pipeline no usadas presentes",
                "Columnas del pipeline permitidas disponibles",
            ],
            "n": [
                len(presentes_prohibidas),
                len(presentes_no_usadas),
                len([c for c in COLUMNAS_PIPELINE_PERMITIDAS if c in df.columns]),
            ],
            "detalle": [
                ", ".join(presentes_prohibidas) or "ninguna",
                ", ".join(presentes_no_usadas) or "ninguna",
                str(len([c for c in COLUMNAS_PIPELINE_PERMITIDAS if c in df.columns])) + " de 14",
            ],
            "estado": [
                "OK" if not presentes_prohibidas else "VIOLACION",
                "OK" if not presentes_no_usadas else "VIOLACION",
                "OK",
            ],
        }
    )


def descartar_columnas_blindadas(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina fisicamente del DataFrame las columnas prohibidas y las no usadas."""
    a_quitar = [c for c in COLUMNAS_PROHIBIDAS + COLUMNAS_NO_USADAS if c in df.columns]
    return df.drop(columns=a_quitar)


# ---------------------------------------------------------------------------
# Carga de fuentes
# ---------------------------------------------------------------------------
COLS_PROC_NUM = [
    "precio_base", "proveedores_invitados", "proveedores_con_invitacion",
    "proveedores_que_manifestaron", "respuestas_al_procedimiento", "respuestas_externas",
    "conteo_de_respuestas_a_ofertas", "proveedores_unicos_con", "visualizaciones_del",
    "numero_de_lotes", "duracion", "valor_total_adjudicacion",
]

COLS_PROC_UTILES = COLS_PROC_NUM + [
    "id_del_portafolio", "unidad_de_duracion", "adjudicado", "estado_resumen", "fase",
    "modalidad_de_contratacion", "tipo_de_contrato", "estado_del_procedimiento",
    "fecha_de_publicacion", "fecha_adjudicacion",
]

# Descartadas por varianza cero documentada en la fuente de proveedores (numeral 5)
COLS_PROV_DESCARTADAS = ["es_entidad", "esta_activa", "pais", "es_grupo"]
COLS_PROV_UTILES = [
    "codigo", "tipo_empresa", "espyme", "fecha_creacion",
    "codigo_categoria_principal", "departamento", "municipio",
]


def cargar_contratos(blindar: bool = True) -> pd.DataFrame:
    """Carga el dataset integrado de 48.331 contratos.

    El insumo proviene del pipeline compartido (notebooks/00-06), cuya autoria sigue
    pendiente de confirmacion con el director (MATRIZ_OBJETIVOS_CODIGO.md, prioridad 1).
    """
    df = pd.read_parquet(P_CONTRATOS)
    if blindar:
        df = descartar_columnas_blindadas(df)
    return df


def cargar_procesos_dedup() -> tuple[pd.DataFrame, dict]:
    """Carga procesos y lo deduplica al grano de `id_del_portafolio`.

    Regla de precedencia declarada: dentro de un mismo portafolio se conserva la fila
    adjudicada (`adjudicado == 'Si'`) y, entre ellas, la de publicacion mas reciente.
    Es una decision metodologica deliberada: las variables de competencia son
    practicamente invariantes dentro del portafolio (se reporta la evidencia en el
    notebook 01), de modo que la eleccion de fila no altera su distribucion.
    """
    proc = pd.read_parquet(P_PROCESOS)
    diag = {
        "filas_originales": len(proc),
        "dup_id_del_proceso": int(proc["id_del_proceso"].duplicated().sum()),
        "dup_id_del_portafolio": int(proc["id_del_portafolio"].duplicated().sum()),
        "portafolios_unicos": int(proc["id_del_portafolio"].nunique()),
    }
    for c in COLS_PROC_NUM:
        proc[c] = pd.to_numeric(proc[c], errors="coerce")
    proc["_adjudicado_flag"] = (proc["adjudicado"] == "Si").astype(int)
    proc["_fecha_pub"] = pd.to_datetime(proc["fecha_de_publicacion"], errors="coerce")
    proc = proc.sort_values(
        ["id_del_portafolio", "_adjudicado_flag", "_fecha_pub"],
        ascending=[True, False, False], na_position="last",
    )
    dedup = proc.drop_duplicates("id_del_portafolio", keep="first")
    dedup = dedup[[c for c in COLS_PROC_UTILES if c in dedup.columns]].copy()
    diag["filas_deduplicadas"] = len(dedup)
    return dedup, diag


def cargar_proveedores_dedup() -> tuple[pd.DataFrame, dict]:
    """Carga el registro de proveedores deduplicado por `codigo`."""
    prov = pd.read_parquet(P_PROVEEDORES)
    diag = {
        "filas_originales": len(prov),
        "dup_codigo": int(prov["codigo"].duplicated().sum()),
        "codigos_unicos": int(prov["codigo"].nunique()),
        "varianza_cero": {c: int(prov[c].nunique(dropna=False)) for c in COLS_PROV_DESCARTADAS},
    }
    prov = prov.drop_duplicates("codigo", keep="first")
    prov = prov[[c for c in COLS_PROV_UTILES if c in prov.columns]].copy()
    prov["fecha_creacion"] = pd.to_datetime(prov["fecha_creacion"], errors="coerce")
    diag["filas_deduplicadas"] = len(prov)
    return prov, diag


# ---------------------------------------------------------------------------
# Derivaciones propias
# ---------------------------------------------------------------------------
_RE_DURACION = re.compile(r"(\d+)\s*(Dia|Mes)", flags=re.IGNORECASE)


def parsear_duracion_dias(texto) -> float:
    """Parseo propio de `duraci_n_del_contrato` (texto libre).

    Regla declarada: 'Dia(s)' se toma literal; 'Mes(es)' se multiplica por 30;
    cualquier otro formato ('No definido', unidades no reconocidas) devuelve NaN.
    """
    if pd.isna(texto):
        return np.nan
    m = _RE_DURACION.match(str(texto).strip())
    if not m:
        return np.nan
    n, unidad = int(m.group(1)), m.group(2).lower()
    return float(n * 30) if unidad == "mes" else float(n)


_FACTOR_UNIDAD = {
    "día(s)": 1.0, "dia(s)": 1.0, "Dia(s)": 1.0,
    "Semana(s)": 7.0, "Mes(es)": 30.0, "Año(s)": 365.0, "Hora(s)": 1 / 24,
}


def duracion_proceso_dias(duracion, unidad) -> float:
    """Convierte `duracion` + `unidad_de_duracion` de procesos a dias.

    Fuente independiente del mismo dato que `duraci_n_del_contrato`; se usa para
    validar el parseo propio (insight N-08).
    """
    if pd.isna(duracion) or pd.isna(unidad):
        return np.nan
    f = _FACTOR_UNIDAD.get(str(unidad).strip())
    if f is None:
        return np.nan
    return float(duracion) * f


DOCS_PERSONA_NATURAL = [
    "Cédula de Ciudadanía", "Cédula de Extranjería", "Tarjeta de Identidad",
    "Permiso especial de permanencia",
]


def derivar_tipo_contratista(df: pd.DataFrame) -> pd.Series:
    """Deriva tipo_contratista desde columnas del propio contrato (insight N-07)."""
    es_grupo = df["es_grupo"]
    tdoc = df["tipodocproveedor"]
    out = pd.Series("No definido", index=df.index, dtype=object)
    out[tdoc.isin(DOCS_PERSONA_NATURAL)] = "Persona Natural"
    out[tdoc == "NIT"] = "Persona Juridica"
    out[es_grupo == "Si"] = "Consorcio / Union Temporal"
    return out


ESTADOS_FINALIZADOS = ["terminado", "Cerrado", "cedido"]
ESTADOS_ACTIVOS = [
    "En ejecución", "Suspendido", "Cancelado", "Borrador",
    "Aprobado", "En aprobación", "enviado Proveedor",
]


def marcar_observable(df: pd.DataFrame) -> tuple[pd.Series, pd.DataFrame]:
    """Construye la marca booleana `observable` (criterios 3.6.3/3.6.4).

    Devuelve la serie booleana alineada al indice de `df` y el embudo paso a paso
    sobre el universo completo. Cada paso se acumula: la marca final es la conjuncion.
    """
    n0 = len(df)
    firma = pd.to_datetime(df["fecha_de_firma"], errors="coerce")
    c1 = (firma >= "2018-01-01") & (firma <= "2024-12-31")
    c2 = c1 & df[
        ["valor_del_contrato", "fecha_de_inicio_del_contrato",
         "fecha_de_fin_del_contrato", "estado_contrato"]
    ].notna().all(axis=1)
    c3 = c2 & (df["valor_del_contrato"] > 0)
    c4 = c3 & (df["fecha_de_fin_del_contrato"] >= df["fecha_de_inicio_del_contrato"])
    incluir = df["estado_contrato"].isin(ESTADOS_FINALIZADOS) | (df["liquidaci_n"] == "Si")
    excluir = df["estado_contrato"].isin(ESTADOS_ACTIVOS)
    c5 = c4 & incluir & ~excluir

    embudo = pd.DataFrame(
        {
            "paso": [
                "0. Universo completo de contratos de obra integrados",
                "1. Fecha de firma dentro de 2018-2024 (3.6.3)",
                "2. Campos minimos no nulos: valor, fechas, estado (3.6.3)",
                "3. Excluidos valor_del_contrato <= 0 (3.6.4)",
                "4. Excluidas fechas invertidas fin < inicio (3.6.4)",
                "5. Estado avanzado/finalizado excluyendo activos, criterio conservador (3.6.3/3.6.4)",
            ],
            "contratos": [n0, int(c1.sum()), int(c2.sum()), int(c3.sum()),
                          int(c4.sum()), int(c5.sum())],
        }
    )
    embudo["retencion_pct"] = (embudo["contratos"] / n0 * 100).round(2)
    embudo["perdida_paso"] = embudo["contratos"].diff().fillna(0).astype(int)
    return c5.rename("observable"), embudo


def clasificar_alcance(df: pd.DataFrame) -> pd.Series:
    """Indice de alcance categorico con precedencia explicita.

    conclusion > (suspension | cesion) > entrega total.
    """
    out = pd.Series("Entregado en su totalidad", index=df.index, dtype=object)
    parcial = (df["tiene_suspension"] == 1) | (df["tiene_cesion"] == 1)
    out[parcial] = "Entregado parcialmente"
    out[df["tiene_conclusion"] == 1] = "No entregado"
    return out


ORDEN_ALCANCE = ["Entregado en su totalidad", "Entregado parcialmente", "No entregado"]

BINS_CUANTIA = [0, 50e6, 200e6, 1e9, 10e9, np.inf]
ETIQ_CUANTIA = ["<50M", "50M-200M", "200M-1.000M", "1.000M-10.000M", ">10.000M"]

BINS_COMPETENCIA = [-0.5, 0.5, 1.5, 3.5, 9.5, np.inf]
ETIQ_COMPETENCIA = ["0 (sin oferta registrada)", "1 (oferente unico)", "2-3 (baja)",
                    "4-9 (media)", "10+ (alta)"]

BINS_PLAZO = [-np.inf, 30, 90, 180, 365, 730, np.inf]
ETIQ_PLAZO = ["<=1 mes", "1-3 meses", "3-6 meses", "6-12 meses", "1-2 anios", ">2 anios"]

MODALIDADES_ALTA_COMPETENCIA = ["Licitación pública", "Licitación pública Obra Publica"]


def es_licitacion_publica(serie: pd.Series) -> pd.Series:
    return serie.astype(str).str.startswith("Licitación pública")


# ---------------------------------------------------------------------------
# Helpers estadisticos — siempre con tamano de efecto y N efectivo
# ---------------------------------------------------------------------------
def interpretar_r(r: float) -> str:
    a = abs(r)
    if a < 0.1:
        return "nulo"
    if a < 0.3:
        return "pequeno"
    if a < 0.5:
        return "mediano"
    return "grande"


def interpretar_v(v: float) -> str:
    if v < 0.1:
        return "nulo/insignificante"
    if v < 0.2:
        return "debil"
    if v < 0.3:
        return "debil-moderado"
    if v < 0.5:
        return "moderado"
    return "fuerte"


def mann_whitney(a, b, etiqueta_a="grupo A", etiqueta_b="grupo B") -> dict:
    """Mann-Whitney U con rank-biserial. Signo negativo = el grupo A tiene rangos mayores."""
    a = pd.Series(a).dropna().astype(float)
    b = pd.Series(b).dropna().astype(float)
    n1, n2 = len(a), len(b)
    if n1 < 3 or n2 < 3:
        return {"prueba": "Mann-Whitney U", "n_a": n1, "n_b": n2, "U": np.nan,
                "p": np.nan, "rank_biserial": np.nan, "efecto": "N insuficiente",
                "mediana_a": np.nan, "mediana_b": np.nan,
                "etiqueta_a": etiqueta_a, "etiqueta_b": etiqueta_b, "significativo": False}
    u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    rb = 1 - (2 * u) / (n1 * n2)
    return {
        "prueba": "Mann-Whitney U", "etiqueta_a": etiqueta_a, "etiqueta_b": etiqueta_b,
        "n_a": n1, "n_b": n2, "n_efectivo": n1 + n2,
        "mediana_a": float(a.median()), "mediana_b": float(b.median()),
        "U": float(u), "p": float(p), "rank_biserial": float(rb),
        "efecto": interpretar_r(rb), "significativo": bool(p < ALFA),
    }


def cramers_v(tabla: pd.DataFrame) -> dict:
    """Chi-cuadrado + V de Cramer con verificacion de frecuencias esperadas."""
    chi2, p, gl, esperadas = stats.chi2_contingency(tabla)
    n = tabla.values.sum()
    k = min(tabla.shape) - 1
    v = np.sqrt(chi2 / (n * k)) if n > 0 and k > 0 else np.nan
    return {
        "prueba": "Chi-cuadrado de independencia", "chi2": float(chi2), "gl": int(gl),
        "p": float(p), "V_cramer": float(v), "efecto": interpretar_v(v),
        "n_efectivo": int(n),
        "min_esperada": float(esperadas.min()),
        "pct_celdas_esperada_menor_5": float((esperadas < 5).mean() * 100),
        "significativo": bool(p < ALFA),
    }


def kruskal(grupos: dict) -> dict:
    """Kruskal-Wallis con epsilon-cuadrado como tamano de efecto."""
    limpio = {k: pd.Series(v).dropna().astype(float) for k, v in grupos.items()}
    limpio = {k: v for k, v in limpio.items() if len(v) >= 3}
    if len(limpio) < 2:
        return {"prueba": "Kruskal-Wallis", "H": np.nan, "p": np.nan,
                "epsilon2": np.nan, "efecto": "N insuficiente", "k_grupos": len(limpio),
                "n_efectivo": int(sum(len(v) for v in limpio.values())), "significativo": False}
    h, p = stats.kruskal(*limpio.values())
    n = int(sum(len(v) for v in limpio.values()))
    k = len(limpio)
    eps2 = (h - k + 1) / (n - k) if n > k else np.nan
    return {
        "prueba": "Kruskal-Wallis", "H": float(h), "p": float(p), "gl": k - 1,
        "epsilon2": float(eps2), "efecto": interpretar_v(np.sqrt(max(eps2, 0))),
        "k_grupos": k, "n_efectivo": n, "significativo": bool(p < ALFA),
    }


def spearman(x, y) -> dict:
    d = pd.DataFrame({"x": pd.to_numeric(pd.Series(x), errors="coerce"),
                      "y": pd.to_numeric(pd.Series(y), errors="coerce")}).dropna()
    if len(d) < 5:
        return {"rho": np.nan, "p": np.nan, "n_efectivo": len(d), "efecto": "N insuficiente"}
    rho, p = stats.spearmanr(d["x"], d["y"])
    return {"rho": float(rho), "p": float(p), "n_efectivo": int(len(d)),
            "efecto": interpretar_r(rho), "significativo": bool(p < ALFA)}


def fmt_p(p: float) -> str:
    if pd.isna(p):
        return "n/d"
    if p < 1e-300:
        return "< 1e-300"
    if p < 0.001:
        return f"{p:.2e}"
    return f"{p:.4f}"


def resumen_prueba(res: dict) -> str:
    """Linea de texto estandar para reportar una prueba con su tamano de efecto."""
    if res.get("prueba") == "Mann-Whitney U":
        base = (f"Mann-Whitney U = {res['U']:,.1f} | p = {fmt_p(res['p'])} | "
                f"rank-biserial = {res['rank_biserial']:+.3f} ({res['efecto']}) | "
                f"N efectivo = {res['n_a']:,} ({res['etiqueta_a']}) vs {res['n_b']:,} ({res['etiqueta_b']}) | "
                f"medianas {res['mediana_a']:,.2f} vs {res['mediana_b']:,.2f}")
    elif res.get("prueba", "").startswith("Chi"):
        base = (f"chi2 = {res['chi2']:,.2f} | gl = {res['gl']} | p = {fmt_p(res['p'])} | "
                f"V de Cramer = {res['V_cramer']:.3f} ({res['efecto']}) | "
                f"N efectivo = {res['n_efectivo']:,} | minima frecuencia esperada = {res['min_esperada']:.1f}")
    elif res.get("prueba") == "Kruskal-Wallis":
        base = (f"H = {res['H']:,.2f} | gl = {res['gl']} | p = {fmt_p(res['p'])} | "
                f"epsilon2 = {res['epsilon2']:.4f} ({res['efecto']}) | "
                f"k = {res['k_grupos']} grupos | N efectivo = {res['n_efectivo']:,}")
    else:
        base = str(res)
    if res.get("significativo") and res.get("efecto") in ("nulo", "nulo/insignificante"):
        base += "\n  ADVERTENCIA: significancia estadistica con tamano de efecto nulo. Con N grande esto NO sostiene la hipotesis."
    return base


# ---------------------------------------------------------------------------
# Doble lectura
# ---------------------------------------------------------------------------
def doble_lectura(df: pd.DataFrame, funcion, nombre: str) -> pd.DataFrame:
    """Aplica `funcion` al universo completo y al subconjunto observable."""
    total = funcion(df)
    obs = funcion(df[df["observable"]])
    if np.isscalar(total):
        return pd.DataFrame({"metrica": [nombre],
                             "universo_completo": [total], "observable": [obs]})
    out = pd.DataFrame({"universo_completo": total, "observable": obs})
    out.index.name = nombre
    return out


# ---------------------------------------------------------------------------
# Figuras — paleta validada, modo claro (las figuras se embeben como PNG)
# ---------------------------------------------------------------------------
PALETA = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
          "#e87ba4", "#008300", "#4a3aa7", "#e34948"]
SURFACE = "#fcfcfb"
TEXT_1 = "#0b0b0b"
TEXT_2 = "#52514e"
GRID = "#e3e2de"
SEQ_BLUE = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
DIVERGENTE = ["#0d366b", "#256abf", "#6da7ec", "#cde2fb", "#f0efec",
              "#f6c9c9", "#e88a89", "#e34948", "#a82322"]


def configurar_matplotlib():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE, "figure.dpi": 110, "savefig.dpi": 110,
        "font.size": 10, "axes.titlesize": 12, "axes.titleweight": "bold",
        "axes.labelsize": 10, "axes.labelcolor": TEXT_2,
        "axes.edgecolor": GRID, "axes.linewidth": 0.8,
        "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7, "grid.alpha": 0.9,
        "axes.spines.top": False, "axes.spines.right": False,
        "xtick.color": TEXT_2, "ytick.color": TEXT_2,
        "text.color": TEXT_1, "legend.frameon": False,
        "axes.prop_cycle": plt.cycler(color=PALETA),
        "figure.autolayout": False,
    })
    cmap_seq = LinearSegmentedColormap.from_list("seq_blue", SEQ_BLUE)
    cmap_div = LinearSegmentedColormap.from_list("div_br", DIVERGENTE)
    return plt, cmap_seq, cmap_div


def guardar_mostrar(fig, nombre: str):
    """Guarda la figura en figuras/ y la muestra embebida en el notebook."""
    from IPython.display import Image, display
    import matplotlib.pyplot as plt
    ruta = DIR_FIG / nombre
    fig.savefig(ruta, bbox_inches="tight")
    plt.close(fig)
    display(Image(filename=str(ruta)))
    print("Figura persistida:", ruta.name)


def miles(x) -> str:
    return f"{x:,.0f}".replace(",", ".")


def pct(x, d=1) -> str:
    return f"{x:.{d}f}%"


# ---------------------------------------------------------------------------
# Trazabilidad de celdas: toda cifra citada debe poder localizarse
# ---------------------------------------------------------------------------
_CELDAS: dict = {}


def marcar(nombre: str) -> int:
    """Registra el `execution_count` de la celda actual bajo un nombre logico.

    Permite que cada hallazgo cite la celda exacta que produjo su evidencia. El
    numero es el `execution_count` que queda persistido en el .ipynb ejecutado, de
    modo que la cita es verificable abriendo el cuaderno.
    """
    try:
        from IPython import get_ipython
        n = int(get_ipython().execution_count)
    except Exception:
        n = -1
    _CELDAS[nombre] = n
    return n


def ref(nombre: str) -> str:
    return f"c{_CELDAS.get(nombre, -1):03d}"


# ---------------------------------------------------------------------------
# Registro de hallazgos etiquetados
# ---------------------------------------------------------------------------
ETIQUETAS_VALIDAS = {"A-OE02", "A-OE03", "A-OE04", "A-H1", "A-H2", "A-H3",
                     "B-OE2", "B-OE3-insumo", "CALIDAD"}


class RegistroHallazgos:
    """Acumula hallazgos etiquetados y los persiste como CSV para la tabla maestra."""

    def __init__(self, notebook: str):
        self.notebook = notebook
        self.filas = []

    def add(self, hid, titulo, evidencia, celda, etiquetas, valor="Medio", nota=""):
        etq = [e.strip() for e in etiquetas]
        for e in etq:
            if e not in ETIQUETAS_VALIDAS:
                raise ValueError(f"Etiqueta no valida: {e}")
        self.filas.append({
            "id": hid, "notebook": self.notebook, "celda": celda,
            "hallazgo": titulo, "evidencia": evidencia,
            "etiquetas": " ".join(f"[{e}]" for e in etq),
            "valor": valor, "nota": nota,
        })
        return self

    def tabla(self) -> pd.DataFrame:
        return pd.DataFrame(self.filas)

    def guardar(self) -> Path:
        ruta = DIR_DATA / f"hallazgos_{self.notebook}.csv"
        self.tabla().to_csv(ruta, index=False)
        return ruta
