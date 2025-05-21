from flask import Blueprint

pdv_bp = Blueprint('pdv', __name__, url_prefix='/pdv')

from . import routes
