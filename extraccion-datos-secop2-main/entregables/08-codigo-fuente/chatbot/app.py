"""
Streamlit app — Chatbot consultor de riesgo contractual.

Ejecutar:
    cd modelo_predictivo_global/chatbot
    streamlit run app.py
"""

from __future__ import annotations
import sys
from pathlib import Path

import streamlit as st

# Asegurar que el módulo local esté en path
sys.path.insert(0, str(Path(__file__).parent))

from gemini_client import ChatBot


st.set_page_config(
    page_title="Riesgo Contractual — SECOP II",
    page_icon=":bar_chart:",
    layout="wide",
)


# ----------------------------------------------------------------------- #
# Inicialización (cacheado)                                                #
# ----------------------------------------------------------------------- #

@st.cache_resource(show_spinner="Cargando modelo LightGBM y conectando con Gemini...")
def cargar_bot() -> ChatBot:
    return ChatBot()


# ----------------------------------------------------------------------- #
# Layout                                                                   #
# ----------------------------------------------------------------------- #

st.title("Consultor de Riesgo Contractual")
st.caption(
    "Prototipo basado en el modelo predictivo LightGBM entrenado sobre 48.331 "
    "contratos de obra pública del SECOP II Colombia. Estima probabilidad de "
    "atraso y sobrecosto en contratos."
)

with st.sidebar:
    st.header("Acerca del modelo")
    st.markdown("""
**Algoritmo**: LightGBM con tuning Random Search + CV 5.

**Métricas test**:
- AUC atraso: 0,9091
- AUC sobrecosto: 0,8338
- F1 atraso: 0,8503

**Universo**: 48.331 contratos de obra pública.

**Features**: 152 variables (contrato, entidad, geografía, RUP proveedor, indicadores pliego).
    """)
    st.divider()
    st.markdown("**Limitaciones**:")
    st.markdown("""
- NO predice si la empresa será adjudicada.
- NO evalúa capacidad técnica específica.
- Probabilidades basadas en históricos similares.
    """)
    st.divider()
    if st.button("Reiniciar conversación", use_container_width=True):
        st.session_state.pop('mensajes', None)
        st.session_state.pop('bot', None)
        st.rerun()


# ----------------------------------------------------------------------- #
# Estado conversacional                                                    #
# ----------------------------------------------------------------------- #

if 'bot' not in st.session_state:
    st.session_state.bot = cargar_bot()

if 'mensajes' not in st.session_state:
    st.session_state.mensajes = [
        {
            'role': 'assistant',
            'content': (
                "Hola. Soy un asistente que analiza el riesgo histórico de "
                "contratos de obra pública en SECOP II Colombia.\n\n"
                "Cuéntame sobre la licitación que te interesa:\n"
                "- ¿En qué departamento y ciudad?\n"
                "- ¿Cuál es el valor estimado del contrato?\n"
                "- ¿Cuánto tiempo planificado de ejecución?\n"
                "- ¿Bajo qué modalidad (licitación pública, contratación directa, ...)?\n"
                "- ¿Tu empresa es pyme? ¿Participarás como consorcio?\n\n"
                "Con esos datos puedo estimar la probabilidad de atraso y sobrecosto."
            ),
        }
    ]


# ----------------------------------------------------------------------- #
# Render histórico                                                         #
# ----------------------------------------------------------------------- #

for msg in st.session_state.mensajes:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])


# ----------------------------------------------------------------------- #
# Input usuario                                                            #
# ----------------------------------------------------------------------- #

prompt = st.chat_input("Describe tu situación...")
if prompt:
    st.session_state.mensajes.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        with st.spinner("Analizando..."):
            try:
                respuesta = st.session_state.bot.send(prompt)
            except Exception as e:
                respuesta = f"**Error**: {e}"
        st.markdown(respuesta)

    st.session_state.mensajes.append({'role': 'assistant', 'content': respuesta})
