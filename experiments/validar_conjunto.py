"""
Validacion del conjunto de evaluacion y calculo de sus respuestas de referencia.

Lee eval/preguntas.yaml y, para cada pregunta:
  1. valida su estructura contra las reglas de eval/README.md;
  2. analiza el SQL de referencia con un analizador sintactico y le asigna una
     dificultad por regla, a partir de sus componentes;
  3. ejecuta el SQL como consulta_nlq, el mismo rol y las mismas restricciones
     que tendra el sistema, y guarda el resultado como respuesta de referencia.

La dificultad se deriva del SQL y no del criterio del autor, para que la
estratificacion sea reproducible. Se mide sobre la capa semantica: la misma
pregunta resulta mas dificil sobre el esquema crudo, y esa diferencia es
justamente lo que mide la configuracion 1a del experimento.

Uso:    python experiments/validar_conjunto.py            valida y ejecuta
        python experiments/validar_conjunto.py --sin-base  solo valida y clasifica
Salida: eval/respuestas_referencia.json
        experiments/salidas/conjunto_evaluacion.md
"""

import hashlib
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime
from decimal import Decimal
from pathlib import Path

import sqlglot
import yaml
from sqlglot import exp

RAIZ = Path(__file__).resolve().parents[1]
CONJUNTO = RAIZ / "eval" / "preguntas.yaml"
REFERENCIA = RAIZ / "eval" / "respuestas_referencia.json"
INFORME = RAIZ / "experiments" / "salidas" / "conjunto_evaluacion.md"
SOLICITUDES = RAIZ / "data" / "interim" / "solicitudes_candidatas.csv"
ENV = RAIZ / ".env"

RUTAS = {"sql", "documental"}
COMPORTAMIENTOS = {"responder", "ambigua", "abstenerse"}
ESTADOS = {"propuesta", "verificada", "descartada"}
TIPOS_ORIGEN = {"solicitud_pnt", "generada_ia", "nota_periodistica", "reporte_oficial",
                "variante", "otro"}
ESQUEMA_PERMITIDO = "semantica"
MAX_FILAS_AVISO = 1000

# --- Regla de dificultad (ver eval/README.md) ---
# Cada componente del SQL de referencia suma puntos. Los umbrales se fijan
# ANTES de correr los experimentos: ajustarlos despues de ver resultados
# seria acomodar la medicion a lo medido.
PESOS = {
    "condicion": 1,              # cada predicado en WHERE o HAVING
    "agrupacion": 2,             # GROUP BY
    "having": 1,                 # filtro sobre agregados
    "top_n": 1,                  # ORDER BY con LIMIT
    "join": 2,                   # cada JOIN
    "subconsulta": 3,            # cada consulta anidada o CTE
    "ventana": 3,                # cada funcion de ventana
    "conjunto": 3,               # UNION, INTERSECT, EXCEPT
    "division": 2,               # razones y porcentajes
    "condicional": 1,            # cada CASE, tipico de la agregacion condicional
    "comparacion_temporal": 2,   # la pregunta cruza ejercicios
}
UMBRAL_MEDIA = 4
UMBRAL_ALTA = 7

# Metas de estratificacion, propuestas en eval/README.md. Solo informan el avance.
META_TOTAL = (200, 300)
META_COMPORTAMIENTO = {"responder": 0.70, "ambigua": 0.15, "abstenerse": 0.15}
META_DIFICULTAD = {"baja": 0.30, "media": 0.40, "alta": 0.30}


# ===========================================================================
# Estructura
# ===========================================================================

