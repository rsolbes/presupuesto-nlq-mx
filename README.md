# presupuesto-nlq-mx

Sistema de consulta en lenguaje natural sobre informacion presupuestaria publica de Mexico: traduccion de preguntas a SQL sobre datos de la SHCP y recuperacion aumentada sobre normatividad, con el SQL ejecutado o la cita documental siempre a la vista.

Tesis de licenciatura en Ingenieria, Facultad de Ingenieria Tampico, Universidad Autonoma de Tamaulipas.

> **Titulo del trabajo:** Sistema de consulta en lenguaje natural para informacion presupuestaria publica mediante modelos de lenguaje y recuperacion de informacion.

## Que resuelve

La informacion presupuestaria publica mexicana esta publicada en formatos abiertos, pero interpretarla exige conocimientos de analisis de datos y de contabilidad gubernamental. Ademas esta partida en dos naturalezas: las cifras viven en bases estructuradas y las reglas y definiciones viven en documentos normativos. Este sistema recibe preguntas en espanol y las resuelve por una de dos rutas, decididas por un enrutador:

1. **Ruta de datos (text-to-SQL).** Traduce la pregunta a SQL, lo valida, lo ejecuta con permisos de solo lectura y devuelve la tabla de resultados junto con la consulta ejecutada.
2. **Ruta documental (RAG).** Recupera fragmentos de documentos oficiales y genera una respuesta con citas verificables a su fuente.

El sistema se abstiene cuando la informacion disponible no permite responder.

## Organizacion del repositorio

| Ruta | Contenido |
|---|---|
| `src/` | Codigo del sistema: almacen estructurado, indice documental, orquestacion, interfaz |
| `experiments/` | Codigo de experimentacion y registros de cada corrida. Deliberadamente separado de `src/` |
| `eval/` | Conjunto de evaluacion: preguntas, ruta correcta, respuesta y evidencia de referencia |
| `data/` | Datos originales y derivados. **El contenido no se versiona** (ver abajo) |
| `docs/` | Documento de tesis y bitacora de decisiones |

## Convencion sobre los datos

Los archivos de `data/` estan excluidos del control de versiones por peso y por licencia de redistribucion. Lo que si se versiona es **como obtenerlos**: cada subcarpeta de `data/raw/` lleva un `PROCEDENCIA.md` con la URL de origen, la fecha de descarga y el hash del archivo. Esto importa porque los portales oficiales actualizan sus publicaciones, y sin ese registro los resultados dejan de ser reproducibles.

El portal de la SHCP bloquea el acceso automatizado: las descargas son manuales.

## Estado

Fase 1 (preparacion de datos), iniciando. El cronograma completo esta en `CLAUDE.md`.
