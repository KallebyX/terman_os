from app import db

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, default=0)
    imagem = db.Column(db.String(200))
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    itens_pedido = db.relationship('ItemPedido', backref='produto', lazy='dynamic') 