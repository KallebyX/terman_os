from app import celery
from flask_mail import Message
from flask import current_app, render_template

@celery.task
def enviar_email_confirmacao(user_id):
    from app.models.user import User
    
    with current_app.app_context():
        user = User.query.get(user_id)
        if not user:
            return False
            
        msg = Message('Bem-vindo ao Terman OS',
                     sender=current_app.config['MAIL_DEFAULT_SENDER'],
                     recipients=[user.email])
                     
        msg.html = render_template('email/confirmacao.html', user=user)
        current_app.mail.send(msg)
        return True

@celery.task
def enviar_email_pedido(pedido_id):
    from app.models.pedido import Pedido
    
    with current_app.app_context():
        pedido = Pedido.query.get(pedido_id)
        if not pedido:
            return False
            
        msg = Message('Pedido Recebido - Terman OS',
                     sender=current_app.config['MAIL_DEFAULT_SENDER'],
                     recipients=[pedido.cliente.user.email])
                     
        msg.html = render_template('email/pedido.html', pedido=pedido)
        current_app.mail.send(msg)
        return True 