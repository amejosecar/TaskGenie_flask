# lisatdo_contenido.py
import os
from pathlib import Path

# ————— CONFIGURACIÓN —————
ROOT_DIR = Path(r"C:\americo\API\TaskGenie_flask").resolve()
OUTPUT   = ROOT_DIR / "utilitis" / "listado_contenido.txt"

IGNORE_DIRS = {"__pycache__", "utilitis", "venv"}

ALLOWED_ROOT = {"app", "migrations"}

ALLOWED_APP = {"blueprints", "services", "templates", "version"}

def listar_contenido():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as out:
        for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
            rel   = Path(dirpath).relative_to(ROOT_DIR)
            parts = rel.parts

            # Ignorar carpetas no deseadas en cualquier parte del árbol
            if any(p in IGNORE_DIRS for p in parts):
                continue

            # Nivel raíz: permitimos carpetas específicas y también listamos archivos directamente ahí
            if len(parts) == 0:
                dirnames[:] = [d for d in dirnames if d in ALLOWED_ROOT]
                for fname in filenames:
                    full = Path(dirpath) / fname
                    out.write(f'r"{full}",\n')
                continue

            # app/ y subdirectorios válidos
            if parts[0] == "app":
                if len(parts) == 1:
                    dirnames[:] = [d for d in dirnames if d in ALLOWED_APP]
                else:
                    dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

            # migrations/ se incluye completamente
            elif parts[0] == "migrations":
                dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

            else:
                continue

            for fname in filenames:
                full = Path(dirpath) / fname
                out.write(f'r"{full}",\n')


if __name__ == "__main__":
    listar_contenido()
