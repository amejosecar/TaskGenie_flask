# app/blueprints/tareas/forms.py
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired

class ActualizarTareaForm(FlaskForm):
    detalle_alumno = TextAreaField(
        "Tu respuesta",
        validators=[DataRequired(message="El detalle es obligatorio")]
    )
    estado_id = SelectField(
        "Estado",
        choices=[
            ("04", "En desarrollo"),
            ("02", "Completada")
        ],
        validators=[DataRequired(message="Debes elegir un estado")]
    )
    submit = SubmitField("Guardar")
