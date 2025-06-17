# utilitis/seed_initial.py

"""
Script para insertar datos iniciales en tb_importancia y tb_estado_tarea.
Ejecutar: python scripts/seed_initial.py
"""

from app import create_app
from app.extensions import db
from app.models import Importancia, EstadoTarea

def seed_importancia():
    if not Importancia.query.first():
        datos_imp = [
            ("01", "alta",  "Muy importante"),
            ("02", "media", "Importante"),
            ("03", "baja",  "Normal"),
        ]
        for cod, tipo, desc in datos_imp:
            db.session.add(Importancia(
                cod_id=cod,
                tipo_importancia=tipo,
                desc_importancia=desc
            ))
        print("Semilla: tb_importancia completada.")
    else:
        print("tb_importancia ya contiene datos; se omite semilla.")

def seed_estado_tarea():
    if not EstadoTarea.query.first():
        datos_est = [
            ("01", "asignada"),
            ("02", "completada"),
            ("03", "cancelada"),
        ]
        for cod, desc in datos_est:
            db.session.add(EstadoTarea(
                cod_id=cod,
                desc_estado_tarea=desc
            ))
        print("Semilla: tb_estado_tarea completada.")
    else:
        print("tb_estado_tarea ya contiene datos; se omite semilla.")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_importancia()
        seed_estado_tarea()
        db.session.commit()
        print("Inserción de datos iniciales finalizada.")
