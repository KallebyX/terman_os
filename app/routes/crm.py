"""
Rotas CRM (Customer Relationship Management)
Gestão de clientes, leads, oportunidades e pipeline de vendas
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required, current_user
from app.models.crm import Cliente, Lead, Oportunidade, Interacao, Atividade, Proposta
from app.models.user import User
from app import db
from app.decorators import admin_required
from app.utils import paginate_query
from sqlalchemy import or_, func
from datetime import datetime, timedelta

crm_bp = Blueprint('crm', __name__)


# ==================== DASHBOARD CRM ====================

@crm_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Dashboard CRM com métricas principais"""
    # Contadores
    total_clientes = Cliente.query.filter_by(ativo=True).count()
    total_leads = Lead.query.filter(Lead.status.notin_(['ganho', 'perdido', 'descartado'])).count()
    total_oportunidades = Oportunidade.query.filter_by(status='aberta').count()

    # Valor total do pipeline
    pipeline_valor = db.session.query(
        func.sum(Oportunidade.valor_ponderado)
    ).filter_by(status='aberta').scalar() or 0

    # Leads por status
    leads_por_status = db.session.query(
        Lead.status, func.count(Lead.id)
    ).group_by(Lead.status).all()

    # Oportunidades por estágio
    oportunidades_por_estagio = db.session.query(
        Oportunidade.estagio, func.count(Oportunidade.id), func.sum(Oportunidade.valor_estimado)
    ).filter_by(status='aberta').group_by(Oportunidade.estagio).all()

    # Atividades pendentes do usuário
    atividades_pendentes = Atividade.query.filter(
        Atividade.usuario_responsavel_id == current_user.id,
        Atividade.concluida == False,
        Atividade.cancelada == False
    ).order_by(Atividade.data_vencimento.asc()).limit(10).all()

    # Últimos leads
    ultimos_leads = Lead.query.order_by(Lead.data_criacao.desc()).limit(5).all()

    return render_template(
        'crm/dashboard.html',
        total_clientes=total_clientes,
        total_leads=total_leads,
        total_oportunidades=total_oportunidades,
        pipeline_valor=pipeline_valor,
        leads_por_status=leads_por_status,
        oportunidades_por_estagio=oportunidades_por_estagio,
        atividades_pendentes=atividades_pendentes,
        ultimos_leads=ultimos_leads
    )


# ==================== LEADS ====================

