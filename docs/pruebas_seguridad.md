# Verificacion del rol de solo lectura

Generado el 2026-09-21 10:54 por `tests/verificar_rol_consulta.py`, conectado como `consulta_nlq` a `presupuesto_nlq`.

Cada prueba compara el resultado contra un valor o un codigo SQLSTATE concreto: una prueba que falla por una razon distinta a la esperada cuenta como fallida.

Una **barrera** no puede quitarla la propia sesion (privilegios, confinamiento a la base). Una **salvaguarda** si puede cambiarse desde la sesion (`SET`, `BEGIN READ WRITE`, `set_config`), por lo que evita accidentes pero no es frontera de seguridad: la capa de orquestacion debe imponer su propio tiempo limite y rechazar `SET` y `set_config`.

| Prueba | Tipo | Esperado | Obtenido | Resultado | Que demuestra |
|---|---|---|---|---|---|
| identidad | control | valor `consulta_nlq` | valor `consulta_nlq` | paso | la prueba corre realmente como el rol |
| lee la capa semantica | acceso | valor `1` | valor `1` | paso | acceso a lo que el sistema necesita |
| lee el esquema crudo | acceso | valor `1` | valor `1` | paso | acceso a la condicion de control experimental |
| no lee las tablas base | barrera | SQLSTATE `42501` | SQLSTATE `42501` | paso | las tablas base solo son alcanzables a traves de vistas |
| no escribe aun sin solo lectura | barrera | SQLSTATE `42501` | SQLSTATE `42501` | paso | los privilegios detienen la escritura aunque se desactive la salvaguarda |
| no crea tablas temporales | barrera | SQLSTATE `42501` | SQLSTATE `42501` | paso | sin permiso TEMPORARY sobre la base |
| confinado a su base | barrera | conexion rechazada | error: connection failed: connection to server at "127.0.0.1", port 5432 failed: FATAL:  permiso denegado a la base de datos �postgres� | paso | no puede conectarse a otras bases del servidor |
| solo lectura por defecto | salvaguarda | valor `on` | valor `on` | paso | toda transaccion inicia en solo lectura |
| escritura bloqueada por defecto | salvaguarda | SQLSTATE `25006` | SQLSTATE `25006` | paso | la salvaguarda detiene la escritura antes que los privilegios |
| tiempo limite configurado | salvaguarda | valor `15s` | valor `15s` | paso | limite por sentencia |
| tiempo limite efectivo | salvaguarda | SQLSTATE `57014` | SQLSTATE `57014` | paso | una sentencia de 20 s se cancela a los 15 s |

Codigos SQLSTATE: `42501` privilegio insuficiente; `25006` escritura en transaccion de solo lectura; `57014` sentencia cancelada por tiempo limite.
