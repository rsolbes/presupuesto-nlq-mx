-- ---------------------------------------------------------------------------
-- presupuesto-nlq-mx : esquema base
--
-- PostgreSQL. Modelo en estrella sobre la Cuenta Publica federal, ejercicios
-- 2020 a 2025.
--
-- Dos esquemas:
--   presupuesto  tablas base. Solo el usuario de carga escribe aqui.
--   semantica    vistas con nombres legibles. Es lo unico que ve el sistema
--                de consulta y el usuario de solo lectura.
--
-- Los tipos de las columnas de clave se eligieron a partir del perfilado de
-- 1,285,233 renglones, no por convencion:
--   ur_id        590,407 valores alfanumericos (G00, GYN, K00)  -> texto
--   modalidad_id siempre una letra                              -> texto
--   cartera_id   643,609 valores con ceros a la izquierda y
--                13,781 alfanumericos (1906A000001)             -> texto
--   partida_id   llega a 99101, no cabe en smallint             -> integer
-- Declarar cualquiera de las tres primeras como numerica destruiria claves.
--
-- Uso:  psql -d presupuesto_nlq -f src/sql/01_esquema.sql
-- ---------------------------------------------------------------------------

CREATE SCHEMA IF NOT EXISTS presupuesto;
CREATE SCHEMA IF NOT EXISTS semantica;

SET search_path = presupuesto, public;


-- ===========================================================================
-- Dimensiones conformadas
--
-- Una fila por llave natural, con la descripcion del ejercicio mas reciente en
-- que aparece; si en ese ejercicio hay varias, la mas usada. Las variantes
-- historicas viven en descripcion_historica.
--
-- Las llaves compuestas no son preferencia de diseno: son necesarias. La clave
-- de programa presupuestario por si sola apunta a hasta 19 programas distintos
-- segun el ramo; la de unidad responsable se repite entre ramos. Verificado en
-- los seis ejercicios.
-- ===========================================================================

CREATE TABLE dim_ramo (
    ramo_id     smallint PRIMARY KEY,
    ramo_desc   text NOT NULL
);
COMMENT ON TABLE  dim_ramo IS
    'Clasificacion administrativa de primer nivel: quien ejerce el gasto. '
    'Dependencia, entidad o ramo general.';
COMMENT ON COLUMN dim_ramo.ramo_id IS
    'Numero de ramo del catalogo de claves presupuestarias. Ejemplo: 12 = Salud.';

CREATE TABLE dim_unidad_responsable (
    ramo_id     smallint    NOT NULL REFERENCES dim_ramo (ramo_id),
    ur_id       varchar(3)  NOT NULL,
    ur_desc     text        NOT NULL,
    PRIMARY KEY (ramo_id, ur_id)
);
COMMENT ON TABLE  dim_unidad_responsable IS
    'Unidad administrativa dentro de un ramo que ejerce el gasto. La clave solo '
    'es unica dentro de su ramo: ur_id por si sola se repite entre ramos.';

CREATE TABLE dim_finalidad (
    finalidad_id    smallint PRIMARY KEY,
    finalidad_desc  text NOT NULL
);
COMMENT ON TABLE dim_finalidad IS
    'Primer nivel de la clasificacion funcional: para que fin se gasta. '
    'Gobierno, Desarrollo Social, Desarrollo Economico y Otras.';

CREATE TABLE dim_funcion (
    finalidad_id    smallint NOT NULL REFERENCES dim_finalidad (finalidad_id),
    funcion_id      smallint NOT NULL,
    funcion_desc    text     NOT NULL,
    PRIMARY KEY (finalidad_id, funcion_id)
);
COMMENT ON TABLE dim_funcion IS
    'Segundo nivel de la clasificacion funcional. funcion_id solo toma valores '
    'del 1 al 9 y unicamente identifica dentro de su finalidad.';

CREATE TABLE dim_subfuncion (
    finalidad_id    smallint NOT NULL,
    funcion_id      smallint NOT NULL,
    subfuncion_id   smallint NOT NULL,
    subfuncion_desc text     NOT NULL,
    PRIMARY KEY (finalidad_id, funcion_id, subfuncion_id),
    FOREIGN KEY (finalidad_id, funcion_id)
        REFERENCES dim_funcion (finalidad_id, funcion_id)
);
COMMENT ON TABLE dim_subfuncion IS
    'Tercer nivel de la clasificacion funcional. Requiere las tres claves: '
    'subfuncion_id sola toma 9 valores que describen 88 subfunciones distintas.';

CREATE TABLE dim_actividad_institucional (
    ramo_id     smallint NOT NULL REFERENCES dim_ramo (ramo_id),
    ai_id       smallint NOT NULL,
    ai_desc     text     NOT NULL,
    PRIMARY KEY (ramo_id, ai_id)
);
COMMENT ON TABLE dim_actividad_institucional IS
    'Conjunto de acciones sustantivas o de apoyo de las unidades responsables. '
    'Unica dentro del ramo.';

