# -*- coding: utf-8 -*-
"""
Módulo Fiscal PDV - Sistema de Ponto de Venda Completo
Integração SEFAZ - NF-e (Modelo 55) e NFC-e (Modelo 65)
Padrão Governamental - Zero Tolerância a Erros
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, send_file
from flask_login import login_required, current_user
from app import db
from app.decorators import admin_required
from app.models import (
    Produto, Categoria, Cliente, Pedido, ItemPedido,
    ConfiguracaoEmpresa, CertificadoDigital, Contabilista,
    NotaFiscal, ItemNotaFiscal, CartaCorrecao, EnvioEmailNFe,
    ContaBancaria, TransacaoBancaria, ConfiguracaoImposto, InutilizacaoNFe,
    Orcamento, ItemOrcamento
)
from app.services.nfe_service import NFeService
from app.services.certificado_service import CertificadoService
from datetime import datetime, date, timedelta
from decimal import Decimal
import json
import io
import base64
import re
import logging

fiscal_bp = Blueprint('fiscal', __name__)
logger = logging.getLogger(__name__)


# ===================================================================
# VALIDADORES - Padrão SEFAZ/Receita Federal
# ===================================================================

def validar_cnpj(cnpj):
    """Valida CNPJ conforme algoritmo oficial da Receita Federal"""
    cnpj = re.sub(r'[^\d]', '', cnpj)
    if len(cnpj) != 14:
        return False
    if cnpj == cnpj[0] * 14:
        return False

    def calc_digito(cnpj, pesos):
        soma = sum(int(cnpj[i]) * pesos[i] for i in range(len(pesos)))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    d1 = calc_digito(cnpj[:12], pesos1)
    d2 = calc_digito(cnpj[:12] + d1, pesos2)

    return cnpj[-2:] == d1 + d2


def validar_cpf(cpf):
    """Valida CPF conforme algoritmo oficial da Receita Federal"""
    cpf = re.sub(r'[^\d]', '', cpf)
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False

    def calc_digito(cpf, pesos):
        soma = sum(int(cpf[i]) * pesos[i] for i in range(len(pesos)))
        resto = soma % 11
        return '0' if resto < 2 else str(11 - resto)

    pesos1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]

    d1 = calc_digito(cpf[:9], pesos1)
    d2 = calc_digito(cpf[:9] + d1, pesos2)

    return cpf[-2:] == d1 + d2


def validar_inscricao_estadual(ie, uf):
    """Valida Inscrição Estadual por UF - Simplificado"""
    ie = re.sub(r'[^\d]', '', ie)

    # Regras básicas por tamanho (cada UF tem suas regras específicas)
    tamanhos = {
        'AC': 13, 'AL': 9, 'AM': 9, 'AP': 9, 'BA': 9, 'CE': 9, 'DF': 13,
        'ES': 9, 'GO': 9, 'MA': 9, 'MG': 13, 'MS': 9, 'MT': 11, 'PA': 9,
        'PB': 9, 'PE': 9, 'PI': 9, 'PR': 10, 'RJ': 8, 'RN': 10, 'RO': 14,
        'RR': 9, 'RS': 10, 'SC': 9, 'SE': 9, 'SP': 12, 'TO': 11
    }

    if uf in tamanhos:
        return len(ie) == tamanhos[uf]
    return len(ie) >= 8


def validar_ncm(ncm):
    """Valida código NCM (8 dígitos)"""
    ncm = re.sub(r'[^\d]', '', ncm)
    return len(ncm) == 8


def validar_cfop(cfop):
    """Valida código CFOP (4 dígitos)"""
    cfop = re.sub(r'[^\d]', '', cfop)
    if len(cfop) != 4:
        return False
    primeiro = int(cfop[0])
    return primeiro in [1, 2, 3, 5, 6, 7]  # Entrada ou Saída


# ===================================================================
# CÓDIGOS IBGE - Tabelas Oficiais
# ===================================================================

CODIGO_UF_IBGE = {
    'AC': '12', 'AL': '27', 'AM': '13', 'AP': '16', 'BA': '29',
    'CE': '23', 'DF': '53', 'ES': '32', 'GO': '52', 'MA': '21',
    'MG': '31', 'MS': '50', 'MT': '51', 'PA': '15', 'PB': '25',
    'PE': '26', 'PI': '22', 'PR': '41', 'RJ': '33', 'RN': '24',
    'RO': '11', 'RR': '14', 'RS': '43', 'SC': '42', 'SE': '28',
    'SP': '35', 'TO': '17'
}

# Regimes Tributários
REGIMES_TRIBUTARIOS = {
    1: 'Simples Nacional',
    2: 'Simples Nacional - Excesso de sublimite de receita bruta',
    3: 'Regime Normal (Lucro Presumido ou Real)'
}

# Formas de Pagamento NFe
FORMAS_PAGAMENTO = {
    '01': 'Dinheiro',
    '02': 'Cheque',
    '03': 'Cartão de Crédito',
    '04': 'Cartão de Débito',
    '05': 'Crédito Loja',
    '10': 'Vale Alimentação',
    '11': 'Vale Refeição',
    '12': 'Vale Presente',
    '13': 'Vale Combustível',
    '14': 'Duplicata Mercantil',
    '15': 'Boleto Bancário',
    '16': 'Depósito Bancário',
    '17': 'PIX',
    '18': 'Transferência Bancária',
    '19': 'Programa de Fidelidade',
    '90': 'Sem Pagamento',
    '99': 'Outros'
}

# CST ICMS para Regime Normal
CST_ICMS = {
    '00': 'Tributada integralmente',
    '10': 'Tributada com cobrança de ICMS por ST',
    '20': 'Com redução de base de cálculo',
    '30': 'Isenta ou não tributada com cobrança de ICMS por ST',
    '40': 'Isenta',
    '41': 'Não tributada',
    '50': 'Suspensão',
    '51': 'Diferimento',
    '60': 'ICMS cobrado anteriormente por ST',
    '70': 'Com redução de BC e cobrança de ICMS por ST',
    '90': 'Outras'
}

# CSOSN para Simples Nacional
CSOSN_ICMS = {
    '101': 'Tributada com permissão de crédito',
    '102': 'Tributada sem permissão de crédito',
    '103': 'Isenção do ICMS para faixa de receita bruta',
    '201': 'Tributada com permissão de crédito e com cobrança de ICMS por ST',
    '202': 'Tributada sem permissão de crédito e com cobrança de ICMS por ST',
    '203': 'Isenção do ICMS para faixa de receita bruta e com cobrança de ICMS por ST',
    '300': 'Imune',
    '400': 'Não tributada',
    '500': 'ICMS cobrado anteriormente por ST ou por antecipação',
    '900': 'Outros'
}

# CST PIS/COFINS
CST_PIS_COFINS = {
    '01': 'Operação Tributável - Base de Cálculo = Valor da Operação Alíquota Normal',
    '02': 'Operação Tributável - Base de Cálculo = Valor da Operação Alíquota Diferenciada',
    '03': 'Operação Tributável - Base de Cálculo = Quantidade Vendida x Alíquota por Unidade de Produto',
    '04': 'Operação Tributável - Monofásica - Revenda a Alíquota Zero',
    '05': 'Operação Tributável - ST',
    '06': 'Operação Tributável - Alíquota Zero',
    '07': 'Operação Isenta da Contribuição',
    '08': 'Operação sem Incidência da Contribuição',
    '09': 'Operação com Suspensão da Contribuição',
    '49': 'Outras Operações de Saída',
    '99': 'Outras Operações'
}


# ===================================================================
# DASHBOARD FISCAL
# ===================================================================

@fiscal_bp.route('/')
@login_required
@admin_required
def index():
    """Dashboard principal do módulo fiscal"""
    # Verificar se empresa está configurada
    empresa = ConfiguracaoEmpresa.query.first()
    certificado = CertificadoDigital.query.filter_by(ativo=True, padrao=True).first()

    # Estatísticas do mês
    inicio_mes = date.today().replace(day=1)
    fim_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Notas do mês
    notas_mes = NotaFiscal.query.filter(
        NotaFiscal.data_emissao >= inicio_mes,
        NotaFiscal.data_emissao <= fim_mes
    ).all()

    total_notas = len(notas_mes)
    notas_autorizadas = len([n for n in notas_mes if n.status == 'autorizada'])
    notas_canceladas = len([n for n in notas_mes if n.cancelada])
    valor_total_mes = sum(float(n.valor_total or 0) for n in notas_mes if n.status == 'autorizada')

    # Últimas 10 notas
    ultimas_notas = NotaFiscal.query.order_by(NotaFiscal.data_emissao.desc()).limit(10).all()

    # Status SEFAZ
    status_sefaz = None
    if empresa and certificado:
        try:
            cert_service = CertificadoService(certificado)
            if certificado.tipo == 'A1' and certificado.arquivo_pfx:
                cert_service.carregar_certificado_a1(certificado.arquivo_pfx, certificado.senha_pfx)
            nfe_service = NFeService(empresa, cert_service)
            status_sefaz = nfe_service.consultar_status_servico()
        except Exception as e:
            logger.error(f"Erro ao consultar status SEFAZ: {e}")
            status_sefaz = {'online': False, 'mensagem': str(e)}

    # Alertas
    alertas = []

    if not empresa:
        alertas.append({
            'tipo': 'danger',
            'titulo': 'Empresa não configurada',
            'mensagem': 'Configure os dados da empresa emissora antes de emitir notas fiscais.'
        })

    if not certificado:
        alertas.append({
            'tipo': 'danger',
            'titulo': 'Certificado digital não configurado',
            'mensagem': 'Importe um certificado digital ICP-Brasil válido.'
        })
    elif certificado.esta_vencido:
        alertas.append({
            'tipo': 'danger',
            'titulo': 'Certificado digital vencido',
            'mensagem': f'O certificado venceu em {certificado.data_validade.strftime("%d/%m/%Y")}.'
        })
    elif certificado.esta_proximo_vencer:
        alertas.append({
            'tipo': 'warning',
            'titulo': 'Certificado próximo do vencimento',
            'mensagem': f'O certificado vence em {certificado.dias_para_vencer} dias.'
        })

    if empresa and empresa.ambiente_nfe == 2:
        alertas.append({
            'tipo': 'info',
            'titulo': 'Ambiente de Homologação',
            'mensagem': 'O sistema está em modo de testes. As notas não têm validade fiscal.'
        })

    return render_template('fiscal/dashboard.html',
        empresa=empresa,
        certificado=certificado,
        total_notas=total_notas,
        notas_autorizadas=notas_autorizadas,
        notas_canceladas=notas_canceladas,
        valor_total_mes=valor_total_mes,
        ultimas_notas=ultimas_notas,
        status_sefaz=status_sefaz,
        alertas=alertas,
        regimes=REGIMES_TRIBUTARIOS
    )


# ===================================================================
# CONFIGURAÇÃO DA EMPRESA EMISSORA
# ===================================================================

@fiscal_bp.route('/empresa')
@login_required
@admin_required
def empresa():
    """Visualiza/edita configuração da empresa"""
    empresa = ConfiguracaoEmpresa.query.first()
    return render_template('fiscal/empresa/form.html',
        empresa=empresa,
        regimes=REGIMES_TRIBUTARIOS,
        ufs=sorted(CODIGO_UF_IBGE.keys())
    )


@fiscal_bp.route('/empresa/salvar', methods=['POST'])
@login_required
@admin_required
def empresa_salvar():
    """Salva configuração da empresa"""
    empresa = ConfiguracaoEmpresa.query.first()

    if not empresa:
        empresa = ConfiguracaoEmpresa()
        db.session.add(empresa)

    # Validar CNPJ
    cnpj = request.form.get('cnpj', '').strip()
    if not validar_cnpj(cnpj):
        flash('CNPJ inválido. Verifique o número informado.', 'danger')
        return redirect(url_for('fiscal.empresa'))

    # Validar IE
    ie = request.form.get('inscricao_estadual', '').strip()
    uf = request.form.get('uf', '').strip()
    if ie and not validar_inscricao_estadual(ie, uf):
        flash('Inscrição Estadual inválida para a UF selecionada.', 'danger')
        return redirect(url_for('fiscal.empresa'))

    # Dados básicos
    empresa.razao_social = request.form.get('razao_social', '').strip()
    empresa.nome_fantasia = request.form.get('nome_fantasia', '').strip()
    empresa.cnpj = cnpj
    empresa.inscricao_estadual = ie
    empresa.inscricao_municipal = request.form.get('inscricao_municipal', '').strip()
    empresa.inscricao_suframa = request.form.get('inscricao_suframa', '').strip()
    empresa.regime_tributario = int(request.form.get('regime_tributario', 1))

    # CNAE
    empresa.cnae_principal = request.form.get('cnae_principal', '').strip()
    cnae_secundarios = request.form.get('cnae_secundarios', '').strip()
    if cnae_secundarios:
        empresa.set_cnae_secundarios([c.strip() for c in cnae_secundarios.split(',')])

    # Endereço
    empresa.logradouro = request.form.get('logradouro', '').strip()
    empresa.numero = request.form.get('numero', '').strip()
    empresa.complemento = request.form.get('complemento', '').strip()
    empresa.bairro = request.form.get('bairro', '').strip()
    empresa.cidade = request.form.get('cidade', '').strip()
    empresa.codigo_municipio = request.form.get('codigo_municipio', '').strip()
    empresa.uf = uf
    empresa.codigo_uf = CODIGO_UF_IBGE.get(uf, '')
    empresa.cep = request.form.get('cep', '').strip()

    # Contato
    empresa.telefone = request.form.get('telefone', '').strip()
    empresa.celular = request.form.get('celular', '').strip()
    empresa.email = request.form.get('email', '').strip()
    empresa.email_nfe = request.form.get('email_nfe', '').strip()
    empresa.website = request.form.get('website', '').strip()

    # Configurações NFe
    empresa.ambiente_nfe = int(request.form.get('ambiente_nfe', 2))
    empresa.serie_nfe = int(request.form.get('serie_nfe', 1))
    empresa.serie_nfce = int(request.form.get('serie_nfce', 1))
    empresa.csc_id = request.form.get('csc_id', '').strip()
    empresa.csc_token = request.form.get('csc_token', '').strip()

    # DANFE
    empresa.orientacao_danfe = request.form.get('orientacao_danfe', 'P')
    empresa.logo_danfe = request.form.get('logo_danfe') == 'on'

    # Textos padrão
    empresa.info_adicional_padrao = request.form.get('info_adicional_padrao', '').strip()
    empresa.info_fisco_padrao = request.form.get('info_fisco_padrao', '').strip()

    # Email NFe
    empresa.email_host_nfe = request.form.get('email_host_nfe', '').strip()
    empresa.email_porta_nfe = int(request.form.get('email_porta_nfe', 587) or 587)
    empresa.email_usuario_nfe = request.form.get('email_usuario_nfe', '').strip()
    senha_email = request.form.get('email_senha_nfe', '').strip()
    if senha_email:
        empresa.email_senha_nfe = senha_email
    empresa.email_tls_nfe = request.form.get('email_tls_nfe') == 'on'
    empresa.email_assunto_nfe = request.form.get('email_assunto_nfe', '').strip()
    empresa.email_corpo_nfe = request.form.get('email_corpo_nfe', '').strip()

    # Responsável Técnico
    empresa.resp_tecnico_cnpj = request.form.get('resp_tecnico_cnpj', '').strip()
    empresa.resp_tecnico_contato = request.form.get('resp_tecnico_contato', '').strip()
    empresa.resp_tecnico_email = request.form.get('resp_tecnico_email', '').strip()
    empresa.resp_tecnico_telefone = request.form.get('resp_tecnico_telefone', '').strip()
    empresa.resp_tecnico_id_csrt = request.form.get('resp_tecnico_id_csrt', '').strip()
    empresa.resp_tecnico_csrt = request.form.get('resp_tecnico_csrt', '').strip()

    empresa.usuario_atualizacao_id = current_user.id

    try:
        db.session.commit()
        flash('Configurações da empresa salvas com sucesso!', 'success')
        logger.info(f"Empresa {empresa.razao_social} configurada por {current_user.email}")
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao salvar: {str(e)}', 'danger')
        logger.error(f"Erro ao salvar empresa: {e}")

    return redirect(url_for('fiscal.empresa'))


# ===================================================================
# CERTIFICADO DIGITAL ICP-BRASIL
# ===================================================================

@fiscal_bp.route('/certificados')
@login_required
@admin_required
def certificados():
    """Lista certificados digitais"""
    empresa = ConfiguracaoEmpresa.query.first()
    certificados = []
    if empresa:
        certificados = CertificadoDigital.query.filter_by(empresa_id=empresa.id).all()

    return render_template('fiscal/certificados/lista.html',
        certificados=certificados,
        empresa=empresa
    )


@fiscal_bp.route('/certificados/novo')
@login_required
@admin_required
def certificado_novo():
    """Formulário para novo certificado"""
    empresa = ConfiguracaoEmpresa.query.first()
    if not empresa:
        flash('Configure os dados da empresa antes de importar certificados.', 'warning')
        return redirect(url_for('fiscal.empresa'))

    return render_template('fiscal/certificados/form.html', empresa=empresa)


@fiscal_bp.route('/certificados/upload', methods=['POST'])
@login_required
@admin_required
def certificado_upload():
    """Upload e importação de certificado A1"""
    empresa = ConfiguracaoEmpresa.query.first()
    if not empresa:
        flash('Configure os dados da empresa primeiro.', 'danger')
        return redirect(url_for('fiscal.empresa'))

    tipo = request.form.get('tipo', 'A1')
    senha = request.form.get('senha', '')
    arquivo = request.files.get('arquivo')

    if tipo == 'A1':
        if not arquivo:
            flash('Selecione o arquivo .pfx do certificado.', 'danger')
            return redirect(url_for('fiscal.certificado_novo'))

        if not arquivo.filename.lower().endswith('.pfx'):
            flash('O arquivo deve ter extensão .pfx', 'danger')
            return redirect(url_for('fiscal.certificado_novo'))

        pfx_data = arquivo.read()

        # Validar certificado
        cert_service = CertificadoService()
        result = cert_service.carregar_certificado_a1(pfx_data, senha)

        if not result['sucesso']:
            flash(f'Erro ao carregar certificado: {result.get("erro", "Senha inválida ou arquivo corrompido")}', 'danger')
            return redirect(url_for('fiscal.certificado_novo'))

        # Verificar se CNPJ do certificado corresponde à empresa
        cnpj_cert = result.get('cnpj', '').replace('.', '').replace('/', '').replace('-', '')
        cnpj_empresa = empresa.cnpj.replace('.', '').replace('/', '').replace('-', '')

        if cnpj_cert and cnpj_cert != cnpj_empresa:
            flash(f'CNPJ do certificado ({result.get("cnpj")}) não corresponde ao CNPJ da empresa ({empresa.cnpj}).', 'warning')

        # Salvar certificado
        certificado = CertificadoDigital(
            empresa_id=empresa.id,
            tipo='A1',
            nome=result.get('nome', 'Certificado A1'),
            cnpj_certificado=result.get('cnpj'),
            serial_number=result.get('serial_number'),
            thumbprint=result.get('thumbprint'),
            arquivo_pfx=pfx_data,
            senha_pfx=senha,  # Em produção, criptografar
            data_emissao=result.get('data_emissao'),
            data_validade=result.get('data_validade'),
            ativo=True,
            padrao=True,
            usuario_cadastro_id=current_user.id
        )

        # Desativar outros certificados padrão
        CertificadoDigital.query.filter_by(empresa_id=empresa.id, padrao=True).update({'padrao': False})

        db.session.add(certificado)
        db.session.commit()

        flash(f'Certificado importado com sucesso! Válido até {result.get("data_validade").strftime("%d/%m/%Y")}', 'success')
        logger.info(f"Certificado A1 importado por {current_user.email}")

    else:  # A3
        slot = int(request.form.get('slot', 0))
        pin = request.form.get('pin', '')
        biblioteca = request.form.get('biblioteca', '')

        cert_service = CertificadoService()
        result = cert_service.carregar_certificado_a3(slot, pin, biblioteca)

        if not result['sucesso']:
            flash(f'Erro ao carregar certificado A3: {result.get("erro")}', 'danger')
            return redirect(url_for('fiscal.certificado_novo'))

        certificado = CertificadoDigital(
            empresa_id=empresa.id,
            tipo='A3',
            nome=result.get('nome', 'Certificado A3'),
            cnpj_certificado=result.get('cnpj'),
            serial_number=result.get('serial_number'),
            thumbprint=result.get('thumbprint'),
            slot_token=slot,
            biblioteca_token=biblioteca,
            pin_token=pin,  # Em produção, criptografar
            data_emissao=result.get('data_emissao'),
            data_validade=result.get('data_validade'),
            ativo=True,
            padrao=True,
            usuario_cadastro_id=current_user.id
        )

        CertificadoDigital.query.filter_by(empresa_id=empresa.id, padrao=True).update({'padrao': False})

        db.session.add(certificado)
        db.session.commit()

        flash('Certificado A3 configurado com sucesso!', 'success')

    return redirect(url_for('fiscal.certificados'))


@fiscal_bp.route('/certificados/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def certificado_excluir(id):
    """Exclui um certificado"""
    certificado = CertificadoDigital.query.get_or_404(id)

    db.session.delete(certificado)
    db.session.commit()

    flash('Certificado excluído com sucesso.', 'success')
    return redirect(url_for('fiscal.certificados'))


@fiscal_bp.route('/certificados/<int:id>/definir-padrao', methods=['POST'])
@login_required
@admin_required
def certificado_definir_padrao(id):
    """Define certificado como padrão"""
    certificado = CertificadoDigital.query.get_or_404(id)

    CertificadoDigital.query.filter_by(empresa_id=certificado.empresa_id).update({'padrao': False})
    certificado.padrao = True

    db.session.commit()

    flash('Certificado definido como padrão.', 'success')
    return redirect(url_for('fiscal.certificados'))


# ===================================================================
# CONTABILISTA/CONTADOR
# ===================================================================

@fiscal_bp.route('/contabilistas')
@login_required
@admin_required
def contabilistas():
    """Lista contabilistas cadastrados"""
    empresa = ConfiguracaoEmpresa.query.first()
    contabilistas_list = []
    if empresa:
        contabilistas_list = Contabilista.query.filter_by(empresa_id=empresa.id).all()

    return render_template('fiscal/contabilistas/lista.html',
        contabilistas=contabilistas_list,
        empresa=empresa
    )


@fiscal_bp.route('/contabilistas/novo')
@login_required
@admin_required
def contabilista_novo():
    """Formulário novo contabilista"""
    empresa = ConfiguracaoEmpresa.query.first()
    if not empresa:
        flash('Configure os dados da empresa primeiro.', 'warning')
        return redirect(url_for('fiscal.empresa'))

    return render_template('fiscal/contabilistas/form.html',
        contabilista=None,
        empresa=empresa,
        ufs=sorted(CODIGO_UF_IBGE.keys())
    )


@fiscal_bp.route('/contabilistas/<int:id>/editar')
@login_required
@admin_required
def contabilista_editar(id):
    """Edita contabilista"""
    contabilista = Contabilista.query.get_or_404(id)
    empresa = ConfiguracaoEmpresa.query.first()

    return render_template('fiscal/contabilistas/form.html',
        contabilista=contabilista,
        empresa=empresa,
        ufs=sorted(CODIGO_UF_IBGE.keys())
    )


@fiscal_bp.route('/contabilistas/salvar', methods=['POST'])
@login_required
@admin_required
def contabilista_salvar():
    """Salva contabilista"""
    empresa = ConfiguracaoEmpresa.query.first()
    if not empresa:
        flash('Configure os dados da empresa primeiro.', 'danger')
        return redirect(url_for('fiscal.empresa'))

    contabilista_id = request.form.get('id')

    if contabilista_id:
        contabilista = Contabilista.query.get_or_404(int(contabilista_id))
    else:
        contabilista = Contabilista(empresa_id=empresa.id)
        db.session.add(contabilista)

    # Validar CPF/CNPJ
    cpf = request.form.get('cpf', '').strip()
    cnpj = request.form.get('cnpj', '').strip()

    if cpf and not validar_cpf(cpf):
        flash('CPF do contador inválido.', 'danger')
        return redirect(url_for('fiscal.contabilista_novo'))

    if cnpj and not validar_cnpj(cnpj):
        flash('CNPJ do escritório inválido.', 'danger')
        return redirect(url_for('fiscal.contabilista_novo'))

    contabilista.nome = request.form.get('nome', '').strip()
    contabilista.cpf = cpf
    contabilista.cnpj = cnpj
    contabilista.crc = request.form.get('crc', '').strip()
    contabilista.uf_crc = request.form.get('uf_crc', '').strip()
    contabilista.email = request.form.get('email', '').strip()
    contabilista.email_secundario = request.form.get('email_secundario', '').strip()
    contabilista.telefone = request.form.get('telefone', '').strip()
    contabilista.celular = request.form.get('celular', '').strip()

    contabilista.logradouro = request.form.get('logradouro', '').strip()
    contabilista.numero = request.form.get('numero', '').strip()
    contabilista.complemento = request.form.get('complemento', '').strip()
    contabilista.bairro = request.form.get('bairro', '').strip()
    contabilista.cidade = request.form.get('cidade', '').strip()
    contabilista.uf = request.form.get('uf', '').strip()
    contabilista.cep = request.form.get('cep', '').strip()

    contabilista.escritorio_nome = request.form.get('escritorio_nome', '').strip()
    contabilista.escritorio_cnpj = request.form.get('escritorio_cnpj', '').strip()

    contabilista.receber_nfe_xml = request.form.get('receber_nfe_xml') == 'on'
    contabilista.receber_nfe_pdf = request.form.get('receber_nfe_pdf') == 'on'
    contabilista.receber_nfe_cancelamento = request.form.get('receber_nfe_cancelamento') == 'on'
    contabilista.receber_nfe_carta_correcao = request.form.get('receber_nfe_carta_correcao') == 'on'
    contabilista.receber_relatorios = request.form.get('receber_relatorios') == 'on'
    contabilista.frequencia_relatorios = request.form.get('frequencia_relatorios', 'mensal')

    contabilista.ativo = request.form.get('ativo') == 'on'
    contabilista.principal = request.form.get('principal') == 'on'

    if contabilista.principal:
        Contabilista.query.filter(
            Contabilista.empresa_id == empresa.id,
            Contabilista.id != contabilista.id
        ).update({'principal': False})

    try:
        db.session.commit()
        flash('Contabilista salvo com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao salvar: {str(e)}', 'danger')

    return redirect(url_for('fiscal.contabilistas'))


@fiscal_bp.route('/contabilistas/<int:id>/excluir', methods=['POST'])
@login_required
@admin_required
def contabilista_excluir(id):
    """Exclui contabilista"""
    contabilista = Contabilista.query.get_or_404(id)

    db.session.delete(contabilista)
    db.session.commit()

    flash('Contabilista excluído com sucesso.', 'success')
    return redirect(url_for('fiscal.contabilistas'))


# ===================================================================
# PDV - PONTO DE VENDA
# ===================================================================

@fiscal_bp.route('/pdv')
@login_required
@admin_required
def pdv():
    """Interface do PDV"""
    empresa = ConfiguracaoEmpresa.query.first()
    certificado = CertificadoDigital.query.filter_by(ativo=True, padrao=True).first()

    if not empresa:
        flash('Configure os dados da empresa antes de usar o PDV.', 'warning')
        return redirect(url_for('fiscal.empresa'))

    if not certificado:
        flash('Configure um certificado digital antes de usar o PDV.', 'warning')
        return redirect(url_for('fiscal.certificados'))

    if certificado.esta_vencido:
        flash('O certificado digital está vencido. Importe um novo certificado.', 'danger')
        return redirect(url_for('fiscal.certificados'))

    # Produtos para o PDV
    produtos = Produto.query.filter_by(ativo=True).all()
    categorias = Categoria.query.all()

    return render_template('fiscal/pdv/terminal.html',
        empresa=empresa,
        certificado=certificado,
        produtos=produtos,
        categorias=categorias,
        formas_pagamento=FORMAS_PAGAMENTO
    )


@fiscal_bp.route('/pdv/buscar-produto')
@login_required
@admin_required
def pdv_buscar_produto():
    """Busca produto por código ou nome"""
    termo = request.args.get('q', '').strip()

    if not termo:
        return jsonify([])

    produtos = Produto.query.filter(
        db.or_(
            Produto.sku.ilike(f'%{termo}%'),
            Produto.nome.ilike(f'%{termo}%'),
            Produto.codigo_barras.ilike(f'%{termo}%')
        ),
        Produto.ativo == True
    ).limit(20).all()

    return jsonify([{
        'id': p.id,
        'codigo': p.sku,
        'nome': p.nome,
        'preco': float(p.preco or 0),
        'ncm': p.ncm or '',
        'cfop': p.cfop or '5102',
        'unidade': p.unidade or 'UN',
        'estoque': float(p.estoque_atual or 0) if hasattr(p, 'estoque_atual') else 0
    } for p in produtos])


@fiscal_bp.route('/pdv/buscar-cliente')
@login_required
@admin_required
def pdv_buscar_cliente():
    """Busca cliente por CPF/CNPJ ou nome"""
    termo = request.args.get('q', '').strip()

    if not termo:
        return jsonify([])

    clientes = Cliente.query.filter(
        db.or_(
            Cliente.nome.ilike(f'%{termo}%'),
            Cliente.cpf_cnpj.ilike(f'%{termo}%'),
            Cliente.email.ilike(f'%{termo}%')
        )
    ).limit(20).all()

    return jsonify([{
        'id': c.id,
        'nome': c.nome,
        'cpf_cnpj': c.cpf_cnpj or '',
        'email': c.email or '',
        'telefone': c.telefone or '',
        'endereco': f"{c.logradouro or ''}, {c.numero or ''}" if hasattr(c, 'logradouro') else ''
    } for c in clientes])


@fiscal_bp.route('/pdv/emitir-nfe', methods=['POST'])
@login_required
@admin_required
def pdv_emitir_nfe():
    """Emite NFe/NFCe a partir do PDV"""
    try:
        dados = request.get_json()

        empresa = ConfiguracaoEmpresa.query.first()
        certificado = CertificadoDigital.query.filter_by(ativo=True, padrao=True).first()

        if not empresa or not certificado:
            return jsonify({'sucesso': False, 'erro': 'Empresa ou certificado não configurados'})

        if certificado.esta_vencido:
            return jsonify({'sucesso': False, 'erro': 'Certificado digital vencido'})

        # Determinar modelo (55=NFe, 65=NFCe)
        modelo = dados.get('modelo', '65')  # Padrão NFCe para PDV

        # Criar nota fiscal
        numero = empresa.proximo_numero_nfce() if modelo == '65' else empresa.proximo_numero_nfe()
        serie = empresa.serie_nfce if modelo == '65' else empresa.serie_nfe

        nota = NotaFiscal(
            modelo=modelo,
            serie=serie,
            numero=numero,
            natureza_operacao=dados.get('natureza_operacao', 'Venda de Mercadoria'),
            tipo_operacao=1,  # Saída
            finalidade=1,  # Normal

            # Emitente
            emitente_cnpj=empresa.cnpj,
            emitente_razao_social=empresa.razao_social,
            emitente_ie=empresa.inscricao_estadual,
            emitente_endereco=json.dumps({
                'logradouro': empresa.logradouro,
                'numero': empresa.numero,
                'bairro': empresa.bairro,
                'cidade': empresa.cidade,
                'uf': empresa.uf,
                'cep': empresa.cep,
                'codigo_municipio': empresa.codigo_municipio
            }),

            # Destinatário
            destinatario_tipo='F' if len(re.sub(r'[^\d]', '', dados.get('cliente_cpf_cnpj', ''))) == 11 else 'J',
            destinatario_cpf_cnpj=dados.get('cliente_cpf_cnpj', ''),
            destinatario_razao_social=dados.get('cliente_nome', 'CONSUMIDOR NAO IDENTIFICADO'),
            destinatario_email=dados.get('cliente_email', ''),

            # Indicadores
            indicador_ie_destinatario=9,  # Não contribuinte
            indicador_consumidor_final=1,  # Consumidor final
            indicador_presenca=1,  # Presencial

            # Datas
            data_emissao=datetime.now(),
            data_saida_entrada=datetime.now(),

            # Transporte
            modalidade_frete=9,  # Sem frete

            # Pagamento
            forma_pagamento=dados.get('forma_pagamento', '01'),
            tipo_pagamento=0,  # À vista

            # Ambiente e status
            ambiente=empresa.ambiente_nfe,
            status='rascunho',

            usuario_emissao_id=current_user.id
        )

        db.session.add(nota)
        db.session.flush()

        # Adicionar itens
        itens = dados.get('itens', [])
        valor_produtos = Decimal('0')
        numero_item = 1

        for item_data in itens:
            produto_id = item_data.get('produto_id')
            produto = Produto.query.get(produto_id) if produto_id else None

            quantidade = Decimal(str(item_data.get('quantidade', 1)))
            valor_unitario = Decimal(str(item_data.get('valor_unitario', 0)))
            desconto = Decimal(str(item_data.get('desconto', 0)))
            valor_total = quantidade * valor_unitario - desconto

            item = ItemNotaFiscal(
                nota_fiscal_id=nota.id,
                produto_id=produto_id,
                numero_item=numero_item,

                codigo=produto.sku if produto else item_data.get('codigo', ''),
                descricao=produto.nome if produto else item_data.get('descricao', ''),
                ncm=produto.ncm if produto else item_data.get('ncm', '00000000'),
                cfop=item_data.get('cfop', '5102'),
                unidade=produto.unidade if produto else 'UN',

                quantidade=quantidade,
                valor_unitario=valor_unitario,
                valor_total=valor_total,
                valor_desconto=desconto,

                # Calcular impostos
                origem='0',  # Nacional
            )

            # Calcular impostos baseado no regime
            item.calcular_impostos(
                regime_tributario=empresa.regime_tributario,
                uf_origem=empresa.uf,
                uf_destino=empresa.uf
            )

            db.session.add(item)
            valor_produtos += valor_total
            numero_item += 1

        # Atualizar totais da nota
        nota.valor_produtos = valor_produtos
        nota.valor_desconto = Decimal(str(dados.get('desconto_total', 0)))
        nota.valor_total = valor_produtos - nota.valor_desconto
        nota.valor_pagamento = nota.valor_total

        # Recalcular totais de impostos
        nota.calcular_totais()

        db.session.commit()

        # Carregar certificado
        cert_service = CertificadoService(certificado)
        if certificado.tipo == 'A1':
            cert_service.carregar_certificado_a1(certificado.arquivo_pfx, certificado.senha_pfx)
        else:
            cert_service.carregar_certificado_a3(
                certificado.slot_token,
                certificado.pin_token,
                certificado.biblioteca_token
            )

        # Gerar XML
        nfe_service = NFeService(empresa, cert_service)
        xml = nfe_service.gerar_xml_nfe(nota)

        # Assinar
        xml_assinado = nfe_service.assinar_nfe(xml)
        nota.xml_nfe = xml_assinado
        nota.status = 'assinada'
        db.session.commit()

        # Transmitir para SEFAZ
        resultado = nfe_service.transmitir_nfe(xml_assinado)

        if resultado['sucesso']:
            nota.status = 'autorizada'
            nota.protocolo_autorizacao = resultado.get('protocolo')
            nota.data_autorizacao = datetime.now()
            nota.codigo_status_sefaz = resultado.get('codigo')
            nota.motivo_status_sefaz = resultado.get('mensagem')
            nota.xml_autorizacao = resultado.get('xml_retorno')
            db.session.commit()

            logger.info(f"NFe {nota.chave_acesso} autorizada - Protocolo: {nota.protocolo_autorizacao}")

            return jsonify({
                'sucesso': True,
                'nota_id': nota.id,
                'chave_acesso': nota.chave_acesso,
                'protocolo': nota.protocolo_autorizacao,
                'mensagem': 'Nota fiscal autorizada com sucesso!'
            })
        else:
            nota.status = 'rejeitada'
            nota.codigo_status_sefaz = resultado.get('codigo')
            nota.motivo_status_sefaz = resultado.get('mensagem')
            db.session.commit()

            logger.warning(f"NFe rejeitada: {resultado.get('mensagem')}")

            return jsonify({
                'sucesso': False,
                'erro': resultado.get('mensagem', 'Erro na transmissão'),
                'codigo': resultado.get('codigo')
            })

    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao emitir NFe: {str(e)}")
        return jsonify({'sucesso': False, 'erro': str(e)})


# ===================================================================
# NOTAS FISCAIS - LISTAGEM E GESTÃO
# ===================================================================

@fiscal_bp.route('/notas')
@login_required
@admin_required
def notas():
    """Lista notas fiscais"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    modelo = request.args.get('modelo', '')
    data_inicio = request.args.get('data_inicio', '')
    data_fim = request.args.get('data_fim', '')

    query = NotaFiscal.query

    if status:
        query = query.filter(NotaFiscal.status == status)
    if modelo:
        query = query.filter(NotaFiscal.modelo == modelo)
    if data_inicio:
        query = query.filter(NotaFiscal.data_emissao >= datetime.strptime(data_inicio, '%Y-%m-%d'))
    if data_fim:
        query = query.filter(NotaFiscal.data_emissao <= datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1))

    notas_paginadas = query.order_by(NotaFiscal.data_emissao.desc()).paginate(page=page, per_page=20)

    return render_template('fiscal/notas/lista.html',
        notas=notas_paginadas,
        status_atual=status,
        modelo_atual=modelo
    )


