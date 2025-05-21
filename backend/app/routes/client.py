from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.order import Order
from app.models.user import User
from app.models.loyalty import LoyaltyPoints, LoyaltyReward
from app import db
from datetime import datetime
from sqlalchemy import func

bp = Blueprint('client', __name__)

@bp.route('/orders', methods=['GET'])
@jwt_required()
def get_client_orders():
    client_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')

    query = Order.query.filter_by(client_id=client_id)

    if status:
        query = query.filter_by(status=status)

    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page
    )

    return jsonify({
        'items': [order.to_dict() for order in orders.items],
        'total': orders.total,
        'pages': orders.pages,
        'current_page': page
    })

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    client_id = get_jwt_identity()
    client = User.query.get_or_404(client_id)

    # Calcular estatísticas do cliente
    total_orders = Order.query.filter_by(
        client_id=client_id,
        status='completed'
    ).count()

    total_spent = db.session.query(func.sum(Order.total)).filter_by(
        client_id=client_id,
        status='completed'
    ).scalar() or 0

    last_order = Order.query.filter_by(
        client_id=client_id,
        status='completed'
    ).order_by(Order.created_at.desc()).first()

    return jsonify({
        **client.to_dict(),
        'statistics': {
            'total_orders': total_orders,
            'total_spent': float(total_spent),
            'last_order_date': last_order.created_at.isoformat() if last_order else None,
            'member_since': client.created_at.isoformat()
        }
    })

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    client_id = get_jwt_identity()
    client = User.query.get_or_404(client_id)
    data = request.get_json()

    if 'name' in data:
        client.name = data['name']
    if 'email' in data:
        # Verificar se o email já está em uso
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != client_id:
            return jsonify({'message': 'Email já está em uso'}), 400
        client.email = data['email']
    if 'password' in data:
        client.set_password(data['password'])

    db.session.commit()

    return jsonify({'message': 'Perfil atualizado com sucesso'})

@bp.route('/loyalty', methods=['GET'])
@jwt_required()
def get_loyalty_status():
    client_id = get_jwt_identity()
    
    points = LoyaltyPoints.query.filter_by(client_id=client_id).first()
    if not points:
        points = LoyaltyPoints(client_id=client_id, points=0)
        db.session.add(points)
        db.session.commit()

    # Buscar histórico de pontos
    history = db.session.query(
        Order.created_at,
        Order.total,
        Order.number,
        LoyaltyPoints.points_earned
    ).join(
        LoyaltyPoints, Order.id == LoyaltyPoints.order_id
    ).filter(
        Order.client_id == client_id,
        Order.status == 'completed'
    ).order_by(Order.created_at.desc()).limit(10).all()

    # Buscar recompensas disponíveis
    available_rewards = LoyaltyReward.query.filter(
        LoyaltyReward.points_required <= points.points
    ).all()

    return jsonify({
        'current_points': points.points,
        'history': [{
            'date': item.created_at.isoformat(),
            'order_number': item.number,
            'points_earned': item.points_earned,
            'order_total': float(item.total)
        } for item in history],
        'available_rewards': [{
            'id': reward.id,
            'name': reward.name,
            'description': reward.description,
            'points_required': reward.points_required
        } for reward in available_rewards]
    })

@bp.route('/loyalty/redeem', methods=['POST'])
@jwt_required()
def redeem_reward():
    client_id = get_jwt_identity()
    data = request.get_json()
    reward_id = data.get('reward_id')

    points = LoyaltyPoints.query.filter_by(client_id=client_id).first()
    if not points:
        return jsonify({'message': 'Nenhum ponto disponível'}), 400

    reward = LoyaltyReward.query.get_or_404(reward_id)

    if points.points < reward.points_required:
        return jsonify({'message': 'Pontos insuficientes'}), 400

    # Registrar resgate
    redemption = LoyaltyRedemption(
        client_id=client_id,
        reward_id=reward_id,
        points_used=reward.points_required
    )
    points.points -= reward.points_required

    db.session.add(redemption)
    db.session.commit()

    return jsonify({
        'message': 'Recompensa resgatada com sucesso',
        'remaining_points': points.points
    }) 