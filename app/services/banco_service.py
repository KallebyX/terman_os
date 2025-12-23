# -*- coding: utf-8 -*-
"""
Serviço de Integração Bancária
Suporte para principais bancos brasileiros via APIs
"""

import os
import json
import requests
import hashlib
import hmac
from datetime import datetime, timedelta
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class BancoService:
    """Serviço para integração com APIs bancárias"""

    # Códigos dos bancos
    BANCOS = {
        '001': {'nome': 'Banco do Brasil', 'api': 'bb'},
        '033': {'nome': 'Santander', 'api': 'santander'},
        '104': {'nome': 'Caixa Econômica Federal', 'api': 'caixa'},
        '237': {'nome': 'Bradesco', 'api': 'bradesco'},
        '341': {'nome': 'Itaú', 'api': 'itau'},
        '422': {'nome': 'Safra', 'api': 'safra'},
        '756': {'nome': 'Sicoob', 'api': 'sicoob'},
        '748': {'nome': 'Sicredi', 'api': 'sicredi'},
        '077': {'nome': 'Inter', 'api': 'inter'},
        '260': {'nome': 'Nubank', 'api': 'nubank'},
        '336': {'nome': 'C6 Bank', 'api': 'c6'},
    }

    # URLs base das APIs (sandbox e produção)
    API_URLS = {
        'bb': {
            'sandbox': 'https://api.sandbox.bb.com.br',
            'producao': 'https://api.bb.com.br'
        },
        'itau': {
            'sandbox': 'https://devportal.itau.com.br/sandboxapi',
            'producao': 'https://sts.itau.com.br'
        },
        'bradesco': {
            'sandbox': 'https://proxy.api.prebanco.com.br',
            'producao': 'https://openapi.bradesco.com.br'
        },
        'santander': {
            'sandbox': 'https://trust-sandbox.api.santander.com.br',
            'producao': 'https://trust.api.santander.com.br'
        },
        'inter': {
            'sandbox': 'https://cdpj-sandbox.partners.uatinter.co',
            'producao': 'https://cdpj.partners.bancointer.com.br'
        },
        'sicoob': {
            'sandbox': 'https://sandbox.sicoob.com.br',
            'producao': 'https://api.sicoob.com.br'
        }
    }

    def __init__(self, conta_bancaria):
        """
        Inicializa o serviço bancário

        Args:
            conta_bancaria: Objeto ContaBancaria com credenciais
        """
        self.conta = conta_bancaria
        self.banco_info = self.BANCOS.get(conta_bancaria.banco_codigo, {})
        self.api_type = self.banco_info.get('api', 'generico')
        self.ambiente = conta_bancaria.api_ambiente or 'sandbox'

    def obter_token(self):
        """
        Obtém token de autenticação OAuth2

        Returns:
            dict: Token de acesso e informações
        """
        if self.api_type == 'bb':
            return self._obter_token_bb()
        elif self.api_type == 'itau':
            return self._obter_token_itau()
        elif self.api_type == 'bradesco':
            return self._obter_token_bradesco()
        elif self.api_type == 'inter':
            return self._obter_token_inter()
        elif self.api_type == 'sicoob':
            return self._obter_token_sicoob()
        else:
            return {
                'sucesso': False,
                'erro': f'Banco {self.conta.banco_nome} não suportado para integração automática'
            }

    def consultar_saldo(self):
        """
        Consulta saldo da conta

        Returns:
            dict: Saldo atual e disponível
        """
        try:
            token = self._get_valid_token()
            if not token:
                return {'sucesso': False, 'erro': 'Não foi possível obter token de acesso'}

            if self.api_type == 'bb':
                return self._consultar_saldo_bb(token)
            elif self.api_type == 'itau':
                return self._consultar_saldo_itau(token)
            elif self.api_type == 'inter':
                return self._consultar_saldo_inter(token)
            else:
                return {'sucesso': False, 'erro': 'Consulta de saldo não implementada para este banco'}

        except Exception as e:
            logger.error(f"Erro ao consultar saldo: {str(e)}")
            return {'sucesso': False, 'erro': str(e)}

    def consultar_extrato(self, data_inicio, data_fim):
        """
        Consulta extrato bancário

        Args:
            data_inicio: Data inicial (date ou string YYYY-MM-DD)
            data_fim: Data final (date ou string YYYY-MM-DD)

        Returns:
            dict: Lista de transações
        """
        try:
            token = self._get_valid_token()
            if not token:
                return {'sucesso': False, 'erro': 'Não foi possível obter token de acesso'}

            if isinstance(data_inicio, str):
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            if isinstance(data_fim, str):
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()

            if self.api_type == 'bb':
                return self._consultar_extrato_bb(token, data_inicio, data_fim)
            elif self.api_type == 'itau':
                return self._consultar_extrato_itau(token, data_inicio, data_fim)
            elif self.api_type == 'inter':
                return self._consultar_extrato_inter(token, data_inicio, data_fim)
            else:
                return {'sucesso': False, 'erro': 'Consulta de extrato não implementada para este banco'}

        except Exception as e:
            logger.error(f"Erro ao consultar extrato: {str(e)}")
            return {'sucesso': False, 'erro': str(e)}

    def gerar_pix(self, valor, descricao, txid=None, expiracao=3600):
        """
        Gera cobrança PIX

        Args:
            valor: Valor da cobrança
            descricao: Descrição da cobrança
            txid: ID da transação (opcional, gerado automaticamente)
            expiracao: Tempo de expiração em segundos (padrão: 1 hora)

        Returns:
            dict: QR Code e informações do PIX
        """
        try:
            token = self._get_valid_token()
            if not token:
                return {'sucesso': False, 'erro': 'Não foi possível obter token de acesso'}

            if not txid:
                txid = self._gerar_txid()

            if self.api_type == 'bb':
                return self._gerar_pix_bb(token, valor, descricao, txid, expiracao)
            elif self.api_type == 'itau':
                return self._gerar_pix_itau(token, valor, descricao, txid, expiracao)
            elif self.api_type == 'inter':
                return self._gerar_pix_inter(token, valor, descricao, txid, expiracao)
            elif self.api_type == 'sicoob':
                return self._gerar_pix_sicoob(token, valor, descricao, txid, expiracao)
            else:
                return {'sucesso': False, 'erro': 'PIX não implementado para este banco'}

        except Exception as e:
            logger.error(f"Erro ao gerar PIX: {str(e)}")
            return {'sucesso': False, 'erro': str(e)}

    def consultar_pix(self, txid):
        """
        Consulta status de um PIX

        Args:
            txid: ID da transação

        Returns:
            dict: Status e informações do PIX
        """
        try:
            token = self._get_valid_token()
            if not token:
                return {'sucesso': False, 'erro': 'Não foi possível obter token de acesso'}

            if self.api_type == 'bb':
                return self._consultar_pix_bb(token, txid)
            elif self.api_type == 'inter':
                return self._consultar_pix_inter(token, txid)
            else:
                return {'sucesso': False, 'erro': 'Consulta PIX não implementada para este banco'}

        except Exception as e:
            logger.error(f"Erro ao consultar PIX: {str(e)}")
            return {'sucesso': False, 'erro': str(e)}

    def gerar_boleto(self, dados_boleto):
        """
        Gera boleto bancário

        Args:
            dados_boleto: Dict com dados do boleto:
                - valor: Valor do boleto
                - vencimento: Data de vencimento
                - pagador_nome: Nome do pagador
                - pagador_cpf_cnpj: CPF/CNPJ do pagador
                - pagador_endereco: Endereço completo
                - descricao: Descrição/Instruções
                - multa: Percentual de multa (opcional)
                - juros: Percentual de juros ao mês (opcional)

        Returns:
            dict: Linha digitável, código de barras e PDF
        """
        try:
            token = self._get_valid_token()
            if not token:
                return {'sucesso': False, 'erro': 'Não foi possível obter token de acesso'}

            if self.api_type == 'bb':
                return self._gerar_boleto_bb(token, dados_boleto)
            elif self.api_type == 'itau':
                return self._gerar_boleto_itau(token, dados_boleto)
            elif self.api_type == 'bradesco':
                return self._gerar_boleto_bradesco(token, dados_boleto)
            elif self.api_type == 'inter':
                return self._gerar_boleto_inter(token, dados_boleto)
            else:
                return {'sucesso': False, 'erro': 'Boleto não implementado para este banco'}

        except Exception as e:
            logger.error(f"Erro ao gerar boleto: {str(e)}")
            return {'sucesso': False, 'erro': str(e)}

    def configurar_webhook(self, url, eventos=None):
        """
        Configura webhook para notificações

        Args:
            url: URL do webhook
            eventos: Lista de eventos para notificar

        Returns:
            dict: Confirmação de configuração
        """
        try:
            token = self._get_valid_token()
            if not token:
                return {'sucesso': False, 'erro': 'Não foi possível obter token de acesso'}

            if self.api_type == 'bb':
                return self._configurar_webhook_bb(token, url)
            elif self.api_type == 'inter':
                return self._configurar_webhook_inter(token, url)
            else:
                return {'sucesso': False, 'erro': 'Webhook não implementado para este banco'}

        except Exception as e:
            logger.error(f"Erro ao configurar webhook: {str(e)}")
            return {'sucesso': False, 'erro': str(e)}

    # ====== Implementações específicas por banco ======

    def _obter_token_bb(self):
        """Obtém token do Banco do Brasil"""
        url = f"{self._get_base_url()}/oauth/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self._encode_credentials()}'
        }

        data = {
            'grant_type': 'client_credentials',
            'scope': 'cobrancas.boletos-requisicao cobrancas.boletos-info pix.cob.write pix.cob.read'
        }

        response = requests.post(url, headers=headers, data=data, timeout=30)

        if response.status_code == 200:
            token_data = response.json()
            self._salvar_token(token_data)
            return {
                'sucesso': True,
                'access_token': token_data.get('access_token'),
                'expires_in': token_data.get('expires_in')
            }
        else:
            return {
                'sucesso': False,
                'erro': f'Erro {response.status_code}: {response.text}'
            }

    def _obter_token_inter(self):
        """Obtém token do Banco Inter"""
        url = f"{self._get_base_url()}/oauth/v2/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'client_id': self.conta.api_client_id,
            'client_secret': self.conta.api_client_secret,
            'grant_type': 'client_credentials',
            'scope': 'extrato.read boleto-cobranca.read boleto-cobranca.write pix.read pix.write'
        }

        response = requests.post(url, headers=headers, data=data, timeout=30)

        if response.status_code == 200:
            token_data = response.json()
            self._salvar_token(token_data)
            return {
                'sucesso': True,
                'access_token': token_data.get('access_token'),
                'expires_in': token_data.get('expires_in')
            }
        else:
            return {
                'sucesso': False,
                'erro': f'Erro {response.status_code}: {response.text}'
            }

    def _obter_token_itau(self):
        """Obtém token do Itaú"""
        url = f"{self._get_base_url()}/oauth/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.conta.api_client_id,
            'client_secret': self.conta.api_client_secret
        }

        response = requests.post(url, headers=headers, data=data, timeout=30)

        if response.status_code == 200:
            token_data = response.json()
            self._salvar_token(token_data)
            return {
                'sucesso': True,
                'access_token': token_data.get('access_token'),
                'expires_in': token_data.get('expires_in')
            }
        else:
            return {
                'sucesso': False,
                'erro': f'Erro {response.status_code}: {response.text}'
            }

    def _obter_token_sicoob(self):
        """Obtém token do Sicoob"""
        url = f"{self._get_base_url()}/oauth/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self._encode_credentials()}'
        }

        data = {
            'grant_type': 'client_credentials',
            'scope': 'cob.read cob.write pix.read pix.write'
        }

        response = requests.post(url, headers=headers, data=data, timeout=30)

        if response.status_code == 200:
            token_data = response.json()
            self._salvar_token(token_data)
            return {
                'sucesso': True,
                'access_token': token_data.get('access_token'),
                'expires_in': token_data.get('expires_in')
            }
        else:
            return {
                'sucesso': False,
                'erro': f'Erro {response.status_code}: {response.text}'
            }

    def _obter_token_bradesco(self):
        """Obtém token do Bradesco"""
        url = f"{self._get_base_url()}/auth/server/v1.1/token"

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.conta.api_client_id,
            'client_secret': self.conta.api_client_secret
        }

        response = requests.post(url, headers=headers, data=data, timeout=30)

        if response.status_code == 200:
            token_data = response.json()
            self._salvar_token(token_data)
            return {
                'sucesso': True,
                'access_token': token_data.get('access_token'),
                'expires_in': token_data.get('expires_in')
            }
        else:
            return {
                'sucesso': False,
                'erro': f'Erro {response.status_code}: {response.text}'
            }

    def _consultar_saldo_bb(self, token):
        """Consulta saldo no Banco do Brasil"""
        url = f"{self._get_base_url()}/contas-correntes/v1/saldo"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        params = {
            'gw-dev-app-key': self.conta.api_client_id
        }

        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                'sucesso': True,
                'saldo_disponivel': float(data.get('saldoDisponivel', 0)),
                'saldo_bloqueado': float(data.get('saldoBloqueado', 0)),
                'limite': float(data.get('limite', 0)),
                'data_consulta': datetime.now().isoformat()
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _consultar_saldo_inter(self, token):
        """Consulta saldo no Banco Inter"""
        url = f"{self._get_base_url()}/banking/v2/saldo"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            return {
                'sucesso': True,
                'saldo_disponivel': float(data.get('disponivel', 0)),
                'saldo_bloqueado': float(data.get('bloqueadoCheque', 0)),
                'limite': float(data.get('limiteCredito', 0)),
                'data_consulta': datetime.now().isoformat()
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _consultar_extrato_bb(self, token, data_inicio, data_fim):
        """Consulta extrato no Banco do Brasil"""
        url = f"{self._get_base_url()}/contas-correntes/v1/extrato"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        params = {
            'gw-dev-app-key': self.conta.api_client_id,
            'dataInicioSolicitacao': data_inicio.strftime('%d.%m.%Y'),
            'dataFimSolicitacao': data_fim.strftime('%d.%m.%Y')
        }

        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            transacoes = []

            for item in data.get('listaLancamento', []):
                transacoes.append({
                    'data': item.get('dataLancamento'),
                    'descricao': item.get('textoDescricao'),
                    'valor': float(item.get('valorLancamento', 0)),
                    'tipo': 'credito' if item.get('indicadorTipoLancamento') == 'C' else 'debito',
                    'saldo_pos': float(item.get('valorSaldo', 0))
                })

            return {
                'sucesso': True,
                'transacoes': transacoes,
                'quantidade': len(transacoes)
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _consultar_extrato_inter(self, token, data_inicio, data_fim):
        """Consulta extrato no Banco Inter"""
        url = f"{self._get_base_url()}/banking/v2/extrato"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        params = {
            'dataInicio': data_inicio.strftime('%Y-%m-%d'),
            'dataFim': data_fim.strftime('%Y-%m-%d')
        }

        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            transacoes = []

            for item in data.get('transacoes', []):
                transacoes.append({
                    'data': item.get('dataEntrada'),
                    'descricao': item.get('descricao'),
                    'valor': float(item.get('valor', 0)),
                    'tipo': item.get('tipoOperacao', 'debito').lower(),
                    'saldo_pos': float(item.get('saldo', 0))
                })

            return {
                'sucesso': True,
                'transacoes': transacoes,
                'quantidade': len(transacoes)
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _gerar_pix_bb(self, token, valor, descricao, txid, expiracao):
        """Gera PIX no Banco do Brasil"""
        url = f"{self._get_base_url()}/pix/v1/cobqrcode/{txid}"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'gw-dev-app-key': self.conta.api_client_id
        }

        data = {
            'calendario': {
                'expiracao': expiracao
            },
            'valor': {
                'original': f'{float(valor):.2f}'
            },
            'chave': self.conta.pix_chave,
            'solicitacaoPagador': descricao[:140]
        }

        response = requests.put(url, headers=headers, json=data, timeout=30)

        if response.status_code in [200, 201]:
            result = response.json()
            return {
                'sucesso': True,
                'txid': txid,
                'qrcode': result.get('textoImagemQRcode'),
                'qrcode_base64': result.get('imagemQrcode'),
                'copia_cola': result.get('pixCopiaECola'),
                'valor': valor,
                'expiracao': expiracao
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _gerar_pix_inter(self, token, valor, descricao, txid, expiracao):
        """Gera PIX no Banco Inter"""
        url = f"{self._get_base_url()}/pix/v2/cob/{txid}"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        data = {
            'calendario': {
                'expiracao': expiracao
            },
            'valor': {
                'original': f'{float(valor):.2f}'
            },
            'chave': self.conta.pix_chave,
            'solicitacaoPagador': descricao[:140]
        }

        response = requests.put(url, headers=headers, json=data, timeout=30)

        if response.status_code in [200, 201]:
            result = response.json()

            # Obtém QR Code
            qr_url = f"{self._get_base_url()}/pix/v2/cob/{txid}/qrcode"
            qr_response = requests.get(qr_url, headers=headers, timeout=30)
            qr_data = qr_response.json() if qr_response.status_code == 200 else {}

            return {
                'sucesso': True,
                'txid': txid,
                'qrcode': qr_data.get('qrcode'),
                'qrcode_base64': qr_data.get('imagemQrcode'),
                'copia_cola': result.get('pixCopiaECola'),
                'valor': valor,
                'expiracao': expiracao
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _gerar_pix_sicoob(self, token, valor, descricao, txid, expiracao):
        """Gera PIX no Sicoob"""
        url = f"{self._get_base_url()}/pix/api/v2/cob/{txid}"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'client_id': self.conta.api_client_id
        }

        data = {
            'calendario': {
                'expiracao': expiracao
            },
            'valor': {
                'original': f'{float(valor):.2f}'
            },
            'chave': self.conta.pix_chave,
            'solicitacaoPagador': descricao[:140]
        }

        response = requests.put(url, headers=headers, json=data, timeout=30)

        if response.status_code in [200, 201]:
            result = response.json()
            return {
                'sucesso': True,
                'txid': txid,
                'qrcode': result.get('textoImagemQRcode'),
                'copia_cola': result.get('pixCopiaECola'),
                'valor': valor,
                'expiracao': expiracao
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _consultar_pix_bb(self, token, txid):
        """Consulta PIX no Banco do Brasil"""
        url = f"{self._get_base_url()}/pix/v1/cob/{txid}"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'gw-dev-app-key': self.conta.api_client_id
        }

        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            result = response.json()
            return {
                'sucesso': True,
                'txid': txid,
                'status': result.get('status'),
                'valor': float(result.get('valor', {}).get('original', 0)),
                'pago': result.get('status') == 'CONCLUIDA',
                'data_pagamento': result.get('pix', [{}])[0].get('horario') if result.get('pix') else None
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _consultar_pix_inter(self, token, txid):
        """Consulta PIX no Banco Inter"""
        url = f"{self._get_base_url()}/pix/v2/cob/{txid}"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            result = response.json()
            return {
                'sucesso': True,
                'txid': txid,
                'status': result.get('status'),
                'valor': float(result.get('valor', {}).get('original', 0)),
                'pago': result.get('status') == 'CONCLUIDA',
                'data_pagamento': result.get('pix', [{}])[0].get('horario') if result.get('pix') else None
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _gerar_boleto_bb(self, token, dados):
        """Gera boleto no Banco do Brasil"""
        url = f"{self._get_base_url()}/cobrancas/v2/boletos"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'gw-dev-app-key': self.conta.api_client_id
        }

        vencimento = dados.get('vencimento')
        if isinstance(vencimento, str):
            vencimento = datetime.strptime(vencimento, '%Y-%m-%d').date()

        body = {
            'numeroConvenio': self.conta.api_client_id,
            'dataVencimento': vencimento.strftime('%d.%m.%Y'),
            'valorOriginal': float(dados.get('valor', 0)),
            'pagador': {
                'tipoInscricao': 1 if len(dados.get('pagador_cpf_cnpj', '').replace('.', '').replace('-', '').replace('/', '')) == 11 else 2,
                'numeroInscricao': dados.get('pagador_cpf_cnpj', '').replace('.', '').replace('-', '').replace('/', ''),
                'nome': dados.get('pagador_nome', ''),
                'endereco': dados.get('pagador_endereco', ''),
                'cep': dados.get('pagador_cep', '').replace('-', ''),
                'cidade': dados.get('pagador_cidade', ''),
                'bairro': dados.get('pagador_bairro', ''),
                'uf': dados.get('pagador_uf', '')
            },
            'indicadorPix': 'S' if self.conta.pix_chave else 'N'
        }

        if dados.get('descricao'):
            body['descricaoTipoTitulo'] = dados.get('descricao')[:50]

        if dados.get('multa'):
            body['multa'] = {
                'tipo': 2,
                'porcentagem': float(dados.get('multa'))
            }

        if dados.get('juros'):
            body['jurosMora'] = {
                'tipo': 2,
                'porcentagem': float(dados.get('juros'))
            }

        response = requests.post(url, headers=headers, json=body, timeout=30)

        if response.status_code in [200, 201]:
            result = response.json()
            return {
                'sucesso': True,
                'numero': result.get('numero'),
                'linha_digitavel': result.get('linhaDigitavel'),
                'codigo_barras': result.get('codigoBarraNumerico'),
                'nosso_numero': result.get('nossoNumero'),
                'valor': dados.get('valor'),
                'vencimento': vencimento.strftime('%Y-%m-%d')
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _gerar_boleto_inter(self, token, dados):
        """Gera boleto no Banco Inter"""
        url = f"{self._get_base_url()}/cobranca/v2/boletos"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        vencimento = dados.get('vencimento')
        if isinstance(vencimento, str):
            vencimento = datetime.strptime(vencimento, '%Y-%m-%d').date()

        cpf_cnpj = dados.get('pagador_cpf_cnpj', '').replace('.', '').replace('-', '').replace('/', '')

        body = {
            'seuNumero': dados.get('numero', str(int(datetime.now().timestamp()))),
            'valorNominal': float(dados.get('valor', 0)),
            'dataVencimento': vencimento.strftime('%Y-%m-%d'),
            'numDiasAgenda': 60,
            'pagador': {
                'cpfCnpj': cpf_cnpj,
                'tipoPessoa': 'FISICA' if len(cpf_cnpj) == 11 else 'JURIDICA',
                'nome': dados.get('pagador_nome', ''),
                'endereco': dados.get('pagador_endereco', ''),
                'cidade': dados.get('pagador_cidade', ''),
                'uf': dados.get('pagador_uf', ''),
                'cep': dados.get('pagador_cep', '').replace('-', '')
            }
        }

        if dados.get('multa'):
            body['multa'] = {
                'codigoMulta': 'PERCENTUAL',
                'taxa': float(dados.get('multa'))
            }

        if dados.get('juros'):
            body['mora'] = {
                'codigoMora': 'TAXAMENSAL',
                'taxa': float(dados.get('juros'))
            }

        response = requests.post(url, headers=headers, json=body, timeout=30)

        if response.status_code in [200, 201]:
            result = response.json()
            return {
                'sucesso': True,
                'numero': result.get('nossoNumero'),
                'linha_digitavel': result.get('linhaDigitavel'),
                'codigo_barras': result.get('codigoBarras'),
                'nosso_numero': result.get('nossoNumero'),
                'valor': dados.get('valor'),
                'vencimento': vencimento.strftime('%Y-%m-%d')
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _configurar_webhook_bb(self, token, url):
        """Configura webhook no Banco do Brasil"""
        api_url = f"{self._get_base_url()}/pix/v1/webhook/{self.conta.pix_chave}"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'gw-dev-app-key': self.conta.api_client_id
        }

        body = {
            'webhookUrl': url
        }

        response = requests.put(api_url, headers=headers, json=body, timeout=30)

        if response.status_code in [200, 201, 204]:
            return {
                'sucesso': True,
                'mensagem': 'Webhook configurado com sucesso'
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    def _configurar_webhook_inter(self, token, url):
        """Configura webhook no Banco Inter"""
        api_url = f"{self._get_base_url()}/pix/v2/webhook/{self.conta.pix_chave}"

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        body = {
            'webhookUrl': url
        }

        response = requests.put(api_url, headers=headers, json=body, timeout=30)

        if response.status_code in [200, 201, 204]:
            return {
                'sucesso': True,
                'mensagem': 'Webhook configurado com sucesso'
            }
        else:
            return {'sucesso': False, 'erro': f'Erro {response.status_code}: {response.text}'}

    # ====== Métodos auxiliares ======

    def _get_base_url(self):
        """Obtém URL base da API"""
        urls = self.API_URLS.get(self.api_type, {})
        return urls.get(self.ambiente, urls.get('sandbox', ''))

    def _get_valid_token(self):
        """Obtém token válido (usa cache se não expirado)"""
        # Verifica se token está em cache e válido
        if self.conta.api_token and self.conta.api_token_expira:
            if datetime.now() < self.conta.api_token_expira:
                return self.conta.api_token

        # Obtém novo token
        result = self.obter_token()
        if result.get('sucesso'):
            return result.get('access_token')
        return None

    def _salvar_token(self, token_data):
        """Salva token no banco de dados"""
        from app import db

        self.conta.api_token = token_data.get('access_token')
        expires_in = token_data.get('expires_in', 3600)
        self.conta.api_token_expira = datetime.now() + timedelta(seconds=expires_in - 60)

        try:
            db.session.commit()
        except Exception as e:
            logger.error(f"Erro ao salvar token: {str(e)}")
            db.session.rollback()

    def _encode_credentials(self):
        """Codifica credenciais em Base64"""
        import base64
        credentials = f"{self.conta.api_client_id}:{self.conta.api_client_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def _gerar_txid(self):
        """Gera ID único para transação PIX"""
        import uuid
        return str(uuid.uuid4()).replace('-', '')[:35]

    def validar_webhook(self, payload, signature, secret=None):
        """
        Valida assinatura de webhook

        Args:
            payload: Corpo da requisição
            signature: Assinatura recebida
            secret: Secret do webhook (usa da conta se não informado)

        Returns:
            bool: True se válido
        """
        secret = secret or self.conta.webhook_secret
        if not secret:
            return False

        expected = hmac.new(
            secret.encode(),
            payload.encode() if isinstance(payload, str) else payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(expected, signature)
