# app/blueprints/tareas/routes.py
# app/blueprints/tareas/routes.py
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Tarea
from . import tareas_bp

@tareas_bp.route("/", methods=["GET"])
@login_required
def listado():
    tareas = Tarea.query.filter_by(user_id=current_user.id).all()
    return render_template("tareas/listado.html", tareas=tareas)

@tareas_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        tarea = Tarea(titulo=titulo, descripcion=descripcion, user_id=current_user.id)
        db.session.add(tarea)
        db.session.commit()
        flash("Tarea creada con éxito", "success")
        return redirect(url_for("tareas.listado"))
    return render_template("tareas/form.html", accion="Nueva Tarea", tarea=None)

def _get_own_task_or_404(tarea_id):
    tarea = Tarea.query.get(tarea_id)
    if not tarea or tarea.user_id != current_user.id:
        abort(404)
    return tarea

@tareas_bp.route("/<int:tarea_id>/editar", methods=["GET", "POST"])
@login_required
def editar(tarea_id):
    tarea = _get_own_task_or_404(tarea_id)
    if request.method == "POST":
        tarea.titulo      = request.form.get("titulo", "").strip()
        tarea.descripcion = request.form.get("descripcion", "").strip()
        tarea.completada  = "completada" in request.form
        db.session.commit()
        flash("Tarea actualizada", "success")
        return redirect(url_for("tareas.listado"))
    return render_template("tareas/form.html", accion="Editar Tarea", tarea=tarea)

@tareas_bp.route("/<int:tarea_id>/ver", methods=["GET"])
@login_required
def detalle(tarea_id):
    tarea = _get_own_task_or_404(tarea_id)
    return render_template("tareas/detalle.html", tarea=tarea)

@tareas_bp.route("/<int:tarea_id>/eliminar", methods=["POST"])
@login_required
def eliminar(tarea_id):
    tarea = _get_own_task_or_404(tarea_id)
    db.session.delete(tarea)
    db.session.commit()
    flash("Tarea eliminada", "info")
    return redirect(url_for("tareas.listado"))
