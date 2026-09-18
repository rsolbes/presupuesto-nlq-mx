-- ---------------------------------------------------------------------------
-- presupuesto-nlq-mx : rol de solo lectura para el sistema de consulta
--
-- El sistema ejecuta SQL generado por un modelo de lenguaje. Aunque el SQL se
-- valida antes de ejecutarse, la base no debe depender de que esa validacion
-- funcione. Este rol aporta dos tipos de proteccion que conviene no confundir:
--
-- BARRERA (la sesion no puede quitarla):
--   - Privilegios. Solo SELECT sobre los esquemas de vistas; ningun acceso a
--     las tablas base; ningun permiso de crear ni escribir, incluidas las
--     tablas temporales. Verificado: leer presupuesto.hecho_gasto devuelve
--     SQLSTATE 42501.
--   - Solo puede conectarse a presupuesto_nlq, no a otras bases del servidor.
--   - Maximo 5 conexiones simultaneas.
--
-- Verificacion reproducible: tests/verificar_rol_consulta.py
--
-- BARANDALES (evitan accidentes, pero la propia sesion puede cambiarlos con
-- SET, BEGIN READ WRITE o set_config()):
--   - Transacciones de solo lectura por defecto (SQLSTATE 25006 al escribir).
--   - Tiempo limite de 15 segundos por sentencia.
--
-- Consecuencia de diseno: la capa de orquestacion debe imponer su propio
-- tiempo limite desde el cliente, y el validador de SQL debe rechazar SET y
-- las llamadas a set_config(). La seguridad frente a escritura no depende de
-- los barandales: aun con el modo de solo lectura desactivado, los privilegios
-- siguen rechazando cualquier escritura.
--
-- Por que funciona sin permisos sobre las tablas base: en PostgreSQL una vista
-- se ejecuta con los privilegios de su DUENO, no de quien la consulta. El rol
-- puede leer semantica.gasto aunque no tenga acceso a presupuesto.hecho_gasto.
-- Esa es exactamente la propiedad que buscamos: la capa semantica es la unica
-- puerta de entrada.
--
-- Requiere 02_semantica.sql. Correr como el usuario administrador.
-- Uso:  psql -d presupuesto_nlq -f src/sql/03_rol_consulta.sql
--
-- CONTRASENA: este script crea el rol SIN contrasena, a proposito, para que
-- nunca quede escrita en un archivo versionado. Asignala a mano despues:
--     ALTER ROLE consulta_nlq PASSWORD '...';
-- ---------------------------------------------------------------------------

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'consulta_nlq') THEN
        CREATE ROLE consulta_nlq LOGIN;
    END IF;
END
$$;

COMMENT ON ROLE consulta_nlq IS
    'Rol del sistema de consulta en lenguaje natural. Solo lectura, solo el '
    'esquema semantica.';

-- Barandales: valores por defecto de cada sesion del rol. La sesion puede
-- cambiarlos; no son la barrera de seguridad (ver encabezado).
ALTER ROLE consulta_nlq SET default_transaction_read_only = on;
ALTER ROLE consulta_nlq SET statement_timeout = '15s';
ALTER ROLE consulta_nlq CONNECTION LIMIT 5;

-- Nada sobre las tablas base.
REVOKE ALL ON SCHEMA presupuesto FROM consulta_nlq;
REVOKE ALL ON ALL TABLES IN SCHEMA presupuesto FROM consulta_nlq;

-- Confinar el rol a esta base. Por defecto PostgreSQL concede a PUBLIC, es
-- decir a todo rol, permiso de conectarse a cualquier base del servidor y de
-- crear tablas temporales en ella. Se retiran ambos. Los superusuarios y el
-- dueno de cada base no se ven afectados.
REVOKE CONNECT, TEMPORARY ON DATABASE presupuesto_nlq FROM PUBLIC;
REVOKE CONNECT ON DATABASE postgres  FROM PUBLIC;
REVOKE CONNECT ON DATABASE template1 FROM PUBLIC;

-- Solo lectura sobre la capa semantica, incluidas las vistas que se creen despues.
GRANT CONNECT ON DATABASE presupuesto_nlq TO consulta_nlq;
GRANT USAGE ON SCHEMA semantica TO consulta_nlq;
GRANT SELECT ON ALL TABLES IN SCHEMA semantica TO consulta_nlq;
ALTER DEFAULT PRIVILEGES IN SCHEMA semantica GRANT SELECT ON TABLES TO consulta_nlq;
