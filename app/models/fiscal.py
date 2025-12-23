# -*- coding: utf-8 -*-
"""
Modelos Fiscais - Sistema NFe, Orçamentos e Configurações Empresariais
Padrão SEFAZ Brasil - Layout 4.00 NFe
"""

from datetime import datetime, date
from decimal import Decimal
from app import db
import json


class ConfiguracaoEmpresa(db.Model):
    """Configuração completa da empresa emissora de NFe"""
    __tablename__ = 'configuracao_empresa'

    id = db.Column(db.Integer, primary_key=True)

    # Dados Básicos
    razao_social = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(100))
    cnpj = db.Column(db.String(18), unique=True, nullable=False)
    inscricao_estadual = db.Column(db.String(20))
    inscricao_municipal = db.Column(db.String(20))
    inscricao_suframa = db.Column(db.String(20))  # Zona Franca de Manaus

    # Regime Tributário (1=Simples Nacional, 2=Simples Excesso, 3=Regime Normal)
    regime_tributario = db.Column(db.Integer, default=1)

    # CNAE Principal
    cnae_principal = db.Column(db.String(10))
    cnae_secundarios = db.Column(db.Text)  # JSON array

    # Endereço Completo
    logradouro = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    codigo_municipio = db.Column(db.String(7), nullable=False)  # Código IBGE
    uf = db.Column(db.String(2), nullable=False)
    codigo_uf = db.Column(db.String(2))  # Código IBGE UF
    cep = db.Column(db.String(10), nullable=False)
    pais = db.Column(db.String(100), default='Brasil')
    codigo_pais = db.Column(db.String(4), default='1058')  # Código BCB

    # Contato
    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    email = db.Column(db.String(200))
    email_nfe = db.Column(db.String(200))  # Email específico para NFe
    website = db.Column(db.String(200))

    # Logo
    logo_url = db.Column(db.String(500))
    logo_base64 = db.Column(db.Text)  # Para PDF

    # Configurações NFe
    ambiente_nfe = db.Column(db.Integer, default=2)  # 1=Produção, 2=Homologação
    serie_nfe = db.Column(db.Integer, default=1)
    ultimo_numero_nfe = db.Column(db.Integer, default=0)
    serie_nfce = db.Column(db.Integer, default=1)
    ultimo_numero_nfce = db.Column(db.Integer, default=0)
    csc_id = db.Column(db.String(10))  # ID do CSC para NFCe
    csc_token = db.Column(db.String(100))  # Token CSC para NFCe

    # Configurações de Impressão
    orientacao_danfe = db.Column(db.String(1), default='P')  # P=Retrato, L=Paisagem
    logo_danfe = db.Column(db.Boolean, default=True)

    # Textos Padrão
    info_adicional_padrao = db.Column(db.Text)
    info_fisco_padrao = db.Column(db.Text)

    # Configurações de Email NFe
    email_host_nfe = db.Column(db.String(200))
    email_porta_nfe = db.Column(db.Integer, default=587)
    email_usuario_nfe = db.Column(db.String(200))
    email_senha_nfe = db.Column(db.String(200))
    email_tls_nfe = db.Column(db.Boolean, default=True)
    email_assunto_nfe = db.Column(db.String(200), default='NFe - {numero} - {razao_social}')
    email_corpo_nfe = db.Column(db.Text)

    # Responsável Técnico (obrigatório para NFe 4.00)
    resp_tecnico_cnpj = db.Column(db.String(18))
    resp_tecnico_contato = db.Column(db.String(100))
    resp_tecnico_email = db.Column(db.String(200))
    resp_tecnico_telefone = db.Column(db.String(20))
    resp_tecnico_id_csrt = db.Column(db.String(3))
    resp_tecnico_csrt = db.Column(db.String(100))

    # Auditoria
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_atualizacao_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Relacionamentos
    usuario_atualizacao = db.relationship('User', foreign_keys=[usuario_atualizacao_id])
    certificados = db.relationship('CertificadoDigital', backref='empresa', lazy='dynamic')
    contabilistas = db.relationship('Contabilista', backref='empresa', lazy='dynamic')
    contas_bancarias = db.relationship('ContaBancaria', backref='empresa', lazy='dynamic')

    def get_cnae_secundarios(self):
        if self.cnae_secundarios:
            return json.loads(self.cnae_secundarios)
        return []

    def set_cnae_secundarios(self, lista):
        self.cnae_secundarios = json.dumps(lista)

    def proximo_numero_nfe(self):
        self.ultimo_numero_nfe += 1
        return self.ultimo_numero_nfe

    def proximo_numero_nfce(self):
        self.ultimo_numero_nfce += 1
        return self.ultimo_numero_nfce

    def __repr__(self):
        return f'<Empresa {self.razao_social}>'


