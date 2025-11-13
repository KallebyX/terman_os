from app import db
from datetime import datetime

class Produto(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=True)  # SKU/Código do produto
    nome = db.Column(db.String(200), nullable=False, index=True)
    descricao = db.Column(db.Text, nullable=True)
    descricao_curta = db.Column(db.String(500), nullable=True)
    especificacoes = db.Column(db.Text, nullable=True)  # JSON com specs técnicas
    preco = db.Column(db.Float, nullable=False)
    preco_custo = db.Column(db.Float, nullable=True)  # Para cálculo de margem
    preco_promocional = db.Column(db.Float, nullable=True)
    imagem_url = db.Column(db.String(255), nullable=True)
    imagens_adicionais = db.Column(db.Text, nullable=True)  # JSON array de URLs

    # Relacionamento com Categoria
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True, index=True)
    categoria = db.relationship('Categoria', backref=db.backref('produtos', lazy='dynamic'))

    # Controle
    ativo = db.Column(db.Boolean, default=True, index=True)
    destaque = db.Column(db.Boolean, default=False)  # Produto em destaque
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # SEO
    meta_title = db.Column(db.String(200), nullable=True)
    meta_description = db.Column(db.String(500), nullable=True)
    slug = db.Column(db.String(200), unique=True, nullable=True, index=True)

    # Métricas
    visualizacoes = db.Column(db.Integer, default=0)
    vendas_total = db.Column(db.Integer, default=0)

    # Relacionamentos
    estoques = db.relationship('Estoque', backref='produto', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='produto', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def estoque_total(self):
        """Retorna quantidade total em estoque somando todas as localizações"""
        return sum([e.quantidade for e in self.estoques]) if self.estoques else 0

    @property
    def preco_final(self):
        """Retorna preço promocional se existir, senão preço normal"""
        return self.preco_promocional if self.preco_promocional else self.preco

    @property
    def margem_lucro(self):
        """Calcula margem de lucro em %"""
        if self.preco_custo and self.preco_custo > 0:
            return ((self.preco - self.preco_custo) / self.preco_custo) * 100
        return 0

    @property
    def rating_medio(self):
        """Calcula rating médio baseado em reviews"""
        reviews_list = list(self.reviews)
        if reviews_list:
            return sum([r.rating for r in reviews_list]) / len(reviews_list)
        return 0

    def __repr__(self):
        return f'<Produto {self.nome}>'