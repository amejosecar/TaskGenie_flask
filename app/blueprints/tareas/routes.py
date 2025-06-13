from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.services.memory_repo import MemoryDB
from app.models import Tarea
from . import tareas_bp

# Stub en memoria (mismo que en auth)
db = MemoryDB()

@tareas_bp.route("/", methods=["GET"])
@login_required
def listado():
    tareas = db.query(Tarea).all()
    return render_template("tareas/listado.html", tareas=tareas)

@tareas_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descripcion = request.form.get("descripcion")
        tarea = Tarea(titulo=titulo, descripcion=descripcion, completada=False)
        db.add(tarea)
        db.commit()
        flash("Tarea creada con éxito", "success")
        return redirect(url_for("tareas.listado"))
    return render_template("tareas/form.html", accion="Nueva Tarea", tarea=None)

@tareas_bp.route("/<int:tarea_id>/editar", methods=["GET", "POST"])
@login_required
def editar(tarea_id):
    tarea = db.query(Tarea).filter_by(id=tarea_id).first()
    if not tarea:
        flash("Tarea no encontrada", "danger")
        return redirect(url_for("tareas.listado"))

    if request.method == "POST":
        tarea.titulo = request.form.get("titulo")
        tarea.descripcion = request.form.get("descripcion")
        tarea.completada = "completada" in request.form
        db.commit()
        flash("Tarea actualizada", "success")
        return redirect(url_for("tareas.listado"))

    return render_template("tareas/form.html", accion="Editar Tarea", tarea=tarea)

@tareas_bp.route("/<int:tarea_id>/ver", methods=["GET"])
@login_required
def detalle(tarea_id):
    tarea = db.query(Tarea).filter_by(id=tarea_id).first()
    if not tarea:
        flash("Tarea no encontrada", "danger")
        return redirect(url_for("tareas.listado"))
    return render_template("tareas/detalle.html", tarea=tarea)

@tareas_bp.route("/<int:tarea_id>/eliminar", methods=["POST"])
@login_required
def eliminar(tarea_id):
    tarea = db.query(Tarea).filter_by(id=tarea_id).first()
    if tarea:
        db._storage["Tarea"].remove(tarea)
        flash("Tarea eliminada", "info")
    return redirect(url_for("tareas.listado"))
