# 02 — Revisión de calidad sobre todos los datos

**Notebook original:** `eda-extendido-integral/notebooks/02_calidad_extendida.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Aplicación de los mismos umbrales de calidad.** Se retoman las mismas reglas cuantitativas definidas en la primera ronda (apta ≤20% de nulidad, uso restringido 20-50%, no apta >50%), pero ahora se evalúan sobre el universo completo de 48.331 contratos y sobre las nuevas columnas incorporadas en el notebook 01 (número de oferentes, precio base, perfil de proveedor).

2. **Re-detección de duplicados residuales.** Se revisa de nuevo la fuente de adiciones, esta vez confirmando explícitamente que, además de las 96.942 filas 100% idénticas ya eliminadas en la fase compartida, quedan 8.894 registros con el mismo identificador pero contenido ligeramente distinto — el residuo de calidad que se había dejado pendiente en el notebook 03 de la fase compartida. Se documenta como una limitación conocida y no resuelta, en lugar de forzar una decisión arbitraria sobre cuál de las versiones conservar.

3. **Detección de outliers en precio base.** Al revisar la nueva columna de precio base, se encuentran valores absurdos heredados directamente del dato crudo de SECOP: un mínimo negativo de -6.087.355.200 pesos y un máximo de 1,1 × 10¹⁶ pesos, claramente errores de digitación en el sistema origen. Se documentan estos valores extremos, que se tratan con cuidado en el notebook 05 (restringiendo el análisis del sobrecosto a comparaciones válidas, no eliminando registros sin justificación).

4. **Recalculo de la inconsistencia liquidación/estado sobre el universo completo.** Se repite, sobre las 48.331 filas (no solo sobre las 19.194 de antes), el conteo de contratos con `liquidación = "Sí"` y estado activo simultáneamente. El número sube a 7.382 casos — más del doble de los 3.538 encontrados en la primera ronda, simplemente porque ahora se está mirando un universo más grande, no porque el problema se haya agravado proporcionalmente.

5. **Caracterización de los casos inconsistentes.** A diferencia de la primera ronda, aquí se profundiza: se desagregan los 7.382 casos por el estado de ejecución específico que contradice la liquidación (2.800 en "En ejecución", 443 en "Aprobado", 290 en "Suspendido", 5 en "Cancelado"), lo que permite entender mejor la naturaleza del problema en lugar de solo contar cuántos casos hay.

6. **Persistencia del reporte de calidad extendido.** Se genera y guarda una versión ampliada del reporte de calidad, que ahora cubre tanto el universo completo como el subconjunto observable, permitiendo comparar directamente si la calidad de los datos difiere entre ambas lecturas.

## Conclusión

**Qué se hizo, en palabras simples**

Se repitió, pero ahora sobre el universo completo de 48.331 contratos, la misma revisión de calidad que se había hecho antes sobre el subconjunto más pequeño: ¿qué tan completos están los datos?, ¿hay valores raros o inconsistentes? Se confirmó, por ejemplo, que el mismo problema de "contratos liquidados que aparecen como si siguieran activos" también aparece aquí, ahora con un número mayor de casos (7.382), simplemente porque se está mirando un grupo de datos más grande.

**Por qué importa**

Garantiza que las reglas de calidad definidas para el análisis se aplican de forma consistente, sin importar si se mira el grupo pequeño o el grupo grande de contratos.
