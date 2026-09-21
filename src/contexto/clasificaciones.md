# Documentación de clasificaciones y reglas de interpretación

Versión 1 · 2026-09-21 · Base: `semantica.gasto`, Cuenta Pública federal 2020 a 2025.

## 1. Qué contiene la base

La vista `semantica.gasto` contiene el gasto del Gobierno Federal registrado en la Cuenta Pública, en el Estado Analítico del Ejercicio del Presupuesto de Egresos, para los ejercicios fiscales 2020 a 2025. Cada renglón es una combinación única de clasificaciones dentro de un ejercicio; una misma dependencia o un mismo programa ocupa muchos renglones, por lo que las cifras se obtienen siempre con `sum()`.

Los importes están en pesos corrientes, sin descontar la inflación. Para expresarlos en millones de pesos se divide entre 1,000,000. Una comparación entre ejercicios es nominal salvo que la pregunta pida otra cosa, y la respuesta debe decirlo.

La base **no** contiene:

- ejercicios anteriores a 2020 ni posteriores a 2025;
- desagregación por municipio, localidad, obra, evento, contrato o proveedor;
- ingresos, recaudación ni el origen de los recursos por impuesto;
- saldos: ni de la deuda pública, ni de fideicomisos, fondos o cuentas;
- reintegros a la Tesorería de la Federación ni remanentes de fideicomisos;
- presupuestos estatales o municipales propios;
- cifras mensuales o trimestrales: solo el cierre anual.

Si una pregunta requiere alguno de estos datos, la base no permite responderla y el sistema debe decirlo en lugar de aproximar con otra cifra.

## 2. Etapas del gasto

Cada renglón registra seis importes, que corresponden a momentos distintos del gasto:

| Columna | Significado |
|---|---|
| `aprobado` | Presupuesto aprobado por la Cámara de Diputados en el Presupuesto de Egresos de la Federación. |
| `modificado` | Aprobado más las adecuaciones presupuestarias realizadas durante el ejercicio. |
| `devengado` | Obligación de pago reconocida por haber recibido bienes, servicios u obras. Es lo que suele entenderse por "lo que se gastó". |
| `ejercido` | Gasto con cuenta por liquidar certificada o documento equivalente emitido. |
| `pagado` | Gasto efectivamente pagado. |
| `adefas` | Adeudos de ejercicios fiscales anteriores: obligaciones devengadas en un año y pagadas al siguiente. |

Las palabras de una pregunta se traducen a etapas así:

| Palabras en la pregunta | Columna |
|---|---|
| asignado, autorizado, aprobado, presupuestado, destinado, previsto | `aprobado` |
| modificado | `modificado` |
| ejercido, ejecutado | `ejercido` |
| devengado | `devengado` |
| pagado, entregado, transferido, proporcionado, dispersado | `pagado` |
| gasto, gastado, erogado, costó, sin etapa identificable | ambigua |

Cuando la etapa es ambigua, las respuestas difieren según la columna elegida. El sistema debe señalar la ambigüedad o declarar qué etapa usó.

Relaciones entre etapas que conviene conocer:

- **Subejercicio** es `modificado - devengado`. En muchas dependencias resulta cero, porque el presupuesto modificado se ajusta al devengado al cierre del ejercicio.
- En las dependencias y los ramos generales, `ejercido` coincide prácticamente con `devengado`, y `pagado` es algo menor: la diferencia son obligaciones que se pagan después del cierre.
- En los ramos 50 a 53 (IMSS, ISSSTE, Pemex y CFE), que se financian también con ingresos propios, estas relaciones no se cumplen: el devengado puede superar al modificado y el ejercido puede diferir del devengado en ambos sentidos.

## 3. Clasificación administrativa: quién gasta

- `ramo_clave`, `ramo`: el primer nivel. Un ramo es una dependencia (Salud, 12), un poder u órgano autónomo (Poder Legislativo, 1; Instituto Nacional Electoral, 22) o un ramo general que no corresponde a una dependencia.
- `unidad_responsable_clave`, `unidad_responsable`: el área o entidad dentro del ramo que ejerce el gasto. La clave de unidad responsable **no es única entre ramos**: se filtra siempre junto con `ramo_clave`.

Ramos que requieren atención:

