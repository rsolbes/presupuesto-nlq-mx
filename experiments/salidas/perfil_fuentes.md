# Perfilado de las fuentes crudas - Cuenta Publica (SHCP)

Generado el 2026-09-17 por `experiments/perfilado_fuentes.py`.

## 1. Huella de cada archivo

| Archivo | MB | sha256 (16) | Codificacion | Cols. declaradas | Cols. con nombre |
|---|---:|---|---|---:|---:|
| cuenta_publica_2020_gf_ecd_epe.csv | 106.6 | `4366e7e1be1f70bb` | latin-1 | 32 | 32 |
| cuenta_publica_2021_gf_ecd_epe.csv | 112.2 | `617a6e4aac9b1297` | latin-1 | 32 | 32 |
| cuenta_publica_2022_gf_ecd_epe.csv | 326.0 | `59e4e5158f199968` | latin-1 | 212 | 32 |
| cuenta_publica_2022_gf_ecd_epe_desde_xlsx.csv | 107.8 | `d35b722f50712d6f` | latin-1 | 32 | 32 |
| cuenta_publica_2023_gf_ecd_epe.csv | 100.9 | `1c58da6166e1a97c` | latin-1 | 32 | 32 |
| cuenta_publica_2024_gf_ecd_epe.csv | 104.7 | `97fe8043a84801d1` | latin-1 | 32 | 32 |
| cuenta_publica_2025_gf_ecd_epe.csv | 105.6 | `973aab21969233bd` | latin-1 | 32 | 32 |

## 2. Renglones

| Archivo | Utiles | De relleno | Malformados |
|---|---:|---:|---:|
| cuenta_publica_2020_gf_ecd_epe.csv | 223,956 | 0 | 6 |
| cuenta_publica_2021_gf_ecd_epe.csv | 215,551 | 0 | 2 |
| cuenta_publica_2022_gf_ecd_epe.csv | 220,505 | 828,067 | 4 |
| cuenta_publica_2022_gf_ecd_epe_desde_xlsx.csv | 220,508 | 0 | 0 |
| cuenta_publica_2023_gf_ecd_epe.csv | 209,732 | 0 | 3 |
| cuenta_publica_2024_gf_ecd_epe.csv | 205,012 | 0 | 3 |
| cuenta_publica_2025_gf_ecd_epe.csv | 210,458 | 0 | 0 |

## 3. Mapa canonico de columnas

Cada ejercicio publica la misma informacion con nombres distintos. El mapeo es posicional y se valida contra los nombres conocidos.

