from app import db
from datetime import datetime
from sqlalchemy import String


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Recebido')  # Recebido, Separando, Prensando, Finalizado
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True)
    codigo_rastreio = db.Column(String(50), nullable=True)
    nota_fiscal_url = db.Column(String(255), nullable=True)

    def total(self):
        return sum(item.subtotal() for item in self.itens)

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)

    def subtotal(self):
        return self.quantidade * self.preco_unitario