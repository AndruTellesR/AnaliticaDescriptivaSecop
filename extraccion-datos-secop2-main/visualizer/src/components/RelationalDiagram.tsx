"use client";

import { useCallback, useMemo, useState } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  Node,
  Edge,
  MarkerType,
  BackgroundVariant,
  useNodesState,
  useEdgesState,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useRouter } from "next/navigation";
import { RELATIONS } from "@/lib/schema";
import { Dataset } from "@/lib/types";
import { formatNumber } from "@/lib/format";

interface Props {
  datasets: Dataset[];
}

const NODE_POSITIONS: Record<string, { x: number; y: number }> = {
  contratos_electronicos_obra: { x: 420, y: 280 },
  procesos_contratacion_obra: { x: 120, y: 50 },
  proponentes_por_proceso_obra: { x: -200, y: 50 },
  adiciones_obra: { x: 780, y: 50 },
  proveedores_obra: { x: 80, y: 530 },
  proveedores_rup: { x: 780, y: 530 },
  contratos_adiciones_obra: { x: 420, y: 560 },
};

function getEdgeColor(cobertura: number): string {
  if (cobertura >= 90) return "#10b981";
  if (cobertura >= 50) return "#f59e0b";
  return "#ef4444";
}

function buildInitialNodes(datasets: Dataset[]): Node[] {
  return datasets.map((ds) => {
    const slug = ds.archivo.replace(".parquet", "");
    const isMadre = slug === "contratos_electronicos_obra";
    const isDerived = slug === "contratos_adiciones_obra";
    return {
      id: slug,
      position: NODE_POSITIONS[slug] || { x: 400, y: 400 },
      draggable: true,
      data: {
        label: (
          <div className="text-center px-1">
            <div
              className={`text-sm font-semibold ${isMadre ? "text-blue-400" : "text-slate-200"}`}
            >
              {ds.nombre}
            </div>
            <div className="text-[11px] text-slate-400 mt-1">
              {formatNumber(ds.registros)} registros · {ds.num_columnas}{" "}
              cols
            </div>
            {isMadre && (
              <div className="text-[10px] text-blue-400 font-medium mt-1 uppercase tracking-wider">
                Fuente Madre
              </div>
            )}
            {isDerived && (
              <div className="text-[10px] text-slate-500 font-medium mt-1 uppercase tracking-wider">
                Derivado
              </div>
            )}
          </div>
        ),
      },
      style: {
        background: isMadre
          ? "rgba(30, 58, 138, 0.5)"
          : "rgba(30, 41, 59, 0.8)",
        border: isMadre
          ? "2px solid #3b82f6"
          : isDerived
            ? "1px dashed #475569"
            : "1px solid #334155",
        borderRadius: "12px",
        padding: "12px 16px",
        width: 220,
        cursor: "grab",
        boxShadow: isMadre ? "0 0 20px rgba(59, 130, 246, 0.15)" : "none",
      },
    };
  });
}

function buildEdges(): Edge[] {
  const relationEdges: Edge[] = RELATIONS.map((rel, i) => ({
    id: `e-${i}`,
    source: rel.origen,
    target: rel.destino,
    label: `${rel.llave_origen} → ${rel.llave_destino}\n${rel.cobertura}%`,
    style: {
      stroke: getEdgeColor(rel.cobertura),
      strokeWidth: 2,
    },
    labelStyle: {
      fontSize: 10,
      fill: "#94a3b8",
      fontFamily: "monospace",
    },
    labelBgStyle: {
      fill: "#0f172a",
      fillOpacity: 0.9,
    },
    labelBgPadding: [6, 4] as [number, number],
    labelBgBorderRadius: 4,
    markerEnd: {
      type: MarkerType.ArrowClosed,
      color: getEdgeColor(rel.cobertura),
      width: 16,
      height: 16,
    },
    animated: rel.cobertura >= 90,
  }));

  relationEdges.push({
    id: "e-derived",
    source: "contratos_electronicos_obra",
    target: "contratos_adiciones_obra",
    label: "JOIN derivado",
    style: {
      stroke: "#475569",
      strokeWidth: 1,
      strokeDasharray: "5,5",
    },
    labelStyle: {
      fontSize: 10,
      fill: "#64748b",
      fontStyle: "italic",
    },
    labelBgStyle: {
      fill: "#0f172a",
      fillOpacity: 0.9,
    },
    labelBgPadding: [6, 4] as [number, number],
    labelBgBorderRadius: 4,
  });

  return relationEdges;
}

export default function RelationalDiagram({ datasets }: Props) {
  const router = useRouter();
  const [nodes, setNodes, onNodesChange] = useNodesState(
    buildInitialNodes(datasets)
  );
  const [edges, setEdges, onEdgesChange] = useEdgesState(buildEdges());
  const [dragging, setDragging] = useState(false);

  const onNodeDragStart = useCallback(() => {
    setDragging(true);
  }, []);

  const onNodeDragStop = useCallback(() => {
    setTimeout(() => setDragging(false), 100);
  }, []);

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: Node) => {
      // Don't navigate if user just finished dragging
      if (!dragging) {
        router.push(`/dataset/${node.id}`);
      }
    },
    [router, dragging]
  );

  return (
    <div className="h-[600px] rounded-xl border border-gray-200 dark:border-slate-800 overflow-hidden bg-slate-950">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        onNodeDragStart={onNodeDragStart}
        onNodeDragStop={onNodeDragStop}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        minZoom={0.3}
        maxZoom={1.5}
        proOptions={{ hideAttribution: true }}
      >
        <Background
          variant={BackgroundVariant.Dots}
          gap={20}
          size={1}
          color="#1e293b"
        />
        <Controls
          showInteractive={false}
          className="!bg-slate-800 !border-slate-700 !rounded-lg !shadow-lg"
        />
      </ReactFlow>
    </div>
  );
}
