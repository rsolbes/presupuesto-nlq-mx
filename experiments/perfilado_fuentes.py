"""
Perfilado de las fuentes crudas de Cuenta Publica (SHCP).

Recorre los archivos CSV de data/raw/ y produce un informe con:
  - huella del archivo (tamano, sha256, codificacion detectada)
  - estructura declarada frente a estructura real
  - renglones utiles, de relleno y malformados
  - mapa canonico de columnas entre las convenciones de nombres de cada ejercicio
  - totales por medida y ejercicio
  - validacion de las llaves naturales (simples y compuestas)

Uso:    python experiments/perfilado_fuentes.py
Salida: experiments/salidas/perfil_fuentes.md
"""

import csv
import hashlib
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

csv.field_size_limit(10 ** 9)

RAIZ = Path(__file__).resolve().parents[1]
CRUDO = RAIZ / "data" / "raw"
SALIDA = RAIZ / "experiments" / "salidas" / "perfil_fuentes.md"

# Nombres canonicos, en el orden posicional que comparten los seis ejercicios.
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

# Encabezados conocidos por convencion. Validan el mapeo posicional: si aparece
# un encabezado fuera de estas listas, el informe lo marca para revision manual.
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

# Llaves naturales a validar: (columnas de clave, columna de descripcion).
LLAVES = [
    (["ramo_id"], "ramo_desc"),
    (["finalidad_id"], "finalidad_desc"),
    (["modalidad_id"], "modalidad_desc"),
    (["partida_id"], "partida_desc"),
    (["tipogasto_id"], "tipogasto_desc"),
    (["ff_id"], "ff_desc"),
    (["entidad_id"], "entidad_desc"),
    (["ramo_id", "ur_id"], "ur_desc"),
    (["finalidad_id", "funcion_id"], "funcion_desc"),
    (["finalidad_id", "funcion_id", "subfuncion_id"], "subfuncion_desc"),
    (["ramo_id", "ai_id"], "ai_desc"),
    (["ramo_id", "modalidad_id", "pp_id"], "pp_desc"),
]


def sha256(ruta, bloque=1 << 20):
    h = hashlib.sha256()
    with open(ruta, "rb") as fh:
        for trozo in iter(lambda: fh.read(bloque), b""):
            h.update(trozo)
    return h.hexdigest()


def detectar_codificacion(ruta):
    """Primera codificacion con la que el archivo entero resulta legible."""
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            with open(ruta, encoding=enc) as fh:
                while fh.read(1 << 20):
                    pass
            return enc
        except UnicodeDecodeError:
            continue
    return None


def a_decimal(txt):
    """Los importes llegan como texto, a veces con separador de miles."""
    if txt is None:
        return None
    t = txt.strip().replace(",", "")
    if not t:
        return None
    try:
        return Decimal(t)
    except InvalidOperation:
        return None


def perfilar(ruta):
    r = {"archivo": ruta.name, "mb": round(ruta.stat().st_size / 1e6, 1)}
    r["sha256"] = sha256(ruta)[:16]
    enc = detectar_codificacion(ruta)
    r["codificacion"] = enc or "ilegible"
    if enc is None:
        return r

    with open(ruta, encoding=enc, newline="") as fh:
        lector = csv.reader(fh)
        crudo = [c.strip() for c in next(lector)]
        r["cols_declaradas"] = len(crudo)
        nombradas = [c for c in crudo if c]
        r["cols_nombradas"] = len(nombradas)
        r["encabezado"] = nombradas

        # Mapeo posicional contra los nombres canonicos, validado por nombre.
        r["desconocidos"] = [
            (canon, real)
            for canon, real in zip(CANONICO, nombradas)
            if real not in VARIANTES.get(canon, set())
        ]
        idx = {canon: i for i, canon in enumerate(CANONICO[: len(nombradas)])}

        utiles = relleno = malformados = 0
        sumas = {m: Decimal(0) for m in MEDIDAS}
        no_numericos = {m: 0 for m in MEDIDAS}
        distintos = {c: set() for c in idx}
        mapas = {tuple(k): {} for k, _ in LLAVES}

        for fila in lector:
            if not fila or not fila[0].strip():
                relleno += 1
                continue
            if len(fila) != r["cols_declaradas"]:
                malformados += 1
                continue
            utiles += 1
            for c, i in idx.items():
                distintos[c].add(fila[i])
            for m in MEDIDAS:
                v = a_decimal(fila[idx[m]])
                if v is None:
                    no_numericos[m] += 1
                else:
                    sumas[m] += v
            for claves, desc in LLAVES:
                k = tuple(fila[idx[c]] for c in claves)
                mapas[tuple(claves)].setdefault(k, set()).add(fila[idx[desc]])

    r.update(
        utiles=utiles,
        relleno=relleno,
        malformados=malformados,
        sumas=sumas,
        no_numericos=no_numericos,
        cardinalidad={c: len(v) for c, v in distintos.items()},
        llaves=[
            {
                "llave": "+".join(claves),
                "grupos": len(mapas[tuple(claves)]),
                "max_desc": max((len(v) for v in mapas[tuple(claves)].values()), default=0),
            }
            for claves, _ in LLAVES
        ],
    )
    return r


def etiqueta(nombre):
    return (nombre.replace("cuenta_publica_", "")
                  .replace("_gf_ecd_epe", "")
                  .replace(".csv", ""))


