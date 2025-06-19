# app/models.py

from datetime import date
from enum import Enum

from flask_login import UserMixin

from app.extensions import db


class RolEnum(Enum):
    """Enumeración de roles permitidos en la aplicación."""
    ADMIN    = "ADMIN"
    PROFESOR = "PROFESOR"
    ALUMNO   = "ALUMNO"
    USER     = "USER"


class Usuario(UserMixin, db.Model):
    """Representa a un usuario de la plataforma."""
    __tablename__ = "usuarios"

    id               = db.Column(db.Integer, primary_key=True)
    nombre           = db.Column(db.String(50), nullable=False)
    apellido         = db.Column(db.String(50), nullable=False)
    email            = db.Column(db.String(120), unique=True, nullable=False)
    clave_hash       = db.Column(db.String(128), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    rol              = db.Column(db.Enum(RolEnum), default=RolEnum.USER, nullable=False)
    is_blocked       = db.Column(db.Boolean, default=False)

    # Relaciones
    tareas_creadas   = db.relationship(
        "Tarea",
        foreign_keys="Tarea.user_id",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
    tareas_recibidas = db.relationship(
        "Tarea",
        foreign_keys="Tarea.asignado_a_id",
        back_populates="asignado_a"
    )

    def __repr__(self):
        return f"<Usuario {self.email}>"

    @property
    def edad(self) -> int:
        """Calcula la edad en años a partir de la fecha de nacimiento."""
        hoy = date.today()
        born = self.fecha_nacimiento
        delta = (hoy.month, hoy.day) < (born.month, born.day)
        return hoy.year - born.year - delta


class Importancia(db.Model):
    """Niveles de importancia para las tareas."""
    __tablename__ = "tb_importancia"

    cod_id           = db.Column(db.String(2), primary_key=True)
    tipo_importancia = db.Column(db.String(20), nullable=False)
    desc_importancia = db.Column(db.String(100), nullable=False)

    tareas = db.relationship(
        "Tarea",
        back_populates="importancia"
    )

    def __repr__(self):
        return f"<Importancia {self.cod_id}>"


class EstadoTarea(db.Model):
    """Estados posibles de una tarea (asignada, en desarrollo, completada, etc.)."""
    __tablename__ = "tb_estado_tarea"

    cod_id            = db.Column(db.String(2), primary_key=True)
    desc_estado_tarea = db.Column(db.String(50), nullable=False)

    tareas = db.relationship(
        "Tarea",
        back_populates="estado"
    )

    def __repr__(self):
        return f"<EstadoTarea {self.cod_id} {self.desc_estado_tarea}>"


class TareaCalificada(db.Model):
    """Extensión de la tarea para calificaciones y detalle del alumno."""
    __tablename__ = "tb_tarea_calificada"

    cod_id_califica        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_id_tarea           = db.Column(db.Integer, db.ForeignKey("tareas.id"), nullable=False)
    fecha_calificado       = db.Column(db.Date, nullable=True)
    texto_calificado       = db.Column(db.Text, nullable=True)
    puntuacion_calificado  = db.Column(db.Integer, nullable=True)
    estatus_calificado     = db.Column(db.String(2), nullable=False, default="no")
    detalle_alumno         = db.Column(db.Text, nullable=True)
    fecha_detalle_alumno   = db.Column(db.Date, nullable=True)

    tarea = db.relationship(
        "Tarea",
        back_populates="calificaciones",
        foreign_keys=[cod_id_tarea]
    )

    def __repr__(self):
        return f"<TareaCalificada {self.cod_id_califica}>"


class Tarea(db.Model):
    """Tarea principal que puede crear un usuario y asignar a otro."""
    __tablename__ = "tareas"

    id               = db.Column(db.Integer, primary_key=True)
    titulo           = db.Column(db.String(100), nullable=False)
    descripcion      = db.Column(db.Text, nullable=True)
    completada       = db.Column(db.Boolean, default=False)
    fecha_creacion   = db.Column(db.Date, default=date.today)
    fecha_entrega    = db.Column(db.Date, nullable=True)

    # Claves foráneas
    user_id          = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    importancia_id   = db.Column(db.String(2), db.ForeignKey("tb_importancia.cod_id"), nullable=True)
    estado_id        = db.Column(db.String(2), db.ForeignKey("tb_estado_tarea.cod_id"), nullable=True)
    asignado_a_id    = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    calificacion_id  = db.Column(db.Integer, db.ForeignKey("tb_tarea_calificada.cod_id_califica"), nullable=True)

    # Relaciones
    usuario        = db.relationship(
        "Usuario",
        foreign_keys=[user_id],
        back_populates="tareas_creadas"
    )
    asignado_a     = db.relationship(
        "Usuario",
        foreign_keys=[asignado_a_id],
        back_populates="tareas_recibidas"
    )
    importancia    = db.relationship(
        "Importancia",
        back_populates="tareas"
    )
    estado         = db.relationship(
        "EstadoTarea",
        back_populates="tareas"
    )
    calificaciones = db.relationship(
        "TareaCalificada",
        back_populates="tarea",
        cascade="all, delete-orphan",
        foreign_keys="[TareaCalificada.cod_id_tarea]"
    )

    def __repr__(self):
        return f"<Tarea {self.id} {self.titulo}>"
