"""
Blueprint Dashboard BI - Business Intelligence
Dashboards, KPIs e Análises com Chart.js
"""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.decorators import admin_required
from app.models import (
    Pedido, ItemPedido, Produto, Estoque, Cliente, Lead,
    Oportunidade, ContaPagar, ContaReceber, User, Categoria
)
from app import db
from sqlalchemy import func, extract
from datetime import datetime, timedelta
import json

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
@admin_required
def index():
    """Dashboard principal com visão geral"""
    # KPIs básicos
    total_vendas = db.session.query(func.sum(Pedido.total)).scalar() or 0
    total_pedidos = Pedido.query.count()
    total_produtos = Produto.query.filter_by(ativo=True).count()
    total_clientes = Cliente.query.filter_by(ativo=True).count()

    # Ticket médio
    ticket_medio = total_vendas / total_pedidos if total_pedidos > 0 else 0

    # Pedidos por status
    pedidos_pendentes = Pedido.query.filter_by(status='pendente').count()
    pedidos_enviados = Pedido.query.filter_by(status='enviado').count()

    # Estoque baixo
    produtos_estoque_baixo = db.session.query(Produto).join(Estoque).filter(
        Estoque.quantidade <= Estoque.quantidade_minima
    ).count()

    # Leads ativos
    leads_ativos = Lead.query.filter(Lead.status.in_(['novo', 'contatado', 'qualificado'])).count()

    # Oportunidades abertas
    oportunidades_abertas = Oportunidade.query.filter_by(status='aberta').count()
    valor_pipeline = db.session.query(func.sum(Oportunidade.valor_ponderado)).filter_by(status='aberta').scalar() or 0

    context = {
        'total_vendas': total_vendas,
        'total_pedidos': total_pedidos,
        'total_produtos': total_produtos,
        'total_clientes': total_clientes,
        'ticket_medio': ticket_medio,
        'pedidos_pendentes': pedidos_pendentes,
        'pedidos_enviados': pedidos_enviados,
        'produtos_estoque_baixo': produtos_estoque_baixo,
        'leads_ativos': leads_ativos,
        'oportunidades_abertas': oportunidades_abertas,
        'valor_pipeline': valor_pipeline
    }

    return render_template('dashboard/index.html', **context)


@dashboard_bp.route('/api/vendas-mes')
@login_required
@admin_required
def api_vendas_mes():
    """API: Vendas por mês (últimos 12 meses)"""
    hoje = datetime.now()
    doze_meses_atras = hoje - timedelta(days=365)

    # Query vendas por mês
    vendas = db.session.query(
        extract('year', Pedido.data_criacao).label('ano'),
        extract('month', Pedido.data_criacao).label('mes'),
        func.sum(Pedido.total).label('total'),
        func.count(Pedido.id).label('quantidade')
    ).filter(
        Pedido.data_criacao >= doze_meses_atras
    ).group_by('ano', 'mes').order_by('ano', 'mes').all()

    # Formatar dados para Chart.js
    labels = []
    valores = []
    quantidades = []

    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

    for venda in vendas:
        mes_nome = meses[int(venda.mes) - 1]
        ano = int(venda.ano)
        labels.append(f"{mes_nome}/{ano}")
        valores.append(float(venda.total))
        quantidades.append(int(venda.quantidade))

    return jsonify({
        'labels': labels,
        'valores': valores,
        'quantidades': quantidades
    })


@dashboard_bp.route('/api/produtos-mais-vendidos')
@login_required
@admin_required
def api_produtos_mais_vendidos():
    """API: Top 10 produtos mais vendidos"""
    produtos = db.session.query(
        Produto.nome,
        func.sum(ItemPedido.quantidade).label('total_vendido'),
        func.sum(ItemPedido.quantidade * ItemPedido.preco_unitario).label('valor_total')
    ).join(ItemPedido).group_by(Produto.id, Produto.nome).order_by(
        func.sum(ItemPedido.quantidade).desc()
    ).limit(10).all()

    labels = [p.nome for p in produtos]
    quantidades = [int(p.total_vendido) for p in produtos]
    valores = [float(p.valor_total) for p in produtos]

    return jsonify({
        'labels': labels,
        'quantidades': quantidades,
        'valores': valores
    })


