from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import RolEnum

class RegisterForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    apellido = StringField("Apellido", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    fecha_nacimiento = DateField(
        "Fecha de Nacimiento", 
        format="%Y-%m-%d", 
        validators=[DataRequired()]
    )
    rol = SelectField(
        "Rol", 
        choices=[(role.name, role.value) for role in RolEnum],
        validators=[DataRequired()]
    )
    clave = PasswordField("Contraseña", validators=[DataRequired(), EqualTo("confirmar_clave")])
    confirmar_clave = PasswordField("Confirmar Contraseña", validators=[DataRequired()])
    submit = SubmitField("Registrarse")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    clave = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Entrar")
