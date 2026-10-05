# 10 — Las tres hipótesis, puestas a prueba a fondo

**Notebook original:** `eda-extendido-integral/notebooks/10_hipotesis_extendido.ipynb` (aporte propio)

## Explicación técnica paso a paso

### H1 — Licitación pública

1. **Contraste base, en doble lectura.** Se repite el contraste de Mann-Whitney U entre licitación pública y el resto de modalidades, ahora sobre el universo completo (48.331) y sobre el subconjunto observable (19.194) al mismo tiempo. En tiempo: mediana 26 días frente a 0 días en universo completo (rank-biserial -0,3798), y 49 frente a 1 día en observable (-0,3862) — la hipótesis se invierte en ambas lecturas. En costo: -9,18% frente a 0,00% en universo completo (+0,4277), y -2,44% frente a 0,00% en observable (+0,4079) — la hipótesis se sostiene en ambas lecturas. Se declara explícitamente cuál de las dos lecturas es la oficial (universo completo, por instrucción del director) y cuál se usa como verificación de sensibilidad.

2. **Refutación del mecanismo, retomando el notebook 04.** Se incorpora el resultado ya calculado en el notebook 04 —la correlación entre número de oferentes y deslizamiento del plazo es prácticamente nula— como evidencia de que la competencia no es el mecanismo que explica la diferencia encontrada en el paso anterior.

3. **Estratificación por rango de cuantía.** Se repite el contraste de H1, pero ahora por separado dentro de cada rango de cuantía definido en el notebook 05 (menos de 50 millones, 50-200 millones, 200 millones a 1.000 millones, 1.000 a 10.000 millones, más de 10.000 millones). Dos de los cinco estratos (los de menor cuantía) resultan con muestra insuficiente de contratos por licitación pública para una comparación confiable y se marcan como "no evaluables"; en los tres estratos restantes, el efecto de la modalidad sobre el plazo cae de -0,3798 (bruto, sin controlar) a una magnitud media de 0,1113 dentro de los estratos — una reducción del 70,7% en universo completo (72,9% en observable, como verificación).

4. **Conclusión formal de H1.** Con estos tres resultados combinados —se invierte en tiempo, se sostiene en costo, el mecanismo de competencia se refuta, y el efecto se reduce drásticamente al controlar por cuantía— se redacta el veredicto: la hipótesis original queda contrastada, pero su mecanismo explicativo (la competencia) se sustituye por uno respaldado con evidencia (la escala del proyecto).

### H2 — Consorcios y uniones temporales

5. **Contraste base, en doble lectura.** En modificaciones totales: mediana 3 frente a 1 en universo completo (rank-biserial -0,285), y 5 frente a 3 en observable (-0,372) — se sostiene en ambas lecturas, con efecto pequeño en universo completo y mediano en observable. En adiciones de valor específicamente: mediana 0 en ambos grupos y en ambas lecturas, con efecto prácticamente nulo (-0,015 en universo completo) pese a un p-valor significativo — se declara explícitamente que este resultado se rechaza como evidencia sustantiva.

6. **Estratificación por cuantía.** Se repite el mismo procedimiento de estratificación usado en H1, encontrando que el efecto sobre modificaciones totales se reduce en un 70,6% al controlar por cuantía, confirmando que también en H2 buena parte del patrón observado responde a la escala del contrato, no solo al tipo de contratista.

7. **Patrón mixto en alcance.** Se cruza tipo de contratista con índice de alcance mediante chi-cuadrado (V de Cramér = 0,273), encontrando que los consorcios tienen una tasa de "no entregado" del 12,4% frente al 26,4% de las personas jurídicas — es decir, se modifican más pero entregan con más frecuencia. Se retoma aquí, con datos formales, la limitación de cobertura del registro de proveedores documentada en el notebook 07, dejando claro que el perfil de proveedor no puede usarse para explicar esta diferencia sin sesgo.

### H3 — Heterogeneidad territorial

8. **Declaración de no validez, antes del resultado.** Se repite, en este notebook, la declaración explícita de que no existe dato de necesidades básicas insatisfechas por municipio en el dataset, y que el departamento es solo un proxy geográfico, no una medida de NBI.

9. **Análisis de sensibilidad — el aporte propio de este notebook frente a la primera ronda.** Se calcula la prueba de Kruskal-Wallis dos veces para cada indicador: una vez incluyendo el departamento de mayor volumen (Bogotá D.C.) y otra vez excluyéndolo. En tiempo, el tamaño de efecto (épsilon al cuadrado) cae de 0,0577 (con Bogotá, observable) a 0,0098 (sin Bogotá) — una caída del 83%, hasta la categoría "nulo o insignificante". En costo ocurre lo contrario: el efecto sube de 0,0303 a 0,0522 al excluir Bogotá — un aumento del 72%.

10. **Conclusión formal de H3.** Se redacta el veredicto explícito: la heterogeneidad territorial en tiempo que parecía existir en el primer EDA es, en gran medida, un artefacto de la concentración de contratos en un solo departamento, y no debe presentarse como evidencia de heterogeneidad territorial generalizada; en costo, en cambio, la heterogeneidad sí parece ser un fenómeno genuinamente multidepartamental.

## Conclusión

**Qué se hizo, en palabras simples**

Este notebook retoma las tres hipótesis del anteproyecto y las pone a prueba con mucho más cuidado que la primera vez:

- **Sobre la licitación pública:** se confirma que se demora más, pero se demuestra que no es por falta de competencia (ver notebook 04) sino porque estos contratos suelen ser de mayor valor económico. Al comparar solo contratos de tamaños parecidos entre sí, la diferencia entre modalidades se reduce en un 70%.
- **Sobre los consorcios:** se confirma que tienen más modificaciones, pero también se confirma que entregan sus obras completas con más frecuencia que las empresas individuales — un resultado que mezcla cosas buenas y cosas malas.
- **Sobre las zonas más pobres:** se confirma que no se puede comprobar esta hipótesis porque el gobierno no publica ese dato por municipio. Además, se descubre que buena parte de la diferencia que parecía existir entre departamentos en realidad se debía a un solo departamento (Bogotá), que concentra muchísimos contratos.

**Por qué importa**

Es el notebook donde las tres hipótesis del anteproyecto quedan resueltas con evidencia sólida, no solo confirmadas o rechazadas a la ligera.
