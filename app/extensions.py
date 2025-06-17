# app/extensions.py
# 🔌 Inicializa extensiones: ORM, CSRF, Login
# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate

# naming convention para que Alembic autogenere nombres de constraints
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=naming_convention)

db = SQLAlchemy(metadata=metadata)
csrf = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"

@login_manager.user_loader
def load_user(user_id: str):
    from app.models import Usuario
    return db.session.get(Usuario, int(user_id))

