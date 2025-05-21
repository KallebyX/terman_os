from app import celery, db
from app.models.loyalty import LoyaltyPoints, LoyaltyTransaction
from app.models.order import Order
from datetime import datetime, timedelta
from sqlalchemy import func

@celery.task
def calculate_order_points(order_id):
    """Calcula e adiciona pontos de fidelidade para um pedido"""
    order = Order.query.get(order_id)
    if not order or order.status != 'completed':
        return

    # Regras de pontuação
    points_per_currency = 1  # 1 ponto para cada 1 real gasto
    bonus_multiplier = {
        'bronze': 1,
        'silver': 1.2,
        'gold': 1.5,
        'platinum': 2
    }

    loyalty = LoyaltyPoints.query.filter_by(client_id=order.client_id).first()
    if not loyalty:
        loyalty = LoyaltyPoints(client_id=order.client_id)
        db.session.add(loyalty)

    base_points = int(float(order.total) * points_per_currency)
    multiplier = bonus_multiplier.get(loyalty.tier, 1)
    total_points = int(base_points * multiplier)

    loyalty.add_points(
        total_points,
        order_id=order.id,
        description=f'Pontos da compra #{order.number}'
    )
    
    db.session.commit()

@celery.task
def check_tier_upgrades():
    """Verifica e atualiza os níveis de fidelidade dos clientes"""
    loyalty_accounts = LoyaltyPoints.query.all()
    
    for account in loyalty_accounts:
        previous_tier = account.tier
        account.update_tier()
        
        if account.tier != previous_tier:
            # Notificar cliente sobre mudança de nível
            send_tier_change_notification.delay(account.client_id, previous_tier, account.tier)
    
    db.session.commit()

@celery.task
def expire_points():
    """Expira pontos de fidelidade após 12 meses"""
    expiration_date = datetime.utcnow() - timedelta(days=365)
    
    # Buscar transações antigas
    old_transactions = LoyaltyTransaction.query.filter(
        LoyaltyTransaction.created_at < expiration_date,
        LoyaltyTransaction.type == 'credit'
    ).all()

    for transaction in old_transactions:
        if transaction.points > 0:
            loyalty = transaction.loyalty_account
            loyalty.deduct_points(
                transaction.points,
                description='Pontos expirados'
            )

    db.session.commit()

@celery.task
def send_tier_change_notification(client_id, old_tier, new_tier):
    """Envia notificação sobre mudança de nível"""
    # Implementar lógica de notificação (email, push, etc)
    pass

@celery.task
def process_loyalty_redemption(redemption_id):
    """Processa o resgate de recompensas"""
    from app.models.loyalty import LoyaltyRedemption
    
    redemption = LoyaltyRedemption.query.get(redemption_id)
    if not redemption or redemption.status != 'pending':
        return

    try:
        # Verificar disponibilidade da recompensa
        if not redemption.reward.active:
            raise ValueError('Recompensa não está mais disponível')

        # Verificar se o cliente tem pontos suficientes
        loyalty = LoyaltyPoints.query.filter_by(client_id=redemption.client_id).first()
        if not loyalty or loyalty.points < redemption.points_used:
            raise ValueError('Pontos insuficientes')

        # Deduzir pontos
        loyalty.deduct_points(
            redemption.points_used,
            description=f'Resgate de recompensa: {redemption.reward.name}'
        )

        redemption.status = 'completed'
        db.session.commit()

        # Enviar notificação de confirmação
        send_redemption_confirmation.delay(redemption_id)

    except Exception as e:
        redemption.status = 'cancelled'
        db.session.commit()
        raise e

@celery.task
def send_redemption_confirmation(redemption_id):
    """Envia confirmação de resgate de recompensa"""
    # Implementar lógica de notificação
    pass

@celery.task
def generate_monthly_loyalty_report():
    """Gera relatório mensal de fidelidade"""
    now = datetime.utcnow()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    report_data = {
        'total_points_awarded': db.session.query(
            func.sum(LoyaltyTransaction.points)
        ).filter(
            LoyaltyTransaction.type == 'credit',
            LoyaltyTransaction.created_at >= start_of_month
        ).scalar() or 0,
        
        'total_points_redeemed': db.session.query(
            func.sum(LoyaltyTransaction.points)
        ).filter(
            LoyaltyTransaction.type == 'debit',
            LoyaltyTransaction.created_at >= start_of_month
        ).scalar() or 0,
        
        'new_tier_upgrades': db.session.query(
            func.count(LoyaltyPoints.id)
        ).filter(
            LoyaltyPoints.updated_at >= start_of_month
        ).scalar() or 0
    }
    
    # Salvar ou enviar relatório
    return report_data 