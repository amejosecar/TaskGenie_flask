# app/__init__.py
from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from .config import Config
from .extensions import db, csrf, login_manager

# Importa tus Blueprints
from .blueprints.auth import auth_bp
from .blueprints.admin import admin_bp
from .blueprints.perfil import perfil_bp
from .blueprints.tareas import tareas_bp
from .blueprints.usuarios import usuarios_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Inicializa extensiones
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Registra Blueprints
    app.register_blueprint(auth_bp,     url_prefix="")        # /login, /registro
    app.register_blueprint(admin_bp,    url_prefix="/admin")  # /admin/…
    app.register_blueprint(perfil_bp,   url_prefix="/perfil") # /perfil/…
    app.register_blueprint(tareas_bp,   url_prefix="/tareas") # /tareas/…
    app.register_blueprint(usuarios_bp, url_prefix="/u")      # /u/…

    # Crea BD y semilla
    with app.app_context():
        from .models import Usuario, RolEnum
        from werkzeug.security import generate_password_hash
        from datetime import date

        db.create_all()

        if not Usuario.query.first():
            inicial = [
                ("Americo-admin",  "carrillo", "amejosecar@keko.com",   "333333", "1970-12-18", RolEnum.ADMIN),
                ("Americo-profe",  "carrillo", "amejosecar@profe.com",  "333333", "1970-12-18", RolEnum.PROFESOR),
                ("Americo-Alum",   "carrillo", "amejosecar@alumno.com","333333", "1970-12-18", RolEnum.ALUMNO),
            ]
            for nombre,apellido,email,clave,fnac,rol in inicial:
                u = Usuario(
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    clave_hash=generate_password_hash(clave),
                    fecha_nacimiento=date.fromisoformat(fnac),
                    rol=rol
                )
                db.session.add(u)
            db.session.commit()

    # Ruta raíz: home → login o dashboard
    @app.route("/")
    def home():
        if current_user.is_authenticated:
        # Admin va siempre a su panel
            if current_user.rol.name == "ADMIN":
                return redirect(url_for("admin.dashboard"))
        # Profesores/Alumnos al listado de tareas
            return redirect(url_for("tareas.listado"))
        return redirect(url_for("auth.login"))


    # Manejador 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errores.html", mensaje="Página no encontrada"), 404

    return app
