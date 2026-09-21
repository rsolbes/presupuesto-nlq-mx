# Conjunto de evaluación

Preguntas en español sobre el gasto público federal, con su respuesta de referencia verificada. Es el instrumento con el que se mide la exactitud del sistema: cada configuración experimental responde las mismas preguntas y su resultado se compara contra la referencia.

## Regla fundamental: las preguntas no las redacta un modelo de lenguaje

Un modelo tiende a formular las preguntas del modo en que a un modelo le resulta fácil interpretarlas. Un conjunto así mediría la capacidad del sistema de entender preguntas redactadas por sus semejantes, no las que haría una persona, y los resultados de exactitud quedarían sesgados al alza.

Por eso las preguntas provienen de **solicitudes de información reales**, en las palabras literales del ciudadano que las escribió. Cuando la pregunta viene rodeada de fórmulas legales o combinada con otras, se recorta el fragmento pertinente, pero no se reescribe ni se parafrasea. El texto completo de la solicitud queda disponible por su folio.

## Proceso y distribución de responsabilidades

El conjunto se construye con asistencia de un modelo de lenguaje (Claude, de Anthropic), con una división explícita de responsabilidades:

**Selección.** Aleatoria, con semilla fija, sobre las solicitudes que pasan un filtro de palabras clave documentado. No depende del criterio del asistente ni del autor.

**Propuesta, a cargo del asistente.** Recorta la pregunta literal, propone su comportamiento esperado y escribe el SQL de referencia. Toda pregunta entra con `estado: propuesta`.

**Verificación, a cargo del autor.** Revisa cada propuesta: que el recorte conserve el sentido de la solicitud, que el comportamiento esperado sea correcto, que el SQL responda lo que se pregunta, y que la respuesta coincida con una fuente independiente cuando la haya. Solo entonces cambia a `estado: verificada` y registra `verificado_por`.

**Solo las preguntas verificadas entran a los experimentos.** Una propuesta es una sugerencia pendiente de revisión, no una respuesta de referencia.

Este proceso se declara en la metodología de la tesis.

## Fuentes de preguntas

Toda pregunta registra su origen en el campo `origen`, de modo que cualquiera pueda rastrearla.

**Solicitudes de información** (`solicitud_pnt`). La sección de datos abiertos de la Plataforma Nacional de Transparencia publica las solicitudes que los ciudadanos dirigen a las dependencias. Son preguntas reales, en su redacción original, sobre lo que la gente efectivamente quiere saber. Es la fuente preferente, porque corresponde a la población que describe la metodología: preguntas que una persona sin formación técnica plantearía sobre el gasto público. Se registra el folio.

**Notas periodísticas** (`nota_periodistica`). Cifras de gasto citadas en prensa. Además de la pregunta, aportan una respuesta publicada contra la cual contrastar. Se registra la URL.

**Reportes oficiales** (`reporte_oficial`). Cifras que la propia SHCP publica en informes y visualizaciones. Permiten verificar la respuesta de forma independiente. Se registra el documento.

**Variantes** (`variante`). Reformulaciones de una pregunta existente con lenguaje coloquial, referencias temporales relativas ("el año pasado") o ambigüedad introducida a propósito. Se registra el `id` de la pregunta original. Las variantes también las redacta el autor.

## Recorte de ramos

La base contiene los 50 ramos de 2020 a 2025. La evaluación se concentra en un subconjunto, conforme a la sección de Alcances de la tesis.

**Criterio de selección:** PENDIENTE.

**Ramos seleccionados:** PENDIENTE.

Tres observaciones sobre los datos para tomar la decisión:

- El ramo 12, Salud, concentra apenas el 0.5% del gasto devengado en 2025. El gasto en salud fluye principalmente por el IMSS (ramo 50), el ISSSTE (ramo 51) y las aportaciones a entidades (ramo 33). Una pregunta sobre "el gasto en salud" se responde con la clasificación funcional, no con el ramo. Es una trampa de dominio que vale incluir.
- Los ramos 54 (Mujeres) y 55 (Agencia de Transformación Digital y Telecomunicaciones) solo existen en 2025. No sirven para comparaciones entre años, pero sí para preguntas no respondibles.
- Los ramos 28 (Participaciones) y 33 (Aportaciones) contienen las transferencias a entidades federativas y municipios. Son el vínculo con el caso local de Tamaulipas.

