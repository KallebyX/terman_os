from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[
        DataRequired(message='Informe seu e-mail.'),
        Email(message='Digite um e-mail válido.')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Digite sua senha.')
    ])
    lembrar = BooleanField('Lembrar-me')