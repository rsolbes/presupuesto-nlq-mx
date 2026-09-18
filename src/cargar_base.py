"""
Carga de los CSV canonicos a PostgreSQL.

Construye las dimensiones conformadas a partir de los seis ejercicios
normalizados, llena la tabla de hechos con COPY y valida que los totales
cargados coincidan con los del archivo de origen.

La carga completa ocurre en una sola transaccion: si cualquier paso falla, la
base queda exactamente como estaba. Es idempotente: vuelve a correrse sin
duplicar datos, porque vacia las tablas antes de cargar.

La conexion se toma de las variables estandar de libpq (PGHOST, PGPORT,
PGDATABASE, PGUSER, PGPASSWORD) definidas en .env, que no se versiona.

Uso:    python src/cargar_base.py
Salida: base presupuesto_nlq cargada  y  docs/bitacora_carga.md
"""

import csv
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import psycopg

from esquema import CLAVES, DIMENSIONES, MEDIDAS

RAIZ = Path(__file__).resolve().parents[1]
INTERMEDIO = RAIZ / "data" / "interim"
ENV = RAIZ / ".env"
BITACORA = RAIZ / "docs" / "bitacora_carga.md"

ESQUEMA = "presupuesto"
COLUMNAS_HECHO = ["ciclo"] + CLAVES + MEDIDAS


def cargar_env():
    """Carga .env en el entorno. Nunca imprime ni registra los valores."""
    if not ENV.exists():
        sys.exit("Falta el archivo .env. Copia .env.example a .env y completa los datos.")
    for linea in ENV.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        os.environ.setdefault(clave.strip(), valor.strip())
    faltan = [v for v in ("PGDATABASE", "PGUSER", "PGPASSWORD") if not os.environ.get(v)]
    if faltan:
        sys.exit("Faltan valores en .env: " + ", ".join(faltan))


def archivos():
    rutas = sorted(INTERMEDIO.glob("hechos_*.csv"))
    if not rutas:
        sys.exit("No hay CSV normalizados en data/interim. Corre antes src/normalizar_fuentes.py")
    return rutas


def leer(ruta):
    with open(ruta, encoding="utf-8", newline="") as fh:
        yield from csv.DictReader(fh)


def construir_dimensiones(rutas):
    """
    Primera pasada. Para cada dimension reune, por llave natural, el nombre que
    tuvo en cada ejercicio. Tambien acumula conteos y totales de origen, que
    despues sirven para validar lo cargado.
    """
    # historia[tabla][llave][ciclo] = Counter {descripcion: renglones}
    historia = {tabla: defaultdict(lambda: defaultdict(Counter)) for tabla, _, _ in DIMENSIONES}
    conteo = defaultdict(int)
    totales = defaultdict(lambda: {m: Decimal(0) for m in MEDIDAS})

    for ruta in rutas:
        print("   leyendo " + ruta.name, flush=True)
        for fila in leer(ruta):
            ciclo = int(fila["ciclo"])
            conteo[ciclo] += 1
            for m in MEDIDAS:
                totales[ciclo][m] += Decimal(fila[m])
            for tabla, claves, desc in DIMENSIONES:
                llave = tuple(fila[c] for c in claves)
                historia[tabla][llave][ciclo][fila[desc]] += 1

    return historia, conteo, totales


def mas_usada(contador):
    """Descripcion con mas renglones; empate resuelto por orden alfabetico para ser determinista."""
    return sorted(contador.items(), key=lambda kv: (-kv[1], kv[0]))[0][0]


def conformar(historia):
    """
    Dimension conformada: una fila por llave, con el nombre del ejercicio mas
    reciente en que la llave aparece; si en ese ejercicio hay varios, el mas
    usado. Todas las variantes, con su numero de renglones, se conservan aparte.
    """
    dims = {}
    variantes = []
    conflictos = defaultdict(int)
    for tabla, llaves in historia.items():
        filas = []
        for llave, por_ciclo in llaves.items():
            reciente = max(por_ciclo)
            filas.append(list(llave) + [mas_usada(por_ciclo[reciente])])
            for ciclo, contador in por_ciclo.items():
                if len(contador) > 1:
                    conflictos[(tabla, ciclo)] += 1
                for descripcion, renglones in contador.items():
                    variantes.append((tabla, "|".join(llave), ciclo, descripcion, renglones))
        dims[tabla] = filas
    return dims, variantes, conflictos


def copiar(cur, tabla, columnas, filas):
    sentencia = "COPY {}.{} ({}) FROM STDIN".format(ESQUEMA, tabla, ", ".join(columnas))
    with cur.copy(sentencia) as cp:
        for fila in filas:
            cp.write_row(fila)


def filas_hecho(rutas):
    """Segunda pasada: proyecta de cada renglon solo las columnas de la tabla de hechos."""
    for ruta in rutas:
        print("   copiando " + ruta.name, flush=True)
        for fila in leer(ruta):
            yield [fila[c] for c in COLUMNAS_HECHO]


