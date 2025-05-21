from celery import shared_task
from flask_mail import Message
from flask import current_app

@shared_task
def send_welcome_email(user_email):
    """Envia email de boas-vindas para novos usuários"""
    with current_app.app_context():
        msg = Message(
            'Bem-vindo ao Terman OS',
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user_email]
        )
        msg.body = 'Obrigado por se cadastrar no Terman OS!'
        current_app.mail.send(msg)
    return f'Email enviado para {user_email}' 