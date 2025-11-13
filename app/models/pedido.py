from app import db
from datetime import datetime
from sqlalchemy import String


class Pedido(db.Model):
    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    numero_pedido = db.Column(db.String(50), unique=True, nullable=False, index=True)  # Ex: "PED-2025-00001"
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)

    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    data_aprovacao = db.Column(db.DateTime, nullable=True)
    data_envio = db.Column(db.DateTime, nullable=True)
    data_entrega = db.Column(db.DateTime, nullable=True)
    data_cancelamento = db.Column(db.DateTime, nullable=True)

    # Status
    status = db.Column(db.String(50), default='pendente', index=True)
    # Possíveis status: pendente, confirmado, em_separacao, em_producao, enviado, entregue, cancelado, devolvido
    status_pagamento = db.Column(db.String(50), default='pendente')  # pendente, processando, aprovado, recusado, estornado

    # Endereço de entrega
    endereco_entrega = db.Column(db.Text, nullable=True)
    cidade_entrega = db.Column(db.String(100), nullable=True)
    estado_entrega = db.Column(db.String(2), nullable=True)
    cep_entrega = db.Column(db.String(10), nullable=True)
    complemento_entrega = db.Column(db.String(200), nullable=True)

    # Valores
    subtotal = db.Column(db.Float, default=0.0)
    desconto = db.Column(db.Float, default=0.0)
    valor_frete = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)

    # Pagamento
    forma_pagamento = db.Column(db.String(50), nullable=True)  # pix, cartao_credito, cartao_debito, boleto, dinheiro
    parcelas = db.Column(db.Integer, default=1)
    transacao_id = db.Column(db.String(200), nullable=True)  # ID da transação no gateway

    # Rastreamento e NF
    codigo_rastreio = db.Column(String(50), nullable=True, index=True)
    transportadora = db.Column(db.String(100), nullable=True)
    nota_fiscal_numero = db.Column(db.String(50), nullable=True)
    nota_fiscal_url = db.Column(String(255), nullable=True)

    # Outros
    cupom_desconto = db.Column(db.String(50), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    observacoes_internas = db.Column(db.Text, nullable=True)  # Visível apenas para admin

    # Relacionamentos
    itens = db.relationship('ItemPedido', backref='pedido', lazy='dynamic', cascade='all, delete-orphan')
    usuario = db.relationship('User', backref='pedidos')
    historico = db.relationship('HistoricoPedido', backref='pedido', lazy='dynamic', cascade='all, delete-orphan')

    def calcular_total(self):
        """Recalcula o total do pedido"""
        self.subtotal = sum(item.subtotal() for item in self.itens)
        self.total = self.subtotal - self.desconto + self.valor_frete
        return self.total

    @property
    def status_display(self):
        """Retorna nome amigável do status"""
        status_map = {
            'pendente': 'Pendente',
            'confirmado': 'Confirmado',
            'em_separacao': 'Em Separação',
            'em_producao': 'Em Produção',
            'enviado': 'Enviado',
            'entregue': 'Entregue',
            'cancelado': 'Cancelado',
            'devolvido': 'Devolvido'
        }
        return status_map.get(self.status, self.status)

    def __repr__(self):
        return f'<Pedido {self.numero_pedido} | Status: {self.status}>'


class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id', ondelete='CASCADE'), nullable=False, index=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='SET NULL'), nullable=True, index=True)

    # Dados do produto (snapshot no momento da compra)
    produto_nome = db.Column(db.String(200), nullable=False)
    produto_codigo = db.Column(db.String(50), nullable=True)
    produto_imagem = db.Column(db.String(255), nullable=True)

    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    desconto_item = db.Column(db.Float, default=0.0)

    # Relacionamento
    produto = db.relationship('Produto', backref='itens_pedido')

    def subtotal(self):
        return (self.quantidade * self.preco_unitario) - self.desconto_item

    def __repr__(self):
        return f'<ItemPedido Pedido {self.pedido_id} | Produto: {self.produto_nome}>'


class HistoricoPedido(db.Model):
    """Histórico de mudanças de status do pedido"""
    __tablename__ = 'historico_pedidos'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id', ondelete='CASCADE'), nullable=False, index=True)
    status_anterior = db.Column(db.String(50), nullable=True)
    status_novo = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    data_alteracao = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    usuario = db.relationship('User', backref='alteracoes_pedido')

    def __repr__(self):
        return f'<HistoricoPedido {self.pedido_id} | {self.status_anterior} -> {self.status_novo}>'