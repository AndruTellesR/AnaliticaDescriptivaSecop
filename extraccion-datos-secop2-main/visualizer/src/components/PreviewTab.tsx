"use client";

import { useState, useEffect, useCallback, useMemo, useRef } from "react";
import { useDuckDB, QueryResult } from "@/hooks/useDuckDB";
import { DatasetColumn } from "@/lib/types";
import { formatNumber } from "@/lib/format";
import {
  Search,
  ChevronLeft,
  ChevronRight,
  Loader2,
  Columns3,
  X,
  Filter,
} from "lucide-react";

const PAGE_SIZE = 50;

interface ColumnFilter {
  column: string;
  value: string;
}

export default function PreviewTab({
  archivo,
  columnas,
}: {
  archivo: string;
  columnas?: DatasetColumn[];
}) {
  const { query, loading, error } = useDuckDB();
  const [result, setResult] = useState<QueryResult | null>(null);
  const [page, setPage] = useState(0);
  const [initialized, setInitialized] = useState(false);

  // Column visibility
  const [hiddenCols, setHiddenCols] = useState<Set<string>>(new Set());
  const [selectorOpen, setSelectorOpen] = useState(false);
  const [colSearch, setColSearch] = useState("");

  // Column filters
  const [filters, setFilters] = useState<ColumnFilter[]>([]);
  const [showFilters, setShowFilters] = useState(false);

  const colMeta = useMemo(() => {
    if (!columnas) return new Map<string, DatasetColumn>();
    const map = new Map<string, DatasetColumn>();
    columnas.forEach((c) => map.set(c.columna, c));
    return map;
  }, [columnas]);

  const buildWhere = useCallback(() => {
    const clauses = filters
      .filter((f) => f.value.trim())
      .map((f) => {
        const meta = colMeta.get(f.column);
        const dtype = meta?.dtype || "str";
        const val = f.value.trim();

        if (dtype === "str" || dtype === "datetime64[us]") {
          const escaped = val.replace(/'/g, "''");
          return `LOWER(CAST("${f.column}" AS VARCHAR)) LIKE '%${escaped.toLowerCase()}%'`;
        }
        if (dtype === "int64" || dtype === "float64") {
          if (val.startsWith(">")) {
            const num = parseFloat(val.slice(1));
            if (!isNaN(num)) return `"${f.column}" > ${num}`;
          } else if (val.startsWith("<")) {
            const num = parseFloat(val.slice(1));
            if (!isNaN(num)) return `"${f.column}" < ${num}`;
          } else if (val.includes("-") && !val.startsWith("-")) {
            const [a, b] = val.split("-").map((s) => parseFloat(s.trim()));
            if (!isNaN(a) && !isNaN(b))
              return `"${f.column}" BETWEEN ${a} AND ${b}`;
          } else {
            const num = parseFloat(val);
            if (!isNaN(num)) return `"${f.column}" = ${num}`;
          }
          return null;
        }
        if (dtype === "bool") {
          if (val.toLowerCase() === "true" || val === "1")
            return `"${f.column}" = true`;
          if (val.toLowerCase() === "false" || val === "0")
            return `"${f.column}" = false`;
          return null;
        }
        const escaped = val.replace(/'/g, "''");
        return `LOWER(CAST("${f.column}" AS VARCHAR)) LIKE '%${escaped.toLowerCase()}%'`;
      })
      .filter(Boolean);

    return clauses.length > 0 ? " WHERE " + clauses.join(" AND ") : "";
  }, [filters, colMeta]);

  const loadPage = useCallback(
    async (p: number) => {
      const where = buildWhere();
      const r = await query(archivo, PAGE_SIZE, p * PAGE_SIZE, where);
      if (r) {
        setResult(r);
        setPage(p);
      }
    },
    [query, archivo, buildWhere]
  );

  useEffect(() => {
    if (!initialized) {
      setInitialized(true);
      loadPage(0);
    }
  }, [initialized, loadPage]);

  // Re-query when filters change
  const filtersKey = filters.map((f) => `${f.column}:${f.value}`).join("|");
  const prevFiltersKey = useRef(filtersKey);
  useEffect(() => {
    if (initialized && prevFiltersKey.current !== filtersKey) {
      prevFiltersKey.current = filtersKey;
      const timer = setTimeout(() => loadPage(0), 400);
      return () => clearTimeout(timer);
    }
  }, [filtersKey, initialized, loadPage]);

  const visibleColumns = useMemo(() => {
    if (!result) return [];
    return result.columns.filter((c) => !hiddenCols.has(c));
  }, [result, hiddenCols]);

  const filteredColList = useMemo(() => {
    if (!result) return [];
    if (!colSearch) return result.columns;
    const q = colSearch.toLowerCase();
    return result.columns.filter((c) => c.toLowerCase().includes(q));
  }, [result, colSearch]);

  const toggleCol = (col: string) => {
    setHiddenCols((prev) => {
      const next = new Set(prev);
      if (next.has(col)) next.delete(col);
      else next.add(col);
      return next;
    });
  };

  const setFilterValue = (column: string, value: string) => {
    setFilters((prev) => {
      const existing = prev.find((f) => f.column === column);
      if (existing) {
        if (!value) return prev.filter((f) => f.column !== column);
        return prev.map((f) => (f.column === column ? { ...f, value } : f));
      }
      if (!value) return prev;
      return [...prev, { column, value }];
    });
  };

  const getFilterValue = (column: string) =>
    filters.find((f) => f.column === column)?.value || "";

  const getFilterPlaceholder = (column: string) => {
    const meta = colMeta.get(column);
    const dtype = meta?.dtype || "str";
    if (dtype === "int64" || dtype === "float64") return ">100, <50, 10-20";
    if (dtype === "bool") return "true / false";
    return "Buscar...";
  };

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-500 text-sm">Error al cargar el archivo</p>
        <p className="text-xs text-gray-400 dark:text-slate-500 mt-1">
          {error}
        </p>
      </div>
    );
  }

  if (!result && loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16 gap-3">
        <Loader2 className="animate-spin text-blue-500" size={32} />
        <p className="text-sm text-gray-500 dark:text-slate-400">
          Cargando {archivo} con DuckDB-WASM...
        </p>
        <p className="text-xs text-gray-400 dark:text-slate-500">
          Primera carga puede tardar unos segundos
        </p>
      </div>
    );
  }

  if (!result) return null;

  const totalPages = Math.ceil(result.totalRows / PAGE_SIZE);
  const activeFilterCount = filters.filter((f) => f.value.trim()).length;

  return (
    <div className="flex flex-col" style={{ height: "calc(100vh - 320px)", minHeight: "400px" }}>
      {/* Toolbar */}
      <div className="flex items-center justify-between mb-3 gap-3 shrink-0">
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSelectorOpen(!selectorOpen)}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg border transition-colors ${
              selectorOpen
                ? "border-blue-500 bg-blue-500/10 text-blue-600 dark:text-blue-400"
                : "border-gray-200 dark:border-slate-700 text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800"
            }`}
          >
            <Columns3 size={14} />
            Columnas ({visibleColumns.length}/{result.columns.length})
          </button>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg border transition-colors ${
              showFilters || activeFilterCount > 0
                ? "border-blue-500 bg-blue-500/10 text-blue-600 dark:text-blue-400"
                : "border-gray-200 dark:border-slate-700 text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800"
            }`}
          >
            <Filter size={14} />
            Filtros{activeFilterCount > 0 && ` (${activeFilterCount})`}
          </button>
          {activeFilterCount > 0 && (
            <button
              onClick={() => { setFilters([]); setTimeout(() => loadPage(0), 50); }}
              className="text-xs text-red-500 hover:text-red-600 px-2 py-1"
            >
              Limpiar filtros
            </button>
          )}
        </div>
        <div className="flex items-center gap-3">
          <p className="text-xs text-gray-500 dark:text-slate-400 shrink-0">
            {formatNumber(result.totalRows)} filas · {result.columns.length} columnas
          </p>
          {loading && <Loader2 className="animate-spin text-blue-500" size={16} />}
        </div>
      </div>

      <div className="flex flex-1 min-h-0 gap-3">
        {/* Column selector sidebar */}
        {selectorOpen && (
          <div className="w-64 shrink-0 flex flex-col bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-lg overflow-hidden">
            <div className="p-3 border-b border-gray-200 dark:border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-medium text-gray-700 dark:text-slate-300">
                  Columnas visibles
                </span>
                <button
                  onClick={() => setSelectorOpen(false)}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-slate-300"
                >
                  <X size={14} />
                </button>
              </div>
              <div className="relative">
                <Search
                  className="absolute left-2 top-1/2 -translate-y-1/2 text-gray-400"
                  size={12}
                />
                <input
                  type="text"
                  placeholder="Buscar columna..."
                  value={colSearch}
                  onChange={(e) => setColSearch(e.target.value)}
                  className="w-full pl-7 pr-2 py-1.5 bg-gray-50 dark:bg-slate-800 border border-gray-200 dark:border-slate-700 rounded text-xs focus:outline-none focus:ring-1 focus:ring-blue-500/50 dark:text-white placeholder:text-gray-400 dark:placeholder:text-slate-500"
                />
              </div>
              <div className="flex gap-2 mt-2">
                <button
                  onClick={() => setHiddenCols(new Set())}
                  className="text-[10px] text-blue-500 hover:text-blue-600"
                >
                  Todas
                </button>
                <button
                  onClick={() => setHiddenCols(new Set(result.columns))}
                  className="text-[10px] text-blue-500 hover:text-blue-600"
                >
                  Ninguna
                </button>
              </div>
            </div>
            <div className="flex-1 overflow-y-auto p-2">
              {filteredColList.map((col) => (
                <label
                  key={col}
                  className="flex items-center gap-2 px-2 py-1 rounded hover:bg-gray-50 dark:hover:bg-slate-800/50 cursor-pointer"
                >
                  <input
                    type="checkbox"
                    checked={!hiddenCols.has(col)}
                    onChange={() => toggleCol(col)}
                    className="rounded border-gray-300 dark:border-slate-600 text-blue-500 focus:ring-blue-500/50"
                  />
                  <span className="text-xs font-mono text-gray-700 dark:text-slate-300 truncate">
                    {col}
                  </span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Table */}
        <div className="flex-1 min-w-0 flex flex-col">
          <div className="flex-1 overflow-auto rounded-lg border border-gray-200 dark:border-slate-800">
            <table className="w-full text-xs">
              <thead className="sticky top-0 z-10">
                <tr className="bg-gray-50 dark:bg-slate-800/50">
                  {visibleColumns.map((col) => (
                    <th
                      key={col}
                      className="px-3 py-2.5 text-left font-medium text-gray-500 dark:text-slate-400 whitespace-nowrap bg-gray-50 dark:bg-slate-800/90"
                    >
                      {col}
                    </th>
                  ))}
                </tr>
                {showFilters && (
                  <tr className="bg-gray-50/80 dark:bg-slate-800/30">
                    {visibleColumns.map((col) => (
                      <th key={col} className="px-2 py-1.5 bg-gray-50/80 dark:bg-slate-800/70">
                        <input
                          type="text"
                          value={getFilterValue(col)}
                          onChange={(e) => setFilterValue(col, e.target.value)}
                          placeholder={getFilterPlaceholder(col)}
                          className="w-full min-w-[60px] px-2 py-1 bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-700 rounded text-xs font-normal focus:outline-none focus:ring-1 focus:ring-blue-500/50 dark:text-white placeholder:text-gray-400 dark:placeholder:text-slate-500"
                        />
                      </th>
                    ))}
                  </tr>
                )}
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-slate-800/50">
                {result.rows.map((row, i) => (
                  <tr
                    key={i}
                    className="hover:bg-gray-50 dark:hover:bg-slate-800/30"
                  >
                    {visibleColumns.map((col) => (
                      <td
                        key={col}
                        className="px-3 py-2 text-gray-700 dark:text-slate-300 whitespace-nowrap max-w-[300px] truncate"
                      >
                        {formatCell(row[col])}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between mt-3 shrink-0">
            <p className="text-xs text-gray-400 dark:text-slate-500">
              Página {page + 1} de {formatNumber(totalPages)}
            </p>
            <div className="flex items-center gap-2">
              <button
                onClick={() => loadPage(page - 1)}
                disabled={page === 0 || loading}
                className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 dark:border-slate-700 text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                <ChevronLeft size={14} /> Anterior
              </button>
              <button
                onClick={() => loadPage(page + 1)}
                disabled={page >= totalPages - 1 || loading}
                className="flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 dark:border-slate-700 text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                Siguiente <ChevronRight size={14} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function formatCell(value: unknown): string {
  if (value === null || value === undefined) return "—";
  if (typeof value === "boolean") return value ? "Sí" : "No";
  if (typeof value === "number") return formatNumber(value);
  return String(value);
}
