from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.order import Order, OrderItem
from app.models.product import Product
from app import db
from datetime import datetime
import uuid

bp = Blueprint('pdv', __name__)

@bp.route('/create-order', methods=['POST'])
@jwt_required()
def create_order():
    seller_id = get_jwt_identity()
    data = request.get_json()

    # Validar produtos e estoque
    for item in data['items']:
        product = Product.query.get(item['product_id'])
        if not product:
            return jsonify({'message': f'Produto {item["product_id"]} não encontrado'}), 404
        if product.stock_quantity < item['quantity']:
            return jsonify({'message': f'Estoque insuficiente para {product.name}'}), 400

    # Criar pedido
    order = Order(
        number=str(uuid.uuid4().hex[:8].upper()),
        client_id=data.get('client_id'),
        seller_id=seller_id,
        payment_method=data['payment_method']
    )

    # Adicionar itens
    for item_data in data['items']:
        product = Product.query.get(item_data['product_id'])
        item = OrderItem(
            product_id=product.id,
            quantity=item_data['quantity'],
            price=product.price,
            discount=item_data.get('discount', 0)
        )
        order.items.append(item)
        
        # Atualizar estoque
        product.stock_quantity -= item_data['quantity']

    order.total = order.calculate_total()
    
    db.session.add(order)
    db.session.commit()

    return jsonify(order.to_dict()), 201

@bp.route('/orders', methods=['GET'])
@jwt_required()
def list_orders():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    query = Order.query.order_by(Order.created_at.desc())
    
    # Filtros
    status = request.args.get('status')
    if status:
        query = query.filter(Order.status == status)
    
    date = request.args.get('date')
    if date:
        query = query.filter(db.func.date(Order.created_at) == date)

    pagination = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'items': [order.to_dict() for order in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }) 