def validar_estructura(p, vistos):
    """Devuelve la lista de errores de una pregunta. Vacia si es valida."""
    e = []
    pid = p.get("id")
    if not isinstance(pid, str) or not re.fullmatch(r"P\d{4}", pid):
        e.append("id debe tener la forma P0001")
    elif pid in vistos:
        e.append("id duplicado")
    if not str(p.get("pregunta") or "").strip():
        e.append("falta el texto de la pregunta")
    if p.get("ruta") not in RUTAS:
        e.append("ruta debe ser una de: " + ", ".join(sorted(RUTAS)))
    comp = p.get("comportamiento")
    if comp not in COMPORTAMIENTOS:
        e.append("comportamiento debe ser uno de: " + ", ".join(sorted(COMPORTAMIENTOS)))
    if not str(p.get("autor") or "").strip():
        e.append("falta el autor")
    estado = p.get("estado")
    if estado not in ESTADOS:
        e.append("estado debe ser uno de: " + ", ".join(sorted(ESTADOS)))
    if estado == "verificada" and not str(p.get("verificado_por") or "").strip():
        e.append("una pregunta verificada necesita verificado_por")

    origen = p.get("origen") or {}
    if origen.get("tipo") not in TIPOS_ORIGEN:
        e.append("origen.tipo debe ser uno de: " + ", ".join(sorted(TIPOS_ORIGEN)))
    if not str(origen.get("referencia") or "").strip():
        e.append("falta origen.referencia: toda pregunta debe ser rastreable a su fuente")

    tiene_sql = bool(str(p.get("sql") or "").strip())
    interp = p.get("interpretaciones")

    if p.get("ruta") == "sql":
        if comp == "responder" and not tiene_sql:
            e.append("una pregunta sql con comportamiento responder necesita sql")
        if comp == "ambigua":
            if not isinstance(interp, list) or len(interp) < 2:
                e.append("una pregunta ambigua necesita al menos dos interpretaciones")
            else:
                for i, it in enumerate(interp, 1):
                    if not str((it or {}).get("supuesto") or "").strip():
                        e.append("interpretacion {}: falta el supuesto".format(i))
                    if not str((it or {}).get("sql") or "").strip():
                        e.append("interpretacion {}: falta el sql".format(i))
    if comp == "abstenerse":
        if not str(p.get("motivo") or "").strip():
            e.append("una pregunta no respondible necesita motivo")
        if tiene_sql:
            e.append("una pregunta no respondible no lleva sql")
    if comp != "ambigua" and interp:
        e.append("solo las preguntas ambiguas llevan interpretaciones")
    return e


# Patrones de datos personales. La PNT no anonimiza de forma consistente: entre
# el 1 y el 2% de las solicitudes de 2024 a 2026 contienen alguno. Una pregunta
# que los arrastre no puede entrar a un conjunto que se publica.
DATOS_PERSONALES = {
    "CURP": re.compile(r"\b[A-Z][AEIOUX][A-Z]{2}\d{6}[HM][A-Z]{5}[0-9A-Z]\d\b"),
    "RFC de persona fisica": re.compile(r"\b[A-Z&Ñ]{4}\d{6}[A-Z0-9]{3}\b"),
    "correo electronico": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b"),
    "telefono": re.compile(r"(?<!\d)(?:\d[ -]?){10}(?!\d)"),
}


def validar_privacidad(p):
    """Rechaza la pregunta si su texto contiene un patron de dato personal."""
    texto = str(p.get("pregunta") or "")
    return ["la pregunta contiene un posible dato personal ({})".format(nombre)
            for nombre, patron in DATOS_PERSONALES.items() if patron.search(texto)]


def cargar_solicitudes():
    """Texto original de cada solicitud, por folio. None si no esta disponible."""
    if not SOLICITUDES.exists():
        return None
    import csv
    with open(SOLICITUDES, encoding="utf-8-sig", newline="") as fh:
        return {r["folio"]: r["solicitud"] for r in csv.DictReader(fh)}


def validar_literal(p, solicitudes):
    """
    Una pregunta tomada de una solicitud debe ser un fragmento literal de ella:
    se puede recortar, pero no reescribir. Devuelve la lista de errores.
    """
    origen = p.get("origen") or {}
    if origen.get("tipo") != "solicitud_pnt" or solicitudes is None:
        return []
    folio = "".join(ch for ch in str(origen.get("referencia") or "") if ch.isdigit())
    if folio not in solicitudes:
        return ["el folio {} no esta entre las solicitudes candidatas".format(folio)]
    if str(p.get("pregunta") or "") not in solicitudes[folio]:
        return ["la pregunta no es un fragmento literal de la solicitud {}".format(folio)]
    return []


# ===========================================================================
# Analisis del SQL
# ===========================================================================

PREDICADOS = (exp.EQ, exp.NEQ, exp.GT, exp.GTE, exp.LT, exp.LTE,
              exp.In, exp.Between, exp.Like, exp.ILike, exp.Is)