| Canonico | 2020 | 2021 | 2022 | 2022_desde_xlsx | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| `ciclo` | CICLO | CICLO | Ciclo | Ciclo | Ciclo | Ciclo | Ciclo |
| `ramo_id` | ID_RAMO | ID_RAMO | ID_RAMO | ID_RAMO | ID_RAMO | ID_RAMO | R |
| `ramo_desc` | DESC_RAMO | DESC_RAMO | DESC_RAMO | DESC_RAMO | DESC_RAMO | DESC_RAMO | RAMO_DESC |
| `ur_id` | ID_UR | ID_UR | ID_UR | ID_UR | ID_UR | ID_UR | UR |
| `ur_desc` | DESC_UR | DESC_UR | DESC_UR | DESC_UR | DESC_UR | DESC_UR | UR_DESC |
| `finalidad_id` | GPO_FUNCIONAL | GPO_FUNCIONAL | GPO_FUNCIONAL | GPO_FUNCIONAL | GPO_FUNCIONAL | GPO_FUNCIONAL | FI |
| `finalidad_desc` | DESC_GPO_FUNCIONAL | DESC_GPO_FUNCIONAL | DESC_GPO_FUNCIONAL | DESC_GPO_FUNCIONAL | DESC_GPO_FUNCIONAL | DESC_GPO_FUNCIONAL | FIN_DESC |
| `funcion_id` | ID_FUNCION | ID_FUNCION | ID_FUNCION | ID_FUNCION | ID_FUNCION | ID_FUNCION | FU |
| `funcion_desc` | DESC_FUNCION | DESC_FUNCION | DESC_FUNCION | DESC_FUNCION | DESC_FUNCION | DESC_FUNCION | FUN_DESC |
| `subfuncion_id` | ID_SUBFUNCION | ID_SUBFUNCION | ID_SUBFUNCION | ID_SUBFUNCION | ID_SUBFUNCION | ID_SUBFUNCION | SF |
| `subfuncion_desc` | DESC_SUBFUNCION | DESC_SUBFUNCION | DESC_SUBFUNCION | DESC_SUBFUNCION | DESC_SUBFUNCION | DESC_SUBFUNCION | SF_DESC |
| `ai_id` | ID_AI | ID_AI | ID_AI | ID_AI | ID_AI | ID_AI | AI |
| `ai_desc` | DESC_AI | DESC_AI | DESC_AI | DESC_AI | DESC_AI | DESC_AI | AI_DESC |
| `modalidad_id` | ID_MODALIDAD | ID_MODALIDAD | ID_MODALIDAD | ID_MODALIDAD | ID_MODALIDAD | ID_MODALIDAD | MOD |
| `modalidad_desc` | DESC_MODALIDAD | DESC_MODALIDAD | DESC_MODALIDAD | DESC_MODALIDAD | DESC_MODALIDAD | DESC_MODALIDAD | MOD_DESC |
| `pp_id` | ID_PP | ID_PP | ID_PP | ID_PP | ID_PP | ID_PP | PP |
| `pp_desc` | DESC_PP | DESC_PP | DESC_PP | DESC_PP | DESC_PP | DESC_PP | PP_DESC |
| `partida_id` | ID_OBJETO_DEL_GASTO | ID_OBJETO_DEL_GASTO | ID_OBJETO_DEL_GASTO | ID_OBJETO_DEL_GASTO | ID_OBJETO_DEL_GASTO | ID_OBJETO_DEL_GASTO | PTDA |
| `partida_desc` | DESC_OBJETO_DEL_GASTO | DESC_OBJETO_DEL_GASTO | DESC_OBJETO_DEL_GASTO | DESC_OBJETO_DEL_GASTO | DESC_OBJETO_DEL_GASTO | DESC_OBJETO_DEL_GASTO | PTDA_DESC |
| `tipogasto_id` | ID_TIPOGASTO | ID_TIPOGASTO | ID_TIPOGASTO | ID_TIPOGASTO | ID_TIPOGASTO | ID_TIPOGASTO | TG |
| `tipogasto_desc` | DESC_TIPOGASTO | DESC_TIPOGASTO | DESC_TIPOGASTO | DESC_TIPOGASTO | DESC_TIPOGASTO | DESC_TIPOGASTO | TG_DESC |
| `ff_id` | ID_FF | ID_FF | ID_FF | ID_FF | ID_FF | ID_FF | FF |
| `ff_desc` | DESC_FF | DESC_FF | DESC_FF | DESC_FF | DESC_FF | DESC_FF | FF_DESC |
| `entidad_id` | ID_ENTIDAD_FEDERATIVA | ID_ENTIDAD_FEDERATIVA | ID_ENTIDAD_FEDERATIVA | ID_ENTIDAD_FEDERATIVA | ID_ENTIDAD_FEDERATIVA | ID_ENTIDAD_FEDERATIVA | EF |
| `entidad_desc` | ENTIDAD_FEDERATIVA | ENTIDAD_FEDERATIVA | ENTIDAD_FEDERATIVA | ENTIDAD_FEDERATIVA | ENTIDAD_FEDERATIVA | ENTIDAD_FEDERATIVA | EF_DESC |
| `cartera_id` | ID_CLAVE_CARTERA | ID_CLAVE_CARTERA | ID_CLAVE_CARTERA | ID_CLAVE_CARTERA | ID_CLAVE_CARTERA | ID_CLAVE_CARTERA | PPI |
| `aprobado` | MONTO_APROBADO | MONTO_APROBADO | MONTO_APROBADO | MONTO_APROBADO | MONTO_APROBADO | MONTO_APROBADO | Original_Bruto |
| `modificado` | MONTO_MODIFICADO | MONTO_MODIFICADO | MONTO_MODIFICADO | MONTO_MODIFICADO | MONTO_MODIFICADO | MONTO_MODIFICADO | Modificado_Bruto |
| `devengado` | MONTO_DEVENGADO | MONTO_DEVENGADO | MONTO_DEVENGADO | MONTO_DEVENGADO | MONTO_DEVENGADO | MONTO_DEVENGADO | Devengado |
| `pagado` | MONTO_PAGADO | MONTO_PAGADO | MONTO_PAGADO | MONTO_PAGADO | MONTO_PAGADO | MONTO_PAGADO | Pagado |
| `adefas` | ADEFAS | ADEFAS | ADEFAS | ADEFAS | ADEFAS | ADEFAS | Adefas |
| `ejercido` | EJERCICIO | EJERCICIO | EJERCICIO | EJERCICIO | EJERCICIO | MONTO_EJERCIDO | Ejercido_Bruto |

