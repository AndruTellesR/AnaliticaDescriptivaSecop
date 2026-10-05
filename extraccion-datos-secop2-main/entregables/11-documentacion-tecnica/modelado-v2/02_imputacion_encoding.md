# Documento 02 — Preprocesamiento (winsorización, encoding, imputación)

**Notebook**: `notebooks/02_preprocesamiento.ipynb`
**Inputs**: `data/consolidado_global.parquet` (48.331 × 55)
**Outputs**:

| Archivo | Descripción |
|---------|-------------|
| `data/consolidado_imputado.parquet` | 48.331 × 154 features + 2 targets |
| `data/imputers/winsor_limits.pkl` | Límites p1/p99 por columna |
| `data/imputers/freq_maps.pkl` | Mapas de Frequency Encoding |
| `data/imputers/imputer_mediana.pkl` | SimpleImputer ajustado |

## 1. Winsorización p1/p99

### ¿Por qué?

Los outliers extremos (valores absurdos por errores de extracción o
reporte) inflan rangos y desestabilizan tanto los imputadores
posteriores como los algoritmos sensibles a escala (LR, KNN, SVM, MLP).

Ejemplo de outliers detectados:
- `rup_activo_total`: max ~10¹³ (errores de coma decimal)
- `n_proponentes_por_proceso`: max 118 (atípico)
- Algunos valores históricos con magnitudes absurdas

### ¿Cómo?

Para cada columna numérica con > 3 valores únicos:

```python
p1  = X[col].quantile(0.01)
p99 = X[col].quantile(0.99)
X[col] = X[col].clip(lower=p1, upper=p99)
```

Se preservan los binarios y muy discretos (≤ 3 únicos) sin tocar.

Persistido en `imputers/winsor_limits.pkl` para reaplicar en inferencia.

### Justificación de p1/p99 (no p5/p95)

- p5/p95 recorta demasiada masa (10 % del dataset → pérdida de
  variabilidad útil).
- p1/p99 recorta solo extremos genuinos (~2 % de la masa) preservando
  la distribución central.

## 2. Encoding de variables categóricas

### Umbral cardinalidad = 20

Decisión técnica:

| Cardinalidad | Estrategia | Razón |
|--------------|------------|-------|
| < 20 | One-Hot Encoding | Genera columnas manejables, sin orden artificial |
| ≥ 20 | Frequency Encoding | Evita explosión dimensional; preserva info de prevalencia |

### Tratamiento de NaN en categóricas

Antes del OHE se reemplazan los NaN por la categoría `'desconocido'`.
Esto preserva las filas y permite que el modelo aprenda si "no tener
dato" es informativo (similar a la lógica de `_was_nan` para numéricas).

### Frequency Encoding

```python
for c in cols_freq:
    fmap = X[c].value_counts(normalize=True).to_dict()
    X_freq[c + '_freq'] = X[c].map(fmap).fillna(0.0)
```

Valores no vistos en train → frecuencia 0 (señal de "categoría
desconocida").

`freq_maps.pkl` se persiste para reaplicar exactamente en inferencia,
evitando recalcular y producir scores distintos.

### Resultado del encoding

| Tipo | Cols entrada | Cols salida |
|------|--------------|-------------|
| OHE | ~22 | ~125 dummies |
| Frequency | ~6 | 6 cols `_freq` |
| Numéricas | ~12 | 12 (sin cambio) |

Total intermedio: ~143 columnas antes de imputación.

## 3. Imputación con mediana + flag `_was_nan`

### Estrategia

Para cada columna numérica con NaN:

```python
# 1. Crear flag binario
flags[col + '_was_nan'] = X[col].isna().astype(int)

# 2. Imputar con mediana
X[col] = X[col].fillna(X[col].median())
```

El flag se concatena como columna adicional al dataset, NO reemplaza
la columna original.

### Justificación

Comparativa cuantitativa realizada en sub-sprint consorcios:

| Estrategia | AUC downstream | Tiempo | Conclusión |
|------------|---------------|--------|------------|
| **mediana + flag** | **0,8542** | 0,02 s | Gana en AUC y tiempo |
| KNN (k=5) | 0,8093 | 6,09 s | −0,045 AUC |
| MICE-Bayesian Ridge | 0,8066 | 44,32 s | −0,048 AUC |
| MICE-Random Forest | 0,8015 | 33,65 s | −0,053 AUC |

**Hallazgo central**: el flag `_was_nan` aporta más señal que un valor
imputado más sofisticado. El **patrón de ausencia** codifica info
implícita del proceso (qué modalidades, qué entidades, qué formatos
documentales permiten extraer el dato).

Los métodos avanzados borran ese patrón al "tapar el hueco" con un
valor plausible.

### Cols con `_was_nan` generadas en v2

9 columnas:
- `rup_idx_endeudamiento_was_nan`, `rup_idx_liquidez_was_nan`,
  `rup_ingresos_was_nan`, `rup_utilidad_neta_was_nan`, `rup_multas_was_nan`
- `rup_empleados_was_nan`, `rup_activo_total_was_nan`,
  `rup_patrimonio_was_nan`
- `n_proponentes_por_proceso_was_nan`

(Las cols `rup_tamano`, `rup_sanciones`, `rup_inhabilidad` son
categóricas y su NaN se trata como categoría `desconocido` en el OHE,
no como flag binario.)

## 4. Resultado final

```
Filas:                   48.331
Features finales:        152
Targets:                 2
NaN restantes:           0
Cols winsorizadas:       ~9 numéricas continuas
OHE generadas:           ~125 dummies
Freq generadas:          6 features _freq
Flags _was_nan:          9 binarios
```

`consolidado_imputado.parquet` queda listo para alimentar los 8
notebooks del zoológico (04–11).

## 5. Trazabilidad para inferencia

Para predecir sobre datos nuevos hay que aplicar **exactamente las
mismas transformaciones** ajustadas en train:

```python
import joblib
winsor = joblib.load('imputers/winsor_limits.pkl')
freq   = joblib.load('imputers/freq_maps.pkl')
imp    = joblib.load('imputers/imputer_mediana.pkl')

# 1. Winsorizar
for c, (p1, p99) in winsor.items():
    X_new[c] = X_new[c].clip(p1, p99)
# 2. Categóricas: rellenar NaN, OHE (mismas columnas que train)
# 3. Frequency: mapear; sin match → 0
# 4. Crear flags _was_nan
# 5. Imputar con mediana
```

Este orden NO puede alterarse.

## 6. Diferencia clave con v1

v1 usó:
- 53 cols dataset depurado
- 94 features tras encoding
- Imputación mediana + flag pero con menos cols con NaN

v2 usa:
- 55 cols dataset enriquecido (+20 estructurales)
- 152 features tras encoding (+58 dummies + 9 nuevos flags)
- Misma estrategia validada

El crecimiento de features (94 → 152) viene principalmente del
encoding de `codigo_de_categoria_principal_freq`, `localizaci_n_freq`
y de los OHE de variables nuevas como `nacionalidad_representante_legal`,
`pilares_del_acuerdo`.
