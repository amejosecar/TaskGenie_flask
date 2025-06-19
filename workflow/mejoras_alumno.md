## Modelo de workflow del alumno

    1.- Un alumno puede listar todas sus tareas sin importar el estado de la tarea
    2.- Un alumno puede editar su tarea con el estado asignado
        2.1- agregar comentarios sobre su tarea
        2.2- puede guardar su tarea con el estado desarrollo, cuando guarda su tarea con el
             estado en desarrollo y la app asgina por defecto la fecha que guardo su tarea
    3.- Un alumno puede guardar su tarea con el estado completado y la app asgina por defecto la fecha que guardo su tarea
    4.- Un alumno solo puede visualizar las tareas completadas (NO PUEDE EDITARLA)
    5.- al momento de ingresar un alumno a la app, debe visualizar todas sus tareas
    6.- crear un campo en la tabla tb_tarea_calificada, con el nombre detalle_alumno y fecha_detalle_alumno, para que el alumno agregue su respuestas de la tarea
    7.- crear un nuevo valor en la tabla tb_estado_tarea
        cod_id = 04
        dsc_estado_tarea = "en desarrollo"
    8.- crear todos los archivos py y html que haga faltan para implementar el workflow
    9.- moficar todos los archivos py y html que haga faltan para implementar el workflow

    actividad: crear un plan de trabajo para ejecutar toda esta actividad, no incluyas codigo, elabora un cuadro paso a paso con una columna que se llame explicacion


    # 🎓 Workflow del Alumno – Plan de Trabajo

| Paso | Acción                                                        | Explicación                                                                                                                      |
| :--: | :------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------- |
|  1️⃣  | Listar todas las tareas                                       | Asegurar que la vista de “Mis Tareas” muestra **todos** los registros (sin filtrar por estado).                                  |
|  2️⃣  | Permitir edición sólo si el estado = “asignado”               | Ajustar lógica en ruta de edición para que compruebe el estado de la tarea antes de renderizar el formulario.                    |
| 2.1  | Añadir campo de comentarios                                   | Extender el formulario de edición para que el alumno pueda escribir “comentarios” sobre su propia tarea.                         |
| 2.2  | Guardar “en desarrollo” + asignar fecha                       | Al enviar en estado “en desarrollo”, fijar automáticamente la fecha de guardado y asignar el nuevo estado.                       |
|  3️⃣  | Guardar como “completado” + asignar fecha                     | Igual que el anterior pero con estado “completado”: bloquear edición y marcar fecha de entrega.                                  |
|  4️⃣  | Sólo visualizar completadas                                   | En la ruta de detalle, si estado = “completada”, deshabilitar cualquier control de edición.                                      |
|  5️⃣  | Vista inicial de alumno                                       | Configurar home/“Mis Tareas” para que al iniciar sesión el alumno vea directamente **todas** sus tareas.                         |
|  6️⃣  | Nuevo campo `detalle_alumno` en `tb_tarea_calificada`         | Ampliar modelo y migración para guardar la respuesta o desarrollo que el alumno añade a la calificación con su fecha.            |
|  7️⃣  | Nuevo valor en `tb_estado_tarea`: <br>– `04`: “en desarrollo” | Insertar en la tabla de estados el código 04 y su descripción; actualizar seed o migración.                                      |
|  8️⃣  | Crear archivos faltantes (forms, routes, templates)           | Generar el blueprint `alumno/` con sus formularios (`Asignar`, `Editar`, `Detalle`), controladores y vistas HTML.                |
|  9️⃣  | Modificar archivos existentes para integrar el nuevo flujo    | Ajustar `models.py`, servicios, blueprints de `tareas/` y `profe/`, plantillas globales y rutas de login/perfil si es necesario. |

---

# 🗂️ Estructura de Archivos – “Alumno” (nuevos y a modificar)

