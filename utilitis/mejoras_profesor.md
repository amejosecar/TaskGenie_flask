# Plan de Implementación – Workflow PROFESOR

A continuación tienes el paso a paso con nombres de archivos y acciones (sin código).

---

## 1. Modelos y Migraciones

### 1.1 Modificar `app/models.py`

✅ Listo

- Añadir nuevas clases ORM:
  - **Importancia** (tabla `tb_importancia`)
  - **EstadoTarea** (tabla `tb_estado_tarea`)
  - **TareaCalificada** (tabla `tb_tarea_calificada`)
- Extender el modelo **Tarea**:
  - `importancia_id` → FK a `tb_importancia`
  - `estado_id` → FK a `tb_estado_tarea`
  - `fecha_entrega` → `db.Column(db.Date)`
  - `asignado_a_id` → FK a `usuarios.id` (alumno)
  - `calificacion_id`→ FK a `tb_tarea_calificada.cod_id_califica` (opcional)

### 1.2 Generar y aplicar migración

```bash
flask db migrate -m "Añade tablas Importancia, EstadoTarea, TareaCalificada y campos a Tarea"
# -> revisar y ajustar script en migrations/versions/…
flask db upgrade
```

2.  Servicios y Lógica de Negocio
    2.1 Crear app/services/tarea_service.py
    asignar_tarea(...)

         Crea un registro en Tarea con:

         completada=False

         fecha_creacion=date.today()

         FK de importancia, estado, asignado_a

         Crea un registro inicial en TareaCalificada con estatus_calificado='no'

         calificar_tarea(tarea_id, texto, puntuacion, fecha)

         Verifica que el usuario sea PROFESOR

         Actualiza el registro de TareaCalificada:

         Asigna texto_calificado, puntuacion_calificado, fecha_calificado

         Cambia estatus_calificado a 'si'

3.  Rutas y Blueprints
    3.1 Nuevo Blueprint profe
    app/blueprints/profe/**init**.py

         app/blueprints/profe/routes.py

         GET /POST /profe/nueva → Formulario de asignación de tarea

         GET /profe/listado → Tabla de tareas pendientes de calificar

         GET /POST /profe/calificar/<tarea_id> → Formulario de calificación

3.2 Ajustar create_app() en app/**init**.py
Al hacer login, si current_user.rol == 'PROFESOR', redirigir automáticamente a /profe/listado

4.  Formularios WTForms
    4.1 Crear app/blueprints/profe/forms.py
    AsignarTareaForm

         Campos: titulo, descripcion, fecha_entrega (DateField), importancia (SelectField), asignado_a (SelectField)

         CalificarTareaForm

         Campos: texto_calificado (TextAreaField), puntuacion_calificado (IntegerField), fecha_calificado (DateField)

5.  Plantillas Jinja2
    5.1 Estructura de carpetas
    app/blueprints/profe/templates/profe/
    ├── profe_nueva.html
    ├── profe_listado.html
    └── profe_calificar.html
    5.2 profe_nueva.html
    Renderiza AsignarTareaForm

Incluye menú PROFESOR:

    | Ingresar tarea | Listar tareas | Mi perfil | Cerrar sesión |

5.3 profe_listado.html
Renderiza una tabla con columnas:

    | Título | Descripción | Asignado a | Fecha Entrega |
    | Importancia | Completada | Fecha Creación | Estatus Calificado | Acción (Calificar) |
    Filtra solo tareas con estatus_calificado == 'no'

5.4 profe_calificar.html
Muestra en solo lectura los datos de la tarea

Renderiza CalificarTareaForm para introducir la calificación

6. Navegación y Roles
   Modificar app/templates/base.html

   Detectar current_user.rol == 'PROFESOR' y mostrar el menú específico de rutas /profe/\*

7. Pruebas Manuales
   Crear dos usuarios: uno con rol PROFESOR y otro ALUMNO

   Loguear como PROFESOR → acceder a /profe/listado (debería estar vacío)

   Asignar una nueva tarea → verificar que aparece en /profe/listado

   Calificar la tarea → verificar que desaparece del listado

   Loguear como ALUMNO → acceder a /tareas y comprobar que la tarea existe (con su estado)

Con estos pasos y archivos descritos en markdown, tu flujo de trabajo PROFESOR quedará implementado de manera ordenada y legible. 🚀
