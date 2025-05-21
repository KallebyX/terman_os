from app import db
from datetime import datetime

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    total = db.Column(db.Numeric(10, 2))
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    client = db.relationship('User', foreign_keys=[client_id])
    seller = db.relationship('User', foreign_keys=[seller_id])
    items = db.relationship('OrderItem', backref='order')

    def calculate_total(self):
        return sum(item.subtotal for item in self.items)

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'client': self.client.name,
            'seller': self.seller.name if self.seller else None,
            'status': self.status,
            'total': float(self.total),
            'payment_method': self.payment_method,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2))
    discount = db.Column(db.Numeric(10, 2), default=0)

    product = db.relationship('Product')

    @property
    def subtotal(self):
        return (self.price * self.quantity) - self.discount

    def to_dict(self):
        return {
            'product': self.product.name,
            'quantity': self.quantity,
            'price': float(self.price),
            'discount': float(self.discount),
            'subtotal': float(self.subtotal)
        } 