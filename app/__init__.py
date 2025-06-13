# app/__init__.py
# 🍺 Application Factory: define create_app()

from flask import Flask, render_template
from .config import Config
from .extensions import db, csrf, login_manager

# Importa tus Blueprints
from .blueprints.auth import auth_bp
from .blueprints.admin import admin_bp
from .blueprints.perfil import perfil_bp
from .blueprints.tareas import tareas_bp
from .blueprints.usuarios import usuarios_bp

def create_app():
    # 1. Crea la app y carga configuración
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # 2. Inicializa extensiones
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # 3. Registra Blueprints
    app.register_blueprint(auth_bp,     url_prefix="")        # login / registro
    app.register_blueprint(admin_bp,    url_prefix="/admin")  # panel admin
    app.register_blueprint(perfil_bp,   url_prefix="/perfil") # perfil usuario
    app.register_blueprint(tareas_bp,   url_prefix="/tareas") # gestión de tareas
    app.register_blueprint(usuarios_bp, url_prefix="/u")      # API usuarios

    # 4. Crea tablas SQLite en instance/taskgenie.db y semillas de prueba
    with app.app_context():
        db.create_all()

        # Poblado inicial: tres usuarios de prueba
        from .models import Usuario, RolEnum
        from werkzeug.security import generate_password_hash
        from datetime import date

        if not Usuario.query.first():
            inicial = [
                {
                    "nombre": "Americo-admin",
                    "apellido": "carrillo",
                    "email": "amejosecar@keko.com",
                    "clave": "333333",
                    "fecha_nacimiento": "1970-12-18",
                    "rol": RolEnum.ADMIN
                },
                {
                    "nombre": "Americo-profe",
                    "apellido": "carrillo",
                    "email": "amejosecar@profe.com",
                    "clave": "333333",
                    "fecha_nacimiento": "1970-12-18",
                    "rol": RolEnum.PROFESOR
                },
                {
                    "nombre": "Americo-Alum",
                    "apellido": "carrillo",
                    "email": "amejosecar@alumno.com",
                    "clave": "333333",
                    "fecha_nacimiento": "1970-12-18",
                    "rol": RolEnum.ALUMNO
                },
            ]
            for u in inicial:
                usuario = Usuario(
                    nombre=u["nombre"],
                    apellido=u["apellido"],
                    email=u["email"],
                    clave_hash=generate_password_hash(u["clave"]),
                    fecha_nacimiento=date.fromisoformat(u["fecha_nacimiento"]),
                    rol=u["rol"]
                )
                db.session.add(usuario)
            db.session.commit()

    # 5. Manejador genérico de 404
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errores.html", mensaje="Página no encontrada"), 404

    return app
