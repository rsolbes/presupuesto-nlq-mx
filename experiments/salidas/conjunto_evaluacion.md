# Estado del conjunto de evaluacion

Generado el 2026-09-18 12:18 por `experiments/validar_conjunto.py`.

Comprobacion de texto literal: realizada contra `data/interim/solicitudes_candidatas.csv`.

**17 preguntas**, 17 validas. Meta: entre 200 y 300.

**Por estado:** 0 verificadas, 17 propuestas, 0 descartadas. Solo las verificadas entran a los experimentos: una propuesta es una sugerencia pendiente de revision humana, no una respuesta de referencia.

## Por comportamiento esperado

| Comportamiento | Preguntas | Proporcion | Meta |
|---|---:|---:|---:|
| responder | 2 | 12% | 70% |
| ambigua | 3 | 18% | 15% |
| abstenerse | 12 | 71% | 15% |

## Por dificultad (preguntas a responder)

| Dificultad | Preguntas | Proporcion | Meta |
|---|---:|---:|---:|
| baja | 0 | 0% | 30% |
| media | 1 | 50% | 40% |
| alta | 1 | 50% | 30% |

## Por origen

| Origen | Preguntas |
|---|---:|
| solicitud_pnt | 17 |

## Detalle

| Id | Estado | Ruta | Comportamiento | Dificultad | Puntos | Componentes | Filas | ms | Validacion |
|---|---|---|---|---|---:|---|---:|---:|---|
| P0001 | propuesta | sql | ambigua | baja | 2 | condicion 2 | 2 | 271 | valida |
| P0002 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0003 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0004 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0005 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0006 | propuesta | sql | responder | media | 5 | agrupacion 1, condicion 3 | 93 | 13 | valida |
| P0007 | propuesta | sql | ambigua | baja | 2 | condicion 2 | 9 | 1343 | valida |
| P0008 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0009 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0010 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0011 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0012 | propuesta | sql | ambigua | media | 4 | agrupacion 1, condicion 2 | 32 | 103 | valida |
| P0013 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0014 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0015 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0016 | propuesta | sql | responder | alta | 8 | agrupacion 1, comparacion_temporal 1, condicion 4 | 6 | 22 | valida |
| P0017 | propuesta | sql | abstenerse |  |  |  |  |  | valida |

## Regla de dificultad

| Componente | Puntos |
|---|---:|
| condicion | 1 |
| agrupacion | 2 |
| having | 1 |
| top_n | 1 |
| join | 2 |
| subconsulta | 3 |
| ventana | 3 |
| conjunto | 3 |
| division | 2 |
| condicional | 1 |
| comparacion_temporal | 2 |

Baja: menos de 4 puntos. Media: de 4 a 6. Alta: 7 o mas.
