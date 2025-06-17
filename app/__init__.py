# app/__init__.py

from flask import Flask, render_template, redirect, url_for
from flask_login import current_user
from .config import Config
from .extensions import db, csrf, login_manager, migrate

# Importa blueprints
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
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Registra Blueprints
    app.register_blueprint(auth_bp,     url_prefix="")
    app.register_blueprint(admin_bp,    url_prefix="/admin")
    app.register_blueprint(perfil_bp,   url_prefix="/perfil")
    app.register_blueprint(tareas_bp,   url_prefix="/tareas")
    app.register_blueprint(usuarios_bp, url_prefix="/u")

    # Seed inicial
    with app.app_context():
        from .models import Usuario, RolEnum, Tarea, Importancia, EstadoTarea
        from werkzeug.security import generate_password_hash
        from datetime import date

        # Crea esquema de tablas si no existe
        db.create_all()

        # Seed de Usuarios
        if not Usuario.query.first():
            inicial = [
                ("Americo-admin",  "carrillo", "amejosecar@keko.com",    "333333", "1970-12-18", RolEnum.ADMIN),
                ("Americo-profe",  "carrillo", "amejosecar@profe.com",   "333333", "1970-12-18", RolEnum.PROFESOR),
                ("Americo-Alum",   "carrillo", "amejosecar@alumno.com",  "333333", "1970-12-18", RolEnum.ALUMNO),
            ]
            for nombre, apellido, email, clave, fnac, rol in inicial:
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

        # Seed de Importancia
        if not Importancia.query.first():
            datos_imp = [
                ("01", "alta",  "Muy importante"),
                ("02", "media", "Importante"),
                ("03", "baja",  "Normal"),
            ]
            for cod, tipo, desc in datos_imp:
                db.session.add(Importancia(
                    cod_id=cod,
                    tipo_importancia=tipo,
                    desc_importancia=desc
                ))
            db.session.commit()

        # Seed de EstadoTarea
        if not EstadoTarea.query.first():
            datos_est = [
                ("01", "asignada"),
                ("02", "completada"),
                ("03", "cancelada"),
            ]
            for cod, desc in datos_est:
                db.session.add(EstadoTarea(
                    cod_id=cod,
                    desc_estado_tarea=desc
                ))
            db.session.commit()

    @app.route("/")
    def home():
        if current_user.is_authenticated:
            if current_user.rol == Config.RolEnum.ADMIN:
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("tareas.listado"))
        return redirect(url_for("auth.login"))

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errores.html", mensaje="Página no encontrada"), 404

    return app
