#!/usr/bin/env python3
"""Genera un archivo de pronóstico de ejemplo con valores SINTÉTICOS (no usa datos del SIVIGILA).

Uso: python scripts/generar_ejemplo.py [equipo] [modelo]
"""
import csv, datetime as dt, json, math, random, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CFG = json.loads((RAIZ / "hub-config/tasks.json").read_text(encoding="utf-8"))
equipo = sys.argv[1] if len(sys.argv) > 1 else "epihub"
modelo = sys.argv[2] if len(sys.argv) > 2 else "ingenuo"
with open(RAIZ / CFG["entidades"], encoding="utf-8") as f:
    entidades = [r["location"] for r in csv.DictReader(f)]
ref = dt.date.fromisoformat(CFG["reference_date"])
z = lambda p: math.sqrt(2) * _erfinv(2 * p - 1)

def _erfinv(y):
    a = 0.147
    l = math.log(1 - y * y)
    t = 2 / (math.pi * a) + l / 2
    return math.copysign(math.sqrt(math.sqrt(t * t - l / a) - t), y)

random.seed(2026)
salida = RAIZ / "model-output" / f"{equipo}-{modelo}" / f"{CFG['reference_date']}-{equipo}-{modelo}.csv"
salida.parent.mkdir(parents=True, exist_ok=True)
with open(salida, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(CFG["columnas"])
    for loc in entidades:
        base = random.uniform(5, 400)          # nivel sintético
        for h in CFG["horizon"]:
            sd = 0.25 + 0.04 * h               # más incertidumbre a mayor horizonte
            for q in CFG["output_type_id"]:
                v = base * math.exp(sd * z(q))
                w.writerow([CFG["reference_date"], CFG["target"], h, loc,
                            (ref + dt.timedelta(weeks=h)).isoformat(), "quantile", q, round(v, 2)])
meta = RAIZ / "model-metadata" / f"{equipo}-{modelo}.yml"
if not meta.exists():
    meta.write_text(f"team_abbr: {equipo}\nmodel_abbr: {modelo}\nmodel_name: {equipo} {modelo}\n"
                    "designated_model: false\nmethods: Ejemplo sintético.\nlicense: CC-BY-4.0\n", encoding="utf-8")
print(f"Escrito {salida.relative_to(RAIZ)}")
