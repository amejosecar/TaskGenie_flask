# app/blueprints/profe/__init__.py

from flask import Blueprint

profe_bp = Blueprint(
    "profe",
    __name__,
    template_folder="templates/profe"
)

from . import routes
