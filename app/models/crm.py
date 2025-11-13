"""
Modelos CRM (Customer Relationship Management)
Gestão de clientes, leads, oportunidades e pipeline de vendas
"""
from app import db
from datetime import datetime


class Cliente(db.Model):
    """Cliente estendido - informações além do User"""
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True, index=True)

    # Dados Pessoais
    cpf_cnpj = db.Column(db.String(18), unique=True, nullable=True, index=True)
    telefone = db.Column(db.String(20), nullable=True)
    celular = db.Column(db.String(20), nullable=True)
    data_nascimento = db.Column(db.Date, nullable=True)
    sexo = db.Column(db.String(1), nullable=True)  # M, F, O

    # Endereço Principal
    endereco = db.Column(db.String(300), nullable=True)
    numero = db.Column(db.String(10), nullable=True)
    complemento = db.Column(db.String(100), nullable=True)
    bairro = db.Column(db.String(100), nullable=True)
    cidade = db.Column(db.String(100), nullable=True)
    estado = db.Column(db.String(2), nullable=True)
    cep = db.Column(db.String(10), nullable=True)

    # Empresa (para clientes PJ)
    empresa = db.Column(db.String(200), nullable=True)
    cargo = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    inscricao_estadual = db.Column(db.String(20), nullable=True)

    # Classificação e Segmentação
    tipo = db.Column(db.String(20), default='varejo')  # varejo, atacado, distribuidor, industrial
    categoria = db.Column(db.String(50), nullable=True)  # VIP, Premium, Regular, Bronze
    segmento = db.Column(db.String(100), nullable=True)  # Ex: Agricultura, Indústria, Construção
    origem = db.Column(db.String(50), nullable=True)  # site, indicacao, telefone, redes_sociais

    # Informações Comerciais
    limite_credito = db.Column(db.Float, default=0.0)
    credito_disponivel = db.Column(db.Float, default=0.0)
    dia_vencimento_preferido = db.Column(db.Integer, nullable=True)  # 1-31

    # Vendedor responsável
    vendedor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Métricas
    total_compras = db.Column(db.Float, default=0.0)
    quantidade_pedidos = db.Column(db.Integer, default=0)
    ticket_medio = db.Column(db.Float, default=0.0)
    ultima_compra = db.Column(db.DateTime, nullable=True)
    score_rfm = db.Column(db.Integer, default=0)  # Recency, Frequency, Monetary

    # Status
    ativo = db.Column(db.Boolean, default=True, index=True)
    bloqueado = db.Column(db.Boolean, default=False)
    motivo_bloqueio = db.Column(db.Text, nullable=True)

    # Datas
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Observações
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos
    usuario = db.relationship('User', foreign_keys=[usuario_id], backref='cliente_info')
    vendedor = db.relationship('User', foreign_keys=[vendedor_id], backref='clientes_atribuidos')
    enderecos = db.relationship('EnderecoCliente', backref='cliente', lazy='dynamic', cascade='all, delete-orphan')
    interacoes = db.relationship('Interacao', backref='cliente', lazy='dynamic', cascade='all, delete-orphan')

    def calcular_rfm(self):
        """Calcula score RFM (Recency, Frequency, Monetary)"""
        # Implementação simplificada - pode ser refinada
        recency_score = 5 if self.ultima_compra and (datetime.utcnow() - self.ultima_compra).days < 30 else 1
        frequency_score = min(5, self.quantidade_pedidos // 2)
        monetary_score = min(5, int(self.total_compras / 1000))
        self.score_rfm = (recency_score + frequency_score + monetary_score) // 3
        return self.score_rfm

    def __repr__(self):
        return f'<Cliente {self.usuario_id} | Tipo: {self.tipo}>'


class EnderecoCliente(db.Model):
    """Múltiplos endereços para um cliente"""
    __tablename__ = 'enderecos_clientes'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id', ondelete='CASCADE'), nullable=False, index=True)

    tipo = db.Column(db.String(50), nullable=False)  # residencial, comercial, cobranca, entrega
    apelido = db.Column(db.String(100), nullable=True)  # "Casa", "Escritório"

    endereco = db.Column(db.String(300), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(100), nullable=True)
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(10), nullable=False)

    principal = db.Column(db.Boolean, default=False)  # Endereço principal
    ativo = db.Column(db.Boolean, default=True)

    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<EnderecoCliente {self.apelido or self.tipo} | Cliente: {self.cliente_id}>'


