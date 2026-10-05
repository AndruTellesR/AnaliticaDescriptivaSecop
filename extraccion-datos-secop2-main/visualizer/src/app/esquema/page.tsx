"use client";

import dynamic from "next/dynamic";
import { useDiccionario } from "@/hooks/useDiccionario";
import { RELATIONS } from "@/lib/schema";
import { formatPercent } from "@/lib/format";

const RelationalDiagram = dynamic(
  () => import("@/components/RelationalDiagram"),
  {
    ssr: false,
    loading: () => (
      <div className="flex items-center justify-center h-[600px] rounded-xl border border-gray-200 dark:border-slate-800">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
      </div>
    ),
  }
);

export default function SchemaPage() {
  const { data, loading } = useDiccionario();

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
      </div>
    );
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Esquema Relacional
        </h1>
        <p className="text-gray-500 dark:text-slate-400">
          Relaciones entre los datasets del proyecto. Click en un nodo para ver
          su detalle.
        </p>
      </div>

      <RelationalDiagram datasets={data.datasets} />

      {/* Relations table */}
      <div className="mt-8">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Detalle de relaciones
        </h2>
        <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-slate-800">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 dark:bg-slate-800/50 text-left">
                <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400">
                  Origen
                </th>
                <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400">
                  Llave origen
                </th>
                <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400">
                  Destino
                </th>
                <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400">
                  Llave destino
                </th>
                <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400 text-right">
                  Cobertura
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100 dark:divide-slate-800/50">
              {RELATIONS.map((rel, i) => (
                <tr
                  key={i}
                  className="hover:bg-gray-50 dark:hover:bg-slate-800/30"
                >
                  <td className="px-4 py-2.5 text-gray-900 dark:text-white text-xs">
                    {rel.origen.replace("_obra", "")}
                  </td>
                  <td className="px-4 py-2.5 font-mono text-xs text-gray-500 dark:text-slate-400">
                    {rel.llave_origen}
                  </td>
                  <td className="px-4 py-2.5 text-gray-900 dark:text-white text-xs">
                    {rel.destino.replace("_obra", "")}
                  </td>
                  <td className="px-4 py-2.5 font-mono text-xs text-gray-500 dark:text-slate-400">
                    {rel.llave_destino}
                  </td>
                  <td className="px-4 py-2.5 text-right">
                    <CoverageBadge value={rel.cobertura} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function CoverageBadge({ value }: { value: number }) {
  const color =
    value >= 90
      ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
      : value >= 50
        ? "bg-amber-500/10 text-amber-600 dark:text-amber-400"
        : "bg-red-500/10 text-red-600 dark:text-red-400";
  return (
    <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-semibold ${color}`}>
      {formatPercent(value)}
    </span>
  );
}