CREATE TABLE dim_modalidad (
    modalidad_id    char(1) PRIMARY KEY,
    modalidad_desc  text NOT NULL
);
COMMENT ON TABLE dim_modalidad IS
    'Tipo de intervencion publica del programa presupuestario, identificada con '
    'una letra. Ejemplos: E = prestacion de servicios, S = sujeto a reglas de '
    'operacion, K = proyectos de inversion.';

CREATE TABLE dim_programa_presupuestario (
    ramo_id         smallint NOT NULL,
    modalidad_id    char(1)  NOT NULL REFERENCES dim_modalidad (modalidad_id),
    pp_id           smallint NOT NULL,
    pp_desc         text     NOT NULL,
    PRIMARY KEY (ramo_id, modalidad_id, pp_id),
    FOREIGN KEY (ramo_id) REFERENCES dim_ramo (ramo_id)
);
COMMENT ON TABLE dim_programa_presupuestario IS
    'Programa presupuestario. ATENCION: la clave visible al publico (por ejemplo '
    'P001) combina modalidad y numero, y NO es unica. La pareja modalidad P mas '
    'numero 1 corresponde a 19 programas distintos segun el ramo. Toda consulta '
    'por programa debe calificar el ramo o aceptar que agrega programas ajenos.';

CREATE TABLE dim_partida (
    partida_id      integer PRIMARY KEY,
    partida_desc    text NOT NULL
);
COMMENT ON TABLE dim_partida IS
    'Partida especifica del Clasificador por Objeto del Gasto: en que se gasta. '
    'El primer digito indica el capitulo (1000 servicios personales, 2000 '
    'materiales, 3000 servicios generales, 4000 transferencias, 5000 bienes '
    'muebles, 6000 inversion publica, 7000 inversiones financieras, 8000 '
    'participaciones, 9000 deuda).';

CREATE TABLE dim_tipo_gasto (
    tipogasto_id    smallint PRIMARY KEY,
    tipogasto_desc  text NOT NULL
);
COMMENT ON TABLE dim_tipo_gasto IS
    'Naturaleza economica de la asignacion: corriente, de capital, pensiones y '
    'jubilaciones, o participaciones.';

CREATE TABLE dim_fuente_financiamiento (
    ff_id       smallint PRIMARY KEY,
    ff_desc     text NOT NULL
);
COMMENT ON TABLE dim_fuente_financiamiento IS
    'Origen de los recursos con que se financia la asignacion.';

CREATE TABLE dim_entidad_federativa (
    entidad_id      smallint PRIMARY KEY,
    entidad_desc    text NOT NULL
);
COMMENT ON TABLE dim_entidad_federativa IS
    'Destino geografico del gasto. Incluye las 32 entidades mas claves para '
    'gasto no distribuible geograficamente y erogaciones en el extranjero.';


-- ===========================================================================
-- Variantes historicas de las descripciones
--
-- Las dimensiones son conformadas: guardan un solo nombre por clave. Pero los
-- catalogos cambian entre ejercicios (48 ramos en 2024, 50 en 2025; las
-- unidades responsables pasan de 463 a 531 entre 2022 y 2025). Esta tabla
-- conserva el nombre exacto que tuvo cada clave en cada ejercicio, de modo que
-- la simplificacion no destruya el dato original.
-- ===========================================================================

-- Una clave puede tener mas de un nombre incluso dentro del mismo ejercicio:
-- en 2021, 25 partidas aparecen con dos o tres descripciones, en los dos
-- formatos publicados. Por eso la descripcion forma parte de la llave y se
-- registra cuantos renglones usan cada variante.
CREATE TABLE descripcion_historica (
    dimension       text     NOT NULL,
    llave           text     NOT NULL,
    ciclo           smallint NOT NULL,
    descripcion     text     NOT NULL,
    renglones       integer  NOT NULL,
    PRIMARY KEY (dimension, llave, ciclo, descripcion)
);
COMMENT ON TABLE descripcion_historica IS
    'Cada nombre que tuvo cada clave en cada ejercicio, con el numero de '
    'renglones que lo usan. Permite auditar los cambios de nomenclatura que '
    'las dimensiones conformadas ocultan, incluidas las variantes dentro de un '
    'mismo ejercicio.';


-- ===========================================================================
-- Tabla de hechos
--
-- Un renglon por combinacion de clasificaciones y ejercicio, con las etapas del
-- gasto como medidas. Las etapas no son intercambiables: para 2025 la diferencia
-- entre devengado y pagado supera los 185 mil millones de pesos. Una pregunta
-- sobre "cuanto se gasto" es ambigua hasta que se elige la etapa.
-- ===========================================================================

