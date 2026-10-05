export function formatNumber(n: number): string {
  return n.toLocaleString("es-CO");
}

export function formatPercent(n: number, decimals = 1): string {
  return `${n.toFixed(decimals)}%`;
}

export function getTypeColor(tipo: string): string {
  const colors: Record<string, string> = {
    Texto: "bg-blue-500/20 text-blue-600 dark:text-blue-400",
    "Número": "bg-emerald-500/20 text-emerald-600 dark:text-emerald-400",
    Fecha: "bg-orange-500/20 text-orange-600 dark:text-orange-400",
    Booleano: "bg-purple-500/20 text-purple-600 dark:text-purple-400",
    URL: "bg-cyan-500/20 text-cyan-600 dark:text-cyan-400",
  };
  return colors[tipo] || "bg-gray-500/20 text-gray-600 dark:text-gray-400";
}

export function getCoverageColor(pct: number): string {
  if (pct >= 90) return "bg-emerald-500";
  if (pct >= 50) return "bg-amber-500";
  return "bg-red-500";
}

export function getCoverageTextColor(pct: number): string {
  if (pct >= 90) return "text-emerald-400";
  if (pct >= 50) return "text-amber-400";
  return "text-red-400";
}

export function getSlug(archivo: string): string {
  return archivo.replace(".parquet", "");
}
