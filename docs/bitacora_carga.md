# Bitacora de carga

Generada el 2026-09-18 08:56 por `src/cargar_base.py`, sobre la base `presupuesto_nlq`.

La carga ocurre en una sola transaccion y termina con una validacion: los conteos y los totales por etapa de cada ejercicio se comparan contra el archivo de origen al peso. Si algo no coincide, la transaccion se revierte completa. Que exista esta bitacora significa que la validacion paso.

## Dimensiones conformadas

| Tabla | Filas |
|---|---:|
| `dim_ramo` | 50 |
| `dim_unidad_responsable` | 1,926 |
| `dim_finalidad` | 4 |
| `dim_funcion` | 28 |
| `dim_subfuncion` | 91 |
| `dim_actividad_institucional` | 375 |
| `dim_modalidad` | 23 |
| `dim_programa_presupuestario` | 901 |
| `dim_partida` | 459 |
| `dim_tipo_gasto` | 9 |
| `dim_fuente_financiamiento` | 6 |
| `dim_entidad_federativa` | 34 |
| `descripcion_historica` | 18,724 |

## Claves con mas de un nombre dentro del mismo ejercicio

Defecto del dato de origen: aparece en los dos formatos publicados. La dimension conformada toma el nombre del ejercicio mas reciente y, si ahi tambien hay varios, el mas usado. Todas las variantes quedan en `descripcion_historica` con su numero de renglones.

| Dimension | Ejercicio | Claves afectadas |
|---|---|---:|
| `dim_partida` | 2021 | 25 |

## Hechos cargados y validados

| Ejercicio | Renglones | Aprobado (MDP) | Devengado (MDP) | Pagado (MDP) |
|---|---:|---:|---:|---:|
| 2020 | 223,966 | 6,953,750.3 | 6,941,079.4 | 6,856,091.6 |
| 2021 | 215,553 | 7,230,920.9 | 7,691,856.4 | 7,662,162.0 |
| 2022 | 220,508 | 8,111,725.1 | 8,661,883.7 | 8,624,738.3 |
| 2023 | 209,733 | 9,465,847.7 | 9,425,316.9 | 9,315,241.0 |
| 2024 | 205,015 | 10,406,689.0 | 10,555,267.3 | 10,506,472.4 |
| 2025 | 210,458 | 10,795,085.1 | 11,276,211.2 | 11,091,126.6 |
| **Total** | **1,285,233** | | | |

Archivos de origen: `hechos_2020.csv`, `hechos_2021.csv`, `hechos_2022.csv`, `hechos_2023.csv`, `hechos_2024.csv`, `hechos_2025.csv`.

Duracion: 148 segundos.
