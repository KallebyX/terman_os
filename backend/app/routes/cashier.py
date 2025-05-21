from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.cashier import CashierSession, CashierTransaction
from app.utils.permissions import manager_required
from app import db
from datetime import datetime

bp = Blueprint('cashier', __name__)

@bp.route('/open', methods=['POST'])
@jwt_required()
@manager_required
def open_cashier():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Verificar se já existe um caixa aberto
    active_session = CashierSession.query.filter_by(
        status='open'
    ).first()

    if active_session:
        return jsonify({
            'message': 'Já existe um caixa aberto'
        }), 400

    session = CashierSession(
        user_id=user_id,
        initial_amount=data['initial_amount'],
        opened_at=datetime.utcnow(),
        status='open'
    )

    db.session.add(session)
    db.session.commit()

    return jsonify({
        'message': 'Caixa aberto com sucesso',
        'session_id': session.id
    })

@bp.route('/close', methods=['POST'])
@jwt_required()
@manager_required
def close_cashier():
    data = request.get_json()
    user_id = get_jwt_identity()

    active_session = CashierSession.query.filter_by(
        status='open'
    ).first()

    if not active_session:
        return jsonify({
            'message': 'Não há caixa aberto'
        }), 400

    # Calcular resumo final
    summary = active_session.calculate_summary()

    active_session.final_amount = data['final_amount']
    active_session.closed_at = datetime.utcnow()
    active_session.status = 'closed'
    active_session.difference = float(data['final_amount']) - summary['expected_amount']

    db.session.commit()

    return jsonify({
        'message': 'Caixa fechado com sucesso',
        'summary': summary,
        'difference': float(active_session.difference)
    })

@bp.route('/status', methods=['GET'])
@jwt_required()
def get_status():
    active_session = CashierSession.query.filter_by(
        status='open'
    ).first()

    if not active_session:
        return jsonify({
            'status': 'closed'
        })

    summary = active_session.calculate_summary()

    return jsonify({
        'status': 'open',
        'session_id': active_session.id,
        'opened_at': active_session.opened_at.isoformat(),
        'initial_amount': float(active_session.initial_amount),
        'summary': summary
    })

@bp.route('/transaction', methods=['POST'])
@jwt_required()
@manager_required
def add_transaction():
    data = request.get_json()
    user_id = get_jwt_identity()

    active_session = CashierSession.query.filter_by(
        status='open'
    ).first()

    if not active_session:
        return jsonify({
            'message': 'Não há caixa aberto'
        }), 400

    transaction = CashierTransaction(
        session_id=active_session.id,
        type=data['type'],
        amount=data['amount'],
        description=data.get('description'),
        created_by_id=user_id
    )

    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        'message': 'Transação registrada com sucesso',
        'transaction_id': transaction.id
    }) 