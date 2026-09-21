# Contexto para el modelo

Textos que el sistema entrega al modelo de lenguaje junto con la pregunta. Forman parte de la capa semántica y son objeto de evaluación: cambiar una línea de estos archivos puede cambiar la exactitud medida, por lo que se versionan igual que el código y cada ejecución experimental registra la versión que usó.

| Archivo | Uso |
|---|---|
| `clasificaciones.md` | Documentación de clasificaciones y reglas de interpretación. Se incluye en la configuración 2 y en las siguientes. |

Lo que recibe el modelo en cada configuración:

| Configuración | Esquema | Comentarios de tablas y columnas | `clasificaciones.md` |
|---|---|---|---|
| 1a | `crudo` | no | no |
| 1b | `semantica` | no | no |
| 2, 3 y 4 | `semantica` | sí | sí |

La configuración 1 recibe solo nombres y tipos de columnas. Los comentarios de la base (`COMMENT ON` en `src/sql/02_semantica.sql`) son documentación, y por eso se entregan a partir de la configuración 2: así la diferencia entre 1b y 2 mide exactamente la aportación de la documentación.

## Criterios de redacción

- Solo se afirma lo que se comprobó en la base o en una fuente oficial. La tabla de procedencia, abajo, registra de dónde sale cada regla.
- Las reglas se escriben en términos generales, no como respuestas a preguntas concretas. No se incluyen cifras que respondan preguntas del conjunto de evaluación.
- El texto describe los datos y su interpretación; no da instrucciones de formato de salida, que pertenecen al prompt de cada configuración.

## Riesgo de contaminación

Varias reglas se identificaron al construir el conjunto de evaluación: el autor de la documentación conocía preguntas que después medirán su efecto. Eso puede inflar la mejora de la configuración 2 sobre las preguntas escritas antes de la documentación.

Control: la versión 1 se congela el 2026-09-21. Las preguntas tienen fecha de alta, de modo que la mejora puede reportarse por separado para las preguntas anteriores y posteriores a esa fecha. Una diferencia marcada entre ambos grupos indicaría que la documentación se ajustó a las preguntas y no al dominio. Cualquier cambio posterior crea una nueva versión con su fecha, y no se modifica durante una serie de experimentos.

## Procedencia de las reglas

| Regla (sección) | Evidencia |
|---|---|
| Cobertura: 2020 a 2025, sin municipios ni saldos (1) | Estructura de la base; columnas de la fuente publicada. |
| Significado de las etapas (2) | Diccionario de datos de la Cuenta Pública 2025 y momentos contables del CONAC; **pendiente de citar la norma del CONAC en su fuente original**. |
| Correspondencia entre palabras y etapas (2) | Criterio del proyecto, el mismo de `eval/README.md`. |
| Subejercicio = modificado − devengado (2) | Estado analítico del ISSSTE en la Cuenta Pública 2024: la columna de subejercicio es esa diferencia en cada renglón. Cero en 32 de 44 ramos distintos de entidades en 2024. |
| Ejercido ≈ devengado fuera de los ramos 50 a 53 (2) | Consulta a la base: diferencia menor a 32 millones por año en el conjunto de esos ramos, 2020 a 2025. |
| Devengado mayor que modificado en ramos 50 a 53 (2) | Consulta a la base: ocurre en 2020, 2023 y 2025. |
| Unidad responsable y programa no únicos entre ramos (3, 5) | Consulta a la base: 211 claves de unidad responsable aparecen en más de un ramo en 2025; hasta 19 programas distintos por clave. |
| Ramos 19, 23, 24, 25 (3) | Programas y unidades responsables con mayor devengado en 2024. |
| Cambios de nombre de los ramos 9, 27 y 38 (3) | Tabla `presupuesto.descripcion_historica`. |
| IMSS-Bienestar en el ramo 47, caída del ramo 12 (3) | Consulta a la base: unidad `AYO` del ramo 47 desde 2023; aprobado del ramo 12 de 209,616.5 millones en 2023 a 96,990.0 en 2024. |
| Niveles funcionales: 4, 28 y 91 (4) | Consulta a la base. |
| Letras de modalidad (5) | Consulta a la base: cada letra corresponde a una sola modalidad. |
| Programas con dos claves en un ejercicio (5) | Consulta a la base, ramo 20 en 2020. |
| Capítulos y concepto 3600 (6) | Clasificador por Objeto del Gasto del CONAC, verificado en su fuente (`data/raw/PROCEDENCIA.md`). |
| Siglas de los fondos del ramo 33 (7) | Claves y siglas: consulta a la base. Nombres completos: Ley de Coordinación Fiscal; **pendiente de verificar en su fuente original**. |
| Valores geográficos que no son entidades; efecto sede (8) | Consulta a la base: la Ciudad de México concentra cerca del 40% del devengado de 2024; el gasto no distribuible, cerca del 11%. |
| Gasto bruto y neto (10) | Diferencia entre el gasto neto total del artículo 2 del Presupuesto de Egresos 2024, citado en una solicitud, y el aprobado bruto de la base. **Pendiente de verificar el decreto y la definición de gasto neto en su fuente original.** |
