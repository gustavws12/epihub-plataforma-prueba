"""Modelo de ejemplo del equipo andes: pronóstico SINTÉTICO (no usa datos del SIVIGILA)."""
import csv, datetime as dt, json, math, random
from pathlib import Path

REF = dt.date(2026, 11, 14)
CUANTILES = [0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975, 0.99]
HORIZONTES = range(1, 13)
ENTIDADES = ['05', '08', '11', '13', '15', '17', '18', '19', '20', '23', '25', '27', '41', '44', '47', '50', '52', '54', '63', '66', '68', '70', '73', '76', '81', '85', '86', '88', '91', '94', '95', '97', '99', '08001', '13001', '47001', '76001', '76109']

def erfinv(y):
    a = 0.147; l = math.log(1 - y * y); t = 2 / (math.pi * a) + l / 2
    return math.copysign(math.sqrt(math.sqrt(t * t - l / a) - t), y)

random.seed(101)
salida = Path(__file__).resolve().parents[2] / "model-output" / "andes-sarimax" / "2026-11-14-andes-sarimax.csv"
salida.parent.mkdir(parents=True, exist_ok=True)
with open(salida, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["reference_date","target","horizon","location","target_end_date","output_type","output_type_id","value"])
    for loc in ENTIDADES:
        base = random.uniform(5, 400)
        for h in HORIZONTES:
            sd = 0.2 + 0.04 * h
            for q in CUANTILES:
                v = base * math.exp(sd * math.sqrt(2) * erfinv(2 * q - 1))
                w.writerow([REF.isoformat(), "case dengue", h, loc, (REF + dt.timedelta(weeks=h)).isoformat(), "quantile", q, round(v, 2)])
print("Escrito", salida)
