from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from flask import jsonify

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({'message': 'Acesso não autorizado'}), 403
        return f(*args, **kwargs)
    return decorated_function

def seller_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.role not in ['admin', 'seller']:
            return jsonify({'message': 'Acesso não autorizado'}), 403
        return f(*args, **kwargs)
    return decorated_function 