Todos los encabezados corresponden a variantes ya conocidas.

## 4. Totales por medida (millones de pesos)

| Archivo | Aprobado | Modificado | Devengado | Pagado | Adefas | Ejercido |
|---|---|---|---|---|---|---|
| cuenta_publica_2020_gf_ecd_epe.csv | 6,953,704.4 | 6,884,157.3 | 6,941,045.7 | 6,856,057.7 | 22,253.5 | 6,882,441.7 |
| cuenta_publica_2021_gf_ecd_epe.csv | 7,230,923.7 | 7,693,958.6 | 7,691,858.2 | 7,662,163.8 | 21,927.0 | 7,688,316.3 |
| cuenta_publica_2022_gf_ecd_epe.csv | 8,111,715.9 | 8,672,133.9 | 8,661,875.9 | 8,624,730.5 | 40,405.6 | 8,669,757.8 |
| cuenta_publica_2022_gf_ecd_epe_desde_xlsx.csv | 8,111,725.1 | 8,672,141.8 | 8,661,883.7 | 8,624,738.3 | 40,405.6 | 8,669,765.6 |
| cuenta_publica_2023_gf_ecd_epe.csv | 9,465,846.4 | 9,368,978.0 | 9,425,314.3 | 9,315,238.1 | 46,164.9 | 9,366,104.6 |
| cuenta_publica_2024_gf_ecd_epe.csv | 10,412,919.2 | 10,569,107.2 | 10,564,964.6 | 10,516,169.7 | 43,877.2 | 10,563,856.6 |
| cuenta_publica_2025_gf_ecd_epe.csv | 10,795,085.1 | 11,175,477.3 | 11,276,211.2 | 11,091,126.6 | 75,720.6 | 11,272,216.4 |

**Valores no numericos en columnas de importe:**

- `cuenta_publica_2020_gf_ecd_epe.csv` / `aprobado`: 59,478 valores
- `cuenta_publica_2020_gf_ecd_epe.csv` / `modificado`: 57,066 valores
- `cuenta_publica_2020_gf_ecd_epe.csv` / `devengado`: 58,061 valores
- `cuenta_publica_2020_gf_ecd_epe.csv` / `pagado`: 58,573 valores
- `cuenta_publica_2020_gf_ecd_epe.csv` / `adefas`: 216,770 valores
- `cuenta_publica_2020_gf_ecd_epe.csv` / `ejercido`: 57,853 valores
- `cuenta_publica_2021_gf_ecd_epe.csv` / `aprobado`: 56,723 valores
- `cuenta_publica_2021_gf_ecd_epe.csv` / `modificado`: 38,078 valores
- `cuenta_publica_2021_gf_ecd_epe.csv` / `devengado`: 49,376 valores
- `cuenta_publica_2021_gf_ecd_epe.csv` / `pagado`: 49,940 valores
- `cuenta_publica_2021_gf_ecd_epe.csv` / `adefas`: 207,653 valores
- `cuenta_publica_2021_gf_ecd_epe.csv` / `ejercido`: 49,333 valores

## 5. Llaves naturales

`max_desc` es el mayor numero de descripciones distintas asociadas a una misma llave. Debe ser 1: si es mayor, esa columna no identifica por si sola y la llave tiene que componerse.

