from app import db
from datetime import datetime

class LoyaltyPoints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    points = db.Column(db.Integer, default=0)
    tier = db.Column(db.String(20), default='bronze')  # bronze, silver, gold, platinum
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    client = db.relationship('User', backref='loyalty_points')
    transactions = db.relationship('LoyaltyTransaction', backref='loyalty_account')

    def add_points(self, points, order_id=None, description=None):
        transaction = LoyaltyTransaction(
            loyalty_account_id=self.id,
            points=points,
            type='credit',
            order_id=order_id,
            description=description
        )
        self.points += points
        self.update_tier()
        db.session.add(transaction)
        return transaction

    def deduct_points(self, points, description=None):
        if self.points < points:
            raise ValueError('Pontos insuficientes')
        
        transaction = LoyaltyTransaction(
            loyalty_account_id=self.id,
            points=points,
            type='debit',
            description=description
        )
        self.points -= points
        self.update_tier()
        db.session.add(transaction)
        return transaction

    def update_tier(self):
        if self.points >= 10000:
            self.tier = 'platinum'
        elif self.points >= 5000:
            self.tier = 'gold'
        elif self.points >= 1000:
            self.tier = 'silver'
        else:
            self.tier = 'bronze'

class LoyaltyTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loyalty_account_id = db.Column(db.Integer, db.ForeignKey('loyalty_points.id'))
    points = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # credit, debit
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship('Order')

class LoyaltyReward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    points_required = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    redemptions = db.relationship('LoyaltyRedemption', backref='reward')

class LoyaltyRedemption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reward_id = db.Column(db.Integer, db.ForeignKey('loyalty_reward.id'))
    points_used = db.Column(db.Integer, nullable=False)
    redeemed_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled

    client = db.relationship('User') 