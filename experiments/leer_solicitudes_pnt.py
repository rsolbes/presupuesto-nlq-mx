"""
Lectura de las solicitudes de informacion descargadas de la PNT.

Los archivos que entrega la Plataforma Nacional de Transparencia tienen dos
defectos que impiden leerlos con un lector JSON estandar:

  - Codificacion Windows-1252, no UTF-8. Se nota en las comillas tipograficas
    (bytes 0x93 y 0x94), que en esa codificacion son caracteres validos.
  - Comillas sin escapar dentro del texto de los ciudadanos, que rompen el
    JSON: el analizador interpreta la comilla como fin del valor.

La estructura, en cambio, es regular: un registro por linea y los campos
siempre en el mismo orden. Cada registro se intenta leer como JSON; si falla,
se reconstruye extrayendo cada valor entre dos nombres de campo conocidos, que
no dependen de que las comillas del texto esten bien escapadas.

Este modulo solo lee y repara. No selecciona preguntas: esa decision es del
autor, pregunta por pregunta (ver eval/README.md).

Ademas exporta las candidatas para el conjunto de evaluacion: solicitudes de
informacion publica (no de datos personales) que contienen al menos una palabra
del nucleo presupuestario. A cada candidata se le asigna un orden aleatorio
reproducible, y la revision procede en ese orden.

Uso:    python experiments/leer_solicitudes_pnt.py
Salida: experiments/salidas/solicitudes_pnt.md
        data/interim/solicitudes_candidatas.csv
"""

import csv
import json
import random
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
ORIGEN = RAIZ / "data" / "raw" / "pnt_solicitudes"
INFORME = RAIZ / "experiments" / "salidas" / "solicitudes_pnt.md"
CANDIDATAS = RAIZ / "data" / "interim" / "solicitudes_candidatas.csv"

# Filtro de candidatas. Prefijos, sin acentos, al inicio de palabra.
# Calibrado sobre una muestra aleatoria de 2026: las solicitudes que solo
# contenian palabras genericas ("monto", "recursos") no trataban de gasto
# publico en ningun caso, por lo que se excluyen del filtro.
NUCLEO = ["presupuest", "gasto", "ejercid", "devengad", "erogac", "erogad",
          "cuenta publica", "partida", "programa presupuestario"]
SEMILLA = 20260918

CAMPOS = [
    "Folio", "FechaSolicitud", "Dependencia", "Estatus", "MedioEntrada",
    "TipoSolicitud", "DescripcionSolicitud", "OtrosDatos", "ArchivosAdjuntos",
    "MedioEntrega", "FechaLimite", "Respuesta", "TextoRespuesta", "FechaRespuesta",
    "FechaSolicitudTermino", "Pais", "Estado", "Municipio", "CodigoPostal",
    "Sector", "Prorroga", "Prevencion", "Disponibilidad", "TipoDerechoARCOP",
    "Queja", "FechaOficialRecepcion",
]

# Cada valor se toma de forma perezosa hasta el siguiente nombre de campo
# conocido, que funciona como delimitador confiable aunque el texto del
# ciudadano contenga comillas sin escapar.
PATRON = re.compile(
    r"^\{"
    + ",".join(r'"{0}":"(?P<{0}>.*?)"'.format(c) for c in CAMPOS)
    + r"\}$",
    re.DOTALL,
)
COMILLA_SIN_ESCAPAR = re.compile(r'(?<!\\)"')


def desescapar(v):
    """Interpreta las secuencias de escape JSON de un valor extraido a mano."""
    try:
        return json.loads('"' + v + '"')
    except json.JSONDecodeError:
        return json.loads('"' + COMILLA_SIN_ESCAPAR.sub(r'\\"', v) + '"')


def leer(ruta):
    """Devuelve (registros, estadisticas) de un archivo de solicitudes."""
    texto = ruta.read_bytes().decode("cp1252")
    registros, est = [], Counter()
    for linea in texto.splitlines():
        linea = linea.strip().lstrip(",").rstrip(",")
        if not linea.startswith('{"Folio"'):
            continue
        est["registros"] += 1
        try:
            registros.append(json.loads(linea))
            est["json_valido"] += 1
            continue
        except json.JSONDecodeError:
            pass
        m = PATRON.match(linea)
        if m:
            registros.append({c: desescapar(m.group(c)) for c in CAMPOS})
            est["reparados"] += 1
        else:
            est["irrecuperables"] += 1
    return registros, est


def aaaammdd(fecha):
    """dd/mm/aaaa -> aaaammdd, para ordenar."""
    d, m, a = fecha.split("/")
    return a + m + d


