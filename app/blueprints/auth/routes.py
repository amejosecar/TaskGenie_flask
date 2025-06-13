from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.services.memory_repo import MemoryDB
from app.services.auth_service import registrar_usuario, autenticar_usuario
from . import auth_bp
from .forms import RegisterForm, LoginForm

# Instancia global del stub en memoria
db = MemoryDB()

@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for("tareas.listado"))

    form = RegisterForm()
    if form.validate_on_submit():
        try:
            u = registrar_usuario(
                db,
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                edad=form.edad.data,
                email=form.email.data,
                clave=form.clave.data,
                fecha_nacimiento=form.fecha_nacimiento.data.strftime("%Y-%m-%d"),
                rol=form.rol.data
            )
            flash(f"Usuario {u.email} registrado correctamente", "success")
            return redirect(url_for("auth.login"))
        except ValueError as e:
            flash(str(e), "danger")

    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("tareas.listado"))

    form = LoginForm()
    if form.validate_on_submit():
        user = autenticar_usuario(db, email=form.email.data, clave=form.clave.data)
        if user:
            login_user(user)
            flash("Has iniciado sesión correctamente", "success")
            next_page = request.args.get("next") or url_for("tareas.listado")
            return redirect(next_page)
        flash("Email o contraseña incorrectos", "danger")

    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión", "info")
    return redirect(url_for("auth.login"))
