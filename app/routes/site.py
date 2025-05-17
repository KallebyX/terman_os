from flask import Blueprint, render_template

site_bp = Blueprint('site', __name__)

@site_bp.route('/')
def homepage():
    return render_template('index.html')

@site_bp.route('/sobre')
def sobre_nos():
    return render_template('sobre.html')

@site_bp.route('/contato', methods=['GET', 'POST'])
def contato():
    return render_template('contato.html')