def normalizar(texto):
    t = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def palabras_nucleo(texto):
    t = normalizar(texto)
    return [k for k in NUCLEO if re.search(r"\b" + re.escape(k), t)]


def candidatas(nombre_archivo, registros):
    """
    Solicitudes de informacion publica con alguna palabra del nucleo, cada una
    con su posicion en un orden aleatorio reproducible. La semilla se deriva
    del nombre del archivo: agregar otros anos no altera el orden de este.

    Se deduplica por folio antes de sortear. La exportacion de la PNT puede
    repetir una solicitud: en 2025, un mismo folio aparece 37 veces, con las
    copias identicas salvo en TipoDerechoARCOP. Sin deduplicar, esa solicitud
    tendria 37 oportunidades de salir en el sorteo en lugar de una.
    """
    elegidas, vistos = [], set()
    for r in registros:
        if r["Folio"] in vistos:
            continue
        vistos.add(r["Folio"])
        if r.get("TipoSolicitud") != "Información pública":
            continue
        ks = palabras_nucleo(r.get("DescripcionSolicitud", ""))
        if ks:
            elegidas.append((r, ks))
    elegidas.sort(key=lambda x: x[0]["Folio"])
    orden = list(range(1, len(elegidas) + 1))
    random.Random("{}-{}".format(SEMILLA, nombre_archivo)).shuffle(orden)
    return sorted(((pos, r, ks) for pos, (r, ks) in zip(orden, elegidas)), key=lambda x: x[0])


UMBRAL_SIMILITUD = 0.6


def grupos_similares(textos):
    """
    Agrupa solicitudes casi identicas: dos solicitudes son similares si el
    indice de Jaccard entre sus conjuntos de palabras (normalizadas, de cuatro
    letras o mas) es de al menos UMBRAL_SIMILITUD. Los grupos se cierran por
    transitividad. Detecta campanas de solicitudes con la misma plantilla y
    solicitudes que repiten una pregunta cambiando solo un dato.

    Devuelve, para cada texto, el indice del representante de su grupo.
    """
    conjuntos = [set(w for w in re.findall(r"[a-z]+", normalizar(t)) if len(w) >= 4)
                 for t in textos]
    padre = list(range(len(textos)))

    def raiz(i):
        while padre[i] != i:
            padre[i] = padre[padre[i]]
            i = padre[i]
        return i

    # Ordenar por tamano permite descartar pares cuya diferencia de tamano ya
    # hace imposible alcanzar el umbral, sin compararlos.
    orden = sorted(range(len(textos)), key=lambda i: len(conjuntos[i]))
    for a_pos, i in enumerate(orden):
        a = conjuntos[i]
        if not a:
            continue
        for j in orden[a_pos + 1:]:
            b = conjuntos[j]
            if len(a) < UMBRAL_SIMILITUD * len(b):
                break
            if len(a & b) >= UMBRAL_SIMILITUD * len(a | b):
                padre[raiz(i)] = raiz(j)
    return [raiz(i) for i in range(len(textos))]


def exportar_candidatas(por_archivo_regs):
    CANDIDATAS.parent.mkdir(parents=True, exist_ok=True)
    filas = []
    for nombre, regs in por_archivo_regs:
        for pos, r, ks in candidatas(nombre, regs):
            filas.append([nombre, pos, r["Folio"], r["FechaSolicitud"], " ".join(ks),
                          r.get("Respuesta", ""),
                          " ".join(r.get("DescripcionSolicitud", "").split()),
                          " ".join(r.get("TextoRespuesta", "").split())])

    # El grupo se identifica por el folio menor de sus miembros. Es estable ante
    # el orden de los archivos, pero NO ante archivos nuevos: si llega una
    # solicitud de folio menor que se une al grupo, el identificador cambia.
    # Por eso el registro de revision cita al representante del grupo (su
    # pregunta y su folio), nunca el identificador del grupo.
    rep = grupos_similares([f[6] for f in filas])
    miembros = Counter(rep)
    folio_menor = {}
    for k, f in zip(rep, filas):
        folio_menor[k] = min(folio_menor.get(k, f[2]), f[2])

    total, grupos = Counter(), Counter()
    # utf-8-sig: Excel en Windows solo reconoce los acentos de un CSV UTF-8 si lleva BOM.
    with open(CANDIDATAS, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["archivo", "orden_aleatorio", "folio", "fecha_solicitud", "palabras_clave",
                    "tipo_respuesta", "solicitud", "texto_respuesta",
                    "grupo_similar", "tamano_grupo"])
        for k, f in zip(rep, filas):
            n = miembros[k]
            w.writerow(f + (["G" + folio_menor[k], n] if n > 1 else ["", 1]))
            total[f[0]] += 1
            if n > 1:
                grupos["G" + folio_menor[k]] = n
    return total, grupos