@dashboard_bp.route('/api/pedidos-status')
@login_required
@admin_required
def api_pedidos_status():
    """API: Distribuição de pedidos por status"""
    pedidos = db.session.query(
        Pedido.status,
        func.count(Pedido.id).label('quantidade')
    ).group_by(Pedido.status).all()

    # Mapeamento de status para português
    status_map = {
        'pendente': 'Pendente',
        'confirmado': 'Confirmado',
        'em_separacao': 'Em Separação',
        'em_producao': 'Em Produção',
        'enviado': 'Enviado',
        'entregue': 'Entregue',
        'cancelado': 'Cancelado'
    }

    labels = [status_map.get(p.status, p.status) for p in pedidos]
    valores = [int(p.quantidade) for p in pedidos]

    return jsonify({
        'labels': labels,
        'valores': valores
    })


@dashboard_bp.route('/api/estoque-critico')
@login_required
@admin_required
def api_estoque_critico():
    """API: Produtos com estoque crítico"""
    produtos = db.session.query(
        Produto.nome,
        Estoque.quantidade,
        Estoque.quantidade_minima
    ).join(Estoque).filter(
        Estoque.quantidade <= Estoque.quantidade_minima
    ).order_by(Estoque.quantidade).limit(10).all()

    labels = [p.nome[:30] for p in produtos]  # Truncar nomes longos
    quantidades = [int(p.quantidade) for p in produtos]
    minimas = [int(p.quantidade_minima) for p in produtos]

    return jsonify({
        'labels': labels,
        'quantidades': quantidades,
        'minimas': minimas
    })


@dashboard_bp.route('/api/vendas-por-categoria')
@login_required
@admin_required
def api_vendas_por_categoria():
    """API: Vendas por categoria de produto"""
    vendas = db.session.query(
        Categoria.nome,
        func.count(ItemPedido.id).label('quantidade'),
        func.sum(ItemPedido.quantidade * ItemPedido.preco_unitario).label('valor_total')
    ).join(Produto, Produto.categoria_id == Categoria.id).join(
        ItemPedido, ItemPedido.produto_id == Produto.id
    ).group_by(Categoria.id, Categoria.nome).order_by(
        func.sum(ItemPedido.quantidade * ItemPedido.preco_unitario).desc()
    ).all()

    labels = [v.nome for v in vendas]
    quantidades = [int(v.quantidade) for v in vendas]
    valores = [float(v.valor_total) for v in vendas]

    return jsonify({
        'labels': labels,
        'quantidades': quantidades,
        'valores': valores
    })


@dashboard_bp.route('/api/pipeline-crm')
@login_required
@admin_required
def api_pipeline_crm():
    """API: Pipeline de vendas CRM"""
    pipeline = db.session.query(
        Oportunidade.estagio,
        func.count(Oportunidade.id).label('quantidade'),
        func.sum(Oportunidade.valor_ponderado).label('valor_total')
    ).filter_by(status='aberta').group_by(Oportunidade.estagio).all()

    # Mapeamento de estágios
    estagios_map = {
        'prospeccao': 'Prospecção',
        'qualificacao': 'Qualificação',
        'proposta': 'Proposta',
        'negociacao': 'Negociação',
        'fechamento': 'Fechamento'
    }

    labels = [estagios_map.get(p.estagio, p.estagio) for p in pipeline]
    quantidades = [int(p.quantidade) for p in pipeline]
    valores = [float(p.valor_total) for p in pipeline]

    return jsonify({
        'labels': labels,
        'quantidades': quantidades,
        'valores': valores
    })


@dashboard_bp.route('/api/financeiro-resumo')
@login_required
@admin_required
def api_financeiro_resumo():
    """API: Resumo financeiro (contas a pagar/receber)"""
    hoje = datetime.now().date()

    # Contas a receber
    a_receber_total = db.session.query(func.sum(ContaReceber.valor_original)).filter(
        ContaReceber.status != 'recebido'
    ).scalar() or 0

    a_receber_vencidas = db.session.query(func.sum(ContaReceber.valor_original)).filter(
        ContaReceber.status != 'recebido',
        ContaReceber.data_vencimento < hoje
    ).scalar() or 0

    # Contas a pagar
    a_pagar_total = db.session.query(func.sum(ContaPagar.valor_original)).filter(
        ContaPagar.status != 'pago'
    ).scalar() or 0

    a_pagar_vencidas = db.session.query(func.sum(ContaPagar.valor_original)).filter(
        ContaPagar.status != 'pago',
        ContaPagar.data_vencimento < hoje
    ).scalar() or 0

    return jsonify({
        'a_receber_total': float(a_receber_total),
        'a_receber_vencidas': float(a_receber_vencidas),
        'a_pagar_total': float(a_pagar_total),
        'a_pagar_vencidas': float(a_pagar_vencidas),
        'saldo': float(a_receber_total - a_pagar_total)
    })
