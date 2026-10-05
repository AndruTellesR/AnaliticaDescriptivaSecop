"use client";

import { useState, useMemo, useEffect, useCallback, useRef } from "react";
import { useDiccionario } from "@/hooks/useDiccionario";
import { useDuckDB } from "@/hooks/useDuckDB";
import { formatNumber, formatPercent } from "@/lib/format";
import { SENTINEL_VALUES } from "@/lib/schema";
import { Search, AlertTriangle, Loader2 } from "lucide-react";

interface SentinelRow {
  dataset: string;
  columna: string;
  valor: string;
  cantidad: number;
  total: number;
  pct: number;
}

export default function SentinelContent() {
  const { data, loading: dictLoading } = useDiccionario();
  const { queryRaw } = useDuckDB();
  const [filterDataset, setFilterDataset] = useState<string>("todos");
  const [search, setSearch] = useState("");
  const [sentinels, setSentinels] = useState<SentinelRow[]>([]);
  const [scanning, setScanning] = useState(false);
  const [progress, setProgress] = useState("");
  const scanned = useRef(false);

  const scanSentinels = useCallback(async () => {
    if (!data || scanned.current) return;
    scanned.current = true;
    setScanning(true);

    const results: SentinelRow[] = [];
    const nonEmptySentinels = SENTINEL_VALUES.filter((v) => v.trim() !== "");
    const inList = nonEmptySentinels
      .map((v) => `'${v.replace(/'/g, "''")}'`)
      .join(", ");

    for (const ds of data.datasets) {
      setProgress(`Escaneando ${ds.nombre}...`);

      const strCols = ds.columnas
        .filter((c) => c.dtype === "str")
        .map((c) => c.columna);

      for (const col of strCols) {
        try {
          // Count exact matches for non-empty sentinels
          const textRows = await queryRaw(
            ds.archivo,
            `SELECT "${col}" as valor, COUNT(*)::INTEGER as cantidad
             FROM '${ds.archivo}'
             WHERE "${col}" IN (${inList})
             GROUP BY "${col}"`
          );
          for (const r of textRows) {
            const cantidad = Number(r.cantidad);
            if (cantidad > 0) {
              results.push({
                dataset: ds.nombre,
                columna: col,
                valor: String(r.valor),
                cantidad,
                total: ds.registros,
                pct: +((cantidad / ds.registros) * 100).toFixed(2),
              });
            }
          }

          // Count empty strings
          const emptyRows = await queryRaw(
            ds.archivo,
            `SELECT COUNT(*)::INTEGER as cantidad FROM '${ds.archivo}' WHERE "${col}" = ''`
          );
          const emptyCount = Number(emptyRows[0]?.cantidad ?? 0);
          if (emptyCount > 0) {
            results.push({
              dataset: ds.nombre,
              columna: col,
              valor: "(vac\u00edo)",
              cantidad: emptyCount,
              total: ds.registros,
              pct: +((emptyCount / ds.registros) * 100).toFixed(2),
            });
          }
        } catch {
          // Skip columns that cause query errors
        }
      }
    }

    results.sort((a, b) => b.cantidad - a.cantidad);
    setSentinels(results);
    setScanning(false);
    setProgress("");
  }, [data, queryRaw]);

  useEffect(() => {
    if (data && !scanned.current) {
      scanSentinels();
    }
  }, [data, scanSentinels]);

  const datasetNames = useMemo(() => {
    return [...new Set(sentinels.map((s) => s.dataset))];
  }, [sentinels]);

  const filtered = useMemo(() => {
    let result = sentinels;
    if (filterDataset !== "todos") {
      result = result.filter((s) => s.dataset === filterDataset);
    }
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(
        (s) =>
          s.columna.toLowerCase().includes(q) ||
          s.valor.toLowerCase().includes(q)
      );
    }
    return result;
  }, [sentinels, filterDataset, search]);

  if (dictLoading || !data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
      </div>
    );
  }

  const totalSentinels = sentinels.reduce((s, r) => s + r.cantidad, 0);

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Valores Sentinela
        </h1>
        <p className="text-gray-500 dark:text-slate-400">
          Pseudo-nulos detectados en todos los datasets. Estos valores enmascaran
          datos faltantes.
        </p>
      </div>

      {scanning && (
        <div className="flex items-center gap-3 mb-6 p-4 bg-blue-500/5 dark:bg-blue-500/10 border border-blue-200 dark:border-blue-500/20 rounded-lg">
          <Loader2 className="animate-spin text-blue-500" size={20} />
          <div>
            <p className="text-sm font-medium text-blue-700 dark:text-blue-400">
              Escaneando archivos Parquet con DuckDB...
            </p>
            <p className="text-xs text-blue-600/70 dark:text-blue-400/70 mt-0.5">
              {progress}
            </p>
          </div>
        </div>
      )}

      {/* Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-5">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 rounded-lg bg-amber-500/10">
              <AlertTriangle className="text-amber-500" size={18} />
            </div>
            <span className="text-sm text-gray-500 dark:text-slate-400">
              Total ocurrencias
            </span>
          </div>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {formatNumber(totalSentinels)}
          </p>
        </div>
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-5">
          <p className="text-sm text-gray-500 dark:text-slate-400 mb-2">
            Valores únicos detectados
          </p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {[...new Set(sentinels.map((s) => s.valor))].length}
          </p>
        </div>
        <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-5">
          <p className="text-sm text-gray-500 dark:text-slate-400 mb-2">
            Columnas afectadas
          </p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {[...new Set(sentinels.map((s) => `${s.dataset}-${s.columna}`))].length}
          </p>
        </div>
      </div>

      {/* Known sentinels */}
      <div className="mb-6 bg-amber-500/5 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-500/20 rounded-lg p-4">
        <h3 className="text-sm font-medium text-amber-700 dark:text-amber-400 mb-2">
          Valores sentinela conocidos
        </h3>
        <div className="flex flex-wrap gap-2">
          {SENTINEL_VALUES.filter((v) => v.trim()).map((v) => (
            <span
              key={v}
              className="px-2 py-0.5 rounded bg-amber-100 dark:bg-amber-500/20 text-amber-700 dark:text-amber-300 text-xs font-mono"
            >
              &quot;{v}&quot;
            </span>
          ))}
          <span className="px-2 py-0.5 rounded bg-amber-100 dark:bg-amber-500/20 text-amber-700 dark:text-amber-300 text-xs font-mono">
            &quot;&quot; (vacío)
          </span>
          <span className="px-2 py-0.5 rounded bg-amber-100 dark:bg-amber-500/20 text-amber-700 dark:text-amber-300 text-xs font-mono">
            &quot; &quot; (espacio)
          </span>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-4 mb-4">
        <div className="relative flex-1 max-w-sm">
          <Search
            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            size={16}
          />
          <input
            type="text"
            placeholder="Buscar por columna o valor..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 dark:text-white placeholder:text-gray-400 dark:placeholder:text-slate-500"
          />
        </div>
        <select
          value={filterDataset}
          onChange={(e) => setFilterDataset(e.target.value)}
          className="px-3 py-2 bg-white dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 dark:text-white"
        >
          <option value="todos">Todos los datasets</option>
          {datasetNames.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
      </div>

      {/* Table */}
      <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-slate-800">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-50 dark:bg-slate-800/50 text-left">
              <th className="px-4 py-3 font-medium text-gray-500 dark:text-slate-400">
                Dataset
              </th>
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
            {filtered.length === 0 && !scanning && (
              <tr>
                <td
                  colSpan={5}
                  className="px-4 py-8 text-center text-gray-400 dark:text-slate-500 text-sm"
                >
                  No se encontraron valores sentinela
                </td>
              </tr>
            )}
            {filtered.slice(0, 200).map((s, i) => (
              <tr
                key={i}
                className="hover:bg-gray-50 dark:hover:bg-slate-800/30"
              >
                <td className="px-4 py-2.5 text-xs text-gray-900 dark:text-white">
                  {s.dataset}
                </td>
                <td className="px-4 py-2.5 font-mono text-xs text-gray-500 dark:text-slate-400">
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
      <p className="text-xs text-gray-400 dark:text-slate-500 mt-3">
        Mostrando {Math.min(filtered.length, 200)} de {filtered.length}{" "}
        registros
      </p>
    </div>
  );
}
