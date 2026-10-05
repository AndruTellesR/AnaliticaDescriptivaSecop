"""Tablero interactivo de analitica descriptiva de contratacion de obra publica (SECOP II).

Objetivo especifico que atiende: OE-04 del anteproyecto (AnteproyectoAndres.md, numeral 1.4.2,
RF-05): "Disenar visualizaciones y tableros interactivos que presenten resultados (distribuciones,
outliers con box plots, segmentaciones por modalidad/entidad/territorio) para apoyar la
interpretacion, la transparencia y la toma de decisiones."

Universo: 48.331 contratos de obra publica (lectura oficial "universo_completo", instruccion del
tutor de usar el total de datos disponibles, sin la restriccion temporal 2018-2024 del anteproyecto
original). Fuente: eda-extendido-integral/data/universo_extendido.parquet, ya calculado y verificado
en esa carpeta; este tablero no recalcula ningun indicador, solo los visualiza.
"""

import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Contratacion de Obra Publica SECOP II", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "universo_completo.parquet"


@st.cache_data
def cargar_datos():
    return pd.read_parquet(DATA_PATH)


df = cargar_datos()

# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------
st.title("Analitica descriptiva de la contratacion de obra publica en Colombia")
st.caption(
    "Universo completo: 48.331 contratos de obra publica de SECOP II (lectura oficial). "
    "Marco teorico: restriccion de hierro (tiempo, costo, alcance)."
)

# ---------------------------------------------------------------------------
# Filtros dinamicos (barra lateral) — aplican a todas las secciones
# ---------------------------------------------------------------------------
st.sidebar.header("Filtros")

modalidades = ["Todas"] + sorted(df["modalidad_de_contratacion"].dropna().unique().tolist())
modalidad_sel = st.sidebar.selectbox("Modalidad de contratacion", modalidades)

departamentos = ["Todos"] + sorted(df["departamento"].dropna().unique().tolist())
departamento_sel = st.sidebar.selectbox("Departamento", departamentos)

ordenes = ["Todos"] + sorted(df["orden"].dropna().unique().tolist())
orden_sel = st.sidebar.selectbox("Orden de la entidad", ordenes)

tipos_contratista = ["Todos"] + sorted(df["tipo_contratista"].dropna().unique().tolist())
tipo_contratista_sel = st.sidebar.selectbox("Tipo de contratista", tipos_contratista)

datos = df.copy()
if modalidad_sel != "Todas":
    datos = datos[datos["modalidad_de_contratacion"] == modalidad_sel]
if departamento_sel != "Todos":
    datos = datos[datos["departamento"] == departamento_sel]
if orden_sel != "Todos":
    datos = datos[datos["orden"] == orden_sel]
if tipo_contratista_sel != "Todos":
    datos = datos[datos["tipo_contratista"] == tipo_contratista_sel]

st.sidebar.markdown("---")
st.sidebar.metric("Contratos filtrados", f"{len(datos):,}".replace(",", "."))
st.sidebar.metric("Contratos en el universo", f"{len(df):,}".replace(",", "."))

st.sidebar.markdown("---")
st.sidebar.caption(
    "Winsorizacion P1-P99 aplicada unicamente para las visualizaciones de esta pagina "
    "(no modifica los datos ni los indicadores)."
)


def winsorizar(serie: pd.Series, p_bajo: float = 0.01, p_alto: float = 0.99) -> pd.Series:
    s = serie.dropna()
    if s.empty:
        return s
    lo, hi = s.quantile(p_bajo), s.quantile(p_alto)
    return s.clip(lo, hi)


tab_dist, tab_outliers, tab_segmentado = st.tabs(
    ["Distribuciones", "Outliers (box plots)", "Segmentaciones"]
)

