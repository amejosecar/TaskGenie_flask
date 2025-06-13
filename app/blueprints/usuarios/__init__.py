from flask import Blueprint

usuarios_bp = Blueprint(
    "usuarios",
    __name__,
    url_prefix="/u",
    template_folder="templates/usuarios"
)

# Importa las rutas automáticamente
from . import routes
