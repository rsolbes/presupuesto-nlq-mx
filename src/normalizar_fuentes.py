"""
Normalizacion de las fuentes crudas de Cuenta Publica.

Lee los archivos publicados por la SHCP, aplica el mapa canonico de columnas y
escribe un CSV uniforme por ejercicio en data/interim/. Deja bitacora versionada
de cada decision aplicada.

Criterio de formato, derivado del cruce entre los dos formatos publicados
(ver experiments/salidas/cruce_xlsx_csv.md):

  2020-2024  ->  xlsx. Los CSV publicados pierden renglones en todos estos
                 ejercicios, y el de 2024 ademas reporta 9,699 millones de mas
                 en el ramo 51, cifra que no coincide con el informe oficial
                 de Cuenta Publica.
  2025       ->  csv. Los dos formatos son identicos y el csv se lee mas rapido.

Uso:    python src/normalizar_fuentes.py
Salida: data/interim/hechos_AAAA.csv  y  docs/bitacora_normalizacion.md
"""

import csv
import sys
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import openpyxl

from esquema import CANONICO, CORRECCIONES, MEDIDAS, VACIO_ES_CERO, mapear_encabezado

RAIZ = Path(__file__).resolve().parents[1]
CRUDO = RAIZ / "data" / "raw"
INTERMEDIO = RAIZ / "data" / "interim"
BITACORA = RAIZ / "docs" / "bitacora_normalizacion.md"

CENTAVO = Decimal("0.01")

FUENTES = {
    "2020": ("cuenta_publica_2020_gf_ecd_epe.xlsx", "xlsx"),
    "2021": ("cuenta_publica_2021_gf_ecd_epe.xlsx", "xlsx"),
    "2022": ("cuenta_publica_2022_gf_ecd_epe.xlsx", "xlsx"),
    "2023": ("cuenta_publica_2023_gf_ecd_epe.xlsx", "xlsx"),
    "2024": ("cuenta_publica_2024_gf_ecd_epe.xlsx", "xlsx"),
    "2025": ("cuenta_publica_2025_gf_ecd_epe.csv", "csv"),
}


def texto(v):
    """Normaliza una celda a texto sin alterar claves alfanumericas."""
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def importe(t, est):
    """Convierte un importe a Decimal con dos decimales."""
    t = t.replace(",", "").strip()
    if not t:
        est["vacios"] += 1
        return Decimal("0.00") if VACIO_ES_CERO else None
    try:
        return Decimal(t).quantize(CENTAVO)
    except InvalidOperation:
        est["no_numericos"] += 1
        return Decimal("0.00")


def filas_csv(ruta, est):
    with open(ruta, encoding="latin-1", newline="") as fh:
        lector = csv.reader(fh)
        encabezado = [c.strip() for c in next(lector)]
        ncol = len(encabezado)
        yield encabezado
        for fila in lector:
            if not fila or not fila[0].strip():
                est["relleno"] += 1
                continue
            if len(fila) != ncol:
                est["malformados"] += 1
                est["muestras_malformados"].append(len(fila))
                continue
            yield [c.strip() for c in fila]


def filas_xlsx(ruta, est):
    wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    it = ws.iter_rows(values_only=True)
    encabezado = [texto(c) for c in next(it)]
    yield encabezado
    for fila in it:
        if fila is None or fila[0] in (None, ""):
            est["relleno"] += 1
            continue
        yield [texto(v) for v in fila]
    wb.close()


