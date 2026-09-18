-- ---------------------------------------------------------------------------
-- presupuesto-nlq-mx : esquema crudo (condicion de control experimental)
--
-- Expone el modelo en estrella tal como esta, sin la ayuda de la capa
-- semantica: claves numericas, joins por llaves compuestas a cargo de quien
-- consulta, sin capitulo derivado ni clave publica de programa.
--
-- Existe para medir cuanto aporta la capa semantica. La configuracion 1 del
-- experimento de text-to-SQL ("solo esquema") se corre dos veces: una contra
-- este esquema y otra contra semantica. La diferencia de exactitud de
-- ejecucion entre ambas es la contribucion directa de la capa semantica.
--
-- Las vistas son de paso directo (SELECT de las tablas base) y no llevan
-- comentarios: en la condicion de control el modelo solo recibe la estructura.
-- Se omiten a proposito dim_capitulo, que es un enriquecimiento de la capa
-- semantica, y descripcion_historica, que es de auditoria.
--
-- El rol consulta_nlq lee estas vistas, igual que las de semantica: la
-- seguridad no cambia, el sistema sigue tocando unicamente vistas.
--
-- Requiere 03_rol_consulta.sql.
-- Uso:  psql -d presupuesto_nlq -f src/sql/04_esquema_crudo.sql
-- ---------------------------------------------------------------------------

CREATE SCHEMA IF NOT EXISTS crudo;

COMMENT ON SCHEMA crudo IS
    'Condicion de control experimental: el modelo en estrella sin capa '
    'semantica. No usar fuera de los experimentos.';

CREATE OR REPLACE VIEW crudo.hecho_gasto AS
    SELECT ciclo, ramo_id, ur_id, finalidad_id, funcion_id, subfuncion_id,
           ai_id, modalidad_id, pp_id, partida_id, tipogasto_id, ff_id,
           entidad_id, cartera_id,
           aprobado, modificado, devengado, pagado, adefas, ejercido
    FROM presupuesto.hecho_gasto;

CREATE OR REPLACE VIEW crudo.dim_ramo                    AS SELECT * FROM presupuesto.dim_ramo;
CREATE OR REPLACE VIEW crudo.dim_unidad_responsable      AS SELECT * FROM presupuesto.dim_unidad_responsable;
CREATE OR REPLACE VIEW crudo.dim_finalidad               AS SELECT * FROM presupuesto.dim_finalidad;
CREATE OR REPLACE VIEW crudo.dim_funcion                 AS SELECT * FROM presupuesto.dim_funcion;
CREATE OR REPLACE VIEW crudo.dim_subfuncion              AS SELECT * FROM presupuesto.dim_subfuncion;
CREATE OR REPLACE VIEW crudo.dim_actividad_institucional AS SELECT * FROM presupuesto.dim_actividad_institucional;
CREATE OR REPLACE VIEW crudo.dim_modalidad               AS SELECT * FROM presupuesto.dim_modalidad;
CREATE OR REPLACE VIEW crudo.dim_programa_presupuestario AS SELECT * FROM presupuesto.dim_programa_presupuestario;
CREATE OR REPLACE VIEW crudo.dim_partida                 AS SELECT * FROM presupuesto.dim_partida;
CREATE OR REPLACE VIEW crudo.dim_tipo_gasto              AS SELECT * FROM presupuesto.dim_tipo_gasto;
CREATE OR REPLACE VIEW crudo.dim_fuente_financiamiento   AS SELECT * FROM presupuesto.dim_fuente_financiamiento;
CREATE OR REPLACE VIEW crudo.dim_entidad_federativa      AS SELECT * FROM presupuesto.dim_entidad_federativa;

GRANT USAGE ON SCHEMA crudo TO consulta_nlq;
GRANT SELECT ON ALL TABLES IN SCHEMA crudo TO consulta_nlq;
