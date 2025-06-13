from flask import Blueprint

perfil_bp = Blueprint(
    "perfil",
    __name__,
    template_folder="templates/perfil"
)

# Importa las rutas para que Flask las registre
from . import routes
