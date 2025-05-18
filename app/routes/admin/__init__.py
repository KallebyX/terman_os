from flask import Blueprint

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

from app.routes.admin import produtos
from app.routes.admin import categorias
from app.routes.admin import pedidos