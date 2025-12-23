# -*- coding: utf-8 -*-
"""
Serviço de Geração de PDFs
DANFE, Orçamentos, Relatórios, OS
"""

import os
import io
import base64
from datetime import datetime
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether
)
from reportlab.graphics.barcode import code128
from reportlab.graphics.shapes import Drawing, Rect, String
import logging

logger = logging.getLogger(__name__)


class PDFService:
    """Serviço para geração de PDFs profissionais"""

    # Cores padrão
    COR_PRIMARIA = colors.HexColor('#0071e3')
    COR_SECUNDARIA = colors.HexColor('#1d1d1f')
    COR_CINZA = colors.HexColor('#86868b')
    COR_FUNDO = colors.HexColor('#f5f5f7')
    COR_BORDA = colors.HexColor('#d2d2d7')

    def __init__(self, empresa=None):
        """
        Inicializa o serviço de PDF

        Args:
            empresa: Objeto ConfiguracaoEmpresa para dados da empresa
        """
        self.empresa = empresa
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()

    def _configurar_estilos(self):
        """Configura estilos customizados"""
        self.styles.add(ParagraphStyle(
            name='Titulo',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=self.COR_SECUNDARIA,
            spaceAfter=10,
            alignment=TA_CENTER
        ))

        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=self.COR_PRIMARIA,
            spaceAfter=8
        ))

        self.styles.add(ParagraphStyle(
            name='TextoNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.COR_SECUNDARIA,
            leading=14
        ))

        self.styles.add(ParagraphStyle(
            name='TextoPequeno',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=self.COR_CINZA,
            leading=10
        ))

        self.styles.add(ParagraphStyle(
            name='TextoDestaque',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.COR_PRIMARIA,
            fontName='Helvetica-Bold'
        ))

    def gerar_danfe(self, nota_fiscal, salvar_arquivo=None):
        """
        Gera DANFE (Documento Auxiliar da NFe)

        Args:
            nota_fiscal: Objeto NotaFiscal
            salvar_arquivo: Path para salvar (opcional)

        Returns:
            bytes: PDF em bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=10*mm,
            leftMargin=10*mm,
            topMargin=10*mm,
            bottomMargin=10*mm
        )

        elements = []

        # Cabeçalho com logo e dados da empresa
        elements.append(self._criar_cabecalho_danfe(nota_fiscal))
        elements.append(Spacer(1, 5*mm))

        # Código de barras da chave de acesso
        elements.append(self._criar_codigo_barras_nfe(nota_fiscal.chave_acesso))
        elements.append(Spacer(1, 3*mm))

        # Chave de acesso
        elements.append(self._criar_chave_acesso(nota_fiscal))
        elements.append(Spacer(1, 5*mm))

        # Natureza da operação e protocolo
        elements.append(self._criar_natureza_protocolo(nota_fiscal))
        elements.append(Spacer(1, 5*mm))

        # Destinatário/Remetente
        elements.append(self._criar_destinatario_danfe(nota_fiscal))
        elements.append(Spacer(1, 5*mm))

        # Fatura/Duplicatas
        if nota_fiscal.duplicatas:
            elements.append(self._criar_fatura_danfe(nota_fiscal))
            elements.append(Spacer(1, 5*mm))

        # Impostos
        elements.append(self._criar_impostos_danfe(nota_fiscal))
        elements.append(Spacer(1, 5*mm))

        # Transportadora
        elements.append(self._criar_transportadora_danfe(nota_fiscal))
        elements.append(Spacer(1, 5*mm))

        # Produtos
        elements.append(self._criar_produtos_danfe(nota_fiscal))
        elements.append(Spacer(1, 5*mm))

        # Informações adicionais
        if nota_fiscal.informacoes_complementares or nota_fiscal.informacoes_fisco:
            elements.append(self._criar_info_adicionais_danfe(nota_fiscal))

        doc.build(elements)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        if salvar_arquivo:
            with open(salvar_arquivo, 'wb') as f:
                f.write(pdf_bytes)

        return pdf_bytes

    def _criar_cabecalho_danfe(self, nota_fiscal):
        """Cria cabeçalho do DANFE"""
        dados = [
            ['IDENTIFICAÇÃO DO EMITENTE', 'DANFE', 'NFe'],
            [self.empresa.razao_social if self.empresa else 'EMPRESA',
             f'Nº {nota_fiscal.numero}\nSérie {nota_fiscal.serie}',
             f'{nota_fiscal.tipo_operacao == 0 and "ENTRADA" or "SAÍDA"}'],
            [f'{self.empresa.logradouro}, {self.empresa.numero}' if self.empresa else '',
             f'Folha 1/1',
             '']
        ]

        # Logo da empresa (se disponível)
        if self.empresa and self.empresa.logo_base64:
            try:
                logo_bytes = base64.b64decode(self.empresa.logo_base64)
                logo_img = Image(io.BytesIO(logo_bytes), width=30*mm, height=15*mm)
                dados[0][0] = logo_img
            except:
                pass

        tabela = Table(dados, colWidths=[100*mm, 50*mm, 40*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_FUNDO),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('SPAN', (0, 0), (0, 2)),
        ]))

        return tabela

    def _criar_codigo_barras_nfe(self, chave_acesso):
        """Cria código de barras Code128 da chave de acesso"""
        try:
            barcode = code128.Code128(chave_acesso, barWidth=0.3*mm, barHeight=12*mm)
            return barcode
        except:
            return Paragraph(f'Chave: {chave_acesso}', self.styles['TextoPequeno'])

    def _criar_chave_acesso(self, nota_fiscal):
        """Formata e exibe chave de acesso"""
        chave = nota_fiscal.chave_acesso or ''
        chave_formatada = ' '.join([chave[i:i+4] for i in range(0, len(chave), 4)])

        dados = [
            ['CHAVE DE ACESSO'],
            [chave_formatada]
        ]

        tabela = Table(dados, colWidths=[190*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_FUNDO),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        return tabela

    def _criar_natureza_protocolo(self, nota_fiscal):
        """Natureza da operação e protocolo de autorização"""
        protocolo = nota_fiscal.protocolo_autorizacao or 'Aguardando autorização'
        data_auth = nota_fiscal.data_autorizacao.strftime('%d/%m/%Y %H:%M:%S') if nota_fiscal.data_autorizacao else ''

        dados = [
            ['NATUREZA DA OPERAÇÃO', 'PROTOCOLO DE AUTORIZAÇÃO DE USO'],
            [nota_fiscal.natureza_operacao, f'{protocolo} - {data_auth}']
        ]

        tabela = Table(dados, colWidths=[100*mm, 90*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_FUNDO),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        return tabela

    def _criar_destinatario_danfe(self, nota_fiscal):
        """Dados do destinatário"""
        dados = [
            ['DESTINATÁRIO/REMETENTE'],
            [
                f'NOME/RAZÃO SOCIAL: {nota_fiscal.destinatario_razao_social or ""}',
                f'CNPJ/CPF: {nota_fiscal.destinatario_cpf_cnpj or ""}',
                f'DATA EMISSÃO: {nota_fiscal.data_emissao.strftime("%d/%m/%Y") if nota_fiscal.data_emissao else ""}'
            ]
        ]

        tabela = Table(dados, colWidths=[100*mm, 50*mm, 40*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_FUNDO),
            ('SPAN', (0, 0), (2, 0)),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        return tabela

    def _criar_fatura_danfe(self, nota_fiscal):
        """Fatura e duplicatas"""
        duplicatas = nota_fiscal.get_duplicatas() if hasattr(nota_fiscal, 'get_duplicatas') else []

        dados = [['FATURA/DUPLICATAS']]
        if duplicatas:
            for dup in duplicatas:
                dados.append([f"Nº {dup.get('numero', '')} - Venc: {dup.get('vencimento', '')} - R$ {dup.get('valor', '0,00')}"])
        else:
            dados.append(['Pagamento à vista'])

        tabela = Table(dados, colWidths=[190*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_FUNDO),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        return tabela

    def _criar_impostos_danfe(self, nota_fiscal):
        """Resumo dos impostos"""
        dados = [
            ['BASE CÁLC. ICMS', 'VALOR ICMS', 'BASE CÁLC. ST', 'VALOR ICMS ST',
             'VALOR IPI', 'VALOR TOTAL'],
            [
                f'R$ {float(nota_fiscal.valor_bc_icms or 0):,.2f}',
                f'R$ {float(nota_fiscal.valor_icms or 0):,.2f}',
                f'R$ {float(nota_fiscal.valor_bc_icms_st or 0):,.2f}',
                f'R$ {float(nota_fiscal.valor_icms_st or 0):,.2f}',
                f'R$ {float(nota_fiscal.valor_ipi or 0):,.2f}',
                f'R$ {float(nota_fiscal.valor_total or 0):,.2f}'
            ]
        ]

        tabela = Table(dados, colWidths=[32*mm, 32*mm, 32*mm, 32*mm, 32*mm, 30*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_FUNDO),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        return tabela

    def _criar_transportadora_danfe(self, nota_fiscal):
        """Dados da transportadora"""
        frete_map = {0: 'Emitente', 1: 'Destinatário', 2: 'Terceiros', 9: 'Sem Frete'}
        frete = frete_map.get(nota_fiscal.modalidade_frete, 'Sem Frete')

        dados = [
            ['TRANSPORTADOR/VOLUMES TRANSPORTADOS'],
            [
                f'RAZÃO SOCIAL: {nota_fiscal.transportadora_razao_social or ""}',
                f'FRETE: {frete}',
                f'PLACA: {nota_fiscal.veiculo_placa or ""}'
            ],
            [
                f'QTDE VOL: {nota_fiscal.quantidade_volumes or ""}',
                f'PESO BRUTO: {float(nota_fiscal.peso_bruto or 0):.3f} kg',
                f'PESO LÍQ: {float(nota_fiscal.peso_liquido or 0):.3f} kg'
            ]
        ]

        tabela = Table(dados, colWidths=[80*mm, 55*mm, 55*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_FUNDO),
            ('SPAN', (0, 0), (2, 0)),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        return tabela

    def _criar_produtos_danfe(self, nota_fiscal):
        """Tabela de produtos"""
        dados = [
            ['CÓD', 'DESCRIÇÃO', 'NCM', 'CFOP', 'UN', 'QTD', 'V.UNIT', 'V.TOTAL']
        ]

        for item in nota_fiscal.itens:
            dados.append([
                item.codigo[:10] if item.codigo else '',
                item.descricao[:40] if item.descricao else '',
                item.ncm or '',
                item.cfop or '',
                item.unidade or 'UN',
                f'{float(item.quantidade):.2f}',
                f'{float(item.valor_unitario):,.2f}',
                f'{float(item.valor_total):,.2f}'
            ])

        tabela = Table(dados, colWidths=[20*mm, 60*mm, 20*mm, 15*mm, 12*mm, 18*mm, 22*mm, 23*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_FUNDO),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (5, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        return tabela

    def _criar_info_adicionais_danfe(self, nota_fiscal):
        """Informações adicionais"""
        info = nota_fiscal.informacoes_complementares or ''
        if nota_fiscal.informacoes_fisco:
            info = f"INFORMAÇÕES AO FISCO: {nota_fiscal.informacoes_fisco}\n\n{info}"

        dados = [
            ['INFORMAÇÕES COMPLEMENTARES'],
            [Paragraph(info[:2000], self.styles['TextoPequeno'])]
        ]

        tabela = Table(dados, colWidths=[190*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_FUNDO),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        return tabela

    def gerar_orcamento_pdf(self, orcamento, salvar_arquivo=None):
        """
        Gera PDF do orçamento comercial

        Args:
            orcamento: Objeto Orcamento
            salvar_arquivo: Path para salvar (opcional)

        Returns:
            bytes: PDF em bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15*mm,
            leftMargin=15*mm,
            topMargin=15*mm,
            bottomMargin=15*mm
        )

        elements = []

        # Logo e cabeçalho
        elements.append(self._criar_cabecalho_orcamento(orcamento))
        elements.append(Spacer(1, 10*mm))

        # Título
        elements.append(Paragraph(
            f'ORÇAMENTO Nº {orcamento.numero_orcamento}',
            self.styles['Titulo']
        ))
        elements.append(Spacer(1, 5*mm))

        # Data e validade
        elements.append(self._criar_datas_orcamento(orcamento))
        elements.append(Spacer(1, 10*mm))

        # Dados do cliente
        elements.append(Paragraph('CLIENTE', self.styles['Subtitulo']))
        elements.append(self._criar_cliente_orcamento(orcamento))
        elements.append(Spacer(1, 10*mm))

        # Itens do orçamento
        elements.append(Paragraph('PRODUTOS/SERVIÇOS', self.styles['Subtitulo']))
        elements.append(self._criar_itens_orcamento(orcamento))
        elements.append(Spacer(1, 10*mm))

        # Totais
        elements.append(self._criar_totais_orcamento(orcamento))
        elements.append(Spacer(1, 10*mm))

        # Condições comerciais
        if orcamento.forma_pagamento or orcamento.prazo_entrega:
            elements.append(Paragraph('CONDIÇÕES COMERCIAIS', self.styles['Subtitulo']))
            elements.append(self._criar_condicoes_orcamento(orcamento))
            elements.append(Spacer(1, 10*mm))

        # Observações
        if orcamento.observacoes:
            elements.append(Paragraph('OBSERVAÇÕES', self.styles['Subtitulo']))
            elements.append(Paragraph(orcamento.observacoes, self.styles['TextoNormal']))
            elements.append(Spacer(1, 10*mm))

        # Condições gerais
        if orcamento.condicoes_gerais:
            elements.append(Paragraph('CONDIÇÕES GERAIS', self.styles['Subtitulo']))
            elements.append(Paragraph(orcamento.condicoes_gerais, self.styles['TextoPequeno']))
            elements.append(Spacer(1, 10*mm))

        # Rodapé com assinatura
        elements.append(self._criar_rodape_orcamento())

        doc.build(elements)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        if salvar_arquivo:
            with open(salvar_arquivo, 'wb') as f:
                f.write(pdf_bytes)

        return pdf_bytes

    def _criar_cabecalho_orcamento(self, orcamento):
        """Cabeçalho do orçamento com logo"""
        dados_empresa = []

        if self.empresa:
            dados_empresa = [
                [self.empresa.razao_social],
                [f'{self.empresa.logradouro}, {self.empresa.numero} - {self.empresa.bairro}'],
                [f'{self.empresa.cidade}/{self.empresa.uf} - CEP: {self.empresa.cep}'],
                [f'CNPJ: {self.empresa.cnpj} - IE: {self.empresa.inscricao_estadual or ""}'],
                [f'Tel: {self.empresa.telefone or ""} - Email: {self.empresa.email or ""}']
            ]
        else:
            dados_empresa = [['EMPRESA'], [''], [''], [''], ['']]

        tabela = Table(dados_empresa, colWidths=[180*mm])
        tabela.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.COR_SECUNDARIA),
        ]))

        return tabela

    def _criar_datas_orcamento(self, orcamento):
        """Datas de emissão e validade"""
        data_emissao = orcamento.data_criacao.strftime('%d/%m/%Y') if orcamento.data_criacao else ''
        data_validade = orcamento.data_validade.strftime('%d/%m/%Y') if orcamento.data_validade else ''

        dados = [
            ['Data de Emissão:', data_emissao, 'Válido até:', data_validade]
        ]

        tabela = Table(dados, colWidths=[35*mm, 45*mm, 30*mm, 45*mm])
        tabela.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.COR_SECUNDARIA),
        ]))

        return tabela

    def _criar_cliente_orcamento(self, orcamento):
        """Dados do cliente"""
        dados = [
            [f'Nome/Razão Social: {orcamento.cliente_nome or ""}'],
            [f'CPF/CNPJ: {orcamento.cliente_cpf_cnpj or ""}'],
            [f'Email: {orcamento.cliente_email or ""} - Tel: {orcamento.cliente_telefone or ""}'],
            [f'Endereço: {orcamento.cliente_endereco or ""} - {orcamento.cliente_cidade or ""}/{orcamento.cliente_uf or ""}']
        ]

        tabela = Table(dados, colWidths=[180*mm])
        tabela.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))

        return tabela

    def _criar_itens_orcamento(self, orcamento):
        """Tabela de itens do orçamento"""
        dados = [
            ['#', 'CÓDIGO', 'DESCRIÇÃO', 'UN', 'QTD', 'V.UNIT', 'DESC', 'SUBTOTAL']
        ]

        for i, item in enumerate(orcamento.itens, 1):
            subtotal = item.subtotal if hasattr(item, 'subtotal') else (
                float(item.quantidade) * float(item.preco_unitario) - float(item.desconto_valor or 0)
            )
            dados.append([
                str(i),
                item.codigo or '',
                item.descricao[:50] if item.descricao else '',
                item.unidade or 'UN',
                f'{float(item.quantidade):,.2f}',
                f'R$ {float(item.preco_unitario):,.2f}',
                f'{float(item.desconto_percentual or 0):,.1f}%',
                f'R$ {subtotal:,.2f}'
            ])

        tabela = Table(dados, colWidths=[8*mm, 20*mm, 62*mm, 12*mm, 18*mm, 25*mm, 15*mm, 25*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_PRIMARIA),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (4, 1), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))

        return tabela

    def _criar_totais_orcamento(self, orcamento):
        """Resumo de valores do orçamento"""
        subtotal = float(orcamento.subtotal or 0)
        desconto = float(orcamento.desconto_valor or 0)
        frete = float(orcamento.valor_frete or 0)
        outras = float(orcamento.outras_despesas or 0)
        total = float(orcamento.total or 0)

        dados = [
            ['', 'Subtotal:', f'R$ {subtotal:,.2f}'],
            ['', 'Desconto:', f'R$ {desconto:,.2f}'],
            ['', 'Frete:', f'R$ {frete:,.2f}'],
            ['', 'Outras Despesas:', f'R$ {outras:,.2f}'],
            ['', 'TOTAL:', f'R$ {total:,.2f}'],
        ]

        tabela = Table(dados, colWidths=[100*mm, 40*mm, 40*mm])
        tabela.setStyle(TableStyle([
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (1, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (-1, -1), (-1, -1), 12),
            ('TEXTCOLOR', (-1, -1), (-1, -1), self.COR_PRIMARIA),
            ('LINEABOVE', (1, -1), (-1, -1), 1, self.COR_PRIMARIA),
            ('TOPPADDING', (0, -1), (-1, -1), 8),
        ]))

        return tabela

    def _criar_condicoes_orcamento(self, orcamento):
        """Condições comerciais"""
        dados = []

        if orcamento.forma_pagamento:
            dados.append([f'Forma de Pagamento: {orcamento.forma_pagamento}'])
        if orcamento.condicao_pagamento:
            dados.append([f'Condição: {orcamento.condicao_pagamento}'])
        if orcamento.prazo_entrega:
            dados.append([f'Prazo de Entrega: {orcamento.prazo_entrega}'])
        if orcamento.frete_tipo:
            dados.append([f'Frete: {orcamento.frete_tipo}'])
        if orcamento.transportadora:
            dados.append([f'Transportadora: {orcamento.transportadora}'])

        if not dados:
            dados.append(['A combinar'])

        tabela = Table(dados, colWidths=[180*mm])
        tabela.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))

        return tabela

    def _criar_rodape_orcamento(self):
        """Rodapé com espaço para assinatura"""
        dados = [
            ['', ''],
            ['_' * 50, '_' * 50],
            ['Vendedor', 'Cliente'],
            ['', ''],
            [f'Documento gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}', '']
        ]

        tabela = Table(dados, colWidths=[90*mm, 90*mm])
        tabela.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('TEXTCOLOR', (0, -1), (-1, -1), self.COR_CINZA),
            ('FONTSIZE', (0, -1), (-1, -1), 7),
        ]))

        return tabela

    def gerar_os_pdf(self, ordem_servico, salvar_arquivo=None):
        """
        Gera PDF da Ordem de Serviço

        Args:
            ordem_servico: Objeto OrdemServico
            salvar_arquivo: Path para salvar (opcional)

        Returns:
            bytes: PDF em bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=15*mm,
            leftMargin=15*mm,
            topMargin=15*mm,
            bottomMargin=15*mm
        )

        elements = []

        # Cabeçalho
        elements.append(self._criar_cabecalho_os(ordem_servico))
        elements.append(Spacer(1, 10*mm))

        # Dados da OS
        elements.append(self._criar_dados_os(ordem_servico))
        elements.append(Spacer(1, 10*mm))

        # Descrição do serviço
        elements.append(Paragraph('DESCRIÇÃO DO SERVIÇO', self.styles['Subtitulo']))
        elements.append(Paragraph(
            ordem_servico.descricao_servico or 'Não informada',
            self.styles['TextoNormal']
        ))
        elements.append(Spacer(1, 10*mm))

        # Materiais utilizados
        if ordem_servico.produtos:
            elements.append(Paragraph('MATERIAIS/PRODUTOS', self.styles['Subtitulo']))
            elements.append(self._criar_materiais_os(ordem_servico))
            elements.append(Spacer(1, 10*mm))

        # Custos
        elements.append(Paragraph('CUSTOS', self.styles['Subtitulo']))
        elements.append(self._criar_custos_os(ordem_servico))
        elements.append(Spacer(1, 10*mm))

        # Observações
        if ordem_servico.observacoes:
            elements.append(Paragraph('OBSERVAÇÕES', self.styles['Subtitulo']))
            elements.append(Paragraph(ordem_servico.observacoes, self.styles['TextoNormal']))
            elements.append(Spacer(1, 10*mm))

        # Assinaturas
        elements.append(self._criar_assinaturas_os())

        doc.build(elements)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        if salvar_arquivo:
            with open(salvar_arquivo, 'wb') as f:
                f.write(pdf_bytes)

        return pdf_bytes

    def _criar_cabecalho_os(self, ordem_servico):
        """Cabeçalho da OS"""
        dados = [
            [f'ORDEM DE SERVIÇO Nº {ordem_servico.numero_os}',
             f'Status: {ordem_servico.status.upper()}']
        ]

        tabela = Table(dados, colWidths=[120*mm, 60*mm])
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.COR_PRIMARIA),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 14),
            ('FONTSIZE', (1, 0), (1, 0), 10),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))

        return tabela

    def _criar_dados_os(self, ordem_servico):
        """Dados da OS"""
        dados = [
            ['CLIENTE:', ordem_servico.cliente_nome or ''],
            ['TIPO DE SERVIÇO:', ordem_servico.tipo_servico or ''],
            ['PRIORIDADE:', ordem_servico.prioridade.upper() if ordem_servico.prioridade else ''],
            ['DATA ABERTURA:', ordem_servico.data_criacao.strftime('%d/%m/%Y') if ordem_servico.data_criacao else ''],
            ['PREVISÃO ENTREGA:', ordem_servico.prazo_entrega.strftime('%d/%m/%Y') if ordem_servico.prazo_entrega else ''],
        ]

        tabela = Table(dados, colWidths=[45*mm, 135*mm])
        tabela.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ]))

        return tabela

    def _criar_materiais_os(self, ordem_servico):
        """Materiais utilizados na OS"""
        dados = [['CÓDIGO', 'DESCRIÇÃO', 'QTD', 'UN', 'CUSTO UNIT', 'TOTAL']]

        for prod in ordem_servico.produtos:
            custo_total = float(prod.custo_total or 0)
            dados.append([
                prod.produto_codigo or '',
                prod.produto_nome or '',
                f'{float(prod.quantidade or 0):,.2f}',
                prod.unidade or 'UN',
                f'R$ {float(prod.custo_unitario or 0):,.2f}',
                f'R$ {custo_total:,.2f}'
            ])

        tabela = Table(dados, colWidths=[25*mm, 65*mm, 18*mm, 15*mm, 28*mm, 29*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_FUNDO),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        return tabela

    def _criar_custos_os(self, ordem_servico):
        """Resumo de custos da OS"""
        mao_obra = float(ordem_servico.custo_mao_obra or 0)
        materiais = float(ordem_servico.custo_materiais or 0)
        total_custo = float(ordem_servico.custo_total or 0)
        valor_servico = float(ordem_servico.valor_servico or 0)

        dados = [
            ['Mão de Obra:', f'R$ {mao_obra:,.2f}'],
            ['Materiais:', f'R$ {materiais:,.2f}'],
            ['Custo Total:', f'R$ {total_custo:,.2f}'],
            ['VALOR DO SERVIÇO:', f'R$ {valor_servico:,.2f}'],
        ]

        tabela = Table(dados, colWidths=[130*mm, 50*mm])
        tabela.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('TEXTCOLOR', (0, -1), (-1, -1), self.COR_PRIMARIA),
            ('LINEABOVE', (0, -1), (-1, -1), 1, self.COR_PRIMARIA),
        ]))

        return tabela

    def _criar_assinaturas_os(self):
        """Área de assinaturas"""
        dados = [
            ['', '', ''],
            ['_' * 35, '_' * 35, '_' * 35],
            ['Responsável Técnico', 'Cliente', 'Controle de Qualidade'],
        ]

        tabela = Table(dados, colWidths=[60*mm, 60*mm, 60*mm])
        tabela.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
        ]))

        return tabela

    def gerar_relatorio_vendas(self, dados_vendas, periodo, salvar_arquivo=None):
        """
        Gera relatório de vendas em PDF

        Args:
            dados_vendas: Lista de dicionários com dados de vendas
            periodo: String com o período (ex: "Janeiro/2025")
            salvar_arquivo: Path para salvar (opcional)

        Returns:
            bytes: PDF em bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=10*mm,
            leftMargin=10*mm,
            topMargin=15*mm,
            bottomMargin=15*mm
        )

        elements = []

        # Título
        elements.append(Paragraph(
            f'RELATÓRIO DE VENDAS - {periodo}',
            self.styles['Titulo']
        ))
        elements.append(Spacer(1, 10*mm))

        # Data de geração
        elements.append(Paragraph(
            f'Gerado em: {datetime.now().strftime("%d/%m/%Y às %H:%M")}',
            self.styles['TextoPequeno']
        ))
        elements.append(Spacer(1, 10*mm))

        # Tabela de vendas
        dados_tabela = [['DATA', 'PEDIDO', 'CLIENTE', 'PRODUTOS', 'SUBTOTAL', 'DESC', 'FRETE', 'TOTAL', 'STATUS']]

        total_geral = 0
        for venda in dados_vendas:
            total_geral += float(venda.get('total', 0))
            dados_tabela.append([
                venda.get('data', ''),
                venda.get('numero', ''),
                venda.get('cliente', '')[:30],
                str(venda.get('qtd_produtos', 0)),
                f"R$ {float(venda.get('subtotal', 0)):,.2f}",
                f"R$ {float(venda.get('desconto', 0)):,.2f}",
                f"R$ {float(venda.get('frete', 0)):,.2f}",
                f"R$ {float(venda.get('total', 0)):,.2f}",
                venda.get('status', ''),
            ])

        # Linha de total
        dados_tabela.append(['', '', '', '', '', '', 'TOTAL GERAL:', f"R$ {total_geral:,.2f}", ''])

        tabela = Table(dados_tabela, colWidths=[22*mm, 25*mm, 55*mm, 18*mm, 28*mm, 25*mm, 25*mm, 30*mm, 25*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -2), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_PRIMARIA),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 10),
            ('TEXTCOLOR', (0, -1), (-1, -1), self.COR_PRIMARIA),
        ]))

        elements.append(tabela)

        doc.build(elements)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        if salvar_arquivo:
            with open(salvar_arquivo, 'wb') as f:
                f.write(pdf_bytes)

        return pdf_bytes

    def gerar_relatorio_estoque(self, produtos, salvar_arquivo=None):
        """
        Gera relatório de estoque em PDF

        Args:
            produtos: Lista de produtos com dados de estoque
            salvar_arquivo: Path para salvar (opcional)

        Returns:
            bytes: PDF em bytes
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=10*mm,
            leftMargin=10*mm,
            topMargin=15*mm,
            bottomMargin=15*mm
        )

        elements = []

        # Título
        elements.append(Paragraph('RELATÓRIO DE ESTOQUE', self.styles['Titulo']))
        elements.append(Spacer(1, 5*mm))
        elements.append(Paragraph(
            f'Gerado em: {datetime.now().strftime("%d/%m/%Y às %H:%M")}',
            self.styles['TextoPequeno']
        ))
        elements.append(Spacer(1, 10*mm))

        # Tabela de produtos
        dados = [['CÓDIGO', 'PRODUTO', 'ESTOQUE', 'MÍN', 'MÁX', 'STATUS', 'VALOR']]

        valor_total = 0
        for prod in produtos:
            estoque = float(prod.get('estoque', 0))
            preco = float(prod.get('preco', 0))
            valor_estoque = estoque * preco
            valor_total += valor_estoque

            status = 'OK'
            if estoque <= 0:
                status = 'SEM ESTOQUE'
            elif estoque <= float(prod.get('minimo', 0)):
                status = 'BAIXO'

            dados.append([
                prod.get('codigo', '')[:15],
                prod.get('nome', '')[:40],
                f"{estoque:,.0f}",
                f"{float(prod.get('minimo', 0)):,.0f}",
                f"{float(prod.get('maximo', 0)):,.0f}",
                status,
                f"R$ {valor_estoque:,.2f}"
            ])

        dados.append(['', '', '', '', '', 'VALOR TOTAL:', f"R$ {valor_total:,.2f}"])

        tabela = Table(dados, colWidths=[25*mm, 60*mm, 20*mm, 18*mm, 18*mm, 25*mm, 30*mm])
        tabela.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -2), 0.5, self.COR_BORDA),
            ('BACKGROUND', (0, 0), (-1, 0), self.COR_PRIMARIA),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))

        elements.append(tabela)

        doc.build(elements)

        pdf_bytes = buffer.getvalue()
        buffer.close()

        if salvar_arquivo:
            with open(salvar_arquivo, 'wb') as f:
                f.write(pdf_bytes)

        return pdf_bytes
