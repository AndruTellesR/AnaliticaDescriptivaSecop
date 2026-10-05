# Chatbot Consultor de Riesgo Contractual — Prototipo v1

Asistente conversacional que estima el riesgo de **atraso** y **sobrecosto**
de un contrato de obra pública en Colombia (SECOP II), usando el modelo
LightGBM ganador del modelo predictivo global v2.

## Arquitectura

```
Usuario (texto libre)
   ↓
Gemini 2.5 Flash (LLM)
   ↓ function_call("predecir_riesgo", {features})
Predictor (Python)
   ├─ Winsorización (winsor_limits.pkl)
   ├─ OHE + Frequency Encoding (freq_maps.pkl)
   ├─ Imputación mediana + flags _was_nan (imputer_mediana.pkl)
   ├─ LightGBM atraso (lgbm.pkl)
   ├─ LightGBM sobrecosto (lgbm_sobrecosto.pkl, entrenado on-the-fly)
   └─ SHAP top-3 factores
   ↓
Gemini humaniza respuesta
   ↓
Usuario (texto + tabla + recomendaciones)
```

## Estructura

```
chatbot/
├── README.md           ← este archivo
├── requirements.txt    ← deps Python
├── .env.example        ← plantilla (la real va en proyecto raíz)
├── predictor.py        ← wrapper modelo + pipeline preprocesamiento
├── prompts.py          ← system prompt + schema de la tool
├── gemini_client.py    ← cliente Gemini + bucle function calling + CLI
└── app.py              ← interfaz Streamlit
```

## Pre-requisitos

1. Modelo y artifacts del modelo_predictivo_global v2 entrenados:
   - `../data/modelos/lgbm.pkl`
   - `../data/imputers/freq_maps.pkl`
   - `../data/imputers/imputer_mediana.pkl`
   - `../data/imputers/winsor_limits.pkl`
   - `../data/consolidado_imputado.parquet` (para reconstrucción schema)

2. `.env` en la raíz del proyecto (`extraccion-datos/.env`) con:
   ```
   GEMINI_API_KEY=tu-api-key
   ```

3. Dependencias instaladas en el `.venv` del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

## Modos de ejecución

### A) Consola (CLI)

```bash
cd modelo_predictivo_global/chatbot
python gemini_client.py
```

Conversación bidireccional. Escribe `salir` para terminar.

### B) Web (Streamlit)

```bash
cd modelo_predictivo_global/chatbot
streamlit run app.py
```

Abre `http://localhost:8501`. Interfaz con histórico de chat persistente
en sesión, sidebar con info del modelo, botón de reset.

## Ejemplo de conversación

> **Usuario**: Hola. Soy una microempresa de construcción en Bogotá.
> Quiero participar en una licitación pública de obra para una vía urbana
> por 2 mil millones COP con duración de 12 meses. Soy pyme y no me
> asocio con otros. ¿Qué riesgo tengo?

> **Bot**:
> Análisis del contrato propuesto:
> - **Probabilidad de atraso**: 12,18 %
> - **Probabilidad de sobrecosto**: 50,90 %
>
> **Factores principales (atraso)**:
> 1. Duración planificada 360 días → reduce riesgo
> 2. ...
>
> **Recomendaciones**: ...
>
> **Limitaciones**: el modelo no predice adjudicación...

## Cómo funciona el predictor

`predictor.py` replica exactamente el pipeline del `notebook 02`:

1. Normaliza input: completa NaN para features no provistas.
2. Winsorización p1/p99 con `winsor_limits.pkl`.
3. Encoding:
   - OHE para categóricas con cardinalidad < 20.
   - Frequency Encoding con `freq_maps.pkl` para alta cardinalidad.
   - Categorías no vistas → frecuencia 0.
4. Genera flags `_was_nan` por feature numérica con NaN.
5. Imputa con `imputer_mediana.pkl`.
6. Alinea exactamente con las 152 cols esperadas por el modelo
   (cols extra se eliminan, cols faltantes → 0).
7. Sanitiza nombres de columnas (LightGBM no acepta caracteres especiales).
8. Devuelve probabilidad + SHAP top-3.

## Limitaciones conocidas

1. **Calibración**: las probabilidades no han pasado por Platt scaling
   ni isotonic regression. Pueden estar sesgadas en extremos.
2. **Categorías no vistas**: si el usuario nombra un departamento/ciudad
   no presente en el train, se trata como categoría desconocida (freq 0).
3. **Sobrecosto entrenado on-the-fly**: el primer arranque tarda ~30 s
   en entrenar el modelo de sobrecosto (se cachea en
   `data/modelos/lgbm_sobrecosto.pkl`).
4. **SHAP TreeExplainer con LightGBM binario** emite un warning sobre el
   formato de salida. La lógica del wrapper maneja ambos formatos.
5. **No persiste conversaciones entre sesiones**: el histórico vive en
   `st.session_state` (Streamlit) o solo en RAM (CLI).

## Próximos pasos

- Threshold tuning + calibración Platt/isotonic (Fase 5 CRISP-DM).
- Persistencia conversaciones (SQLite o similar).
- Validación con datos reales de empresas piloto.
- Integración con SECOP II API para autocompletar features del contrato
  a partir del ID del proceso (CO1.BDOS.*).
