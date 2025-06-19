# app/blueprints/tareas/routes.py

from flask import (
    render_template, request, redirect,
    url_for, flash, abort
)
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Tarea, TareaCalificada, RolEnum
from app.services.tarea_service import actualizar_tarea_alumno
from . import tareas_bp
from .forms import ActualizarTareaForm


def _get_own_task_or_404(tarea_id: int) -> Tarea:
    """Obtiene una tarea por ID y verifica que el usuario tenga permisos."""
    tarea = Tarea.query.get(tarea_id)
    if not tarea:
        abort(404, "Tarea no encontrada")
    # ALUMNO solo ve las asignadas, otros ven las que crearon
    if current_user.rol == RolEnum.ALUMNO and tarea.asignado_a_id != current_user.id:
        abort(404)
    if current_user.rol != RolEnum.ALUMNO and tarea.user_id != current_user.id:
        abort(404)
    return tarea


@tareas_bp.route("/", methods=["GET"])
@login_required
def listado():
    """Muestra la lista de tareas del usuario."""
    if current_user.rol == RolEnum.ALUMNO:
        tareas = Tarea.query.filter_by(asignado_a_id=current_user.id).all()
    else:
        tareas = Tarea.query.filter_by(user_id=current_user.id).all()
    return render_template("tareas/listado.html", tareas=tareas)


@tareas_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva():
    """
    Permite al usuario crear una nueva tarea.
    (Los PROFESORES usan su propio blueprint);
    aquí la permitimos solo a ADMIN y USER.
    """
    if current_user.rol == RolEnum.ALUMNO:
        abort(403)
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            user_id=current_user.id
        )
        db.session.add(tarea)
        db.session.commit()
        flash("Tarea creada con éxito", "success")
        return redirect(url_for("tareas.listado"))
    return render_template("tareas/form.html",
                           accion="Nueva Tarea",
                           tarea=None)


@tareas_bp.route("/<int:tarea_id>/editar", methods=["GET", "POST"])
@login_required
def editar(tarea_id: int):
    """
    Permite al ALUMNO actualizar su detalle y estado.
    No se usa el checkbox antiguo; ahora hay un form especializado.
    """
    if current_user.rol != RolEnum.ALUMNO:
        abort(403)

    tarea = _get_own_task_or_404(tarea_id)
    cal = TareaCalificada.query.filter_by(cod_id_tarea=tarea_id).first()

    form = ActualizarTareaForm(
        detalle_alumno=cal.detalle_alumno or "",
        estado_id=tarea.estado_id or "01"
    )

    if form.validate_on_submit():
        actualizar_tarea_alumno(
            tarea_id=tarea.id,
            alumno_id=current_user.id,
            detalle_alumno=form.detalle_alumno.data,
            estado_destino=form.estado_id.data
        )
        flash("Tu avance se ha guardado", "success")
        return redirect(url_for("tareas.listado"))

    return render_template(
        "tareas/editar_alumno.html",
        tarea=tarea,
        form=form
    )


@tareas_bp.route("/<int:tarea_id>/ver", methods=["GET"])
@login_required
def detalle(tarea_id: int):
    """Muestra los datos de la tarea y su calificación/avance."""
    tarea = _get_own_task_or_404(tarea_id)
    cal = TareaCalificada.query.filter_by(cod_id_tarea=tarea_id).first()
    return render_template(
        "tareas/detalle.html",
        tarea=tarea,
        calificacion=cal
    )


@tareas_bp.route("/<int:tarea_id>/eliminar", methods=["POST"])
@login_required
def eliminar(tarea_id: int):
    """Elimina la tarea si el usuario tiene permisos."""
    tarea = _get_own_task_or_404(tarea_id)
    # Solo ADMIN y USER pueden borrar sus propias tareas
    if current_user.rol == RolEnum.ALUMNO:
        abort(403)
    db.session.delete(tarea)
    db.session.commit()
    flash("Tarea eliminada", "info")
    return redirect(url_for("tareas.listado"))
