from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from app.models.user import User
from . import api_bp

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': 'Credenciais inválidas'}), 401
        
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'email': user.email,
            'nome': user.nome,
            'tipo': user.tipo
        }
    }) 