| Ramo | Nombre | Qué registra |
|---|---|---|
| 19 | Aportaciones a Seguridad Social | Aportaciones del Gobierno Federal a la seguridad social, incluidas pensiones. |
| 23 | Provisiones Salariales y Económicas | Provisiones y erogaciones que no corresponden a una dependencia, como el subsidio a las tarifas eléctricas y las aportaciones a fondos de estabilización. |
| 24 | Deuda Pública | El **costo financiero** de la deuda (intereses, comisiones y gastos). No es el saldo de la deuda. |
| 25 | Previsiones y Aportaciones para los Sistemas de Educación Básica, Normal, Tecnológica y de Adultos | Principalmente el gasto de la Autoridad Educativa Federal en la Ciudad de México. |
| 28 | Participaciones a Entidades Federativas y Municipios | Participaciones: recursos federales de libre uso para estados y municipios. |
| 30 | Adeudos de Ejercicios Fiscales Anteriores | Pago de adeudos de años anteriores, como ramo. No confundir con la columna `adefas`. |
| 33 | Aportaciones Federales para Entidades Federativas y Municipios | Fondos de aportaciones: recursos federales con destino específico (ver sección 7). |
| 34 | Erogaciones para los Programas de Apoyo a Ahorradores y Deudores de la Banca | Apoyos a ahorradores y deudores de la banca. |
| 47 | Entidades no Sectorizadas | Entidades sin sector; desde 2023 incluye a IMSS-Bienestar. |
| 50 | Instituto Mexicano del Seguro Social | Entidad de control directo. |
| 51 | Instituto de Seguridad y Servicios Sociales de los Trabajadores del Estado | Entidad de control directo. |
| 52 | Petróleos Mexicanos | Empresa productiva del Estado. |
| 53 | Comisión Federal de Electricidad | Empresa productiva del Estado. |

Cambios de nombre y de estructura: la base usa el nombre más reciente de cada ramo. El ramo 9 se llamaba Comunicaciones y Transportes hasta 2023; el ramo 27, Función Pública hasta 2024; y el ramo 38, Consejo Nacional de Ciencia y Tecnología hasta 2023. Los ramos 54 (Mujeres) y 55 (Agencia de Transformación Digital y Telecomunicaciones) solo existen en 2025. Una pregunta que use un nombre anterior se refiere al mismo ramo.

Los servicios de salud para personas sin seguridad social se trasladaron a IMSS-Bienestar, que aparece como unidad responsable `AYO` del ramo 47 a partir de 2023. Por eso el presupuesto del ramo 12, Salud, cae a partir de 2024. Una pregunta sobre "el presupuesto de salud" no equivale al ramo 12 (ver también la sección 4).

## 4. Clasificación funcional: para qué se gasta

Tiene tres niveles jerárquicos: `finalidad` (4 valores), `funcion` (28 combinaciones) y `subfuncion` (91 combinaciones). Las finalidades son Gobierno, Desarrollo Social, Desarrollo Económico y Otras no Clasificadas en Funciones Anteriores.

La clasificación funcional es **independiente** de la administrativa. La función Salud reúne el gasto en salud de todos los ramos (Salud, IMSS, ISSSTE, IMSS-Bienestar y otros), mientras que el ramo 12 es solo una dependencia. Lo mismo ocurre con la función Educación y el ramo 11. Cuando una pregunta dice "sector salud" o "gasto en educación" sin más precisión, admite las dos lecturas, con cifras muy distintas.

## 5. Clasificación programática: mediante qué programa

- `programa_clave`: clave pública del programa presupuestario, como aparece en los documentos oficiales: una letra de modalidad seguida de tres dígitos (E023, S072, U006).
- `programa`: nombre del programa.
- `modalidad`: tipo de programa, que corresponde a la letra de la clave. Por ejemplo, S es Sujetos a Reglas de Operación, U es Otros Subsidios, E es Prestación de Servicios Públicos, K es Proyectos de Inversión, I es Gasto Federalizado y C es Participaciones.
- `actividad_institucional`: agrupación intermedia de las acciones de cada ramo.

Reglas:

- La clave de programa **no es única entre ramos**: la misma clave corresponde a programas distintos en ramos distintos. Se filtra por `ramo_clave` y `programa_clave` juntos, o se agrupa por ramo, clave y nombre.
- Un mismo programa puede cambiar de clave entre ejercicios, e incluso tener dos claves en un mismo ejercicio mientras cambia de modalidad. Para seguir un programa a lo largo de varios años es más seguro filtrar por nombre dentro del ramo que por una sola clave, y comprobar qué claves aparecen.

## 6. Clasificación por objeto del gasto: en qué se gasta

Sigue el Clasificador por Objeto del Gasto del CONAC, con tres niveles derivables de la base:

- `capitulo_clave`, `capitulo`: primer nivel, de 1000 a 9000.
- Concepto: segundo nivel, no tiene columna propia. Son los dos primeros dígitos de la partida: `partida_clave / 1000` devuelve 36 para la partida 36101, que pertenece al concepto 3600.
- `partida_clave`, `partida`: nivel más detallado, de cinco dígitos.