class CertificadoDigital(db.Model):
    """Certificado Digital A1/A3 para assinatura de NFe"""
    __tablename__ = 'certificado_digital'

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('configuracao_empresa.id'), nullable=False)

    # Tipo de Certificado
    tipo = db.Column(db.String(2), nullable=False)  # A1 ou A3

    # Dados do Certificado
    nome = db.Column(db.String(200))
    cnpj_certificado = db.Column(db.String(18))
    serial_number = db.Column(db.String(100))
    thumbprint = db.Column(db.String(100))

    # Para A1 - Arquivo PFX
    arquivo_pfx = db.Column(db.LargeBinary)  # Conteúdo do arquivo .pfx
    senha_pfx = db.Column(db.String(100))  # Senha criptografada

    # Para A3 - Token/SmartCard USB
    slot_token = db.Column(db.Integer, default=0)
    biblioteca_token = db.Column(db.String(500))  # Path para .dll/.so
    pin_token = db.Column(db.String(100))  # PIN criptografado

    # Validade
    data_emissao = db.Column(db.Date)
    data_validade = db.Column(db.Date, nullable=False)

    # Status
    ativo = db.Column(db.Boolean, default=True)
    padrao = db.Column(db.Boolean, default=False)  # Certificado padrão

    # Auditoria
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usuario_cadastro_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    usuario_cadastro = db.relationship('User', foreign_keys=[usuario_cadastro_id])

    @property
    def dias_para_vencer(self):
        if self.data_validade:
            delta = self.data_validade - date.today()
            return delta.days
        return None

    @property
    def esta_vencido(self):
        if self.data_validade:
            return self.data_validade < date.today()
        return False

    @property
    def esta_proximo_vencer(self):
        """Retorna True se vence em menos de 30 dias"""
        dias = self.dias_para_vencer
        if dias is not None:
            return 0 < dias <= 30
        return False

    def __repr__(self):
        return f'<Certificado {self.tipo} - {self.nome}>'


class Contabilista(db.Model):
    """Dados do Contabilista/Contador responsável"""
    __tablename__ = 'contabilista'

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('configuracao_empresa.id'), nullable=False)

    # Dados Pessoais/Empresa
    nome = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(14))
    cnpj = db.Column(db.String(18))
    crc = db.Column(db.String(20), nullable=False)  # Registro CRC
    uf_crc = db.Column(db.String(2), nullable=False)

    # Contato
    email = db.Column(db.String(200), nullable=False)
    email_secundario = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20))

    # Endereço
    logradouro = db.Column(db.String(200))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    cep = db.Column(db.String(10))

    # Escritório de Contabilidade
    escritorio_nome = db.Column(db.String(200))
    escritorio_cnpj = db.Column(db.String(18))

    # Configurações de Envio
    receber_nfe_xml = db.Column(db.Boolean, default=True)
    receber_nfe_pdf = db.Column(db.Boolean, default=True)
    receber_nfe_cancelamento = db.Column(db.Boolean, default=True)
    receber_nfe_carta_correcao = db.Column(db.Boolean, default=True)
    receber_relatorios = db.Column(db.Boolean, default=True)
    frequencia_relatorios = db.Column(db.String(20), default='mensal')  # diario, semanal, mensal

    # Status
    ativo = db.Column(db.Boolean, default=True)
    principal = db.Column(db.Boolean, default=False)

    # Auditoria
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Contabilista {self.nome} - CRC {self.crc}>'


