# listado_contenido.py

"""
Este script recorre recursivamente todos los archivos ubicados dentro de la carpeta raíz del proyecto
e imprime en un archivo de texto la ruta completa de cada archivo encontrado.

Exclusiones:
- Se omiten por completo las siguientes carpetas (y su contenido): 
  'respaldo', 'utilitis', 'venv', '__pycache__', '.git', y '.vscode'.

Salida:
- Se guarda en: '<raíz_del_proyecto>\\utilitis\\listado_contenido.txt'
- Si el archivo ya existe, se elimina antes de generar uno nuevo.
- Al finalizar, se muestra en consola la cantidad total de archivos listados y el tiempo empleado.
"""

import os
import time
from pathlib import Path

# ————— CONFIGURACIÓN AUTOMÁTICA —————
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR   = SCRIPT_DIR.parent  # Asumiendo que el script está en /utilitis
OUTPUT     = ROOT_DIR / "utilitis" / "listado_contenido.txt"
IGNORED_DIRS = {"respaldo", "utilitis", "venv", "__pycache__", ".git", ".vscode"}

def listar_contenido():
    start_time = time.time()

    if OUTPUT.exists():
        print(f"[ℹ] Archivo existente encontrado: {OUTPUT}")
        try:
            OUTPUT.unlink()
            print("[✘] Archivo anterior eliminado.")
        except Exception as e:
            print(f"[⚠] No se pudo eliminar el archivo existente: {e}")
    else:
        print("[ℹ] Archivo anterior no encontrado. Se creará uno nuevo.")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    contador = 0

    with OUTPUT.open("w", encoding="utf-8") as out:
        for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
            current_path = Path(dirpath).resolve()

            dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS]

            if any(part in IGNORED_DIRS for part in current_path.parts):
                continue

            for fname in filenames:
                file_path = current_path / fname
                out.write(f'r"{file_path}",\n')
                contador += 1

    elapsed = time.time() - start_time
    print(f"\n[✔] Se han listado {contador} archivos en: {OUTPUT}")
    print(f"[⏱️] Tiempo total: {elapsed:.2f} segundos")

if __name__ == "__main__":
    listar_contenido()
