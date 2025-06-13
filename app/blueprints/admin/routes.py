from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.memory_repo import MemoryDB
from app.models import Usuario, RolEnum
from . import admin_bp

# Instancia del stub
db = MemoryDB()

def solo_admin(fn):
    """Decorator para restringir acceso sólo a ADMIN."""
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or current_user.rol != RolEnum.ADMIN:
            flash("Acceso denegado", "danger")
            return redirect(url_for("auth.login"))
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return login_required(wrapper)

@admin_bp.route("/", methods=["GET"])
@solo_admin
def dashboard():
    users = db.query(Usuario).all()
    return render_template("admin/dashboard_admin.html", users=users)

@admin_bp.route("/user/<int:user_id>/change-role", methods=["POST"])
@solo_admin
def change_role(user_id):
    user = db.query(Usuario).filter_by(id=user_id).first()
    if user:
        user.rol = RolEnum.ADMIN if user.rol == RolEnum.USER else RolEnum.USER
        db.commit()
        flash(f"Rol de {user.email} cambiado a {user.rol.value}", "success")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/user/<int:user_id>/toggle-block", methods=["POST"])
@solo_admin
def toggle_block(user_id):
    user = db.query(Usuario).filter_by(id=user_id).first()
    if user:
        user.is_blocked = not getattr(user, "is_blocked", False)
        db.commit()
        estado = "bloqueado" if user.is_blocked else "desbloqueado"
        flash(f"Usuario {user.email} {estado}", "info")
    return redirect(url_for("admin.dashboard"))

@admin_bp.route("/user/<int:user_id>/delete", methods=["POST"])
@solo_admin
def delete_user(user_id):
    user = db.query(Usuario).filter_by(id=user_id).first()
    if user:
        db._storage["Usuario"].remove(user)
        flash(f"Usuario {user.email} eliminado", "warning")
    return redirect(url_for("admin.dashboard"))
