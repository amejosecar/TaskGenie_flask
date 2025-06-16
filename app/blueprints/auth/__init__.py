#app/blueprints/auth/init.py
from flask import Blueprint

# Antes tenías:
# auth_bp = Blueprint(
#     "auth",
#     __name__,
#     template_folder="templates/auth"
# )

# Ahora indicamos que el directorio 'templates' (que a su vez
# contiene la carpeta 'auth') es la raíz de plantillas del BP:
auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates"
)

# Importa las rutas para que se registren
from . import routes
