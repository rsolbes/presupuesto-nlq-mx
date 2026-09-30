"""
Hoja de verificacion del conjunto de evaluacion.

Para cada pregunta en estado `propuesta` con SQL de referencia, reune lo que el
autor necesita para verificarla:

  1. la pregunta, sus notas y su SQL;
  2. el resultado actual en la base, ejecutado con el rol de solo lectura, y un
     aviso si difiere del guardado en eval/respuestas_referencia.json;
  3. el mismo filtro sumado en cada etapa del gasto, para ver si la eleccion de
     etapa cambia la respuesta;
  4. la receta para recalcular la cifra en el archivo xlsx publicado: que
     archivo abrir, que columnas filtrar (con el encabezado de ese ejercicio)
     y que columna sumar.

El recalculo en el xlsx es independiente de la normalizacion, de la carga, de
la capa semantica y del SQL: si coincide, la cifra es fiel al archivo oficial.
No sustituye a una fuente oficial distinta cuando la haya, y la hoja lo dice.

Uso:
    python experiments/hoja_verificacion.py                  todas las propuestas con SQL
    python experiments/hoja_verificacion.py --origen generada_ia
    python experiments/hoja_verificacion.py --ids P0042-P0061

Salida: experiments/salidas/hoja_verificacion.md
"""
import json
import sys
from decimal import Decimal
from pathlib import Path

import sqlglot
import yaml
from sqlglot import exp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validar_conjunto as vc  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

RAIZ = vc.RAIZ
CONJUNTO = RAIZ / "eval" / "preguntas.yaml"
REFERENCIAS = RAIZ / "eval" / "respuestas_referencia.json"
CRUDOS = RAIZ / "data" / "raw"
SALIDA = RAIZ / "experiments" / "salidas" / "hoja_verificacion.md"

ETAPAS = ["aprobado", "modificado", "devengado", "ejercido", "pagado"]

# Columna de semantica.gasto -> columna canonica del archivo publicado.
# programa_clave y capitulo_clave no existen en el archivo: se traducen aparte.
A_CANONICO = {
    "ejercicio": "ciclo",
    "ramo_clave": "ramo_id",
    "ramo": "ramo_desc",
    "unidad_responsable_clave": "ur_id",
    "unidad_responsable": "ur_desc",
    "finalidad": "finalidad_desc",
    "funcion": "funcion_desc",
    "subfuncion": "subfuncion_desc",
    "actividad_institucional": "ai_desc",
    "programa": "pp_desc",
    "modalidad": "modalidad_desc",
    "partida_clave": "partida_id",
    "partida": "partida_desc",
    "tipo_de_gasto": "tipogasto_desc",
    "fuente_de_financiamiento": "ff_desc",
    "entidad_federativa": "entidad_desc",
    "proyecto_de_inversion_clave": "cartera_id",
    "aprobado": "aprobado",
    "modificado": "modificado",
    "devengado": "devengado",
    "pagado": "pagado",
    "ejercido": "ejercido",
    "adefas": "adefas",
}

# Nombres que la base toma del ejercicio mas reciente: en archivos anteriores
# el mismo valor puede aparecer con otro nombre.
DESCRIPCIONES = {"ramo", "unidad_responsable", "programa", "funcion", "subfuncion",
                 "finalidad", "entidad_federativa", "partida", "modalidad",
                 "tipo_de_gasto", "fuente_de_financiamiento", "actividad_institucional"}


# ---------------------------------------------------------------------------
# Encabezados publicados
# ---------------------------------------------------------------------------