# ---------------------------------------------------------------------------
# TAB 1 — Distribuciones
# ---------------------------------------------------------------------------
with tab_dist:
    st.subheader("Distribuciones de los indicadores de la restriccion de hierro")

    col1, col2 = st.columns(2)

    with col1:
        n_tiempo = datos["deslizamiento_plazo_dias"].notna().sum()
        st.markdown(f"**Deslizamiento del plazo contractual (dias)** — N = {n_tiempo:,}".replace(",", "."))
        fig = px.histogram(
            datos.assign(_v=winsorizar(datos["deslizamiento_plazo_dias"])),
            x="_v", nbins=50,
            labels={"_v": "Dias (positivo = retraso; winsorizado P1-P99)"},
        )
        fig.add_vline(x=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
        if n_tiempo > 0:
            st.caption(
                f"Mediana: {datos['deslizamiento_plazo_dias'].median():.1f} dias | "
                f"% con retraso (>0): {(datos['deslizamiento_plazo_dias'] > 0).mean() * 100:.1f}%"
            )

    with col2:
        n_costo = datos["desviacion_costo_pct"].notna().sum()
        st.markdown(f"**Desviacion de costo (%)** — N = {n_costo:,}".replace(",", "."))
        fig = px.histogram(
            datos.assign(_v=winsorizar(datos["desviacion_costo_pct"])),
            x="_v", nbins=50,
            labels={"_v": "% de desviacion (positivo = sobrecosto; winsorizado P1-P99)"},
        )
        fig.add_vline(x=0, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
        if n_costo > 0:
            st.caption(
                f"Mediana: {datos['desviacion_costo_pct'].median():.2f}% | "
                f"% con sobrecosto (>0): {(datos['desviacion_costo_pct'] > 0).mean() * 100:.2f}%"
            )

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Valor del contrato (escala log10, COP)**")
        valores_pos = datos.loc[datos["valor_del_contrato"] > 0, "valor_del_contrato"]
        if len(valores_pos) > 0:
            import numpy as np
            fig = px.histogram(x=np.log10(valores_pos), nbins=50,
                                labels={"x": "log10(valor del contrato)"})
            st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("**Indice de cumplimiento de alcance**")
        orden_cats = ["Entregado en su totalidad", "Entregado parcialmente", "No entregado"]
        conteo = datos["indice_alcance"].value_counts().reindex(orden_cats).fillna(0)
        fig = px.bar(x=conteo.index, y=conteo.values,
                     labels={"x": "", "y": "Numero de contratos"},
                     color=conteo.index,
                     color_discrete_map={
                         "Entregado en su totalidad": "#38a169",
                         "Entregado parcialmente": "#f6ad55",
                         "No entregado": "#e53e3e",
                     })
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 2 — Outliers (box plots)
# ---------------------------------------------------------------------------
with tab_outliers:
    st.subheader("Deteccion de valores atipicos (box plots)")
    st.caption(
        "Los box plots se calculan sobre el dato winsorizado en P1-P99 solo para visualizacion; "
        "los indicadores originales, con sus valores extremos, se conservan intactos en los datasets."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Deslizamiento del plazo (dias)**")
        fig = px.box(datos.assign(_v=winsorizar(datos["deslizamiento_plazo_dias"])), y="_v",
                     labels={"_v": "Dias"})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Desviacion de costo (%)**")
        fig = px.box(datos.assign(_v=winsorizar(datos["desviacion_costo_pct"])), y="_v",
                     labels={"_v": "%"})
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("**Plazo pactado (dias)**")
        fig = px.box(datos.assign(_v=winsorizar(datos["plazo_pactado_dias"])), y="_v",
                     labels={"_v": "Dias"})
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# TAB 3 — Segmentaciones por modalidad / entidad / territorio
# ---------------------------------------------------------------------------
with tab_segmentado:
    st.subheader("Segmentaciones por modalidad, entidad y territorio")

    col_a, col_b = st.columns(2)
    with col_a:
        indicador_sel = st.selectbox(
            "Indicador a segmentar",
            ["Deslizamiento del plazo (dias)", "Desviacion de costo (%)"],
        )
    with col_b:
        eje_sel = st.selectbox(
            "Segmentar por",
            ["Modalidad de contratacion", "Tipo de contratista", "Sector (entidad)",
             "Orden (entidad)", "Departamento (territorio)"],
        )

    col_map = {
        "Deslizamiento del plazo (dias)": "deslizamiento_plazo_dias",
        "Desviacion de costo (%)": "desviacion_costo_pct",
    }
    eje_map = {
        "Modalidad de contratacion": "modalidad_de_contratacion",
        "Tipo de contratista": "tipo_contratista",
        "Sector (entidad)": "sector",
        "Orden (entidad)": "orden",
        "Departamento (territorio)": "departamento",
    }
    col_ind = col_map[indicador_sel]
    col_eje = eje_map[eje_sel]

    # Para departamento/sector, limitar a los de mayor volumen para legibilidad
    top_n = 12
    top_cats = datos[col_eje].value_counts().head(top_n).index
    sub = datos[datos[col_eje].isin(top_cats)].copy()
    sub["_v"] = winsorizar(sub[col_ind])

    orden_cats_plot = sub.groupby(col_eje)[col_ind].median().sort_values(ascending=False).index.tolist()

    fig = px.box(sub, x=col_eje, y="_v", category_orders={col_eje: orden_cats_plot},
                 labels={"_v": indicador_sel, col_eje: eje_sel})
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    fig.update_xaxes(tickangle=30)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"**Tabla resumen — {indicador_sel} por {eje_sel}** (top {top_n} por volumen)")
    tabla = (
        sub.groupby(col_eje)
        .agg(n_contratos=("id_contrato", "count"), mediana=(col_ind, "median"))
        .reindex(orden_cats_plot)
        .rename(columns={"n_contratos": "N. contratos", "mediana": f"Mediana {indicador_sel}"})
    )
    st.dataframe(tabla, use_container_width=True)

    st.markdown(f"**Indice de cumplimiento de alcance por {eje_sel}** (top {top_n} por volumen, %)")
    ct = pd.crosstab(sub[col_eje], sub["indice_alcance"], normalize="index") * 100
    ct = ct.reindex(orden_cats_plot)
    orden_cats = ["Entregado en su totalidad", "Entregado parcialmente", "No entregado"]
    ct = ct[[c for c in orden_cats if c in ct.columns]]
    fig2 = px.bar(ct, barmode="stack",
                  labels={"value": "% de contratos", col_eje: eje_sel},
                  color_discrete_map={
                      "Entregado en su totalidad": "#38a169",
                      "Entregado parcialmente": "#f6ad55",
                      "No entregado": "#e53e3e",
                  })
    fig2.update_xaxes(tickangle=30)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption(
    "Fuente de los indicadores: eda-extendido-integral/ (notebooks 01-11, ejecutados y verificados). "
    "Este tablero es unicamente una capa de visualizacion; no recalcula ni modifica ningun indicador."
)
