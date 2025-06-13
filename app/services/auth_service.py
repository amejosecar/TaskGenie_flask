# app/services/auth_service.py

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from ..models import Usuario, RolEnum

def registrar_usuario(db, nombre, apellido, edad, email, clave, fecha_nacimiento, rol=RolEnum.USER):
    # 1) Validaciones (unicidad de email, formato de fecha…)
    if db.query(Usuario).filter_by(email=email).first():
        raise ValueError("Email ya registrado")

    # 2) Crear instancia
    usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        edad=edad, 
        email=email,
        clave_hash=generate_password_hash(clave),
        fecha_nacimiento=datetime.strptime(fecha_nacimiento, "%Y-%m-%d").date(),
        rol=rol
    )

    # 3) Persistir
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def autenticar_usuario(db, email, clave):
    usuario = db.query(Usuario).filter_by(email=email).first()
    if not usuario or not check_password_hash(usuario.clave_hash, clave):
        return None
    return usuario
