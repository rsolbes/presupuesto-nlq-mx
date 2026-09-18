-- ---------------------------------------------------------------------------
-- presupuesto-nlq-mx : capa semantica
--
-- Vistas con nombres legibles sobre el modelo en estrella. Es lo unico que ve
-- el sistema de consulta: resuelve de antemano los joins por llaves compuestas
-- y la traduccion de claves a descripciones, que es donde un modelo de lenguaje
-- mas se equivoca al generar SQL.
--
-- Requiere 01_esquema.sql.
-- Uso:  psql -d presupuesto_nlq -f src/sql/02_semantica.sql
-- ---------------------------------------------------------------------------


-- ===========================================================================
-- Capitulos del Clasificador por Objeto del Gasto
--
-- Los datos publicados traen la partida (cinco digitos) pero no el capitulo al
-- que pertenece, aunque "cuanto se gasto en servicios personales" es de las
-- preguntas mas naturales. El capitulo es el primer digito de la partida.
--
-- Fuente: Clasificador por Objeto del Gasto del Consejo Nacional de
-- Armonizacion Contable (CONAC).
-- Verificacion: los capitulos 1000 a 7000 coinciden con los que reporta la
-- Cuenta Publica 2024 en el estado analitico del ISSSTE
-- (data/raw/Verificacion/51GYN.03.F_OBJGASTO.xls). Los capitulos 8000 y 9000
-- no aparecen en ese documento porque el ISSSTE no ejerce gasto en ellos:
-- PENDIENTE verificarlos contra el clasificador vigente del CONAC antes de
-- citarlos en la tesis.
-- ===========================================================================

CREATE TABLE IF NOT EXISTS presupuesto.dim_capitulo (
    capitulo_id     integer PRIMARY KEY,
    capitulo_desc   text NOT NULL
);

INSERT INTO presupuesto.dim_capitulo (capitulo_id, capitulo_desc) VALUES
    (1000, 'Servicios personales'),
    (2000, 'Materiales y suministros'),
    (3000, 'Servicios generales'),
    (4000, 'Transferencias, asignaciones, subsidios y otras ayudas'),
    (5000, 'Bienes muebles, inmuebles e intangibles'),
    (6000, 'Inversion publica'),
    (7000, 'Inversiones financieras y otras provisiones'),
    (8000, 'Participaciones y aportaciones'),
    (9000, 'Deuda publica')
ON CONFLICT (capitulo_id) DO UPDATE SET capitulo_desc = EXCLUDED.capitulo_desc;

COMMENT ON TABLE presupuesto.dim_capitulo IS
    'Primer nivel del Clasificador por Objeto del Gasto (CONAC). Se deriva del '
    'primer digito de la partida; no viene en los datos publicados.';


-- ===========================================================================
-- Vista principal: semantica.gasto
--
-- Un renglon por renglon de la tabla de hechos, con todas las claves ya
-- traducidas. La mayoria de las preguntas se responden sobre esta sola vista,
-- sin joins: eso elimina la clase de error mas comun en la generacion de SQL
-- sobre este esquema, que es unir por una llave incompleta.
-- ===========================================================================

CREATE OR REPLACE VIEW semantica.gasto AS
SELECT
    h.ciclo                                             AS ejercicio,

    h.ramo_id                                           AS ramo_clave,
    r.ramo_desc                                         AS ramo,
    h.ur_id                                             AS unidad_responsable_clave,
    ur.ur_desc                                          AS unidad_responsable,

    fi.finalidad_desc                                   AS finalidad,
    fu.funcion_desc                                     AS funcion,
    sf.subfuncion_desc                                  AS subfuncion,

    ai.ai_desc                                          AS actividad_institucional,

    h.modalidad_id || lpad(h.pp_id::text, 3, '0')       AS programa_clave,
    pp.pp_desc                                          AS programa,
    mo.modalidad_desc                                   AS modalidad,

    ca.capitulo_id                                      AS capitulo_clave,
    ca.capitulo_desc                                    AS capitulo,
    h.partida_id                                        AS partida_clave,
    pa.partida_desc                                     AS partida,

    tg.tipogasto_desc                                   AS tipo_de_gasto,
    ff.ff_desc                                          AS fuente_de_financiamiento,
    ef.entidad_desc                                     AS entidad_federativa,
    h.cartera_id                                        AS proyecto_de_inversion_clave,

    h.aprobado,
    h.modificado,
    h.devengado,
    h.pagado,
    h.ejercido,
    h.adefas
