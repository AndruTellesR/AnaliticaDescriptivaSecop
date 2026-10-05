# 01 — Reestructuración en modelo dimensional simplificado


## Resultado

Se separaron 125 columnas del dataset integrado en 1 tabla de hechos (grano contrato, 48.331 filas, 20 columnas) y 5 tablas de dimensión:

| Tabla | Grano | Filas |
|---|---|---|
| `hechos_contratos` | 1 fila = 1 contrato de obra pública único | 48.331 |
| `dim_proceso` | 1 fila = 1 proceso de compra | 43.451 |
| `dim_proveedor` | 1 fila = 1 proveedor único | 23.192 |
| `dim_entidad` | 1 fila = 1 entidad contratante única | 2.534 |
| `dim_territorio` | 1 fila = 1 combinación única departamento-ciudad-orden | 848 |
| `dim_modalidad` | 1 fila = 1 modalidad de contratación única | 9 |

Integridad referencial verificada al 100% en las cinco relaciones. Se derivó de forma independiente la variable `tipo_contratista` (Persona Jurídica: 11.254, Consorcio/UT: 9.378, Persona Natural: 2.461, No definido: 99), a partir de `es_grupo` y `tipodocproveedor`.

## Limitación declarada

Modelo dimensional simplificado sobre archivos Parquet, no motor relacional formal (PostgreSQL/DuckDB/SQLite). Las relaciones se sostienen por convención documentada y verificación programática, no por restricciones `FOREIGN KEY` de un motor real.

## Artefactos generados

- `analitica-descriptiva-andres/data/modelo_dimensional/*.parquet` (6 archivos)
- Diagrama Mermaid del esquema (dentro del notebook)
- Diccionario de convenciones (dentro del notebook)
