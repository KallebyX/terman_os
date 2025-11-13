"""
Modelos de Manufatura/Indústria
Gestão de ordens de serviço, produção e controle de qualidade
"""
from app import db
from datetime import datetime


class OrdemServico(db.Model):
    """Ordens de Serviço - Prensagem de mangueiras e serviços técnicos"""
    __tablename__ = 'ordens_servico_new'

    id = db.Column(db.Integer, primary_key=True)
    numero_os = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id', ondelete='SET NULL'), nullable=True, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    cliente_nome = db.Column(db.String(200), nullable=True)  # Snapshot

    # Relacionamento com pedido
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id', ondelete='SET NULL'), nullable=True)

    # Tipo de serviço
    tipo_servico = db.Column(db.String(100), nullable=False)  # prensagem, montagem, reparo, manutencao, instalacao
    prioridade = db.Column(db.String(20), default='normal')  # baixa, normal, alta, urgente

    # Descrição
    descricao_servico = db.Column(db.Text, nullable=False)
    especificacoes_tecnicas = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_inicio_prevista = db.Column(db.DateTime, nullable=True)
    data_inicio_real = db.Column(db.DateTime, nullable=True)
    data_conclusao_prevista = db.Column(db.DateTime, nullable=True)
    data_conclusao_real = db.Column(db.DateTime, nullable=True)
    prazo_entrega = db.Column(db.DateTime, nullable=True)

    # Status
    status = db.Column(db.String(50), default='aberta', index=True)
    # Status: aberta, em_andamento, aguardando_material, aguardando_aprovacao, concluida, cancelada, pausada

    # Recursos
    operador_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    equipamento = db.Column(db.String(200), nullable=True)  # Máquina/equipamento utilizado
    setor = db.Column(db.String(100), nullable=True)  # Setor da fábrica

    # Custos e valores
    custo_mao_obra = db.Column(db.Float, default=0.0)
    custo_materiais = db.Column(db.Float, default=0.0)
    custo_total = db.Column(db.Float, default=0.0)
    valor_servico = db.Column(db.Float, default=0.0)

    # Controle de qualidade
    aprovado_qc = db.Column(db.Boolean, nullable=True)
    responsavel_qc_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    data_inspecao = db.Column(db.DateTime, nullable=True)
    observacoes_qc = db.Column(db.Text, nullable=True)

    # Garantia
    tem_garantia = db.Column(db.Boolean, default=True)
    prazo_garantia_dias = db.Column(db.Integer, default=90)
    data_vencimento_garantia = db.Column(db.Date, nullable=True)

    # Relacionamentos
    cliente = db.relationship('Cliente', backref='ordens_servico_new')
    usuario = db.relationship('User', foreign_keys=[usuario_id], backref='ordens_servico_solicitadas')
    operador = db.relationship('User', foreign_keys=[operador_id], backref='ordens_servico_executadas')
    responsavel_qc = db.relationship('User', foreign_keys=[responsavel_qc_id], backref='ordens_servico_inspecionadas')
    pedido = db.relationship('Pedido', backref='ordens_servico_new')
    produtos = db.relationship('ProdutoOS', backref='ordem_servico', lazy='dynamic', cascade='all, delete-orphan')
    anexos = db.relationship('AnexoOS', backref='ordem_servico', lazy='dynamic', cascade='all, delete-orphan')
    historico = db.relationship('HistoricoOS', backref='ordem_servico', lazy='dynamic', cascade='all, delete-orphan', order_by='HistoricoOS.data_alteracao.desc()')

    def calcular_custo_total(self):
        """Calcula custo total da OS"""
        self.custo_materiais = sum(p.custo_total for p in self.produtos)
        self.custo_total = self.custo_mao_obra + self.custo_materiais
        return self.custo_total

    @property
    def margem_lucro(self):
        """Calcula margem de lucro"""
        if self.custo_total > 0 and self.valor_servico > 0:
            return ((self.valor_servico - self.custo_total) / self.valor_servico) * 100
        return 0

    @property
    def tempo_execucao_horas(self):
        """Calcula tempo de execução em horas"""
        if self.data_inicio_real and self.data_conclusao_real:
            delta = self.data_conclusao_real - self.data_inicio_real
            return delta.total_seconds() / 3600
        return None

    def __repr__(self):
        return f'<OrdemServico {self.numero_os} | Status: {self.status}>'


