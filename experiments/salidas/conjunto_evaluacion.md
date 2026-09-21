# Estado del conjunto de evaluacion

Generado el 2026-09-21 09:58 por `experiments/validar_conjunto.py`.

Comprobacion de texto literal: realizada contra `data/interim/solicitudes_candidatas.csv`.

**61 preguntas**, 61 validas. Meta: entre 200 y 300.

**Por estado:** 0 verificadas, 61 propuestas, 0 descartadas. Solo las verificadas entran a los experimentos: una propuesta es una sugerencia pendiente de revision humana, no una respuesta de referencia.

## Por comportamiento esperado

| Comportamiento | Preguntas | Proporcion | Meta |
|---|---:|---:|---:|
| responder | 24 | 39% | 70% |
| ambigua | 5 | 8% | 15% |
| abstenerse | 32 | 52% | 15% |

## Por dificultad (preguntas a responder)

| Dificultad | Preguntas | Proporcion | Meta |
|---|---:|---:|---:|
| baja | 12 | 52% | 30% |
| media | 9 | 39% | 40% |
| alta | 2 | 9% | 30% |

## Por origen

| Origen | Preguntas |
|---|---:|
| solicitud_pnt | 41 |
| generada_ia | 20 |

## Detalle

| Id | Estado | Ruta | Comportamiento | Dificultad | Puntos | Componentes | Filas | ms | Validacion |
|---|---|---|---|---|---:|---|---:|---:|---|
| P0001 | propuesta | sql | ambigua | baja | 2 | condicion 2 | 2 | 407 | valida |
| P0002 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0003 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0004 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0005 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0006 | propuesta | sql | responder | media | 5 | agrupacion 1, condicion 3 | 93 | 13 | valida |
| P0007 | propuesta | sql | ambigua | baja | 2 | condicion 2 | 9 | 1635 | valida |
| P0008 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0009 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0010 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0011 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0012 | propuesta | sql | ambigua | media | 4 | agrupacion 1, condicion 2 | 32 | 197 | valida |
| P0013 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0014 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0015 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0016 | propuesta | sql | responder | alta | 8 | agrupacion 1, comparacion_temporal 1, condicion 4 | 6 | 32 | valida |
| P0017 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0018 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0019 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0020 | propuesta | documental | responder |  |  |  |  |  | valida |
| P0021 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0022 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0023 | propuesta | sql | ambigua | baja | 2 | condicion 2 | 2 | 419 | valida |
| P0024 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0025 | propuesta | sql | ambigua | media | 5 | agrupacion 1, comparacion_temporal 1, condicion 1 | 7 | 47 | valida |
| P0026 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0027 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0028 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0029 | propuesta | sql | responder | baja | 3 | condicion 3 | 1 | 18 | valida |
| P0030 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0031 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0032 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0033 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0034 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0035 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0036 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0037 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0038 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0039 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0040 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0041 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0042 | propuesta | sql | responder | baja | 2 | condicion 2 | 1 | 54 | valida |
| P0043 | propuesta | sql | responder | baja | 3 | condicion 3 | 1 | 17 | valida |
| P0044 | propuesta | sql | responder | baja | 3 | condicion 3 | 1 | 41 | valida |
| P0045 | propuesta | sql | responder | media | 6 | agrupacion 1, comparacion_temporal 1, condicion 2 | 6 | 98 | valida |
| P0046 | propuesta | sql | responder | media | 4 | agrupacion 1, condicion 1, top_n 1 | 5 | 1111 | valida |
| P0047 | propuesta | sql | responder | baja | 3 | condicion 3 | 1 | 34 | valida |
| P0048 | propuesta | sql | responder | media | 4 | agrupacion 1, condicion 1, top_n 1 | 1 | 431 | valida |
| P0049 | propuesta | sql | responder | baja | 2 | condicion 2 | 1 | 119 | valida |
| P0050 | propuesta | sql | responder | baja | 2 | condicion 2 | 1 | 282 | valida |
| P0051 | propuesta | sql | responder | media | 5 | agrupacion 1, condicion 3 | 14 | 22 | valida |
| P0052 | propuesta | sql | responder | media | 6 | agrupacion 1, comparacion_temporal 1, condicion 2 | 6 | 19 | valida |
| P0053 | propuesta | sql | responder | media | 5 | agrupacion 1, condicion 2, top_n 1 | 3 | 397 | valida |
| P0054 | propuesta | sql | responder | baja | 2 | condicion 2 | 1 | 62 | valida |
| P0055 | propuesta | sql | responder | baja | 3 | agrupacion 1, condicion 1 | 4 | 266 | valida |
| P0056 | propuesta | sql | responder | baja | 2 | condicion 2 | 1 | 69 | valida |
| P0057 | propuesta | sql | responder | baja | 2 | condicion 2 | 1 | 42 | valida |
| P0058 | propuesta | sql | responder | media | 4 | condicion 1, condicional 1, division 1 | 1 | 222 | valida |
| P0059 | propuesta | sql | responder | alta | 8 | comparacion_temporal 1, condicion 2, condicional 2, division 1 | 1 | 89 | valida |
| P0060 | propuesta | sql | responder | baja | 2 | condicion 2 | 1 | 44 | valida |
| P0061 | propuesta | sql | responder | media | 5 | agrupacion 1, condicion 2, top_n 1 | 1 | 105 | valida |

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
