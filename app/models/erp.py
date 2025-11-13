"""
Modelos ERP (Enterprise Resource Planning)
Gestão de compras, fornecedores, financeiro e recursos humanos
"""
from app import db
from datetime import datetime


class Fornecedor(db.Model):
    """Fornecedores de produtos"""
    __tablename__ = 'fornecedores'

    id = db.Column(db.Integer, primary_key=True)

    # Dados básicos
    razao_social = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(200), nullable=True)
    cnpj = db.Column(db.String(18), unique=True, nullable=False, index=True)
    inscricao_estadual = db.Column(db.String(20), nullable=True)
    inscricao_municipal = db.Column(db.String(20), nullable=True)

    # Contato
    email = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    celular = db.Column(db.String(20), nullable=True)
    website = db.Column(db.String(200), nullable=True)

    # Endereço
    endereco = db.Column(db.String(300), nullable=True)
    numero = db.Column(db.String(10), nullable=True)
    complemento = db.Column(db.String(100), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    cep = db.Column(db.String(10), nullable=True)

    # Pessoa de contato
    contato_nome = db.Column(db.String(200), nullable=True)
    contato_cargo = db.Column(db.String(100), nullable=True)
    contato_email = db.Column(db.String(120), nullable=True)
    contato_telefone = db.Column(db.String(20), nullable=True)

    # Classificação
    tipo = db.Column(db.String(50), nullable=True)  # materia_prima, servicos, revenda
    categoria = db.Column(db.String(100), nullable=True)
    segmento = db.Column(db.String(100), nullable=True)

    # Condições comerciais
    prazo_pagamento_padrao = db.Column(db.String(100), nullable=True)  # "30 dias", "À vista"
    prazo_entrega_medio = db.Column(db.Integer, nullable=True)  # em dias
    pedido_minimo = db.Column(db.Float, default=0.0)

    # Métricas
    total_comprado = db.Column(db.Float, default=0.0)
    quantidade_compras = db.Column(db.Integer, default=0)
    ultima_compra = db.Column(db.DateTime, nullable=True)

    # Avaliação
    rating = db.Column(db.Integer, nullable=True)  # 1-5
    qualidade_produto = db.Column(db.Integer, nullable=True)  # 1-5
    pontualidade_entrega = db.Column(db.Integer, nullable=True)  # 1-5
    atendimento = db.Column(db.Integer, nullable=True)  # 1-5

    # Status
    ativo = db.Column(db.Boolean, default=True, index=True)
    bloqueado = db.Column(db.Boolean, default=False)
    motivo_bloqueio = db.Column(db.Text, nullable=True)

    # Datas
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Observações
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos
    compras = db.relationship('Compra', backref='fornecedor', lazy='dynamic')
    produtos_fornecidos = db.relationship('ProdutoFornecedor', backref='fornecedor', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Fornecedor {self.nome_fantasia or self.razao_social}>'


class ProdutoFornecedor(db.Model):
    """Relacionamento entre produtos e fornecedores com preços"""
    __tablename__ = 'produtos_fornecedores'

    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='CASCADE'), nullable=False, index=True)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id', ondelete='CASCADE'), nullable=False, index=True)

    # Informações do produto no fornecedor
    codigo_fornecedor = db.Column(db.String(50), nullable=True)  # Código do produto no catálogo do fornecedor
    preco_custo = db.Column(db.Float, nullable=False)
    preco_ultima_compra = db.Column(db.Float, nullable=True)
    quantidade_minima = db.Column(db.Integer, default=1)
    prazo_entrega_dias = db.Column(db.Integer, nullable=True)

    # Status
    preferencial = db.Column(db.Boolean, default=False)  # Fornecedor preferencial para este produto
    ativo = db.Column(db.Boolean, default=True)

    # Datas
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_ultima_compra = db.Column(db.DateTime, nullable=True)
    data_atualizacao_preco = db.Column(db.DateTime, nullable=True)

    # Relacionamento
    produto = db.relationship('Produto', backref='fornecedores')

    def __repr__(self):
        return f'<ProdutoFornecedor Produto: {self.produto_id} | Fornecedor: {self.fornecedor_id}>'


