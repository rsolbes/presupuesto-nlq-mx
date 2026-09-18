"""
Definicion canonica del esquema presupuestario.

Fuente unica de verdad para el normalizador, el generador de DDL y la capa
semantica. Todo lo que hay aqui se derivo del perfilado de las fuentes crudas
(ver experiments/salidas/perfil_fuentes.md y cruce_xlsx_csv.md), no de supuestos.
"""

# --- Columnas canonicas, en el orden posicional que comparten los seis ejercicios ---
CANONICO = [
    "ciclo",
    "ramo_id", "ramo_desc",
    "ur_id", "ur_desc",
    "finalidad_id", "finalidad_desc",
    "funcion_id", "funcion_desc",
    "subfuncion_id", "subfuncion_desc",
    "ai_id", "ai_desc",
    "modalidad_id", "modalidad_desc",
    "pp_id", "pp_desc",
    "partida_id", "partida_desc",
    "tipogasto_id", "tipogasto_desc",
    "ff_id", "ff_desc",
    "entidad_id", "entidad_desc",
    "cartera_id",
    "aprobado", "modificado", "devengado", "pagado", "adefas", "ejercido",
]

MEDIDAS = ["aprobado", "modificado", "devengado", "pagado", "adefas", "ejercido"]

CLAVES = [c for c in CANONICO if c.endswith("_id")]

# --- Encabezados publicados por convencion ---
# La SHCP uso tres nomenclaturas distintas entre 2020 y 2025, y ademas nombra
# las columnas de forma diferente segun el formato (csv o xlsx) del mismo
# ejercicio. El mapeo es posicional; estas listas lo validan.
VARIANTES = {
    "ciclo": {"CICLO", "Ciclo"},
    "ramo_id": {"ID_RAMO", "RAMO", "R"},
    "ramo_desc": {"DESC_RAMO", "RAMO_DESC"},
    "ur_id": {"ID_UR", "UR"},
    "ur_desc": {"DESC_UR", "UR_DESC"},
    "finalidad_id": {"GPO_FUNCIONAL", "FI"},
    "finalidad_desc": {"DESC_GPO_FUNCIONAL", "FIN_DESC"},
    "funcion_id": {"ID_FUNCION", "FUNCION", "FU"},
    "funcion_desc": {"DESC_FUNCION", "FUN_DESC"},
    "subfuncion_id": {"ID_SUBFUNCION", "SUBFUNCION", "SF"},
    "subfuncion_desc": {"DESC_SUBFUNCION", "SF_DESC"},
    "ai_id": {"ID_AI", "AI"},
    "ai_desc": {"DESC_AI", "AI_DESC"},
    "modalidad_id": {"ID_MODALIDAD", "MODALIDAD", "MOD"},
    "modalidad_desc": {"DESC_MODALIDAD", "MOD_DESC"},
    "pp_id": {"ID_PP", "PP"},
    "pp_desc": {"DESC_PP", "PP_DESC"},
    "partida_id": {"ID_OBJETO_DEL_GASTO", "OBJETO_DEL_GASTO", "PTDA"},
    "partida_desc": {"DESC_OBJETO_DEL_GASTO", "PTDA_DESC"},
    "tipogasto_id": {"ID_TIPOGASTO", "TIPOGASTO", "TG"},
    "tipogasto_desc": {"DESC_TIPOGASTO", "TG_DESC"},
    "ff_id": {"ID_FF", "FF"},
    "ff_desc": {"DESC_FF", "FF_DESC"},
    "entidad_id": {"ID_ENTIDAD_FEDERATIVA", "EF"},
    "entidad_desc": {"ENTIDAD_FEDERATIVA", "DESC_ENTIDAD_FEDERATIVA", "EF_DESC"},
    "cartera_id": {"ID_CLAVE_CARTERA", "CLAVE_CARTERA", "PPI"},
    "aprobado": {"MONTO_APROBADO", "Original_Bruto"},
    "modificado": {"MONTO_MODIFICADO", "Modificado_Bruto"},
    "devengado": {"MONTO_DEVENGADO", "Devengado"},
    "pagado": {"MONTO_PAGADO", "Pagado"},
    "adefas": {"ADEFAS", "Adefas"},
    "ejercido": {"EJERCICIO", "MONTO_EJERCIDO", "Ejercido_Bruto"},
}

# --- Dimensiones conformadas ---
# (tabla, columnas de llave natural, columna de descripcion)
# Las llaves compuestas no son una preferencia de diseno: son necesarias.
# pp_id por si solo apunta a hasta 19 programas distintos segun el ramo.
# Validado en los seis ejercicios.
DIMENSIONES = [
    ("dim_ramo", ["ramo_id"], "ramo_desc"),
    ("dim_unidad_responsable", ["ramo_id", "ur_id"], "ur_desc"),
    ("dim_finalidad", ["finalidad_id"], "finalidad_desc"),
    ("dim_funcion", ["finalidad_id", "funcion_id"], "funcion_desc"),
    ("dim_subfuncion", ["finalidad_id", "funcion_id", "subfuncion_id"], "subfuncion_desc"),
    ("dim_actividad_institucional", ["ramo_id", "ai_id"], "ai_desc"),
    ("dim_modalidad", ["modalidad_id"], "modalidad_desc"),
    ("dim_programa_presupuestario", ["ramo_id", "modalidad_id", "pp_id"], "pp_desc"),
    ("dim_partida", ["partida_id"], "partida_desc"),
    ("dim_tipo_gasto", ["tipogasto_id"], "tipogasto_desc"),
    ("dim_fuente_financiamiento", ["ff_id"], "ff_desc"),
    ("dim_entidad_federativa", ["entidad_id"], "entidad_desc"),
]

# --- Correcciones explicitas sobre descripciones publicadas ---
# Cada entrada corrige un error tipografico detectado en la fuente. Se aplican
# de forma declarada y quedan registradas en la bitacora de normalizacion:
# corregir en silencio seria indistinguible de alterar el dato.
CORRECCIONES = {
    "finalidad_desc": {"Desarrollo SoSocial": "Desarrollo Social"},
}

# Los ejercicios 2020 y 2021 dejan celdas de importe en blanco donde los demas
# escriben cero. En 2020 el vacio esta en los dos formatos publicados, asi que
# es caracteristica del dato de origen. Se interpreta como cero, porque las
# sumas por etapa coinciden con esa lectura y porque permite declarar las
# medidas como NOT NULL.
VACIO_ES_CERO = True


def mapear_encabezado(encabezado):
    """
    Recibe la lista de encabezados publicados y devuelve {canonico: posicion}.

    El mapeo es posicional y se valida contra VARIANTES. Si aparece un
    encabezado desconocido se levanta una excepcion en lugar de adivinar: un
    cambio de nomenclatura no anunciado debe detener la carga, no colarse.
    """
    nombradas = [c for c in encabezado if c]
    if len(nombradas) != len(CANONICO):
        raise ValueError(
            "Se esperaban {} columnas con nombre y llegaron {}".format(
                len(CANONICO), len(nombradas)))
    desconocidos = [
        (canon, real)
        for canon, real in zip(CANONICO, nombradas)
        if real not in VARIANTES[canon]
    ]
    if desconocidos:
        raise ValueError("Encabezados no reconocidos: " + repr(desconocidos))
    return {canon: i for i, canon in enumerate(CANONICO)}
