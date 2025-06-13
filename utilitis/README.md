# 🚀 TaskGenie

**TaskGenie** es un sistema de gestión de tareas y usuarios desarrollado con **FastAPI**, pensado para entornos académicos o administrativos. Permite manejar distintos roles (administrador, profesor, alumno) y ofrece vistas personalizadas, autenticación segura y funcionalidades avanzadas.

---

## 📋 Índice

- [🚀 TaskGenie](#-taskgenie)
  - [📋 Índice](#-índice)
  - [📋 Análisis Global](#-análisis-global)
    - [🏗️ Arquitectura](#️-arquitectura)
  - [📦 Paquetes Utilizados](#-paquetes-utilizados)
  - [🛠️ Funcionalidad](#️-funcionalidad)
  - [📁 Estructura del Proyecto](#-estructura-del-proyecto)
  - [📆 Contexto Formativo](#-contexto-formativo)
  - [👨‍💼 Equipo](#-equipo)
  - [📊 Características](#-características)
  - [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
  - [🔧 Cómo Usar](#-cómo-usar)

---

## 📋 Análisis Global

### 🏗️ Arquitectura

- **Backend**: FastAPI con routers modularizados
- **Base de datos**: SQLite gestionada por SQLAlchemy
- **Plantillas**: Jinja2 para HTML dinámico
- **Autenticación**: Formularios + cookies HTTP-only

---

## 📦 Paquetes Utilizados

| Paquete            | Uso                                            |
| ------------------ | ---------------------------------------------- |
| **FastAPI**        | Creación de endpoints y API REST               |
| **SQLAlchemy**     | ORM para administrar la base de datos SQLite   |
| **Pydantic**       | Validación y modelado de datos con `BaseModel` |
| **Jinja2**         | Motor de plantillas para vistas HTML           |
| **Pathlib**        | Gestión de rutas y archivos                    |
| **datetime**       | Manipulación de fechas y horas                 |
| **Enum**           | Definición de roles (`RolEnum`)                |
| **IntegrityError** | Manejo de errores de integridad en la BD       |

---

## 🛠️ Funcionalidad

- 🔒 **Autenticación**  
  Login y logout con cookies HTTP-only
- 📝 **Registro de usuarios**  
  Formularios con validación de campos y control de errores
- ✅ **Gestión de tareas**  
  Crear, asignar, actualizar estado y eliminar
- 👥 **Administración de usuarios**  
  Listar, buscar, cambiar roles y bloquear/desbloquear
- 📊 **Dashboards personalizados**  
  Vistas adaptadas a cada rol (admin, profesor, alumno)

---

## 📁 Estructura del Proyecto

```text
TaskGenie/
├── .env # 🔒 Variables de entorno
├── .gitignore # 🚫 Archivos ignorados
├── requirements.txt # 📦 Dependencias del proyecto
├── **init**.py # 🧩 Inicializador de módulo
├── auth.py # 🔑 Autenticación de usuarios
├── config.py # ⚙️ Configuración de entorno
├── database.py # 🗄️ Conexión y gestión de BD
├── main.py # 🚀 Punto de entrada de la aplicación
├── models.py # 📜 Modelos SQLAlchemy
├── schemas.py # 📊 Esquemas Pydantic
├── README.md # 📖 Documentación del proyecto
├── routers/ # 📌 Endpoints organizados por funcionalidad
│----├── **init**.py # 🧩 Inicializador de rutas
│----├── admin.md # 📄 Documentación de administración
│----├── admin.py # 👥 Administración de usuarios
│----├── perfil.py # 🧑‍💼 Información del perfil
│----├── tareas.py # ✅ Gestión de tareas
│----└── usuarios.py # 🔍 Registro y búsqueda de usuarios
├── services/ # 🔧 Lógica de negocio y servicios
│----└── auth_service.py # 🛠️ Servicio de autenticación
└── templates/ # 🎨 Vistas HTML con Jinja2
----├── dashboard.html # 🏠 Dashboard general
----├── dashboard_admin.html # 👑 Panel de administrador
----├── dashboard_profesor.html # 🧑‍🏫 Panel de profesor
----├── dashboard_alumno.html # 👨‍🎓 Panel de alumno
----├── errores.html # ❌ Página de errores
----├── index.html # 🔑 Formulario de login
----├── login.html # 🎫 Vista de login
----└── registro.html # 📝 Formulario de registro
```

---

## 📆 Contexto Formativo

Este proyecto forma parte de **LABORLAN VI 2025: Programación Web con Especialización en IA y Python**, una iniciativa de **DEMA** (Agencia Foral de Empleo y Emprendimiento de Bizkaia) en colaboración con **GAIA**, que conecta talento y empresas tecnológicas. El programa combina teoría y práctica para impulsar la empleabilidad en el sector TIC.

---

## 👨‍💼 Equipo

- **Instructor:** [Aitor Donado](https://github.com/Aitor-Donado)
- **Participante-Desarrollador:** [Américo Carrillo](https://github.com/amejosecar)

---

## 📊 Características

✅ Registro de usuarios con datos completos (nombre, email, fecha de nacimiento, rol)  
✅ Validación automática de formularios y control de errores (duplicidad, formato)  
✅ Selección de rol mediante lista desplegable (admin, profesor, alumno)  
✅ Dashboards interactivos con tablas dinámicas  
✅ Cambio de rol y estado (bloqueo) desde la interfaz  
✅ Búsqueda de usuarios por email con resultados instantáneos  
✅ Vistas diferenciadas por rol

---

## 🛠️ Tecnologías Utilizadas

- **Backend**:  
  ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)  
  ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)

- **Base de datos**:  
  ![SQLite](https://img.shields.io/badge/SQLite-07405E?logo=sqlite&logoColor=white)  
  ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-13656B?logo=sqlalchemy&logoColor=white)

- **Validación**:  
  ![Pydantic](https://img.shields.io/badge/Pydantic-009688?logo=pydantic&logoColor=white)

- **Plantillas**:  
  ![Jinja2](https://img.shields.io/badge/Jinja2-B41717?logo=jinja&logoColor=white)

- **Frontend**:  
  ![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)  
  ![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)  
  ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)

- **Iconos**:  
  ![Font Awesome](https://img.shields.io/badge/Font%20Awesome-05122A?logo=font-awesome&logoColor=white)

- **Utilidades**:  
  ![Pathlib](https://img.shields.io/badge/Pathlib-F4BB44?logo=python&logoColor=white)  
  ![Datetime](https://img.shields.io/badge/Datetime-FFCC00?logo=python&logoColor=white)

---

## 🔧 Cómo Usar

1. Clona el repositorio

   ```bash
   git clone https://github.com/amejosecar/TaskGenie.git
   cd TaskGenie

   ```

2. Instala dependencias
   pip install -r requirements.txt

3. Ejecuta la app
   uvicorn main:app --reload

4. Abre tu navegador en http://127.0.0.1:8000