## Estructura de una pregunta

Las preguntas viven en `preguntas.yaml`, una lista de entradas con estos campos:

| Campo | Obligatorio | Contenido |
|---|---|---|
| `id` | siempre | `P0001`, `P0002`... Único y nunca se reutiliza. |
| `pregunta` | siempre | El texto tal como se formuló en la fuente, o tal como se redactó la variante. |
| `ruta` | siempre | `sql` o `documental`. La ruta a la que corresponde la pregunta, aunque no sea respondible. |
| `comportamiento` | siempre | `responder`, `ambigua` o `abstenerse`. Ver la sección siguiente. |
| `origen.tipo` | siempre | `solicitud_pnt`, `nota_periodistica`, `reporte_oficial`, `variante` u `otro`. |
| `origen.referencia` | siempre | Folio, URL, documento o `id` de la pregunta original. |
| `sql` | si es `responder` en ruta `sql` | Consulta de referencia sobre el esquema `semantica`. |
| `interpretaciones` | si es `ambigua` | Al menos dos, cada una con `supuesto` y `sql`. |
| `motivo` | si es `abstenerse` | Por qué la información disponible no permite responder. |
| `verificacion` | recomendado | `documento`, `ubicacion` y `valor`: la fuente independiente que confirma la respuesta. |
| `autor` | siempre | Quién propuso la entrada: `asistente-ia` o las iniciales del autor. |
| `estado` | siempre | `propuesta`, `verificada` o `descartada`. |
| `verificado_por` | si es `verificada` | Iniciales de quien la verificó. |
| `fecha` | recomendado | Fecha de redacción. |
| `notas` | opcional | Cualquier aclaración. |

## Comportamiento esperado

El sistema no siempre debe devolver un número. Cada pregunta declara qué respuesta se considera correcta.

**`responder`.** La pregunta tiene una única interpretación razonable y los datos la cubren. La respuesta correcta es el resultado del SQL de referencia.

**`ambigua`.** Admite más de una interpretación con respuestas distintas. El caso típico es la etapa del gasto: "cuánto se gastó" puede referirse al aprobado, al devengado o al pagado, y para 2025 la diferencia entre devengado y pagado supera los 185 mil millones de pesos. El comportamiento correcto es advertir la ambigüedad, o responder declarando explícitamente el supuesto. Cada interpretación lleva su propio SQL.

**`abstenerse`.** La información disponible no permite responder: un ejercicio que no está en la base, una dependencia que no existía ese año, un nivel de detalle que los datos no tienen, una pregunta sobre gasto municipal. El comportamiento correcto es reconocerlo en lugar de inventar una respuesta. Estas preguntas miden la capacidad de abstención, que es la quinta pregunta de investigación.

## Criterios de lectura

Reglas con que se clasifica cada solicitud y se escribe su SQL de referencia. Son las que el autor verifica en cada propuesta.

**Inclusión.** Se incluye una solicitud si pide una cifra monetaria o una clasificación de las finanzas públicas. Se descarta si pide documentos, plazas, nóminas o tabuladores individuales, datos de contratos, o si es una queja o una pregunta de política sin cifra. Toda decisión, incluida la de descartar, queda en `revision_candidatas.csv` con su motivo.

**Lectura literal.** La pregunta se evalúa tal como la recibiría el sistema, sin el contexto de la solicitud. Una solicitud dirigida a la SHCP que dice "los vehículos oficiales" no se lee como "los vehículos de la SHCP": el sistema no sabe a quién iba dirigida.

**Cobertura.** Si la pregunta es de finanzas públicas pero la base no la cubre (ejercicios fuera de 2020 a 2025, detalle municipal o por proyecto, ingresos, fideicomisos, reintegros), el comportamiento esperado es `abstenerse`.

**Etapa del gasto.** Las palabras del ciudadano se traducen a etapas así:

