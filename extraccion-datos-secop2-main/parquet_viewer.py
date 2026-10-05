"""
Visor de archivos Parquet — GUI con Tkinter
Uso: python parquet_viewer.py [ruta.parquet]
"""

import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import webbrowser

import pandas as pd
import pyarrow.parquet as pq


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------
PAGE_SIZE = 200  # filas por pagina
MAX_CELL = 80    # caracteres visibles por celda


class ParquetViewer(tk.Tk):
    def __init__(self, initial_path: str | None = None):
        super().__init__()
        self.title("Parquet Viewer")
        self.geometry("1200x700")
        self.minsize(800, 500)

        self.df: pd.DataFrame | None = None
        self.filtered_df: pd.DataFrame | None = None
        self.page = 0
        self.visible_cols: list[str] = []

        self._build_ui()

        if initial_path:
            self._load_file(initial_path)

    # -----------------------------------------------------------------------
    # UI
    # -----------------------------------------------------------------------
    def _build_ui(self):
        # --- Barra superior ---
        top = ttk.Frame(self)
        top.pack(fill="x", padx=6, pady=(6, 2))

        ttk.Button(top, text="Abrir archivo", command=self._open_dialog).pack(side="left")
        self.lbl_file = ttk.Label(top, text="  Ningun archivo cargado", foreground="gray")
        self.lbl_file.pack(side="left", padx=8)

        # --- Info / metadata ---
        info_frame = ttk.LabelFrame(self, text="Metadata")
        info_frame.pack(fill="x", padx=6, pady=2)
        self.lbl_info = ttk.Label(info_frame, text="", justify="left")
        self.lbl_info.pack(anchor="w", padx=6, pady=4)

        # --- Filtros ---
        filt = ttk.LabelFrame(self, text="Filtros")
        filt.pack(fill="x", padx=6, pady=2)

        row1 = ttk.Frame(filt)
        row1.pack(fill="x", padx=4, pady=2)
        ttk.Label(row1, text="Buscar texto:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(row1, textvariable=self.search_var, width=40)
        search_entry.pack(side="left", padx=4)
        search_entry.bind("<Return>", lambda _: self._apply_filters())
        ttk.Button(row1, text="Filtrar", command=self._apply_filters).pack(side="left")
        ttk.Button(row1, text="Limpiar", command=self._clear_filters).pack(side="left", padx=4)

        row2 = ttk.Frame(filt)
        row2.pack(fill="x", padx=4, pady=2)
        ttk.Label(row2, text="Columna:").pack(side="left")
        self.col_var = tk.StringVar()
        self.col_combo = ttk.Combobox(row2, textvariable=self.col_var, state="readonly", width=35)
        self.col_combo.pack(side="left", padx=4)
        ttk.Label(row2, text="Contiene:").pack(side="left")
        self.col_search_var = tk.StringVar()
        col_entry = ttk.Entry(row2, textvariable=self.col_search_var, width=30)
        col_entry.pack(side="left", padx=4)
        col_entry.bind("<Return>", lambda _: self._apply_filters())

        # --- Tabla ---
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=6, pady=2)

        self.tree = ttk.Treeview(table_frame, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # click en header para ordenar
        self.tree.bind("<Button-1>", self._on_header_click)

        # menu contextual (click derecho)
        self.ctx_menu = tk.Menu(self, tearoff=0)
        self.tree.bind("<Button-3>", self._on_right_click)

        # --- Paginacion ---
        pag = ttk.Frame(self)
        pag.pack(fill="x", padx=6, pady=(2, 6))

        self.btn_prev = ttk.Button(pag, text="<< Anterior", command=self._prev_page, state="disabled")
        self.btn_prev.pack(side="left")
        self.lbl_page = ttk.Label(pag, text="")
        self.lbl_page.pack(side="left", padx=12)
        self.btn_next = ttk.Button(pag, text="Siguiente >>", command=self._next_page, state="disabled")
        self.btn_next.pack(side="left")

        ttk.Button(pag, text="Exportar vista a CSV", command=self._export_csv).pack(side="right")

        # --- Barra de detalle (celda completa) ---
        det = ttk.LabelFrame(self, text="Detalle de celda seleccionada")
        det.pack(fill="x", padx=6, pady=(0, 6))
        self.detail_var = tk.StringVar()
        det_entry = ttk.Entry(det, textvariable=self.detail_var, state="readonly")
        det_entry.pack(fill="x", padx=4, pady=4)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    # -----------------------------------------------------------------------
    # Carga
    # -----------------------------------------------------------------------
    def _open_dialog(self):
        path = filedialog.askopenfilename(
            title="Seleccionar archivo Parquet",
            filetypes=[("Parquet", "*.parquet"), ("Todos", "*.*")],
        )
        if path:
            self._load_file(path)

    def _load_file(self, path: str):
        try:
            p = Path(path)
            # metadata rapida sin leer todo
            pf = pq.ParquetFile(p)
            meta = pf.metadata
            schema = pf.schema_arrow

            self.df = pd.read_parquet(p)
            self.filtered_df = self.df
            self.page = 0

            # actualizar UI
            self.title(f"Parquet Viewer — {p.name}")
            self.lbl_file.config(text=f"  {p.name}", foreground="black")

            size_mb = p.stat().st_size / (1024 * 1024)
            info_lines = (
                f"Archivo: {p.name}  |  Tamano: {size_mb:.2f} MB  |  "
                f"Filas: {meta.num_rows:,}  |  Columnas: {meta.num_columns}  |  "
                f"Row groups: {meta.num_row_groups}"
            )
            self.lbl_info.config(text=info_lines)

            # columnas para combo
            cols = ["(todas)"] + list(self.df.columns)
            self.col_combo["values"] = cols
            self.col_combo.current(0)

            self.visible_cols = list(self.df.columns)
            self._refresh_table()

        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))

    # -----------------------------------------------------------------------
    # Filtros
    # -----------------------------------------------------------------------
    def _apply_filters(self):
        if self.df is None:
            return

        result = self.df

        # filtro global de texto
        search = self.search_var.get().strip()
        if search:
            mask = result.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
            result = result[mask]

        # filtro por columna especifica
        col = self.col_var.get()
        col_search = self.col_search_var.get().strip()
        if col and col != "(todas)" and col_search:
            mask = result[col].astype(str).str.contains(col_search, case=False, na=False)
            result = result[mask]

        self.filtered_df = result
        self.page = 0
        self._refresh_table()

    def _clear_filters(self):
        self.search_var.set("")
        self.col_search_var.set("")
        self.col_combo.current(0)
        self.filtered_df = self.df
        self.page = 0
        self._refresh_table()

    # -----------------------------------------------------------------------
    # Tabla / paginacion
    # -----------------------------------------------------------------------
    def _refresh_table(self):
        if self.filtered_df is None:
            return

        df = self.filtered_df
        total = len(df)
        start = self.page * PAGE_SIZE
        end = min(start + PAGE_SIZE, total)
        page_df = df.iloc[start:end]

        # columnas
        cols = list(page_df.columns)
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, minwidth=60, stretch=False)

        # filas
        self.tree.delete(*self.tree.get_children())
        for _, row in page_df.iterrows():
            vals = [str(v)[:MAX_CELL] if pd.notna(v) else "" for v in row]
            self.tree.insert("", "end", values=vals)

        # paginacion
        total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        current = self.page + 1
        self.lbl_page.config(text=f"Pagina {current}/{total_pages}  ({total:,} filas)")
        self.btn_prev.config(state="normal" if self.page > 0 else "disabled")
        self.btn_next.config(state="normal" if end < total else "disabled")

    def _prev_page(self):
        if self.page > 0:
            self.page -= 1
            self._refresh_table()

    def _next_page(self):
        if self.filtered_df is not None:
            if (self.page + 1) * PAGE_SIZE < len(self.filtered_df):
                self.page += 1
                self._refresh_table()

    # -----------------------------------------------------------------------
    # Ordenamiento por header
    # -----------------------------------------------------------------------
    def _on_header_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "heading" or self.filtered_df is None:
            return
        col_id = self.tree.identify_column(event.x)
        col_idx = int(col_id.replace("#", "")) - 1
        col_name = self.filtered_df.columns[col_idx]

        # toggle ascendente/descendente
        current_heading = self.tree.heading(col_name, "text")
        ascending = not current_heading.endswith(" ▲")

        self.filtered_df = self.filtered_df.sort_values(col_name, ascending=ascending, na_position="last")
        self.page = 0

        # actualizar headers con indicador
        for c in self.filtered_df.columns:
            self.tree.heading(c, text=c)
        arrow = " ▲" if ascending else " ▼"
        self.tree.heading(col_name, text=f"{col_name}{arrow}")

        self._refresh_table()

    # -----------------------------------------------------------------------
    # Detalle de celda
    # -----------------------------------------------------------------------
    def _on_select(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        item = self.tree.item(sel[0])
        # mostrar columna:valor de la primera celda con focus
        col_id = self.tree.focus()
        vals = item["values"]
        if vals:
            # obtener indice real del dataframe
            row_idx = self.tree.index(sel[0])
            real_idx = self.page * PAGE_SIZE + row_idx
            if self.filtered_df is not None and real_idx < len(self.filtered_df):
                row = self.filtered_df.iloc[real_idx]
                detail = " | ".join(f"{c}={v}" for c, v in row.items() if pd.notna(v) and str(v).strip())
                self.detail_var.set(detail[:500])

    # -----------------------------------------------------------------------
    # Menu contextual (click derecho)
    # -----------------------------------------------------------------------
    def _get_cell_value(self, event):
        """Devuelve (col_name, full_value) de la celda bajo el cursor."""
        row_id = self.tree.identify_row(event.y)
        col_id = self.tree.identify_column(event.x)
        if not row_id or not col_id:
            return None, None
        col_idx = int(col_id.replace("#", "")) - 1
        row_idx = self.tree.index(row_id)
        real_idx = self.page * PAGE_SIZE + row_idx
        if self.filtered_df is None or real_idx >= len(self.filtered_df):
            return None, None
        col_name = self.filtered_df.columns[col_idx]
        raw = self.filtered_df.iloc[real_idx][col_name]
        value = "" if pd.isna(raw) else str(raw)
        return col_name, value

    @staticmethod
    def _is_url(text: str) -> bool:
        return text.startswith(("http://", "https://"))

    def _on_right_click(self, event):
        col_name, value = self._get_cell_value(event)
        if col_name is None:
            return

        self.ctx_menu.delete(0, "end")
        self.ctx_menu.add_command(
            label=f"Copiar valor ({col_name})",
            command=lambda: self._copy_to_clipboard(value),
        )
        if self._is_url(value):
            self.ctx_menu.add_command(
                label="Abrir URL en navegador",
                command=lambda: webbrowser.open(value),
            )
        self.ctx_menu.tk_popup(event.x_root, event.y_root)

    def _copy_to_clipboard(self, text: str):
        self.clipboard_clear()
        self.clipboard_append(text)

    # -----------------------------------------------------------------------
    # Exportar
    # -----------------------------------------------------------------------
    def _export_csv(self):
        if self.filtered_df is None:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            title="Exportar vista filtrada",
        )
        if path:
            self.filtered_df.to_csv(path, index=False)
            messagebox.showinfo("Exportado", f"{len(self.filtered_df):,} filas guardadas en {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    initial = sys.argv[1] if len(sys.argv) > 1 else None
    app = ParquetViewer(initial)
    app.mainloop()