class Lead(db.Model):
    """Leads - potenciais clientes"""
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)

    # Dados básicos
    nome = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=True, index=True)
    telefone = db.Column(db.String(20), nullable=True)
    celular = db.Column(db.String(20), nullable=True)
    empresa = db.Column(db.String(200), nullable=True)
    cargo = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(200), nullable=True)

    # Origem
    origem = db.Column(db.String(50), nullable=True, index=True)  # site, facebook, google_ads, indicacao
    campanha = db.Column(db.String(100), nullable=True)  # Nome da campanha
    midia = db.Column(db.String(50), nullable=True)  # utm_medium

    # Status
    status = db.Column(db.String(50), default='novo', index=True)
    # Status: novo, contatado, qualificado, proposta_enviada, negociacao, ganho, perdido, descartado
    qualificacao = db.Column(db.String(20), nullable=True)  # quente, morno, frio

    # Interesse
    interesse = db.Column(db.Text, nullable=True)  # Produtos/serviços de interesse
    necessidade = db.Column(db.Text, nullable=True)
    orcamento_estimado = db.Column(db.Float, nullable=True)

    # Atribuição
    vendedor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)

    # Score
    score = db.Column(db.Integer, default=0)  # Lead scoring (0-100)

    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    data_primeira_interacao = db.Column(db.DateTime, nullable=True)
    data_ultima_interacao = db.Column(db.DateTime, nullable=True)
    data_conversao = db.Column(db.DateTime, nullable=True)

    # Motivo de perda (se aplicável)
    motivo_perda = db.Column(db.String(200), nullable=True)

    # Observações
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos
    vendedor = db.relationship('User', backref='leads_atribuidos')
    interacoes = db.relationship('Interacao', backref='lead', lazy='dynamic', cascade='all, delete-orphan')
    oportunidade = db.relationship('Oportunidade', uselist=False, backref='lead', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Lead {self.nome} | Status: {self.status}>'


class Oportunidade(db.Model):
    """Oportunidades de venda - pipeline"""
    __tablename__ = 'oportunidades'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)  # "Venda de mangueiras para Fazenda XYZ"

    # Relacionamentos
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id', ondelete='CASCADE'), nullable=True, index=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id', ondelete='CASCADE'), nullable=True, index=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=False, index=True)

    # Pipeline
    estagio = db.Column(db.String(50), nullable=False, default='prospeccao', index=True)
    # Estágios: prospeccao, qualificacao, proposta, negociacao, fechamento, ganho, perdido

    # Valores
    valor_estimado = db.Column(db.Float, nullable=False)
    probabilidade = db.Column(db.Integer, default=10)  # 0-100%
    valor_ponderado = db.Column(db.Float, default=0.0)  # valor_estimado * (probabilidade/100)

    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    data_fechamento_esperada = db.Column(db.Date, nullable=True)
    data_fechamento_real = db.Column(db.DateTime, nullable=True)

    # Resultado
    status = db.Column(db.String(20), default='aberta')  # aberta, ganha, perdida, cancelada
    motivo_ganho = db.Column(db.String(200), nullable=True)
    motivo_perda = db.Column(db.String(200), nullable=True)

    # Informações adicionais
    descricao = db.Column(db.Text, nullable=True)
    proximos_passos = db.Column(db.Text, nullable=True)

    # Relacionamentos
    cliente = db.relationship('Cliente', backref='oportunidades')
    vendedor = db.relationship('User', backref='oportunidades')
    atividades = db.relationship('Atividade', backref='oportunidade', lazy='dynamic', cascade='all, delete-orphan')
    proposta = db.relationship('Proposta', uselist=False, backref='oportunidade', cascade='all, delete-orphan')

    def calcular_valor_ponderado(self):
        """Calcula valor ponderado pela probabilidade"""
        self.valor_ponderado = self.valor_estimado * (self.probabilidade / 100)
        return self.valor_ponderado

    def __repr__(self):
        return f'<Oportunidade {self.nome} | Estágio: {self.estagio}>'


