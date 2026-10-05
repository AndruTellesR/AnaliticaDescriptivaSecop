"use client";

import { useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import { Dataset } from "@/lib/types";
import { formatNumber, formatPercent } from "@/lib/format";

const PIE_COLORS = [
  "#3b82f6",
  "#10b981",
  "#f59e0b",
  "#8b5cf6",
  "#06b6d4",
  "#ef4444",
  "#ec4899",
];

export default function QualityTab({ dataset }: { dataset: Dataset }) {
  const sentinels = useMemo(() => {
    return dataset.columnas
      .filter((c) => c.valores_sentinela && c.valores_sentinela.length > 0)
      .flatMap((c) =>
        c.valores_sentinela!.map((s) => ({
          columna: c.columna,
          valor: s.valor || "(vacío)",
          cantidad: s.cantidad,
          pct: +((s.cantidad / c.total) * 100).toFixed(2),
        }))
      )
      .sort((a, b) => b.cantidad - a.cantidad);
  }, [dataset]);

  const highNulls = useMemo(() => {
    return dataset.columnas
      .filter((c) => c.pct_nulos > 10)
      .sort((a, b) => b.pct_nulos - a.pct_nulos)
      .slice(0, 20)
      .map((c) => ({
        name: c.columna.length > 25 ? c.columna.slice(0, 22) + "..." : c.columna,
        fullName: c.columna,
        pct: +c.pct_nulos.toFixed(1),
      }));
  }, [dataset]);

  const typeDist = useMemo(() => {
    const counts: Record<string, number> = {};
    dataset.columnas.forEach((c) => {
      counts[c.tipo_oficial] = (counts[c.tipo_oficial] || 0) + 1;
    });
    return Object.entries(counts)
      .map(([name, value]) => ({ name, value }))
      .sort((a, b) => b.value - a.value);
  }, [dataset]);

  return (
    <div className="space-y-8">
      {/* Sentinel values */}
      {sentinels.length > 0 && (
        <Section title="Valores sentinela detectados" count={sentinels.length}>
          <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-slate-800">
            <table className="w-full text-sm">
              <thead>
                <tr className="bg-gray-50 dark:bg-slate-800/50 text-left">
                  <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400">
                    Columna
                  </th>
                  <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400">
                    Valor sentinela
                  </th>
                  <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400 text-right">
                    Cantidad
                  </th>
                  <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400 text-right">
                    % del total
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-slate-800/50">
                {sentinels.map((s, i) => (
                  <tr
                    key={`${s.columna}-${s.valor}-${i}`}
                    className="hover:bg-gray-50 dark:hover:bg-slate-800/30"
                  >
                    <td className="px-4 py-2.5 font-mono text-xs text-gray-900 dark:text-white">
                      {s.columna}
                    </td>
                    <td className="px-4 py-2.5">
                      <span className="px-2 py-0.5 rounded bg-amber-500/10 text-amber-600 dark:text-amber-400 text-xs font-medium">
                        {s.valor}
                      </span>
                    </td>
                    <td className="px-4 py-2.5 text-right tabular-nums text-gray-900 dark:text-white">
                      {formatNumber(s.cantidad)}
                    </td>
                    <td className="px-4 py-2.5 text-right tabular-nums text-gray-500 dark:text-slate-400">
                      {formatPercent(s.pct)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Columns with >10% nulls */}
        <Section
          title="Columnas con >10% nulos"
          count={highNulls.length}
        >
          {highNulls.length > 0 ? (
            <div className="bg-white dark:bg-slate-900 rounded-lg border border-gray-200 dark:border-slate-800 p-4">
              <ResponsiveContainer width="100%" height={Math.max(highNulls.length * 32, 150)}>
                <BarChart
                  data={highNulls}
                  layout="vertical"
                  margin={{ left: 10, right: 40, top: 5, bottom: 5 }}
                >
                  <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 12, fill: "#94a3b8" }} />
                  <YAxis
                    type="category"
                    dataKey="name"
                    width={160}
                    tick={{ fontSize: 11, fill: "#94a3b8" }}
                  />
                  <Tooltip
                    content={({ active, payload }) => {
                      if (!active || !payload?.[0]) return null;
                      const d = payload[0].payload;
                      return (
                        <div className="bg-slate-800 text-white text-xs px-3 py-2 rounded shadow-lg">
                          <p className="font-mono">{d.fullName}</p>
                          <p className="text-amber-400 font-bold">{d.pct}% nulos</p>
                        </div>
                      );
                    }}
                  />
                  <Bar dataKey="pct" fill="#f59e0b" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p className="text-sm text-gray-400 dark:text-slate-500">
              Ninguna columna supera el 10% de nulos
            </p>
          )}
        </Section>

        {/* Type distribution */}
        <Section title="Distribución de tipos de dato">
          <div className="bg-white dark:bg-slate-900 rounded-lg border border-gray-200 dark:border-slate-800 p-4">
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={typeDist}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={90}
                  dataKey="value"
                  nameKey="name"
                  paddingAngle={2}
                  label={({ name, value }) => `${name} (${value})`}
                >
                  {typeDist.map((_, i) => (
                    <Cell
                      key={i}
                      fill={PIE_COLORS[i % PIE_COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip
                  content={({ active, payload }) => {
                    if (!active || !payload?.[0]) return null;
                    return (
                      <div className="bg-slate-800 text-white text-xs px-3 py-2 rounded shadow-lg">
                        {payload[0].name}: {payload[0].value} columnas
                      </div>
                    );
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </Section>
      </div>
    </div>
  );
}

function Section({
  title,
  count,
  children,
}: {
  title: string;
  count?: number;
  children: React.ReactNode;
}) {
  return (
    <div>
      <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
        {title}
        {count !== undefined && (
          <span className="text-xs font-normal px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-gray-500 dark:text-slate-400">
            {count}
          </span>
        )}
      </h3>
      {children}
    </div>
  );
}
