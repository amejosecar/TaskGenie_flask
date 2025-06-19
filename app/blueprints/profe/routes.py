# app/blueprints/profe/routes.py

# app/blueprints/profe/routes.py

from datetime import date
from functools import wraps
from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from . import profe_bp
from .forms import AsignarTareaForm, CalificarTareaForm
from app.models import RolEnum, TareaCalificada, Usuario, Importancia
from app.services.tarea_service import asignar_tarea, calificar_tarea

def solo_profe(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.rol != RolEnum.PROFESOR:
            abort(403, description="Acceso sólo para PROFESORES")
        return fn(*args, **kwargs)
    return login_required(wrapper)


@profe_bp.route("/nueva", methods=["GET", "POST"])
@solo_profe
def nueva():
    form = AsignarTareaForm()
    # rellenar select choices
    form.importancia_id.choices = [
        (imp.cod_id, imp.tipo_importancia) for imp in Importancia.query.all()
    ]
    form.asignado_a_id.choices = [
        (u.id, f"{u.nombre} {u.apellido}")
        for u in Usuario.query.filter_by(rol=RolEnum.ALUMNO)
    ]

    if form.validate_on_submit():
        asignar_tarea(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            fecha_entrega=form.fecha_entrega.data,
            importancia_id=form.importancia_id.data,
            asignado_a_id=form.asignado_a_id.data,
            creador_id=current_user.id
        )
        flash("Tarea asignada con éxito", "success")
        return redirect(url_for("profe.listado"))

    # Busca en .../templates/profe/nueva.html
    return render_template("nueva.html", form=form)


@profe_bp.route("/calificar/<int:tarea_id>", methods=["GET", "POST"])
@solo_profe
def calificar(tarea_id):
    cal = TareaCalificada.query.filter_by(cod_id_tarea=tarea_id).first_or_404()
    form = CalificarTareaForm(
        texto_calificado=cal.texto_calificado,
        puntuacion_calificado=cal.puntuacion_calificado,
        fecha_calificado=cal.fecha_calificado
    )

    if form.validate_on_submit():
        calificar_tarea(
            tarea_id=tarea_id,
            profesor_id=current_user.id,
            texto=form.texto_calificado.data,
            puntuacion=form.puntuacion_calificado.data,
            fecha_calificado=form.fecha_calificado.data
        )
        flash("Calificación guardada", "success")
        return redirect(url_for("profe.listado"))

    # Busca en .../templates/profe/calificar.html
    return render_template("calificar.html", form=form, tarea=cal.tarea)


@profe_bp.route("/listado")
@solo_profe
def listado():
    pendientes = TareaCalificada.query.filter_by(estatus_calificado="no").all()
    # Ahora Jinja buscará en <blueprint>/templates/profe/listado.html
    return render_template("listado.html", pendientes=pendientes)