@fiscal_bp.route('/notas/<int:id>')
@login_required
@admin_required
def nota_detalhe(id):
    """Detalhes de uma nota fiscal"""
    nota = NotaFiscal.query.get_or_404(id)
    itens = ItemNotaFiscal.query.filter_by(nota_fiscal_id=nota.id).all()
    cartas = CartaCorrecao.query.filter_by(nota_fiscal_id=nota.id).all()

    return render_template('fiscal/notas/detalhe.html',
        nota=nota,
        itens=itens,
        cartas_correcao=cartas
    )


@fiscal_bp.route('/notas/<int:id>/xml')
@login_required
@admin_required
def nota_xml(id):
    """Download do XML da NFe"""
    nota = NotaFiscal.query.get_or_404(id)

    if not nota.xml_nfe:
        flash('XML não disponível para esta nota.', 'warning')
        return redirect(url_for('fiscal.nota_detalhe', id=id))

    return send_file(
        io.BytesIO(nota.xml_nfe.encode('utf-8')),
        mimetype='application/xml',
        as_attachment=True,
        download_name=f'NFe_{nota.chave_acesso}.xml'
    )


@fiscal_bp.route('/notas/<int:id>/danfe')
@login_required
@admin_required
def nota_danfe(id):
    """Gera DANFE em PDF"""
    nota = NotaFiscal.query.get_or_404(id)
    empresa = ConfiguracaoEmpresa.query.first()

    try:
        from app.services.pdf_service import gerar_danfe
        pdf_buffer = gerar_danfe(nota, empresa)

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=False,
            download_name=f'DANFE_{nota.chave_acesso}.pdf'
        )
    except Exception as e:
        flash(f'Erro ao gerar DANFE: {str(e)}', 'danger')
        return redirect(url_for('fiscal.nota_detalhe', id=id))


