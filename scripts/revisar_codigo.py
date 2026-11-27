#!/usr/bin/env python3
"""Revisión básica de seguridad del código de los equipos (antesala del Agente revisor IA y de semgrep).

Bloquea llamadas de red y ejecución de comandos del sistema en R y Python.
Uso: python scripts/revisar_codigo.py [carpeta_o_archivo ...]   (por omisión, todo codigo/)
"""
import os, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REGLAS = [
    (r"\b(download\.file|url\s*\(|httr::|curl::|RCurl|GET\s*\(|POST\s*\()", "llamada de red en R"),
    (r"\b(system2?|shell)\s*\(", "ejecución de comandos del sistema en R"),
    (r"\b(requests\.|urllib|http\.client|socket\.|httpx)", "llamada de red en Python"),
    (r"\b(os\.system|subprocess\.|os\.popen)", "ejecución de comandos del sistema en Python"),
    (r"\beval\s*\(\s*parse|exec\s*\(", "ejecución de código dinámico"),
    (r"(Sys\.getenv|os\.environ).*(TOKEN|KEY|SECRET|PASSWORD)", "lectura de secretos del entorno"),
]

def revisar(rutas):
    hallazgos = []
    for base in rutas:
        base = Path(base)
        archivos = [base] if base.is_file() else [p for p in base.rglob("*") if p.suffix.lower() in (".r", ".py", ".rmd", ".qmd")]
        for a in archivos:
            for n, linea in enumerate(a.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if linea.strip().startswith("#"):
                    continue
                for patron, motivo in REGLAS:
                    if re.search(patron, linea):
                        hallazgos.append((a.relative_to(RAIZ) if a.is_relative_to(RAIZ) else a, n, motivo, linea.strip()))
    return hallazgos

def main(argv):
    rutas = [RAIZ / a for a in argv] if argv else [RAIZ / "codigo"]
    h = revisar([r for r in rutas if r.exists()])
    if not h:
        print("✓ Revisión de seguridad: sin hallazgos"); return 0
    print(f"✗ Revisión de seguridad: {len(h)} hallazgo(s) bloqueante(s)")
    for archivo, n, motivo, linea in h:
        print(f"   - {archivo}:{n}: {motivo} -> {linea[:90]}")
        if os.getenv("GITHUB_ACTIONS"):
            print(f"::error file={archivo},line={n}::{motivo}")
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
