from flask_login import current_user
from flask import abort
from functools import wraps


def admin_required(f):
    """Requer que o usuario seja admin ou super_admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(403)
        if current_user.tipo_usuario not in ['admin', 'super_admin']:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


def super_admin_required(f):
    """Requer que o usuario seja super_admin - acesso total ao sistema"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(403)
        if current_user.tipo_usuario != 'super_admin':
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function