# Plan de Implementación – Workflow PROFESOR

Paso Descripción Explicación Estado
1.1 Modificar app/models.py Se definieron correctamente las clases Importancia, EstadoTarea, TareaCalificada y se extendió Tarea con las FKs necesarias. ✅
1.2 Generar y aplicar migración El archivo 06009f2cb2b5*initial_schema_usuarios_tareas*.py existe y refleja los cambios. ✅
2.1 Crear tarea_service.py Contiene asignar_tarea() y calificar_tarea() con validaciones, relaciones y commits. ✅
3.1 Blueprint profe con rutas routes.py define /nueva, /listado, /calificar/<id> y usa solo_profe. ✅
3.2 Redirección tras login En auth/routes.py, si el rol es PROFESOR, redirige a profe.listado. ✅
4.1 Formularios WTForms forms.py define AsignarTareaForm y CalificarTareaForm con validaciones y campos correctos. ✅
5.1 Estructura de plantillas Existen nueva.html, listado.html, calificar.html en templates/profe/. ✅
5.2 profe_nueva.html Renderiza AsignarTareaForm con helpers WTForms. El menú está en base.html. ✅
5.3 profe_listado.html Muestra tabla de tareas con estatus_calificado == 'no' y link a calificar. ✅
5.4 profe_calificar.html Muestra datos de tarea y renderiza CalificarTareaForm. ✅
6 Navegación y roles base.html detecta rol == 'PROFESOR' y muestra menú con /profe/listado. ✅
7 Pruebas manuales No hay evidencia en el código de pruebas automatizadas o fixtures de prueba. ❌