@crm_bp.route('/leads')
@login_required
@admin_required
def listar_leads():
    """Listar todos os leads"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    search = request.args.get('q', '').strip()

    query = Lead.query

    # Filtrar por status
    if status:
        query = query.filter_by(status=status)

    # Busca por nome/email
    if search:
        query = query.filter(
            or_(
                Lead.nome.ilike(f'%{search}%'),
                Lead.email.ilike(f'%{search}%'),
                Lead.empresa.ilike(f'%{search}%')
            )
        )

    query = query.order_by(Lead.data_criacao.desc())
    pagination = paginate_query(query, page, 20)

    return render_template(
        'crm/leads/listar.html',
        leads=pagination['items'],
        pagination=pagination,
        status_filtro=status,
        search=search
    )


@crm_bp.route('/leads/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def novo_lead():
    """Criar novo lead"""
    if request.method == 'POST':
        lead = Lead(
            nome=request.form.get('nome'),
            email=request.form.get('email'),
            telefone=request.form.get('telefone'),
            celular=request.form.get('celular'),
            empresa=request.form.get('empresa'),
            cargo=request.form.get('cargo'),
            origem=request.form.get('origem'),
            interesse=request.form.get('interesse'),
            observacoes=request.form.get('observacoes'),
            vendedor_id=request.form.get('vendedor_id', type=int) or current_user.id
        )

        db.session.add(lead)
        db.session.commit()

        current_app.logger.info(f"Lead criado: {lead.nome} por {current_user.id}")
        flash('Lead criado com sucesso!', 'success')
        return redirect(url_for('crm.visualizar_lead', lead_id=lead.id))

    vendedores = User.query.filter_by(tipo_usuario='admin').all()
    return render_template('crm/leads/novo.html', vendedores=vendedores)


@crm_bp.route('/leads/<int:lead_id>')
@login_required
@admin_required
def visualizar_lead(lead_id):
    """Visualizar detalhes de um lead"""
    lead = Lead.query.get_or_404(lead_id)
    interacoes = lead.interacoes.order_by(Interacao.data_interacao.desc()).limit(10).all()

    return render_template(
        'crm/leads/visualizar.html',
        lead=lead,
        interacoes=interacoes
    )


@crm_bp.route('/leads/<int:lead_id>/editar', methods=['GET', 'POST'])
@login_required
@admin_required
def editar_lead(lead_id):
    """Editar lead"""
    lead = Lead.query.get_or_404(lead_id)

    if request.method == 'POST':
        lead.nome = request.form.get('nome')
        lead.email = request.form.get('email')
        lead.telefone = request.form.get('telefone')
        lead.celular = request.form.get('celular')
        lead.empresa = request.form.get('empresa')
        lead.cargo = request.form.get('cargo')
        lead.origem = request.form.get('origem')
        lead.status = request.form.get('status')
        lead.qualificacao = request.form.get('qualificacao')
        lead.interesse = request.form.get('interesse')
        lead.observacoes = request.form.get('observacoes')
        lead.vendedor_id = request.form.get('vendedor_id', type=int)

        db.session.commit()
        flash('Lead atualizado com sucesso!', 'success')
        return redirect(url_for('crm.visualizar_lead', lead_id=lead.id))

    vendedores = User.query.filter_by(tipo_usuario='admin').all()
    return render_template('crm/leads/editar.html', lead=lead, vendedores=vendedores)


@crm_bp.route('/leads/<int:lead_id>/interacao', methods=['POST'])
@login_required
@admin_required
def adicionar_interacao_lead(lead_id):
    """Adicionar interação a um lead"""
    lead = Lead.query.get_or_404(lead_id)

    interacao = Interacao(
        lead_id=lead_id,
        usuario_id=current_user.id,
        tipo=request.form.get('tipo'),
        direcao=request.form.get('direcao'),
        assunto=request.form.get('assunto'),
        descricao=request.form.get('descricao'),
        duracao_minutos=request.form.get('duracao_minutos', type=int)
    )

    # Atualizar datas do lead
    lead.data_ultima_interacao = datetime.utcnow()
    if not lead.data_primeira_interacao:
        lead.data_primeira_interacao = datetime.utcnow()

    db.session.add(interacao)
    db.session.commit()

    flash('Interação registrada com sucesso!', 'success')
    return redirect(url_for('crm.visualizar_lead', lead_id=lead_id))


# ==================== CLIENTES ====================

@crm_bp.route('/clientes')
@login_required
@admin_required
def listar_clientes():
    """Listar todos os clientes"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('q', '').strip()
    tipo = request.args.get('tipo', '')

    query = Cliente.query.filter_by(ativo=True)

    if tipo:
        query = query.filter_by(tipo=tipo)

    if search:
        query = query.join(User, Cliente.usuario_id == User.id).filter(
            or_(
                User.nome.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%'),
                Cliente.cpf_cnpj.ilike(f'%{search}%')
            )
        )

    query = query.order_by(Cliente.data_cadastro.desc())
    pagination = paginate_query(query, page, 20)

    return render_template(
        'crm/clientes/listar.html',
        clientes=pagination['items'],
        pagination=pagination,
        tipo_filtro=tipo,
        search=search
    )


@crm_bp.route('/clientes/<int:cliente_id>')
@login_required
@admin_required
def visualizar_cliente(cliente_id):
    """Visualizar detalhes de um cliente"""
    cliente = Cliente.query.get_or_404(cliente_id)
    interacoes = cliente.interacoes.order_by(Interacao.data_interacao.desc()).limit(10).all()

    return render_template(
        'crm/clientes/visualizar.html',
        cliente=cliente,
        interacoes=interacoes
    )


# ==================== OPORTUNIDADES ====================

@crm_bp.route('/oportunidades')
@login_required
@admin_required
def listar_oportunidades():
    """Listar oportunidades - Pipeline de Vendas"""
    status = request.args.get('status', 'aberta')

    query = Oportunidade.query

    if status:
        query = query.filter_by(status=status)

    oportunidades = query.order_by(Oportunidade.data_criacao.desc()).all()

    # Agrupar por estágio
    estagios = ['prospeccao', 'qualificacao', 'proposta', 'negociacao', 'fechamento']
    pipeline = {estagio: [] for estagio in estagios}

    for op in oportunidades:
        if op.estagio in pipeline:
            pipeline[op.estagio].append(op)

    return render_template(
        'crm/oportunidades/pipeline.html',
        pipeline=pipeline,
        estagios=estagios,
        status_filtro=status
    )


