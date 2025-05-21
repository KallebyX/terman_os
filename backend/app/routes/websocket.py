from flask import Blueprint
from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.websocket import socketio
from app.models.user import User
from app.models.notification import Notification
from datetime import datetime

bp = Blueprint('websocket', __name__)

@socketio.on('join_pdv')
@jwt_required()
def handle_join_pdv(data):
    """Vendedor entra na sala do PDV"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role in ['admin', 'seller']:
        join_room('pdv_room')
        emit('pdv_joined', {'status': 'success'})
    else:
        emit('pdv_joined', {'status': 'error', 'message': 'Unauthorized'})

@socketio.on('leave_pdv')
def handle_leave_pdv():
    """Vendedor sai da sala do PDV"""
    leave_room('pdv_room')
    emit('pdv_left', {'status': 'success'})

@socketio.on('new_order')
def handle_new_order(data):
    """Notifica sobre novo pedido"""
    emit('order_notification', data, room='pdv_room')

@socketio.on('stock_update')
def handle_stock_update(data):
    """Notifica sobre atualização de estoque"""
    emit('stock_notification', data, room='pdv_room')

def notify_user(user_id, title, message, type='info'):
    """Envia notificação para um usuário específico"""
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=type,
        created_at=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    emit('notification', {
        'id': notification.id,
        'title': title,
        'message': message,
        'type': type,
        'created_at': notification.created_at.isoformat()
    }, room=f'user_{user_id}')

def notify_admins(title, message, type='info'):
    """Envia notificação para todos os administradores"""
    admin_users = User.query.filter_by(role='admin').all()
    
    for admin in admin_users:
        notify_user(admin.id, title, message, type) 