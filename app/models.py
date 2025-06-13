# app/models.py

from enum import Enum
from datetime import date
from flask_login import UserMixin
from app.extensions import db

class RolEnum(Enum):
    ADMIN    = "ADMIN"
    PROFESOR = "PROFESOR"
    ALUMNO   = "ALUMNO"
    USER     = "USER"

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id               = db.Column(db.Integer, primary_key=True)
    nombre           = db.Column(db.String(50), nullable=False)
    apellido         = db.Column(db.String(50), nullable=False)
    email            = db.Column(db.String(120), unique=True, nullable=False)
    clave_hash       = db.Column(db.String(128), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    rol              = db.Column(db.Enum(RolEnum), default=RolEnum.USER, nullable=False)
    is_blocked       = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Usuario {self.email}>"

    @property
    def edad(self) -> int:
        """Calcula la edad a partir de la fecha de nacimiento."""
        today = date.today()
        born = self.fecha_nacimiento
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class Tarea(db.Model):
    __tablename__  = "tareas"

    id             = db.Column(db.Integer, primary_key=True)
    titulo         = db.Column(db.String(100), nullable=False)
    descripcion    = db.Column(db.Text, nullable=True)
    completada     = db.Column(db.Boolean, default=False)
    fecha_creacion = db.Column(db.Date, default=date.today)

    def __repr__(self):
        return f"<Tarea {self.id} {self.titulo}>"