class Orcamento(db.Model):
    """Orçamento comercial completo"""
    __tablename__ = 'orcamento'

    id = db.Column(db.Integer, primary_key=True)
    numero_orcamento = db.Column(db.String(20), unique=True, nullable=False)

    # Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    cliente_nome = db.Column(db.String(200), nullable=False)
    cliente_cpf_cnpj = db.Column(db.String(18))
    cliente_email = db.Column(db.String(200))
    cliente_telefone = db.Column(db.String(20))
    cliente_endereco = db.Column(db.String(300))
    cliente_cidade = db.Column(db.String(100))
    cliente_uf = db.Column(db.String(2))
    cliente_cep = db.Column(db.String(10))

    # Vendedor
    vendedor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Status
    status = db.Column(db.String(20), default='rascunho')
    # rascunho, enviado, visualizado, aprovado, reprovado, expirado, convertido

    # Validade
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_validade = db.Column(db.Date, nullable=False)
    data_envio = db.Column(db.DateTime)
    data_visualizacao = db.Column(db.DateTime)
    data_aprovacao = db.Column(db.DateTime)
    data_reprovacao = db.Column(db.DateTime)

    # Valores
    subtotal = db.Column(db.Numeric(15, 2), default=0)
    desconto_percentual = db.Column(db.Numeric(5, 2), default=0)
    desconto_valor = db.Column(db.Numeric(15, 2), default=0)
    valor_frete = db.Column(db.Numeric(15, 2), default=0)
    outras_despesas = db.Column(db.Numeric(15, 2), default=0)
    total = db.Column(db.Numeric(15, 2), default=0)

    # Condições Comerciais
    forma_pagamento = db.Column(db.String(100))
    condicao_pagamento = db.Column(db.String(200))
    prazo_entrega = db.Column(db.String(100))
    frete_tipo = db.Column(db.String(20))  # CIF, FOB
    transportadora = db.Column(db.String(200))

    # Observações
    observacoes = db.Column(db.Text)
    observacoes_internas = db.Column(db.Text)
    condicoes_gerais = db.Column(db.Text)

    # PDF gerado
    pdf_url = db.Column(db.String(500))

    # Token para visualização externa
    token_visualizacao = db.Column(db.String(100), unique=True)

    # Conversão para Pedido/OS/NFe
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordem_servico.id'))
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('nota_fiscal.id'))

    # Relacionamentos
    cliente = db.relationship('Cliente', backref='orcamentos')
    vendedor = db.relationship('User', foreign_keys=[vendedor_id])
    itens = db.relationship('ItemOrcamento', backref='orcamento', lazy='dynamic', cascade='all, delete-orphan')
    historico = db.relationship('HistoricoOrcamento', backref='orcamento', lazy='dynamic', cascade='all, delete-orphan')

    def calcular_total(self):
        """Calcula o total do orçamento"""
        self.subtotal = sum(item.subtotal for item in self.itens)
        desconto = self.desconto_valor or 0
        if self.desconto_percentual:
            desconto += (self.subtotal * self.desconto_percentual / 100)
        self.total = self.subtotal - desconto + (self.valor_frete or 0) + (self.outras_despesas or 0)
        return self.total

    @property
    def esta_vencido(self):
        return self.status not in ['aprovado', 'convertido'] and self.data_validade < date.today()

    @property
    def dias_para_vencer(self):
        if self.data_validade:
            delta = self.data_validade - date.today()
            return delta.days
        return None

    @staticmethod
    def gerar_numero():
        """Gera número único do orçamento"""
        ano = datetime.now().year
        ultimo = Orcamento.query.filter(
            Orcamento.numero_orcamento.like(f'ORC-{ano}-%')
        ).order_by(Orcamento.id.desc()).first()

        if ultimo:
            try:
                ultimo_num = int(ultimo.numero_orcamento.split('-')[-1])
            except:
                ultimo_num = 0
        else:
            ultimo_num = 0

        return f'ORC-{ano}-{str(ultimo_num + 1).zfill(5)}'

    def __repr__(self):
        return f'<Orcamento {self.numero_orcamento}>'


