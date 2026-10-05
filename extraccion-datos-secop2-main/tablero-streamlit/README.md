# Tablero interactivo — Analitica descriptiva de contratacion de obra publica (SECOP II)

Objetivo especifico que atiende: **OE-04** del anteproyecto (`InformesRev/AnteproyectoAndres.md`,
numeral 1.4.2, RF-05): "Disenar visualizaciones y tableros interactivos que presenten resultados
(distribuciones, outliers con box plots, segmentaciones por modalidad/entidad/territorio) para
apoyar la interpretacion, la transparencia y la toma de decisiones."

## Alcance de este tablero

- **Universo:** 48.331 contratos de obra publica (lectura `universo_completo`, instruccion del
  tutor de usar el total de datos disponibles). No incluye el subconjunto `observable` (19.194)
  ni contraste de hipotesis (H1-H3): esta version cubre unicamente lo minimo exigido por OE-04.
- **No recalcula nada.** Los indicadores (deslizamiento del plazo, desviacion de costo, indice de
  alcance) ya fueron calculados y verificados en `eda-extendido-integral/` (notebooks 01 y 03).
  Este tablero solo lee `data/universo_completo.parquet` (copia de las columnas necesarias de
  `eda-extendido-integral/data/universo_extendido.parquet`) y los visualiza.

## Contenido

- **Distribuciones:** histogramas de deslizamiento del plazo, desviacion de costo, valor del
  contrato (log10) e indice de cumplimiento de alcance.
- **Outliers (box plots):** box plots de los indicadores continuos, winsorizados en P1-P99
  unicamente para la visualizacion (el dato original no se modifica).
- **Segmentaciones:** por modalidad de contratacion, tipo de contratista, sector, orden y
  departamento, con selector de indicador y filtros dinamicos en la barra lateral.

## Como ejecutarlo

```bash
cd tablero-streamlit
pip install -r requirements.txt
streamlit run app.py
```

Se abre en `http://localhost:8501`. No requiere conexion a internet ni credenciales: todo el dato
esta persistido localmente en `data/universo_completo.parquet`.

## Limitaciones declaradas

- No incluye mapas coropleticos (fuera del alcance minimo acordado para esta version).
- No incluye los resultados de H1, H2, H3 ni el hallazgo de `precio_base`/sobrecosto — esos quedan
  documentados en `eda-extendido-integral/EVALUACION_ASESOR.md` y en el capitulo de resultados de
  la tesis, no en este tablero.
- Este tablero corre localmente; no esta desplegado en ningun servicio en linea.