@fiscal_bp.route('/notas/<int:id>/cancelar', methods=['POST'])
@login_required
@admin_required
def nota_cancelar(id):
    """Cancela uma NFe autorizada"""
    nota = NotaFiscal.query.get_or_404(id)

    if nota.status != 'autorizada':
        flash('Apenas notas autorizadas podem ser canceladas.', 'warning')
        return redirect(url_for('fiscal.nota_detalhe', id=id))

    if nota.cancelada:
        flash('Esta nota já foi cancelada.', 'warning')
        return redirect(url_for('fiscal.nota_detalhe', id=id))

    # Verificar prazo (geralmente 24h)
    horas_desde_emissao = (datetime.now() - nota.data_autorizacao).total_seconds() / 3600
    if horas_desde_emissao > 24:
        flash('O prazo para cancelamento (24 horas) expirou.', 'danger')
        return redirect(url_for('fiscal.nota_detalhe', id=id))

    justificativa = request.form.get('justificativa', '').strip()
    if len(justificativa) < 15:
        flash('A justificativa deve ter pelo menos 15 caracteres.', 'danger')
        return redirect(url_for('fiscal.nota_detalhe', id=id))

    try:
        empresa = ConfiguracaoEmpresa.query.first()
        certificado = CertificadoDigital.query.filter_by(ativo=True, padrao=True).first()

        cert_service = CertificadoService(certificado)
        if certificado.tipo == 'A1':
            cert_service.carregar_certificado_a1(certificado.arquivo_pfx, certificado.senha_pfx)

        nfe_service = NFeService(empresa, cert_service)
        resultado = nfe_service.cancelar_nfe(
            nota.chave_acesso,
            nota.protocolo_autorizacao,
            justificativa
        )

        if resultado['sucesso']:
            nota.cancelada = True
            nota.data_cancelamento = datetime.now()
            nota.protocolo_cancelamento = resultado.get('protocolo')
            nota.justificativa_cancelamento = justificativa
            nota.status = 'cancelada'
            nota.xml_cancelamento = resultado.get('xml_retorno')
            db.session.commit()

            flash('Nota fiscal cancelada com sucesso!', 'success')
            logger.info(f"NFe {nota.chave_acesso} cancelada por {current_user.email}")
        else:
            flash(f'Erro ao cancelar: {resultado.get("mensagem")}', 'danger')

    except Exception as e:
        flash(f'Erro ao cancelar: {str(e)}', 'danger')
        logger.error(f"Erro ao cancelar NFe: {e}")

    return redirect(url_for('fiscal.nota_detalhe', id=id))