```text
taskgenie_flask/
├── app/
│   ├── models.py                 ✏️ agregar columna detalle_alumno en TareaCalificada
│   ├── migrations/
│   │   └── versions/
│   │       └── XXXX_add_detalle_alumno_and_estado_desarrollo.py  🆕 migración
│   ├── blueprints/
│   │   ├── tareas/               ✏️ actualizar routes.py (edición según estado)
│   │   │   ├── routes.py         ✏️ lógica de listar, editar, detalle
│   │   │   ├── forms.py          🆕 Extender con campo comentarios
│   │   │   └── templates/
│   │   │       ├── form.html     ✏️ añadir textarea comentarios y botones de estado
│   │   │       ├── listado.html  ✏️ mostrar todas las tareas
│   │   │       └── detalle.html  ✏️ deshabilitar edición si completada
│   │   └── alumno/               🆕 nuevo blueprint para separar lógica de alumno
│   │       ├── __init__.py       🆕 registrar blueprint
│   │       ├── routes.py         🆕 rutas específicas (inicio, editar, detalle)
│   │       ├── forms.py          🆕 formulario de desarrollo y comentarios
│   │       └── templates/
│   │           ├── inicio.html   🆕 vista “Mis Tareas” alumno
│   │           ├── editar.html   🆕 formulario de edición según estado
│   │           └── detalle.html  🆕 vista de sólo lectura para completadas
│   ├── services/
│   │   └── tarea_service.py      ✏️ añadir funciones para cambiar estado y fecha
│   └── templates/
│       └── base.html             ✏️ ajustar nav y enlaces para rol ALUMNO
└── instance/
    └── taskgenie.db             ✏️ BD migrada con nuevo campo y estado
```

# 📋 Pasos para Implementar el Workflow del Alumno

1. **Preparar el entorno y la base de datos**  
   Explicación: Asegura que tu entorno virtual esté activado, instala dependencias y sincroniza la base de datos con las últimas migraciones existentes.

2. **Extender el modelo de calificación**  
   Explicación: Añade en el modelo de `TareaCalificada` el campo `detalle_alumno` y `fehca_detalle_alumno`para que el alumno pueda registrar su respuesta al guardar o editar.

3. **Registrar el nuevo estado “en desarrollo”**  
   Explicación: Inserta en la tabla de estados de tarea el código `04` con la descripción “en desarrollo”, de modo que la aplicación lo reconozca como opción válida.

4. **Crear migración de esquema**

Explicación: Genera y aplica una migración que incluya el nuevo campo `detalle_alumno` y el estado `04` en la tabla de estados, garantizando consistencia en la base de datos.

5. **Actualizar la lógica de negocio**  
   Explicación: Modifica los servicios encargados de crear y actualizar tareas para que, al cambiar a “en desarrollo” o “completado”, se registre automáticamente la fecha de guardado y permita capturar comentarios del alumno.

6. **Ampliar los formularios de tareas**  
   Explicación: Añade al formulario del alumno un espacio para comentarios (`detalle_alumno`) y opciones de estado (“asignado”, “en desarrollo”, “completado”), respetando la secuencia de flujo definida.

7. **Ajustar rutas y controladores de tareas**  
   Explicación: Controla el acceso a la edición según el estado actual (solo “asignado” permite editar), procesa el guardado en “en desarrollo” y “completado” y separa vistas de consulta y edición.

8. **Crear blueprint específico de alumno**  
   Explicación: Estructura un nuevo módulo (blueprint) para encapsular rutas, formularios y plantillas propias del alumno, manteniendo el código organizado y centrado en su rol.

9. **Diseñar plantillas HTML para el alumno**  
   Explicación: Implementa vistas de “Mis Tareas” (listado completo), “Editar Tarea” (con controles según estado) y “Detalle” (solo lectura cuando la tarea esté completada), cuidando la UX.

10. **Ajustar la plantilla base y navegación**  
    Explicación: Adapta el menú y enlaces de navegación para que el rol ALUMNO vea directamente su dashboard de tareas al iniciar sesión y no muestre rutas de administración o profesor.

11. **Probar el flujo completo**  
    Explicación: Realiza pruebas funcionales de extremo a extremo: listar tareas, editar en “asignado”, guardar en “en desarrollo” y “completado”, y validar restricciones de acceso y actualización de fechas.

12. **Validación final y despliegue**  
    Explicación: Verifica en un entorno de staging que todo funcione según el modelo de workflow, recopila feedback de usuarios y despliega los cambios a producción con una copia de seguridad de la base de datos.
