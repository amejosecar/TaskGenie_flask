#!/usr/bin/env python3
"""
create_estructura.py

Este script crea la estructura de carpetas y archivos vacíos para el proyecto
TaskGenie_flask. Debe ubicarse en:
    C:/americo/API/TaskGenie_flask/utilities/create_estructura.py

Al ejecutarlo, generará todo el árbol en:
    C:/americo/API/TaskGenie_flask/
"""

from pathlib import Path

def main():
    # Directorio base: dos niveles arriba de este script
    base_dir = Path(__file__).resolve().parent.parent

    # Lista de carpetas a crear (relativas a base_dir)
    carpetas = [
        "instance",
        "app",
        "app/services",
        "app/blueprints/auth",
        "app/blueprints/auth/templates/auth",
        "app/blueprints/admin",
        "app/blueprints/admin/templates/admin",
        "app/blueprints/perfil",
        "app/blueprints/perfil/templates/perfil",
        "app/blueprints/tareas",
        "app/blueprints/tareas/templates/tareas",
        "app/blueprints/usuarios",
        "app/blueprints/usuarios/templates/usuarios",
        "app/templates",
        "app/static",
    ]

    # Lista de archivos a crear (relativos a base_dir)
    archivos = [
        ".env",
        ".gitignore",
        "requirements.txt",
        "run.py",
        "app/__init__.py",
        "app/config.py",
        "app/extensions.py",
        "app/services/auth_service.py",
        "app/models.py",
        "app/blueprints/auth/__init__.py",
        "app/blueprints/auth/routes.py",
        "app/blueprints/auth/forms.py",
        "app/blueprints/admin/__init__.py",
        "app/blueprints/admin/routes.py",
        "app/blueprints/perfil/__init__.py",
        "app/blueprints/perfil/routes.py",
        "app/blueprints/tareas/__init__.py",
        "app/blueprints/tareas/routes.py",
        "app/blueprints/usuarios/__init__.py",
        "app/blueprints/usuarios/routes.py",
        "app/templates/base.html",
        "app/templates/dashboard.html",
        "app/templates/errores.html",
        "instance/taskgenie.db",
    ]

    # Creación de carpetas
    for carpeta in carpetas:
        path = base_dir / carpeta
        path.mkdir(parents=True, exist_ok=True)
        print(f"Carpeta creada: {path}")

    # Creación de archivos vacíos
    for archivo in archivos:
        path = base_dir / archivo
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.touch()
            print(f"Archivo creado: {path}")
        else:
            print(f"Archivo ya existe: {path}")

if __name__ == "__main__":
    main()
