from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from app.decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# Rota principal do admin
@admin_bp.route('/')
@login_required
@admin_required
def painel_admin():
    return redirect(url_for('admin.dashboard'))


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')


from app.routes.admin import produtos
from app.routes.admin import categorias
from app.routes.admin import pedidos