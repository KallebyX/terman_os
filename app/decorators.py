from flask_login import current_user
from flask import abort
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo_usuario != 'admin':
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function