@fiscal_bp.route('/notas/<int:id>/carta-correcao', methods=['POST'])
@login_required
@admin_required
def nota_carta_correcao(id):
    """Envia Carta de Correção"""
    nota = NotaFiscal.query.get_or_404(id)

    if nota.status != 'autorizada':
        flash('Apenas notas autorizadas podem receber carta de correção.', 'warning')
        return redirect(url_for('fiscal.nota_detalhe', id=id))

    if nota.cancelada:
        flash('Notas canceladas não podem receber carta de correção.', 'warning')
        return redirect(url_for('fiscal.nota_detalhe', id=id))

    correcao = request.form.get('correcao', '').strip()
    if len(correcao) < 15 or len(correcao) > 1000:
        flash('A correção deve ter entre 15 e 1000 caracteres.', 'danger')
        return redirect(url_for('fiscal.nota_detalhe', id=id))

    try:
        empresa = ConfiguracaoEmpresa.query.first()
        certificado = CertificadoDigital.query.filter_by(ativo=True, padrao=True).first()

        # Próxima sequência de CC-e
        ultima_cce = CartaCorrecao.query.filter_by(nota_fiscal_id=nota.id).order_by(CartaCorrecao.sequencia.desc()).first()
        sequencia = (ultima_cce.sequencia + 1) if ultima_cce else 1

        if sequencia > 20:
            flash('Limite de 20 cartas de correção atingido.', 'danger')
            return redirect(url_for('fiscal.nota_detalhe', id=id))

        cert_service = CertificadoService(certificado)
        if certificado.tipo == 'A1':
            cert_service.carregar_certificado_a1(certificado.arquivo_pfx, certificado.senha_pfx)

        nfe_service = NFeService(empresa, cert_service)
        resultado = nfe_service.carta_correcao(nota.chave_acesso, sequencia, correcao)

        carta = CartaCorrecao(
            nota_fiscal_id=nota.id,
            sequencia=sequencia,
            correcao=correcao,
            data_evento=datetime.now(),
            usuario_id=current_user.id
        )

        if resultado['sucesso']:
            carta.status = 'autorizada'
            carta.protocolo = resultado.get('protocolo')
            carta.codigo_status = resultado.get('codigo')
            carta.motivo_status = resultado.get('mensagem')
            carta.xml_evento = resultado.get('xml_retorno')
            nota.tem_carta_correcao = True

            flash('Carta de correção enviada com sucesso!', 'success')
            logger.info(f"CC-e {sequencia} enviada para NFe {nota.chave_acesso}")
        else:
            carta.status = 'rejeitada'
            carta.codigo_status = resultado.get('codigo')
            carta.motivo_status = resultado.get('mensagem')

            flash(f'Erro ao enviar CC-e: {resultado.get("mensagem")}', 'danger')

        db.session.add(carta)
        db.session.commit()

    except Exception as e:
        flash(f'Erro ao enviar CC-e: {str(e)}', 'danger')
        logger.error(f"Erro ao enviar CC-e: {e}")

    return redirect(url_for('fiscal.nota_detalhe', id=id))


