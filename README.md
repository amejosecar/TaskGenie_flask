# TaskGenie_flask
Migración de TaskGenie con Flask

taskgenie/
├── instance/                   # 🔒 Carpeta de instancia (fuera de VCS)
│   └── taskgenie.db            # 🗄️ SQLite (se crea al arrancar)
│
├── .env                        # 🔑 Variables de entorno
├── .gitignore                  # 🚫 Archivos ignorados
├── requirements.txt            # 📦 Dependencias
├── run.py                      # 🚀 Launcher (factory pattern)
│
└── app/                        # 🧩 Paquete principal
----├── __init__.py             # 🍺 create_app()
----├── config.py               # ⚙️ Carga de .env
----├── extensions.py           # 🔌 db, csrf, login_manager…
----├── services/               # 🔧 Lógica de negocio
----│   └── auth_service.py
----├── models.py               # 📜 Modelos SQLAlchemy
----├── blueprints/             # 📌 Blueprints por funcionalidad
----│   ├── auth/               # 🔑 Login & Registro
----│   │   ├── __init__.py
----│   │   ├── routes.py
----│   │   ├── forms.py
----│   │   └── templates/auth/
----│   ├── admin/              # 👑 Panel de administración
----│   │   ├── __init__.py
----│   │   ├── routes.py
----│   │   └── templates/admin/
----│   ├── perfil/             # 🧑‍💼 Perfil de usuario
----│   │   ├── __init__.py
----│   │   ├── routes.py
----│   │   └── templates/perfil/
----│   ├── tareas/             # ✅ Gestión de tareas
----│   │   ├── __init__.py
----│   │   ├── routes.py
----│   │   └── templates/tareas/
----│   └── usuarios/           # 🔍 API usuarios
----│       ├── __init__.py
----│       ├── routes.py
----│       └── templates/usuarios/
----├── templates/              # 🎨 Plantillas globales
----│   ├── base.html
----│   ├── dashboard.html
----│   └── errores.html
----└── static/                 # 📁 CSS, JS, imágenes…

