# 03 — Indicadores de tiempo, costo y alcance (el corazón del trabajo)

**Notebook original:** `analitica-descriptiva-andres/notebooks/03_indicadores_restriccion_hierro.ipynb` (aporte propio)

## Explicación técnica paso a paso

1. **Declaración explícita de blindaje de autoría.** La primera celda de markdown del notebook enumera, por nombre, todas las columnas producidas por el código excluido del compañero (`tiempo`, `presupuesto`, `alcance`, `sobrecosto_ratio`, `duracion_planificada_dias`, `ratio_extension_duracion`, `dias_hasta_primera_adicion`, `ventana_adiciones_dias`, `log_valor_contrato`, y las variables `rup_*`), dejando constancia de que ninguna de ellas se usa en este notebook, y que los tres indicadores que siguen se construyen leyendo solo el texto del anteproyecto.

2. **Parseo del plazo pactado.** El campo `duraci_n_del_contrato` llega desde SECOP como texto libre (por ejemplo, "4 Mes(es)", "135 Dia(s)", o "No definido"). Se construye una función de interpretación propia: si el texto contiene la palabra "Dia(s)", se toma el número literal; si contiene "Mes(es)", se multiplica el número por 30; cualquier otro formato se marca como no interpretable (valor nulo). Este parseo logra interpretar 16.326 de los 19.194 contratos de la muestra analítica (85,1%).

3. **Cálculo del plazo real.** Se calcula la diferencia en días entre `fecha_de_fin_del_contrato` y `fecha_de_inicio_del_contrato`, disponible para el 100% de la muestra (19.194 contratos), ya que estas dos fechas fueron parte de los campos exigidos como completos en el notebook 02.

4. **Cálculo del deslizamiento del plazo (desviación de tiempo).** Se resta: plazo real menos plazo pactado. Un valor positivo indica que el contrato tomó más días de los pactados originalmente. Este cálculo solo es posible para los 16.326 contratos donde el parseo del plazo pactado tuvo éxito.

5. **Cálculo de la desviación de costo.** Se calcula la diferencia entre `valor_pagado` y `valor_del_contrato`, expresada como porcentaje del valor del contrato, y restringida a los casos donde `valor_pagado` es mayor que cero (para no confundir "no se ha reportado el pago" con "se pagó cero"). Esto deja un N efectivo de 8.681 contratos (45,2% de la muestra).

6. **Construcción del índice de alcance.** Se define una variable categórica de tres niveles a partir de las banderas ya agregadas en el notebook 05 compartido: si el contrato tiene una conclusión anticipada registrada, se clasifica como "No entregado"; si no tiene conclusión pero sí tiene suspensión o cesión, se clasifica como "Entregado parcialmente"; en cualquier otro caso, se clasifica como "Entregado en su totalidad". Este orden de prioridad (conclusión > suspensión/cesión > sin eventos) se justifica más adelante, con datos de co-ocurrencia, en el notebook 08 del EDA extendido.

7. **Nota sobre las columnas prohibidas y no usadas.** Se deja escrito explícitamente, en una celda de markdown, cuáles columnas del dataset de 125 no se usan y por qué, distinguiendo entre las prohibidas por blindaje de autoría y las que simplemente no se necesitan para este cálculo (por ejemplo, `rup_idx_endeudamiento`, que es información financiera del proveedor, no del contrato).

8. **Persistencia.** Los tres indicadores, junto con las columnas de identificación y segmentación necesarias para los notebooks siguientes (modalidad, tipo de contratista, territorio, y las columnas `n_adicion_valor`, `n_modificaciones_total`, `dias_adicionados` requeridas más adelante para el contraste de H2), se guardan en `indicadores_restriccion_hierro.parquet`.

## Conclusión

**Qué se hizo, en palabras simples**

Este es el notebook donde se construyen, desde cero, los tres números que resumen si un contrato de obra pública "salió bien" o "salió mal":

- **¿Se demoró?** Se calculó la diferencia entre cuántos días duró realmente el contrato y cuántos días se habían pactado al firmarlo.
- **¿Costó más de lo previsto?** Se calculó la diferencia entre lo que se pagó y lo que se había contratado, como un porcentaje.
- **¿Se entregó completo?** Se clasificó cada contrato en tres categorías: entregado completo, entregado a medias, o no entregado — según si tuvo una terminación anticipada, una suspensión o un cambio de contratista en el camino.

Estas tres fórmulas se construyeron leyendo únicamente la definición que aparece en el anteproyecto de este trabajo, sin mirar ni copiar en ningún momento cómo lo calcula el proyecto del compañero de tesis (que tiene un propósito distinto: predecir, no describir).

**Por qué importa**

Sin estos tres indicadores, no habría nada concreto que graficar, comparar entre modalidades, ni poner a prueba en las hipótesis. Es el resultado más importante de todo el trabajo descriptivo.
