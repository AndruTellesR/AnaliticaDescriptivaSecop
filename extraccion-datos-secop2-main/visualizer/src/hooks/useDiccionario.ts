"use client";

import { useState, useEffect } from "react";
import { Diccionario } from "@/lib/types";

let cache: Diccionario | null = null;
let promise: Promise<Diccionario> | null = null;

export function useDiccionario() {
  const [data, setData] = useState<Diccionario | null>(cache);
  const [loading, setLoading] = useState(!cache);

  useEffect(() => {
    if (cache) {
      setData(cache);
      setLoading(false);
      return;
    }
    if (!promise) {
      promise = fetch("/data/diccionario_datos.json").then((r) => r.json());
    }
    promise.then((d) => {
      cache = d;
      setData(d);
      setLoading(false);
    });
  }, []);

  return { data, loading };
}
