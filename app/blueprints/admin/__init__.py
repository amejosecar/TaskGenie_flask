# app/blueprints/admin/__init__.py
from flask import Blueprint

admin_bp = Blueprint(
    "admin",
    __name__,
    template_folder="templates"   # <-- antes era "templates/admin"
)

from . import routes