def analizar(sql):
    """
    Valida que sea una sola consulta sobre la capa semantica y cuenta sus
    componentes. Devuelve (componentes, errores).
    """
    try:
        sentencias = [s for s in sqlglot.parse(sql, dialect="postgres") if s is not None]
    except sqlglot.errors.ParseError as err:
        return None, ["el SQL no se pudo analizar: " + str(err).splitlines()[0]]
    if len(sentencias) != 1:
        return None, ["el SQL debe ser una sola sentencia; tiene {}".format(len(sentencias))]
    arbol = sentencias[0]
    if not isinstance(arbol, exp.Query):
        return None, ["el SQL debe ser una consulta (SELECT); es " + type(arbol).__name__]

    errores = []
    ctes = {c.alias for c in arbol.find_all(exp.CTE)}
    for t in arbol.find_all(exp.Table):
        if t.name in ctes:
            continue
        if t.db != ESQUEMA_PERMITIDO:
            errores.append("la tabla {} debe calificarse con el esquema {}".format(
                t.sql(dialect="postgres"), ESQUEMA_PERMITIDO))

    c = Counter()
    for n in arbol.find_all(*PREDICADOS):
        if n.find_ancestor(exp.Where, exp.Having):
            c["condicion"] += 1
    c["agrupacion"] = len(list(arbol.find_all(exp.Group)))
    c["having"] = len(list(arbol.find_all(exp.Having)))
    for s in arbol.find_all(exp.Select):
        if s.args.get("order") and s.args.get("limit"):
            c["top_n"] += 1
    c["join"] = len(list(arbol.find_all(exp.Join)))
    conjuntos = len(list(arbol.find_all(exp.Union, exp.Intersect, exp.Except)))
    c["conjunto"] = conjuntos
    c["subconsulta"] = max(0, len(list(arbol.find_all(exp.Select))) - 1 - conjuntos)
    c["ventana"] = len(list(arbol.find_all(exp.Window)))
    c["division"] = len(list(arbol.find_all(exp.Div)))
    c["condicional"] = len(list(arbol.find_all(exp.Case)))
    c["comparacion_temporal"] = 1 if cruza_ejercicios(arbol) else 0
    return dict(c), errores


def cruza_ejercicios(arbol):
    """La consulta abarca mas de un ejercicio fiscal."""
    def es_ejercicio(n):
        return isinstance(n, exp.Column) and n.name == "ejercicio"
    for g in arbol.find_all(exp.Group):
        if any(es_ejercicio(n) for n in g.find_all(exp.Column)):
            return True
    for n in arbol.find_all(exp.In):
        if es_ejercicio(n.this) and len(n.expressions) >= 2:
            return True
    for n in arbol.find_all(exp.Between):
        if es_ejercicio(n.this):
            return True
    valores = set()
    for n in arbol.find_all(exp.EQ):
        lados = [n.this, n.expression]
        if any(es_ejercicio(x) for x in lados):
            valores.update(x.sql() for x in lados if isinstance(x, exp.Literal))
    return len(valores) >= 2


def dificultad(componentes):
    puntos = sum(PESOS[k] * v for k, v in componentes.items())
    if puntos >= UMBRAL_ALTA:
        return "alta", puntos
    if puntos >= UMBRAL_MEDIA:
        return "media", puntos
    return "baja", puntos


# ===========================================================================
# Ejecucion como consulta_nlq
# ===========================================================================

def cargar_env():
    if not ENV.exists():
        sys.exit("Falta el archivo .env. Copia .env.example a .env y completa los datos.")
    for linea in ENV.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if linea and not linea.startswith("#") and "=" in linea:
            k, v = linea.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
    faltan = [v for v in ("PGDATABASE", "CONSULTA_PGUSER", "CONSULTA_PGPASSWORD")
              if not os.environ.get(v)]
    if faltan:
        sys.exit("Faltan valores en .env: " + ", ".join(faltan))


def conectar():
    import psycopg
    return psycopg.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=os.environ.get("PGPORT", "5432"),
        dbname=os.environ["PGDATABASE"],
        user=os.environ["CONSULTA_PGUSER"],
        password=os.environ["CONSULTA_PGPASSWORD"],
        autocommit=True,
        connect_timeout=10,
    )


def a_json(v):
    if isinstance(v, Decimal):
        return str(v)
    if v is None or isinstance(v, (int, float, str, bool)):
        return v
    return str(v)


