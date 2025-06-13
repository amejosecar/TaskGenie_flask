#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path

# ————— CONFIGURACIÓN —————
ROOT_DIR = Path(r"C:\americo\API\TaskGenie_flask").resolve()
OUTPUT  = ROOT_DIR / "utilitis" / "listado_contenido.txt"

# Directorios que nunca queremos entrar
IGNORE_DIRS = {"__pycache__", "utilitis", "venv"}

# En la raíz solo descendemos a "app"
ALLOWED_ROOT = {"app"}

# Dentro de "app" solo a estos submódulos
ALLOWED_APP = {"blueprints", "services", "templates"}


def listar_contenido():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as out:
        for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
            rel   = Path(dirpath).relative_to(ROOT_DIR)
            parts = rel.parts  # () en la raíz, ("app",), ("app","blueprints"),...

            # 1) Si aparece un directorio ignorado en la ruta, saltamos todo el árbol
            if any(p in IGNORE_DIRS for p in parts):
                continue

            # 2) Filtrado de carpetas según nivel
            if len(parts) == 0:
                dirnames[:] = [d for d in dirnames if d in ALLOWED_ROOT]
            elif parts[0] == "app" and len(parts) == 1:
                dirnames[:] = [d for d in dirnames if d in ALLOWED_APP]
            elif parts[0] == "app" and parts[1] in ALLOWED_APP:
                dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
            else:
                continue

            # 3) Listamos todos los archivos que queden
            for fname in filenames:
                full = Path(dirpath) / fname
                # Escribimos cada ruta en formato: r"<ruta_completa>",
                out.write(f'r"{full}",\n')


if __name__ == "__main__":
    listar_contenido()