CREATE TABLE hecho_gasto (
    hecho_id        bigserial PRIMARY KEY,
    ciclo           smallint    NOT NULL,
    ramo_id         smallint    NOT NULL,
    ur_id           varchar(3)  NOT NULL,
    finalidad_id    smallint    NOT NULL,
    funcion_id      smallint    NOT NULL,
    subfuncion_id   smallint    NOT NULL,
    ai_id           smallint    NOT NULL,
    modalidad_id    char(1)     NOT NULL,
    pp_id           smallint    NOT NULL,
    partida_id      integer     NOT NULL,
    tipogasto_id    smallint    NOT NULL,
    ff_id           smallint    NOT NULL,
    entidad_id      smallint    NOT NULL,
    cartera_id      varchar(11) NOT NULL,
    aprobado        numeric(18,2) NOT NULL,
    modificado      numeric(18,2) NOT NULL,
    devengado       numeric(18,2) NOT NULL,
    pagado          numeric(18,2) NOT NULL,
    adefas          numeric(18,2) NOT NULL,
    ejercido        numeric(18,2) NOT NULL,

    FOREIGN KEY (ramo_id) REFERENCES dim_ramo (ramo_id),
    FOREIGN KEY (ramo_id, ur_id)
        REFERENCES dim_unidad_responsable (ramo_id, ur_id),
    FOREIGN KEY (finalidad_id) REFERENCES dim_finalidad (finalidad_id),
    FOREIGN KEY (finalidad_id, funcion_id)
        REFERENCES dim_funcion (finalidad_id, funcion_id),
    FOREIGN KEY (finalidad_id, funcion_id, subfuncion_id)
        REFERENCES dim_subfuncion (finalidad_id, funcion_id, subfuncion_id),
    FOREIGN KEY (ramo_id, ai_id)
        REFERENCES dim_actividad_institucional (ramo_id, ai_id),
    FOREIGN KEY (modalidad_id) REFERENCES dim_modalidad (modalidad_id),
    FOREIGN KEY (ramo_id, modalidad_id, pp_id)
        REFERENCES dim_programa_presupuestario (ramo_id, modalidad_id, pp_id),
    FOREIGN KEY (partida_id) REFERENCES dim_partida (partida_id),
    FOREIGN KEY (tipogasto_id) REFERENCES dim_tipo_gasto (tipogasto_id),
    FOREIGN KEY (ff_id) REFERENCES dim_fuente_financiamiento (ff_id),
    FOREIGN KEY (entidad_id) REFERENCES dim_entidad_federativa (entidad_id)
);

COMMENT ON TABLE hecho_gasto IS
    'Ejercicio del presupuesto de egresos de la Federacion, un renglon por '
    'combinacion de clasificaciones. Fuente: Cuenta Publica, Estado Analitico '
    'del Ejercicio del Presupuesto de Egresos.';
COMMENT ON COLUMN hecho_gasto.aprobado IS
    'Asignacion comprometida en el Presupuesto de Egresos aprobado por la '
    'Camara de Diputados. Importe bruto.';
COMMENT ON COLUMN hecho_gasto.modificado IS
    'Presupuesto aprobado mas las adecuaciones presupuestarias del ejercicio.';
COMMENT ON COLUMN hecho_gasto.devengado IS
    'Obligacion de pago reconocida a favor de terceros por bienes u obras '
    'recibidos de conformidad. Es la etapa que suele entenderse por "gastado".';
COMMENT ON COLUMN hecho_gasto.pagado IS
    'Obligaciones efectivamente liquidadas mediante desembolso.';
COMMENT ON COLUMN hecho_gasto.ejercido IS
    'Emision de la cuenta por liquidar certificada o documento equivalente.';
COMMENT ON COLUMN hecho_gasto.adefas IS
    'Adeudos de ejercicios fiscales anteriores cubiertos con el presupuesto '
    'del ejercicio en curso.';
COMMENT ON COLUMN hecho_gasto.cartera_id IS
    'Clave del programa o proyecto de inversion. Alfanumerica y con ceros a la '
    'izquierda significativos: nunca convertir a numero.';

CREATE INDEX ix_hecho_ciclo          ON hecho_gasto (ciclo);
CREATE INDEX ix_hecho_ramo           ON hecho_gasto (ciclo, ramo_id);
CREATE INDEX ix_hecho_ur             ON hecho_gasto (ramo_id, ur_id);
CREATE INDEX ix_hecho_pp             ON hecho_gasto (ramo_id, modalidad_id, pp_id);
CREATE INDEX ix_hecho_partida        ON hecho_gasto (partida_id);
CREATE INDEX ix_hecho_entidad        ON hecho_gasto (ciclo, entidad_id);
CREATE INDEX ix_hecho_funcional      ON hecho_gasto (finalidad_id, funcion_id, subfuncion_id);
