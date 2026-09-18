# Bitacora de normalizacion de fuentes

Generada el 2026-09-17 por `src/normalizar_fuentes.py`.

Registra que se hizo con cada archivo publicado antes de cargarlo. Las correcciones sobre el dato original se aplican de forma declarada: corregir en silencio seria indistinguible de alterarlo.

## Formato elegido por ejercicio

La SHCP publica cada ejercicio en csv y en xlsx. No son equivalentes.

| Ejercicio | Archivo de origen | Formato | Motivo |
|---|---|---|---|
| 2020 | `cuenta_publica_2020_gf_ecd_epe.xlsx` | xlsx | el csv publicado pierde 10 renglones |
| 2021 | `cuenta_publica_2021_gf_ecd_epe.xlsx` | xlsx | el csv publicado pierde 2 renglones y deja importes en blanco |
| 2022 | `cuenta_publica_2022_gf_ecd_epe.xlsx` | xlsx | el csv publicado pierde 3 renglones y trae 828,067 de relleno |
| 2023 | `cuenta_publica_2023_gf_ecd_epe.xlsx` | xlsx | el csv publicado pierde 1 renglon y corrompe una llave |
| 2024 | `cuenta_publica_2024_gf_ecd_epe.xlsx` | xlsx | el csv publicado reporta 9,699 MDP de mas en el ramo 51, cifra que no coincide con el informe oficial de Cuenta Publica |
| 2025 | `cuenta_publica_2025_gf_ecd_epe.csv` | csv | ambos formatos son identicos; el csv se lee mas rapido |

## Renglones procesados

| Ejercicio | Utiles | De relleno | Malformados | Salida | MB |
|---|---:|---:|---:|---|---:|
| 2020 | 223,966 | 0 | 0 | `hechos_2020.csv` | 114.1 |
| 2021 | 215,553 | 0 | 0 | `hechos_2021.csv` | 110.3 |
| 2022 | 220,508 | 828,067 | 0 | `hechos_2022.csv` | 113.1 |
| 2023 | 209,733 | 0 | 0 | `hechos_2023.csv` | 105.4 |
| 2024 | 205,015 | 0 | 0 | `hechos_2024.csv` | 103.8 |
| 2025 | 210,458 | 0 | 0 | `hechos_2025.csv` | 106.1 |

## Tratamiento de importes sin valor

Los ejercicios 2020 y 2021 dejan celdas de importe en blanco donde los demas escriben cero. En 2020 el vacio aparece en los dos formatos publicados, de modo que es caracteristica del dato de origen y no del proceso de exportacion.

**Decision:** el vacio se interpreta como cero. Las sumas por etapa coinciden con esa lectura y permite declarar las medidas como NOT NULL.

| Ejercicio | Celdas vacias convertidas a cero | Valores no numericos |
|---|---:|---:|
| 2020 | 507,822 | 0 |
| 2021 | 56,817 | 0 |
| 2022 | 0 | 0 |
| 2023 | 0 | 0 |
| 2024 | 0 | 0 |
| 2025 | 0 | 0 |

## Correcciones aplicadas sobre descripciones

| Ejercicio | Valor publicado | Corregido a | Renglones |
|---|---|---|---:|
| — | ninguna | — | 0 |

El error tipografico `Desarrollo SoSocial` detectado en 2024 aparece unicamente en el csv publicado. Al cargar desde xlsx no se presenta, y la correccion queda declarada por si la fuente cambia.

## Totales por medida despues de normalizar (millones de pesos)

| Ejercicio | Aprobado | Modificado | Devengado | Pagado | Adefas | Ejercido |
|---|---|---|---|---|---|---|
| 2020 | 6,953,750.3 | 6,884,192.0 | 6,941,079.4 | 6,856,091.6 | 22,253.5 | 6,882,475.7 |
| 2021 | 7,230,920.9 | 7,693,956.8 | 7,691,856.4 | 7,662,162.0 | 21,927.0 | 7,688,314.5 |
| 2022 | 8,111,725.1 | 8,672,141.8 | 8,661,883.7 | 8,624,738.3 | 40,405.6 | 8,669,765.6 |
| 2023 | 9,465,847.7 | 9,368,980.3 | 9,425,316.9 | 9,315,241.0 | 46,164.9 | 9,366,107.6 |
| 2024 | 10,406,689.0 | 10,559,409.9 | 10,555,267.3 | 10,506,472.4 | 43,877.2 | 10,554,159.3 |
| 2025 | 10,795,085.1 | 11,175,477.3 | 11,276,211.2 | 11,091,126.6 | 75,720.6 | 11,272,216.4 |

## Nomenclatura de origen por ejercicio

| Ejercicio | Primeras columnas tal como se publican |
|---|---|
| 2020 | `CICLO`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL`, `DESC_GPO_FUNCIONAL`, `ID_FUNCION` |
| 2021 | `CICLO`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL`, `DESC_GPO_FUNCIONAL`, `ID_FUNCION` |
| 2022 | `Ciclo`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL`, `DESC_GPO_FUNCIONAL`, `ID_FUNCION` |
| 2023 | `Ciclo`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL`, `DESC_GPO_FUNCIONAL`, `ID_FUNCION` |
| 2024 | `Ciclo`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL`, `DESC_GPO_FUNCIONAL`, `ID_FUNCION` |
| 2025 | `Ciclo`, `R`, `RAMO_DESC`, `UR`, `UR_DESC`, `FI`, `FIN_DESC`, `FU` |
