from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

class CashierSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    opened_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    closed_at = db.Column(db.DateTime)
    initial_amount = db.Column(db.Numeric(10, 2), nullable=False)
    final_amount = db.Column(db.Numeric(10, 2))
    expected_amount = db.Column(db.Numeric(10, 2))
    difference = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default='open')  # open, closed
    summary = db.Column(JSONB)
    notes = db.Column(db.Text)

    user = db.relationship('User', backref='cashier_sessions')
    transactions = db.relationship('CashierTransaction', backref='session')

    def calculate_summary(self):
        """Calcula o resumo do caixa"""
        from app.models.order import Order
        from sqlalchemy import func

        # Total de vendas
        orders = Order.query.filter(
            Order.created_at.between(self.opened_at, self.closed_at or datetime.utcnow()),
            Order.status == 'completed'
        ).all()

        total_sales = sum(float(order.total) for order in orders)
        total_orders = len(orders)

        # Totais por método de pagamento
        payment_totals = {}
        for order in orders:
            method = order.payment_method
            payment_totals[method] = payment_totals.get(method, 0) + float(order.total)

        # Transações do caixa
        transactions = CashierTransaction.query.filter_by(session_id=self.id).all()
        cash_in = sum(float(t.amount) for t in transactions if t.type == 'in')
        cash_out = sum(float(t.amount) for t in transactions if t.type == 'out')

        self.summary = {
            'total_sales': total_sales,
            'total_orders': total_orders,
            'payment_methods': payment_totals,
            'cash_in': cash_in,
            'cash_out': cash_out,
            'cash_flow': cash_in - cash_out,
            'expected_amount': float(self.initial_amount) + cash_in - cash_out
        }

        self.expected_amount = self.summary['expected_amount']
        db.session.commit()

        return self.summary

class CashierTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('cashier_session.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # in, out
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    created_by = db.relationship('User') 