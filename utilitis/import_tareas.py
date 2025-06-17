#!/usr/bin/env python3
# utilitis/import_tareas.py

import sys
from pathlib import Path
import csv
from datetime import datetime, date

# ── Aseguramos que la raíz del proyecto esté en sys.path ──────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import create_app
from app.extensions import db
from app.models import Tarea, Usuario, RolEnum

CSV_PATH = ROOT / "utilitis" / "carga_tareas.csv"

def str_to_bool(s: str) -> bool:
    return str(s).strip().lower() in ("1", "true", "yes", "y", "sí", "si")

def parse_date(s: str) -> date:
    s = str(s).strip()
    return date.today() if not s else datetime.strptime(s, "%Y-%m-%d").date()

def main():
    app = create_app()
    with app.app_context():
        if not CSV_PATH.exists():
            print(f"ERROR: no existe {CSV_PATH}")
            return

        total = 0
        inserted = 0

        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                total += 1

                # Validamos que haya al menos 6 columnas:
                # user_id;rol;titulo;descripcion;completada;fecha_creacion
                if len(row) < 6:
                    print(f"[Línea {total}] columnas insuficientes, se omite: {row}")
                    continue

                user_id_str, rol_str, titulo, descripcion, completa_str, fecha_str = row

                # 1) Parsear el rol del CSV
                rol_key = rol_str.strip().upper()
                try:
                    rol_csv = RolEnum[rol_key]
                except KeyError:
                    print(f"[Línea {total}] rol inválido '{rol_str}', se omite.")
                    continue

                # 2) Sólo ALUMNO o PROFESOR pueden cargar tareas
                if rol_csv not in (RolEnum.ALUMNO, RolEnum.PROFESOR):
                    print(f"[Línea {total}] rol '{rol_csv.value}' no permite tareas, se omite.")
                    continue

                # 3) Validar user_id
                try:
                    user_id = int(user_id_str)
                except ValueError:
                    print(f"[Línea {total}] user_id inválido '{user_id_str}', se omite.")
                    continue

                # 4) Verificar que el Usuario exista en BD
                usuario = db.session.get(Usuario, user_id)
                if not usuario:
                    print(f"[Línea {total}] usuario {user_id} no existe, se omite.")
                    continue

                # 5) Crear e insertar la tarea
                try:
                    tarea = Tarea(
                        titulo=titulo.strip(),
                        descripcion=descripcion.strip() or None,
                        completada=str_to_bool(completa_str),
                        fecha_creacion=parse_date(fecha_str),
                        user_id=user_id
                    )
                    db.session.add(tarea)
                    inserted += 1
                except Exception as e:
                    print(f"[Línea {total}] ERROR creando Tarea: {e}")

        # 6) Commit final
        if inserted:
            db.session.commit()

        print(f"Total filas leídas:   {total}")
        print(f"Tareas insertadas:    {inserted}")

if __name__ == "__main__":
    main()
