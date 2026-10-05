"""
Genera el diccionario de datos de todos los parquets del proyecto.
Cruza las columnas reales con las definiciones oficiales SECOP en dataset.json.

Salida: data/diccionario_datos.json  (consumido luego para generar .md)

Uso:
    python scripts/generar_diccionario_datos.py
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path

# ── Configuracion ──────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
DATASET_JSON = BASE / "dataset.json"
OUTPUT = DATA / "diccionario_datos.json"

# Mapeo: nombre_parquet → fuente en dataset.json (None = no tiene fuente SECOP)
PARQUETS = {
    "contratos_electronicos_obra.parquet": {
        "fuente_json": "contratosElectronicos",
        "nombre": "Contratos Electrónicos — Obra",
        "descripcion": "Contratos de Obra Pública firmados electrónicamente en SECOP II. Fuente madre del proyecto: contiene variables de ejecución, estados contractuales y datos del proveedor adjudicado.",
        "nivel": "1 fila = 1 contrato firmado",
        "notebook": "01_contratos_electronicos.ipynb",
    },
    "procesos_contratacion_obra.parquet": {
        "fuente_json": "procesosDeContratacion",
        "nombre": "Procesos de Contratación — Obra",
        "descripcion": "Procesos de compra pública de Obra en SECOP II. Contiene información pre-contractual: modalidad, plazos de publicación, presupuesto estimado y cantidad de oferentes.",
        "nivel": "1 fila = 1 proceso de compra",
        "notebook": "02_procesos_contratacion.ipynb",
    },
    "adiciones_obra.parquet": {
        "fuente_json": "adiciones",
        "nombre": "Adiciones — Obra",
        "descripcion": "Modificaciones contractuales (adiciones en valor, tiempo, o ambos) registradas sobre contratos de Obra en SECOP II.",
        "nivel": "1 fila = 1 modificación contractual",
        "notebook": "03_adiciones.ipynb",
    },
    "proveedores_obra.parquet": {
        "fuente_json": "proveedoresRegistrados",
        "nombre": "Proveedores Registrados — Obra",
        "descripcion": "Proveedores registrados en SECOP II que participan en contratos de Obra. Incluye datos de registro, clasificación UNSPSC, tamaño de empresa y ubicación.",
        "nivel": "1 fila = 1 proveedor registrado",
        "notebook": "04_proveedores.ipynb",
    },
    "proponentes_por_proceso_obra.parquet": {
        "fuente_json": "proponentesporProceso",
        "nombre": "Proponentes por Proceso — Obra",
        "descripcion": "Listado de todos los proveedores que presentaron oferta en cada proceso de contratación de Obra. Permite conocer la competencia real de cada licitación.",
        "nivel": "1 fila = 1 proponente en 1 proceso",
        "notebook": "06_proponentes_por_proceso.ipynb",
    },
    "contratos_adiciones_obra.parquet": {
        "fuente_json": None,
        "fuentes_heredadas": ["contratosElectronicos", "adiciones"],
        "nombre": "Contratos + Adiciones (integrado)",
        "descripcion": "Dataset resultado del JOIN entre contratos electrónicos y adiciones. Consolida la información contractual con las modificaciones, a nivel de contrato.",
        "nivel": "1 fila = 1 contrato (con adiciones agregadas)",
        "notebook": "05_integracion_contratos_adiciones.ipynb",
    },
    "proveedores_rup.parquet": {
        "fuente_json": None,
        "nombre": "Proveedores RUP (enriquecido)",
        "descripcion": "Dataset unificado de NITs de proveedores/proponentes de Obra, enriquecido con información financiera extraída del Registro Único de Proponentes (RUP) mediante web scraping.",
        "nivel": "1 fila = 1 NIT de proveedor/proponente",
        "notebook": "06_proponentes_por_proceso.ipynb + scripts/extraer_rup_auto.py",
    },
}

# Definiciones manuales para columnas que no vienen del SECOP (datasets derivados)
DEFINICIONES_RUP = {
    "nit": {"descripcion": "NIT del proveedor/proponente (llave única, sin dígito verificador)", "tipo": "Texto"},
    "nombre_proveedor": {"descripcion": "Nombre o razón social del proveedor", "tipo": "Texto"},
    "origen": {"descripcion": "Fuente de donde se obtuvo el NIT: 'procesos', 'electronicos' o 'ambos'", "tipo": "Texto"},
    "rup_estado": {"descripcion": "Estado de la matrícula RUP (ACTIVA, CANCELADA, etc.)", "tipo": "Texto"},
    "rup_tamano": {"descripcion": "Tamaño de empresa según clasificación RUP (01=Micro, 02=Pequeña, 03=Mediana, 04=Grande)", "tipo": "Texto"},
    "rup_empleados": {"descripcion": "Número de empleados declarados ante la Cámara de Comercio", "tipo": "Número"},
    "rup_municipio": {"descripcion": "Municipio del domicilio comercial del proveedor", "tipo": "Texto"},
    "rup_sanciones": {"descripcion": "Cantidad de sanciones registradas en el RUP", "tipo": "Número"},
    "rup_multas": {"descripcion": "Cantidad de multas registradas en el RUP", "tipo": "Número"},
    "rup_inhabilidad": {"descripcion": "Inhabilidad vigente registrada en el RUP (si aplica)", "tipo": "Texto"},
    "rup_ano_financiero": {"descripcion": "Año fiscal de la información financiera reportada", "tipo": "Texto"},
    "rup_activo_total": {"descripcion": "Activo total en COP según estados financieros", "tipo": "Número"},
    "rup_patrimonio": {"descripcion": "Patrimonio neto en COP según estados financieros", "tipo": "Número"},
    "rup_ingresos": {"descripcion": "Ingresos por actividad ordinaria en COP", "tipo": "Número"},
    "rup_utilidad_neta": {"descripcion": "Resultado del período (utilidad o pérdida) en COP", "tipo": "Número"},
    "rup_idx_liquidez": {"descripcion": "Índice de liquidez: Activo Corriente / Pasivo Corriente", "tipo": "Número"},
    "rup_idx_endeudamiento": {"descripcion": "Índice de endeudamiento: Pasivo Total / Activo Total", "tipo": "Número"},
    "rup_idx_cobertura": {"descripcion": "Cobertura de intereses: Utilidad Operacional / Gastos Intereses", "tipo": "Número"},
    "rup_rent_patrimonio": {"descripcion": "Rentabilidad sobre patrimonio: Utilidad Neta / Patrimonio", "tipo": "Número"},
    "rup_rent_activo": {"descripcion": "Rentabilidad sobre activos: Utilidad Neta / Activo Total", "tipo": "Número"},
    "procesado": {"descripcion": "Indica si el NIT ya fue consultado en la API del RUP", "tipo": "Booleano"},
    "procesar": {"descripcion": "Indica si el NIT debe procesarse (False para consorcios/UT)", "tipo": "Booleano"},
}


def cargar_definiciones_secop():
    """Carga las definiciones oficiales del SECOP desde dataset.json."""
    with open(DATASET_JSON, "r", encoding="utf-8") as f:
        ds = json.load(f)

    defs = {}
    for fuente_key, fuente_data in ds["fuentes"].items():
        defs[fuente_key] = {}
        for col in fuente_data.get("columnas", []):
            api_name = col.get("nombreCampoApi", "")
            defs[fuente_key][api_name] = {
                "nombreColumna": col.get("nombreColumna", ""),
                "descripcion": col.get("descripcion", ""),
                "tipo": col.get("tipo", ""),
            }
    return defs


def perfilar_columna(serie):
    """Perfila una columna de un DataFrame."""
    total = len(serie)
    nulos = int(serie.isna().sum())
    no_nulos = total - nulos
    n_unicos = int(serie.nunique())

    perfil = {
        "dtype": str(serie.dtype),
        "total": total,
        "no_nulos": no_nulos,
        "nulos": nulos,
        "pct_nulos": round(nulos / total * 100, 1) if total > 0 else 0,
        "unicos": n_unicos,
    }

    # Valores especiales / sentinela
    sentinelas = []
    if serie.dtype == "object":
        for val in ["No Definido", "No Provisto", "No Aplica", "", " ", "nan", "None",
                     "NO DEFINIDO", "SIN DEFINIR", "No definido"]:
            count = int((serie == val).sum())
            if count > 0:
                sentinelas.append({"valor": val if val != "" else "(cadena vacía)", "cantidad": count})

    if sentinelas:
        perfil["valores_sentinela"] = sentinelas

    # Top 10 valores mas frecuentes (solo si tiene sentido)
    if 0 < n_unicos <= 50 or serie.dtype == "object":
        top = serie.dropna().value_counts().head(10)
        perfil["top_valores"] = [
            {"valor": str(v), "cantidad": int(c)}
            for v, c in top.items()
        ]
    elif serie.dtype in ("int64", "float64", "int32", "float32"):
        desc = serie.dropna().describe()
        perfil["estadisticas"] = {
            "min": float(desc.get("min", 0)),
            "max": float(desc.get("max", 0)),
            "media": round(float(desc.get("mean", 0)), 2),
            "mediana": round(float(desc.get("50%", 0)), 2),
            "std": round(float(desc.get("std", 0)), 2),
        }

    return perfil


def procesar_parquet(filename, config, defs_secop):
    """Procesa un parquet y devuelve su diccionario."""
    path = DATA / filename
    df = pd.read_parquet(path)

    fuente_key = config["fuente_json"]
    defs_fuente = defs_secop.get(fuente_key, {}) if fuente_key else {}

    # Para datasets derivados, buscar en fuentes heredadas
    if not defs_fuente and "fuentes_heredadas" in config:
        for fk in config["fuentes_heredadas"]:
            defs_fuente.update(defs_secop.get(fk, {}))

    columnas = []
    for col in df.columns:
        perfil = perfilar_columna(df[col])

        # Buscar definicion oficial
        if col in defs_fuente:
            oficial = defs_fuente[col]
            definicion = {
                "columna": col,
                "nombre_original": oficial["nombreColumna"],
                "descripcion": oficial["descripcion"],
                "tipo_oficial": oficial["tipo"],
            }
        elif col in DEFINICIONES_RUP:
            manual = DEFINICIONES_RUP[col]
            definicion = {
                "columna": col,
                "nombre_original": col,
                "descripcion": manual["descripcion"],
                "tipo_oficial": manual["tipo"],
            }
        else:
            definicion = {
                "columna": col,
                "nombre_original": col,
                "descripcion": "(sin definición oficial — columna derivada o calculada)",
                "tipo_oficial": str(df[col].dtype),
            }

        definicion.update(perfil)
        columnas.append(definicion)

    return {
        "archivo": filename,
        "nombre": config["nombre"],
        "descripcion": config["descripcion"],
        "nivel": config["nivel"],
        "notebook": config["notebook"],
        "fuente_secop": fuente_key,
        "registros": len(df),
        "num_columnas": len(df.columns),
        "columnas": columnas,
    }


def main():
    print("Cargando definiciones SECOP...")
    defs_secop = cargar_definiciones_secop()

    diccionario = {"datasets": []}

    for filename, config in PARQUETS.items():
        path = DATA / filename
        if not path.exists():
            print(f"  SKIP {filename} (no existe)")
            continue
        print(f"  Perfilando {filename}...")
        info = procesar_parquet(filename, config, defs_secop)
        diccionario["datasets"].append(info)
        print(f"    {info['registros']:,} registros, {info['num_columnas']} columnas")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=2)

    print(f"\nDiccionario guardado en {OUTPUT}")
    print(f"Total: {len(diccionario['datasets'])} datasets")


if __name__ == "__main__":
    main()