def informe(perfiles):
    L = []
    L.append("# Perfilado de las fuentes crudas - Cuenta Publica (SHCP)")
    L.append("")
    L.append("Generado el " + date.today().isoformat()
             + " por `experiments/perfilado_fuentes.py`.")

    L.append("")
    L.append("## 1. Huella de cada archivo")
    L.append("")
    L.append("| Archivo | MB | sha256 (16) | Codificacion | Cols. declaradas | Cols. con nombre |")
    L.append("|---|---:|---|---|---:|---:|")
    for p in perfiles:
        L.append("| {} | {} | `{}` | {} | {} | {} |".format(
            p["archivo"], p["mb"], p["sha256"], p["codificacion"],
            p.get("cols_declaradas", "-"), p.get("cols_nombradas", "-")))

    L.append("")
    L.append("## 2. Renglones")
    L.append("")
    L.append("| Archivo | Utiles | De relleno | Malformados |")
    L.append("|---|---:|---:|---:|")
    for p in perfiles:
        L.append("| {} | {:,} | {:,} | {:,} |".format(
            p["archivo"], p.get("utiles", 0), p.get("relleno", 0), p.get("malformados", 0)))

    L.append("")
    L.append("## 3. Mapa canonico de columnas")
    L.append("")
    L.append("Cada ejercicio publica la misma informacion con nombres distintos. "
             "El mapeo es posicional y se valida contra los nombres conocidos.")
    L.append("")
    L.append("| Canonico | " + " | ".join(etiqueta(p["archivo"]) for p in perfiles) + " |")
    L.append("|---" * (len(perfiles) + 1) + "|")
    for i, canon in enumerate(CANONICO):
        celdas = [p["encabezado"][i] if i < len(p.get("encabezado", [])) else "-"
                  for p in perfiles]
        L.append("| `" + canon + "` | " + " | ".join(celdas) + " |")

    desconocidos = [(p["archivo"], p["desconocidos"]) for p in perfiles if p.get("desconocidos")]
    L.append("")
    if desconocidos:
        L.append("**Encabezados no reconocidos** (revisar antes de cargar):")
        L.append("")
        for arch, ds in desconocidos:
            for canon, real in ds:
                L.append("- `" + arch + "`: la posicion de `" + canon + "` trae `" + real + "`")
    else:
        L.append("Todos los encabezados corresponden a variantes ya conocidas.")

    L.append("")
    L.append("## 4. Totales por medida (millones de pesos)")
    L.append("")
    L.append("| Archivo | " + " | ".join(m.capitalize() for m in MEDIDAS) + " |")
    L.append("|---" * (len(MEDIDAS) + 1) + "|")
    for p in perfiles:
        if "sumas" not in p:
            continue
        vals = ["{:,.1f}".format(p["sumas"][m] / 1000000) for m in MEDIDAS]
        L.append("| " + p["archivo"] + " | " + " | ".join(vals) + " |")

    nn = [(p["archivo"], m, p["no_numericos"][m])
          for p in perfiles if "no_numericos" in p
          for m in MEDIDAS if p["no_numericos"][m]]
    if nn:
        L.append("")
        L.append("**Valores no numericos en columnas de importe:**")
        L.append("")
        for arch, m, n in nn:
            L.append("- `{}` / `{}`: {:,} valores".format(arch, m, n))

    L.append("")
    L.append("## 5. Llaves naturales")
    L.append("")
    L.append("`max_desc` es el mayor numero de descripciones distintas asociadas a una misma "
             "llave. Debe ser 1: si es mayor, esa columna no identifica por si sola y la llave "
             "tiene que componerse.")
    for p in perfiles:
        if "llaves" not in p:
            continue
        L.append("")
        L.append("### " + p["archivo"])
        L.append("")
        L.append("| Llave | Grupos | max_desc | Veredicto |")
        L.append("|---|---:|---:|---|")
        for k in p["llaves"]:
            v = "unica" if k["max_desc"] == 1 else "AMBIGUA"
            L.append("| `{}` | {:,} | {} | {} |".format(k["llave"], k["grupos"], k["max_desc"], v))

    L.append("")
    L.append("## 6. Cardinalidad de las columnas de clave")
    L.append("")
    cols = [c for c in CANONICO if c.endswith("_id") or c == "ciclo"]
    L.append("| Archivo | " + " | ".join("`" + c + "`" for c in cols) + " |")
    L.append("|---" * (len(cols) + 1) + "|")
    for p in perfiles:
        if "cardinalidad" not in p:
            continue
        vals = [str(p["cardinalidad"].get(c, "-")) for c in cols]
        L.append("| " + p["archivo"] + " | " + " | ".join(vals) + " |")

    return "\n".join(L) + "\n"


def main():
    archivos = sorted(CRUDO.glob("cuenta_publica_*.csv"))
    if not archivos:
        sys.exit("No hay archivos que perfilar en " + str(CRUDO))
    perfiles = []
    for ruta in archivos:
        print("perfilando " + ruta.name + " ...", flush=True)
        perfiles.append(perfilar(ruta))
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(informe(perfiles), encoding="utf-8")
    print("")
    print("informe escrito en " + str(SALIDA.relative_to(RAIZ)))


if __name__ == "__main__":
    main()
