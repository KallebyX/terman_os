from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.product import Product, Category, StockMovement
from app.models.order import Order
from app import db
from app.utils.permissions import admin_required
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('admin', __name__)

@bp.route('/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard():
    today = datetime.utcnow().date()
    start_of_month = today.replace(day=1)

    # Métricas de vendas
    daily_sales = db.session.query(func.sum(Order.total)).filter(
        func.date(Order.created_at) == today,
        Order.status == 'completed'
    ).scalar() or 0

    monthly_sales = db.session.query(func.sum(Order.total)).filter(
        Order.created_at >= start_of_month,
        Order.status == 'completed'
    ).scalar() or 0

    # Produtos com estoque baixo
    low_stock_products = Product.query.filter(
        Product.stock_quantity <= Product.min_stock
    ).count()

    # Novos clientes
    new_customers = User.query.filter(
        User.role == 'client',
        User.created_at >= start_of_month
    ).count()

    return jsonify({
        'daily_sales': float(daily_sales),
        'monthly_sales': float(monthly_sales),
        'low_stock_products': low_stock_products,
        'new_customers': new_customers
    })

@bp.route('/reports/sales', methods=['GET'])
@jwt_required()
@admin_required
def sales_report():
    start_date = request.args.get('start_date', type=datetime)
    end_date = request.args.get('end_date', type=datetime)
    group_by = request.args.get('group_by', 'day')

    query = db.session.query(
        func.date(Order.created_at).label('date'),
        func.sum(Order.total).label('total'),
        func.count(Order.id).label('count')
    ).filter(Order.status == 'completed')

    if start_date:
        query = query.filter(Order.created_at >= start_date)
    if end_date:
        query = query.filter(Order.created_at <= end_date)

    if group_by == 'month':
        query = query.group_by(func.date_trunc('month', Order.created_at))
    else:
        query = query.group_by(func.date(Order.created_at))

    results = query.all()

    return jsonify({
        'data': [{
            'date': result.date.isoformat(),
            'total': float(result.total),
            'count': result.count
        } for result in results]
    })

@bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def list_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    role = request.args.get('role')

    query = User.query

    if role:
        query = query.filter(User.role == role)

    users = query.paginate(page=page, per_page=per_page)

    return jsonify({
        'items': [user.to_dict() for user in users.items],
        'total': users.total,
        'pages': users.pages,
        'current_page': page
    })

@bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'role' in data:
        user.role = data['role']
    if 'active' in data:
        user.active = data['active']
    if 'password' in data:
        user.set_password(data['password'])

    db.session.commit()

    return jsonify(user.to_dict())

@bp.route('/inventory/movements', methods=['POST'])
@jwt_required()
@admin_required
def create_stock_movement():
    data = request.get_json()
    product = Product.query.get_or_404(data['product_id'])

    movement = StockMovement(
        product_id=product.id,
        type=data['type'],
        quantity=data['quantity'],
        reference=data.get('reference'),
        notes=data.get('notes')
    )

    if movement.type == 'entrada':
        product.stock_quantity += movement.quantity
    elif movement.type == 'saída':
        if product.stock_quantity < movement.quantity:
            return jsonify({'message': 'Estoque insuficiente'}), 400
        product.stock_quantity -= movement.quantity

    db.session.add(movement)
    db.session.commit()

    return jsonify({
        'message': 'Movimentação registrada com sucesso',
        'current_stock': product.stock_quantity
    })

@bp.route('/reports/inventory', methods=['GET'])
@jwt_required()
@admin_required
def inventory_report():
    category_id = request.args.get('category_id', type=int)
    
    query = db.session.query(
        Product,
        func.sum(StockMovement.quantity).label('total_movements')
    ).outerjoin(StockMovement)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    query = query.group_by(Product.id)

    results = query.all()

    return jsonify({
        'products': [{
            **product.to_dict(),
            'total_movements': total_movements or 0
        } for product, total_movements in results]
    })

@bp.route('/reports/financial', methods=['GET'])
@jwt_required()
@admin_required
def financial_report():
    start_date = request.args.get('start_date', type=datetime)
    end_date = request.args.get('end_date', type=datetime)

    # Receita total
    revenue_query = db.session.query(func.sum(Order.total)).filter(
        Order.status == 'completed'
    )

    # Custo total
    cost_query = db.session.query(
        func.sum(OrderItem.quantity * Product.cost_price)
    ).join(
        Order, OrderItem.order_id == Order.id
    ).join(
        Product, OrderItem.product_id == Product.id
    ).filter(
        Order.status == 'completed'
    )

    if start_date:
        revenue_query = revenue_query.filter(Order.created_at >= start_date)
        cost_query = cost_query.filter(Order.created_at >= start_date)
    if end_date:
        revenue_query = revenue_query.filter(Order.created_at <= end_date)
        cost_query = cost_query.filter(Order.created_at <= end_date)

    total_revenue = revenue_query.scalar() or 0
    total_cost = cost_query.scalar() or 0
    gross_profit = total_revenue - total_cost
    margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0

    return jsonify({
        'total_revenue': float(total_revenue),
        'total_cost': float(total_cost),
        'gross_profit': float(gross_profit),
        'margin': float(margin)
    }) 