class Compra(db.Model):
    """Pedidos de compra para fornecedores"""
    __tablename__ = 'compras'

    id = db.Column(db.Integer, primary_key=True)
    numero_compra = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Fornecedor
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id', ondelete='RESTRICT'), nullable=False, index=True)

    # Datas
    data_pedido = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_prevista_entrega = db.Column(db.Date, nullable=True)
    data_entrega_real = db.Column(db.DateTime, nullable=True)
    data_cancelamento = db.Column(db.DateTime, nullable=True)

    # Status
    status = db.Column(db.String(50), default='pendente', index=True)
    # Status: pendente, aprovado, em_transito, recebido_parcial, recebido, cancelado

    # Valores
    subtotal = db.Column(db.Float, default=0.0)
    desconto = db.Column(db.Float, default=0.0)
    valor_frete = db.Column(db.Float, default=0.0)
    outras_despesas = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, default=0.0)

    # Pagamento
    forma_pagamento = db.Column(db.String(100), nullable=True)
    condicao_pagamento = db.Column(db.String(200), nullable=True)

    # Responsável
    comprador_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Informações de entrega
    endereco_entrega = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos
    itens = db.relationship('ItemCompra', backref='compra', lazy='dynamic', cascade='all, delete-orphan')
    comprador = db.relationship('User', backref='compras_realizadas')
    recebimentos = db.relationship('RecebimentoCompra', backref='compra', lazy='dynamic', cascade='all, delete-orphan')

    def calcular_total(self):
        """Recalcula o total da compra"""
        self.subtotal = sum(item.subtotal() for item in self.itens)
        self.total = self.subtotal - self.desconto + self.valor_frete + self.outras_despesas
        return self.total

    def __repr__(self):
        return f'<Compra {self.numero_compra} | Fornecedor: {self.fornecedor_id}>'


class ItemCompra(db.Model):
    """Itens do pedido de compra"""
    __tablename__ = 'itens_compra'

    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id', ondelete='CASCADE'), nullable=False, index=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='RESTRICT'), nullable=False)

    quantidade_pedida = db.Column(db.Integer, nullable=False)
    quantidade_recebida = db.Column(db.Integer, default=0)
    preco_unitario = db.Column(db.Float, nullable=False)
    desconto_item = db.Column(db.Float, default=0.0)

    # Relacionamento
    produto = db.relationship('Produto', backref='itens_compra')

    def subtotal(self):
        return (self.quantidade_pedida * self.preco_unitario) - self.desconto_item

    def __repr__(self):
        return f'<ItemCompra Compra: {self.compra_id} | Produto: {self.produto_id}>'


