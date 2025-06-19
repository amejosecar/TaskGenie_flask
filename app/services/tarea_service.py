# app/services/tarea_service.py

from datetime import date
from app.models import Tarea, TareaCalificada, RolEnum
from app.extensions import db
from flask import abort
from app.models import Tarea, TareaCalificada


def asignar_tarea(titulo: str,
                  descripcion: str,
                  fecha_entrega: date,
                  importancia_id: str,
                  asignado_a_id: int,
                  creador_id: int) -> Tarea:
    """
    Crea una Tarea y un TareaCalificada inicial.
    """
    # 1) Construye la tarea
    tarea = Tarea(
        titulo=titulo,
        descripcion=descripcion,
        fecha_creacion=date.today(),
        fecha_entrega=fecha_entrega,
        importancia_id=importancia_id,
        estado_id="01",           # 'asignada'
        asignado_a_id=asignado_a_id,
        user_id=creador_id
    )
    db.session.add(tarea)
    db.session.flush()  # Para obtener tarea.id

    # 2) Crea TareaCalificada inicial
    cal = TareaCalificada(
        cod_id_tarea=tarea.id,
        estatus_calificado="no"
    )
    db.session.add(cal)
    db.session.flush()

    # 3) Relaciona la FK en tarea
    tarea.calificacion_id = cal.cod_id_califica

    db.session.commit()
    return tarea

def calificar_tarea(tarea_id: int,
                    profesor_id: int,
                    texto: str,
                    puntuacion: int,
                    fecha_calificado: date) -> TareaCalificada:
    """
    Añade texto, puntuación y fecha a la calificación.
    Solo PROFESORES pueden hacerlo.
    """
    # 1) Carga la tarea y su calificación
    cal = TareaCalificada.query.filter_by(cod_id_tarea=tarea_id).first()
    if not cal:
        raise ValueError("Calificación no encontrada")
    # 2) Valida rol del profesor
    from app.models import Usuario
    prof = Usuario.query.get(profesor_id)
    if prof.rol != RolEnum.PROFESOR:
        raise PermissionError("Sólo PROFESORES pueden calificar")
    # 3) Actualiza
    cal.texto_calificado = texto
    cal.puntuacion_calificado = puntuacion
    cal.fecha_calificado = fecha_calificado
    cal.estatus_calificado = "si"
    # 4) Cambia estado de la tarea
    tarea = Tarea.query.get(tarea_id)
    tarea.estado_id = "02"  # 'completada'
    db.session.commit()
    return cal

def actualizar_tarea_alumno(tarea_id: int,
                            alumno_id: int,
                            detalle_alumno: str,
                            estado_destino: str) -> TareaCalificada:
    """
    Permite al alumno subir su detalle y cambiar el estado de la tarea.
    Si estado_destino == '04' fija 'en desarrollo'; si '02' fija completado + fecha_entrega.
    """
    # 1) Obtener la tarea y verificar propiedad
    tarea = Tarea.query.get(tarea_id)
    if not tarea or tarea.user_id != alumno_id:
        abort(404, "Tarea no encontrada o sin permisos")

    # 2) Sólo permitir avanzar desde 'asignada'(01) o 'en desarrollo'(04)
    if tarea.estado_id not in ('01', '04'):
        abort(403, "No puedes modificar esta tarea en su estado actual")

    # 3) Actualizar estado de la tarea
    tarea.estado_id = estado_destino
    if estado_destino == '02':  # completada
        tarea.fecha_entrega = date.today()

    # 4) Actualizar la calificación con detalle del alumno
    cal = TareaCalificada.query.filter_by(cod_id_tarea=tarea_id).first()
    cal.detalle_alumno = detalle_alumno
    cal.fecha_detalle_alumno = date.today()

    # 5) Commit
    db.session.commit()
    return cal