# ===================================================================
# INUTILIZAÇÃO DE NUMERAÇÃO
# ===================================================================

@fiscal_bp.route('/inutilizacao')
@login_required
@admin_required
def inutilizacao():
    """Lista inutilizações"""
    page = request.args.get('pagina', 1, type=int)
    per_page = 20

    query = InutilizacaoNFe.query.order_by(InutilizacaoNFe.data_criacao.desc())
    total = query.count()
    total_paginas = (total + per_page - 1) // per_page

    inutilizacoes = query.offset((page - 1) * per_page).limit(per_page).all()
    empresa = ConfiguracaoEmpresa.query.first()

    return render_template('fiscal/inutilizacao/lista.html',
        inutilizacoes=inutilizacoes,
        empresa=empresa,
        ano_atual=datetime.now().year,
        pagina=page,
        total_paginas=total_paginas
    )


@fiscal_bp.route('/inutilizacao/salvar', methods=['POST'])
@login_required
@admin_required
def inutilizacao_salvar():
    """Salva nova inutilização"""
    empresa = ConfiguracaoEmpresa.query.first()

    if True:  # POST method
        try:
            ano = int(request.form.get('ano', datetime.now().year % 100))
            modelo = request.form.get('modelo', '55')
            serie = int(request.form.get('serie', 1))
            numero_inicial = int(request.form.get('numero_inicial', 0))
            numero_final = int(request.form.get('numero_final', 0))
            justificativa = request.form.get('justificativa', '').strip()

            if len(justificativa) < 15:
                flash('A justificativa deve ter pelo menos 15 caracteres.', 'danger')
                return redirect(url_for('fiscal.inutilizacao'))

            if numero_inicial > numero_final:
                flash('Número inicial não pode ser maior que o final.', 'danger')
                return redirect(url_for('fiscal.inutilizacao'))

            certificado = CertificadoDigital.query.filter_by(ativo=True, padrao=True).first()

            cert_service = CertificadoService(certificado)
            if certificado.tipo == 'A1':
                cert_service.carregar_certificado_a1(certificado.arquivo_pfx, certificado.senha_pfx)

            nfe_service = NFeService(empresa, cert_service)
            resultado = nfe_service.inutilizar_numeracao(ano, serie, numero_inicial, numero_final, justificativa)

            inut = InutilizacaoNFe(
                ano=ano,
                modelo=modelo,
                serie=serie,
                numero_inicial=numero_inicial,
                numero_final=numero_final,
                justificativa=justificativa,
                usuario_id=current_user.id
            )

            if resultado['sucesso']:
                inut.status = 'homologado'
                inut.protocolo = resultado.get('protocolo')
                inut.codigo_status = resultado.get('codigo')
                inut.motivo_status = resultado.get('mensagem')
                inut.data_inutilizacao = datetime.now()
                inut.xml_retorno = resultado.get('xml_retorno')

                flash('Numeração inutilizada com sucesso!', 'success')
            else:
                inut.status = 'rejeitado'
                inut.codigo_status = resultado.get('codigo')
                inut.motivo_status = resultado.get('mensagem')

                flash(f'Erro na inutilização: {resultado.get("mensagem")}', 'danger')

            db.session.add(inut)
            db.session.commit()

        except Exception as e:
            flash(f'Erro: {str(e)}', 'danger')

    return redirect(url_for('fiscal.inutilizacao'))


