# app/config.py
# ⚙️ Carga de .env y definición de configuración

# app/config.py

# app/config.py
import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR     = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "cambiame-ya")

    # Construye el path absoluto a la BD por defecto
    default_db = INSTANCE_DIR.joinpath("taskgenie.db").as_posix()

    # Lee env var y normaliza si es SQLite
    raw = os.getenv("DATABASE_URL", f"sqlite:///{default_db}")
    if raw.startswith("sqlite:///"):
        # extrae el path tras 'sqlite:///' y conviértelo a absoluto si no lo es
        p = raw[10:]
        p = Path(p)
        if not p.is_absolute():
            p = BASE_DIR / p
        db_uri = f"sqlite:///{p.as_posix()}"
    else:
        db_uri = raw

    SQLALCHEMY_DATABASE_URI      = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG                        = os.getenv("DEBUG_MODE", "False").lower() in ("true","1","yes")
