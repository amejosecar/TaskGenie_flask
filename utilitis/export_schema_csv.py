# utilitis/export_schema_csv.py

"""
Lee la estructura de todas las tablas de taskgenie.db
y exporta la información de columnas a un único CSV
en la carpeta utilitis dentro del proyecto.
"""

import sqlite3
import csv
import os

def get_table_names(conn):
    cursor = conn.execute("""
        SELECT name 
          FROM sqlite_master 
         WHERE type='table' 
           AND name NOT LIKE 'sqlite_%';
    """)
    return [row[0] for row in cursor.fetchall()]

def get_table_info(conn, table):
    cursor = conn.execute(f"PRAGMA table_info('{table}')")
    # cid, name, type, notnull, dflt_value, pk
    return cursor.fetchall()

def export_schema_to_csv(db_path, csv_path):
    conn = sqlite3.connect(db_path)
    tables = get_table_names(conn)

    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Cabecera
        writer.writerow([
            "table_name", "cid", "column_name", "data_type",
            "not_null", "default_value", "is_pk"
        ])

        for tbl in tables:
            for cid, name, col_type, notnull, dflt, pk in get_table_info(conn, tbl):
                writer.writerow([tbl, cid, name, col_type, notnull, dflt, pk])

    conn.close()
    print(f"Esquema exportado a {csv_path}")


if __name__ == "__main__":
    # Base del proyecto
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    # Ruta del fichero SQLite
    db_file = os.path.join(project_root, "instance", "taskgenie.db")
    # Directorio de salida solicitado
    output_dir = os.path.join(project_root, "utilitis")
    os.makedirs(output_dir, exist_ok=True)
    # Ruta completa al CSV
    csv_file = os.path.join(output_dir, "schema_export.csv")

    export_schema_to_csv(db_file, csv_file)
