# Estado del conjunto de evaluacion

Generado el 2026-09-21 09:29 por `experiments/validar_conjunto.py`.

Comprobacion de texto literal: realizada contra `data/interim/solicitudes_candidatas.csv`.

**41 preguntas**, 41 validas. Meta: entre 200 y 300.

**Por estado:** 0 verificadas, 41 propuestas, 0 descartadas. Solo las verificadas entran a los experimentos: una propuesta es una sugerencia pendiente de revision humana, no una respuesta de referencia.

## Por comportamiento esperado

| Comportamiento | Preguntas | Proporcion | Meta |
|---|---:|---:|---:|
| responder | 4 | 10% | 70% |
| ambigua | 5 | 12% | 15% |
| abstenerse | 32 | 78% | 15% |

## Por dificultad (preguntas a responder)

| Dificultad | Preguntas | Proporcion | Meta |
|---|---:|---:|---:|
| baja | 1 | 33% | 30% |
| media | 1 | 33% | 40% |
| alta | 1 | 33% | 30% |

## Por origen

| Origen | Preguntas |
|---|---:|
| solicitud_pnt | 41 |

## Detalle

| Id | Estado | Ruta | Comportamiento | Dificultad | Puntos | Componentes | Filas | ms | Validacion |
|---|---|---|---|---|---:|---|---:|---:|---|
| P0001 | propuesta | sql | ambigua | baja | 2 | condicion 2 | 2 | 330 | valida |
| P0002 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0003 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0004 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0005 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0006 | propuesta | sql | responder | media | 5 | agrupacion 1, condicion 3 | 93 | 15 | valida |
| P0007 | propuesta | sql | ambigua | baja | 2 | condicion 2 | 9 | 1315 | valida |
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
| P0018 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0019 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0020 | propuesta | documental | responder |  |  |  |  |  | valida |
| P0021 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0022 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0023 | propuesta | sql | ambigua | baja | 2 | condicion 2 | 2 | 314 | valida |
| P0024 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0025 | propuesta | sql | ambigua | media | 5 | agrupacion 1, comparacion_temporal 1, condicion 1 | 7 | 27 | valida |
| P0026 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0027 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0028 | propuesta | sql | abstenerse |  |  |  |  |  | valida |
| P0029 | propuesta | sql | responder | baja | 3 | condicion 3 | 1 | 19 | valida |
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
