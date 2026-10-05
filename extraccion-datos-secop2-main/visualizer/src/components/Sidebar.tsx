"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  GitBranch,
  AlertTriangle,
  Sun,
  Moon,
  Database,
} from "lucide-react";
import { useTheme } from "./ThemeProvider";

const NAV_ITEMS = [
  { href: "/", label: "Catálogo", icon: LayoutDashboard },
  { href: "/esquema", label: "Esquema Relacional", icon: GitBranch },
  { href: "/sentinelas", label: "Valores Sentinela", icon: AlertTriangle },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { theme, toggleTheme } = useTheme();

  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-white dark:bg-slate-900 border-r border-gray-200 dark:border-slate-800 flex flex-col z-50">
      {/* Logo */}
      <Link href="/" className="block p-6 border-b border-gray-200 dark:border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-blue-600">
            <Database className="text-white" size={18} />
          </div>
          <div>
            <h1 className="text-sm font-bold text-gray-900 dark:text-white leading-tight">
              SECOP II
            </h1>
            <p className="text-[11px] text-gray-500 dark:text-slate-400 leading-tight">
              Modelo Predictivo Obra Pública
            </p>
          </div>
        </div>
      </Link>

      {/* Navigation */}
      <nav className="flex-1 p-3 space-y-0.5">
        <p className="px-3 py-2 text-[10px] font-semibold uppercase tracking-wider text-gray-400 dark:text-slate-500">
          Navegación
        </p>
        {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
          const active =
            href === "/" ? pathname === "/" : pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                active
                  ? "bg-blue-500/10 text-blue-600 dark:text-blue-400"
                  : "text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800/60"
              }`}
            >
              <Icon size={18} />
              {label}
            </Link>
          );
        })}
      </nav>

      {/* Theme toggle */}
      <div className="p-3 border-t border-gray-200 dark:border-slate-800">
        <button
          onClick={toggleTheme}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-gray-600 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800/60 w-full transition-colors"
        >
          {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          {theme === "dark" ? "Modo claro" : "Modo oscuro"}
        </button>
      </div>
    </aside>
  );
}
