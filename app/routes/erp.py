"""
Rotas ERP (Enterprise Resource Planning)
Gestão de compras, fornecedores, financeiro
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required, current_user
from app.models.erp import Fornecedor, Compra, ItemCompra, ContaPagar, ContaReceber
from app.models.produto import Produto
from app import db
from app.decorators import admin_required
from app.utils import paginate_query
from sqlalchemy import or_, func
from datetime import datetime, timedelta
import uuid

erp_bp = Blueprint('erp', __name__)


# ==================== DASHBOARD ERP ====================

@erp_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Dashboard ERP com métricas financeiras"""
    hoje = datetime.now().date()
    inicio_mes = hoje.replace(day=1)

    # Fornecedores ativos
    total_fornecedores = Fornecedor.query.filter_by(ativo=True).count()

    # Compras pendentes
    compras_pendentes = Compra.query.filter(
        Compra.status.in_(['pendente', 'aprovado', 'em_transito'])
    ).count()

    # Contas a pagar - vencidas e a vencer
    contas_pagar_vencidas = ContaPagar.query.filter(
        ContaPagar.status != 'pago',
        ContaPagar.data_vencimento < hoje
    ).count()

    contas_pagar_mes = db.session.query(
        func.sum(ContaPagar.valor_original - ContaPagar.valor_pago)
    ).filter(
        ContaPagar.status != 'pago',
        ContaPagar.data_vencimento >= inicio_mes,
        ContaPagar.data_vencimento <= hoje.replace(day=28)
    ).scalar() or 0

    # Contas a receber - vencidas e a vencer
    contas_receber_vencidas = ContaReceber.query.filter(
        ContaReceber.status != 'recebido',
        ContaReceber.data_vencimento < hoje
    ).count()

    contas_receber_mes = db.session.query(
        func.sum(ContaReceber.valor_original - ContaReceber.valor_recebido)
    ).filter(
        ContaReceber.status != 'recebido',
        ContaReceber.data_vencimento >= inicio_mes,
        ContaReceber.data_vencimento <= hoje.replace(day=28)
    ).scalar() or 0

    # Próximos vencimentos (contas a pagar)
    proximos_vencimentos = ContaPagar.query.filter(
        ContaPagar.status != 'pago',
        ContaPagar.data_vencimento >= hoje,
        ContaPagar.data_vencimento <= hoje + timedelta(days=7)
    ).order_by(ContaPagar.data_vencimento.asc()).limit(10).all()

    return render_template(
        'erp/dashboard.html',
        total_fornecedores=total_fornecedores,
        compras_pendentes=compras_pendentes,
        contas_pagar_vencidas=contas_pagar_vencidas,
        contas_pagar_mes=contas_pagar_mes,
        contas_receber_vencidas=contas_receber_vencidas,
        contas_receber_mes=contas_receber_mes,
        proximos_vencimentos=proximos_vencimentos
    )


# ==================== FORNECEDORES ====================