### cuenta_publica_2020_gf_ecd_epe.csv

| Llave | Grupos | max_desc | Veredicto |
|---|---:|---:|---|
| `ramo_id` | 48 | 1 | unica |
| `finalidad_id` | 4 | 1 | unica |
| `modalidad_id` | 22 | 1 | unica |
| `partida_id` | 435 | 1 | unica |
| `tipogasto_id` | 9 | 1 | unica |
| `ff_id` | 5 | 1 | unica |
| `entidad_id` | 34 | 1 | unica |
| `ramo_id+ur_id` | 1,473 | 1 | unica |
| `finalidad_id+funcion_id` | 28 | 1 | unica |
| `finalidad_id+funcion_id+subfuncion_id` | 91 | 1 | unica |
| `ramo_id+ai_id` | 332 | 1 | unica |
| `ramo_id+modalidad_id+pp_id` | 746 | 1 | unica |

### cuenta_publica_2021_gf_ecd_epe.csv

| Llave | Grupos | max_desc | Veredicto |
|---|---:|---:|---|
| `ramo_id` | 48 | 1 | unica |
| `finalidad_id` | 4 | 1 | unica |
| `modalidad_id` | 22 | 1 | unica |
| `partida_id` | 437 | 3 | AMBIGUA |
| `tipogasto_id` | 8 | 1 | unica |
| `ff_id` | 4 | 1 | unica |
| `entidad_id` | 34 | 1 | unica |
| `ramo_id+ur_id` | 1,377 | 1 | unica |
| `finalidad_id+funcion_id` | 28 | 1 | unica |
| `finalidad_id+funcion_id+subfuncion_id` | 90 | 1 | unica |
| `ramo_id+ai_id` | 330 | 1 | unica |
| `ramo_id+modalidad_id+pp_id` | 700 | 1 | unica |

### cuenta_publica_2022_gf_ecd_epe.csv

| Llave | Grupos | max_desc | Veredicto |
|---|---:|---:|---|
| `ramo_id` | 48 | 1 | unica |
| `finalidad_id` | 4 | 1 | unica |
| `modalidad_id` | 22 | 1 | unica |
| `partida_id` | 435 | 1 | unica |
| `tipogasto_id` | 8 | 1 | unica |
| `ff_id` | 4 | 1 | unica |
| `entidad_id` | 34 | 1 | unica |
| `ramo_id+ur_id` | 1,348 | 1 | unica |
| `finalidad_id+funcion_id` | 28 | 1 | unica |
| `finalidad_id+funcion_id+subfuncion_id` | 90 | 1 | unica |
| `ramo_id+ai_id` | 331 | 1 | unica |
| `ramo_id+modalidad_id+pp_id` | 710 | 1 | unica |

### cuenta_publica_2022_gf_ecd_epe_desde_xlsx.csv

| Llave | Grupos | max_desc | Veredicto |
|---|---:|---:|---|
| `ramo_id` | 48 | 1 | unica |
| `finalidad_id` | 4 | 1 | unica |
| `modalidad_id` | 22 | 1 | unica |
| `partida_id` | 435 | 1 | unica |
| `tipogasto_id` | 8 | 1 | unica |
| `ff_id` | 4 | 1 | unica |
| `entidad_id` | 34 | 1 | unica |
| `ramo_id+ur_id` | 1,348 | 1 | unica |
| `finalidad_id+funcion_id` | 28 | 1 | unica |
| `finalidad_id+funcion_id+subfuncion_id` | 90 | 1 | unica |
| `ramo_id+ai_id` | 331 | 1 | unica |
| `ramo_id+modalidad_id+pp_id` | 710 | 1 | unica |

### cuenta_publica_2023_gf_ecd_epe.csv

