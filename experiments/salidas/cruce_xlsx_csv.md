# Cruce entre CSV y XLSX publicados - Cuenta Publica (SHCP)

Generado el 2026-09-17 por `experiments/cruce_xlsx_csv.py`.

Un xlsx no puede presentar renglones malformados: el defecto de escapado es exclusivo del texto delimitado. La comparacion util es si el CSV publicado pierde informacion frente al xlsx del mismo ejercicio.

## 1. Renglones utiles

| Ejercicio | CSV | XLSX | Diferencia | Malformados en CSV |
|---|---:|---:|---:|---:|
| 2020 | 223,956 | 223,966 | -10 | 6 |
| 2021 | 215,551 | 215,553 | -2 | 2 |
| 2022 | 220,505 | 220,508 | -3 | 4 |
| 2023 | 209,732 | 209,733 | -1 | 3 |
| 2024 | 205,012 | 205,015 | -3 | 3 |
| 2025 | 210,458 | falta | - | - |

## 2. Totales por medida (millones de pesos)


### Ejercicio 2020

| Medida | CSV | XLSX | Diferencia | Coincide |
|---|---:|---:|---:|---|
| aprobado | 6,953,704.4 | 6,953,750.3 | -45.9 | NO |
| modificado | 6,884,157.3 | 6,884,192.0 | -34.7 | NO |
| devengado | 6,941,045.7 | 6,941,079.4 | -33.6 | NO |
| pagado | 6,856,057.7 | 6,856,091.6 | -34.0 | NO |
| adefas | 22,253.5 | 22,253.5 | +0.0 | si |
| ejercido | 6,882,441.7 | 6,882,475.7 | -34.0 | NO |

### Ejercicio 2021

| Medida | CSV | XLSX | Diferencia | Coincide |
|---|---:|---:|---:|---|
| aprobado | 7,230,923.7 | 7,230,920.9 | +2.8 | NO |
| modificado | 7,693,958.6 | 7,693,956.8 | +1.8 | NO |
| devengado | 7,691,858.2 | 7,691,856.4 | +1.8 | NO |
| pagado | 7,662,163.8 | 7,662,162.0 | +1.8 | NO |
| adefas | 21,927.0 | 21,927.0 | +0.0 | si |
| ejercido | 7,688,316.3 | 7,688,314.5 | +1.8 | NO |

### Ejercicio 2022

| Medida | CSV | XLSX | Diferencia | Coincide |
|---|---:|---:|---:|---|
| aprobado | 8,111,715.9 | 8,111,725.1 | -9.2 | NO |
| modificado | 8,672,133.9 | 8,672,141.8 | -7.8 | NO |
| devengado | 8,661,875.9 | 8,661,883.7 | -7.8 | NO |
| pagado | 8,624,730.5 | 8,624,738.3 | -7.8 | NO |
| adefas | 40,405.6 | 40,405.6 | +0.0 | si |
| ejercido | 8,669,757.8 | 8,669,765.6 | -7.8 | NO |

### Ejercicio 2023

| Medida | CSV | XLSX | Diferencia | Coincide |
|---|---:|---:|---:|---|
| aprobado | 9,465,846.4 | 9,465,847.7 | -1.4 | NO |
| modificado | 9,368,978.0 | 9,368,980.3 | -2.3 | NO |
| devengado | 9,425,314.3 | 9,425,316.9 | -2.5 | NO |
| pagado | 9,315,238.1 | 9,315,241.0 | -3.0 | NO |
| adefas | 46,164.9 | 46,164.9 | +0.0 | si |
| ejercido | 9,366,104.6 | 9,366,107.6 | -3.0 | NO |

### Ejercicio 2024

| Medida | CSV | XLSX | Diferencia | Coincide |
|---|---:|---:|---:|---|
| aprobado | 10,412,919.2 | 10,406,689.0 | +6,230.2 | NO |
| modificado | 10,569,107.2 | 10,559,409.9 | +9,697.3 | NO |
| devengado | 10,564,964.6 | 10,555,267.3 | +9,697.3 | NO |
| pagado | 10,516,169.7 | 10,506,472.4 | +9,697.3 | NO |
| adefas | 43,877.2 | 43,877.2 | +0.0 | si |
| ejercido | 10,563,856.6 | 10,554,159.3 | +9,697.3 | NO |

## 3. Celdas de importe sin valor

| Ejercicio | Formato | aprobado | modificado | devengado | pagado | adefas | ejercido |
|---|---|---|---|---|---|---|---|
| 2020 | csv | 59,478 | 57,066 | 58,061 | 58,573 | 216,770 | 57,853 |
| 2020 | xlsx | 59,473 | 57,070 | 58,065 | 58,577 | 216,780 | 57,857 |
| 2021 | csv | 56,723 | 38,078 | 49,376 | 49,940 | 207,653 | 49,333 |
| 2021 | xlsx | 56,497 | 64 | 64 | 64 | 64 | 64 |
| 2022 | csv | 0 | 0 | 0 | 0 | 0 | 0 |
| 2022 | xlsx | 0 | 0 | 0 | 0 | 0 | 0 |
| 2023 | csv | 0 | 0 | 0 | 0 | 0 | 0 |
| 2023 | xlsx | 0 | 0 | 0 | 0 | 0 | 0 |
| 2024 | csv | 0 | 0 | 0 | 0 | 0 | 0 |
| 2024 | xlsx | 0 | 0 | 0 | 0 | 0 | 0 |
| 2025 | csv | 0 | 0 | 0 | 0 | 0 | 0 |

## 4. Llaves naturales que resultan ambiguas

| Ejercicio | Formato | Llaves ambiguas |
|---|---|---|
| 2020 | csv | ninguna |
| 2020 | xlsx | ninguna |
| 2021 | csv | `partida_id` |
| 2021 | xlsx | `partida_id` |
| 2022 | csv | ninguna |
| 2022 | xlsx | ninguna |
| 2023 | csv | `finalidad_id+funcion_id+subfuncion_id` |
| 2023 | xlsx | ninguna |
| 2024 | csv | `finalidad_id` |
| 2024 | xlsx | ninguna |
| 2025 | csv | ninguna |

## 5. Encabezados por formato

| Ejercicio | Formato | Primeras columnas |
|---|---|---|
| 2020 | csv | `CICLO`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL` |
| 2020 | xlsx | `CICLO`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL` |
| 2021 | csv | `CICLO`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL` |
| 2021 | xlsx | `CICLO`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL` |
| 2022 | csv | `Ciclo`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL` |
| 2022 | xlsx | `Ciclo`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL` |
| 2023 | csv | `Ciclo`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL` |
| 2023 | xlsx | `Ciclo`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL` |
| 2024 | csv | `Ciclo`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL` |
| 2024 | xlsx | `Ciclo`, `ID_RAMO`, `DESC_RAMO`, `ID_UR`, `DESC_UR`, `GPO_FUNCIONAL` |
| 2025 | csv | `Ciclo`, `R`, `RAMO_DESC`, `UR`, `UR_DESC`, `FI` |