@erp_bp.route('/fornecedores')
@login_required
@admin_required
def listar_fornecedores():
    """Listar fornecedores"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '').strip()

    query = Fornecedor.query.filter_by(ativo=True)

    if search:
        query = query.filter(
            or_(
                Fornecedor.razao_social.ilike(f'%{search}%'),
                Fornecedor.nome_fantasia.ilike(f'%{search}%'),
                Fornecedor.cnpj.ilike(f'%{search}%')
            )
        )

    query = query.order_by(Fornecedor.razao_social.asc())
    pagination = paginate_query(query, page, 20)

    return render_template(
        'erp/fornecedores/listar.html',
        fornecedores=pagination['items'],
        pagination=pagination,
        search=search
    )


@erp_bp.route('/fornecedores/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_fornecedor():
    """Criar novo fornecedor"""
    if request.method == 'POST':
        # Verificar CNPJ único
        cnpj = request.form.get('cnpj', '').strip()
        if Fornecedor.query.filter_by(cnpj=cnpj).first():
            flash('Já existe um fornecedor com este CNPJ.', 'danger')
            return redirect(url_for('erp.novo_fornecedor'))

        fornecedor = Fornecedor(
            razao_social=request.form.get('razao_social'),
            nome_fantasia=request.form.get('nome_fantasia'),
            cnpj=cnpj,
            inscricao_estadual=request.form.get('inscricao_estadual'),
            email=request.form.get('email'),
            telefone=request.form.get('telefone'),
            celular=request.form.get('celular'),
            website=request.form.get('website'),
            endereco=request.form.get('endereco'),
            numero=request.form.get('numero'),
            complemento=request.form.get('complemento'),
            bairro=request.form.get('bairro'),
            cidade=request.form.get('cidade'),
            estado=request.form.get('estado'),
            cep=request.form.get('cep'),
            contato_nome=request.form.get('contato_nome'),
            contato_email=request.form.get('contato_email'),
            contato_telefone=request.form.get('contato_telefone'),
            tipo=request.form.get('tipo'),
            prazo_pagamento_padrao=request.form.get('prazo_pagamento_padrao'),
            observacoes=request.form.get('observacoes')
        )

        db.session.add(fornecedor)
        db.session.commit()

        current_app.logger.info(f"Fornecedor criado: {fornecedor.razao_social}")
        flash('Fornecedor cadastrado com sucesso!', 'success')
        return redirect(url_for('erp.visualizar_fornecedor', fornecedor_id=fornecedor.id))

    return render_template('erp/fornecedores/novo.html')


@erp_bp.route('/fornecedores/<int:fornecedor_id>')
@login_required
@admin_required
def visualizar_fornecedor(fornecedor_id):
    """Visualizar detalhes do fornecedor"""
    fornecedor = Fornecedor.query.get_or_404(fornecedor_id)
    ultimas_compras = fornecedor.compras.order_by(Compra.data_pedido.desc()).limit(10).all()

    return render_template(
        'erp/fornecedores/visualizar.html',
        fornecedor=fornecedor,
        ultimas_compras=ultimas_compras
    )


@erp_bp.route('/fornecedores/<int:fornecedor_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_fornecedor(fornecedor_id):
    """Editar fornecedor"""
    fornecedor = Fornecedor.query.get_or_404(fornecedor_id)

    if request.method == 'POST':
        fornecedor.razao_social = request.form.get('razao_social')
        fornecedor.nome_fantasia = request.form.get('nome_fantasia')
        fornecedor.email = request.form.get('email')
        fornecedor.telefone = request.form.get('telefone')
        fornecedor.celular = request.form.get('celular')
        fornecedor.website = request.form.get('website')
        fornecedor.endereco = request.form.get('endereco')
        fornecedor.numero = request.form.get('numero')
        fornecedor.complemento = request.form.get('complemento')
        fornecedor.bairro = request.form.get('bairro')
        fornecedor.cidade = request.form.get('cidade')
        fornecedor.estado = request.form.get('estado')
        fornecedor.cep = request.form.get('cep')
        fornecedor.contato_nome = request.form.get('contato_nome')
        fornecedor.contato_email = request.form.get('contato_email')
        fornecedor.contato_telefone = request.form.get('contato_telefone')
        fornecedor.tipo = request.form.get('tipo')
        fornecedor.prazo_pagamento_padrao = request.form.get('prazo_pagamento_padrao')
        fornecedor.observacoes = request.form.get('observacoes')

        db.session.commit()
        flash('Fornecedor atualizado com sucesso!', 'success')
        return redirect(url_for('erp.visualizar_fornecedor', fornecedor_id=fornecedor.id))

    return render_template('erp/fornecedores/editar.html', fornecedor=fornecedor)


# ==================== COMPRAS ====================

@erp_bp.route('/compras')
@login_required
@admin_required
def listar_compras():
    """Listar pedidos de compra"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')

    query = Compra.query

    if status:
        query = query.filter_by(status=status)

    query = query.order_by(Compra.data_pedido.desc())
    pagination = paginate_query(query, page, 20)

    return render_template(
        'erp/compras/listar.html',
        compras=pagination['items'],
        pagination=pagination,
        status_filtro=status
    )


