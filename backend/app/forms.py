from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])

class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=3)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', 
                                   validators=[DataRequired(), EqualTo('password')])
    cpf = StringField('CPF', validators=[DataRequired(), Length(11)])
    telefone = StringField('Telefone')
    endereco = StringField('Endereço') 