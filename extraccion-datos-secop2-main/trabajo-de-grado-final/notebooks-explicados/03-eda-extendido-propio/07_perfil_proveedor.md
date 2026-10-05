# 07 — Un vistazo más de cerca a los proveedores

**Notebook original:** `eda-extendido-integral/notebooks/07_perfil_proveedor.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Recuperación de la variable `es_pyme`.** Se identifica que el campo que indica si un proveedor es una pequeña o mediana empresa está disponible directamente en el contrato (heredado de la fuente de contratos electrónicos) con cobertura del 100%, y que hasta este punto del trabajo no se había usado en ningún análisis. Se incorpora como variable de perfil.

2. **Cálculo de la cobertura del registro externo por tipo de contratista.** Se calcula, por separado para consorcios/uniones temporales y para personas jurídicas individuales, qué porcentaje de cada grupo tiene un registro completo en la fuente de proveedores registrados (tipo de empresa, antigüedad, categoría UNSPSC). El resultado muestra una diferencia muy marcada: la cobertura es del 0,0% para consorcios frente al 82,4% para personas jurídicas — es decir, el registro externo de proveedores prácticamente no contiene perfiles de consorcios.

3. **Declaración de la limitación antes de usar los datos, no después.** Al encontrar esta brecha de cobertura, se decide, de forma explícita y documentada, no usar las variables de perfil de proveedor (tipo de empresa, antigüedad) para comparar consorcios contra personas jurídicas en el contraste de la hipótesis H2, porque cualquier diferencia observada sería un artefacto de la falta de datos, no un patrón real. Esta decisión se toma y se documenta antes de que el notebook 10 use esta información, precisamente para evitar sesgar el contraste de hipótesis.

4. **Perfil comparado en las variables que sí son confiables.** Sobre las variables que sí están disponibles para ambos grupos (valor del contrato, número de oferentes, si es PYME, si fue por licitación pública, mediana de deslizamiento del plazo, porcentaje con retraso mayor a 30 días), se construye una tabla comparativa entre consorcios y personas jurídicas, que sirve de insumo directo para la interpretación del patrón mixto encontrado en H2.

5. **Análisis de concentración de mercado.** Se revisa si un número reducido de proveedores acumula una proporción desproporcionada de contratos (reincidencia), como una exploración adicional sobre la estructura del mercado de contratistas de obra pública.

## Conclusión

**Qué se hizo, en palabras simples**

Se examinó el perfil de los proveedores —si son pequeñas o grandes empresas, hace cuánto existen, a qué se dedican— y se comparó ese perfil entre consorcios y empresas individuales. Se descubrió una limitación importante: el registro de proveedores del gobierno tiene mucha menos información disponible para los consorcios que para las empresas individuales, lo que significa que cualquier comparación de perfil entre estos dos grupos hay que tomarla con cuidado.

**Por qué importa**

Evita sacar conclusiones injustas: si parece que los consorcios "tienen menos información de perfil", no es necesariamente porque sean distintos, sino porque el propio sistema del gobierno los registra peor.
