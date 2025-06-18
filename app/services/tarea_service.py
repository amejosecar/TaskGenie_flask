# app/services/tarea_service.py

from datetime import date
from app.models import Tarea, TareaCalificada, RolEnum
from app.extensions import db

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


