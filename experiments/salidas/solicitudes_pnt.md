# Solicitudes de informacion de la PNT: lectura

Generado el 2026-09-21 09:26 por `experiments/leer_solicitudes_pnt.py`. Solo estadisticas: el texto de las solicitudes no se reproduce aqui.

## Archivos

| Archivo | Registros | JSON valido | Reparados | Irrecuperables | Folios unicos | Primera solicitud | Ultima |
|---|---:|---:|---:|---:|---:|---|---|
| `2024.JSON` | 3,212 | 2,876 | 336 | 0 | 3,212 | 20231221 | 20241218 |
| `2025.JSON` | 4,189 | 3,993 | 196 | 0 | 4,153 | 20241218 | 20251219 |
| `2026.JSON` | 3,051 | 2,880 | 171 | 0 | 3,051 | 20251219 | 20260918 |

Folios unicos: 10,416 de 10,452 registros.

## TipoSolicitud

| Valor | Registros |
|---|---:|
| Información pública | 10,128 |
| Datos Personales | 324 |

## TipoDerechoARCOP

| Valor | Registros |
|---|---:|
| No Aplica | 10,093 |
| Acceso | 336 |
| Rectificación | 9 |
| Oposición | 8 |
| Portabilidad | 5 |
| Cancelación | 1 |

## Dependencia

| Valor | Registros |
|---|---:|
| FED - Secretaría de Hacienda y Crédito Público (SHCP) | 5,543 |
| Secretaría de Hacienda y Crédito Público (SHCP) | 4,775 |
| FED-H - Secretaría de Hacienda y Crédito Público (SHCP) | 134 |

## Estatus

| Valor | Registros |
|---|---:|
| Terminada | 9,504 |
| Desechada por falta de respuesta del ciudadano | 374 |
| En proceso | 197 |
| Desechada por falta de selección del medio de entrega | 168 |
| Pendiente de acreditación de la identidad | 129 |
| En proceso con prórroga | 25 |
| Pendiente de entrega de respuesta | 16 |
| En espera de ampliación de información | 10 |
| Desechada por falta de pago | 7 |
| En espera de forma de entrega | 6 |
| Con pago realizado | 5 |
| En proceso, sin identidad acreditada | 3 |
| En proceso, información adicional | 2 |
| En proceso con prevención, sin identidad acreditada | 2 |
| Por registrar que se hizo efectivo el derecho | 1 |
| En proceso de entrega de informacion | 1 |
| En espera de pago | 1 |
| En proceso con prórroga, sin identidad acreditada | 1 |

## Respuesta

| Valor | Registros |
|---|---:|
| Entrega de información vía Plataforma Nacional de Transparencia (Terminada) | 4,654 |
| Inexistencia de información (Terminada) | 2,256 |
| Notoria incompetencia (Terminada) | 1,998 |
| Prevención | 326 |
| Información confidencial (Terminada) | 215 |
| Registro de la Solicitud | 193 |
| Disponibilidad de la información | 174 |
| Notificación de disponibilidad de respuesta (Previa acreditación) | 146 |
| Información disponible públicamente (Terminada) | 118 |
| Notoria incompetencia ARCOP (Terminada) | 92 |
| Información reservada (Terminada) | 76 |
| Prevención o existencia de un trámite | 58 |
| Notificación de lugar y fecha de entrega (Terminada) | 49 |
| Prórroga | 25 |
| Disposición de la información en consulta directa (Terminada) | 19 |
| Respuesta a la entrega de información, con costo | 13 |
| Registro del ejercicio de los derechos ARCOP (Terminada) | 11 |
| Inexistencia de los datos (Terminada) | 5 |
| Notificación de envío de la información (Terminada) | 5 |
| Registro manual de la solicitud de información pública | 4 |
| Improcedencia (Terminada) | 2 |
| Fe de Erratas | 2 |
| Desahogo de la prevención | 2 |
| Registro de la solicitud | 2 |
| Prevención desahogada sin aceptar trámite | 2 |
| Acceso en copia simple o certificada de forma gratuita | 1 |
| Entrega de información (Procedencia) | 1 |
| Respuesta a la entrega de información, sin costo | 1 |
| Prórroga ARCOP | 1 |
| Registro manual de la solicitud de datos personales | 1 |

## Candidatas para el conjunto de evaluacion

Solicitudes de informacion publica con al menos una palabra del nucleo: `presupuest`, `gasto`, `ejercid`, `devengad`, `erogac`, `erogad`, `cuenta publica`, `partida`, `programa presupuestario`. Se excluyen las de datos personales.

Orden de revision aleatorio y reproducible, con semilla `20260918` combinada con el nombre de cada archivo.

| Archivo | Candidatas |
|---|---:|
| `2024.JSON` | 773 |
| `2025.JSON` | 905 |
| `2026.JSON` | 621 |

## Solicitudes casi identicas

Dos candidatas son casi identicas si el indice de Jaccard entre sus conjuntos de palabras es de al menos 0.6. Detecta campanas con una misma plantilla y solicitudes que repiten una pregunta cambiando solo un dato (un estado, un municipio, una dependencia).

835 de 2,299 candidatas (36.3%) pertenecen a uno de 136 grupos. En la revision, solo el primer miembro de cada grupo que aparece en el orden aleatorio se evalua; los demas se registran como casi duplicados.

