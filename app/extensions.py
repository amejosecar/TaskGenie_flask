# app/extensions.py
# 🔌 Inicializa extensiones: ORM, CSRF, Login

# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager

# ORM: maneja la conexión y los modelos
db = SQLAlchemy()

# Protege todos los formularios de ataques CSRF
csrf = CSRFProtect()

# Gestiona login/logout y la sesión del usuario
login_manager = LoginManager()
login_manager.login_view = "auth.login"      
login_manager.session_protection = "strong"  

@login_manager.user_loader
def load_user(user_id: str):
    """
    Callback para Flask-Login: carga un Usuario dado su ID desde la sesión.
    Importamos aquí para evitar circular imports.
    """
    from app.models import Usuario
    return db.session.get(Usuario, int(user_id))
