# 04 — Datasets en formato Apache Parquet

Esta carpeta contiene los diez datasets centrales del proyecto. El formato
Apache Parquet se eligió por su eficiencia en compresión, preservación de
tipos de datos y compatibilidad nativa con `pandas`.

## Contenido

### Datasets crudos (extracción directa del SECOP)

| Archivo | Filas | Columnas | Descripción |
|---------|-------|----------|-------------|
| `contratos_electronicos_obra.parquet` | 51.353 | 87 | Fuente madre del proyecto. Ciclo de vida completo del contrato firmado |
| `procesos_contratacion_obra.parquet` | 138.112 | 59 | Pre-contrato: el proceso de compra antes de la firma |
| `adiciones_obra.parquet` | 249.037 | 5 | Modificaciones contractuales (adiciones, prórrogas, suspensiones) |
| `proveedores_obra.parquet` | 13.117 | 25 | Perfil del proveedor: tipo, tamaño, ubicación, antigüedad |
| `proveedores_rup.parquet` | 28.548 | 22 | Información financiera del Registro Único de Proponentes |
| `proponentes_por_proceso_obra.parquet` | 276.770 | 9 | Oferentes que se presentaron a cada proceso |

### Datasets integrados y depurados

| Archivo | Filas | Columnas | Descripción |
|---------|-------|----------|-------------|
| `contratos_adiciones_obra.parquet` | 48.331 | 125 | Integración primaria de contratos con sus modificaciones |
| `contratos_depurado_modelo.parquet` | 48.331 | 53 | Dataset depurado v1 (sprint principal) |
| `consolidado_global.parquet` | 48.331 | 55 | Dataset enriquecido v2 con variables estructurales |
| `consolidado_imputado.parquet` | 48.331 | 154 | Dataset codificado e imputado listo para modelado |

## Cómo cargar

```python
import pandas as pd
df = pd.read_parquet("consolidado_imputado.parquet")
print(df.shape)
# (48331, 154)
```

## Esquema relacional entre las fuentes crudas

```
procesosDeContratacion (id_del_portafolio)  →  contratosElectronicos (proceso_de_compra)
                                                        │ id_contrato
                                                        ↓
                                              adiciones (id_contrato)
                                                        │ codigo_proveedor
                                                        ↓
                                              proveedoresRegistrados (codigo) ─ nit ─→ proveedoresRUP (nit)

procesosDeContratacion (id_del_proceso) →  proponentesPorProceso (id_procedimiento)
```

Cobertura observada en los joins:

- Procesos → Contratos: 99.9 %
- Adiciones → Contratos: 69.2 %
- Proveedores → Contratos: 54.4 %
- RUP → Proveedores: 63.5 %
- Proponentes → Procesos de Obra: 48.2 %

## Variables objetivo del modelado

Los dos targets del modelo final se construyen a partir de variables internas
del dataset depurado:

```python
tuvo_atraso     = (tiempo == 1).astype(int)        # prevalencia 60.48 %
tuvo_sobrecosto = (presupuesto == 1).astype(int)   # prevalencia 83.41 %
```

## Variables leakage prohibidas

Catorce variables fueron excluidas del set de predictores por riesgo de fuga
de información temporal. La lista completa está en
`../02-anexos/ANEXO-A-fuentes-y-variables.md`.

## Tamaño y peso de los archivos

El tamaño total de los diez datasets es de aproximadamente 97 MB. El más
pesado es `procesos_contratacion_obra.parquet` (34 MB), seguido de
`contratos_adiciones_obra.parquet` (17 MB).
