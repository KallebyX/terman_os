from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db
from datetime import datetime

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Dados inválidos'}), 400

    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Email ou senha inválidos'}), 401

    if not user.active:
        return jsonify({'message': 'Usuário inativo'}), 401

    user.last_login = datetime.utcnow()
    db.session.commit()

    return jsonify({
        'access_token': create_access_token(identity=user.id),
        'refresh_token': create_refresh_token(identity=user.id),
        'user': user.to_dict()
    })

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    return jsonify({
        'access_token': create_access_token(identity=identity)
    })

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify(user.to_dict())

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email já cadastrado'}), 400

    user = User(
        email=data['email'],
        name=data['name'],
        role='client'
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'Usuário registrado com sucesso',
        'user': user.to_dict()
    }), 201 