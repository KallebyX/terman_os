"""
Modelos do Terman OS
Importações centralizadas de todos os modelos do sistema
"""

# Modelos Core
from .user import User
from .categoria import Categoria

# Modelos de Produto e Estoque
from .produto import Produto
from .estoque import Estoque, MovimentacaoEstoque, Review

# Modelos de Pedidos
from .pedido import Pedido, ItemPedido, HistoricoPedido

# Modelos CRM (Customer Relationship Management)
from .crm import (
    Cliente,
    EnderecoCliente,
    Lead,
    Oportunidade,
    Interacao,
    Atividade,
    Proposta,
    ItemProposta
)

# Modelos ERP (Enterprise Resource Planning)
from .erp import (
    Fornecedor,
    ProdutoFornecedor,
    Compra,
    ItemCompra,
    RecebimentoCompra,
    ItemRecebimento,
    ContaPagar,
    PagamentoCP,
    ContaReceber,
    RecebimentoCR
)

# Modelos de Manufatura/Indústria
from .manufatura import (
    OrdemServico,
    ProdutoOS,
    AnexoOS,
    HistoricoOS,
    OrdemProducao,
    InspecaoQualidade
)

# Modelos de Conteúdo (Site Institucional)
from .conteudo import (
    Post,
    ComentarioPost,
    FAQ,
    Depoimento,
    Contato,
    Newsletter,
    Banner
)

# Modelo legado (manter por compatibilidade)
from .ordem_servico import OrdemServico as OrdemServicoLegacy

__all__ = [
    # Core
    'User',
    'Categoria',
    # Produtos
    'Produto',
    'Estoque',
    'MovimentacaoEstoque',
    'Review',
    # Pedidos
    'Pedido',
    'ItemPedido',
    'HistoricoPedido',
    # CRM
    'Cliente',
    'EnderecoCliente',
    'Lead',
    'Oportunidade',
    'Interacao',
    'Atividade',
    'Proposta',
    'ItemProposta',
    # ERP
    'Fornecedor',
    'ProdutoFornecedor',
    'Compra',
    'ItemCompra',
    'RecebimentoCompra',
    'ItemRecebimento',
    'ContaPagar',
    'PagamentoCP',
    'ContaReceber',
    'RecebimentoCR',
    # Manufatura
    'OrdemServico',
    'ProdutoOS',
    'AnexoOS',
    'HistoricoOS',
    'OrdemProducao',
    'InspecaoQualidade',
    # Conteúdo
    'Post',
    'ComentarioPost',
    'FAQ',
    'Depoimento',
    'Contato',
    'Newsletter',
    'Banner',
]