@crm_bp.route('/oportunidades/nova', methods=['GET', 'POST'])
@login_required
@admin_required
def nova_oportunidade():
    """Criar nova oportunidade"""
    if request.method == 'POST':
        oportunidade = Oportunidade(
            nome=request.form.get('nome'),
            lead_id=request.form.get('lead_id', type=int),
            cliente_id=request.form.get('cliente_id', type=int),
            vendedor_id=request.form.get('vendedor_id', type=int) or current_user.id,
            valor_estimado=request.form.get('valor_estimado', type=float),
            probabilidade=request.form.get('probabilidade', type=int) or 10,
            descricao=request.form.get('descricao'),
            proximos_passos=request.form.get('proximos_passos')
        )

        oportunidade.calcular_valor_ponderado()

        db.session.add(oportunidade)
        db.session.commit()

        flash('Oportunidade criada com sucesso!', 'success')
        return redirect(url_for('crm.listar_oportunidades'))

    leads = Lead.query.filter(Lead.status.notin_(['ganho', 'perdido'])).all()
    clientes = Cliente.query.filter_by(ativo=True).all()
    vendedores = User.query.filter_by(tipo_usuario='admin').all()

    return render_template(
        'crm/oportunidades/nova.html',
        leads=leads,
        clientes=clientes,
        vendedores=vendedores
    )


@crm_bp.route('/oportunidades/<int:op_id>/atualizar-estagio', methods=['POST'])
@login_required
@admin_required
def atualizar_estagio_oportunidade(op_id):
    """Atualizar estágio de uma oportunidade (para drag-and-drop)"""
    oportunidade = Oportunidade.query.get_or_404(op_id)
    novo_estagio = request.json.get('estagio')

    estagios_validos = ['prospeccao', 'qualificacao', 'proposta', 'negociacao', 'fechamento']
    if novo_estagio not in estagios_validos:
        return jsonify({'error': 'Estágio inválido'}), 400

    oportunidade.estagio = novo_estagio

    # Atualizar probabilidade baseada no estágio
    probabilidades = {
        'prospeccao': 10,
        'qualificacao': 25,
        'proposta': 50,
        'negociacao': 75,
        'fechamento': 90
    }
    oportunidade.probabilidade = probabilidades.get(novo_estagio, oportunidade.probabilidade)
    oportunidade.calcular_valor_ponderado()

    db.session.commit()

    return jsonify({'success': True, 'estagio': novo_estagio})


# ==================== ATIVIDADES ====================

@crm_bp.route('/atividades')
@login_required
@admin_required
def listar_atividades():
    """Listar atividades do usuário"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pendente')

    query = Atividade.query.filter_by(usuario_responsavel_id=current_user.id)

    if status == 'pendente':
        query = query.filter_by(concluida=False, cancelada=False)
    elif status == 'concluida':
        query = query.filter_by(concluida=True)

    query = query.order_by(Atividade.data_vencimento.asc())
    pagination = paginate_query(query, page, 20)

    return render_template(
        'crm/atividades/listar.html',
        atividades=pagination['items'],
        pagination=pagination,
        status_filtro=status
    )


@crm_bp.route('/atividades/<int:atividade_id>/concluir', methods=['POST'])
@login_required
@admin_required
def concluir_atividade(atividade_id):
    """Marcar atividade como concluída"""
    atividade = Atividade.query.get_or_404(atividade_id)

    if atividade.usuario_responsavel_id != current_user.id:
        flash('Você não pode concluir esta atividade.', 'danger')
        return redirect(url_for('crm.listar_atividades'))

    atividade.concluida = True
    atividade.data_conclusao = datetime.utcnow()

    db.session.commit()
    flash('Atividade concluída!', 'success')
    return redirect(url_for('crm.listar_atividades'))


# ==================== APIS ====================

@crm_bp.route('/api/leads-status')
@login_required
@admin_required
def api_leads_status():
    """API: Leads por status"""
    dados = db.session.query(
        Lead.status, func.count(Lead.id)
    ).group_by(Lead.status).all()

    return jsonify([{'status': s, 'count': c} for s, c in dados])


@crm_bp.route('/api/pipeline-valor')
@login_required
@admin_required
def api_pipeline_valor():
    """API: Valor do pipeline por estágio"""
    dados = db.session.query(
        Oportunidade.estagio,
        func.count(Oportunidade.id),
        func.sum(Oportunidade.valor_estimado),
        func.sum(Oportunidade.valor_ponderado)
    ).filter_by(status='aberta').group_by(Oportunidade.estagio).all()

    return jsonify([{
        'estagio': e,
        'quantidade': q,
        'valor_total': float(v or 0),
        'valor_ponderado': float(p or 0)
    } for e, q, v, p in dados])