def ejecutar(conn, sql):
    import psycopg
    inicio = time.perf_counter()
    try:
        cur = conn.execute(sql)
        filas = cur.fetchall()
        columnas = [d.name for d in cur.description]
    except psycopg.Error as err:
        return {"error": (getattr(err, "sqlstate", None) or "") + " " + str(err).strip().splitlines()[0]}
    ms = round((time.perf_counter() - inicio) * 1000)
    return {
        "columnas": columnas,
        "filas": [[a_json(v) for v in f] for f in filas],
        "n_filas": len(filas),
        "ms": ms,
    }


def huella(sql):
    """Huella del SQL: permite saber si la respuesta guardada sigue correspondiendo."""
    return hashlib.sha256(sql.strip().encode("utf-8")).hexdigest()[:16]


# ===========================================================================
# Principal
# ===========================================================================

def main():
    sin_base = "--sin-base" in sys.argv
    if not CONJUNTO.exists():
        sys.exit("No existe " + str(CONJUNTO.relative_to(RAIZ)))
    preguntas = yaml.safe_load(CONJUNTO.read_text(encoding="utf-8")) or []
    if not isinstance(preguntas, list):
        sys.exit("preguntas.yaml debe contener una lista de preguntas")

    conn = None
    hay_sql = any(p.get("sql") or p.get("interpretaciones") for p in preguntas if isinstance(p, dict))
    if hay_sql and not sin_base:
        cargar_env()
        conn = conectar()

    solicitudes = cargar_solicitudes()
    filas_informe, referencia, vistos = [], {}, set()
    for p in preguntas:
        if not isinstance(p, dict):
            filas_informe.append({"id": "?", "errores": ["entrada que no es una pregunta"]})
            continue
        pid = p.get("id", "?")
        errores = validar_estructura(p, vistos)
        errores.extend(validar_literal(p, solicitudes))
        errores.extend(validar_privacidad(p))
        vistos.add(pid)
        r = {"id": pid, "ruta": p.get("ruta"), "comportamiento": p.get("comportamiento"),
             "origen": (p.get("origen") or {}).get("tipo"), "estado": p.get("estado"),
             "errores": errores}

        # Una pregunta ambigua se clasifica por su interpretacion mas dificil.
        consultas = []
        if p.get("sql"):
            consultas.append((None, p["sql"]))
        for it in p.get("interpretaciones") or []:
            if isinstance(it, dict) and it.get("sql"):
                consultas.append((it.get("supuesto"), it["sql"]))

        mejor, resultados = None, []
        for supuesto, sql in consultas:
            comp, errs = analizar(sql)
            errores.extend(errs)
            if comp is None:
                continue
            nivel, puntos = dificultad(comp)
            if mejor is None or puntos > mejor[1]:
                mejor = (nivel, puntos, comp)
            if conn and not errs:
                res = ejecutar(conn, sql)
                if "error" in res:
                    errores.append("el SQL fallo al ejecutarse: " + res["error"])
                else:
                    if res["n_filas"] > MAX_FILAS_AVISO:
                        errores.append("el resultado tiene {:,} filas; revisa si la pregunta es demasiado amplia".format(res["n_filas"]))
                    res["huella_sql"] = huella(sql)
                    if supuesto:
                        res["supuesto"] = supuesto
                    resultados.append(res)

        if mejor:
            r["dificultad"], r["puntos"], r["componentes"] = mejor
        if resultados:
            r["n_filas"] = sum(x["n_filas"] for x in resultados)
            r["ms"] = max(x["ms"] for x in resultados)
            referencia[pid] = resultados if p.get("comportamiento") == "ambigua" else resultados[0]
        filas_informe.append(r)

    if conn:
        conn.close()
        REFERENCIA.write_text(json.dumps(
            {"generado": datetime.now().isoformat(timespec="seconds"),
             "rol": os.environ.get("CONSULTA_PGUSER"),
             "preguntas": referencia},
            ensure_ascii=False, indent=1), encoding="utf-8")

    escribir_informe(filas_informe, sin_base, solicitudes is not None)
    con_error = [r for r in filas_informe if r["errores"]]
    print("{} preguntas, {} con errores".format(len(filas_informe), len(con_error)))
    for r in con_error:
        for e in r["errores"]:
            print("  {}: {}".format(r["id"], e))
    print("informe escrito en " + str(INFORME.relative_to(RAIZ)))
    if conn:
        print("respuestas de referencia en " + str(REFERENCIA.relative_to(RAIZ)))
    sys.exit(1 if con_error else 0)


