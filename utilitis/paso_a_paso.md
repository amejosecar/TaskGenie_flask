# 🛠️ Plan de Inicio de Desarrollo

Este documento describe, paso a paso, cómo arrancar la migración de FastAPI a Flask usando la estructura de Blueprints.

## 📂 Estructura del Proyecto (por ahora)

```text
taskgenie_flask/
├── instance/                   # 🔒 Carpeta de instancia (fuera de VCS)
│   └── taskgenie.db            # 🗄️ SQLite (se crea al arrancar)
├── .env                        # 🔑 Variables de entorno
├── .gitignore                  # 🚫 Archivos ignorados
├── requirements.txt            # 📦 Dependencias
├── run.py                      # 🚀 Launcher (factory pattern)
└── app/                        # 🧩 Paquete principal
    ├── __init__.py             # 🍺 create_app()
    ├── config.py               # ⚙️ Carga de .env
    ├── extensions.py           # 🔌 db, csrf, login_manager…
    ├── services/               # 🔧 Lógica de negocio
    │   └── auth_service.py
    ├── models.py               # 📜 Modelos SQLAlchemy
    ├── blueprints/             # 📌 Blueprints por funcionalidad
    │   ├── auth/               # 🔑 Login & Registro
    │   │   ├── __init__.py
    │   │   ├── routes.py
    │   │   ├── forms.py
    │   │   └── templates/auth/
    │   ├── admin/              # 👑 Panel de administración
    │   │   ├── __init__.py
    │   │   ├── routes.py
    │   │   └── templates/admin/
    │   ├── perfil/             # 🧑‍💼 Perfil de usuario
    │   │   ├── __init__.py
    │   │   ├── routes.py
    │   │   └── templates/perfil/
    │   ├── tareas/             # ✅ Gestión de tareas
    │   │   ├── __init__.py
    │   │   ├── routes.py
    │   │   └── templates/tareas/
    │   └── usuarios/           # 🔍 API usuarios
    │       ├── __init__.py
    │       ├── routes.py
    │       └── templates/usuarios/
    ├── templates/              # 🎨 Plantillas globales
    │   ├── base.html
    │   ├── dashboard.html
    │   └── errores.html
    └── static/                 # 📁 CSS, JS, imágenes…
```

---

## 1. Preparación del Entorno

1. Crea y activa tu entorno virtual.
2. Rellena `.env` con `DATABASE_URL`, `SECRET_KEY`, `DEBUG_MODE`.
3. En `requirements.txt` añade: Flask Flask-WTF Flask-Login python-dotenv Flask-SQLAlchemy Pydantic
4. En `.gitignore` incluye: instance/ \*.pyc .env

✅Listo creado por copailot - 13/06/2025

---

## 2. Estructura Inicial y Launcher

- **run.py**  
  – Script de arranque que invoca `create_app()`.
- **app/**init**.py**  
   – Define `create_app()`: carga configuración, inicializa extensiones y registra Blueprints.
  ✅Listo creado por copailot - 13/06/2025

---

## 3. Configuración Global

- **app/config.py**  
  – Lee `.env` y define `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `DEBUG`.
- **app/extensions.py**  
   – Instancias de `db`, `csrf`, `login_manager` sin atar aún a la app.
  ✅Listo creado por copailot - 13/06/2025

---

## 4. Stub en Memoria (Servicio Sin BD)

1. Crea `app/services/memory_repo.py` con clase `MemoryDB` que implemente `add()`, `commit()`, `query()`, `rollback()`, `refresh()`.
2. Ajusta temporalmente `app/services/auth_service.py` o en tus Blueprints para inyectar `MemoryDB()` en lugar de `SessionLocal()`.
   ✅Listo creado por copailot - 13/06/2025

---

## 5. Plantillas Base y Páginas Globales

- **app/templates/base.html**  
  – Layout general con bloques de Jinja2.
- **app/templates/errores.html**  
  – Página de error (404).
- **app/templates/dashboard.html**  
  – Dashboard genérico para usuarios autenticados.
  ✅Listo creado por copailot - 13/06/2025

---

## 6. Blueprint: Autenticación

Ruta: `app/blueprints/auth/`

- `__init__.py` → instancia de `auth_bp`
- `routes.py` → `/login`, `/registro` (GET y POST)
- `forms.py` → `LoginForm`, `RegisterForm` (Flask-WTF + CSRF)
- `templates/auth/login.html`, `templates/auth/register.html` (extienden `base.html`)
  ✅Listo creado por copailot - 13/06/2025

---

## 7. Blueprint: Administración

Ruta: `app/blueprints/admin/`

- `__init__.py` → instancia de `admin_bp`
- `routes.py` → Listar usuarios, buscar, cambiar rol/bloqueo, eliminar
- `templates/admin/dashboard_admin.html`
  ✅Listo creado por copailot - 13/06/2025

---

## 8. Blueprint: Perfil

Ruta: `app/blueprints/perfil/`

- `__init__.py` → `perfil_bp`
- `routes.py` → `/perfil` (ver/editar datos)
- `templates/perfil/perfil.html`
  ✅Listo creado por copailot - 13/06/2025

---

## 9. Blueprint: Tareas

Ruta: `app/blueprints/tareas/`

- `__init__.py` → `tareas_bp`
- `routes.py` → CRUD de tareas (listar, crear, editar, ver)
- `templates/tareas/listado.html`, `templates/tareas/form.html`, `templates/tareas/detalle.html`
  ✅Listo creado por copailot - 13/06/2025

---

## 10. Blueprint: API Usuarios (JSON)

Ruta: `app/blueprints/usuarios/`

- `__init__.py` → `usuarios_bp`
- `routes.py` → `/u/registro-json`, búsqueda por email/rol, etc.
- `templates/usuarios/` (copailot por favor desarrolla algo para saber que funciona)
  ✅Listo creado por copailot - 13/06/2025

---

## 11. Modelos y Creación de la BD

- **app/models.py** → Define `Usuario`, `Tarea`, `RolEnum`.
- En `create_app()`, dentro de `app.app_context()`, invoca `db.create_all()` para generar `instance/taskgenie.db`.
- Inserta 3 usuarios a la bd de pruebas

```
  usuario1
    nombre= Americo-admin,
    apellido=carrillo,
    edad=24,
    email=amejosecar@keko.com,
    clave_hash=333333,
    fecha_nacimiento=1970-12-18,
    rol=administrador
  usuario2
    nombre= Americo-profe,
    apellido=carrillo,
    edad=24,
    email=amejosecar@profe.com,
    clave_hash=333333,
    fecha_nacimiento=1970-12-18,
    rol=profesor
  usuario3
    nombre= Americo-Alum,
    apellido=carrillo,
    edad=24,
    email=amejosecar@alumno.com,
    clave_hash=333333,
    fecha_nacimiento=1970-12-18,
    rol=alumno
```

---

## 12. Migración a BD Real

1. Sustituye en Blueprints `MemoryDB()` por la sesión real:

```python
from app.extensions import db
session = db.session



ya vremos
Arranca la app y comprueba instance/taskgenie.db con tablas creadas.

13. Recursos Estáticos y Refinamientos
app/static/ → CSS, JS e imágenes.

Ajusta validaciones en app/services/auth_service.py, formularios WTForms y plantillas Jinja2.

Prepara pruebas unitarias primero con stub y luego con la BD real.
```
