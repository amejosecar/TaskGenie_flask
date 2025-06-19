"""Agregar estado 04 “en desarrollo”

Revision ID: a1b2c3d4e5f6
Revises: 06009f2cb2b5
Create Date: 2025-06-19 15:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# Identificadores de la migración
revision = 'a1b2c3d4e5f6'
down_revision = '06009f2cb2b5'
branch_labels = None
depends_on = None

def upgrade():
    # Inserción del nuevo estado en desarrollo
    op.execute(
        "INSERT INTO tb_estado_tarea (cod_id, desc_estado_tarea) "
        "VALUES ('04', 'en desarrollo')"
    )

def downgrade():
    # Eliminación del estado si se revierte la migración
    op.execute(
        "DELETE FROM tb_estado_tarea WHERE cod_id = '04'"
    )
