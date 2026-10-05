# Prompt maestro — App de visualizacion de datos SECOP II

> Copia y pega este prompt completo en una nueva sesion de Claude Code para que construya la app.

---

## PROMPT

Necesito que construyas una aplicacion web **sin backend** (solo frontend) para visualizar los datasets de mi proyecto de investigacion sobre contratacion publica en Colombia (SECOP II - Obra Publica).

### Objetivo

Una herramienta visual, moderna y bonita para explorar los 7 datasets del proyecto junto a mi director de trabajo de grado. Debe permitir:

1. Ver el **catalogo de datasets** con su descripcion, registros, columnas y relaciones
2. Explorar la **definicion de cada dataset**: tabla de columnas con nombre, tipo, descripcion oficial SECOP, % nulos, valores unicos
3. Ver **valores sentinela** detectados por dataset
4. Visualizar el **esquema relacional** entre datasets (diagrama interactivo)
5. **Previsualizar datos**: cargar un parquet y ver las primeras N filas en tabla paginada con filtros
6. Ver **estadisticas basicas** por columna: distribucion, top valores, nulos, histogramas para numericas

### Stack tecnologico

- **React** con Vite (o Next.js static export)
- **TailwindCSS** para estilos — tema oscuro como default, toggle a claro
- **Shadcn/ui** o similar para componentes (tablas, tabs, cards, badges)
- **Recharts** o **Nivo** para graficos (histogramas, barras, donut)
- **DuckDB-WASM** o **Arquero** para leer parquets directamente en el navegador (sin backend)
- **React Flow** o **Mermaid** para el diagrama relacional
- Desplegable como static site (Vercel, GitHub Pages, o simplemente `npm run build`)

### Fuentes de datos

Los datos vienen de 2 fuentes que la app debe consumir:

#### 1. Diccionario de datos (JSON) — metadatos
Archivo: `data/diccionario_datos.json`

Estructura:
```json
{
  "datasets": [
    {
      "archivo": "contratos_electronicos_obra.parquet",
      "nombre": "Contratos Electrónicos — Obra",
      "descripcion": "Contratos de Obra Pública firmados electrónicamente...",
      "nivel": "1 fila = 1 contrato firmado",
      "notebook": "01_contratos_electronicos.ipynb",
      "fuente_secop": "contratosElectronicos",
      "registros": 51353,
      "num_columnas": 87,
      "columnas": [
        {
          "columna": "nombre_entidad",
          "nombre_original": "Nombre Entidad",
          "descripcion": "Nombre de la entidad del estado que publica el contrato",
          "tipo_oficial": "Texto",
          "dtype": "str",
          "total": 51353,
          "no_nulos": 51353,
          "nulos": 0,
          "pct_nulos": 0.0,
          "unicos": 2528,
          "top_valores": [{"valor": "...", "cantidad": 1234}],
          "valores_sentinela": [{"valor": "No Definido", "cantidad": 567}],
          "estadisticas": {"min": 0, "max": 100, "media": 50, "mediana": 48, "std": 15}
        }
      ]
    }
  ]
}
```

Campos opcionales por columna: `top_valores`, `valores_sentinela`, `estadisticas` (solo numericas con >50 unicos).

#### 2. Archivos Parquet — datos crudos
Directorio: `data/`

| Archivo | Registros | Columnas | Tamano |
|---------|-----------|----------|--------|
| contratos_electronicos_obra.parquet | 51,353 | 87 | 16 MB |
| procesos_contratacion_obra.parquet | 138,112 | 57 | 34 MB |
| adiciones_obra.parquet | 249,037 | 5 | 12 MB |
| proveedores_obra.parquet | 13,117 | 25 | 1.8 MB |
| proponentes_por_proceso_obra.parquet | 276,770 | 9 | 9.6 MB |
| contratos_adiciones_obra.parquet | 48,331 | 111 | 17 MB |
| proveedores_rup.parquet | 28,548 | 22 | 1.6 MB |

Los parquets deben leerse **en el navegador** con DuckDB-WASM o similar. Si el archivo es muy grande, paginar la carga.

### Esquema relacional (hardcoded en la app)

```
contratos_electronicos_obra (FUENTE MADRE)
  |
  |-- proceso_de_compra = id_del_portafolio --> procesos_contratacion_obra
  |                                               |
  |                                               |-- id_del_proceso = id_procedimiento --> proponentes_por_proceso_obra
  |
  |-- id_contrato = id_contrato --> adiciones_obra
  |
  |-- codigo_proveedor = codigo --> proveedores_obra
  |
  |-- codigo_proveedor = nit --> proveedores_rup
  |
  +-- [JOIN con adiciones] --> contratos_adiciones_obra (derivado)
```

Llaves y coberturas:

| Origen | Llave origen | Destino | Llave destino | Cobertura |
|--------|-------------|---------|---------------|-----------|
| contratos_electronicos | proceso_de_compra | procesos_contratacion | id_del_portafolio | 99.9% |
| contratos_electronicos | id_contrato | adiciones | id_contrato | 69.2% |
| contratos_electronicos | codigo_proveedor | proveedores | codigo | 54.4% |
| contratos_electronicos | codigo_proveedor | proveedores_rup | nit | 63.5% |
| procesos_contratacion | id_del_proceso | proponentes_por_proceso | id_procedimiento | 29.4% |

### Diseno de la app — Paginas/Vistas

#### Vista 1: Dashboard / Catalogo
- Cards para cada dataset con: nombre, icono, registros, columnas, fuente SECOP, descripcion corta
- Resumen general: total registros, total columnas, total datasets
- Click en una card lleva a la Vista 2

#### Vista 2: Detalle del dataset
- Header con nombre, descripcion completa, nivel de granularidad, notebook de origen
- **Tab 1 — Columnas**: Tabla con todas las columnas del dataset. Columnas de la tabla: #, Nombre API, Nombre original, Tipo oficial, Descripcion, No nulos, Nulos (%), Unicos. Debe ser ordenable y filtrable con un buscador.
- **Tab 2 — Calidad**: Valores sentinela detectados (tabla), columnas con >10% nulos (barra horizontal), distribucion de tipos de dato (donut)
- **Tab 3 — Distribuciones**: Para columnas categoricas con <=30 valores unicos, mostrar barras horizontales con top valores. Para numericas, mostrar las estadisticas (min, max, media, mediana, std) en cards.
- **Tab 4 — Preview**: Cargar el parquet con DuckDB-WASM, mostrar las primeras 100 filas en tabla paginada (10 por pagina). Incluir buscador de texto sobre la tabla. Boton para cargar mas filas.

#### Vista 3: Esquema relacional
- Diagrama interactivo (React Flow preferiblemente) mostrando los 7 datasets como nodos
- Las aristas muestran la llave de JOIN y el % de cobertura
- Colores: verde para >90%, amarillo para 50-90%, rojo para <50%
- `contratos_electronicos_obra` como nodo central/destacado (es la fuente madre)
- Click en un nodo lleva a la Vista 2 de ese dataset

#### Vista 4: Valores sentinela (global)
- Tabla consolidada de todos los sentinelas encontrados en todos los datasets
- Columnas: Dataset, Columna, Valor sentinela, Cantidad, % del total
- Filtrable por dataset

### Valores sentinela conocidos

La app debe resaltar estos como "pseudo-nulos":

```
"No Definido", "No definido", "NO DEFINIDO",
"No Defenido",  // error ortografico en procesos
"No Provisto",
"Sin Descripcion",
"No aplica",
"No D",
"No Valido",
"", " "
```

### Requisitos de UX

- **Tema oscuro** por defecto (fondo #0f172a o similar slate-900), con toggle a claro
- **Responsive** pero optimizado para desktop (se usara en reuniones con pantalla grande)
- **Navegacion**: sidebar fija con links a las 4 vistas + logo/titulo del proyecto
- **Breadcrumbs** en la vista de detalle
- **Numeros formateados** con separador de miles (formato colombiano: 51.353, no 51,353)
- **Badges de color** para tipos de dato: Texto=azul, Numero=verde, Fecha=naranja, Booleano=morado
- **Indicador de cobertura** con progress bars coloreadas (verde >80%, amarillo 50-80%, rojo <50%)
- Transiciones suaves entre vistas
- Titulo del proyecto: "SECOP II — Modelo Predictivo Obra Publica"

### Estructura del proyecto

```
app-visualizacion/
  public/
    data/
      diccionario_datos.json          ← copiar desde data/
      contratos_electronicos_obra.parquet  ← copiar desde data/
      procesos_contratacion_obra.parquet
      adiciones_obra.parquet
      proveedores_obra.parquet
      proponentes_por_proceso_obra.parquet
      contratos_adiciones_obra.parquet
      proveedores_rup.parquet
  src/
    components/
    pages/
    hooks/
    lib/
    App.tsx
    main.tsx
  package.json
  vite.config.ts
  tailwind.config.ts
```

### Instrucciones de ejecucion

Al terminar, dame los comandos para:
1. Instalar dependencias
2. Copiar los archivos de datos al directorio correcto
3. Ejecutar en modo desarrollo
4. Hacer build para produccion

### Notas importantes

- **NO necesita backend**. Todo se ejecuta en el navegador.
- Los parquets se leen con DuckDB-WASM (o Arquero/Apache Arrow JS). No convertir a JSON.
- El `diccionario_datos.json` ya tiene toda la metadata pre-calculada; la app solo lo renderiza.
- Los parquets solo se cargan bajo demanda (cuando el usuario entra a la pestaña "Preview").
- Si un parquet es muy grande (>100K filas), paginar con `LIMIT/OFFSET` en DuckDB.
- El idioma de la interfaz es **espanol**.
- No inventar datos. Todo viene del JSON o de los parquets.