# ===================================================================
# CONFIGURAÇÃO DE IMPOSTOS
# ===================================================================

@fiscal_bp.route('/impostos')
@login_required
@admin_required
def impostos():
    """Configurações de impostos"""
    empresa = ConfiguracaoEmpresa.query.first()

    # Criar config padrao se nao existir
    config = {}
    if empresa:
        config = {
            'regime_tributario': empresa.regime_tributario or 1,
            'icms_aliquota_interna': 17,
            'icms_reducao_bc': 0,
            'icms_mva': 0,
            'icms_interestadual_sul': 12,
            'icms_interestadual_norte': 7,
            'icms_importacao': 4,
            'ipi_aliquota': 0,
            'ipi_cst_entrada': '00',
            'ipi_cst_saida': '50',
            'pis_aliquota': 0.65,
            'pis_cst': '01',
            'cofins_aliquota': 3.0,
            'cofins_cst': '01',
            'cst_venda': '00',
            'cst_devolucao': '41',
            'cst_bonificacao': '41',
            'csosn_venda': '102',
            'csosn_devolucao': '400',
            'csosn_bonificacao': '400',
            'exibir_tributos_aproximados': True,
            'fonte_ibpt': 'ibpt',
            'versao_ibpt': None
        }

    # Carregar configuracao existente se houver
    config_db = ConfiguracaoImposto.query.filter_by(ativo=True).first()
    if config_db:
        for key in config:
            if hasattr(config_db, key):
                config[key] = getattr(config_db, key)

    # Criar objeto compativel com template
    class ConfigObj:
        pass
    config_obj = ConfigObj()
    for key, val in config.items():
        setattr(config_obj, key, val)

    return render_template('fiscal/impostos/configurar.html',
        config=config_obj,
        cst_icms=CST_ICMS,
        csosn_icms=CSOSN_ICMS,
        cst_pis_cofins=CST_PIS_COFINS
    )


