# app/blueprints/profe/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class AsignarTareaForm(FlaskForm):
    """
    Formulario para que el profesor asigne una nueva tarea a un alumno.
    """
    titulo = StringField(
        "Título",
        validators=[
            DataRequired(message="El título es obligatorio."),
            Length(max=100, message="Máximo 100 caracteres.")
        ]
    )
    descripcion = TextAreaField(
        "Descripción",
        validators=[
            Length(max=500, message="Máximo 500 caracteres.")
        ]
    )
    fecha_entrega = DateField(
        "Fecha de entrega",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La fecha de entrega es obligatoria.")]
    )
    importancia_id = SelectField(
        "Importancia",
        coerce=str,
        validators=[DataRequired(message="Debes seleccionar un nivel de importancia.")]
    )
    asignado_a_id = SelectField(
        "Asignar a (Alumno)",
        coerce=int,
        validators=[DataRequired(message="Debes seleccionar un alumno.")]
    )
    submit = SubmitField("Asignar tarea")


class CalificarTareaForm(FlaskForm):
    """
    Formulario para que el profesor califique una tarea existente.
    """
    texto_calificado = TextAreaField(
        "Texto de la calificación",
        validators=[DataRequired(message="Debes escribir tu valoración.")]
    )
    puntuacion_calificado = IntegerField(
        "Puntuación",
        validators=[
            DataRequired(message="La puntuación es obligatoria."),
            NumberRange(min=0, max=10, message="La puntuación debe estar entre 0 y 10.")
        ]
    )
    fecha_calificado = DateField(
        "Fecha de calificación",
        format="%Y-%m-%d",
        validators=[DataRequired(message="Debes indicar la fecha de calificación.")]
    )
    submit = SubmitField("Guardar calificación")