def main():
    cargar_env()
    rutas = archivos()
    inicio = datetime.now()

    print("1. construyendo dimensiones ...", flush=True)
    historia, conteo, totales = construir_dimensiones(rutas)
    dims, variantes, conflictos = conformar(historia)

    tablas = ["hecho_gasto", "descripcion_historica"] + [t for t, _, _ in DIMENSIONES]

    with psycopg.connect() as conn:
        base = conn.info.dbname
        print("2. conectado a la base " + base, flush=True)

        with conn.transaction():
            with conn.cursor() as cur:
                cur.execute("TRUNCATE {} RESTART IDENTITY".format(
                    ", ".join(ESQUEMA + "." + t for t in tablas)))

                print("3. cargando dimensiones ...", flush=True)
                # DIMENSIONES ya viene ordenada respetando las llaves foraneas.
                for tabla, claves, desc in DIMENSIONES:
                    copiar(cur, tabla, claves + [desc], dims[tabla])
                    print("   {:<32} {:>7,} filas".format(tabla, len(dims[tabla])), flush=True)
                copiar(cur, "descripcion_historica",
                       ["dimension", "llave", "ciclo", "descripcion", "renglones"], variantes)

                print("4. cargando hechos ...", flush=True)
                copiar(cur, "hecho_gasto", COLUMNAS_HECHO, filas_hecho(rutas))

                print("5. validando ...", flush=True)
                cur.execute(
                    "SELECT ciclo, count(*), " + ", ".join("sum(" + m + ")" for m in MEDIDAS)
                    + " FROM {}.hecho_gasto GROUP BY ciclo ORDER BY ciclo".format(ESQUEMA))
                cargado = {r[0]: r for r in cur.fetchall()}

                errores = []
                for ciclo in sorted(conteo):
                    r = cargado.get(ciclo)
                    if r is None:
                        errores.append("ciclo {}: no se cargo".format(ciclo))
                        continue
                    if r[1] != conteo[ciclo]:
                        errores.append("ciclo {}: {} renglones en origen, {} cargados".format(
                            ciclo, conteo[ciclo], r[1]))
                    for i, m in enumerate(MEDIDAS, start=2):
                        if r[i] != totales[ciclo][m]:
                            errores.append("ciclo {} / {}: origen {} cargado {}".format(
                                ciclo, m, totales[ciclo][m], r[i]))
                if errores:
                    # Levantar la excepcion revierte la transaccion completa.
                    raise RuntimeError("La validacion fallo:\n  " + "\n  ".join(errores))

    duracion = (datetime.now() - inicio).total_seconds()
    escribir_bitacora(base, rutas, dims, variantes, conflictos, conteo, totales, duracion)
    print("")
    print("carga completa y validada en {:.0f} s".format(duracion))
    print("bitacora escrita en " + str(BITACORA.relative_to(RAIZ)))


def escribir_bitacora(base, rutas, dims, variantes, conflictos, conteo, totales, duracion):
    L = []
    L.append("# Bitacora de carga")
    L.append("")
    L.append("Generada el " + datetime.now().strftime("%Y-%m-%d %H:%M")
             + " por `src/cargar_base.py`, sobre la base `" + base + "`.")
    L.append("")
    L.append("La carga ocurre en una sola transaccion y termina con una validacion: los "
             "conteos y los totales por etapa de cada ejercicio se comparan contra el "
             "archivo de origen al peso. Si algo no coincide, la transaccion se revierte "
             "completa. Que exista esta bitacora significa que la validacion paso.")

    L.append("")
    L.append("## Dimensiones conformadas")
    L.append("")
    L.append("| Tabla | Filas |")
    L.append("|---|---:|")
    for tabla, _, _ in DIMENSIONES:
        L.append("| `{}` | {:,} |".format(tabla, len(dims[tabla])))
    L.append("| `descripcion_historica` | {:,} |".format(len(variantes)))

    L.append("")
    L.append("## Claves con mas de un nombre dentro del mismo ejercicio")
    L.append("")
    L.append("Defecto del dato de origen: aparece en los dos formatos publicados. La "
             "dimension conformada toma el nombre del ejercicio mas reciente y, si ahi "
             "tambien hay varios, el mas usado. Todas las variantes quedan en "
             "`descripcion_historica` con su numero de renglones.")
    L.append("")
    if conflictos:
        L.append("| Dimension | Ejercicio | Claves afectadas |")
        L.append("|---|---|---:|")
        for (tabla, ciclo), n in sorted(conflictos.items()):
            L.append("| `{}` | {} | {:,} |".format(tabla, ciclo, n))
    else:
        L.append("Ninguna.")

    L.append("")
    L.append("## Hechos cargados y validados")
    L.append("")
    L.append("| Ejercicio | Renglones | Aprobado (MDP) | Devengado (MDP) | Pagado (MDP) |")
    L.append("|---|---:|---:|---:|---:|")
    for ciclo in sorted(conteo):
        t = totales[ciclo]
        L.append("| {} | {:,} | {:,.1f} | {:,.1f} | {:,.1f} |".format(
            ciclo, conteo[ciclo], t["aprobado"] / 1000000,
            t["devengado"] / 1000000, t["pagado"] / 1000000))
    L.append("| **Total** | **{:,}** | | | |".format(sum(conteo.values())))

    L.append("")
    L.append("Archivos de origen: " + ", ".join("`" + r.name + "`" for r in rutas) + ".")
    L.append("")
    L.append("Duracion: {:.0f} segundos.".format(duracion))

    BITACORA.parent.mkdir(parents=True, exist_ok=True)
    BITACORA.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
