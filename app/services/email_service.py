# -*- coding: utf-8 -*-
"""
Serviço de Email
Envio de NFe, Orçamentos, Relatórios para clientes e contabilista
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """Serviço para envio de emails com anexos"""

    # Templates de email
    TEMPLATE_NFE = """
    <html>
    <head>
        <style>
            body {{ font-family: 'Helvetica', Arial, sans-serif; color: #1d1d1f; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #0071e3; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background: #f5f5f7; }}
            .footer {{ padding: 20px; text-align: center; color: #86868b; font-size: 12px; }}
            .btn {{ display: inline-block; padding: 12px 24px; background: #0071e3; color: white; text-decoration: none; border-radius: 8px; }}
            .info {{ background: white; padding: 15px; margin: 10px 0; border-radius: 8px; }}
            .info strong {{ color: #0071e3; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{empresa_nome}</h1>
            </div>
            <div class="content">
                <h2>Nota Fiscal Eletrônica</h2>
                <p>Prezado(a) <strong>{destinatario_nome}</strong>,</p>
                <p>Segue em anexo a Nota Fiscal Eletrônica referente à sua compra.</p>

                <div class="info">
                    <p><strong>Número:</strong> {nfe_numero}</p>
                    <p><strong>Série:</strong> {nfe_serie}</p>
                    <p><strong>Chave de Acesso:</strong> {chave_acesso}</p>
                    <p><strong>Data de Emissão:</strong> {data_emissao}</p>
                    <p><strong>Valor Total:</strong> R$ {valor_total}</p>
                </div>

                <p>Anexos:</p>
                <ul>
                    <li>DANFE (PDF)</li>
                    <li>XML da NFe</li>
                </ul>

                <p>Para consultar a autenticidade da NFe, acesse:</p>
                <p><a href="https://www.nfe.fazenda.gov.br/portal/consultaRecaptcha.aspx" class="btn">Consultar NFe</a></p>
            </div>
            <div class="footer">
                <p>{empresa_nome}</p>
                <p>{empresa_endereco}</p>
                <p>{empresa_telefone} | {empresa_email}</p>
            </div>
        </div>
    </body>
    </html>
    """

    TEMPLATE_ORCAMENTO = """
    <html>
    <head>
        <style>
            body {{ font-family: 'Helvetica', Arial, sans-serif; color: #1d1d1f; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #0071e3; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background: #f5f5f7; }}
            .footer {{ padding: 20px; text-align: center; color: #86868b; font-size: 12px; }}
            .btn {{ display: inline-block; padding: 12px 24px; background: #30d158; color: white; text-decoration: none; border-radius: 8px; margin: 5px; }}
            .btn-outline {{ display: inline-block; padding: 12px 24px; background: white; color: #0071e3; text-decoration: none; border-radius: 8px; border: 1px solid #0071e3; margin: 5px; }}
            .info {{ background: white; padding: 15px; margin: 10px 0; border-radius: 8px; }}
            .info strong {{ color: #0071e3; }}
            .valor {{ font-size: 24px; color: #0071e3; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{empresa_nome}</h1>
            </div>
            <div class="content">
                <h2>Orçamento Comercial</h2>
                <p>Prezado(a) <strong>{cliente_nome}</strong>,</p>
                <p>Conforme solicitado, segue em anexo nosso orçamento.</p>

                <div class="info">
                    <p><strong>Orçamento Nº:</strong> {orcamento_numero}</p>
                    <p><strong>Data:</strong> {data_emissao}</p>
                    <p><strong>Válido até:</strong> {data_validade}</p>
                    <p><strong>Itens:</strong> {qtd_itens} produto(s)</p>
                    <p class="valor">Total: R$ {valor_total}</p>
                </div>

                <p><strong>Condições Comerciais:</strong></p>
                <ul>
                    <li>Pagamento: {forma_pagamento}</li>
                    <li>Prazo de Entrega: {prazo_entrega}</li>
                    <li>Frete: {frete}</li>
                </ul>

                <p style="text-align: center; margin-top: 20px;">
                    <a href="{link_aprovar}" class="btn">✓ Aprovar Orçamento</a>
                    <a href="{link_visualizar}" class="btn-outline">Ver Detalhes</a>
                </p>

                <p style="margin-top: 20px;">Em caso de dúvidas, entre em contato conosco.</p>
            </div>
            <div class="footer">
                <p>{empresa_nome}</p>
                <p>{empresa_endereco}</p>
                <p>{empresa_telefone} | {empresa_email}</p>
            </div>
        </div>
    </body>
    </html>
    """

    TEMPLATE_CONTABILIDADE = """
    <html>
    <head>
        <style>
            body {{ font-family: 'Helvetica', Arial, sans-serif; color: #1d1d1f; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #5856d6; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background: #f5f5f7; }}
            .footer {{ padding: 20px; text-align: center; color: #86868b; font-size: 12px; }}
            .info {{ background: white; padding: 15px; margin: 10px 0; border-radius: 8px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #d2d2d7; }}
            th {{ background: #f5f5f7; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Documentos Fiscais</h1>
                <p>{empresa_nome}</p>
            </div>
            <div class="content">
                <p>Prezado(a) <strong>{contador_nome}</strong>,</p>
                <p>Segue(m) em anexo o(s) documento(s) fiscal(is) para sua análise.</p>

                <div class="info">
                    <p><strong>Período:</strong> {periodo}</p>
                    <p><strong>Tipo:</strong> {tipo_documento}</p>
                    <p><strong>Quantidade:</strong> {quantidade} documento(s)</p>
                </div>

                <h3>Resumo:</h3>
                <table>
                    <tr>
                        <th>Descrição</th>
                        <th>Valor</th>
                    </tr>
                    <tr>
                        <td>Total de Notas Emitidas</td>
                        <td>R$ {total_emitidas}</td>
                    </tr>
                    <tr>
                        <td>Total de Notas Canceladas</td>
                        <td>R$ {total_canceladas}</td>
                    </tr>
                    <tr>
                        <td>ICMS Total</td>
                        <td>R$ {total_icms}</td>
                    </tr>
                    <tr>
                        <td>IPI Total</td>
                        <td>R$ {total_ipi}</td>
                    </tr>
                </table>

                <p><strong>Arquivos anexados:</strong></p>
                <ul>
                    {lista_arquivos}
                </ul>
            </div>
            <div class="footer">
                <p>Gerado automaticamente pelo Sistema TermanOS</p>
                <p>{empresa_nome} - CNPJ: {empresa_cnpj}</p>
            </div>
        </div>
    </body>
    </html>
    """

    def __init__(self, empresa=None):
        """
        Inicializa o serviço de email

        Args:
            empresa: Objeto ConfiguracaoEmpresa com dados de email
        """
        self.empresa = empresa

        # Configurações de email (usa da empresa ou variáveis de ambiente)
        if empresa and empresa.email_host_nfe:
            self.smtp_host = empresa.email_host_nfe
            self.smtp_port = empresa.email_porta_nfe or 587
            self.smtp_user = empresa.email_usuario_nfe
            self.smtp_password = empresa.email_senha_nfe
            self.use_tls = empresa.email_tls_nfe
        else:
            self.smtp_host = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
            self.smtp_port = int(os.environ.get('MAIL_PORT', 587))
            self.smtp_user = os.environ.get('MAIL_USERNAME', '')
            self.smtp_password = os.environ.get('MAIL_PASSWORD', '')
            self.use_tls = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'

        self.from_email = self.smtp_user
        self.from_name = empresa.razao_social if empresa else 'TermanOS'

    def enviar_nfe(self, nota_fiscal, destinatarios, pdf_bytes, xml_string, contabilista=None):
        """
        Envia NFe por email com DANFE e XML

        Args:
            nota_fiscal: Objeto NotaFiscal
            destinatarios: Lista de emails ou string única
            pdf_bytes: PDF do DANFE em bytes
            xml_string: XML da NFe como string
            contabilista: Objeto Contabilista (opcional)

        Returns:
            dict: Resultado do envio
        """
        if isinstance(destinatarios, str):
            destinatarios = [destinatarios]

        # Adiciona contabilista se configurado
        if contabilista and contabilista.receber_nfe_xml and contabilista.email:
            if contabilista.email not in destinatarios:
                destinatarios.append(contabilista.email)

        # Prepara dados do template
        dados = {
            'empresa_nome': self.empresa.razao_social if self.empresa else 'Empresa',
            'empresa_endereco': f'{self.empresa.logradouro}, {self.empresa.numero} - {self.empresa.cidade}/{self.empresa.uf}' if self.empresa else '',
            'empresa_telefone': self.empresa.telefone if self.empresa else '',
            'empresa_email': self.empresa.email if self.empresa else '',
            'destinatario_nome': nota_fiscal.destinatario_razao_social or 'Cliente',
            'nfe_numero': nota_fiscal.numero,
            'nfe_serie': nota_fiscal.serie,
            'chave_acesso': nota_fiscal.chave_acesso or '',
            'data_emissao': nota_fiscal.data_emissao.strftime('%d/%m/%Y') if nota_fiscal.data_emissao else '',
            'valor_total': f'{float(nota_fiscal.valor_total or 0):,.2f}',
        }

        html_body = self.TEMPLATE_NFE.format(**dados)

        # Assunto do email
        assunto = f'NFe {nota_fiscal.numero} - {self.empresa.razao_social if self.empresa else "Empresa"}'

        # Anexos
        anexos = []
        if pdf_bytes:
            anexos.append({
                'nome': f'DANFE_{nota_fiscal.numero}.pdf',
                'conteudo': pdf_bytes,
                'tipo': 'application/pdf'
            })
        if xml_string:
            anexos.append({
                'nome': f'NFe_{nota_fiscal.chave_acesso}.xml',
                'conteudo': xml_string.encode('utf-8'),
                'tipo': 'application/xml'
            })

        return self._enviar_email(destinatarios, assunto, html_body, anexos)

    def enviar_orcamento(self, orcamento, pdf_bytes, link_aprovar=None, link_visualizar=None):
        """
        Envia orçamento por email

        Args:
            orcamento: Objeto Orcamento
            pdf_bytes: PDF do orçamento em bytes
            link_aprovar: URL para aprovar o orçamento
            link_visualizar: URL para visualizar detalhes

        Returns:
            dict: Resultado do envio
        """
        destinatarios = [orcamento.cliente_email] if orcamento.cliente_email else []

        if not destinatarios:
            return {
                'sucesso': False,
                'erro': 'Email do cliente não informado'
            }

        # Prepara dados do template
        base_url = os.environ.get('BASE_URL', 'http://localhost:5000')
        dados = {
            'empresa_nome': self.empresa.razao_social if self.empresa else 'Empresa',
            'empresa_endereco': f'{self.empresa.logradouro}, {self.empresa.numero}' if self.empresa else '',
            'empresa_telefone': self.empresa.telefone if self.empresa else '',
            'empresa_email': self.empresa.email if self.empresa else '',
            'cliente_nome': orcamento.cliente_nome or 'Cliente',
            'orcamento_numero': orcamento.numero_orcamento,
            'data_emissao': orcamento.data_criacao.strftime('%d/%m/%Y') if orcamento.data_criacao else '',
            'data_validade': orcamento.data_validade.strftime('%d/%m/%Y') if orcamento.data_validade else '',
            'qtd_itens': orcamento.itens.count() if hasattr(orcamento.itens, 'count') else len(list(orcamento.itens)),
            'valor_total': f'{float(orcamento.total or 0):,.2f}',
            'forma_pagamento': orcamento.forma_pagamento or 'A combinar',
            'prazo_entrega': orcamento.prazo_entrega or 'A combinar',
            'frete': orcamento.frete_tipo or 'A combinar',
            'link_aprovar': link_aprovar or f'{base_url}/orcamento/{orcamento.token_visualizacao}/aprovar',
            'link_visualizar': link_visualizar or f'{base_url}/orcamento/{orcamento.token_visualizacao}',
        }

        html_body = self.TEMPLATE_ORCAMENTO.format(**dados)

        assunto = f'Orçamento {orcamento.numero_orcamento} - {self.empresa.razao_social if self.empresa else "Empresa"}'

        anexos = []
        if pdf_bytes:
            anexos.append({
                'nome': f'Orcamento_{orcamento.numero_orcamento}.pdf',
                'conteudo': pdf_bytes,
                'tipo': 'application/pdf'
            })

        return self._enviar_email(destinatarios, assunto, html_body, anexos)

    def enviar_para_contabilidade(self, contabilista, periodo, tipo_documento, arquivos, resumo=None):
        """
        Envia documentos fiscais para o contabilista

        Args:
            contabilista: Objeto Contabilista
            periodo: String do período (ex: "Dezembro/2024")
            tipo_documento: Tipo de documento (NFe, NFCe, CTe, etc)
            arquivos: Lista de dicts com {nome, conteudo, tipo}
            resumo: Dict com valores resumidos

        Returns:
            dict: Resultado do envio
        """
        if not contabilista or not contabilista.email:
            return {
                'sucesso': False,
                'erro': 'Email do contabilista não configurado'
            }

        resumo = resumo or {}

        # Lista de arquivos para template
        lista_arquivos = '\n'.join([f"<li>{arq['nome']}</li>" for arq in arquivos])

        dados = {
            'empresa_nome': self.empresa.razao_social if self.empresa else 'Empresa',
            'empresa_cnpj': self.empresa.cnpj if self.empresa else '',
            'contador_nome': contabilista.nome,
            'periodo': periodo,
            'tipo_documento': tipo_documento,
            'quantidade': len(arquivos),
            'total_emitidas': f"{resumo.get('total_emitidas', 0):,.2f}",
            'total_canceladas': f"{resumo.get('total_canceladas', 0):,.2f}",
            'total_icms': f"{resumo.get('total_icms', 0):,.2f}",
            'total_ipi': f"{resumo.get('total_ipi', 0):,.2f}",
            'lista_arquivos': lista_arquivos
        }

        html_body = self.TEMPLATE_CONTABILIDADE.format(**dados)

        assunto = f'[Documentos Fiscais] {tipo_documento} - {periodo} - {self.empresa.razao_social if self.empresa else "Empresa"}'

        return self._enviar_email([contabilista.email], assunto, html_body, arquivos)

    def enviar_relatorio(self, destinatarios, titulo, descricao, pdf_bytes):
        """
        Envia relatório por email

        Args:
            destinatarios: Lista de emails
            titulo: Título do relatório
            descricao: Descrição do conteúdo
            pdf_bytes: PDF do relatório em bytes

        Returns:
            dict: Resultado do envio
        """
        if isinstance(destinatarios, str):
            destinatarios = [destinatarios]

        html_body = f"""
        <html>
        <body style="font-family: 'Helvetica', Arial, sans-serif; color: #1d1d1f; padding: 20px;">
            <h2 style="color: #0071e3;">{titulo}</h2>
            <p>{descricao}</p>
            <p>Segue o relatório em anexo.</p>
            <hr style="border: 1px solid #d2d2d7; margin: 20px 0;">
            <p style="color: #86868b; font-size: 12px;">
                Gerado em {datetime.now().strftime('%d/%m/%Y às %H:%M')}<br>
                {self.empresa.razao_social if self.empresa else 'TermanOS'}
            </p>
        </body>
        </html>
        """

        anexos = [{
            'nome': f'{titulo.replace(" ", "_")}.pdf',
            'conteudo': pdf_bytes,
            'tipo': 'application/pdf'
        }]

        return self._enviar_email(destinatarios, titulo, html_body, anexos)

    def enviar_cancelamento_nfe(self, nota_fiscal, destinatarios, contabilista=None):
        """
        Envia notificação de cancelamento de NFe

        Args:
            nota_fiscal: Objeto NotaFiscal cancelada
            destinatarios: Lista de emails
            contabilista: Objeto Contabilista (opcional)

        Returns:
            dict: Resultado do envio
        """
        if isinstance(destinatarios, str):
            destinatarios = [destinatarios]

        if contabilista and contabilista.receber_nfe_cancelamento and contabilista.email:
            if contabilista.email not in destinatarios:
                destinatarios.append(contabilista.email)

        html_body = f"""
        <html>
        <body style="font-family: 'Helvetica', Arial, sans-serif; color: #1d1d1f; padding: 20px;">
            <div style="background: #ff453a; color: white; padding: 20px; text-align: center; border-radius: 8px;">
                <h2>⚠️ NFe CANCELADA</h2>
            </div>
            <div style="padding: 20px; background: #f5f5f7; margin-top: 10px; border-radius: 8px;">
                <p>Informamos que a Nota Fiscal abaixo foi cancelada:</p>
                <ul>
                    <li><strong>Número:</strong> {nota_fiscal.numero}</li>
                    <li><strong>Série:</strong> {nota_fiscal.serie}</li>
                    <li><strong>Chave de Acesso:</strong> {nota_fiscal.chave_acesso}</li>
                    <li><strong>Data Cancelamento:</strong> {nota_fiscal.data_cancelamento.strftime('%d/%m/%Y %H:%M') if nota_fiscal.data_cancelamento else ''}</li>
                    <li><strong>Protocolo:</strong> {nota_fiscal.protocolo_cancelamento or ''}</li>
                    <li><strong>Justificativa:</strong> {nota_fiscal.justificativa_cancelamento or ''}</li>
                </ul>
            </div>
            <p style="color: #86868b; font-size: 12px; margin-top: 20px;">
                {self.empresa.razao_social if self.empresa else 'TermanOS'}
            </p>
        </body>
        </html>
        """

        assunto = f'[CANCELADA] NFe {nota_fiscal.numero} - {self.empresa.razao_social if self.empresa else "Empresa"}'

        return self._enviar_email(destinatarios, assunto, html_body, [])

    def _enviar_email(self, destinatarios, assunto, html_body, anexos=None):
        """
        Método interno para envio de email

        Args:
            destinatarios: Lista de emails
            assunto: Assunto do email
            html_body: Corpo em HTML
            anexos: Lista de dicts com {nome, conteudo, tipo}

        Returns:
            dict: Resultado do envio
        """
        anexos = anexos or []

        try:
            # Cria mensagem
            msg = MIMEMultipart('mixed')
            msg['Subject'] = assunto
            msg['From'] = f'{self.from_name} <{self.from_email}>'
            msg['To'] = ', '.join(destinatarios)

            # Corpo HTML
            html_part = MIMEText(html_body, 'html', 'utf-8')
            msg.attach(html_part)

            # Anexos
            for anexo in anexos:
                if isinstance(anexo.get('conteudo'), str):
                    conteudo = anexo['conteudo'].encode('utf-8')
                else:
                    conteudo = anexo['conteudo']

                part = MIMEApplication(conteudo, Name=anexo['nome'])
                part['Content-Disposition'] = f'attachment; filename="{anexo["nome"]}"'
                msg.attach(part)

            # Conecta e envia
            if self.use_tls:
                context = ssl.create_default_context()
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls(context=context)
                    server.login(self.smtp_user, self.smtp_password)
                    server.sendmail(self.from_email, destinatarios, msg.as_string())
            else:
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                    server.login(self.smtp_user, self.smtp_password)
                    server.sendmail(self.from_email, destinatarios, msg.as_string())

            logger.info(f"Email enviado com sucesso para: {', '.join(destinatarios)}")
            return {
                'sucesso': True,
                'destinatarios': destinatarios,
                'mensagem': 'Email enviado com sucesso'
            }

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"Erro de autenticação SMTP: {str(e)}")
            return {
                'sucesso': False,
                'erro': 'Erro de autenticação no servidor de email'
            }
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"Destinatários rejeitados: {str(e)}")
            return {
                'sucesso': False,
                'erro': 'Um ou mais destinatários foram rejeitados'
            }
        except Exception as e:
            logger.error(f"Erro ao enviar email: {str(e)}")
            return {
                'sucesso': False,
                'erro': str(e)
            }

    def testar_conexao(self):
        """
        Testa conexão com servidor SMTP

        Returns:
            dict: Resultado do teste
        """
        try:
            if self.use_tls:
                context = ssl.create_default_context()
                with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=10) as server:
                    server.starttls(context=context)
                    server.login(self.smtp_user, self.smtp_password)
            else:
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, timeout=10) as server:
                    server.login(self.smtp_user, self.smtp_password)

            return {
                'sucesso': True,
                'mensagem': 'Conexão SMTP bem sucedida'
            }

        except Exception as e:
            return {
                'sucesso': False,
                'erro': str(e)
            }
