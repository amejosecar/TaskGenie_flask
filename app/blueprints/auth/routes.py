# app/blueprints/auth/routes.py

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from .forms import RegisterForm, LoginForm
from app.services.auth_service import registrar_usuario, autenticar_usuario
from app.models import RolEnum

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("tareas.listado"))

    form = RegisterForm()
    if form.validate_on_submit():
        try:
            # Convertimos el nombre de rol en RolEnum
            rol_enum = RolEnum[form.rol.data]
            u = registrar_usuario(
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                email=form.email.data,
                clave=form.clave.data,
                fecha_nacimiento=form.fecha_nacimiento.data.strftime("%Y-%m-%d"),
                rol=rol_enum
            )
            flash(f"Usuario {u.email} registrado correctamente", "success")
            return redirect(url_for("auth.login"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = autenticar_usuario(
            email=form.email.data,
            clave=form.clave.data
        )
        if not user:
            flash("Email o contraseña incorrectos", "danger")
            return render_template("auth/login.html", form=form)

        # Loguear usuario
        login_user(user)
        flash("Has iniciado sesión correctamente", "success")

        # Redirigir según rol
        if user.rol == RolEnum.ADMIN:
            return redirect(url_for("admin.dashboard"))
        elif user.rol == RolEnum.PROFESOR:
            return redirect(url_for("profe.listado"))
        else:
            return redirect(url_for("tareas.listado"))

    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión", "info")
    return redirect(url_for("auth.login"))
