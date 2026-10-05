"use client";

import { useState, useMemo } from "react";
import { DatasetColumn } from "@/lib/types";
import { formatNumber, formatPercent, getTypeColor } from "@/lib/format";
import { Search, ChevronUp, ChevronDown } from "lucide-react";

type SortKey = "columna" | "tipo_oficial" | "pct_nulos" | "unicos";
type SortDir = "asc" | "desc";

export default function ColumnTable({
  columns,
}: {
  columns: DatasetColumn[];
}) {
  const [search, setSearch] = useState("");
  const [sortKey, setSortKey] = useState<SortKey>("columna");
  const [sortDir, setSortDir] = useState<SortDir>("asc");

  const filtered = useMemo(() => {
    let result = [...columns];
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(
        (c) =>
          c.columna.toLowerCase().includes(q) ||
          c.nombre_original.toLowerCase().includes(q) ||
          c.descripcion.toLowerCase().includes(q)
      );
    }
    result.sort((a, b) => {
      const va = a[sortKey];
      const vb = b[sortKey];
      const cmp = va < vb ? -1 : va > vb ? 1 : 0;
      return sortDir === "asc" ? cmp : -cmp;
    });
    return result;
  }, [columns, search, sortKey, sortDir]);

  const toggleSort = (key: SortKey) => {
    if (sortKey === key) setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    else {
      setSortKey(key);
      setSortDir("asc");
    }
  };

  const SortIcon = ({ col }: { col: SortKey }) => {
    if (sortKey !== col)
      return (
        <ChevronUp size={14} className="opacity-0 group-hover:opacity-30" />
      );
    return sortDir === "asc" ? (
      <ChevronUp size={14} />
    ) : (
      <ChevronDown size={14} />
    );
  };

  return (
    <div>
      <div className="mb-4 relative">
        <Search
          className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
          size={16}
        />
        <input
          type="text"
          placeholder="Buscar columna por nombre o descripción..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full pl-10 pr-4 py-2.5 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 dark:text-white placeholder:text-gray-400 dark:placeholder:text-slate-500"
        />
      </div>

      <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-slate-800">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 dark:bg-slate-800/50 text-left">
              <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400 w-12">
                #
              </th>
              <th
                onClick={() => toggleSort("columna")}
                className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400 cursor-pointer group"
              >
                <span className="flex items-center gap-1">
                  Nombre API <SortIcon col="columna" />
                </span>
              </th>
              <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400">
                Original
              </th>
              <th
                onClick={() => toggleSort("tipo_oficial")}
                className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400 cursor-pointer group"
              >
                <span className="flex items-center gap-1">
                  Tipo <SortIcon col="tipo_oficial" />
                </span>
              </th>
              <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400">
                Descripción
              </th>
              <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400 text-right">
                No nulos
              </th>
              <th
                onClick={() => toggleSort("pct_nulos")}
                className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400 text-right cursor-pointer group"
              >
                <span className="flex items-center justify-end gap-1">
                  Nulos (%) <SortIcon col="pct_nulos" />
                </span>
              </th>
              <th
                onClick={() => toggleSort("unicos")}
                className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400 text-right cursor-pointer group"
              >
                <span className="flex items-center justify-end gap-1">
                  Únicos <SortIcon col="unicos" />
                </span>
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-slate-800/50">
            {filtered.map((col, i) => (
              <tr
                key={col.columna}
                className="hover:bg-gray-50 dark:hover:bg-slate-800/30 transition-colors"
              >
                <td className="px-4 py-2.5 text-gray-400 dark:text-slate-600 tabular-nums">
                  {i + 1}
                </td>
                <td className="px-4 py-2.5 font-mono text-xs text-gray-900 dark:text-white">
                  {col.columna}
                </td>
                <td className="px-4 py-2.5 text-gray-500 dark:text-slate-400 text-xs">
                  {col.nombre_original}
                </td>
                <td className="px-4 py-2.5">
                  <span
                    className={`inline-block px-2 py-0.5 rounded-full text-xs font-medium ${getTypeColor(
                      col.tipo_oficial
                    )}`}
                  >
                    {col.tipo_oficial}
                  </span>
                </td>
                <td className="px-4 py-2.5 text-gray-500 dark:text-slate-400 max-w-sm text-xs wrap-break-word whitespace-normal">
                  {col.descripcion}
                </td>
                <td className="px-4 py-2.5 text-right tabular-nums text-gray-900 dark:text-white">
                  {formatNumber(col.no_nulos)}
                </td>
                <td className="px-4 py-2.5 text-right tabular-nums">
                  <span
                    className={
                      col.pct_nulos > 10
                        ? "text-red-500"
                        : col.pct_nulos > 0
                          ? "text-amber-500"
                          : "text-gray-400 dark:text-slate-500"
                    }
                  >
                    {formatPercent(col.pct_nulos)}
                  </span>
                </td>
                <td className="px-4 py-2.5 text-right tabular-nums text-gray-900 dark:text-white">
                  {formatNumber(col.unicos)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="text-xs text-gray-400 dark:text-slate-500 mt-3">
        Mostrando {filtered.length} de {columns.length} columnas
      </p>
    </div>
  );
}
