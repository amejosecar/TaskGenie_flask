#app/__init__.py
import sys

from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from .config import Config
from .extensions import db, csrf, login_manager, migrate
from .models import RolEnum

# Blueprints
from .blueprints.auth import auth_bp
from .blueprints.admin import admin_bp
from .blueprints.perfil import perfil_bp
from .blueprints.tareas import tareas_bp
from .blueprints.usuarios import usuarios_bp
from .blueprints.profe import profe_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Inicializa extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Registra Blueprints
    app.register_blueprint(auth_bp,     url_prefix="")
    app.register_blueprint(admin_bp,    url_prefix="/admin")
    app.register_blueprint(perfil_bp,   url_prefix="/perfil")
    app.register_blueprint(tareas_bp,   url_prefix="/tareas")
    app.register_blueprint(usuarios_bp, url_prefix="/u")
    app.register_blueprint(profe_bp,    url_prefix="/profe") 

    # ——————————————————————————————
    # IMPORTANTE: eliminamos el bloque de create_all() y seeds
    # para que Alembic sea el único responsable de crear el esquema
    # Nunca ejecutar db.create_all() aquí si usamos migraciones
    # ——————————————————————————————

    @app.route("/")
    def home():
        if current_user.is_authenticated:
            if current_user.rol == RolEnum.ADMIN:
                return redirect(url_for("admin.dashboard"))
            elif current_user.rol == RolEnum.PROFESOR:
                return redirect(url_for("profe.listado"))
            else:
                return redirect(url_for("tareas.listado"))
        return redirect(url_for("auth.login"))

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errores.html", mensaje="Página no encontrada"), 404

    return app
