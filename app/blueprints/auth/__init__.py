from flask import Blueprint

auth_bp = Blueprint(
    "auth", 
    __name__, 
    template_folder="templates/auth"
)

# Importamos las rutas para que se registren
from . import routes
