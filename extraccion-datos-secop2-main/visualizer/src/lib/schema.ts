import { RelationEdge } from "./types";

export const RELATIONS: RelationEdge[] = [
  {
    origen: "contratos_electronicos_obra",
    llave_origen: "proceso_de_compra",
    destino: "procesos_contratacion_obra",
    llave_destino: "id_del_portafolio",
    cobertura: 99.9,
  },
  {
    origen: "contratos_electronicos_obra",
    llave_origen: "id_contrato",
    destino: "adiciones_obra",
    llave_destino: "id_contrato",
    cobertura: 69.2,
  },
  {
    origen: "contratos_electronicos_obra",
    llave_origen: "codigo_proveedor",
    destino: "proveedores_obra",
    llave_destino: "codigo",
    cobertura: 54.4,
  },
  {
    origen: "contratos_electronicos_obra",
    llave_origen: "codigo_proveedor",
    destino: "proveedores_rup",
    llave_destino: "nit",
    cobertura: 63.5,
  },
  {
    origen: "procesos_contratacion_obra",
    llave_origen: "id_del_proceso",
    destino: "proponentes_por_proceso_obra",
    llave_destino: "id_procedimiento",
    cobertura: 29.4,
  },
];

export const DATASET_LABELS: Record<string, string> = {
  contratos_electronicos_obra: "Contratos Electrónicos",
  procesos_contratacion_obra: "Procesos Contratación",
  adiciones_obra: "Adiciones",
  proveedores_obra: "Proveedores",
  proponentes_por_proceso_obra: "Proponentes por Proceso",
  contratos_adiciones_obra: "Contratos + Adiciones",
  proveedores_rup: "Proveedores RUP",
};

export const SENTINEL_VALUES = [
  "No Definido",
  "No definido",
  "NO DEFINIDO",
  "No Defenido",
  "No Provisto",
  "Sin Descripcion",
  "No aplica",
  "No D",
  "No Valido",
  "",
  " ",
];
