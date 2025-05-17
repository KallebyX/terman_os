from flask import Blueprint, render_template

conteudo_bp = Blueprint('conteudo', __name__)

@conteudo_bp.route('/')
def dicas():
    return render_template('conteudo.html')