| Llave | Grupos | max_desc | Veredicto |
|---|---:|---:|---|
| `ramo_id` | 48 | 1 | unica |
| `finalidad_id` | 4 | 1 | unica |
| `modalidad_id` | 22 | 1 | unica |
| `partida_id` | 441 | 1 | unica |
| `tipogasto_id` | 8 | 1 | unica |
| `ff_id` | 4 | 1 | unica |
| `entidad_id` | 34 | 1 | unica |
| `ramo_id+ur_id` | 1,321 | 1 | unica |
| `finalidad_id+funcion_id` | 28 | 1 | unica |
| `finalidad_id+funcion_id+subfuncion_id` | 89 | 2 | AMBIGUA |
| `ramo_id+ai_id` | 338 | 1 | unica |
| `ramo_id+modalidad_id+pp_id` | 726 | 1 | unica |

### cuenta_publica_2024_gf_ecd_epe.csv

| Llave | Grupos | max_desc | Veredicto |
|---|---:|---:|---|
| `ramo_id` | 48 | 1 | unica |
| `finalidad_id` | 4 | 2 | AMBIGUA |
| `modalidad_id` | 23 | 1 | unica |
| `partida_id` | 442 | 1 | unica |
| `tipogasto_id` | 8 | 1 | unica |
| `ff_id` | 4 | 1 | unica |
| `entidad_id` | 34 | 1 | unica |
| `ramo_id+ur_id` | 1,303 | 1 | unica |
| `finalidad_id+funcion_id` | 28 | 1 | unica |
| `finalidad_id+funcion_id+subfuncion_id` | 89 | 1 | unica |
| `ramo_id+ai_id` | 339 | 1 | unica |
| `ramo_id+modalidad_id+pp_id` | 724 | 1 | unica |

### cuenta_publica_2025_gf_ecd_epe.csv

| Llave | Grupos | max_desc | Veredicto |
|---|---:|---:|---|
| `ramo_id` | 50 | 1 | unica |
| `finalidad_id` | 4 | 1 | unica |
| `modalidad_id` | 23 | 1 | unica |
| `partida_id` | 438 | 1 | unica |
| `tipogasto_id` | 9 | 1 | unica |
| `ff_id` | 5 | 1 | unica |
| `entidad_id` | 34 | 1 | unica |
| `ramo_id+ur_id` | 1,464 | 1 | unica |
| `finalidad_id+funcion_id` | 28 | 1 | unica |
| `finalidad_id+funcion_id+subfuncion_id` | 88 | 1 | unica |
| `ramo_id+ai_id` | 348 | 1 | unica |
| `ramo_id+modalidad_id+pp_id` | 726 | 1 | unica |

## 6. Cardinalidad de las columnas de clave

| Archivo | `ciclo` | `ramo_id` | `ur_id` | `finalidad_id` | `funcion_id` | `subfuncion_id` | `ai_id` | `modalidad_id` | `pp_id` | `partida_id` | `tipogasto_id` | `ff_id` | `entidad_id` | `cartera_id` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cuenta_publica_2020_gf_ecd_epe.csv | 1 | 48 | 486 | 4 | 9 | 9 | 42 | 22 | 145 | 435 | 9 | 5 | 34 | 936 |
| cuenta_publica_2021_gf_ecd_epe.csv | 1 | 48 | 470 | 4 | 9 | 9 | 42 | 22 | 130 | 437 | 8 | 4 | 34 | 1111 |
| cuenta_publica_2022_gf_ecd_epe.csv | 1 | 48 | 463 | 4 | 9 | 9 | 39 | 22 | 127 | 435 | 8 | 4 | 34 | 1247 |
| cuenta_publica_2022_gf_ecd_epe_desde_xlsx.csv | 1 | 48 | 463 | 4 | 9 | 9 | 39 | 22 | 127 | 435 | 8 | 4 | 34 | 1247 |
| cuenta_publica_2023_gf_ecd_epe.csv | 1 | 48 | 475 | 4 | 9 | 9 | 41 | 22 | 128 | 441 | 8 | 4 | 34 | 1328 |
| cuenta_publica_2024_gf_ecd_epe.csv | 1 | 48 | 501 | 4 | 9 | 9 | 41 | 23 | 130 | 442 | 8 | 4 | 34 | 1289 |
| cuenta_publica_2025_gf_ecd_epe.csv | 1 | 50 | 531 | 4 | 9 | 9 | 40 | 23 | 129 | 438 | 9 | 5 | 34 | 1315 |