@fiscal_bp.route('/impostos/salvar', methods=['POST'])
@login_required
@admin_required
def impostos_salvar():
    """Salva configuração de imposto"""
    config_id = request.form.get('id')

    if config_id:
        config = ConfiguracaoImposto.query.get_or_404(int(config_id))
    else:
        config = ConfiguracaoImposto()
        db.session.add(config)

    config.ncm = request.form.get('ncm', '').strip()
    config.cfop = request.form.get('cfop', '').strip()
    config.uf_origem = request.form.get('uf_origem', '').strip()
    config.uf_destino = request.form.get('uf_destino', '').strip()

    config.cst_icms = request.form.get('cst_icms', '').strip()
    config.aliquota_icms = Decimal(request.form.get('aliquota_icms', 0) or 0)
    config.reducao_bc_icms = Decimal(request.form.get('reducao_bc_icms', 0) or 0)

    config.mva = Decimal(request.form.get('mva', 0) or 0)
    config.aliquota_icms_st = Decimal(request.form.get('aliquota_icms_st', 0) or 0)

    config.cst_ipi = request.form.get('cst_ipi', '').strip()
    config.aliquota_ipi = Decimal(request.form.get('aliquota_ipi', 0) or 0)

    config.cst_pis = request.form.get('cst_pis', '').strip()
    config.aliquota_pis = Decimal(request.form.get('aliquota_pis', 0) or 0)

    config.cst_cofins = request.form.get('cst_cofins', '').strip()
    config.aliquota_cofins = Decimal(request.form.get('aliquota_cofins', 0) or 0)

    config.percentual_federal = Decimal(request.form.get('percentual_federal', 0) or 0)
    config.percentual_estadual = Decimal(request.form.get('percentual_estadual', 0) or 0)
    config.percentual_municipal = Decimal(request.form.get('percentual_municipal', 0) or 0)

    config.ativo = True

    try:
        db.session.commit()
        flash('Configuração de imposto salva com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao salvar: {str(e)}', 'danger')

    return redirect(url_for('fiscal.impostos'))