def normalizar(anio, archivo, formato):
    ruta = CRUDO / archivo
    est = {
        "anio": anio, "archivo": archivo, "formato": formato,
        "utiles": 0, "relleno": 0, "malformados": 0, "muestras_malformados": [],
        "vacios": 0, "no_numericos": 0, "correcciones": {},
        "sumas": {m: Decimal(0) for m in MEDIDAS},
    }

    origen = filas_csv(ruta, est) if formato == "csv" else filas_xlsx(ruta, est)
    encabezado = next(origen)
    idx = mapear_encabezado(encabezado)
    est["encabezado_origen"] = [c for c in encabezado if c]

    destino = INTERMEDIO / ("hechos_" + anio + ".csv")
    INTERMEDIO.mkdir(parents=True, exist_ok=True)

    with open(destino, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
        w.writerow(CANONICO)
        for fila in origen:
            salida = []
            for canon in CANONICO:
                v = fila[idx[canon]]
                if canon in MEDIDAS:
                    salida.append(str(importe(v, est)))
                    continue
                arreglos = CORRECCIONES.get(canon)
                if arreglos and v in arreglos:
                    est["correcciones"][v] = est["correcciones"].get(v, 0) + 1
                    v = arreglos[v]
                salida.append(v)
            for m in MEDIDAS:
                est["sumas"][m] += Decimal(salida[CANONICO.index(m)])
            w.writerow(salida)
            est["utiles"] += 1

    est["destino"] = destino.name
    est["mb"] = round(destino.stat().st_size / 1e6, 1)
    return est


def bitacora(resultados):
    L = []
    L.append("# Bitacora de normalizacion de fuentes")
    L.append("")
    L.append("Generada el " + date.today().isoformat()
             + " por `src/normalizar_fuentes.py`.")
    L.append("")
    L.append("Registra que se hizo con cada archivo publicado antes de cargarlo. "
             "Las correcciones sobre el dato original se aplican de forma declarada: "
             "corregir en silencio seria indistinguible de alterarlo.")

    L.append("")
    L.append("## Formato elegido por ejercicio")
    L.append("")
    L.append("La SHCP publica cada ejercicio en csv y en xlsx. No son equivalentes.")
    L.append("")
    L.append("| Ejercicio | Archivo de origen | Formato | Motivo |")
    L.append("|---|---|---|---|")
    motivos = {
        "2020": "el csv publicado pierde 10 renglones",
        "2021": "el csv publicado pierde 2 renglones y deja importes en blanco",
        "2022": "el csv publicado pierde 3 renglones y trae 828,067 de relleno",
        "2023": "el csv publicado pierde 1 renglon y corrompe una llave",
        "2024": "el csv publicado reporta 9,699 MDP de mas en el ramo 51, "
                "cifra que no coincide con el informe oficial de Cuenta Publica",
        "2025": "ambos formatos son identicos; el csv se lee mas rapido",
    }
    for r in resultados:
        L.append("| {} | `{}` | {} | {} |".format(
            r["anio"], r["archivo"], r["formato"], motivos.get(r["anio"], "")))

    L.append("")
    L.append("## Renglones procesados")
    L.append("")
    L.append("| Ejercicio | Utiles | De relleno | Malformados | Salida | MB |")
    L.append("|---|---:|---:|---:|---|---:|")
    for r in resultados:
        L.append("| {} | {:,} | {:,} | {:,} | `{}` | {} |".format(
            r["anio"], r["utiles"], r["relleno"], r["malformados"],
            r["destino"], r["mb"]))

    L.append("")
    L.append("## Tratamiento de importes sin valor")
    L.append("")
    L.append("Los ejercicios 2020 y 2021 dejan celdas de importe en blanco donde los "
             "demas escriben cero. En 2020 el vacio aparece en los dos formatos "
             "publicados, de modo que es caracteristica del dato de origen y no del "
             "proceso de exportacion.")
    L.append("")
    L.append("**Decision:** el vacio se interpreta como cero. Las sumas por etapa "
             "coinciden con esa lectura y permite declarar las medidas como NOT NULL.")
    L.append("")
    L.append("| Ejercicio | Celdas vacias convertidas a cero | Valores no numericos |")
    L.append("|---|---:|---:|")
    for r in resultados:
        L.append("| {} | {:,} | {:,} |".format(r["anio"], r["vacios"], r["no_numericos"]))

    L.append("")
    L.append("## Correcciones aplicadas sobre descripciones")
    L.append("")
    hubo = False
    L.append("| Ejercicio | Valor publicado | Corregido a | Renglones |")
    L.append("|---|---|---|---:|")
    for r in resultados:
        for mal, n in sorted(r["correcciones"].items()):
            hubo = True
            bien = ""
            for col, arreglos in CORRECCIONES.items():
                if mal in arreglos:
                    bien = arreglos[mal]
            L.append("| {} | `{}` | `{}` | {:,} |".format(r["anio"], mal, bien, n))
    if not hubo:
        L.append("| — | ninguna | — | 0 |")
        L.append("")
        L.append("El error tipografico `Desarrollo SoSocial` detectado en 2024 aparece "
                 "unicamente en el csv publicado. Al cargar desde xlsx no se presenta, "
                 "y la correccion queda declarada por si la fuente cambia.")

    L.append("")
    L.append("## Totales por medida despues de normalizar (millones de pesos)")
    L.append("")
    L.append("| Ejercicio | " + " | ".join(m.capitalize() for m in MEDIDAS) + " |")
    L.append("|---" * (len(MEDIDAS) + 1) + "|")
    for r in resultados:
        vals = ["{:,.1f}".format(r["sumas"][m] / 1000000) for m in MEDIDAS]
        L.append("| " + r["anio"] + " | " + " | ".join(vals) + " |")

    L.append("")
    L.append("## Nomenclatura de origen por ejercicio")
    L.append("")
    L.append("| Ejercicio | Primeras columnas tal como se publican |")
    L.append("|---|---|")
    for r in resultados:
        L.append("| {} | {} |".format(
            r["anio"], ", ".join("`" + h + "`" for h in r["encabezado_origen"][:8])))

    return "\n".join(L) + "\n"


def main():
    resultados = []
    for anio, (archivo, formato) in FUENTES.items():
        ruta = CRUDO / archivo
        if not ruta.exists():
            print("FALTA " + archivo + " - se omite " + anio, flush=True)
            continue
        print("normalizando " + anio + " desde " + formato + " ...", flush=True)
        r = normalizar(anio, archivo, formato)
        print("   {:,} renglones -> {}".format(r["utiles"], r["destino"]), flush=True)
        resultados.append(r)

    BITACORA.parent.mkdir(parents=True, exist_ok=True)
    BITACORA.write_text(bitacora(resultados), encoding="utf-8")
    print("")
    print("bitacora escrita en " + str(BITACORA.relative_to(RAIZ)))


if __name__ == "__main__":
    main()
