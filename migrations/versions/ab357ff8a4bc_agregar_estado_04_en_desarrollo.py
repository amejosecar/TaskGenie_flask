"""Agregar estado 04 en desarrollo

Revision ID: ab357ff8a4bc
Revises: 35847497fc1c
Create Date: 2025-06-19 14:15:21.663394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab357ff8a4bc'
down_revision = '35847497fc1c'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
    "INSERT INTO tb_estado_tarea (cod_id, desc_estado_tarea) "
    "VALUES ('04', 'en desarrollo')"
)

def downgrade():
    op.execute("DELETE FROM tb_estado_tarea WHERE cod_id = '04'")
