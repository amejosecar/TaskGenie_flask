# app/blueprints/tareas/routes.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models import Tarea
from . import tareas_bp

@tareas_bp.route("/", methods=["GET"])
@login_required
def listado():
    tareas = Tarea.query.all()
    return render_template("tareas/listado.html", tareas=tareas)

@tareas_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva():
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        tarea = Tarea(titulo=titulo, descripcion=descripcion)
        db.session.add(tarea)
        db.session.commit()
        flash("Tarea creada con éxito", "success")
        return redirect(url_for("tareas.listado"))
    return render_template("tareas/form.html", accion="Nueva Tarea", tarea=None)

@tareas_bp.route("/<int:tarea_id>/editar", methods=["GET", "POST"])
@login_required
def editar(tarea_id):
    tarea = Tarea.query.get(tarea_id)
    if not tarea:
        flash("Tarea no encontrada", "danger")
        return redirect(url_for("tareas.listado"))

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
    tarea = Tarea.query.get(tarea_id)
    if not tarea:
        flash("Tarea no encontrada", "danger")
        return redirect(url_for("tareas.listado"))
    return render_template("tareas/detalle.html", tarea=tarea)

@tareas_bp.route("/<int:tarea_id>/eliminar", methods=["POST"])
@login_required
def eliminar(tarea_id):
    tarea = Tarea.query.get(tarea_id)
    if tarea:
        db.session.delete(tarea)
        db.session.commit()
        flash("Tarea eliminada", "info")
    return redirect(url_for("tareas.listado"))