# ===================================================================
# STATUS SEFAZ
# ===================================================================

@fiscal_bp.route('/status-sefaz')
@login_required
@admin_required
def status_sefaz():
    """Consulta status do serviço SEFAZ"""
    empresa = ConfiguracaoEmpresa.query.first()
    certificado = CertificadoDigital.query.filter_by(ativo=True, padrao=True).first()

    if not empresa or not certificado:
        return jsonify({'online': False, 'mensagem': 'Empresa ou certificado não configurados'})

    try:
        cert_service = CertificadoService(certificado)
        if certificado.tipo == 'A1':
            cert_service.carregar_certificado_a1(certificado.arquivo_pfx, certificado.senha_pfx)

        nfe_service = NFeService(empresa, cert_service)
        resultado = nfe_service.consultar_status_servico()

        return jsonify(resultado)

    except Exception as e:
        return jsonify({'online': False, 'mensagem': str(e)})


# ===================================================================
# RELATÓRIOS FISCAIS
# ===================================================================

@fiscal_bp.route('/relatorios')
@login_required
@admin_required
def relatorios():
    """Página de relatórios fiscais"""
    # Buscar relatorios gerados (se houver tabela)
    relatorios = []
    return render_template('fiscal/relatorios/lista.html', relatorios=relatorios)


@fiscal_bp.route('/relatorios/gerar', methods=['POST'])
@login_required
@admin_required
def relatorio_gerar():
    """Gera novo relatório"""
    tipo = request.form.get('tipo', '')
    data_inicio = request.form.get('data_inicio', '')
    data_fim = request.form.get('data_fim', '')
    modelo = request.form.get('modelo', '')
    formato = request.form.get('formato', 'pdf')

    # Redirecionar para relatorio especifico baseado no tipo
    if tipo == 'vendas_diarias' or tipo == 'vendas_mensal':
        return redirect(url_for('fiscal.relatorio_notas_periodo',
            data_inicio=data_inicio, data_fim=data_fim))
    elif tipo == 'nfe_emitidas':
        return redirect(url_for('fiscal.notas',
            data_inicio=data_inicio, data_fim=data_fim, modelo='55'))
    elif tipo == 'nfce_emitidas':
        return redirect(url_for('fiscal.notas',
            data_inicio=data_inicio, data_fim=data_fim, modelo='65'))

    flash('Tipo de relatorio nao implementado ainda.', 'info')
    return redirect(url_for('fiscal.relatorios'))


@fiscal_bp.route('/relatorios/notas-periodo')
@login_required
@admin_required
def relatorio_notas_periodo():
    """Relatório de notas por período"""
    data_inicio = request.args.get('data_inicio', date.today().replace(day=1).isoformat())
    data_fim = request.args.get('data_fim', date.today().isoformat())

    notas = NotaFiscal.query.filter(
        NotaFiscal.data_emissao >= datetime.strptime(data_inicio, '%Y-%m-%d'),
        NotaFiscal.data_emissao <= datetime.strptime(data_fim, '%Y-%m-%d') + timedelta(days=1)
    ).order_by(NotaFiscal.data_emissao.asc()).all()

    total_notas = len(notas)
    total_autorizadas = len([n for n in notas if n.status == 'autorizada' and not n.cancelada])
    total_canceladas = len([n for n in notas if n.cancelada])
    valor_total = sum(float(n.valor_total or 0) for n in notas if n.status == 'autorizada' and not n.cancelada)
    total_icms = sum(float(n.valor_icms or 0) for n in notas if n.status == 'autorizada' and not n.cancelada)

    return render_template('fiscal/relatorios/notas_periodo.html',
        notas=notas,
        data_inicio=data_inicio,
        data_fim=data_fim,
        total_notas=total_notas,
        total_autorizadas=total_autorizadas,
        total_canceladas=total_canceladas,
        valor_total=valor_total,
        total_icms=total_icms
    )