FROM presupuesto.hecho_gasto h
JOIN presupuesto.dim_ramo r
    ON r.ramo_id = h.ramo_id
JOIN presupuesto.dim_unidad_responsable ur
    ON ur.ramo_id = h.ramo_id AND ur.ur_id = h.ur_id
JOIN presupuesto.dim_finalidad fi
    ON fi.finalidad_id = h.finalidad_id
JOIN presupuesto.dim_funcion fu
    ON fu.finalidad_id = h.finalidad_id AND fu.funcion_id = h.funcion_id
JOIN presupuesto.dim_subfuncion sf
    ON sf.finalidad_id = h.finalidad_id
   AND sf.funcion_id = h.funcion_id
   AND sf.subfuncion_id = h.subfuncion_id
JOIN presupuesto.dim_actividad_institucional ai
    ON ai.ramo_id = h.ramo_id AND ai.ai_id = h.ai_id
JOIN presupuesto.dim_modalidad mo
    ON mo.modalidad_id = h.modalidad_id
JOIN presupuesto.dim_programa_presupuestario pp
    ON pp.ramo_id = h.ramo_id
   AND pp.modalidad_id = h.modalidad_id
   AND pp.pp_id = h.pp_id
JOIN presupuesto.dim_partida pa
    ON pa.partida_id = h.partida_id
JOIN presupuesto.dim_capitulo ca
    ON ca.capitulo_id = (h.partida_id / 10000) * 1000
JOIN presupuesto.dim_tipo_gasto tg
    ON tg.tipogasto_id = h.tipogasto_id
JOIN presupuesto.dim_fuente_financiamiento ff
    ON ff.ff_id = h.ff_id
JOIN presupuesto.dim_entidad_federativa ef
    ON ef.entidad_id = h.entidad_id;

COMMENT ON VIEW semantica.gasto IS
    'Gasto del Gobierno Federal por ejercicio fiscal (2020 a 2025), con todas '
    'las clasificaciones traducidas a su nombre. Fuente: Cuenta Publica, Estado '
    'Analitico del Ejercicio del Presupuesto de Egresos. Importes en pesos.';

COMMENT ON COLUMN semantica.gasto.ejercicio IS
    'Ano fiscal. Disponibles: 2020 a 2025.';
COMMENT ON COLUMN semantica.gasto.ramo IS
    'Dependencia o ramo que ejerce el gasto. Ejemplos: Salud, Educacion Publica, '
    'Instituto de Seguridad y Servicios Sociales de los Trabajadores del Estado.';
COMMENT ON COLUMN semantica.gasto.programa_clave IS
    'Clave publica del programa, como aparece en documentos oficiales (E023, '
    'S072). ATENCION: no es unica. La misma clave corresponde a programas '
    'distintos en ramos distintos; filtrar tambien por ramo.';
COMMENT ON COLUMN semantica.gasto.capitulo IS
    'En que se gasta, a nivel agregado: servicios personales (nomina), '
    'materiales, servicios generales, transferencias, inversion, deuda, etc.';
COMMENT ON COLUMN semantica.gasto.entidad_federativa IS
    'Destino geografico del gasto. Buena parte del gasto federal no es '
    'distribuible por entidad y aparece con una clave propia.';
COMMENT ON COLUMN semantica.gasto.aprobado IS
    'Presupuesto aprobado por la Camara de Diputados, en pesos.';
COMMENT ON COLUMN semantica.gasto.modificado IS
    'Presupuesto aprobado mas las adecuaciones del ejercicio, en pesos.';
COMMENT ON COLUMN semantica.gasto.devengado IS
    'Gasto reconocido como obligacion de pago, en pesos. Es la etapa que suele '
    'entenderse por "lo que se gasto". Si la pregunta no especifica etapa, es '
    'ambigua: el resultado cambia segun se use aprobado, devengado o pagado.';
COMMENT ON COLUMN semantica.gasto.pagado IS
    'Gasto efectivamente pagado, en pesos.';
COMMENT ON COLUMN semantica.gasto.ejercido IS
    'Gasto con cuenta por liquidar certificada emitida, en pesos.';
COMMENT ON COLUMN semantica.gasto.adefas IS
    'Adeudos de ejercicios anteriores pagados con presupuesto de este ejercicio.';