def escribir_informe(filas, sin_base, literal_comprobado):
    L = []
    L.append("# Estado del conjunto de evaluacion")
    L.append("")
    L.append("Generado el " + datetime.now().strftime("%Y-%m-%d %H:%M")
             + " por `experiments/validar_conjunto.py`"
             + (" (sin ejecutar contra la base)." if sin_base else "."))
    L.append("")
    L.append("Comprobacion de texto literal: " + (
        "realizada contra `data/interim/solicitudes_candidatas.csv`."
        if literal_comprobado else
        "**omitida**, porque no esta disponible `data/interim/solicitudes_candidatas.csv`. "
        "Correr antes `experiments/leer_solicitudes_pnt.py`."))
    validas = [f for f in filas if not f["errores"]]
    n = len(filas)
    L.append("")
    L.append("**{} preguntas**, {} validas. Meta: entre {} y {}.".format(
        n, len(validas), META_TOTAL[0], META_TOTAL[1]))
    ce = Counter(f.get("estado") for f in validas)
    L.append("")
    L.append("**Por estado:** {} verificadas, {} propuestas, {} descartadas. "
             "Solo las verificadas entran a los experimentos: una propuesta es "
             "una sugerencia pendiente de revision humana, no una respuesta de "
             "referencia.".format(ce.get("verificada", 0), ce.get("propuesta", 0),
                                  ce.get("descartada", 0)))

    L.append("")
    L.append("## Por comportamiento esperado")
    L.append("")
    L.append("| Comportamiento | Preguntas | Proporcion | Meta |")
    L.append("|---|---:|---:|---:|")
    cc = Counter(f.get("comportamiento") for f in validas)
    for k, meta in META_COMPORTAMIENTO.items():
        L.append("| {} | {} | {:.0%} | {:.0%} |".format(
            k, cc.get(k, 0), cc.get(k, 0) / len(validas) if validas else 0, meta))

    L.append("")
    L.append("## Por dificultad (preguntas a responder)")
    L.append("")
    L.append("| Dificultad | Preguntas | Proporcion | Meta |")
    L.append("|---|---:|---:|---:|")
    resp = [f for f in validas if f.get("comportamiento") == "responder" and f.get("dificultad")]
    cd = Counter(f["dificultad"] for f in resp)
    for k, meta in META_DIFICULTAD.items():
        L.append("| {} | {} | {:.0%} | {:.0%} |".format(
            k, cd.get(k, 0), cd.get(k, 0) / len(resp) if resp else 0, meta))

    L.append("")
    L.append("## Por origen")
    L.append("")
    L.append("| Origen | Preguntas |")
    L.append("|---|---:|")
    for k, v in Counter(f.get("origen") for f in validas).most_common():
        L.append("| {} | {} |".format(k, v))

    L.append("")
    L.append("## Detalle")
    L.append("")
    L.append("| Id | Estado | Ruta | Comportamiento | Dificultad | Puntos | Componentes | Filas | ms | Validacion |")
    L.append("|---|---|---|---|---|---:|---|---:|---:|---|")
    for f in filas:
        comp = ", ".join("{} {}".format(k, v) for k, v in sorted((f.get("componentes") or {}).items()) if v)
        L.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            f["id"], f.get("estado") or "", f.get("ruta") or "", f.get("comportamiento") or "",
            f.get("dificultad") or "", f.get("puntos", ""), comp,
            f.get("n_filas", ""), f.get("ms", ""),
            "valida" if not f["errores"] else "**" + "; ".join(f["errores"]) + "**"))

    L.append("")
    L.append("## Regla de dificultad")
    L.append("")
    L.append("| Componente | Puntos |")
    L.append("|---|---:|")
    for k, v in PESOS.items():
        L.append("| {} | {} |".format(k, v))
    L.append("")
    L.append("Baja: menos de {} puntos. Media: de {} a {}. Alta: {} o mas.".format(
        UMBRAL_MEDIA, UMBRAL_MEDIA, UMBRAL_ALTA - 1, UMBRAL_ALTA))

    INFORME.parent.mkdir(parents=True, exist_ok=True)
    INFORME.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
