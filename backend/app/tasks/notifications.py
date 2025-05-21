from app import celery
from app.models.user import User
from app.utils.notifications import send_email, send_push_notification
from datetime import datetime, timedelta

@celery.task
def send_abandoned_cart_reminder():
    """Envia lembretes para carrinhos abandonados"""
    threshold = datetime.utcnow() - timedelta(hours=24)
    
    # Implementar lógica de carrinho abandonado
    # Este é um exemplo básico que pode ser expandido conforme necessário
    abandoned_carts = Cart.query.filter(
        Cart.updated_at <= threshold,
        Cart.status == 'active'
    ).all()

    for cart in abandoned_carts:
        user = User.query.get(cart.user_id)
        if user:
            send_email(
                to_email=user.email,
                subject='Não esqueça seus produtos!',
                template='abandoned_cart',
                context={
                    'user_name': user.name,
                    'cart_items': cart.items
                }
            )

@celery.task
def send_price_drop_notification(product_id, old_price, new_price):
    """Notifica usuários interessados sobre queda de preço"""
    from app.models.product import Product, ProductAlert
    
    product = Product.query.get(product_id)
    if not product:
        return

    # Buscar usuários que registraram interesse no produto
    alerts = ProductAlert.query.filter_by(
        product_id=product_id,
        active=True
    ).all()

    for alert in alerts:
        user = User.query.get(alert.user_id)
        if user:
            send_email(
                to_email=user.email,
                subject=f'O preço do {product.name} caiu!',
                template='price_drop',
                context={
                    'product_name': product.name,
                    'old_price': float(old_price),
                    'new_price': float(new_price),
                    'discount_percentage': ((old_price - new_price) / old_price) * 100
                }
            )

@celery.task
def send_restock_notification(product_id):
    """Notifica usuários quando um produto volta ao estoque"""
    from app.models.product import Product, ProductAlert
    
    product = Product.query.get(product_id)
    if not product:
        return

    alerts = ProductAlert.query.filter_by(
        product_id=product_id,
        alert_type='restock',
        active=True
    ).all()

    for alert in alerts:
        user = User.query.get(alert.user_id)
        if user:
            send_email(
                to_email=user.email,
                subject=f'{product.name} está de volta!',
                template='restock_alert',
                context={
                    'product_name': product.name,
                    'price': float(product.price)
                }
            )
            
            # Desativar o alerta após enviar a notificação
            alert.active = False

    db.session.commit() 