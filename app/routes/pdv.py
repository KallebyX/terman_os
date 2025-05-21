from flask import Blueprint, render_template
from flask_login import login_required, current_user

pdv_bp = Blueprint('pdv', __name__, url_prefix='/pdv')

@pdv_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.tipo_usuario != 'funcionario':
        return "Acesso restrito ao PDV", 403
    return render_template('pdv/dashboard.html', usuario=current_user)