class RecebimentoCompra(db.Model):
    """Registro de recebimento de mercadorias"""
    __tablename__ = 'recebimentos_compra'

    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id', ondelete='CASCADE'), nullable=False, index=True)

    data_recebimento = db.Column(db.DateTime, default=datetime.utcnow)
    recebedor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    nota_fiscal_numero = db.Column(db.String(50), nullable=True)
    nota_fiscal_valor = db.Column(db.Float, nullable=True)

    conferido = db.Column(db.Boolean, default=False)
    aprovado = db.Column(db.Boolean, default=True)
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamento
    recebedor = db.relationship('User', backref='recebimentos_compra_realizados')
    itens = db.relationship('ItemRecebimento', backref='recebimento', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<RecebimentoCompra Compra: {self.compra_id} | Data: {self.data_recebimento}>'


class ItemRecebimento(db.Model):
    """Itens recebidos em cada recebimento"""
    __tablename__ = 'itens_recebimento'

    id = db.Column(db.Integer, primary_key=True)
    recebimento_id = db.Column(db.Integer, db.ForeignKey('recebimentos_compra.id', ondelete='CASCADE'), nullable=False)
    item_compra_id = db.Column(db.Integer, db.ForeignKey('itens_compra.id', ondelete='CASCADE'), nullable=False)

    quantidade_recebida = db.Column(db.Integer, nullable=False)
    quantidade_aprovada = db.Column(db.Integer, nullable=False)
    quantidade_rejeitada = db.Column(db.Integer, default=0)

    motivo_rejeicao = db.Column(db.Text, nullable=True)
    lote = db.Column(db.String(50), nullable=True)
    data_validade = db.Column(db.Date, nullable=True)

    # Relacionamento
    item_compra = db.relationship('ItemCompra', backref='recebimentos')

    def __repr__(self):
        return f'<ItemRecebimento {self.quantidade_recebida} unidades>'


class ContaPagar(db.Model):
    """Contas a pagar"""
    __tablename__ = 'contas_pagar'

    id = db.Column(db.Integer, primary_key=True)
    numero_documento = db.Column(db.String(50), nullable=True, index=True)

    # Fornecedor ou outro beneficiário
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id', ondelete='SET NULL'), nullable=True, index=True)
    beneficiario = db.Column(db.String(200), nullable=True)  # Se não for fornecedor

    # Relacionamento com compra (opcional)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id', ondelete='SET NULL'), nullable=True)

    # Tipo e categoria
    tipo = db.Column(db.String(50), nullable=False)  # fornecedor, salario, aluguel, servicos, outros
    categoria = db.Column(db.String(100), nullable=True)  # Categoria de despesa
    descricao = db.Column(db.Text, nullable=False)

    # Valores
    valor_original = db.Column(db.Float, nullable=False)
    valor_pago = db.Column(db.Float, default=0.0)
    valor_desconto = db.Column(db.Float, default=0.0)
    valor_juros = db.Column(db.Float, default=0.0)
    valor_multa = db.Column(db.Float, default=0.0)

    # Datas
    data_emissao = db.Column(db.Date, nullable=False, index=True)
    data_vencimento = db.Column(db.Date, nullable=False, index=True)
    data_pagamento = db.Column(db.Date, nullable=True, index=True)

    # Status
    status = db.Column(db.String(50), default='pendente', index=True)  # pendente, pago_parcial, pago, cancelado

    # Forma de pagamento
    forma_pagamento = db.Column(db.String(50), nullable=True)  # dinheiro, transferencia, boleto, cheque
    conta_bancaria_id = db.Column(db.Integer, nullable=True)  # FK para conta bancária (se implementado)

    # Parcelamento
    parcela_numero = db.Column(db.Integer, default=1)
    parcela_total = db.Column(db.Integer, default=1)

    # Recorrência
    recorrente = db.Column(db.Boolean, default=False)
    frequencia = db.Column(db.String(20), nullable=True)  # mensal, trimestral, anual

    # Observações
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos
    fornecedor = db.relationship('Fornecedor', backref='contas_pagar')
    compra = db.relationship('Compra', backref='contas_pagar')
    pagamentos = db.relationship('PagamentoCP', backref='conta', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def valor_pendente(self):
        return self.valor_original + self.valor_juros + self.valor_multa - self.valor_desconto - self.valor_pago

    @property
    def esta_vencida(self):
        if self.status == 'pago':
            return False
        return self.data_vencimento < datetime.now().date()

    def __repr__(self):
        return f'<ContaPagar {self.numero_documento} | Valor: R$ {self.valor_original}>'


class PagamentoCP(db.Model):
    """Registro de pagamentos de contas a pagar"""
    __tablename__ = 'pagamentos_cp'

    id = db.Column(db.Integer, primary_key=True)
    conta_pagar_id = db.Column(db.Integer, db.ForeignKey('contas_pagar.id', ondelete='CASCADE'), nullable=False)

    data_pagamento = db.Column(db.Date, nullable=False)
    valor_pago = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamento
    usuario = db.relationship('User', backref='pagamentos_realizados')

    def __repr__(self):
        return f'<PagamentoCP Valor: R$ {self.valor_pago} | Data: {self.data_pagamento}>'


class ContaReceber(db.Model):
    """Contas a receber"""
    __tablename__ = 'contas_receber'

    id = db.Column(db.Integer, primary_key=True)
    numero_documento = db.Column(db.String(50), nullable=True, index=True)

    # Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id', ondelete='SET NULL'), nullable=True, index=True)
    cliente_nome = db.Column(db.String(200), nullable=True)

    # Relacionamento com pedido (opcional)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id', ondelete='SET NULL'), nullable=True)

    # Tipo
    tipo = db.Column(db.String(50), default='venda')  # venda, servico, outros
    descricao = db.Column(db.Text, nullable=False)

    # Valores
    valor_original = db.Column(db.Float, nullable=False)
    valor_recebido = db.Column(db.Float, default=0.0)
    valor_desconto = db.Column(db.Float, default=0.0)
    valor_juros = db.Column(db.Float, default=0.0)
    valor_multa = db.Column(db.Float, default=0.0)

    # Datas
    data_emissao = db.Column(db.Date, nullable=False, index=True)
    data_vencimento = db.Column(db.Date, nullable=False, index=True)
    data_recebimento = db.Column(db.Date, nullable=True, index=True)

    # Status
    status = db.Column(db.String(50), default='pendente', index=True)  # pendente, recebido_parcial, recebido, cancelado

    # Forma de pagamento
    forma_pagamento = db.Column(db.String(50), nullable=True)

    # Parcelamento
    parcela_numero = db.Column(db.Integer, default=1)
    parcela_total = db.Column(db.Integer, default=1)

    # Observações
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos
    cliente = db.relationship('Cliente', backref='contas_receber')
    pedido = db.relationship('Pedido', backref='contas_receber')
    recebimentos = db.relationship('RecebimentoCR', backref='conta', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def valor_pendente(self):
        return self.valor_original + self.valor_juros + self.valor_multa - self.valor_desconto - self.valor_recebido

    @property
    def esta_vencida(self):
        if self.status == 'recebido':
            return False
        return self.data_vencimento < datetime.now().date()

    def __repr__(self):
        return f'<ContaReceber {self.numero_documento} | Valor: R$ {self.valor_original}>'


class RecebimentoCR(db.Model):
    """Registro de recebimentos de contas a receber"""
    __tablename__ = 'recebimentos_cr'

    id = db.Column(db.Integer, primary_key=True)
    conta_receber_id = db.Column(db.Integer, db.ForeignKey('contas_receber.id', ondelete='CASCADE'), nullable=False)

    data_recebimento = db.Column(db.Date, nullable=False)
    valor_recebido = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)

    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamento
    usuario = db.relationship('User', backref='recebimentos_cr_realizados')

    def __repr__(self):
        return f'<RecebimentoCR Valor: R$ {self.valor_recebido} | Data: {self.data_recebimento}>'
