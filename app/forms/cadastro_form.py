from wtforms import ValidationError
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class CadastroForm(FlaskForm):
    nome = StringField('Nome completo', validators=[DataRequired(), Length(min=3)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar senha', validators=[
        DataRequired(), EqualTo('senha', message='As senhas devem coincidir.')
    ])

    def validate_nome(self, field):
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', field.data):
            raise ValidationError('O nome deve conter apenas letras e espaços.')