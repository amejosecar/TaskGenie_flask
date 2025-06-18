# seed_tasks.py

from datetime import date, datetime
from app import create_app
from app.extensions import db
from app.models import (
    Usuario, Importancia, EstadoTarea,
    Tarea, TareaCalificada, RolEnum
)

# 1) Usuarios iniciales
USERS = [
    ("Americo-admin", "carrillo", "amejosecar@keko.com", "333333", "1970-12-18", RolEnum.ADMIN),
    ("Americo-profe", "carrillo", "amejosecar@profe.com", "333333", "1970-12-18", RolEnum.PROFESOR),
    ("Americo-Alum",  "carrillo", "amejosecar@alumno.com", "333333", "1970-12-18", RolEnum.ALUMNO),
]

# 2) Importancias
IMPORTANCIAS = [
    ("01", "alta",  "Muy importante"),
    ("02", "media", "Importante"),
    ("03", "baja",  "Normal"),
]

# 3) Estados de tarea
ESTADOS = [
    ("01", "asignada"),
    ("02", "completada"),
    ("03", "cancelada"),
]

# 4) Tareas de prueba
# (id, título, descripción, completada, fecha_creación,
#  user_id, fecha_entrega, importancia_id, estado_id,
#  asignado_a_id, calificacion_id)
TASKS = [
    (1,  "Revisar presupuesto Q2",
         "Verificar gastos y ajustar previsiones para el segundo trimestre",
         False, "2025-06-01", 2, "2025-06-08", "01", "01", 3, 1),
    (2,  "Actualizar documentación API",
         "Incorporar nuevos endpoints y detalles de uso en manual técnico",
         False, "2025-06-02", 2, "2025-06-09", "03", "01", 3, 2),
    (3,  "Diseñar propuesta cliente",
         "Crear mockups y presentación para propuesta de diseño web",
         False, "2025-06-03", 2, "2025-06-10", "02", "01", 3, 3),
    (4,  "Optimizar base de datos",
         "Implementar índices y limpiar registros obsoletos",
         False, "2025-06-04", 2, "2025-06-11", "01", "01", 3, 4),
    (5,  "Plan de marketing",
         "Definir estrategias digitales para el próximo trimestre",
         False, "2025-06-05", 2, "2025-06-12", "02", "01", 3, 5),
    (6,  "Reunión con proveedores",
         "Agendar y preparar agenda para negociación de precios",
         False, "2025-06-06", 2, "2025-06-13", "03", "01", 3, 6),
    (7,  "Test de usabilidad",
         "Realizar pruebas con usuarios y documentar hallazgos",
         False, "2025-06-07", 2, "2025-06-14", "02", "01", 3, 7),
    (8,  "Implementar autenticación",
         "Añadir OAuth2 al módulo de inicio de sesión",
         False, "2025-06-08", 2, "2025-06-15", "01", "01", 3, 8),
    (9,  "Refactorizar código legacy",
         "Mejorar legibilidad y rendimiento de módulos antiguos",
         False, "2025-06-09", 2, "2025-06-16", "03", "01", 3, 9),
    (10, "Analizar métricas KPIs",
         "Revisar indicadores clave y preparar informe ejecutivo",
         False, "2025-06-10", 2, "2025-06-17", "01", "01", 3, 10),
]

def run():
    app = create_app()
    with app.app_context():
        # Seed Usuarios
        if not Usuario.query.first():
            for nombre, apellido, email, clave, fn, rol in USERS:
                u = Usuario(
                    nombre=nombre,
                    apellido=apellido,
                    email=email,
                    clave_hash=Usuario().__class__.__dict__['clave_hash'],  # placeholder
                    fecha_nacimiento=datetime.fromisoformat(fn).date(),
                    rol=rol
                )
                # Hashea la clave (reemplazar con generate_password_hash)
                from werkzeug.security import generate_password_hash
                u.clave_hash = generate_password_hash(clave)
                db.session.add(u)
            db.session.commit()
            print("✔️ Usuarios semeados")

        # Seed Importancias
        if not Importancia.query.first():
            for cod, tipo, desc in IMPORTANCIAS:
                db.session.add(Importancia(
                    cod_id=cod,
                    tipo_importancia=tipo,
                    desc_importancia=desc
                ))
            db.session.commit()
            print("✔️ Importancias semeadas")

        # Seed Estados
        if not EstadoTarea.query.first():
            for cod, desc in ESTADOS:
                db.session.add(EstadoTarea(
                    cod_id=cod,
                    desc_estado_tarea=desc
                ))
            db.session.commit()
            print("✔️ Estados de tarea semeados")

        # Seed Tareas
        exist = Tarea.query.first()
        if not exist:
            for (
                id_, titulo, descripcion, completada,
                fc, uid, fe, imp, est, asg, cid
            ) in TASKS:
                t = Tarea(
                    id=id_,
                    titulo=titulo,
                    descripcion=descripcion,
                    completada=completada,
                    fecha_creacion=date.fromisoformat(fc),
                    user_id=uid,
                    fecha_entrega=date.fromisoformat(fe),
                    importancia_id=imp,
                    estado_id=est,
                    asignado_a_id=asg
                )
                db.session.add(t)
            db.session.commit()
            print("✔️ Tareas semeadas")

        # Seed Calificaciones
        exist_cal = TareaCalificada.query.first()
        if not exist_cal:
            for (
                id_, *_rest, cid
            ) in TASKS:
                c = TareaCalificada(
                    cod_id_tarea=cid,
                    estatus_calificado="no"
                )
                db.session.add(c)
            db.session.commit()
            print("✔️ Calificaciones semeadas")

        print("✅ Seed completo.")

if __name__ == "__main__":
    run()
