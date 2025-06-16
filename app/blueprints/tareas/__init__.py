# app/blueprints/tareas/__init__.py
from flask import Blueprint

tareas_bp = Blueprint(
    "tareas",
    __name__,
    template_folder="templates"   # <-- antes era "templates/tareas"
)

from . import routes