@erp_bp.route('/compras/nova', methods=['GET', 'POST'])
@login_required
@admin_required
def nova_compra():
    """Criar novo pedido de compra"""
    if request.method == 'POST':
        # Gerar número da compra
        numero = f"PC-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

        compra = Compra(
            numero_compra=numero,
            fornecedor_id=request.form.get('fornecedor_id', type=int),
            data_prevista_entrega=datetime.strptime(request.form.get('data_prevista_entrega'), '%Y-%m-%d').date() if request.form.get('data_prevista_entrega') else None,
            forma_pagamento=request.form.get('forma_pagamento'),
            condicao_pagamento=request.form.get('condicao_pagamento'),
            observacoes=request.form.get('observacoes'),
            comprador_id=current_user.id
        )

        db.session.add(compra)
        db.session.commit()

        flash('Pedido de compra criado! Adicione os itens.', 'success')
        return redirect(url_for('erp.editar_compra', compra_id=compra.id))

    fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome_fantasia.asc()).all()
    return render_template('erp/compras/nova.html', fornecedores=fornecedores)


@erp_bp.route('/compras/<int:compra_id>')
@login_required
@admin_required
def visualizar_compra(compra_id):
    """Visualizar pedido de compra"""
    compra = Compra.query.get_or_404(compra_id)
    return render_template('erp/compras/visualizar.html', compra=compra)


@erp_bp.route('/compras/<int:compra_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_compra(compra_id):
    """Editar pedido de compra e adicionar itens"""
    compra = Compra.query.get_or_404(compra_id)

    if compra.status not in ['pendente', 'aprovado']:
        flash('Este pedido não pode mais ser editado.', 'warning')
        return redirect(url_for('erp.visualizar_compra', compra_id=compra.id))

    if request.method == 'POST':
        # Adicionar item
        if 'adicionar_item' in request.form:
            item = ItemCompra(
                compra_id=compra.id,
                produto_id=request.form.get('produto_id', type=int),
                quantidade_pedida=request.form.get('quantidade', type=int),
                preco_unitario=request.form.get('preco_unitario', type=float)
            )
            db.session.add(item)
            compra.calcular_total()
            db.session.commit()
            flash('Item adicionado!', 'success')

        # Salvar pedido
        elif 'salvar' in request.form:
            compra.desconto = request.form.get('desconto', type=float) or 0
            compra.valor_frete = request.form.get('valor_frete', type=float) or 0
            compra.outras_despesas = request.form.get('outras_despesas', type=float) or 0
            compra.calcular_total()
            db.session.commit()
            flash('Pedido atualizado!', 'success')

        return redirect(url_for('erp.editar_compra', compra_id=compra.id))

    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome.asc()).all()
    return render_template('erp/compras/editar.html', compra=compra, produtos=produtos)


@erp_bp.route('/compras/<int:compra_id>/aprovar', methods=['POST'])
@login_required
@admin_required
def aprovar_compra(compra_id):
    """Aprovar pedido de compra"""
    compra = Compra.query.get_or_404(compra_id)

    if compra.status != 'pendente':
        flash('Este pedido não pode ser aprovado.', 'warning')
        return redirect(url_for('erp.visualizar_compra', compra_id=compra.id))

    compra.status = 'aprovado'
    db.session.commit()

    flash('Pedido aprovado com sucesso!', 'success')
    return redirect(url_for('erp.visualizar_compra', compra_id=compra.id))


# ==================== CONTAS A PAGAR ====================

