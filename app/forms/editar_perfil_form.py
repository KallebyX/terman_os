from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Optional

class EditarPerfilForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Nova Senha', validators=[Optional()])
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[
        EqualTo('senha', message='As senhas devem coincidir'),
        Optional()
    ])
    submit = SubmitField('Salvar Alterações')