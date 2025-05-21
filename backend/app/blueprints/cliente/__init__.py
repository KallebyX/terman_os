from flask import Blueprint

cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')

from . import routes
