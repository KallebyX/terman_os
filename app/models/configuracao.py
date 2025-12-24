"""
Modelo para configuracoes do sistema
Permite Super Admin gerenciar tokens e variaveis de ambiente via interface visual
"""
from app import db
from datetime import datetime


class Configuracao(db.Model):
    """Configuracoes do sistema armazenadas no banco de dados"""
    __tablename__ = 'configuracoes'

    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), unique=True, nullable=False, index=True)
    valor = db.Column(db.Text)
    descricao = db.Column(db.String(255))
    tipo = db.Column(db.String(20), default='string')  # string, integer, boolean, secret
    categoria = db.Column(db.String(50), default='geral')  # geral, email, pagamento, api, seguranca
    editavel = db.Column(db.Boolean, default=True)
    visivel = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    atualizado_por = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Configuracao {self.chave}>'

    @classmethod
    def get(cls, chave, default=None):
        """Obter valor de uma configuracao"""
        config = cls.query.filter_by(chave=chave).first()
        if config:
            if config.tipo == 'integer':
                return int(config.valor) if config.valor else default
            elif config.tipo == 'boolean':
                return config.valor.lower() in ('true', '1', 'sim', 'yes') if config.valor else default
            return config.valor
        return default

    @classmethod
    def set(cls, chave, valor, usuario_id=None, descricao=None, tipo='string', categoria='geral'):
        """Definir ou atualizar uma configuracao"""
        config = cls.query.filter_by(chave=chave).first()
        if config:
            config.valor = str(valor) if valor is not None else None
            config.atualizado_por = usuario_id
            if descricao:
                config.descricao = descricao
        else:
            config = cls(
                chave=chave,
                valor=str(valor) if valor is not None else None,
                descricao=descricao,
                tipo=tipo,
                categoria=categoria,
                atualizado_por=usuario_id
            )
            db.session.add(config)

        db.session.commit()
        return config

    @classmethod
    def get_by_categoria(cls, categoria):
        """Obter todas as configuracoes de uma categoria"""
        return cls.query.filter_by(categoria=categoria, visivel=True).order_by(cls.chave).all()

    @classmethod
    def get_all_editaveis(cls):
        """Obter todas as configuracoes editaveis"""
        return cls.query.filter_by(editavel=True, visivel=True).order_by(cls.categoria, cls.chave).all()

    @classmethod
    def init_defaults(cls):
        """Inicializar configuracoes padrao se nao existirem"""
        defaults = [
            # Geral
            {'chave': 'NOME_EMPRESA', 'valor': 'Mangueiras Terman', 'descricao': 'Nome da empresa', 'categoria': 'geral'},
            {'chave': 'CNPJ_EMPRESA', 'valor': '04.625.577/0001-40', 'descricao': 'CNPJ da empresa', 'categoria': 'geral'},
            {'chave': 'TELEFONE_EMPRESA', 'valor': '(55) 99710-8864', 'descricao': 'Telefone principal', 'categoria': 'geral'},
            {'chave': 'EMAIL_EMPRESA', 'valor': 'contato@mangueirasterman.com.br', 'descricao': 'Email de contato', 'categoria': 'geral'},

            # Email
            {'chave': 'MAIL_SERVER', 'valor': 'smtp.gmail.com', 'descricao': 'Servidor SMTP', 'categoria': 'email'},
            {'chave': 'MAIL_PORT', 'valor': '587', 'descricao': 'Porta SMTP', 'tipo': 'integer', 'categoria': 'email'},
            {'chave': 'MAIL_USERNAME', 'valor': '', 'descricao': 'Usuario SMTP', 'categoria': 'email'},
            {'chave': 'MAIL_PASSWORD', 'valor': '', 'descricao': 'Senha SMTP', 'tipo': 'secret', 'categoria': 'email'},
            {'chave': 'MAIL_USE_TLS', 'valor': 'true', 'descricao': 'Usar TLS', 'tipo': 'boolean', 'categoria': 'email'},

            # APIs Externas
            {'chave': 'GOOGLE_ANALYTICS_ID', 'valor': '', 'descricao': 'ID do Google Analytics', 'categoria': 'api'},
            {'chave': 'GOOGLE_MAPS_API_KEY', 'valor': '', 'descricao': 'Chave API Google Maps', 'tipo': 'secret', 'categoria': 'api'},
            {'chave': 'RECAPTCHA_SITE_KEY', 'valor': '', 'descricao': 'Chave publica reCAPTCHA', 'categoria': 'api'},
            {'chave': 'RECAPTCHA_SECRET_KEY', 'valor': '', 'descricao': 'Chave secreta reCAPTCHA', 'tipo': 'secret', 'categoria': 'api'},

            # Pagamento
            {'chave': 'MERCADO_PAGO_PUBLIC_KEY', 'valor': '', 'descricao': 'Chave publica Mercado Pago', 'categoria': 'pagamento'},
            {'chave': 'MERCADO_PAGO_ACCESS_TOKEN', 'valor': '', 'descricao': 'Access Token Mercado Pago', 'tipo': 'secret', 'categoria': 'pagamento'},
            {'chave': 'STRIPE_PUBLIC_KEY', 'valor': '', 'descricao': 'Chave publica Stripe', 'categoria': 'pagamento'},
            {'chave': 'STRIPE_SECRET_KEY', 'valor': '', 'descricao': 'Chave secreta Stripe', 'tipo': 'secret', 'categoria': 'pagamento'},
            {'chave': 'PIX_CHAVE', 'valor': '', 'descricao': 'Chave PIX para recebimentos', 'categoria': 'pagamento'},

            # WhatsApp/Comunicacao
            {'chave': 'WHATSAPP_NUMERO', 'valor': '5555997108864', 'descricao': 'Numero WhatsApp (com DDI)', 'categoria': 'comunicacao'},
            {'chave': 'WHATSAPP_API_TOKEN', 'valor': '', 'descricao': 'Token API WhatsApp Business', 'tipo': 'secret', 'categoria': 'comunicacao'},
            {'chave': 'TELEGRAM_BOT_TOKEN', 'valor': '', 'descricao': 'Token do Bot Telegram', 'tipo': 'secret', 'categoria': 'comunicacao'},

            # Seguranca
            {'chave': 'TAXA_LIMITE_LOGIN', 'valor': '10', 'descricao': 'Tentativas de login por minuto', 'tipo': 'integer', 'categoria': 'seguranca'},
            {'chave': 'TEMPO_SESSAO', 'valor': '3600', 'descricao': 'Tempo de sessao em segundos', 'tipo': 'integer', 'categoria': 'seguranca'},
            {'chave': 'HABILITAR_2FA', 'valor': 'false', 'descricao': 'Habilitar autenticacao 2 fatores', 'tipo': 'boolean', 'categoria': 'seguranca'},

            # Loja
            {'chave': 'LOJA_ATIVA', 'valor': 'true', 'descricao': 'Loja online ativa', 'tipo': 'boolean', 'categoria': 'loja'},
            {'chave': 'PEDIDO_MINIMO', 'valor': '0', 'descricao': 'Valor minimo do pedido (R$)', 'tipo': 'integer', 'categoria': 'loja'},
            {'chave': 'FRETE_GRATIS_ACIMA', 'valor': '500', 'descricao': 'Frete gratis acima de (R$)', 'tipo': 'integer', 'categoria': 'loja'},
            {'chave': 'ESTOQUE_BAIXO_ALERTA', 'valor': '10', 'descricao': 'Alerta estoque baixo (unidades)', 'tipo': 'integer', 'categoria': 'loja'},
        ]

        for conf in defaults:
            if not cls.query.filter_by(chave=conf['chave']).first():
                nova_config = cls(
                    chave=conf['chave'],
                    valor=conf.get('valor', ''),
                    descricao=conf.get('descricao', ''),
                    tipo=conf.get('tipo', 'string'),
                    categoria=conf.get('categoria', 'geral')
                )
                db.session.add(nova_config)

        db.session.commit()