def letra(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def encabezados():
    """{ejercicio: {canonico: (letra, encabezado)}} leidos de cada xlsx."""
    import openpyxl
    from esquema import CANONICO  # noqa: E402

    out = {}
    for ruta in sorted(CRUDOS.glob("cuenta_publica_*_gf_ecd_epe.xlsx")):
        anio = int(ruta.name.split("_")[2])
        wb = openpyxl.load_workbook(ruta, read_only=True)
        fila = next(wb.worksheets[0].iter_rows(max_row=1, values_only=True))
        wb.close()
        nombradas = [(i, v) for i, v in enumerate(fila) if v]
        assert len(nombradas) == len(CANONICO), ruta.name
        out[anio] = {c: (letra(i), v, ruta.name) for c, (i, v) in zip(CANONICO, nombradas)}
    return out


# ---------------------------------------------------------------------------
# Lectura del SQL
# ---------------------------------------------------------------------------

def literal(n):
    if isinstance(n, exp.Literal):
        return n.this if n.is_string else Decimal(n.this)
    if isinstance(n, exp.Neg):
        return -literal(n.this)
    return None


def condiciones(where):
    """Divide el WHERE en condiciones unidas por AND."""
    if where is None:
        return []
    return list(where.this.flatten()) if isinstance(where.this, exp.And) else [where.this]


def filtros(arbol):
    """
    Traduce las condiciones del WHERE a filtros legibles:
    [(columna_semantica, operador, [valores])]. Las que no sabe leer las
    devuelve como texto para que el autor las aplique a mano.
    """
    leidos, sin_leer = [], []
    for c in condiciones(arbol.args.get("where")):
        neg = isinstance(c, exp.Not)
        base = c.this if neg else c
        if isinstance(base, exp.EQ) and isinstance(base.this, exp.Column) and literal(base.expression) is not None:
            leidos.append((base.this.name, "no es" if neg else "es", [literal(base.expression)]))
        elif isinstance(base, exp.In) and isinstance(base.this, exp.Column):
            vals = [literal(v) for v in base.expressions]
            if None in vals:
                sin_leer.append(c.sql(dialect="postgres"))
            else:
                leidos.append((base.this.name, "no es ninguno de" if neg else "es uno de", vals))
        else:
            sin_leer.append(c.sql(dialect="postgres"))
    return leidos, sin_leer


def medidas(arbol):
    """Etapas que el SELECT suma, y si hay calculos ademas de la suma simple."""
    usadas, calculo = [], False
    for proy in arbol.expressions:
        nodo = proy.this if isinstance(proy, exp.Alias) else proy
        cols = [c.name for c in nodo.find_all(exp.Column)]
        etapas = [c for c in cols if c in ETAPAS + ["adefas"]]
        for e in etapas:
            if e not in usadas:
                usadas.append(e)
        if etapas and not (isinstance(nodo, exp.Sum) and isinstance(nodo.this, exp.Column)):
            calculo = True
    return usadas, calculo


def agrupacion(arbol):
    g = arbol.args.get("group")
    return [e.name for e in g.expressions] if g else []


# ---------------------------------------------------------------------------
# Receta de recalculo en el xlsx
# ---------------------------------------------------------------------------

def fmt_valor(v):
    return str(v) if not isinstance(v, str) else '"{}"'.format(v)


def receta(arbol, cab):
    leidos, sin_leer = filtros(arbol)
    anios = sorted({int(v) for col, op, vals in leidos if col == "ejercicio" and "no" not in op for v in vals})
    if not anios:
        anios = sorted(cab)
    usadas, calculo = medidas(arbol)
    grupos = [g for g in agrupacion(arbol) if g != "ejercicio"]  # un archivo por ejercicio
    L = []
    for anio in anios:
        h = cab[anio]
        L.append("**{}** — archivo `data/raw/{}`".format(anio, h["ciclo"][2]))
        L.append("")
        L.append("| Columna | Encabezado | Filtro |")
        L.append("|---|---|---|")
        avisos = []
        for col, op, vals in leidos:
            if col == "ejercicio":
                continue  # un archivo por ejercicio
            if col == "programa_clave":
                mods = sorted({str(v)[0] for v in vals})
                pps = sorted({int(str(v)[1:]) for v in vals})
                a, b = h["modalidad_id"], h["pp_id"]
                L.append("| {} | {} | {} {} |".format(a[0], a[1], op, ", ".join(mods)))
                L.append("| {} | {} | {} {} |".format(b[0], b[1], op, ", ".join(str(p) for p in pps)))
                if len(vals) > 1:
                    avisos.append("La clave del programa se separa en modalidad (letra) y número; "
                                  "verifica que las combinaciones filtradas sean exactamente " +
                                  ", ".join(str(v) for v in vals) + ".")
                continue
            if col == "capitulo_clave":
                a = h["partida_id"]
                rangos = ", ".join("{} y {}".format(int(v) * 10, int(v) * 10 + 9999) for v in vals)
                L.append("| {} | {} | {} entre {} |".format(a[0], a[1], op, rangos))
                continue
            canon = A_CANONICO.get(col)
            if canon is None:
                avisos.append("Filtro sin traducción automática: `{}`.".format(col))
                continue
            a = h[canon]
            L.append("| {} | {} | {} {} |".format(a[0], a[1], op, ", ".join(fmt_valor(v) for v in vals)))
            if col in DESCRIPCIONES:
                avisos.append("`{}` usa el nombre del ejercicio más reciente; si el valor no aparece "
                              "en este archivo, busca una variante del nombre.".format(a[1]))
        suma = ", ".join("{} ({})".format(h[A_CANONICO[m]][0], h[A_CANONICO[m]][1]) for m in usadas)
        L.append("")
        L.append("Sumar: " + (suma or "sin etapa en el SELECT"))
        if grupos:
            cols = []
            for g in grupos:
                if g == "programa_clave":
                    cols.append("{} y {}".format(h["modalidad_id"][1], h["pp_id"][1]))
                elif g == "capitulo_clave" or g == "capitulo":
                    cols.append("primer dígito de " + h["partida_id"][1])
                elif g in A_CANONICO:
                    cols.append(h[A_CANONICO[g]][1])
                else:
                    cols.append(g)
            L.append("Agrupar por: " + ", ".join(cols) + " (tabla dinámica, con estas columnas en filas).")
        for a in avisos:
            L.append("")
            L.append("Aviso: " + a)
        L.append("")
    if sin_leer:
        L.append("Condiciones que debes aplicar a mano: " + "; ".join("`{}`".format(s) for s in sin_leer))
        L.append("")
    if calculo:
        L.append("El SELECT calcula sobre las sumas (resta, porcentaje o condición): "
                 "obtén primero las sumas con los filtros y aplica el cálculo del SQL.")
        L.append("")
    return L


# ---------------------------------------------------------------------------
# Contexto por etapa
# ---------------------------------------------------------------------------

def por_etapa(conn, arbol):
    """Mismo FROM y WHERE, sumado en cada etapa. Sin GROUP BY ni LIMIT."""
    where = arbol.args.get("where")
    sql = "SELECT " + ", ".join("sum({0}) AS {0}".format(e) for e in ETAPAS) + " FROM semantica.gasto"
    if where is not None:
        sql += " " + where.sql(dialect="postgres")
    r = vc.ejecutar(conn, sql)
    if "error" in r:
        return ["No se pudo calcular: " + r["error"], ""]
    fila = r["filas"][0]
    L = ["| Etapa | Millones de pesos |", "|---|---:|"]
    for e, v in zip(ETAPAS, fila):
        L.append("| {} | {} |".format(e, mdp(v)))
    L.append("")
    return L


def mdp(v):
    if v is None:
        return "—"
    return "{:,.1f}".format(Decimal(str(v)) / Decimal(1000000))


def tabla_resultado(r):
    if "error" in r:
        return ["Error al ejecutar: `{}`".format(r["error"]), ""]
    L = ["| " + " | ".join(r["columnas"]) + " |", "|" + "---|" * len(r["columnas"])]
    for f in r["filas"][:30]:
        celdas = []
        for c, v in zip(r["columnas"], f):
            if _es_importe(c, v):
                celdas.append("{} ({} MDP)".format(v, mdp(v)))
            else:
                celdas.append(str(v))
        L.append("| " + " | ".join(celdas) + " |")
    if r["n_filas"] > 30:
        L.append("")
        L.append("… {} filas en total; se muestran 30.".format(r["n_filas"]))
    L.append("")
    return L


def _es_importe(col, v):
    try:
        return (isinstance(v, str) and abs(Decimal(v)) >= 1000000
                and not any(s in col for s in ("porcentaje", "cambio", "_mdp")))
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Principal
# ---------------------------------------------------------------------------

def seleccion(preguntas):
    args = sys.argv[1:]
    elegidas = [p for p in preguntas if p.get("estado") == "propuesta" and p.get("sql")]
    if "--origen" in args:
        o = args[args.index("--origen") + 1]
        elegidas = [p for p in elegidas if p["origen"]["tipo"] == o]
    if "--ids" in args:
        a, _, b = args[args.index("--ids") + 1].partition("-")
        b = b or a
        elegidas = [p for p in elegidas if int(a[1:]) <= int(p["id"][1:]) <= int(b[1:])]
    return elegidas


def main():
    preguntas = yaml.safe_load(CONJUNTO.read_text(encoding="utf-8")) or []
    elegidas = seleccion(preguntas)
    if not elegidas:
        sys.exit("Ninguna pregunta cumple el filtro.")
    guardadas = json.loads(REFERENCIAS.read_text(encoding="utf-8"))["preguntas"] if REFERENCIAS.exists() else {}
    cab = encabezados()
    vc.cargar_env()
    conn = vc.conectar()

    L = ["# Hoja de verificación", "",
         "Generada por `experiments/hoja_verificacion.py` con el rol `consulta_nlq`. "
         "{} preguntas en estado `propuesta`.".format(len(elegidas)), "",
         "## Cómo verificar cada pregunta", "",
         "1. **La pregunta.** Se entiende, suena natural y no da pistas del esquema.",
         "2. **La lectura.** La etapa, el año y el alcance que asume el SQL son los que pide la pregunta "
         "(criterios en `eval/README.md`). La tabla por etapa muestra cuánto cambia la cifra si la etapa fuera otra.",
         "3. **El SQL.** Hace lo que la pregunta pide, y la trampa de las notas está resuelta.",
         "4. **La cifra.** Recalcúlala en el xlsx publicado con la receta: filtra las columnas indicadas "
         "(Datos → Filtro) y selecciona la columna a sumar; Excel muestra la suma de las celdas visibles en la "
         "barra de estado. Para agrupaciones, usa una tabla dinámica.",
         "5. **Si coincide**, registra en `eval/preguntas.yaml`:", "",
         "```yaml",
         "  verificacion:",
         '    documento: "cuenta_publica_AAAA_gf_ecd_epe.xlsx, recálculo en el archivo publicado"',
         '    ubicacion: "filtros aplicados, tal como en la receta"',
         '    valor: "cifra obtenida"',
         "  estado: verificada",
         "  verificado_por: RSD", "```", "",
         "El recálculo prueba que la cifra es fiel al archivo oficial y que la cadena del proyecto "
         "(normalización, carga, capa semántica y SQL) no la alteró. Si además encuentras la cifra en un "
         "documento oficial distinto, como un tomo de la Cuenta Pública, regístralo en su lugar: es una "
         "verificación más fuerte. Si no coincide, o la lectura no te convence, anótalo en `notas` "
         "y déjala como `propuesta`.", ""]

    resumen = []
    for p in elegidas:
        arbol = sqlglot.parse_one(p["sql"], read="postgres")
        r = vc.ejecutar(conn, p["sql"])
        g = guardadas.get(p["id"])
        if isinstance(g, dict) and "error" not in r:
            cambio = g.get("filas") != r["filas"] or g.get("huella_sql") != vc.huella(p["sql"])
        else:
            cambio = None
        resumen.append((p["id"], p["pregunta"], cambio))

        L.append("---")
        L.append("")
        L.append("## " + p["id"])
        L.append("")
        L.append("> " + p["pregunta"].strip())
        L.append("")
        L.append("Origen: {} · {}".format(p["origen"]["tipo"], p["origen"].get("referencia", "")))
        L.append("")
        if p.get("notas"):
            L.append("Notas: " + p["notas"].strip())
            L.append("")
        L.append("```sql")
        L.append(p["sql"].strip())
        L.append("```")
        L.append("")
        L.append("### Resultado en la base")
        L.append("")
        if cambio:
            L.append("**Atención: difiere de la respuesta guardada en `respuestas_referencia.json`.** "
                     "Vuelve a ejecutar `validar_conjunto.py` antes de verificar.")
            L.append("")
        L.extend(tabla_resultado(r))
        L.append("### Mismo filtro en cada etapa")
        L.append("")
        L.extend(por_etapa(conn, arbol))
        L.append("### Receta de recálculo en el xlsx")
        L.append("")
        L.extend(receta(arbol, cab))
        L.append("### Verificación")
        L.append("")
        L.append("- [ ] La pregunta se entiende y suena natural")
        L.append("- [ ] La lectura (etapa, año, alcance) es la correcta")
        L.append("- [ ] El SQL responde lo que se pregunta")
        L.append("- [ ] La cifra coincide con el recálculo")
        L.append("")

    conn.close()
    indice = ["## Índice", "", "| Pregunta | Texto | Estado del resultado |", "|---|---|---|"]
    for i, t, c in resumen:
        estado = "difiere de lo guardado" if c else ("sin respuesta guardada" if c is None else "igual a lo guardado")
        indice.append("| [{0}](#{1}) | {2} | {3} |".format(i, i.lower(), t.strip()[:80].replace("|", "/"), estado))
    indice.append("")
    L = L[:4] + indice + L[4:]
    SALIDA.write_text("\n".join(L), encoding="utf-8", newline="\n")
    print("hoja escrita en " + str(SALIDA.relative_to(RAIZ)) + " ({} preguntas)".format(len(elegidas)))


if __name__ == "__main__":
    main()
