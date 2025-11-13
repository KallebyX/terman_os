from app import db
from datetime import datetime

class Estoque(db.Model):
    __tablename__ = 'estoque'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False, index=True)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    quantidade_minima = db.Column(db.Integer, default=10)  # Alerta de estoque baixo
    quantidade_maxima = db.Column(db.Integer, nullable=True)  # Limite de estoque
    localizacao = db.Column(db.String(100), nullable=True)  # Ex: "Prateleira A-12", "Depósito 2"
    lote = db.Column(db.String(50), nullable=True)  # Número do lote
    data_validade = db.Column(db.Date, nullable=True)  # Para produtos perecíveis
    data_entrada = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos
    movimentacoes = db.relationship('MovimentacaoEstoque', backref='estoque', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def status(self):
        """Retorna status do estoque"""
        if self.quantidade <= 0:
            return 'out_of_stock'
        elif self.quantidade <= self.quantidade_minima:
            return 'low_stock'
        return 'in_stock'

    @property
    def dias_ate_vencimento(self):
        """Calcula dias até vencimento"""
        if self.data_validade:
            delta = self.data_validade - datetime.now().date()
            return delta.days
        return None

    def __repr__(self):
        return f'<Estoque Produto {self.produto_id} | Qtd: {self.quantidade} | Local: {self.localizacao}>'


class MovimentacaoEstoque(db.Model):
    """Histórico de movimentações de estoque"""
    __tablename__ = 'movimentacoes_estoque'

    id = db.Column(db.Integer, primary_key=True)
    estoque_id = db.Column(db.Integer, db.ForeignKey('estoque.id', ondelete='CASCADE'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # 'entrada', 'saida', 'ajuste', 'transferencia'
    quantidade = db.Column(db.Integer, nullable=False)
    quantidade_anterior = db.Column(db.Integer, nullable=False)
    quantidade_nova = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(200), nullable=True)  # Ex: "Venda", "Compra", "Devolução", "Perda"
    referencia_id = db.Column(db.Integer, nullable=True)  # ID do pedido, compra, etc
    referencia_tipo = db.Column(db.String(50), nullable=True)  # 'pedido', 'compra', 'ordem_servico'
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    data_movimentacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    observacoes = db.Column(db.Text, nullable=True)

    usuario = db.relationship('User', backref='movimentacoes_estoque')

    def __repr__(self):
        return f'<MovimentacaoEstoque {self.tipo} | Qtd: {self.quantidade} | {self.data_movimentacao}>'


class Review(db.Model):
    """Avaliações de produtos"""
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1 a 5 estrelas
    titulo = db.Column(db.String(200), nullable=True)
    comentario = db.Column(db.Text, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    verificado = db.Column(db.Boolean, default=False)  # Compra verificada
    aprovado = db.Column(db.Boolean, default=True)  # Moderação
    util_count = db.Column(db.Integer, default=0)  # Quantas pessoas acharam útil

    usuario = db.relationship('User', backref='reviews')

    def __repr__(self):
        return f'<Review Produto {self.produto_id} | Rating: {self.rating} | User: {self.usuario_id}>'