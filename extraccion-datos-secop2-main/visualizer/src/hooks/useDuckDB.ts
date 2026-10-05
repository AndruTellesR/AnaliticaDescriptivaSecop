"use client";

import { useState, useCallback, useRef } from "react";
import * as duckdb from "@duckdb/duckdb-wasm";

let dbPromise: Promise<duckdb.AsyncDuckDB> | null = null;

async function initDB(): Promise<duckdb.AsyncDuckDB> {
  const JSDELIVR_BUNDLES = duckdb.getJsDelivrBundles();
  const bundle = await duckdb.selectBundle(JSDELIVR_BUNDLES);

  const worker_url = URL.createObjectURL(
    new Blob([`importScripts("${bundle.mainWorker!}");`], {
      type: "text/javascript",
    })
  );
  const worker = new Worker(worker_url);
  const logger = new duckdb.ConsoleLogger();
  const db = new duckdb.AsyncDuckDB(logger, worker);
  await db.instantiate(bundle.mainModule, bundle.pthreadWorker);
  URL.revokeObjectURL(worker_url);
  return db;
}

function getDB(): Promise<duckdb.AsyncDuckDB> {
  if (!dbPromise) {
    dbPromise = initDB();
  }
  return dbPromise;
}

export interface QueryResult {
  columns: string[];
  rows: Record<string, unknown>[];
  totalRows: number;
}

export function useDuckDB() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const registeredFiles = useRef<Set<string>>(new Set());

  const query = useCallback(
    async (
      filename: string,
      limit: number = 100,
      offset: number = 0,
      where: string = ""
    ): Promise<QueryResult | null> => {
      setLoading(true);
      setError(null);
      try {
        const db = await getDB();

        if (!registeredFiles.current.has(filename)) {
          const response = await fetch(`/data/${filename}`);
          if (!response.ok) throw new Error(`No se pudo cargar ${filename}`);
          const buffer = new Uint8Array(await response.arrayBuffer());
          await db.registerFileBuffer(filename, buffer);
          registeredFiles.current.add(filename);
        }

        const conn = await db.connect();

        // Get total count
        const countResult = await conn.query(
          `SELECT COUNT(*)::INTEGER as count FROM '${filename}'${where}`
        );
        const countRows = countResult.toArray();
        const totalRows = Number(
          countRows[0]?.count ?? countRows[0]?.toJSON?.()?.count ?? 0
        );

        // Execute main query with pagination
        const result = await conn.query(
          `SELECT * FROM '${filename}'${where} LIMIT ${limit} OFFSET ${offset}`
        );
        const columns = result.schema.fields.map((f) => f.name);
        const rawRows = result.toArray();
        const rows = rawRows.map((row) => {
          const obj: Record<string, unknown> = {};
          const json = typeof row.toJSON === "function" ? row.toJSON() : row;
          for (const col of columns) {
            const val = json[col];
            obj[col] = typeof val === "bigint" ? Number(val) : val;
          }
          return obj;
        });

        await conn.close();
        return { columns, rows, totalRows };
      } catch (e) {
        setError(e instanceof Error ? e.message : "Error desconocido");
        return null;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const ensureFile = useCallback(async (filename: string) => {
    const db = await getDB();
    if (!registeredFiles.current.has(filename)) {
      const response = await fetch(`/data/${filename}`);
      if (!response.ok) throw new Error(`No se pudo cargar ${filename}`);
      const buffer = new Uint8Array(await response.arrayBuffer());
      await db.registerFileBuffer(filename, buffer);
      registeredFiles.current.add(filename);
    }
    return db;
  }, []);

  const queryRaw = useCallback(
    async (
      filename: string,
      sql: string
    ): Promise<Record<string, unknown>[]> => {
      const db = await ensureFile(filename);
      const conn = await db.connect();
      const result = await conn.query(sql);
      const columns = result.schema.fields.map((f) => f.name);
      const rawRows = result.toArray();
      const rows = rawRows.map((row) => {
        const obj: Record<string, unknown> = {};
        const json = typeof row.toJSON === "function" ? row.toJSON() : row;
        for (const col of columns) {
          const val = json[col];
          obj[col] = typeof val === "bigint" ? Number(val) : val;
        }
        return obj;
      });
      await conn.close();
      return rows;
    },
    [ensureFile]
  );

  return { query, queryRaw, loading, error };
}
