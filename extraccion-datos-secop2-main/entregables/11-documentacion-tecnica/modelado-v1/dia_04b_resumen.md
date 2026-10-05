# Día 4b — Feature Selection

**Notebook**: [`notebooks/04b_feature_selection.ipynb`](../notebooks/04b_feature_selection.ipynb)
**Fecha**: 2026-04-29

---

## Pipeline aplicado (4 métodos en cascada)

| Paso | Método | Cómo funciona | Resultado |
|------|--------|---------------|-----------|
| 1 | **VarianceThreshold** | Drop cols con var < 0.001 | Sanity check |
| 2 | **Correlation filter** | Drop pares \|corr\| > 0.95, eliminando la de menor corr al target | Quita redundancia |
| 3 | **Permutation importance** | Permuta cada col, mide caída en AUC. Drop si caída ≤ 0 | Identifica ruido |
| 4 | **RFECV** | Recursivamente elimina la peor + CV 3-fold | Confirma N óptimo |

**Selección final = intersección** entre supervivientes de Permutation y RFECV.

---

## Resultados

### Reducción

| Métrica | Antes | Después | Δ |
|---------|-------|---------|---|
| **N features** | 94 | **30** | **-64 (-68%)** |

### Comparativa de métricas (XGBoost)

| Versión | AUC | F1 | Precision | Recall | Accuracy |
|---------|-----|-----|-----------|--------|----------|
| Completo (94 cols) | 0.9015 | 0.8421 | 0.8801 | 0.8073 | 0.8169 |
| **Reducido (30 cols)** | **0.9036** | **0.8441** | **0.8808** | **0.8103** | **0.8190** |
| Δ | **+0.0021** ✅ | **+0.0020** ✅ | +0.0007 ✅ | +0.0030 ✅ | +0.0021 ✅ |

**Todas las métricas mejoraron** con menos features. Caso clásico de
"menos es más" — el modelo simplificado generaliza mejor (Occam's razor).

---

## Las 30 features finales

Categorizadas:

### Numéricas core (3)
- `valor_del_contrato`
- `duracion_planificada_dias`
- `duracion_planificada_dias_was_nan`

### Frequency-encoded de alta cardinalidad (8)
- `ciudad_freq`, `departamento_freq`, `sector_freq`
- `recursos_de_credito_freq`, `recursos_propios_freq`
- `recursos_propios_alcald_as_gobernaciones_y_resguardos_ind_genas__freq`
- `presupuesto_general_de_la_nacion_pgn_freq`, `sistema_general_de_regal_as_freq`

### Modalidad de contratación (5 OHE)
- `Contratación Directa (con ofertas)`, `Contratación directa`
- `Contratación régimen especial`, `Mínima cuantía`
- `Selección Abreviada de Menor Cuantía`

### Categóricas dummy (12)
- `condiciones_de_entrega_*` (2)
- `destino_gasto_Funcionamiento`
- `el_contrato_puede_ser_prorrogado_No`
- `entidad_centralizada_Centralizada`
- `es_pyme_No`
- `estado_bpin_No Válido`
- `g_nero_representante_legal_No Definido`
- `habilita_pago_adelantado_*` (2)
- `orden_*` (2)
- `rama_*` (2)

### Lo que NO sobrevivió (insights)

- ✗ Todas las features `pliego_*` → cobertura 2-3% NaN domina, no aportan AÚN
- ✗ Features `rup_*` → 60% NaN, ruido en mayor parte
- ✗ Features `estado_bpin` salvo `No Válido` → bajísima señal
- ✗ Muchas dummies de categorías raras (< 1% del dataset)

> **Implicación importante para el pipeline de extracción**:
> Hoy `pliego_*` no aporta. Pero la cobertura está en 2-3% (creciendo).
> Cuando llegue a 30%+ debería re-evaluarse — los features financieros
> de licitación tienen sentido teórico para predecir atrasos.

---

## Outputs

```
data/
├── X_train_reducido.parquet        (38,664 × 30)
├── X_test_reducido.parquet         (9,667 × 30)
├── features_seleccionadas.csv      (30 features con flags de cada método)
├── comparativa_feature_selection.csv
└── modelos/
    └── xgb_reducido.pkl

figuras/
├── dia_04b_permutation_importance.png   (top 25 + bottom 25)
├── dia_04b_rfecv_curve.png              (CV score vs N features)
└── dia_04b_comparativa_reduccion.png    (modelo completo vs reducido)
```

---

## Decisiones cerradas

- **Día 5 (tuning) usa dataset reducido** (`X_train_reducido.parquet`)
- Más rápido para Random Search 80 iters (30 cols vs 94)
- Mejor generalización
- Si `pliego_*` cobertura sube significativamente → reabrir feature selection

---

## Próximo (Día 5)

Random Search 80 iters × CV 5-fold sobre:
- XGBoost (con 30 cols)
- RandomForest (con 30 cols)

Espacio de búsqueda específico por modelo. Tiempo estimado: 30-60 min.
