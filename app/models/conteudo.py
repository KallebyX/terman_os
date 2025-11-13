"""
Modelos de Conteúdo
Blog, FAQ, Depoimentos e outros conteúdos do site
"""
from app import db
from datetime import datetime


class Post(db.Model):
    """Posts do blog"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)

    # Conteúdo
    resumo = db.Column(db.Text, nullable=True)
    conteudo = db.Column(db.Text, nullable=False)
    imagem_destaque = db.Column(db.String(300), nullable=True)

    # Categorização
    categoria = db.Column(db.String(100), nullable=True, index=True)
    tags = db.Column(db.String(300), nullable=True)  # separadas por vírgula

    # Autor
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Publicação
    status = db.Column(db.String(20), default='rascunho', index=True)  # rascunho, publicado, arquivado
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_publicacao = db.Column(db.DateTime, nullable=True, index=True)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # SEO
    meta_title = db.Column(db.String(200), nullable=True)
    meta_description = db.Column(db.String(500), nullable=True)

    # Métricas
    visualizacoes = db.Column(db.Integer, default=0)

    # Configurações
    permite_comentarios = db.Column(db.Boolean, default=True)
    destaque = db.Column(db.Boolean, default=False)

    # Relacionamentos
    autor = db.relationship('User', backref='posts')
    comentarios = db.relationship('ComentarioPost', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Post {self.titulo}>'


class ComentarioPost(db.Model):
    """Comentários em posts do blog"""
    __tablename__ = 'comentarios_post'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False, index=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Conteúdo
    nome = db.Column(db.String(200), nullable=False)  # Nome do comentarista
    email = db.Column(db.String(120), nullable=True)  # Se não for usuário registrado
    comentario = db.Column(db.Text, nullable=False)

    # Moderação
    aprovado = db.Column(db.Boolean, default=False, index=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relacionamento
    usuario = db.relationship('User', backref='comentarios_blog')

    def __repr__(self):
        return f'<ComentarioPost por {self.nome}>'


class FAQ(db.Model):
    """Perguntas frequentes"""
    __tablename__ = 'faqs'

    id = db.Column(db.Integer, primary_key=True)

    # Conteúdo
    pergunta = db.Column(db.Text, nullable=False)
    resposta = db.Column(db.Text, nullable=False)

    # Categorização
    categoria = db.Column(db.String(100), nullable=True, index=True)
    ordem = db.Column(db.Integer, default=0)  # Para ordenação

    # Status
    ativo = db.Column(db.Boolean, default=True, index=True)
    destaque = db.Column(db.Boolean, default=False)

    # Métricas
    visualizacoes = db.Column(db.Integer, default=0)
    util_count = db.Column(db.Integer, default=0)  # Quantas pessoas acharam útil

    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<FAQ {self.pergunta[:50]}...>'


class Depoimento(db.Model):
    """Depoimentos de clientes"""
    __tablename__ = 'depoimentos'

    id = db.Column(db.Integer, primary_key=True)

    # Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id', ondelete='SET NULL'), nullable=True)
    nome_cliente = db.Column(db.String(200), nullable=False)
    empresa = db.Column(db.String(200), nullable=True)
    cargo = db.Column(db.String(100), nullable=True)
    foto_url = db.Column(db.String(300), nullable=True)

    # Conteúdo
    depoimento = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # 1-5 estrelas

    # Moderação
    aprovado = db.Column(db.Boolean, default=False, index=True)
    destaque = db.Column(db.Boolean, default=False)

    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_aprovacao = db.Column(db.DateTime, nullable=True)

    # Relacionamento
    cliente = db.relationship('Cliente', backref='depoimentos')

    def __repr__(self):
        return f'<Depoimento de {self.nome_cliente}>'


class Contato(db.Model):
    """Mensagens de contato do site"""
    __tablename__ = 'contatos'

    id = db.Column(db.Integer, primary_key=True)

    # Dados do contato
    nome = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    empresa = db.Column(db.String(200), nullable=True)

    # Mensagem
    assunto = db.Column(db.String(200), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

    # Tipo de interesse
    tipo = db.Column(db.String(50), nullable=True)  # orcamento, duvida, reclamacao, sugestao

    # Status
    status = db.Column(db.String(50), default='novo', index=True)  # novo, lido, respondido, arquivado
    atribuido_a_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Datas
    data_envio = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_leitura = db.Column(db.DateTime, nullable=True)
    data_resposta = db.Column(db.DateTime, nullable=True)

    # Resposta
    resposta = db.Column(db.Text, nullable=True)
    respondido_por_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    # Relacionamentos
    atribuido_a = db.relationship('User', foreign_keys=[atribuido_a_id], backref='contatos_atribuidos')
    respondido_por = db.relationship('User', foreign_keys=[respondido_por_id], backref='contatos_respondidos')

    def __repr__(self):
        return f'<Contato de {self.nome} | {self.assunto}>'


class Newsletter(db.Model):
    """Inscritos na newsletter"""
    __tablename__ = 'newsletter'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(200), nullable=True)

    # Status
    ativo = db.Column(db.Boolean, default=True, index=True)
    confirmado = db.Column(db.Boolean, default=False)  # Email confirmado

    # Token de confirmação
    token_confirmacao = db.Column(db.String(100), unique=True, nullable=True)
    token_unsubscribe = db.Column(db.String(100), unique=True, nullable=True)

    # Datas
    data_inscricao = db.Column(db.DateTime, default=datetime.utcnow)
    data_confirmacao = db.Column(db.DateTime, nullable=True)
    data_cancelamento = db.Column(db.DateTime, nullable=True)

    # Origem
    origem = db.Column(db.String(100), nullable=True)  # homepage, checkout, blog

    def __repr__(self):
        return f'<Newsletter {self.email}>'


class Banner(db.Model):
    """Banners e slides da homepage"""
    __tablename__ = 'banners'

    id = db.Column(db.Integer, primary_key=True)

    # Conteúdo
    titulo = db.Column(db.String(200), nullable=False)
    subtitulo = db.Column(db.String(300), nullable=True)
    imagem_url = db.Column(db.String(300), nullable=False)
    imagem_mobile_url = db.Column(db.String(300), nullable=True)

    # Link
    link_url = db.Column(db.String(300), nullable=True)
    link_texto = db.Column(db.String(100), nullable=True)  # Texto do botão CTA
    link_externo = db.Column(db.Boolean, default=False)

    # Posicionamento
    posicao = db.Column(db.String(50), default='principal')  # principal, secundario, lateral
    ordem = db.Column(db.Integer, default=0)

    # Status
    ativo = db.Column(db.Boolean, default=True, index=True)

    # Agendamento
    data_inicio = db.Column(db.DateTime, nullable=True)
    data_fim = db.Column(db.DateTime, nullable=True)

    # Métricas
    visualizacoes = db.Column(db.Integer, default=0)
    cliques = db.Column(db.Integer, default=0)

    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Banner {self.titulo}>'
