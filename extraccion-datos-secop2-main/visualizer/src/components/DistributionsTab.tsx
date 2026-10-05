"use client";

import { useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Dataset } from "@/lib/types";
import { formatNumber } from "@/lib/format";

export default function DistributionsTab({ dataset }: { dataset: Dataset }) {
  const categoricals = useMemo(() => {
    return dataset.columnas.filter(
      (c) => c.top_valores && c.top_valores.length > 0 && c.unicos <= 30
    );
  }, [dataset]);

  const numerics = useMemo(() => {
    return dataset.columnas.filter(
      (c) => c.estadisticas && c.estadisticas.min !== null
    );
  }, [dataset]);

  return (
    <div className="space-y-8">
      {/* Numeric stats */}
      {numerics.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            Estadísticas numéricas
            <span className="text-xs font-normal px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-gray-500 dark:text-slate-400">
              {numerics.length}
            </span>
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
            {numerics.map((col) => (
              <div
                key={col.columna}
                className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-lg p-4"
              >
                <h4 className="font-mono text-xs text-gray-900 dark:text-white mb-3 truncate">
                  {col.columna}
                </h4>
                <div className="grid grid-cols-2 gap-3">
                  <StatItem label="Mínimo" value={fmtStat(col.estadisticas!.min)} />
                  <StatItem label="Máximo" value={fmtStat(col.estadisticas!.max)} />
                  <StatItem label="Media" value={fmtStat(col.estadisticas!.media, 2)} />
                  <StatItem label="Mediana" value={fmtStat(col.estadisticas!.mediana)} />
                  <StatItem
                    label="Desv. est."
                    value={fmtStat(col.estadisticas!.std, 2)}
                  />
                  <StatItem label="Únicos" value={formatNumber(col.unicos)} />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Categorical distributions */}
      {categoricals.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
            Distribuciones categóricas
            <span className="text-xs font-normal px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-gray-500 dark:text-slate-400">
              {categoricals.length}
            </span>
          </h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {categoricals.map((col) => {
              const data = col
                .top_valores!.slice(0, 10)
                .map((v) => ({
                  name:
                    v.valor.length > 30
                      ? v.valor.slice(0, 27) + "..."
                      : v.valor || "(vacío)",
                  fullName: v.valor || "(vacío)",
                  cantidad: v.cantidad,
                }));
              return (
                <div
                  key={col.columna}
                  className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-lg p-4"
                >
                  <h4 className="font-mono text-xs text-gray-900 dark:text-white mb-1 truncate">
                    {col.columna}
                  </h4>
                  <p className="text-xs text-gray-400 dark:text-slate-500 mb-3">
                    {col.nombre_original} · {formatNumber(col.unicos)} valores únicos
                  </p>
                  <ResponsiveContainer width="100%" height={data.length * 32 + 20}>
                    <BarChart
                      data={data}
                      layout="vertical"
                      margin={{ left: 10, right: 40, top: 0, bottom: 0 }}
                    >
                      <XAxis
                        type="number"
                        tick={{ fontSize: 11, fill: "#94a3b8" }}
                        tickFormatter={(v) => formatNumber(v)}
                      />
                      <YAxis
                        type="category"
                        dataKey="name"
                        width={180}
                        tick={{ fontSize: 11, fill: "#94a3b8" }}
                      />
                      <Tooltip
                        content={({ active, payload }) => {
                          if (!active || !payload?.[0]) return null;
                          const d = payload[0].payload;
                          return (
                            <div className="bg-slate-800 text-white text-xs px-3 py-2 rounded shadow-lg">
                              <p>{d.fullName}</p>
                              <p className="text-blue-400 font-bold">
                                {formatNumber(d.cantidad)}
                              </p>
                            </div>
                          );
                        }}
                      />
                      <Bar dataKey="cantidad" fill="#3b82f6" radius={[0, 4, 4, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {categoricals.length === 0 && numerics.length === 0 && (
        <p className="text-sm text-gray-400 dark:text-slate-500 text-center py-12">
          No hay distribuciones disponibles para este dataset
        </p>
      )}
    </div>
  );
}

function fmtStat(v: number | null, decimals?: number): string {
  if (v === null || v === undefined || isNaN(v)) return "—";
  return formatNumber(decimals ? +v.toFixed(decimals) : v);
}

function StatItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-[11px] text-gray-400 dark:text-slate-500">{label}</p>
      <p className="text-sm font-semibold text-gray-900 dark:text-white tabular-nums">
        {value}
      </p>
    </div>
  );
}