| Grupo | Solicitudes |
|---|---:|
| `G330026324000817` | 416 |
| `G330026324000902` | 26 |
| `G330026324001263` | 23 |
| `G340026300125125` | 21 |
| `G330026325000794` | 15 |
| `G340026300158426` | 13 |
| `G330026324003146` | 8 |
| `G330026324002435` | 7 |
| `G330026324000495` | 7 |
| `G330026324000940` | 6 |
| `G330026324001967` | 5 |
| `G330026324000188` | 5 |
| `G340026300112325` | 5 |
| `G340026300188126` | 5 |
| `G340026300232525` | 4 |
| `G340026300084725` | 4 |
| `G340026300288026` | 4 |
| `G340026300020426` | 4 |
| `G340026300071126` | 4 |
| `G330026324000431` | 3 |
| `G330026324000694` | 3 |
| `G330026324001123` | 3 |
| `G330026324003147` | 3 |
| `G330026324000344` | 3 |
| `G330026324000547` | 3 |
| `G330026324000174` | 3 |
| `G330026324000564` | 3 |
| `G330026324001620` | 3 |
| `G330026324001266` | 3 |
| `G340026300012125` | 3 |
| `G340026300081626` | 3 |
| `G340026300142625` | 3 |
| `G340026300101525` | 3 |
| `G340026300091425` | 3 |
| `G340026300118525` | 3 |
| `G340026300096325` | 3 |
| `G330026325001287` | 3 |
| `G340026300203526` | 3 |
| `G330026324002240` | 2 |
| `G330026324000916` | 2 |
| `G330026324003170` | 2 |
| `G330026324000928` | 2 |
| `G330026324000101` | 2 |
| `G330026324000021` | 2 |
| `G330026324000672` | 2 |
| `G330026324001810` | 2 |
| `G330026324002057` | 2 |
| `G330026324002889` | 2 |
| `G330026324001348` | 2 |
| `G330026324001359` | 2 |
| `G330026324002584` | 2 |
| `G330026324002656` | 2 |
| `G330026324001614` | 2 |
| `G330026324000861` | 2 |
| `G330026324000537` | 2 |
| `G330026324000043` | 2 |
| `G330026324000409` | 2 |
| `G330026324003082` | 2 |
| `G330026324000384` | 2 |
| `G330026324000723` | 2 |
| `G330026324002832` | 2 |
| `G330026324000718` | 2 |
| `G330026324002633` | 2 |
| `G330026324001284` | 2 |
| `G330026324000542` | 2 |
| `G330026324000692` | 2 |
| `G330026324002602` | 2 |
| `G330026324001174` | 2 |
| `G330026324001524` | 2 |
| `G330026324000142` | 2 |
| `G330026324001201` | 2 |
| `G330026324001447` | 2 |
| `G330026324001332` | 2 |
| `G330026324001634` | 2 |
| `G330026324001495` | 2 |
| `G330026325000689` | 2 |
| `G340026300108825` | 2 |
| `G340026300099525` | 2 |
| `G330026325000122` | 2 |
| `G340026300000825` | 2 |
| `G330026325000169` | 2 |
| `G340026300004126` | 2 |
| `G330026325000410` | 2 |
| `G340026300146225` | 2 |
| `G330026325000009` | 2 |
| `G330026325001128` | 2 |
| `G330026325001115` | 2 |
| `G340026300154225` | 2 |
| `G330026325000268` | 2 |
| `G330026325001189` | 2 |
| `G340026300195325` | 2 |
| `G340026300044725` | 2 |
| `G340026300238225` | 2 |
| `G340026300040325` | 2 |
| `G340026300066825` | 2 |
| `G330026325001154` | 2 |
| `G340026300052725` | 2 |
| `G340026300073425` | 2 |
| `G340026300039225` | 2 |
| `G330026325000895` | 2 |
| `G340026300200325` | 2 |
| `G340026300013125` | 2 |
| `G340026300162425` | 2 |
| `G340026300092925` | 2 |
| `G340026300204325` | 2 |
| `G340026300150725` | 2 |
| `G330026325000321` | 2 |
| `G340026300149825` | 2 |
| `G340026300257826` | 2 |
| `G340026300017126` | 2 |
| `G340026300235126` | 2 |
| `G340026300014126` | 2 |
| `G340026300165826` | 2 |
| `G340026300034926` | 2 |
| `G340026300245126` | 2 |
| `G340026300175726` | 2 |
| `G340026300228826` | 2 |
| `G340026300228626` | 2 |
| `G340026300214026` | 2 |
| `G340026300233026` | 2 |
| `G340026300002626` | 2 |
| `G340026300031526` | 2 |
| `G340026300037826` | 2 |
| `G340026300003326` | 2 |
| `G340026300025826` | 2 |
| `G340026300067726` | 2 |
| `G340026300066626` | 2 |
| `G340026300195526` | 2 |
| `G340026300262226` | 2 |
| `G340026300161726` | 2 |
| `G340026300031726` | 2 |
| `G340026300183226` | 2 |
| `G340026300032526` | 2 |
| `G340026300206426` | 2 |
| `G340026300167626` | 2 |
| `G340026300072826` | 2 |