| Palabras en la pregunta | Etapa |
|---|---|
| asignado, autorizado, aprobado, presupuestado, destinado, previsto | `aprobado` |
| modificado | `modificado` |
| ejercido, ejecutado | `ejercido` |
| devengado | `devengado` |
| pagado, entregado, transferido, proporcionado, dispersado | `pagado` |
| gasto, gastado, erogado, costó, sin etapa identificable | ambigua |

**Subejercicio.** Se calcula como `modificado - devengado`. Es la definición que usa la Cuenta Pública: en el estado analítico del ISSSTE 2024, la columna de subejercicio es exactamente esa diferencia en cada renglón.

**Ejercicio no indicado.** Si la pregunta no dice de qué año, es ambigua; las interpretaciones declaran el supuesto, normalmente el ejercicio más reciente disponible.

**Casi duplicados.** Las candidatas se agrupan por similitud de vocabulario (ver `experiments/salidas/solicitudes_pnt.md`). De cada grupo solo se evalúa el primer miembro que aparece en el orden aleatorio; los demás se registran como casi duplicados de él. Así una campaña de cientos de solicitudes con la misma plantilla aporta una sola pregunta, igual que cualquier otra.

**Ruta documental.** Una pregunta sobre procedimientos, reglas o definiciones —cómo se determina, qué establece la norma— corresponde a la ruta `documental`, aunque trate de presupuesto. Su respuesta de referencia se fijará al construir el corpus documental.

## Dificultad

La dificultad no la asigna el autor: se deriva del SQL de referencia por regla. Así la estratificación es reproducible, y no puede objetarse que se clasificaron como difíciles las preguntas que convenía.

`experiments/validar_conjunto.py` analiza el árbol sintáctico de cada consulta y suma puntos por componente:

| Componente | Puntos |
|---|---:|
| Cada condición en `WHERE` o `HAVING` | 1 |
| `GROUP BY` | 2 |
| `HAVING` | 1 |
| `ORDER BY` con `LIMIT` | 1 |
| Cada `JOIN` | 2 |
| Cada subconsulta o CTE | 3 |
| Cada función de ventana | 3 |
| `UNION`, `INTERSECT`, `EXCEPT` | 3 |
| Cada división | 2 |
| Cada `CASE` | 1 |
| Comparación entre ejercicios | 2 |

**Baja:** menos de 4 puntos. **Media:** de 4 a 6. **Alta:** 7 o más. Una pregunta ambigua se clasifica por su interpretación más difícil.

La regla se fijó antes de redactar la primera pregunta y no se modifica una vez iniciados los experimentos: ajustarla después de ver resultados sería acomodar la medición a lo medido.

La dificultad se mide sobre la capa semántica. La misma pregunta resulta más difícil sobre el esquema `crudo`, y esa diferencia es lo que mide la configuración 1a.

## Metas de estratificación

Propuesta sujeta a revisión antes de iniciar los experimentos:

- **Total:** entre 200 y 300 preguntas.
- **Por comportamiento:** 70% `responder`, 15% `ambigua`, 15% `abstenerse`.
- **Por dificultad**, entre las de `responder`: 30% baja, 40% media, 30% alta.

El informe del validador reporta el avance contra estas metas.

## Flujo de trabajo

1. Redactar la pregunta en `preguntas.yaml`, con su origen.
2. Escribir el SQL de referencia y probarlo en DataGrip como `consulta_nlq`.
3. Validar la estructura sin tocar la base:

   ```bash
   .venv/Scripts/python.exe experiments/validar_conjunto.py --sin-base
   ```

4. Ejecutar para obtener la respuesta de referencia:

   ```bash
   .venv/Scripts/python.exe experiments/validar_conjunto.py
   ```

5. Contrastar la respuesta contra una fuente independiente y registrarla en `verificacion`.
6. Commit de `preguntas.yaml` y `respuestas_referencia.json`.

## Respuestas de referencia

`respuestas_referencia.json` guarda el resultado de cada SQL de referencia, ejecutado como `consulta_nlq`: columnas, filas, número de filas y tiempo. Es contra lo que se medirá la exactitud de ejecución.

Cada respuesta lleva la huella de su SQL. Si el SQL de una pregunta cambia, su huella deja de coincidir y la respuesta debe regenerarse.