class ProdutoOS(db.Model):
    """Produtos/materiais utilizados na ordem de serviço"""
    __tablename__ = 'produtos_os'

    id = db.Column(db.Integer, primary_key=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico_new.id', ondelete='CASCADE'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='SET NULL'), nullable=True)

    # Snapshot do produto
    produto_nome = db.Column(db.String(200), nullable=False)
    produto_codigo = db.Column(db.String(50), nullable=True)

    # Quantidades
    quantidade = db.Column(db.Float, nullable=False)
    unidade = db.Column(db.String(20), default='un')  # un, m, kg, l

    # Custos
    custo_unitario = db.Column(db.Float, default=0.0)
    custo_total = db.Column(db.Float, default=0.0)

    # Relacionamento
    produto = db.relationship('Produto', backref='produtos_os')

    def __repr__(self):
        return f'<ProdutoOS {self.produto_nome} | Qtd: {self.quantidade}>'


class AnexoOS(db.Model):
    """Anexos da ordem de serviço (fotos, documentos)"""
    __tablename__ = 'anexos_os'

    id = db.Column(db.Integer, primary_key=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico_new.id', ondelete='CASCADE'), nullable=False)

    tipo = db.Column(db.String(50), nullable=False)  # foto, documento, laudo, certificado
    titulo = db.Column(db.String(200), nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    arquivo_url = db.Column(db.String(300), nullable=False)
    nome_arquivo = db.Column(db.String(200), nullable=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('User', backref='anexos_os')

    def __repr__(self):
        return f'<AnexoOS {self.tipo} | OS: {self.ordem_servico_id}>'


class HistoricoOS(db.Model):
    """Histórico de alterações da ordem de serviço"""
    __tablename__ = 'historico_os'

    id = db.Column(db.Integer, primary_key=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico_new.id', ondelete='CASCADE'), nullable=False)

    tipo_alteracao = db.Column(db.String(50), nullable=False)  # status, atribuicao, observacao, qc
    campo_alterado = db.Column(db.String(100), nullable=True)
    valor_anterior = db.Column(db.Text, nullable=True)
    valor_novo = db.Column(db.Text, nullable=True)
    descricao = db.Column(db.Text, nullable=True)

    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    data_alteracao = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    usuario = db.relationship('User', backref='alteracoes_os')

    def __repr__(self):
        return f'<HistoricoOS OS {self.ordem_servico_id} | {self.tipo_alteracao}>'


class OrdemProducao(db.Model):
    """Ordens de produção para manufatura"""
    __tablename__ = 'ordens_producao'

    id = db.Column(db.Integer, primary_key=True)
    numero_op = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Produto a ser produzido
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='RESTRICT'), nullable=False)
    quantidade_planejada = db.Column(db.Integer, nullable=False)
    quantidade_produzida = db.Column(db.Integer, default=0)
    quantidade_aprovada = db.Column(db.Integer, default=0)
    quantidade_rejeitada = db.Column(db.Integer, default=0)

    # Relacionamentos
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id', ondelete='SET NULL'), nullable=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico_new.id', ondelete='SET NULL'), nullable=True)

    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_inicio_planejada = db.Column(db.DateTime, nullable=True)
    data_inicio_real = db.Column(db.DateTime, nullable=True)
    data_fim_planejada = db.Column(db.DateTime, nullable=True)
    data_fim_real = db.Column(db.DateTime, nullable=True)

    # Status
    status = db.Column(db.String(50), default='planejada', index=True)
    # Status: planejada, liberada, em_producao, pausada, concluida, cancelada
    prioridade = db.Column(db.String(20), default='normal')

    # Recursos
    linha_producao = db.Column(db.String(100), nullable=True)
    turno = db.Column(db.String(50), nullable=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Custos
    custo_planejado = db.Column(db.Float, default=0.0)
    custo_real = db.Column(db.Float, default=0.0)

    # Observações
    observacoes = db.Column(db.Text, nullable=True)

    # Relacionamentos
    produto = db.relationship('Produto', backref='ordens_producao')
    pedido = db.relationship('Pedido', backref='ordens_producao')
    ordem_servico = db.relationship('OrdemServico', backref='ordens_producao')
    supervisor = db.relationship('User', backref='ordens_producao_supervisionadas')
    inspecoes = db.relationship('InspecaoQualidade', backref='ordem_producao', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def percentual_concluido(self):
        """Calcula % de conclusão"""
        if self.quantidade_planejada > 0:
            return (self.quantidade_produzida / self.quantidade_planejada) * 100
        return 0

    @property
    def taxa_aprovacao(self):
        """Calcula taxa de aprovação no QC"""
        if self.quantidade_produzida > 0:
            return (self.quantidade_aprovada / self.quantidade_produzida) * 100
        return 0

    def __repr__(self):
        return f'<OrdemProducao {self.numero_op} | Produto: {self.produto_id}>'


class InspecaoQualidade(db.Model):
    """Inspeções de controle de qualidade"""
    __tablename__ = 'inspecoes_qualidade'

    id = db.Column(db.Integer, primary_key=True)

    # Relacionamentos (pode ser OP ou OS)
    ordem_producao_id = db.Column(db.Integer, db.ForeignKey('ordens_producao.id', ondelete='CASCADE'), nullable=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico_new.id', ondelete='CASCADE'), nullable=True)

    # Tipo
    tipo_inspecao = db.Column(db.String(50), nullable=False)  # inicial, processo, final, recebimento
    numero_inspecao = db.Column(db.String(50), unique=True, nullable=True)

    # Inspetor
    inspetor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=False)
    data_inspecao = db.Column(db.DateTime, default=datetime.utcnow)

    # Resultado
    resultado = db.Column(db.String(20), nullable=False)  # aprovado, reprovado, aprovado_com_restricao
    quantidade_inspecionada = db.Column(db.Integer, nullable=False)
    quantidade_aprovada = db.Column(db.Integer, nullable=False)
    quantidade_reprovada = db.Column(db.Integer, default=0)

    # Detalhes
    criterios_inspecao = db.Column(db.Text, nullable=True)  # JSON com critérios
    defeitos_encontrados = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)
    acoes_corretivas = db.Column(db.Text, nullable=True)

    # Anexos
    fotos_url = db.Column(db.Text, nullable=True)  # JSON array de URLs
    laudo_url = db.Column(db.String(300), nullable=True)

    # Relacionamentos
    inspetor = db.relationship('User', backref='inspecoes_realizadas')
    ordem_servico = db.relationship('OrdemServico', backref='inspecoes')

    def __repr__(self):
        return f'<InspecaoQualidade {self.numero_inspecao} | Resultado: {self.resultado}>'
