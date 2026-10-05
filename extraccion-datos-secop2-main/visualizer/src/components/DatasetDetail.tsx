"use client";

import { useState } from "react";
import Link from "next/link";
import dynamic from "next/dynamic";
import {
  ChevronRight,
  Table2,
  ShieldAlert,
  BarChart3,
  Eye,
  FileText,
} from "lucide-react";
import { Dataset } from "@/lib/types";
import { formatNumber } from "@/lib/format";
import { useDiccionario } from "@/hooks/useDiccionario";
import ColumnTable from "@/components/ColumnTable";
import QualityTab from "@/components/QualityTab";
import DistributionsTab from "@/components/DistributionsTab";

const PreviewTab = dynamic(() => import("@/components/PreviewTab"), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center h-32">
      <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500" />
    </div>
  ),
});

const TABS = [
  { id: "columnas", label: "Columnas", icon: Table2 },
  { id: "calidad", label: "Calidad", icon: ShieldAlert },
  { id: "distribuciones", label: "Distribuciones", icon: BarChart3 },
  { id: "preview", label: "Preview", icon: Eye },
] as const;

type TabId = (typeof TABS)[number]["id"];

export default function DatasetDetail({ slug }: { slug: string }) {
  const { data, loading } = useDiccionario();
  const [activeTab, setActiveTab] = useState<TabId>("columnas");

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
      </div>
    );
  }

  const dataset = data.datasets.find(
    (d) => d.archivo.replace(".parquet", "") === slug
  );

  if (!dataset) {
    return (
      <div className="text-center py-16">
        <p className="text-lg text-gray-500 dark:text-slate-400">
          Dataset no encontrado
        </p>
        <Link
          href="/"
          className="text-blue-500 hover:underline text-sm mt-2 inline-block"
        >
          Volver al catálogo
        </Link>
      </div>
    );
  }

  return (
    <div>
      {/* Breadcrumb */}
      <nav className="flex items-center gap-1.5 text-sm text-gray-500 dark:text-slate-400 mb-6">
        <Link
          href="/"
          className="hover:text-gray-900 dark:hover:text-white transition-colors"
        >
          Catálogo
        </Link>
        <ChevronRight size={14} />
        <span className="text-gray-900 dark:text-white font-medium">
          {dataset.nombre}
        </span>
      </nav>

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          {dataset.nombre}
        </h1>
        <p className="text-gray-500 dark:text-slate-400 leading-relaxed max-w-3xl">
          {dataset.descripcion}
        </p>
        <div className="flex flex-wrap items-center gap-3 mt-4">
          <Badge label={dataset.nivel} />
          <Badge label={`${formatNumber(dataset.registros)} registros`} />
          <Badge label={`${dataset.num_columnas} columnas`} />
          <Badge
            label={dataset.fuente_secop}
            color="bg-blue-500/10 text-blue-600 dark:text-blue-400"
          />
          <span className="flex items-center gap-1.5 text-xs text-gray-400 dark:text-slate-500">
            <FileText size={12} />
            {dataset.notebook}
          </span>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-slate-800 mb-6">
        <div className="flex gap-0">
          {TABS.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === id
                  ? "border-blue-500 text-blue-600 dark:text-blue-400"
                  : "border-transparent text-gray-500 dark:text-slate-400 hover:text-gray-700 dark:hover:text-slate-300"
              }`}
            >
              <Icon size={16} />
              {label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab content */}
      {activeTab === "columnas" && (
        <ColumnTable columns={dataset.columnas} />
      )}
      {activeTab === "calidad" && <QualityTab dataset={dataset} />}
      {activeTab === "distribuciones" && (
        <DistributionsTab dataset={dataset} />
      )}
      {activeTab === "preview" && (
        <PreviewTab archivo={dataset.archivo} columnas={dataset.columnas} />
      )}
    </div>
  );
}

function Badge({
  label,
  color,
}: {
  label: string;
  color?: string;
}) {
  return (
    <span
      className={`text-xs px-2.5 py-1 rounded-full font-medium ${
        color ||
        "bg-slate-100 dark:bg-slate-800 text-gray-600 dark:text-slate-400"
      }`}
    >
      {label}
    </span>
  );
}
