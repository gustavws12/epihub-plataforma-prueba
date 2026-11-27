#!/usr/bin/env python3
"""Valida archivos de pronóstico del EpiModelling Hub (formato hubverse, Anexo A).

Uso:
    python scripts/validar_envio.py model-output/equipo-modelo/2026-11-14-equipo-modelo.csv [...]
    python scripts/validar_envio.py --todos        # valida todo model-output/

Solo usa la biblioteca estándar de Python, para correr igual en Windows, Linux y GitHub Actions.
Sale con código 1 si algún archivo tiene errores.
"""
import csv
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CFG = json.loads((RAIZ / "hub-config" / "tasks.json").read_text(encoding="utf-8"))
with open(RAIZ / CFG["entidades"], encoding="utf-8") as f:
    ENTIDADES = {r["location"] for r in csv.DictReader(f)}
COLUMNAS = CFG["columnas"]
HORIZONTES = set(CFG["horizon"])
CUANTILES = [float(q) for q in CFG["output_type_id"]]
REF = dt.date.fromisoformat(CFG["reference_date"])
PATRON = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z0-9]+)-([a-z0-9_]+)\.csv$")
MAX_ERRORES = 25


def validar(ruta: Path) -> list[str]:
    errores: list[str] = []

    def error(msg):
        if len(errores) < MAX_ERRORES:
            errores.append(msg)

    m = PATRON.match(ruta.name)
    if not m:
        return [f"Nombre de archivo inválido: debe ser AAAA-MM-DD-equipo-modelo.csv (recibido {ruta.name})"]
    fecha_nombre, equipo, modelo = m.groups()
    if ruta.parent.name != f"{equipo}-{modelo}":
        error(f"La carpeta debe llamarse {equipo}-{modelo} (está en {ruta.parent.name})")
    if fecha_nombre != CFG["reference_date"]:
        error(f"La fecha del nombre ({fecha_nombre}) no es la reference_date de la ronda ({CFG['reference_date']})")
    meta = RAIZ / "model-metadata" / f"{equipo}-{modelo}.yml"
    if not meta.exists():
        error(f"Falta el archivo de metadatos model-metadata/{equipo}-{modelo}.yml")

    with open(ruta, encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        if lector.fieldnames != COLUMNAS:
            return errores + [f"Columnas esperadas {COLUMNAS}, recibidas {lector.fieldnames}"]
        filas = list(lector)

    vistos = set()
    por_grupo = defaultdict(dict)
    for i, r in enumerate(filas, start=2):
        if r["reference_date"] != CFG["reference_date"]:
            error(f"Fila {i}: reference_date {r['reference_date']} distinta de {CFG['reference_date']}")
        if r["target"] != CFG["target"]:
            error(f"Fila {i}: target '{r['target']}' distinto de '{CFG['target']}'")
        if r["output_type"] != CFG["output_type"]:
            error(f"Fila {i}: output_type '{r['output_type']}' distinto de '{CFG['output_type']}'")
        if r["location"] not in ENTIDADES:
            error(f"Fila {i}: location '{r['location']}' no está entre las 38 entidades (¿perdió el cero inicial?)")
        try:
            h = int(r["horizon"])
        except ValueError:
            error(f"Fila {i}: horizon '{r['horizon']}' no es entero"); continue
        if h not in HORIZONTES:
            error(f"Fila {i}: horizon {h} fuera de 1 a {max(HORIZONTES)}")
        esperado = (REF + dt.timedelta(weeks=h)).isoformat()
        if r["target_end_date"] != esperado:
            error(f"Fila {i}: target_end_date {r['target_end_date']} debería ser {esperado} para horizon {h}")
        try:
            q = float(r["output_type_id"])
        except ValueError:
            error(f"Fila {i}: output_type_id '{r['output_type_id']}' no es numérico"); continue
        if not any(abs(q - c) < 1e-9 for c in CUANTILES):
            error(f"Fila {i}: cuantil {q} no está en la lista de 23 cuantiles")
        try:
            v = float(r["value"])
        except ValueError:
            error(f"Fila {i}: value '{r['value']}' no es numérico"); continue
        if v < 0:
            error(f"Fila {i}: value negativo ({v})")
        clave = (r["location"], h, round(q, 6))
        if clave in vistos:
            error(f"Fila {i}: fila duplicada para location {r['location']}, horizon {h}, cuantil {q}")
        vistos.add(clave)
        por_grupo[(r["location"], h)][round(q, 6)] = v

    esperadas = len(ENTIDADES) * len(HORIZONTES) * len(CUANTILES)
    if len(filas) != esperadas:
        error(f"El archivo tiene {len(filas)} filas; se esperan {esperadas} "
              f"({len(ENTIDADES)} entidades × {len(HORIZONTES)} horizontes × {len(CUANTILES)} cuantiles)")
    for (loc, h), valores in sorted(por_grupo.items()):
        orden = [valores[q] for q in sorted(valores)]
        if any(b < a for a, b in zip(orden, orden[1:])):
            error(f"location {loc}, horizon {h}: los valores no crecen con el cuantil")
    return errores


def main(argv):
    if "--todos" in argv or not argv:
        rutas = sorted((RAIZ / "model-output").glob("*/*.csv"))
    else:
        rutas = [Path(a).resolve() for a in argv if a.endswith(".csv")]
    if not rutas:
        print("No hay archivos para validar."); return 0
    resumen = ["## Validación de envíos", "", "| Archivo | Resultado |", "| --- | --- |"]
    falla = False
    for ruta in rutas:
        errs = validar(ruta)
        nombre = ruta.relative_to(RAIZ) if ruta.is_relative_to(RAIZ) else ruta
        if errs:
            falla = True
            print(f"\n✗ {nombre}: {len(errs)} error(es)")
            for e in errs:
                print(f"   - {e}")
                if os.getenv("GITHUB_ACTIONS"):
                    print(f"::error file={nombre}::{e}")
            resumen.append(f"| `{nombre}` | ✗ {len(errs)} error(es): {errs[0]} |")
        else:
            print(f"✓ {nombre}: válido")
            resumen.append(f"| `{nombre}` | ✓ válido |")
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write("\n".join(resumen) + "\n")
    return 1 if falla else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
