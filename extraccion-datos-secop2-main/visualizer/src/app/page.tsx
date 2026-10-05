"use client";

import Link from "next/link";
import {
  Database,
  FileSpreadsheet,
  Columns3,
  Layers,
  ArrowRight,
} from "lucide-react";
import { useDiccionario } from "@/hooks/useDiccionario";
import { Dataset } from "@/lib/types";
import { formatNumber, getSlug } from "@/lib/format";

export default function Dashboard() {
  const { data, loading } = useDiccionario();

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
      </div>
    );
  }

  const totalRegistros = data.datasets.reduce((s, d) => s + d.registros, 0);
  const totalColumnas = data.datasets.reduce(
    (s, d) => s + d.num_columnas,
    0
  );

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Catálogo de Datasets
        </h1>
        <p className="text-gray-500 dark:text-slate-400">
          Explora los datasets del proyecto SECOP II — Obra Pública
        </p>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <SummaryCard
          icon={<Layers size={20} />}
          label="Datasets"
          value={String(data.datasets.length)}
          color="blue"
        />
        <SummaryCard
          icon={<FileSpreadsheet size={20} />}
          label="Registros totales"
          value={formatNumber(totalRegistros)}
          color="emerald"
        />
        <SummaryCard
          icon={<Columns3 size={20} />}
          label="Columnas totales"
          value={formatNumber(totalColumnas)}
          color="purple"
        />
      </div>

      {/* Dataset grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {data.datasets.map((dataset) => (
          <DatasetCard key={dataset.archivo} dataset={dataset} />
        ))}
      </div>
    </div>
  );
}

function SummaryCard({
  icon,
  label,
  value,
  color,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  color: "blue" | "emerald" | "purple";
}) {
  const colors = {
    blue: "bg-blue-500/10 text-blue-600 dark:text-blue-400",
    emerald: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400",
    purple: "bg-purple-500/10 text-purple-600 dark:text-purple-400",
  };
  return (
    <div className="bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-5">
      <div className="flex items-center gap-3 mb-3">
        <div className={`p-2 rounded-lg ${colors[color]}`}>{icon}</div>
        <span className="text-sm text-gray-500 dark:text-slate-400">
          {label}
        </span>
      </div>
      <p className="text-2xl font-bold text-gray-900 dark:text-white">
        {value}
      </p>
    </div>
  );
}

function DatasetCard({ dataset }: { dataset: Dataset }) {
  const slug = getSlug(dataset.archivo);

  return (
    <Link href={`/dataset/${slug}`} className="group block">
      <div className="h-full bg-white dark:bg-slate-900 border border-gray-200 dark:border-slate-800 rounded-xl p-5 hover:border-blue-500/50 dark:hover:border-blue-500/50 transition-all hover:shadow-lg dark:hover:shadow-blue-500/5">
        <div className="flex items-start gap-4">
          <div className="p-2.5 rounded-lg bg-blue-500/10 shrink-0">
            <Database className="text-blue-600 dark:text-blue-400" size={20} />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-gray-900 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors leading-tight">
              {dataset.nombre}
            </h3>
            <p className="text-sm text-gray-500 dark:text-slate-400 mt-1.5 line-clamp-2 leading-relaxed">
              {dataset.descripcion}
            </p>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-gray-100 dark:border-slate-800">
          <div className="flex items-center justify-between text-sm">
            <div className="flex gap-4">
              <span className="text-gray-500 dark:text-slate-400">
                <span className="font-semibold text-gray-900 dark:text-white">
                  {formatNumber(dataset.registros)}
                </span>{" "}
                registros
              </span>
              <span className="text-gray-500 dark:text-slate-400">
                <span className="font-semibold text-gray-900 dark:text-white">
                  {dataset.num_columnas}
                </span>{" "}
                cols
              </span>
            </div>
            <ArrowRight
              size={16}
              className="text-gray-300 dark:text-slate-600 group-hover:text-blue-500 transition-colors"
            />
          </div>
        </div>

        <div className="flex items-center gap-2 mt-3">
          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-gray-600 dark:text-slate-400">
            {dataset.fuente_secop}
          </span>
          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-gray-600 dark:text-slate-400">
            {dataset.nivel}
          </span>
        </div>
      </div>
    </Link>
  );
}
