# Hoja de verificación

Generada por `experiments/hoja_verificacion.py` con el rol `consulta_nlq`. 20 preguntas en estado `propuesta`.

## Índice

| Pregunta | Texto | Estado del resultado |
|---|---|---|
| [P0042](#p0042) | ¿Cuánto presupuesto se le aprobó a la Secretaría de Educación Pública para 2025? | igual a lo guardado |
| [P0043](#p0043) | ¿Cuánto dinero ejerció la Guardia Nacional en 2023? | igual a lo guardado |
| [P0044](#p0044) | ¿Cuánto se pagó en 2024 a través de la Pensión para el Bienestar de las Personas | igual a lo guardado |
| [P0045](#p0045) | ¿Cuánto se ejerció en el programa Sembrando Vida en cada año de 2020 a 2025? | igual a lo guardado |
| [P0046](#p0046) | ¿Cuáles fueron los cinco programas presupuestarios con más presupuesto aprobado  | igual a lo guardado |
| [P0047](#p0047) | ¿Cuánto ejerció el IMSS en servicios personales en 2024? | igual a lo guardado |
| [P0048](#p0048) | ¿En qué capítulo de gasto se devengó más dinero en 2024? | igual a lo guardado |
| [P0049](#p0049) | ¿Cuánto devengó el gobierno federal en medicinas y productos farmacéuticos duran | igual a lo guardado |
| [P0050](#p0050) | ¿Cuánto gasto federal se pagó con destino a Tamaulipas en 2025? | igual a lo guardado |
| [P0051](#p0051) | ¿Cuánto recibió Tamaulipas en 2024 de cada fondo de aportaciones federales del r | igual a lo guardado |
| [P0052](#p0052) | ¿Cuánto le pagó la Federación a Tamaulipas por participaciones en cada año de 20 | igual a lo guardado |
| [P0053](#p0053) | ¿Cuáles fueron las tres entidades federativas con mayor gasto federal devengado  | igual a lo guardado |
| [P0054](#p0054) | ¿Cuál fue el presupuesto aprobado para la función Educación de la clasificación  | igual a lo guardado |
| [P0055](#p0055) | ¿Cómo se repartió el gasto devengado de 2024 entre las finalidades de la clasifi | igual a lo guardado |
| [P0056](#p0056) | ¿Cuál fue el subejercicio de la Secretaría de Marina en 2024? | igual a lo guardado |
| [P0057](#p0057) | En 2023, ¿cuánto más o cuánto menos ejerció la Secretaría de Energía en comparac | igual a lo guardado |
| [P0058](#p0058) | ¿Qué porcentaje del gasto devengado en 2024 correspondió a pensiones y jubilacio | igual a lo guardado |
| [P0059](#p0059) | ¿En qué porcentaje cambió el presupuesto aprobado de la Secretaría de Salud entr | igual a lo guardado |
| [P0060](#p0060) | ¿Cuántos programas presupuestarios distintos tuvo la Secretaría de Bienestar en  | igual a lo guardado |
| [P0061](#p0061) | ¿Qué unidad responsable de la Secretaría de Educación Pública tuvo el mayor gast | igual a lo guardado |

## Cómo verificar cada pregunta

1. **La pregunta.** Se entiende, suena natural y no da pistas del esquema.
2. **La lectura.** La etapa, el año y el alcance que asume el SQL son los que pide la pregunta (criterios en `eval/README.md`). La tabla por etapa muestra cuánto cambia la cifra si la etapa fuera otra.
3. **El SQL.** Hace lo que la pregunta pide, y la trampa de las notas está resuelta.
4. **La cifra.** Recalcúlala en el xlsx publicado con la receta: filtra las columnas indicadas (Datos → Filtro) y selecciona la columna a sumar; Excel muestra la suma de las celdas visibles en la barra de estado. Para agrupaciones, usa una tabla dinámica.
5. **Si coincide**, registra en `eval/preguntas.yaml`:

```yaml
  verificacion:
    documento: "cuenta_publica_AAAA_gf_ecd_epe.xlsx, recálculo en el archivo publicado"
    ubicacion: "filtros aplicados, tal como en la receta"
    valor: "cifra obtenida"
  estado: verificada
  verificado_por: RSD
```

El recálculo prueba que la cifra es fiel al archivo oficial y que la cadena del proyecto (normalización, carga, capa semántica y SQL) no la alteró. Si además encuentras la cifra en un documento oficial distinto, como un tomo de la Cuenta Pública, regístralo en su lugar: es una verificación más fuerte. Si no coincide, o la lectura no te convence, anótalo en `notas` y déjala como `propuesta`.

---

## P0042

> ¿Cuánto presupuesto se le aprobó a la Secretaría de Educación Pública para 2025?

Origen: generada_ia · matriz de cobertura, lote G1: administrativa / total

```sql
SELECT sum(aprobado) AS aprobado
FROM semantica.gasto
WHERE ejercicio = 2025
  AND ramo_clave = 11
```

### Resultado en la base

| aprobado |
|---|
| 465871888417.00 (465,871.9 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 465,871.9 |
| modificado | 491,067.3 |
| devengado | 490,980.5 |
| ejercido | 490,977.5 |
| pagado | 487,457.5 |

### Receta de recálculo en el xlsx

**2025** — archivo `data/raw/cuenta_publica_2025_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | R | es 11 |

Sumar: AA (MONTO_APROBADO)

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0043

> ¿Cuánto dinero ejerció la Guardia Nacional en 2023?

Origen: generada_ia · matriz de cobertura, lote G1: administrativa / total (unidad responsable)

Notas: La Guardia Nacional es la unidad H00 del ramo 36, Seguridad y Protección Ciudadana.

```sql
SELECT sum(ejercido) AS ejercido
FROM semantica.gasto
WHERE ejercicio = 2023
  AND ramo_clave = 36
  AND unidad_responsable_clave = 'H00'
```

### Resultado en la base

| ejercido |
|---|
| 24432593018.89 (24,432.6 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 67,826.7 |
| modificado | 24,432.6 |
| devengado | 24,432.6 |
| ejercido | 24,432.6 |
| pagado | 23,995.4 |

### Receta de recálculo en el xlsx

**2023** — archivo `data/raw/cuenta_publica_2023_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 36 |
| D | ID_UR | es "H00" |

Sumar: AF (EJERCICIO)

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0044

> ¿Cuánto se pagó en 2024 a través de la Pensión para el Bienestar de las Personas Adultas Mayores?

Origen: generada_ia · matriz de cobertura, lote G1: programática / total

```sql
SELECT sum(pagado) AS pagado
FROM semantica.gasto
WHERE ejercicio = 2024
  AND ramo_clave = 20
  AND programa_clave = 'S176'
```

### Resultado en la base

| pagado |
|---|
| 442459087372.15 (442,459.1 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 465,048.7 |
| modificado | 442,727.4 |
| devengado | 442,727.4 |
| ejercido | 442,727.4 |
| pagado | 442,459.1 |

### Receta de recálculo en el xlsx

**2024** — archivo `data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 20 |
| N | ID_MODALIDAD | es S |
| P | ID_PP | es 176 |

Sumar: AD (MONTO_PAGADO)

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0045

> ¿Cuánto se ejerció en el programa Sembrando Vida en cada año de 2020 a 2025?

Origen: generada_ia · matriz de cobertura, lote G1: programática / comparación entre ejercicios

Notas: Trampa del esquema: el programa tiene dos claves, S287 y U010, que coexisten en 2020. Filtrar por una sola clave omite 4,269.5 millones de ese año; el SQL filtra por nombre.

```sql
SELECT ejercicio, sum(ejercido) AS ejercido
FROM semantica.gasto
WHERE ramo_clave = 20
  AND programa = 'Sembrando Vida'
GROUP BY ejercicio
ORDER BY ejercicio
```

### Resultado en la base

| ejercicio | ejercido |
|---|---|
| 2020 | 27307285988.60 (27,307.3 MDP) |
| 2021 | 28152825039.00 (28,152.8 MDP) |
| 2022 | 29634539976.00 (29,634.5 MDP) |
| 2023 | 34372498102.28 (34,372.5 MDP) |
| 2024 | 35220237189.39 (35,220.2 MDP) |
| 2025 | 35396291343.03 (35,396.3 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 202,503.8 |
| modificado | 190,084.1 |
| devengado | 190,083.7 |
| ejercido | 190,083.7 |
| pagado | 189,713.2 |

### Receta de recálculo en el xlsx

**2020** — archivo `data/raw/cuenta_publica_2020_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 20 |
| Q | DESC_PP | es "Sembrando Vida" |

Sumar: AF (EJERCICIO)

Aviso: `DESC_PP` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

**2021** — archivo `data/raw/cuenta_publica_2021_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 20 |
| Q | DESC_PP | es "Sembrando Vida" |

Sumar: AF (EJERCICIO)

Aviso: `DESC_PP` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

**2022** — archivo `data/raw/cuenta_publica_2022_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 20 |
| Q | DESC_PP | es "Sembrando Vida" |

Sumar: AF (EJERCICIO)

Aviso: `DESC_PP` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

**2023** — archivo `data/raw/cuenta_publica_2023_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 20 |
| Q | DESC_PP | es "Sembrando Vida" |

Sumar: AF (EJERCICIO)

Aviso: `DESC_PP` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

**2024** — archivo `data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 20 |
| Q | DESC_PP | es "Sembrando Vida" |

Sumar: AF (MONTO_EJERCIDO)

Aviso: `DESC_PP` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

**2025** — archivo `data/raw/cuenta_publica_2025_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | R | es 20 |
| Q | DESC_PP | es "Sembrando Vida" |

Sumar: AF (MONTO_EJERCIDO)

Aviso: `DESC_PP` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0046

> ¿Cuáles fueron los cinco programas presupuestarios con más presupuesto aprobado en 2025?

Origen: generada_ia · matriz de cobertura, lote G1: programática / los mayores

Notas: Trampa del esquema: la clave de programa no es única entre ramos. Agrupar solo por clave sumaría programas distintos; el SQL agrupa por ramo, clave y nombre.

```sql
SELECT ramo, programa_clave, programa, sum(aprobado) AS aprobado
FROM semantica.gasto
WHERE ejercicio = 2025
GROUP BY ramo, programa_clave, programa
ORDER BY aprobado DESC
LIMIT 5
```

### Resultado en la base

| ramo | programa_clave | programa | aprobado |
|---|---|---|---|
| Participaciones a Entidades Federativas y Municipios | C001 | Fondo General de Participaciones | 980334377725.00 (980,334.4 MDP) |
| Deuda Pública | D001 | Valores gubernamentales | 967389552695.00 (967,389.6 MDP) |
| Aportaciones a Seguridad Social | J008 | Pensiones y Jubilaciones en curso de Pago | 753202100919.00 (753,202.1 MDP) |
| Instituto Mexicano del Seguro Social | J001 | Pensiones en curso de pago Ley 1973 | 753202100919.00 (753,202.1 MDP) |
| Bienestar | S176 | Pensión para el Bienestar de las Personas Adultas Mayores | 483427619205.00 (483,427.6 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 10,795,085.1 |
| modificado | 11,175,477.3 |
| devengado | 11,276,211.2 |
| ejercido | 11,272,216.4 |
| pagado | 11,091,126.6 |

### Receta de recálculo en el xlsx

**2025** — archivo `data/raw/cuenta_publica_2025_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|

Sumar: AA (MONTO_APROBADO)
Agrupar por: DESC_RAMO, MODALIDAD y PP, DESC_PP (tabla dinámica, con estas columnas en filas).

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0047

> ¿Cuánto ejerció el IMSS en servicios personales en 2024?

Origen: generada_ia · matriz de cobertura, lote G1: objeto del gasto / total (capítulo)

Notas: Servicios personales es el capítulo 1000 del Clasificador por Objeto del Gasto.

```sql
SELECT sum(ejercido) AS ejercido
FROM semantica.gasto
WHERE ejercicio = 2024
  AND ramo_clave = 50
  AND capitulo_clave = 1000
```

### Resultado en la base

| ejercido |
|---|
| 286844053115.00 (286,844.1 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 270,821.0 |
| modificado | 286,844.1 |
| devengado | 287,519.2 |
| ejercido | 286,844.1 |
| pagado | 286,844.1 |

### Receta de recálculo en el xlsx

**2024** — archivo `data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 50 |
| R | ID_OBJETO_DEL_GASTO | es entre 10000 y 19999 |

Sumar: AF (MONTO_EJERCIDO)

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0048

> ¿En qué capítulo de gasto se devengó más dinero en 2024?

Origen: generada_ia · matriz de cobertura, lote G1: objeto del gasto / los mayores

```sql
SELECT capitulo, sum(devengado) AS devengado
FROM semantica.gasto
WHERE ejercicio = 2024
GROUP BY capitulo
ORDER BY devengado DESC
LIMIT 1
```

### Resultado en la base

| capitulo | devengado |
|---|---|
| Transferencias, asignaciones, subsidios y otras ayudas | 3990314365721.56 (3,990,314.4 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 10,406,689.0 |
| modificado | 10,559,409.9 |
| devengado | 10,555,267.3 |
| ejercido | 10,554,159.3 |
| pagado | 10,506,472.4 |

### Receta de recálculo en el xlsx

**2024** — archivo `data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|

Sumar: AC (MONTO_DEVENGADO)
Agrupar por: primer dígito de ID_OBJETO_DEL_GASTO (tabla dinámica, con estas columnas en filas).

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0049

> ¿Cuánto devengó el gobierno federal en medicinas y productos farmacéuticos durante 2023?

Origen: generada_ia · matriz de cobertura, lote G1: objeto del gasto / total (partida)

Notas: Partida 25301, la única del clasificador para medicinas.

```sql
SELECT sum(devengado) AS devengado
FROM semantica.gasto
WHERE ejercicio = 2023
  AND partida_clave = 25301
```

### Resultado en la base

| devengado |
|---|
| 87420457107.46 (87,420.5 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 86,041.3 |
| modificado | 99,447.2 |
| devengado | 87,420.5 |
| ejercido | 99,436.0 |
| pagado | 99,019.9 |

### Receta de recálculo en el xlsx

**2023** — archivo `data/raw/cuenta_publica_2023_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| R | ID_OBJETO_DEL_GASTO | es 25301 |

Sumar: AC (MONTO_DEVENGADO)

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0050

> ¿Cuánto gasto federal se pagó con destino a Tamaulipas en 2025?

Origen: generada_ia · matriz de cobertura, lote G1: geográfica / total (caso local)

Notas: Solo cuenta el gasto con destino geográfico asignado: una parte importante del gasto federal se clasifica como no distribuible geográficamente.

```sql
SELECT sum(pagado) AS pagado
FROM semantica.gasto
WHERE ejercicio = 2025
  AND entidad_federativa = 'Tamaulipas'
```

### Resultado en la base

| pagado |
|---|
| 207999168851.10 (207,999.2 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 194,313.4 |
| modificado | 207,802.7 |
| devengado | 208,067.4 |
| ejercido | 209,124.6 |
| pagado | 207,999.2 |

### Receta de recálculo en el xlsx

**2025** — archivo `data/raw/cuenta_publica_2025_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| Y | DESC_ENTIDAD_FEDERATIVA | es "Tamaulipas" |

Sumar: AD (MONTO_PAGADO)

Aviso: `DESC_ENTIDAD_FEDERATIVA` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0051

> ¿Cuánto recibió Tamaulipas en 2024 de cada fondo de aportaciones federales del ramo 33, en montos pagados?

Origen: generada_ia · matriz de cobertura, lote G1: geográfica + programática / desglose (caso local)

Notas: Los fondos de aportaciones son los programas del ramo 33; la base los nombra por sigla (FASSA, FONE, FAM...).

```sql
SELECT programa_clave, programa, sum(pagado) AS pagado
FROM semantica.gasto
WHERE ejercicio = 2024
  AND ramo_clave = 33
  AND entidad_federativa = 'Tamaulipas'
GROUP BY programa_clave, programa
ORDER BY programa_clave
```

### Resultado en la base

| programa_clave | programa | pagado |
|---|---|---|
| I002 | FASSA | 2384252576.99 (2,384.3 MDP) |
| I003 | FAIS Entidades | 188552255.00 (188.6 MDP) |
| I004 | FAIS Municipal y de las Demarcaciones Territoriales del Distrito Federal | 1366970390.29 (1,367.0 MDP) |
| I005 | FORTAMUN | 3189532198.21 (3,189.5 MDP) |
| I006 | FAM Asistencia Social | 375742657.66 (375.7 MDP) |
| I007 | FAM Infraestructura Educativa Básica | 337733878.00 (337.7 MDP) |
| I008 | FAM Infraestructura Educativa Media Superior y Superior | 161031830.00 (161.0 MDP) |
| I009 | FAETA Educación Tecnológica | 240928650.21 (240.9 MDP) |
| I010 | FAETA Educación de Adultos | 100154946.09 (100.2 MDP) |
| I011 | FASP | 273892265.80 (273.9 MDP) |
| I012 | FAFEF | 1499200306.00 (1,499.2 MDP) |
| I013 | FONE Servicios Personales | 17137874449.58 (17,137.9 MDP) |
| I014 | FONE Otros de Gasto Corriente | 47880373.72 (47.9 MDP) |
| I015 | FONE Gasto de Operación | 537219508.50 (537.2 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 27,820.4 |
| modificado | 27,841.0 |
| devengado | 27,841.0 |
| ejercido | 27,841.0 |
| pagado | 27,841.0 |

### Receta de recálculo en el xlsx

**2024** — archivo `data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 33 |
| Y | ENTIDAD_FEDERATIVA | es "Tamaulipas" |

Sumar: AD (MONTO_PAGADO)
Agrupar por: ID_MODALIDAD y ID_PP, DESC_PP (tabla dinámica, con estas columnas en filas).

Aviso: `ENTIDAD_FEDERATIVA` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0052

> ¿Cuánto le pagó la Federación a Tamaulipas por participaciones en cada año de 2020 a 2025?

Origen: generada_ia · matriz de cobertura, lote G1: geográfica / comparación entre ejercicios (caso local)

Notas: Las participaciones son el ramo 28.

```sql
SELECT ejercicio, sum(pagado) AS pagado
FROM semantica.gasto
WHERE ramo_clave = 28
  AND entidad_federativa = 'Tamaulipas'
GROUP BY ejercicio
ORDER BY ejercicio
```

### Resultado en la base

| ejercicio | pagado |
|---|---|
| 2020 | 26407036106.00 (26,407.0 MDP) |
| 2021 | 28035036673.00 (28,035.0 MDP) |
| 2022 | 31988553801.00 (31,988.6 MDP) |
| 2023 | 34097795129.00 (34,097.8 MDP) |
| 2024 | 37236941175.00 (37,236.9 MDP) |
| 2025 | 39254508390.00 (39,254.5 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 204,229.3 |
| modificado | 197,019.9 |
| devengado | 197,019.9 |
| ejercido | 197,019.9 |
| pagado | 197,019.9 |

### Receta de recálculo en el xlsx

**2020** — archivo `data/raw/cuenta_publica_2020_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 28 |
| Y | ENTIDAD_FEDERATIVA | es "Tamaulipas" |

Sumar: AD (MONTO_PAGADO)

Aviso: `ENTIDAD_FEDERATIVA` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

**2021** — archivo `data/raw/cuenta_publica_2021_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 28 |
| Y | ENTIDAD_FEDERATIVA | es "Tamaulipas" |

Sumar: AD (MONTO_PAGADO)

Aviso: `ENTIDAD_FEDERATIVA` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

**2022** — archivo `data/raw/cuenta_publica_2022_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 28 |
| Y | ENTIDAD_FEDERATIVA | es "Tamaulipas" |

Sumar: AD (MONTO_PAGADO)

Aviso: `ENTIDAD_FEDERATIVA` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

**2023** — archivo `data/raw/cuenta_publica_2023_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 28 |
| Y | ENTIDAD_FEDERATIVA | es "Tamaulipas" |

Sumar: AD (MONTO_PAGADO)

Aviso: `ENTIDAD_FEDERATIVA` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

**2024** — archivo `data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 28 |
| Y | ENTIDAD_FEDERATIVA | es "Tamaulipas" |

Sumar: AD (MONTO_PAGADO)

Aviso: `ENTIDAD_FEDERATIVA` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

**2025** — archivo `data/raw/cuenta_publica_2025_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | R | es 28 |
| Y | DESC_ENTIDAD_FEDERATIVA | es "Tamaulipas" |

Sumar: AD (MONTO_PAGADO)

Aviso: `DESC_ENTIDAD_FEDERATIVA` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0053

> ¿Cuáles fueron las tres entidades federativas con mayor gasto federal devengado en 2024?

Origen: generada_ia · matriz de cobertura, lote G1: geográfica / los mayores

Notas: Trampa del esquema: la dimensión geográfica incluye 'En El Extranjero' y 'No Distribuible Geográficamente', que no son entidades federativas y encabezarían la lista si no se excluyen. Nota para la verificación: la Ciudad de México encabeza con cerca del 40% del gasto devengado por el efecto sede; la clasificación geográfica le asigna buena parte del gasto de las dependencias con oficinas centrales en ella, no necesariamente donde se recibe el beneficio.

```sql
SELECT entidad_federativa, sum(devengado) AS devengado
FROM semantica.gasto
WHERE ejercicio = 2024
  AND entidad_federativa NOT IN ('En El Extranjero', 'No Distribuible Geográficamente')
GROUP BY entidad_federativa
ORDER BY devengado DESC
LIMIT 3
```

### Resultado en la base

| entidad_federativa | devengado |
|---|---|
| Ciudad de México | 4191070310435.03 (4,191,070.3 MDP) |
| Estado de México | 507924041043.88 (507,924.0 MDP) |
| Veracruz | 378283099187.93 (378,283.1 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 9,058,259.5 |
| modificado | 9,395,463.6 |
| devengado | 9,391,321.0 |
| ejercido | 9,390,213.0 |
| pagado | 9,343,200.9 |

### Receta de recálculo en el xlsx

**2024** — archivo `data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| Y | ENTIDAD_FEDERATIVA | no es ninguno de "En El Extranjero", "No Distribuible Geográficamente" |

Sumar: AC (MONTO_DEVENGADO)
Agrupar por: ENTIDAD_FEDERATIVA (tabla dinámica, con estas columnas en filas).

Aviso: `ENTIDAD_FEDERATIVA` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0054

> ¿Cuál fue el presupuesto aprobado para la función Educación de la clasificación funcional en 2025?

Origen: generada_ia · matriz de cobertura, lote G1: funcional / total

Notas: La pregunta nombra la clasificación funcional para distinguirla del ramo 11, Educación Pública: son cifras distintas.

```sql
SELECT sum(aprobado) AS aprobado
FROM semantica.gasto
WHERE ejercicio = 2025
  AND funcion = 'Educación'
```

### Resultado en la base

| aprobado |
|---|
| 1084590853205.00 (1,084,590.9 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 1,084,590.9 |
| modificado | 1,102,595.1 |
| devengado | 1,102,510.8 |
| ejercido | 1,102,507.8 |
| pagado | 1,099,398.3 |

### Receta de recálculo en el xlsx

**2025** — archivo `data/raw/cuenta_publica_2025_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| I | DESC_FUNCION | es "Educación" |

Sumar: AA (MONTO_APROBADO)

Aviso: `DESC_FUNCION` usa el nombre del ejercicio más reciente; si el valor no aparece en este archivo, busca una variante del nombre.

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0055

> ¿Cómo se repartió el gasto devengado de 2024 entre las finalidades de la clasificación funcional?

Origen: generada_ia · matriz de cobertura, lote G1: funcional / desglose

```sql
SELECT finalidad, sum(devengado) AS devengado
FROM semantica.gasto
WHERE ejercicio = 2024
GROUP BY finalidad
ORDER BY devengado DESC
```

### Resultado en la base

| finalidad | devengado |
|---|---|
| Desarrollo Social | 5552493575492.18 (5,552,493.6 MDP) |
| Otras no Clasificadas en Funciones Anteriores | 2355063347366.07 (2,355,063.3 MDP) |
| Desarrollo Económico | 1986074871713.24 (1,986,074.9 MDP) |
| Gobierno | 661635473018.50 (661,635.5 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 10,406,689.0 |
| modificado | 10,559,409.9 |
| devengado | 10,555,267.3 |
| ejercido | 10,554,159.3 |
| pagado | 10,506,472.4 |

### Receta de recálculo en el xlsx

**2024** — archivo `data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|

Sumar: AC (MONTO_DEVENGADO)
Agrupar por: DESC_GPO_FUNCIONAL (tabla dinámica, con estas columnas en filas).

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0056

> ¿Cuál fue el subejercicio de la Secretaría de Marina en 2024?

Origen: generada_ia · matriz de cobertura, lote G1: administrativa / diferencia entre etapas

Notas: Subejercicio como modificado menos devengado, la definición verificada en la Cuenta Pública. Nota para la verificación: el resultado es 0.00 y es correcto. En 2024, 32 de los 44 ramos que no son entidades de control directo ni empresas tienen subejercicio cero, porque al cierre el modificado se ajusta al devengado. La definición común entre el público, aprobado menos devengado, daría una cifra distinta: la pregunta pone a prueba si el sistema usa la definición de la Cuenta Pública.

```sql
SELECT sum(modificado) - sum(devengado) AS subejercicio
FROM semantica.gasto
WHERE ejercicio = 2024
  AND ramo_clave = 13
```

### Resultado en la base

| subejercicio |
|---|
| 0.00 |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 71,888.2 |
| modificado | 127,193.0 |
| devengado | 127,193.0 |
| ejercido | 127,193.0 |
| pagado | 126,817.7 |

### Receta de recálculo en el xlsx

**2024** — archivo `data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 13 |

Sumar: AB (MONTO_MODIFICADO), AC (MONTO_DEVENGADO)

El SELECT calcula sobre las sumas (resta, porcentaje o condición): obtén primero las sumas con los filtros y aplica el cálculo del SQL.

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0057

> En 2023, ¿cuánto más o cuánto menos ejerció la Secretaría de Energía en comparación con su presupuesto aprobado?

Origen: generada_ia · matriz de cobertura, lote G1: administrativa / diferencia entre etapas

Notas: Un resultado positivo indica que se ejerció más de lo aprobado.

```sql
SELECT sum(ejercido) - sum(aprobado) AS diferencia
FROM semantica.gasto
WHERE ejercicio = 2023
  AND ramo_clave = 18
```

### Resultado en la base

| diferencia |
|---|
| 130003505593.79 (130,003.5 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 49,401.9 |
| modificado | 179,405.5 |
| devengado | 179,405.5 |
| ejercido | 179,405.5 |
| pagado | 179,400.8 |

### Receta de recálculo en el xlsx

**2023** — archivo `data/raw/cuenta_publica_2023_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 18 |

Sumar: AF (EJERCICIO), AA (MONTO_APROBADO)

El SELECT calcula sobre las sumas (resta, porcentaje o condición): obtén primero las sumas con los filtros y aplica el cálculo del SQL.

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0058

> ¿Qué porcentaje del gasto devengado en 2024 correspondió a pensiones y jubilaciones?

Origen: generada_ia · matriz de cobertura, lote G1: económica / proporción

Notas: Pensiones y jubilaciones es el tipo de gasto 4.

```sql
SELECT 100 * sum(CASE WHEN tipo_de_gasto = 'Pensiones y jubilaciones' THEN devengado ELSE 0 END)
           / sum(devengado) AS porcentaje
FROM semantica.gasto
WHERE ejercicio = 2024
```

### Resultado en la base

| porcentaje |
|---|
| 23.1532913589703602 |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 10,406,689.0 |
| modificado | 10,559,409.9 |
| devengado | 10,555,267.3 |
| ejercido | 10,554,159.3 |
| pagado | 10,506,472.4 |

### Receta de recálculo en el xlsx

**2024** — archivo `data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|

Sumar: AC (MONTO_DEVENGADO)

El SELECT calcula sobre las sumas (resta, porcentaje o condición): obtén primero las sumas con los filtros y aplica el cálculo del SQL.

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0059

> ¿En qué porcentaje cambió el presupuesto aprobado de la Secretaría de Salud entre 2020 y 2025?

Origen: generada_ia · matriz de cobertura, lote G1: administrativa / comparación entre ejercicios (proporción)

Notas: Cambio porcentual del ramo 12. En términos nominales: no descuenta la inflación. Nota para la verificación: la caída de 48% es consistente con el traslado de servicios de salud a IMSS-Bienestar, que aparece en el ramo 47 Entidades no Sectorizadas (165 mil millones en la función Salud en 2025, ver P0012). La cifra responde a la pregunta sobre el ramo 12, pero no mide la evolución del gasto en salud.

```sql
SELECT 100 * (sum(CASE WHEN ejercicio = 2025 THEN aprobado END)
            / sum(CASE WHEN ejercicio = 2020 THEN aprobado END) - 1) AS cambio_porcentual
FROM semantica.gasto
WHERE ramo_clave = 12
  AND ejercicio IN (2020, 2025)
```

### Resultado en la base

| cambio_porcentual |
|---|
| -48.23018876090224472300 |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 195,519.6 |
| modificado | 217,272.0 |
| devengado | 217,272.0 |
| ejercido | 217,272.0 |
| pagado | 212,575.4 |

### Receta de recálculo en el xlsx

**2020** — archivo `data/raw/cuenta_publica_2020_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 12 |

Sumar: AA (MONTO_APROBADO)

**2021** — archivo `data/raw/cuenta_publica_2021_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 12 |

Sumar: AA (MONTO_APROBADO)

**2022** — archivo `data/raw/cuenta_publica_2022_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 12 |

Sumar: AA (MONTO_APROBADO)

**2023** — archivo `data/raw/cuenta_publica_2023_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 12 |

Sumar: AA (MONTO_APROBADO)

**2024** — archivo `data/raw/cuenta_publica_2024_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 12 |

Sumar: AA (MONTO_APROBADO)

**2025** — archivo `data/raw/cuenta_publica_2025_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | R | es 12 |

Sumar: AA (MONTO_APROBADO)

El SELECT calcula sobre las sumas (resta, porcentaje o condición): obtén primero las sumas con los filtros y aplica el cálculo del SQL.

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0060

> ¿Cuántos programas presupuestarios distintos tuvo la Secretaría de Bienestar en 2025?

Origen: generada_ia · matriz de cobertura, lote G1: programática / total (conteo)

Notas: Dentro de un mismo ramo la clave de programa sí es única.

```sql
SELECT count(DISTINCT programa_clave) AS programas
FROM semantica.gasto
WHERE ejercicio = 2025
  AND ramo_clave = 20
```

### Resultado en la base

| programas |
|---|
| 15 |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 579,883.9 |
| modificado | 606,942.9 |
| devengado | 606,896.5 |
| ejercido | 606,896.5 |
| pagado | 606,890.6 |

### Receta de recálculo en el xlsx

**2025** — archivo `data/raw/cuenta_publica_2025_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | R | es 20 |

Sumar: sin etapa en el SELECT

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo

---

## P0061

> ¿Qué unidad responsable de la Secretaría de Educación Pública tuvo el mayor gasto devengado en 2023?

Origen: generada_ia · matriz de cobertura, lote G1: administrativa / los mayores (unidad responsable)

```sql
SELECT unidad_responsable, sum(devengado) AS devengado
FROM semantica.gasto
WHERE ejercicio = 2023
  AND ramo_clave = 11
GROUP BY unidad_responsable
ORDER BY devengado DESC
LIMIT 1
```

### Resultado en la base

| unidad_responsable | devengado |
|---|---|
| Coordinación Nacional de Becas para el Bienestar Benito Juárez | 82307508877.56 (82,307.5 MDP) |

### Mismo filtro en cada etapa

| Etapa | Millones de pesos |
|---|---:|
| aprobado | 402,276.7 |
| modificado | 420,251.7 |
| devengado | 420,251.7 |
| ejercido | 420,251.7 |
| pagado | 419,913.2 |

### Receta de recálculo en el xlsx

**2023** — archivo `data/raw/cuenta_publica_2023_gf_ecd_epe.xlsx`

| Columna | Encabezado | Filtro |
|---|---|---|
| B | ID_RAMO | es 11 |

Sumar: AC (MONTO_DEVENGADO)
Agrupar por: DESC_UR (tabla dinámica, con estas columnas en filas).

### Verificación

- [ ] La pregunta se entiende y suena natural
- [ ] La lectura (etapa, año, alcance) es la correcta
- [ ] El SQL responde lo que se pregunta
- [ ] La cifra coincide con el recálculo