| Capítulo | Nombre |
|---:|---|
| 1000 | Servicios personales (sueldos, prestaciones, nómina) |
| 2000 | Materiales y suministros |
| 3000 | Servicios generales |
| 4000 | Transferencias, asignaciones, subsidios y otras ayudas |
| 5000 | Bienes muebles, inmuebles e intangibles |
| 6000 | Inversión pública |
| 7000 | Inversiones financieras y otras provisiones |
| 8000 | Participaciones y aportaciones |
| 9000 | Deuda pública |

Algunos términos de uso común corresponden a conceptos con nombre oficial distinto: la publicidad oficial es el concepto 3600, Servicios de comunicación social y publicidad; la nómina es el capítulo 1000.

## 7. Fondos de aportaciones y participaciones

La base nombra los fondos del ramo 33 por su sigla. Equivalencias:

| Sigla | Fondo | Claves |
|---|---|---|
| FONE | Fondo de Aportaciones para la Nómina Educativa y Gasto Operativo | I013 a I016 |
| FASSA | Fondo de Aportaciones para los Servicios de Salud | I002 |
| FAIS | Fondo de Aportaciones para la Infraestructura Social (estatal y municipal) | I003, I004 |
| FORTAMUN | Fondo de Aportaciones para el Fortalecimiento de los Municipios y de las Demarcaciones Territoriales del Distrito Federal | I005 |
| FAM | Fondo de Aportaciones Múltiples | I006 a I008 |
| FAETA | Fondo de Aportaciones para la Educación Tecnológica y de Adultos | I009, I010 |
| FASP | Fondo de Aportaciones para la Seguridad Pública de los Estados y del Distrito Federal | I011 |
| FAFEF | Fondo de Aportaciones para el Fortalecimiento de las Entidades Federativas | I012 |
| FAISPIAM | Fondo de Aportaciones para la Infraestructura Social de los Pueblos y Comunidades Indígenas y Afromexicanas | I017, solo 2025 |

Un fondo con varias claves se suma completo salvo que la pregunta pida uno de sus componentes.

Las **participaciones** (ramo 28: Fondo General de Participaciones, Fondo de Fomento Municipal y otros) y las **aportaciones** (ramo 33) son distintas: las primeras son de libre uso para los gobiernos locales y las segundas tienen destino específico. "Lo que la Federación le dio a un estado" puede referirse a una, a otra o a ambas.

## 8. Clasificación geográfica: dónde se gasta

`entidad_federativa` contiene las 32 entidades más dos valores que **no son entidades**: `En El Extranjero` y `No Distribuible Geográficamente`. Deben excluirse al comparar o jerarquizar entidades.

Reglas:

- El gasto se asigna a la entidad donde se registra, no necesariamente donde se beneficia la población. Las dependencias con oficinas centrales en la capital registran ahí buena parte de su gasto, por lo que la Ciudad de México concentra una proporción del gasto muy superior a su población.
- Una parte del gasto federal no tiene destino geográfico asignado. La suma por entidades es, por tanto, menor que el total.
- La base no desagrega por municipio.

Los nombres se escriben con acentos y en su forma corta: `Michoacán`, `Estado de México`, `Veracruz`, `Coahuila`, `Ciudad de México`.

## 9. Clasificación económica y fuente de financiamiento

`tipo_de_gasto` distingue la naturaleza económica: gasto corriente, pensiones y jubilaciones, gasto de obra pública, gasto de capital diferente de obra pública, participaciones y variantes de gastos indirectos y de recursos otorgados a fideicomisos. Una pregunta por el "gasto de capital" o el "gasto de inversión" en sentido económico reúne el gasto de obra pública y el de capital diferente de obra pública, más las variantes de inversión de gastos indirectos y de fideicomisos.

`fuente_de_financiamiento` distingue el origen de los recursos: recursos fiscales, ingresos propios, recursos fiscales derivados de ingresos excedentes, financiamientos externos (BID-BIRF y otros), contraparte nacional y pasivos de años anteriores. No identifica impuestos específicos.

## 10. Totales: gasto bruto y gasto neto

La suma de cualquier etapa sobre toda la base es gasto **bruto**: cuenta dos veces los recursos que pasan de un ente público a otro, por ejemplo las aportaciones del Gobierno Federal a la seguridad social que después ejercen el IMSS o el ISSSTE. Por eso no coincide con el gasto neto total que publican el Presupuesto de Egresos y la Cuenta Pública, que elimina esas duplicaciones. Si una pregunta cita el gasto neto total o pide reproducirlo, el sistema debe señalar que la base contiene cifras brutas.
