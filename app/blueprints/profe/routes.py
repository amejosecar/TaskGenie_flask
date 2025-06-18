# app/blueprints/profe/routes.py

from datetime import date
from functools import wraps
from flask import (
    render_template, request,
    redirect, url_for, flash, abort
)
from flask_login import login_required, current_user
from . import profe_bp
from app.models import RolEnum, TareaCalificada, Usuario, Importancia
from app.services.tarea_service import asignar_tarea, calificar_tarea

def solo_profe(fn):
    """
    Requiere que current_user.rol == PROFESOR.
    (La autenticación la cubre @login_required).
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.rol != RolEnum.PROFESOR:
            abort(403, description="Acceso sólo para PROFESORES")
        return fn(*args, **kwargs)
    return wrapper

@profe_bp.route("/listado")
@login_required
@solo_profe
def listado():
    pendientes = TareaCalificada.query.filter_by(estatus_calificado="no").all()
    # Ahora buscamos directamente 'listado.html' dentro de templates/profe/
    return render_template("listado.html", pendientes=pendientes)

@profe_bp.route("/nueva", methods=["GET", "POST"])
@login_required
@solo_profe
def nueva():
    if request.method == "POST":
        asignar_tarea(
            titulo        = request.form["titulo"].strip(),
            descripcion   = request.form["descripcion"].strip(),
            fecha_entrega = date.fromisoformat(request.form["fecha_entrega"]),
            importancia_id= request.form["importancia_id"],
            asignado_a_id = int(request.form["asignado_a_id"]),
            creador_id    = current_user.id
        )
        flash("Tarea asignada con éxito", "success")
        return redirect(url_for("profe.listado"))

    alumnos      = Usuario.query.filter_by(rol=RolEnum.ALUMNO).all()
    importancias = Importancia.query.all()
    return render_template(
        "nueva.html",
        alumnos=alumnos,
        importancias=importancias
    )

@profe_bp.route("/calificar/<int:tarea_id>", methods=["GET", "POST"])
@login_required
@solo_profe
def calificar(tarea_id):
    cal = TareaCalificada.query.filter_by(cod_id_tarea=tarea_id).first()
    if not cal:
        abort(404, "Calificación no encontrada")

    if request.method == "POST":
        calificar_tarea(
            tarea_id        = tarea_id,
            profesor_id     = current_user.id,
            texto           = request.form["texto_calificado"].strip(),
            puntuacion      = int(request.form["puntuacion_calificado"]),
            fecha_calificado= date.fromisoformat(request.form["fecha_calificado"])
        )
        flash("Calificación guardada", "success")
        return redirect(url_for("profe.listado"))

    return render_template(
        "calificar.html",
        cal=cal,
        tarea=cal.tarea
    )
