export interface TopValue {
  valor: string;
  cantidad: number;
}

export interface SentinelValue {
  valor: string;
  cantidad: number;
}

export interface ColumnStats {
  min: number;
  max: number;
  media: number;
  mediana: number;
  std: number;
}

export interface DatasetColumn {
  columna: string;
  nombre_original: string;
  descripcion: string;
  tipo_oficial: string;
  dtype: string;
  total: number;
  no_nulos: number;
  nulos: number;
  pct_nulos: number;
  unicos: number;
  top_valores?: TopValue[];
  valores_sentinela?: SentinelValue[];
  estadisticas?: ColumnStats;
}

export interface Dataset {
  archivo: string;
  nombre: string;
  descripcion: string;
  nivel: string;
  notebook: string;
  fuente_secop: string;
  registros: number;
  num_columnas: number;
  columnas: DatasetColumn[];
}

export interface Diccionario {
  datasets: Dataset[];
}

export interface RelationEdge {
  origen: string;
  llave_origen: string;
  destino: string;
  llave_destino: string;
  cobertura: number;
}
