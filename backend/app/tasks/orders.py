from app import celery, db
from app.models.order import Order, OrderItem
from app.models.product import Product, StockMovement
from app.models.user import User
from datetime import datetime, timedelta
from sqlalchemy import func
import json
from app.utils.notifications import send_email, send_push_notification

@celery.task
def process_order(order_id):
    """Processa um novo pedido"""
    order = Order.query.get(order_id)
    if not order:
        return

    try:
        # Verificar estoque
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product.stock_quantity < item.quantity:
                raise ValueError(f'Estoque insuficiente para {product.name}')

        # Atualizar estoque
        for item in order.items:
            product = Product.query.get(item.product_id)
            product.stock_quantity -= item.quantity
            
            # Registrar movimento de estoque
            movement = StockMovement(
                product_id=product.id,
                type='saída',
                quantity=item.quantity,
                reference=f'Pedido #{order.number}'
            )
            db.session.add(movement)

        order.status = 'processing'
        db.session.commit()

        # Calcular pontos de fidelidade
        from app.tasks.loyalty import calculate_order_points
        calculate_order_points.delay(order.id)

        # Enviar confirmação
        send_order_confirmation.delay(order.id)

        # Verificar estoque baixo
        check_low_stock.delay()

    except Exception as e:
        order.status = 'failed'
        db.session.commit()
        send_order_error_notification.delay(order.id, str(e))
        raise e

@celery.task
def send_order_confirmation(order_id):
    """Envia confirmação do pedido"""
    order = Order.query.get(order_id)
    if not order:
        return

    client = User.query.get(order.client_id)
    if not client:
        return

    # Preparar dados do email
    context = {
        'order_number': order.number,
        'client_name': client.name,
        'total': float(order.total),
        'items': [{
            'product': item.product.name,
            'quantity': item.quantity,
            'price': float(item.price)
        } for item in order.items],
        'created_at': order.created_at.strftime('%d/%m/%Y %H:%M')
    }

    # Enviar email
    send_email(
        to_email=client.email,
        subject=f'Confirmação do Pedido #{order.number}',
        template='order_confirmation',
        context=context
    )

    # Enviar notificação push se disponível
    if client.push_token:
        send_push_notification(
            token=client.push_token,
            title=f'Pedido #{order.number} confirmado',
            body=f'Seu pedido no valor de R$ {float(order.total):.2f} foi confirmado'
        )

@celery.task
def check_low_stock():
    """Verifica produtos com estoque baixo"""
    low_stock_products = Product.query.filter(
        Product.stock_quantity <= Product.min_stock,
        Product.active == True
    ).all()

    if low_stock_products:
        # Notificar administradores
        admins = User.query.filter_by(role='admin').all()
        for admin in admins:
            send_email(
                to_email=admin.email,
                subject='Alerta de Estoque Baixo',
                template='low_stock_alert',
                context={'products': low_stock_products}
            )

@celery.task
def update_order_status(order_id, new_status):
    """Atualiza o status do pedido e envia notificações apropriadas"""
    order = Order.query.get(order_id)
    if not order:
        return

    old_status = order.status
    order.status = new_status

    if new_status == 'completed':
        order.completed_at = datetime.utcnow()
        # Calcular pontos de fidelidade se ainda não calculados
        from app.tasks.loyalty import calculate_order_points
        calculate_order_points.delay(order.id)

    db.session.commit()

    # Enviar notificação apropriada
    client = User.query.get(order.client_id)
    if client:
        status_messages = {
            'processing': 'está sendo processado',
            'shipped': 'foi enviado',
            'completed': 'foi concluído',
            'cancelled': 'foi cancelado'
        }

        message = status_messages.get(new_status, 'foi atualizado')
        
        send_email(
            to_email=client.email,
            subject=f'Atualização do Pedido #{order.number}',
            template='order_status_update',
            context={
                'order_number': order.number,
                'old_status': old_status,
                'new_status': new_status,
                'message': message
            }
        )

@celery.task
def generate_daily_sales_report():
    """Gera relatório diário de vendas"""
    yesterday = datetime.utcnow() - timedelta(days=1)
    start_of_day = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Buscar dados de vendas
    sales_data = db.session.query(
        func.count(Order.id).label('total_orders'),
        func.sum(Order.total).label('total_revenue'),
        func.avg(Order.total).label('average_order_value')
    ).filter(
        Order.created_at.between(start_of_day, end_of_day),
        Order.status == 'completed'
    ).first()

    # Produtos mais vendidos
    top_products = db.session.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_quantity'),
        func.sum(OrderItem.quantity * OrderItem.price).label('total_revenue')
    ).join(
        OrderItem, Product.id == OrderItem.product_id
    ).join(
        Order, OrderItem.order_id == Order.id
    ).filter(
        Order.created_at.between(start_of_day, end_of_day),
        Order.status == 'completed'
    ).group_by(
        Product.id
    ).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(10).all()

    report_data = {
        'date': yesterday.date().isoformat(),
        'total_orders': sales_data.total_orders or 0,
        'total_revenue': float(sales_data.total_revenue or 0),
        'average_order_value': float(sales_data.average_order_value or 0),
        'top_products': [{
            'name': product.name,
            'quantity': product.total_quantity,
            'revenue': float(product.total_revenue)
        } for product in top_products]
    }

    # Enviar relatório para administradores
    admins = User.query.filter_by(role='admin').all()
    for admin in admins:
        send_email(
            to_email=admin.email,
            subject=f'Relatório de Vendas - {yesterday.strftime("%d/%m/%Y")}',
            template='daily_sales_report',
            context=report_data
        )

    return report_data 