#!/usr/bin/env python3
import os
from datetime import datetime

# create_structure.py

# Lista de rutas de los archivos a incluir
paths_to_process = [
    r"C:\americo\API\TaskGenie_flask\.env",
    r"C:\americo\API\TaskGenie_flask\.flaskenv",
    r"C:\americo\API\TaskGenie_flask\.gitignore",
    r"C:\americo\API\TaskGenie_flask\README.md",
    r"C:\americo\API\TaskGenie_flask\requirements.txt",
    r"C:\americo\API\TaskGenie_flask\run.py",
    r"C:\americo\API\TaskGenie_flask\app\config.py",
    r"C:\americo\API\TaskGenie_flask\app\extensions.py",
    r"C:\americo\API\TaskGenie_flask\app\models.py",
    r"C:\americo\API\TaskGenie_flask\app\__init__.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\admin\routes.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\admin\__init__.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\admin\templates\admin\dashboard_admin.html",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\auth\forms.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\auth\routes.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\auth\__init__.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\auth\templates\auth\login.html",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\auth\templates\auth\register.html",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\perfil\routes.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\perfil\__init__.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\perfil\templates\perfil\perfil.html",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\tareas\routes.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\tareas\__init__.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\tareas\templates\tareas\detalle.html",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\tareas\templates\tareas\form.html",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\tareas\templates\tareas\listado.html",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\usuarios\routes.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\usuarios\__init__.py",
    r"C:\americo\API\TaskGenie_flask\app\blueprints\usuarios\templates\usuarios\index.html",
    r"C:\americo\API\TaskGenie_flask\app\services\auth_service.py",
    r"C:\americo\API\TaskGenie_flask\app\services\memory_repo.py",
    r"C:\americo\API\TaskGenie_flask\app\templates\base.html",
    r"C:\americo\API\TaskGenie_flask\app\templates\dashboard.html",
    r"C:\americo\API\TaskGenie_flask\app\templates\errores.html",
    r"C:\americo\API\TaskGenie_flask\app\static\css\styles.css",
    r"C:\americo\API\TaskGenie_flask\migrations\versions\2230a4161079_añade_relación_usuario_tarea_y_user_id.py",
    r"C:\americo\API\TaskGenie_flask\migrations\env.py",
    r"C:\americo\API\TaskGenie_flask\migrations\script.py.mako",
    r"C:\americo\API\TaskGenie_flask\migrations\alembic.ini",
]

def write_files_to_txt(file_paths, output_file):
    """
    Escribe la fecha/hora de creación en la primera línea
    y luego vuelca cada archivo con separadores.
    """
    # 1) Cabecera con fecha y hora actuales
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(output_file, "w", encoding="utf8") as outf:
        outf.write(f"Creado el {now_str}\n\n")

        # 2) Contenido de cada archivo
        for file_path in file_paths:
            outf.write("-" * 40 + "\n")
            outf.write(f"# {file_path}\n")
            try:
                with open(file_path, "r", encoding="utf8") as f:
                    outf.write(f.read())
            except Exception as e:
                outf.write(f"# Error al leer este archivo: {e}\n")
            outf.write("\n")

    print(f"Se han copiado {len(file_paths)} archivos a '{output_file}'.")

if __name__ == "__main__":
    # 1) Eliminar versión previa si existe
    target = r"C:\americo\API\TaskGenie_flask\utilitis\a-TaskGenie_flask.txt"
    if os.path.exists(target):
        print("Archivo existente encontrado, eliminando...")
        try:
            os.remove(target)
            print("Archivo eliminado.")
        except Exception as e:
            print(f"No se pudo eliminar el archivo: {e}")
    else:
        print("No se encontró archivo anterior, continuando.")

    # 2) Generar nuevo TXT
    output_file = "a-TaskGenie_flask.txt"
    write_files_to_txt(paths_to_process, output_file)

    # 3) Mensaje final
    print("Código ejecutado con éxito.")