class Interacao(db.Model):
    """Histórico de interações com clientes e leads"""
    __tablename__ = 'interacoes'

    id = db.Column(db.Integer, primary_key=True)

    # Relacionamentos (ou cliente ou lead)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id', ondelete='CASCADE'), nullable=True, index=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id', ondelete='CASCADE'), nullable=True, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Tipo de interação
    tipo = db.Column(db.String(50), nullable=False)  # email, telefone, whatsapp, reuniao, visita, outros
    direcao = db.Column(db.String(20), nullable=True)  # entrada, saida

    # Conteúdo
    assunto = db.Column(db.String(200), nullable=True)
    descricao = db.Column(db.Text, nullable=False)

    # Data
    data_interacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    duracao_minutos = db.Column(db.Integer, nullable=True)

    # Status
    importante = db.Column(db.Boolean, default=False)

    # Relacionamento
    usuario = db.relationship('User', backref='interacoes_realizadas')

    def __repr__(self):
        return f'<Interacao {self.tipo} | {self.data_interacao}>'


class Atividade(db.Model):
    """Tarefas e atividades para vendedores"""
    __tablename__ = 'atividades'

    id = db.Column(db.Integer, primary_key=True)

    # Relacionamentos
    oportunidade_id = db.Column(db.Integer, db.ForeignKey('oportunidades.id', ondelete='CASCADE'), nullable=True, index=True)
    usuario_responsavel_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    usuario_criador_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Tipo
    tipo = db.Column(db.String(50), nullable=False)  # tarefa, reuniao, ligacao, email, outros
    prioridade = db.Column(db.String(20), default='media')  # baixa, media, alta, urgente

    # Conteúdo
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_vencimento = db.Column(db.DateTime, nullable=True, index=True)
    data_conclusao = db.Column(db.DateTime, nullable=True)

    # Status
    concluida = db.Column(db.Boolean, default=False, index=True)
    cancelada = db.Column(db.Boolean, default=False)

    # Lembrete
    lembrete = db.Column(db.DateTime, nullable=True)
    lembrete_enviado = db.Column(db.Boolean, default=False)

    # Relacionamentos
    responsavel = db.relationship('User', foreign_keys=[usuario_responsavel_id], backref='atividades_atribuidas')
    criador = db.relationship('User', foreign_keys=[usuario_criador_id], backref='atividades_criadas')

    def __repr__(self):
        return f'<Atividade {self.titulo} | Status: {"Concluída" if self.concluida else "Pendente"}>'


class Proposta(db.Model):
    """Propostas comerciais"""
    __tablename__ = 'propostas'

    id = db.Column(db.Integer, primary_key=True)
    numero_proposta = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Relacionamentos
    oportunidade_id = db.Column(db.Integer, db.ForeignKey('oportunidades.id', ondelete='CASCADE'), nullable=False, index=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Conteúdo
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    condicoes_comerciais = db.Column(db.Text, nullable=True)
    prazo_entrega = db.Column(db.String(100), nullable=True)
    forma_pagamento = db.Column(db.String(100), nullable=True)

    # Valores
    valor_total = db.Column(db.Float, nullable=False)
    desconto = db.Column(db.Float, default=0.0)
    valor_final = db.Column(db.Float, nullable=False)

    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_validade = db.Column(db.Date, nullable=True)
    data_envio = db.Column(db.DateTime, nullable=True)
    data_visualizacao = db.Column(db.DateTime, nullable=True)
    data_aceite = db.Column(db.DateTime, nullable=True)
    data_recusa = db.Column(db.DateTime, nullable=True)

    # Status
    status = db.Column(db.String(50), default='rascunho')  # rascunho, enviada, visualizada, aceita, recusada, expirada

    # Arquivos
    arquivo_pdf_url = db.Column(db.String(255), nullable=True)

    # Relacionamento
    vendedor = db.relationship('User', backref='propostas')
    itens = db.relationship('ItemProposta', backref='proposta', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Proposta {self.numero_proposta} | Status: {self.status}>'


class ItemProposta(db.Model):
    """Itens da proposta"""
    __tablename__ = 'itens_proposta'

    id = db.Column(db.Integer, primary_key=True)
    proposta_id = db.Column(db.Integer, db.ForeignKey('propostas.id', ondelete='CASCADE'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='SET NULL'), nullable=True)

    descricao = db.Column(db.String(300), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Float, nullable=False)
    desconto = db.Column(db.Float, default=0.0)

    produto = db.relationship('Produto', backref='itens_proposta')

    def subtotal(self):
        return (self.quantidade * self.preco_unitario) - self.desconto

    def __repr__(self):
        return f'<ItemProposta {self.descricao}>'