@erp_bp.route('/contas-pagar')
@login_required
@admin_required
def listar_contas_pagar():
    """Listar contas a pagar"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    vencimento = request.args.get('vencimento', '')

    query = ContaPagar.query

    if status:
        query = query.filter_by(status=status)

    hoje = datetime.now().date()
    if vencimento == 'vencidas':
        query = query.filter(ContaPagar.status != 'pago', ContaPagar.data_vencimento < hoje)
    elif vencimento == 'hoje':
        query = query.filter(ContaPagar.data_vencimento == hoje)
    elif vencimento == 'semana':
        query = query.filter(
            ContaPagar.data_vencimento >= hoje,
            ContaPagar.data_vencimento <= hoje + timedelta(days=7)
        )

    query = query.order_by(ContaPagar.data_vencimento.asc())
    pagination = paginate_query(query, page, 20)

    return render_template(
        'erp/financeiro/contas_pagar.html',
        contas=pagination['items'],
        pagination=pagination,
        status_filtro=status,
        vencimento_filtro=vencimento
    )


@erp_bp.route('/contas-pagar/<int:conta_id>/pagar', methods=['POST'])
@login_required
@admin_required
def pagar_conta(conta_id):
    """Registrar pagamento de conta"""
    conta = ContaPagar.query.get_or_404(conta_id)

    valor_pago = request.form.get('valor_pago', type=float)
    forma_pagamento = request.form.get('forma_pagamento')

    if not valor_pago or valor_pago <= 0:
        flash('Valor de pagamento inválido.', 'danger')
        return redirect(url_for('erp.listar_contas_pagar'))

    conta.valor_pago += valor_pago
    conta.data_pagamento = datetime.now().date()

    if conta.valor_pago >= conta.valor_original:
        conta.status = 'pago'
    else:
        conta.status = 'pago_parcial'

    db.session.commit()
    flash('Pagamento registrado com sucesso!', 'success')
    return redirect(url_for('erp.listar_contas_pagar'))


# ==================== CONTAS A RECEBER ====================

@erp_bp.route('/contas-receber')
@login_required
@admin_required
def listar_contas_receber():
    """Listar contas a receber"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    vencimento = request.args.get('vencimento', '')

    query = ContaReceber.query

    if status:
        query = query.filter_by(status=status)

    hoje = datetime.now().date()
    if vencimento == 'vencidas':
        query = query.filter(ContaReceber.status != 'recebido', ContaReceber.data_vencimento < hoje)
    elif vencimento == 'hoje':
        query = query.filter(ContaReceber.data_vencimento == hoje)
    elif vencimento == 'semana':
        query = query.filter(
            ContaReceber.data_vencimento >= hoje,
            ContaReceber.data_vencimento <= hoje + timedelta(days=7)
        )

    query = query.order_by(ContaReceber.data_vencimento.asc())
    pagination = paginate_query(query, page, 20)

    return render_template(
        'erp/financeiro/contas_receber.html',
        contas=pagination['items'],
        pagination=pagination,
        status_filtro=status,
        vencimento_filtro=vencimento
    )


@erp_bp.route('/contas-receber/<int:conta_id>/receber', methods=['POST'])
@login_required
@admin_required
def receber_conta(conta_id):
    """Registrar recebimento de conta"""
    conta = ContaReceber.query.get_or_404(conta_id)

    valor_recebido = request.form.get('valor_recebido', type=float)
    forma_pagamento = request.form.get('forma_pagamento')

    if not valor_recebido or valor_recebido <= 0:
        flash('Valor de recebimento inválido.', 'danger')
        return redirect(url_for('erp.listar_contas_receber'))

    conta.valor_recebido += valor_recebido
    conta.data_recebimento = datetime.now().date()

    if conta.valor_recebido >= conta.valor_original:
        conta.status = 'recebido'
    else:
        conta.status = 'recebido_parcial'

    db.session.commit()
    flash('Recebimento registrado com sucesso!', 'success')
    return redirect(url_for('erp.listar_contas_receber'))


# ==================== APIS ====================

@erp_bp.route('/api/resumo-financeiro')
@login_required
@admin_required
def api_resumo_financeiro():
    """API: Resumo financeiro do mês"""
    hoje = datetime.now().date()
    inicio_mes = hoje.replace(day=1)

    # Total a pagar no mês
    a_pagar = db.session.query(
        func.sum(ContaPagar.valor_original - ContaPagar.valor_pago)
    ).filter(
        ContaPagar.status != 'pago',
        ContaPagar.data_vencimento >= inicio_mes
    ).scalar() or 0

    # Total a receber no mês
    a_receber = db.session.query(
        func.sum(ContaReceber.valor_original - ContaReceber.valor_recebido)
    ).filter(
        ContaReceber.status != 'recebido',
        ContaReceber.data_vencimento >= inicio_mes
    ).scalar() or 0

    return jsonify({
        'a_pagar': float(a_pagar),
        'a_receber': float(a_receber),
        'saldo': float(a_receber - a_pagar)
    })