def main():
    rutas = sorted(ORIGEN.glob("*.JSON")) + sorted(ORIGEN.glob("*.json"))
    rutas = sorted(set(rutas))
    if not rutas:
        sys.exit("No hay archivos en " + str(ORIGEN.relative_to(RAIZ)))

    todos, por_archivo, por_archivo_regs = [], [], []
    for ruta in rutas:
        regs, est = leer(ruta)
        fechas = sorted(aaaammdd(r["FechaSolicitud"]) for r in regs if r.get("FechaSolicitud"))
        por_archivo.append((ruta.name, est, fechas[0] if fechas else "", fechas[-1] if fechas else ""))
        por_archivo_regs.append((ruta.name, regs))
        todos.extend(regs)
        print("{}: {:,} registros, {:,} reparados, {:,} irrecuperables".format(
            ruta.name, est["registros"], est["reparados"], est["irrecuperables"]))

    L = ["# Solicitudes de informacion de la PNT: lectura", ""]
    L.append("Generado el " + datetime.now().strftime("%Y-%m-%d %H:%M")
             + " por `experiments/leer_solicitudes_pnt.py`. Solo estadisticas: "
               "el texto de las solicitudes no se reproduce aqui.")
    L += ["", "## Archivos", "",
          "| Archivo | Registros | JSON valido | Reparados | Irrecuperables | Folios unicos | Primera solicitud | Ultima |",
          "|---|---:|---:|---:|---:|---:|---|---|"]
    regs_por_nombre = dict(por_archivo_regs)
    for nombre, est, f0, f1 in por_archivo:
        unicos = len({r["Folio"] for r in regs_por_nombre[nombre]})
        L.append("| `{}` | {:,} | {:,} | {:,} | {:,} | {:,} | {} | {} |".format(
            nombre, est["registros"], est["json_valido"], est["reparados"],
            est["irrecuperables"], unicos, f0, f1))

    L += ["", "Folios unicos: {:,} de {:,} registros.".format(
        len({r["Folio"] for r in todos}), len(todos))]

    for campo in ["TipoSolicitud", "TipoDerechoARCOP", "Dependencia", "Estatus", "Respuesta"]:
        L += ["", "## " + campo, "", "| Valor | Registros |", "|---|---:|"]
        for v, n in Counter(r.get(campo, "") for r in todos).most_common():
            L.append("| {} | {:,} |".format(v or "(vacio)", n))

    total, grupos = exportar_candidatas(por_archivo_regs)
    L += ["", "## Candidatas para el conjunto de evaluacion", "",
          "Solicitudes de informacion publica con al menos una palabra del nucleo: "
          + ", ".join("`" + k + "`" for k in NUCLEO) + ". Se excluyen las de datos personales.",
          "",
          "Orden de revision aleatorio y reproducible, con semilla `{}` combinada con el "
          "nombre de cada archivo.".format(SEMILLA),
          "", "| Archivo | Candidatas |", "|---|---:|"]
    for nombre, n in total.items():
        L.append("| `{}` | {:,} |".format(nombre, n))

    en_grupo = sum(grupos.values())
    L += ["", "## Solicitudes casi identicas", "",
          "Dos candidatas son casi identicas si el indice de Jaccard entre sus conjuntos de "
          "palabras es de al menos {}. Detecta campanas con una misma plantilla y solicitudes "
          "que repiten una pregunta cambiando solo un dato (un estado, un municipio, una "
          "dependencia).".format(UMBRAL_SIMILITUD),
          "",
          "{:,} de {:,} candidatas ({:.1%}) pertenecen a uno de {} grupos. En la revision, solo "
          "el primer miembro de cada grupo que aparece en el orden aleatorio se evalua; los "
          "demas se registran como casi duplicados.".format(
              en_grupo, sum(total.values()), en_grupo / max(1, sum(total.values())), len(grupos)),
          "", "| Grupo | Solicitudes |", "|---|---:|"]
    for g, n in grupos.most_common():
        L.append("| `{}` | {:,} |".format(g, n))

    INFORME.parent.mkdir(parents=True, exist_ok=True)
    INFORME.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("{:,} candidatas exportadas a {}".format(sum(total.values()), CANDIDATAS.relative_to(RAIZ)))
    print("informe escrito en " + str(INFORME.relative_to(RAIZ)))


if __name__ == "__main__":
    main()
