from app import db

class Estoque(db.Model):
    __tablename__ = 'estoque'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    localizacao = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Estoque Produto {self.produto_id} | Quantidade: {self.quantidade}>'