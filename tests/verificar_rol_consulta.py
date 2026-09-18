"""
Verificacion reproducible del rol de solo lectura consulta_nlq.

Ejecuta, conectado como consulta_nlq, las pruebas que demuestran cada
contramedida de src/sql/03_rol_consulta.sql, y compara el resultado contra lo
esperado: un valor, o un codigo SQLSTATE concreto. Una prueba que falla por una
razon distinta a la esperada cuenta como fallida: el error tiene que ser el
correcto, no cualquier error.

Distingue las dos clases de proteccion:
  barrera   la sesion no puede quitarla (privilegios, confinamiento a la base)
  barandal  la sesion puede cambiarla (solo lectura, tiempo limite)

Cada prueba abre su propia conexion, para que un error no deje abortada la
transaccion de las siguientes.

Requiere en .env: PGHOST, PGPORT, PGDATABASE, CONSULTA_PGUSER, CONSULTA_PGPASSWORD.
Uso:    python tests/verificar_rol_consulta.py
Salida: docs/pruebas_seguridad.md   (codigo de salida 1 si alguna prueba falla)
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import psycopg

RAIZ = Path(__file__).resolve().parents[1]
ENV = RAIZ / ".env"
SALIDA = RAIZ / "docs" / "pruebas_seguridad.md"


# (nombre, tipo, sentencias, base, esperado, que demuestra)
#   esperado = ("valor", x)       la ultima sentencia devuelve x
#            = ("sqlstate", "c")  falla con ese codigo exacto
#            = ("rechazo", None)  la conexion misma es rechazada por permisos
PRUEBAS = [
    ("identidad", "control",
     ["SELECT current_user"], None, ("valor", "consulta_nlq"),
     "la prueba corre realmente como el rol"),
    ("lee la capa semantica", "acceso",
     ["SELECT 1 FROM semantica.gasto LIMIT 1"], None, ("valor", 1),
     "acceso a lo que el sistema necesita"),
    ("lee el esquema crudo", "acceso",
     ["SELECT 1 FROM crudo.hecho_gasto LIMIT 1"], None, ("valor", 1),
     "acceso a la condicion de control experimental"),
    ("no lee las tablas base", "barrera",
     ["SELECT count(*) FROM presupuesto.hecho_gasto"], None, ("sqlstate", "42501"),
     "las tablas base solo son alcanzables a traves de vistas"),
    ("no escribe aun sin solo lectura", "barrera",
     ["BEGIN READ WRITE", "CREATE TABLE semantica.prueba (x int)"], None, ("sqlstate", "42501"),
     "los privilegios detienen la escritura aunque se desactive el barandal"),
    ("no crea tablas temporales", "barrera",
     ["BEGIN READ WRITE", "CREATE TEMP TABLE prueba_tmp (x int)"], None, ("sqlstate", "42501"),
     "sin permiso TEMPORARY sobre la base"),
    ("confinado a su base", "barrera",
     ["SELECT 1"], "postgres", ("rechazo", None),
     "no puede conectarse a otras bases del servidor"),
    ("solo lectura por defecto", "barandal",
     ["SHOW default_transaction_read_only"], None, ("valor", "on"),
     "toda transaccion inicia en solo lectura"),
    ("escritura bloqueada por defecto", "barandal",
     ["CREATE TABLE semantica.prueba (x int)"], None, ("sqlstate", "25006"),
     "el barandal detiene la escritura antes que los privilegios"),
    ("tiempo limite configurado", "barandal",
     ["SHOW statement_timeout"], None, ("valor", "15s"),
     "limite por sentencia"),
    ("tiempo limite efectivo", "barandal",
     ["SELECT pg_sleep(20)"], None, ("sqlstate", "57014"),
     "una sentencia de 20 s se cancela a los 15 s"),
]


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
    faltan = [v for v in ("PGDATABASE", "CONSULTA_PGUSER", "CONSULTA_PGPASSWORD")
              if not os.environ.get(v)]
    if faltan:
        sys.exit("Faltan valores en .env: " + ", ".join(faltan))


def conectar(base=None):
    # Usuario y contrasena se pasan explicitos: tienen precedencia sobre
    # PGUSER/PGPASSWORD del entorno, que son las credenciales del administrador.
    return psycopg.connect(
        host=os.environ.get("PGHOST", "localhost"),
        port=os.environ.get("PGPORT", "5432"),
        dbname=base or os.environ["PGDATABASE"],
        user=os.environ["CONSULTA_PGUSER"],
        password=os.environ["CONSULTA_PGPASSWORD"],
        autocommit=True,
        connect_timeout=10,
    )


def correr(sentencias, base):
    """Devuelve (True, valor) si todo corre, o (False, sqlstate, mensaje) si algo falla."""
    try:
        with conectar(base) as conn:
            valor = None
            for s in sentencias:
                cur = conn.execute(s)
                if cur.description:
                    valor = cur.fetchone()[0]
            return (True, valor)
    except psycopg.Error as e:
        mensaje = str(e).strip().splitlines()[0] if str(e).strip() else type(e).__name__
        return (False, getattr(e, "sqlstate", None), mensaje)


def evaluar(esperado, obtenido):
    tipo, x = esperado
    if tipo == "valor":
        return obtenido[0] and obtenido[1] == x
    if tipo == "sqlstate":
        return (not obtenido[0]) and obtenido[1] == x
    if tipo == "rechazo":
        # Un rechazo en el arranque de la conexion no trae SQLSTATE en psycopg;
        # se reconoce por el mensaje de permisos del servidor, en ingles o espanol.
        return (not obtenido[0]) and "permis" in obtenido[2].lower()
    return False


def describir(esperado):
    tipo, x = esperado
    if tipo == "valor":
        return "valor `{}`".format(x)
    if tipo == "sqlstate":
        return "SQLSTATE `{}`".format(x)
    return "conexion rechazada"


def describir_obtenido(obtenido):
    if obtenido[0]:
        return "valor `{}`".format(obtenido[1])
    if obtenido[1]:
        return "SQLSTATE `{}`".format(obtenido[1])
    return "error: " + obtenido[2]


def main():
    cargar_env()
    print("verificando el rol {} sobre {}".format(
        os.environ["CONSULTA_PGUSER"], os.environ["PGDATABASE"]), flush=True)

    resultados = []
    for nombre, tipo, sentencias, base, esperado, demuestra in PRUEBAS:
        obtenido = correr(sentencias, base)
        paso = evaluar(esperado, obtenido)
        resultados.append((nombre, tipo, esperado, obtenido, paso, demuestra))
        print("  {:<4} {:<10} {}".format("OK" if paso else "FALLA", tipo, nombre), flush=True)
        if not paso and not obtenido[0]:
            print("       " + obtenido[2], flush=True)

    fallidas = [r for r in resultados if not r[4]]
    escribir_informe(resultados)
    print("")
    print("{} de {} pruebas pasaron".format(len(resultados) - len(fallidas), len(resultados)))
    print("informe escrito en " + str(SALIDA.relative_to(RAIZ)))
    sys.exit(1 if fallidas else 0)


def escribir_informe(resultados):
    L = []
    L.append("# Verificacion del rol de solo lectura")
    L.append("")
    L.append("Generado el " + datetime.now().strftime("%Y-%m-%d %H:%M")
             + " por `tests/verificar_rol_consulta.py`, conectado como `"
             + os.environ["CONSULTA_PGUSER"] + "` a `" + os.environ["PGDATABASE"] + "`.")
    L.append("")
    L.append("Cada prueba compara el resultado contra un valor o un codigo SQLSTATE "
             "concreto: una prueba que falla por una razon distinta a la esperada "
             "cuenta como fallida.")
    L.append("")
    L.append("Una **barrera** no puede quitarla la propia sesion (privilegios, "
             "confinamiento a la base). Un **barandal** si puede cambiarse desde la "
             "sesion (`SET`, `BEGIN READ WRITE`, `set_config`), por lo que evita "
             "accidentes pero no es frontera de seguridad: la capa de orquestacion "
             "debe imponer su propio tiempo limite y rechazar `SET` y `set_config`.")
    L.append("")
    L.append("| Prueba | Tipo | Esperado | Obtenido | Resultado | Que demuestra |")
    L.append("|---|---|---|---|---|---|")
    for nombre, tipo, esperado, obtenido, paso, demuestra in resultados:
        L.append("| {} | {} | {} | {} | {} | {} |".format(
            nombre, tipo, describir(esperado), describir_obtenido(obtenido),
            "paso" if paso else "**FALLO**", demuestra))
    L.append("")
    L.append("Codigos SQLSTATE: `42501` privilegio insuficiente; `25006` escritura en "
             "transaccion de solo lectura; `57014` sentencia cancelada por tiempo limite.")

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
