import os
import subprocess
import sys

def check_command(cmd):
    try:
        subprocess.run([cmd, "--version"], check=True)
        print(f"{cmd} está instalado correctamente.")
    except Exception:
        print(f"{cmd} no está instalado o no está en el PATH.")
        sys.exit(1)

def create_venv():
    if not os.path.exists("venv"):
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print("✅ Entorno virtual creado.")
    else:
        print("ℹ️ Ya existe un entorno virtual llamado 'venv'.")

def main():
    check_command("python")
    check_command("pip")
    create_venv()

if __name__ == "__main__":
    main()
