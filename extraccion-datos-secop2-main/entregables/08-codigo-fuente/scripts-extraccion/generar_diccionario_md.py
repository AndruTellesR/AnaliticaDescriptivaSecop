"""
Genera el diccionario de datos en formato Markdown a partir del JSON perfilado.

Entrada:  data/diccionario_datos.json
Salida:   doc/fase2_comprension_datos/diccionario_datos.md

Uso:
    python scripts/generar_diccionario_md.py
"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
INPUT = BASE / "data" / "diccionario_datos.json"
OUTPUT = BASE / "doc" / "fase2_comprension_datos" / "diccionario_datos.md"

# Definiciones para columnas derivadas del dataset integrado
DEFINICIONES_DERIVADAS = {
    "n_adicion_valor": "Cantidad de adiciones en valor monetario registradas para el contrato",
    "n_cesion": "Cantidad de cesiones (transferencia del contrato a otro contratista)",
    "n_conclusion": "Cantidad de registros de conclusión/terminación anticipada",
    "n_extension": "Cantidad de extensiones en plazo (prórrogas)",
    "n_modif_general": "Cantidad de modificaciones generales al contrato",
    "n_tipo_no_definido": "Cantidad de modificaciones sin tipo definido",
    "n_reactivacion": "Cantidad de reactivaciones del contrato",
    "n_suspension": "Cantidad de suspensiones del contrato",
    "n_modificaciones_total": "Total de modificaciones contractuales (suma de todos los tipos)",
    "n_tipos_distintos": "Cantidad de tipos distintos de modificación aplicados al contrato",
    "fecha_primera_adicion": "Fecha de la primera modificación registrada",
    "fecha_ultima_adicion": "Fecha de la última modificación registrada",
    "tiene_extension_dias": "Indicador binario: el contrato tuvo al menos una extensión de plazo",
    "tiene_adicion_valor": "Indicador binario: el contrato tuvo al menos una adición en valor",
    "tiene_suspension": "Indicador binario: el contrato tuvo al menos una suspensión",
    "tiene_cesion": "Indicador binario: el contrato tuvo al menos una cesión",
    "tiene_conclusion": "Indicador binario: el contrato tuvo al menos una conclusión anticipada",
    "tiene_reactivacion": "Indicador binario: el contrato tuvo al menos una reactivación",
    "tiene_adiciones": "Indicador binario: el contrato tiene al menos una modificación de cualquier tipo",
    "dias_hasta_primera_adicion": "Días transcurridos entre la firma del contrato y la primera modificación",
    "ratio_adiciones_duracion": "Relación entre cantidad de adiciones y duración del contrato (frecuencia de modificaciones)",
    "pct_adicion_valor": "Porcentaje de adición en valor respecto al valor original del contrato",
    "valor_total_adiciones": "Suma total de los montos de todas las adiciones en valor",
    "dias_totales_extension": "Suma total de días de extensión otorgados al contrato",
}


def fmt_num(n):
    """Formatea un numero con separador de miles."""
    if isinstance(n, float):
        if n == int(n):
            return f"{int(n):,}".replace(",", ".")
        return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{n:,}".replace(",", ".")


def generar_md():
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = []
    a = lines.append

    a("# Diccionario de datos")
    a("")
    a("## Datasets del proyecto - Modelo Predictivo SECOP II Obra Publica")
    a("")
    a("> Generado automaticamente por `scripts/generar_diccionario_datos.py`")
    a(f"> Contrastado con definiciones oficiales del SECOP en `dataset.json`")
    a("")
    a("---")
    a("")

    # Indice
    a("## Indice de datasets")
    a("")
    a("| # | Dataset | Registros | Columnas | Fuente SECOP |")
    a("|---|---|---|---|---|")
    for i, ds in enumerate(data["datasets"], 1):
        fuente = ds["fuente_secop"] or "Derivado"
        a(f"| {i} | [{ds['nombre']}](#{ds['archivo'].replace('.parquet', '').replace('_', '-')}) | {fmt_num(ds['registros'])} | {ds['num_columnas']} | {fuente} |")
    a("")
    a("---")
    a("")

    # Cada dataset
    for i, ds in enumerate(data["datasets"], 1):
        anchor = ds["archivo"].replace(".parquet", "").replace("_", "-")
        a(f"## {i}. {ds['nombre']}")
        a("")
        a(f"**Archivo**: `data/{ds['archivo']}`")
        a("")
        a(f"**Descripcion**: {ds['descripcion']}")
        a("")
        a(f"| Atributo | Valor |")
        a(f"|---|---|")
        a(f"| Granularidad | {ds['nivel']} |")
        a(f"| Registros | {fmt_num(ds['registros'])} |")
        a(f"| Columnas | {ds['num_columnas']} |")
        a(f"| Notebook/Script | `{ds['notebook']}` |")
        if ds["fuente_secop"]:
            a(f"| Fuente SECOP | `{ds['fuente_secop']}` |")
        a("")

        # Tabla de columnas
        a("### Definicion de columnas")
        a("")
        a("| # | Columna API | Nombre original | Tipo | Descripcion | No nulos | Nulos (%) | Unicos |")
        a("|---|---|---|---|---|---|---|---|")

        for j, col in enumerate(ds["columnas"], 1):
            desc = col["descripcion"]
            # Enriquecer columnas derivadas
            if "sin definici" in desc and col["columna"] in DEFINICIONES_DERIVADAS:
                desc = DEFINICIONES_DERIVADAS[col["columna"]]

            # Truncar descripcion larga
            if len(desc) > 100:
                desc = desc[:97] + "..."

            nulos_pct = f"{col['pct_nulos']}%" if col['pct_nulos'] > 0 else "0%"
            a(f"| {j} | `{col['columna']}` | {col['nombre_original']} | {col['tipo_oficial']} | {desc} | {fmt_num(col['no_nulos'])} | {fmt_num(col['nulos'])} ({nulos_pct}) | {fmt_num(col['unicos'])} |")

        a("")

        # Valores sentinela encontrados
        cols_sentinela = [c for c in ds["columnas"] if "valores_sentinela" in c]
        if cols_sentinela:
            a("### Valores sentinela detectados")
            a("")
            a("Valores que actuan como sustitutos de nulos en los datos originales del SECOP.")
            a("")
            a("| Columna | Valor sentinela | Cantidad |")
            a("|---|---|---|")
            for col in cols_sentinela:
                for s in col["valores_sentinela"]:
                    a(f"| `{col['columna']}` | `{s['valor']}` | {fmt_num(s['cantidad'])} |")
            a("")

        # Top valores para columnas categoricas importantes (max 5 columnas)
        cols_top = [c for c in ds["columnas"] if "top_valores" in c and c["unicos"] <= 30]
        if cols_top:
            a("### Distribucion de valores (categoricas con <= 30 valores unicos)")
            a("")
            for col in cols_top[:10]:  # max 10 columnas
                a(f"**`{col['columna']}`** ({col['unicos']} valores unicos)")
                a("")
                a("| Valor | Cantidad |")
                a("|---|---|")
                for tv in col["top_valores"][:10]:
                    a(f"| {tv['valor']} | {fmt_num(tv['cantidad'])} |")
                a("")

        a("---")
        a("")

    # Esquema relacional
    a("## Esquema relacional entre datasets")
    a("")
    a("```")
    a("contratos_electronicos_obra (FUENTE MADRE)")
    a("  |")
    a("  |-- proceso_de_compra = id_del_portafolio --> procesos_contratacion_obra")
    a("  |                                               |")
    a("  |                                               |-- id_del_proceso = id_procedimiento --> proponentes_por_proceso_obra")
    a("  |")
    a("  |-- id_contrato = id_contrato --> adiciones_obra")
    a("  |")
    a("  |-- codigo_proveedor = codigo --> proveedores_obra")
    a("  |")
    a("  |-- codigo_proveedor = nit --> proveedores_rup")
    a("  |")
    a("  +-- [JOIN con adiciones] --> contratos_adiciones_obra")
    a("```")
    a("")
    a("### Llaves de integracion")
    a("")
    a("| Origen | Llave origen | Destino | Llave destino | Cobertura |")
    a("|---|---|---|---|---|")
    a("| contratos_electronicos | `proceso_de_compra` | procesos_contratacion | `id_del_portafolio` | 99.9% |")
    a("| contratos_electronicos | `id_contrato` | adiciones | `id_contrato` | 69.2% |")
    a("| contratos_electronicos | `codigo_proveedor` | proveedores_registrados | `codigo` | 54.4% |")
    a("| contratos_electronicos | `codigo_proveedor` | proveedores_rup | `nit` | 63.5% (de procesados) |")
    a("| procesos_contratacion | `id_del_proceso` | proponentes_por_proceso | `id_procedimiento` | 29.4% |")
    a("")
    a("---")
    a("")
    a("## Notas metodologicas")
    a("")
    a("1. **Filtro global**: Todos los datasets estan filtrados por `tipo_de_contrato = 'Obra'`")
    a("2. **Fuente oficial**: Las descripciones de columnas provienen del diccionario oficial del SECOP publicado en datos.gov.co")
    a("3. **Columnas derivadas**: Las columnas marcadas como '(sin definicion oficial)' fueron calculadas durante la fase de comprension/integracion de datos")
    a("4. **Valores sentinela**: El SECOP usa cadenas como 'No Definido', 'No Provisto', '' en lugar de nulos reales. Estos deben tratarse como datos faltantes")
    a("5. **Dataset integrado** (`contratos_adiciones_obra`): Resultado del LEFT JOIN entre contratos y adiciones agregadas. Las 24 columnas adicionales son features derivadas del conteo y tipificacion de modificaciones contractuales")
    a("6. **Proveedores RUP**: Dataset enriquecido mediante web scraping de la API del RUP. Las columnas `rup_*` provienen de la consulta automatizada al Registro Unico de Proponentes")
    a("")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Diccionario generado: {OUTPUT}")
    print(f"  {len(data['datasets'])} datasets, {sum(d['num_columnas'] for d in data['datasets'])} columnas totales")


if __name__ == "__main__":
    generar_md()
