from flask import Blueprint

tareas_bp = Blueprint(
    "tareas",
    __name__,
    template_folder="templates/tareas"
)

# Importa las rutas para que Flask las registre
from . import routes
