from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_jwt_extended import decode_token
from app import db
from app.models.user import User
from functools import wraps
import jwt

socketio = SocketIO()

def authenticated_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not hasattr(flask.request, 'user'):
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@socketio.on('connect')
def handle_connect():
    token = flask.request.args.get('token')
    try:
        decoded = decode_token(token)
        user_id = decoded['sub']
        user = User.query.get(user_id)
        if user:
            flask.request.user = user
            join_room(f'user_{user_id}')
            if user.role in ['admin', 'manager']:
                join_room('admin_room')
            emit('connected', {'status': 'success'})
        else:
            raise Exception('User not found')
    except:
        return False

@socketio.on('disconnect')
def handle_disconnect():
    if hasattr(flask.request, 'user'):
        leave_room(f'user_{flask.request.user.id}')
        if flask.request.user.role in ['admin', 'manager']:
            leave_room('admin_room')

def broadcast_order_update(order):
    """Transmite atualizações de pedidos"""
    data = {
        'order_id': order.id,
        'status': order.status,
        'updated_at': order.updated_at.isoformat()
    }
    
    # Notificar cliente
    emit('order_status_update', data, room=f'user_{order.client_id}')
    
    # Notificar admins
    emit('order_status_update', data, room='admin_room')

def broadcast_stock_alert(product):
    """Transmite alertas de estoque"""
    data = {
        'product_id': product.id,
        'name': product.name,
        'current_stock': product.stock_quantity,
        'min_stock': product.min_stock
    }
    emit('stock_alert', data, room='admin_room')

def broadcast_notification(user_id, notification):
    """Transmite notificações personalizadas"""
    emit('new_notification', notification, room=f'user_{user_id}') 