class ItemOrcamento(db.Model):
    """Item do orçamento"""
    __tablename__ = 'item_orcamento'

    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer, db.ForeignKey('orcamento.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))

    # Dados do produto (snapshot)
    codigo = db.Column(db.String(50))
    descricao = db.Column(db.String(500), nullable=False)
    unidade = db.Column(db.String(10), default='UN')
    ncm = db.Column(db.String(10))

    # Quantidades e valores
    quantidade = db.Column(db.Numeric(15, 4), nullable=False)
    preco_unitario = db.Column(db.Numeric(15, 4), nullable=False)
    desconto_percentual = db.Column(db.Numeric(5, 2), default=0)
    desconto_valor = db.Column(db.Numeric(15, 2), default=0)

    # Ordem no orçamento
    ordem = db.Column(db.Integer, default=0)

    # Observações do item
    observacao = db.Column(db.Text)

    # Relacionamentos
    produto = db.relationship('Produto')

    @property
    def subtotal(self):
        valor = self.quantidade * self.preco_unitario
        desconto = self.desconto_valor or 0
        if self.desconto_percentual:
            desconto += (valor * self.desconto_percentual / 100)
        return valor - desconto

    def __repr__(self):
        return f'<ItemOrcamento {self.descricao}>'


class HistoricoOrcamento(db.Model):
    """Histórico de alterações do orçamento"""
    __tablename__ = 'historico_orcamento'

    id = db.Column(db.Integer, primary_key=True)
    orcamento_id = db.Column(db.Integer, db.ForeignKey('orcamento.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tipo = db.Column(db.String(50), nullable=False)  # criacao, edicao, envio, visualizacao, aprovacao, reprovacao
    descricao = db.Column(db.Text)
    status_anterior = db.Column(db.String(20))
    status_novo = db.Column(db.String(20))

    data = db.Column(db.DateTime, default=datetime.utcnow)
    ip_acesso = db.Column(db.String(50))

    usuario = db.relationship('User')


class NotaFiscal(db.Model):
    """Nota Fiscal Eletrônica (NFe) - Modelo 55"""
    __tablename__ = 'nota_fiscal'

    id = db.Column(db.Integer, primary_key=True)

    # Identificação
    modelo = db.Column(db.String(2), default='55')  # 55=NFe, 65=NFCe
    serie = db.Column(db.Integer, nullable=False)
    numero = db.Column(db.Integer, nullable=False)

    # Chave de Acesso (44 dígitos)
    chave_acesso = db.Column(db.String(44), unique=True)

    # Natureza da Operação
    natureza_operacao = db.Column(db.String(100), default='Venda de Mercadoria')
    tipo_operacao = db.Column(db.Integer, default=1)  # 0=Entrada, 1=Saída
    finalidade = db.Column(db.Integer, default=1)  # 1=Normal, 2=Complementar, 3=Ajuste, 4=Devolução

    # Emitente (snapshot da empresa)
    emitente_cnpj = db.Column(db.String(18), nullable=False)
    emitente_razao_social = db.Column(db.String(200), nullable=False)
    emitente_ie = db.Column(db.String(20))
    emitente_endereco = db.Column(db.Text)  # JSON completo

    # Destinatário
    destinatario_tipo = db.Column(db.String(1))  # F=Física, J=Jurídica, E=Exterior
    destinatario_cpf_cnpj = db.Column(db.String(18))
    destinatario_razao_social = db.Column(db.String(200))
    destinatario_ie = db.Column(db.String(20))
    destinatario_email = db.Column(db.String(200))
    destinatario_telefone = db.Column(db.String(20))
    destinatario_endereco = db.Column(db.Text)  # JSON completo

    # Indicadores
    indicador_ie_destinatario = db.Column(db.Integer, default=9)  # 1=Contribuinte, 2=Isento, 9=Não Contribuinte
    indicador_consumidor_final = db.Column(db.Integer, default=1)  # 0=Normal, 1=Consumidor Final
    indicador_presenca = db.Column(db.Integer, default=1)  # 0=Não se aplica, 1=Presencial, etc.

    # Datas
    data_emissao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_saida_entrada = db.Column(db.DateTime)

    # Valores Totais
    valor_produtos = db.Column(db.Numeric(15, 2), default=0)
    valor_frete = db.Column(db.Numeric(15, 2), default=0)
    valor_seguro = db.Column(db.Numeric(15, 2), default=0)
    valor_desconto = db.Column(db.Numeric(15, 2), default=0)
    valor_outras_despesas = db.Column(db.Numeric(15, 2), default=0)
    valor_total = db.Column(db.Numeric(15, 2), default=0)

    # Impostos Totais
    valor_bc_icms = db.Column(db.Numeric(15, 2), default=0)
    valor_icms = db.Column(db.Numeric(15, 2), default=0)
    valor_bc_icms_st = db.Column(db.Numeric(15, 2), default=0)
    valor_icms_st = db.Column(db.Numeric(15, 2), default=0)
    valor_ipi = db.Column(db.Numeric(15, 2), default=0)
    valor_pis = db.Column(db.Numeric(15, 2), default=0)
    valor_cofins = db.Column(db.Numeric(15, 2), default=0)
    valor_ii = db.Column(db.Numeric(15, 2), default=0)  # Imposto Importação
    valor_fcp = db.Column(db.Numeric(15, 2), default=0)  # Fundo Combate Pobreza
    valor_aproximado_tributos = db.Column(db.Numeric(15, 2), default=0)  # Lei de Transparência

    # Transporte
    modalidade_frete = db.Column(db.Integer, default=9)  # 0=Emitente, 1=Destinatário, 2=Terceiros, 9=Sem frete
    transportadora_cnpj = db.Column(db.String(18))
    transportadora_razao_social = db.Column(db.String(200))
    transportadora_ie = db.Column(db.String(20))
    transportadora_endereco = db.Column(db.String(300))
    veiculo_placa = db.Column(db.String(10))
    veiculo_uf = db.Column(db.String(2))

    # Volumes
    quantidade_volumes = db.Column(db.Integer, default=1)
    especie_volumes = db.Column(db.String(50))
    marca_volumes = db.Column(db.String(50))
    numeracao_volumes = db.Column(db.String(50))
    peso_liquido = db.Column(db.Numeric(15, 3), default=0)
    peso_bruto = db.Column(db.Numeric(15, 3), default=0)

    # Cobrança/Pagamento
    forma_pagamento = db.Column(db.String(50))  # 01=Dinheiro, 02=Cheque, 03=Cartão Crédito, etc.
    tipo_pagamento = db.Column(db.Integer, default=0)  # 0=À Vista, 1=À Prazo
    valor_pagamento = db.Column(db.Numeric(15, 2))

    # Duplicatas JSON [{numero, vencimento, valor}]
    duplicatas = db.Column(db.Text)

    # Informações Adicionais
    informacoes_complementares = db.Column(db.Text)
    informacoes_fisco = db.Column(db.Text)

    # Status SEFAZ
    status = db.Column(db.String(30), default='rascunho')
    # rascunho, validada, assinada, transmitida, autorizada, rejeitada, denegada, cancelada, inutilizada

    codigo_status_sefaz = db.Column(db.String(3))
    motivo_status_sefaz = db.Column(db.String(500))
    data_autorizacao = db.Column(db.DateTime)
    protocolo_autorizacao = db.Column(db.String(20))

    # Cancelamento
    cancelada = db.Column(db.Boolean, default=False)
    data_cancelamento = db.Column(db.DateTime)
    protocolo_cancelamento = db.Column(db.String(20))
    justificativa_cancelamento = db.Column(db.String(500))

    # Carta de Correção
    tem_carta_correcao = db.Column(db.Boolean, default=False)

    # XMLs
    xml_nfe = db.Column(db.Text)  # XML da NFe assinada
    xml_autorizacao = db.Column(db.Text)  # XML de retorno da SEFAZ
    xml_cancelamento = db.Column(db.Text)

    # PDFs
    pdf_danfe_url = db.Column(db.String(500))
    pdf_danfe_base64 = db.Column(db.Text)

    # Ambiente
    ambiente = db.Column(db.Integer, default=2)  # 1=Produção, 2=Homologação

    # Referências
    orcamento_id = db.Column(db.Integer, db.ForeignKey('orcamento.id'))
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordem_servico.id'))
    nfe_referenciada = db.Column(db.String(44))  # Chave NFe referenciada

    # Usuário
    usuario_emissao_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Auditoria
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    itens = db.relationship('ItemNotaFiscal', backref='nota_fiscal', lazy='dynamic', cascade='all, delete-orphan')
    cartas_correcao = db.relationship('CartaCorrecao', backref='nota_fiscal', lazy='dynamic')
    envios_email = db.relationship('EnvioEmailNFe', backref='nota_fiscal', lazy='dynamic')
    usuario_emissao = db.relationship('User', foreign_keys=[usuario_emissao_id])
    orcamento = db.relationship('Orcamento', backref='notas_fiscais')

    def get_duplicatas(self):
        if self.duplicatas:
            return json.loads(self.duplicatas)
        return []

    def set_duplicatas(self, lista):
        self.duplicatas = json.dumps(lista)

    def calcular_totais(self):
        """Recalcula todos os totais da NFe"""
        self.valor_produtos = sum(item.valor_total for item in self.itens)
        self.valor_icms = sum(item.valor_icms for item in self.itens)
        self.valor_ipi = sum(item.valor_ipi for item in self.itens)
        self.valor_pis = sum(item.valor_pis for item in self.itens)
        self.valor_cofins = sum(item.valor_cofins for item in self.itens)
        self.valor_aproximado_tributos = sum(item.valor_aproximado_tributos for item in self.itens)

        self.valor_total = (
            self.valor_produtos
            + (self.valor_frete or 0)
            + (self.valor_seguro or 0)
            + (self.valor_outras_despesas or 0)
            + (self.valor_ipi or 0)
            + (self.valor_icms_st or 0)
            - (self.valor_desconto or 0)
        )

        return self.valor_total

    @staticmethod
    def gerar_chave_acesso(uf, ano_mes, cnpj, modelo, serie, numero, tipo_emissao, codigo_numerico):
        """Gera a chave de acesso de 44 dígitos"""
        # cUF(2) + AAMM(4) + CNPJ(14) + mod(2) + serie(3) + nNF(9) + tpEmis(1) + cNF(8) + cDV(1)
        chave = f"{uf}{ano_mes}{cnpj.replace('.', '').replace('/', '').replace('-', '')}"
        chave += f"{str(modelo).zfill(2)}{str(serie).zfill(3)}{str(numero).zfill(9)}"
        chave += f"{tipo_emissao}{str(codigo_numerico).zfill(8)}"

        # Calcular dígito verificador (módulo 11)
        pesos = [2, 3, 4, 5, 6, 7, 8, 9]
        soma = 0
        for i, digito in enumerate(reversed(chave)):
            soma += int(digito) * pesos[i % 8]

        resto = soma % 11
        dv = 0 if resto < 2 else 11 - resto

        return chave + str(dv)

    def __repr__(self):
        return f'<NFe {self.numero} - {self.chave_acesso}>'


class ItemNotaFiscal(db.Model):
    """Item da Nota Fiscal"""
    __tablename__ = 'item_nota_fiscal'

    id = db.Column(db.Integer, primary_key=True)
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('nota_fiscal.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))

    # Número do item na NFe
    numero_item = db.Column(db.Integer, nullable=False)

    # Produto
    codigo = db.Column(db.String(60), nullable=False)
    descricao = db.Column(db.String(500), nullable=False)
    ncm = db.Column(db.String(8), nullable=False)
    cest = db.Column(db.String(7))  # Código Especificador da Substituição Tributária
    cfop = db.Column(db.String(4), nullable=False)
    unidade = db.Column(db.String(6), default='UN')

    # EAN/GTIN
    ean = db.Column(db.String(14))
    ean_tributavel = db.Column(db.String(14))

    # Quantidades
    quantidade = db.Column(db.Numeric(15, 4), nullable=False)
    quantidade_tributavel = db.Column(db.Numeric(15, 4))
    unidade_tributavel = db.Column(db.String(6))

    # Valores
    valor_unitario = db.Column(db.Numeric(21, 10), nullable=False)
    valor_unitario_tributavel = db.Column(db.Numeric(21, 10))
    valor_total = db.Column(db.Numeric(15, 2), nullable=False)
    valor_frete = db.Column(db.Numeric(15, 2), default=0)
    valor_seguro = db.Column(db.Numeric(15, 2), default=0)
    valor_desconto = db.Column(db.Numeric(15, 2), default=0)
    valor_outras_despesas = db.Column(db.Numeric(15, 2), default=0)

    # ICMS
    origem = db.Column(db.String(1), default='0')  # Origem da mercadoria
    cst_icms = db.Column(db.String(3))  # CST ou CSOSN
    modalidade_bc_icms = db.Column(db.Integer)  # 0=Margem, 1=Pauta, 2=Preço Tabelado, 3=Valor Operação
    valor_bc_icms = db.Column(db.Numeric(15, 2), default=0)
    aliquota_icms = db.Column(db.Numeric(5, 2), default=0)
    valor_icms = db.Column(db.Numeric(15, 2), default=0)

    # ICMS ST
    modalidade_bc_icms_st = db.Column(db.Integer)
    mva_icms_st = db.Column(db.Numeric(5, 2))  # Margem Valor Agregado
    valor_bc_icms_st = db.Column(db.Numeric(15, 2), default=0)
    aliquota_icms_st = db.Column(db.Numeric(5, 2), default=0)
    valor_icms_st = db.Column(db.Numeric(15, 2), default=0)

    # IPI
    cst_ipi = db.Column(db.String(2))
    valor_bc_ipi = db.Column(db.Numeric(15, 2), default=0)
    aliquota_ipi = db.Column(db.Numeric(5, 2), default=0)
    valor_ipi = db.Column(db.Numeric(15, 2), default=0)

    # PIS
    cst_pis = db.Column(db.String(2), default='07')  # 07=Isento para Simples Nacional
    valor_bc_pis = db.Column(db.Numeric(15, 2), default=0)
    aliquota_pis = db.Column(db.Numeric(5, 2), default=0)
    valor_pis = db.Column(db.Numeric(15, 2), default=0)

    # COFINS
    cst_cofins = db.Column(db.String(2), default='07')  # 07=Isento para Simples Nacional
    valor_bc_cofins = db.Column(db.Numeric(15, 2), default=0)
    aliquota_cofins = db.Column(db.Numeric(5, 2), default=0)
    valor_cofins = db.Column(db.Numeric(15, 2), default=0)

    # Lei da Transparência (Lei 12.741/2012)
    valor_aproximado_tributos = db.Column(db.Numeric(15, 2), default=0)
    percentual_tributos_federais = db.Column(db.Numeric(5, 2), default=0)
    percentual_tributos_estaduais = db.Column(db.Numeric(5, 2), default=0)
    percentual_tributos_municipais = db.Column(db.Numeric(5, 2), default=0)

    # Informações adicionais do item
    informacoes_adicionais = db.Column(db.Text)

    # Relacionamento
    produto = db.relationship('Produto')

    def calcular_impostos(self, regime_tributario=1, uf_origem='RS', uf_destino='RS'):
        """Calcula impostos baseado no regime tributário e operação"""
        # Valor base
        self.valor_total = self.quantidade * self.valor_unitario - (self.valor_desconto or 0)

        if regime_tributario == 1:  # Simples Nacional
            # CSOSN para Simples Nacional
            if self.cst_icms is None:
                self.cst_icms = '102'  # Tributada sem permissão de crédito

            self.cst_pis = '07'  # Isento
            self.cst_cofins = '07'  # Isento

        else:  # Regime Normal
            if self.cst_icms is None:
                self.cst_icms = '00'  # Tributada integralmente

            # ICMS
            if self.cst_icms == '00':
                self.valor_bc_icms = self.valor_total
                if uf_origem == uf_destino:
                    self.aliquota_icms = Decimal('17.00')  # Interna RS
                else:
                    self.aliquota_icms = Decimal('12.00')  # Interestadual Sul/Sudeste
                self.valor_icms = self.valor_bc_icms * self.aliquota_icms / 100

            # PIS e COFINS
            self.cst_pis = '01'  # Tributável
            self.valor_bc_pis = self.valor_total
            self.aliquota_pis = Decimal('1.65')
            self.valor_pis = self.valor_bc_pis * self.aliquota_pis / 100

            self.cst_cofins = '01'  # Tributável
            self.valor_bc_cofins = self.valor_total
            self.aliquota_cofins = Decimal('7.60')
            self.valor_cofins = self.valor_bc_cofins * self.aliquota_cofins / 100

        # Cálculo aproximado de tributos (Lei de Transparência)
        # Valores aproximados por NCM - simplificado
        self.percentual_tributos_federais = Decimal('15.00')
        self.percentual_tributos_estaduais = Decimal('17.00')
        self.valor_aproximado_tributos = self.valor_total * (
            self.percentual_tributos_federais + self.percentual_tributos_estaduais
        ) / 100

        return self.valor_total

    def __repr__(self):
        return f'<ItemNFe {self.numero_item} - {self.descricao}>'


class CartaCorrecao(db.Model):
    """Carta de Correção Eletrônica (CC-e)"""
    __tablename__ = 'carta_correcao'

    id = db.Column(db.Integer, primary_key=True)
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('nota_fiscal.id'), nullable=False)

    sequencia = db.Column(db.Integer, nullable=False)  # Número sequencial da CC-e
    correcao = db.Column(db.Text, nullable=False)  # Texto da correção (15-1000 chars)

    # SEFAZ
    data_evento = db.Column(db.DateTime, default=datetime.utcnow)
    protocolo = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pendente')  # pendente, autorizada, rejeitada
    codigo_status = db.Column(db.String(3))
    motivo_status = db.Column(db.String(500))

    # XML
    xml_evento = db.Column(db.Text)
    xml_retorno = db.Column(db.Text)

    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    usuario = db.relationship('User')

    def __repr__(self):
        return f'<CC-e {self.sequencia} - NFe {self.nota_fiscal_id}>'


class EnvioEmailNFe(db.Model):
    """Registro de envios de email de NFe"""
    __tablename__ = 'envio_email_nfe'

    id = db.Column(db.Integer, primary_key=True)
    nota_fiscal_id = db.Column(db.Integer, db.ForeignKey('nota_fiscal.id'), nullable=False)

    destinatario = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(50))  # nfe, cancelamento, carta_correcao

    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    enviado = db.Column(db.Boolean, default=False)
    erro = db.Column(db.Text)

    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    usuario = db.relationship('User')


class ContaBancaria(db.Model):
    """Conta bancária da empresa para integração"""
    __tablename__ = 'conta_bancaria'

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('configuracao_empresa.id'), nullable=False)

    # Dados bancários
    banco_codigo = db.Column(db.String(3), nullable=False)
    banco_nome = db.Column(db.String(100))
    agencia = db.Column(db.String(10), nullable=False)
    agencia_digito = db.Column(db.String(2))
    conta = db.Column(db.String(20), nullable=False)
    conta_digito = db.Column(db.String(2))
    tipo_conta = db.Column(db.String(20), default='corrente')  # corrente, poupanca

    # Titular
    titular = db.Column(db.String(200))
    cpf_cnpj_titular = db.Column(db.String(18))

    # Integração API Bancária
    api_client_id = db.Column(db.String(200))
    api_client_secret = db.Column(db.String(200))
    api_token = db.Column(db.Text)
    api_token_expira = db.Column(db.DateTime)
    api_ambiente = db.Column(db.String(20), default='sandbox')  # sandbox, producao

    # Webhook
    webhook_url = db.Column(db.String(500))
    webhook_secret = db.Column(db.String(200))

    # PIX
    pix_chave = db.Column(db.String(100))
    pix_tipo_chave = db.Column(db.String(20))  # cpf, cnpj, email, telefone, aleatoria

    # Status
    ativo = db.Column(db.Boolean, default=True)
    principal = db.Column(db.Boolean, default=False)

    # Saldo (atualizado periodicamente)
    saldo_atual = db.Column(db.Numeric(15, 2), default=0)
    data_ultimo_saldo = db.Column(db.DateTime)

    # Auditoria
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    transacoes = db.relationship('TransacaoBancaria', backref='conta', lazy='dynamic')

    @property
    def conta_formatada(self):
        return f"{self.agencia}-{self.agencia_digito or '0'} / {self.conta}-{self.conta_digito or '0'}"

    def __repr__(self):
        return f'<ContaBancaria {self.banco_nome} - {self.conta}>'


class TransacaoBancaria(db.Model):
    """Transações bancárias importadas/registradas"""
    __tablename__ = 'transacao_bancaria'

    id = db.Column(db.Integer, primary_key=True)
    conta_id = db.Column(db.Integer, db.ForeignKey('conta_bancaria.id'), nullable=False)

    # Identificação
    id_externo = db.Column(db.String(100))  # ID da transação no banco
    tipo = db.Column(db.String(20), nullable=False)  # credito, debito, transferencia, pix

    # Valores
    valor = db.Column(db.Numeric(15, 2), nullable=False)
    saldo_pos = db.Column(db.Numeric(15, 2))  # Saldo após transação

    # Descrição
    descricao = db.Column(db.String(500))
    categoria = db.Column(db.String(100))

    # Data
    data_transacao = db.Column(db.DateTime, nullable=False)
    data_compensacao = db.Column(db.DateTime)

    # Contraparte
    contraparte_nome = db.Column(db.String(200))
    contraparte_cpf_cnpj = db.Column(db.String(18))
    contraparte_banco = db.Column(db.String(100))
    contraparte_agencia = db.Column(db.String(10))
    contraparte_conta = db.Column(db.String(20))

    # Conciliação
    conciliada = db.Column(db.Boolean, default=False)
    conta_pagar_id = db.Column(db.Integer, db.ForeignKey('conta_pagar.id'))
    conta_receber_id = db.Column(db.Integer, db.ForeignKey('conta_receber.id'))
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'))

    # Auditoria
    data_importacao = db.Column(db.DateTime, default=datetime.utcnow)
    importado_por_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    importado_por = db.relationship('User')

    def __repr__(self):
        return f'<TransacaoBancaria {self.tipo} R${self.valor}>'


class ConfiguracaoImposto(db.Model):
    """Configurações de impostos por NCM/CFOP"""
    __tablename__ = 'configuracao_imposto'

    id = db.Column(db.Integer, primary_key=True)

    # Identificação
    ncm = db.Column(db.String(8))
    cfop = db.Column(db.String(4))
    uf_origem = db.Column(db.String(2))
    uf_destino = db.Column(db.String(2))

    # ICMS
    cst_icms = db.Column(db.String(3))
    aliquota_icms = db.Column(db.Numeric(5, 2))
    reducao_bc_icms = db.Column(db.Numeric(5, 2))

    # ICMS ST
    mva = db.Column(db.Numeric(5, 2))
    aliquota_icms_st = db.Column(db.Numeric(5, 2))

    # IPI
    cst_ipi = db.Column(db.String(2))
    aliquota_ipi = db.Column(db.Numeric(5, 2))

    # PIS
    cst_pis = db.Column(db.String(2))
    aliquota_pis = db.Column(db.Numeric(5, 2))

    # COFINS
    cst_cofins = db.Column(db.String(2))
    aliquota_cofins = db.Column(db.Numeric(5, 2))

    # Lei de Transparência
    percentual_federal = db.Column(db.Numeric(5, 2))
    percentual_estadual = db.Column(db.Numeric(5, 2))
    percentual_municipal = db.Column(db.Numeric(5, 2))

    # Status
    ativo = db.Column(db.Boolean, default=True)

    # Auditoria
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<ConfigImposto NCM:{self.ncm} CFOP:{self.cfop}>'


class InutilizacaoNFe(db.Model):
    """Registro de inutilização de numeração de NFe"""
    __tablename__ = 'inutilizacao_nfe'

    id = db.Column(db.Integer, primary_key=True)

    ano = db.Column(db.Integer, nullable=False)
    modelo = db.Column(db.String(2), default='55')
    serie = db.Column(db.Integer, nullable=False)
    numero_inicial = db.Column(db.Integer, nullable=False)
    numero_final = db.Column(db.Integer, nullable=False)

    justificativa = db.Column(db.String(500), nullable=False)

    # SEFAZ
    protocolo = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pendente')
    codigo_status = db.Column(db.String(3))
    motivo_status = db.Column(db.String(500))
    data_inutilizacao = db.Column(db.DateTime)

    # XML
    xml_pedido = db.Column(db.Text)
    xml_retorno = db.Column(db.Text)

    # Auditoria
    usuario_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('User')

    def __repr__(self):
        return f'<Inutilização {self.numero_inicial}-{self.numero_final}>'
