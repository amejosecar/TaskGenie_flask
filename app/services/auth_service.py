# app/services/auth_service.py

# app/services/auth_service.py
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app.models import Usuario, RolEnum
from app.extensions import db

def registrar_usuario(nombre: str,
                      apellido: str,
                      email: str,
                      clave: str,
                      fecha_nacimiento: str,
                      rol: RolEnum = RolEnum.USER) -> Usuario:
    # 1) Unicidad de email
    if Usuario.query.filter_by(email=email).first():
        raise ValueError("Email ya registrado")

    # 2) Crear y persistir
    usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        clave_hash=generate_password_hash(clave),
        fecha_nacimiento=datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date(),
        rol=rol
    )
    db.session.add(usuario)
    db.session.commit()
    # db.session.refresh(usuario)  # SQLAlchemy ya lo actualiza con el ID
    return usuario

def autenticar_usuario(email: str, clave: str) -> Usuario | None:
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not check_password_hash(usuario.clave_hash, clave):
        return None
    return usuario
