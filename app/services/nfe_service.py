# -*- coding: utf-8 -*-
"""
Serviço de Nota Fiscal Eletrônica (NFe)
Integração completa com SEFAZ - Layout 4.00
"""

import os
import random
import hashlib
from datetime import datetime
from decimal import Decimal
from lxml import etree
import requests
import logging

from .certificado_service import CertificadoService

logger = logging.getLogger(__name__)


class NFeService:
    """Serviço para emissão, transmissão e gerenciamento de NFe"""

    # Versão do layout NFe
    VERSAO_NFE = '4.00'

    # Namespaces
    NS_NFE = 'http://www.portalfiscal.inf.br/nfe'
    NS_SOAP = 'http://www.w3.org/2003/05/soap-envelope'

    # URLs dos Web Services SEFAZ por UF
    WS_URLS = {
        'RS': {
            'homologacao': {
                'autorizacao': 'https://nfe-homologacao.sefazrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao4.asmx',
                'retorno': 'https://nfe-homologacao.sefazrs.rs.gov.br/ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx',
                'consulta': 'https://nfe-homologacao.sefazrs.rs.gov.br/ws/NfeConsulta/NfeConsulta4.asmx',
                'inutilizacao': 'https://nfe-homologacao.sefazrs.rs.gov.br/ws/NfeInutilizacao/NfeInutilizacao4.asmx',
                'evento': 'https://nfe-homologacao.sefazrs.rs.gov.br/ws/recepcaoevento/recepcaoevento4.asmx',
                'status': 'https://nfe-homologacao.sefazrs.rs.gov.br/ws/NfeStatusServico/NfeStatusServico4.asmx',
            },
            'producao': {
                'autorizacao': 'https://nfe.sefazrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao4.asmx',
                'retorno': 'https://nfe.sefazrs.rs.gov.br/ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx',
                'consulta': 'https://nfe.sefazrs.rs.gov.br/ws/NfeConsulta/NfeConsulta4.asmx',
                'inutilizacao': 'https://nfe.sefazrs.rs.gov.br/ws/NfeInutilizacao/NfeInutilizacao4.asmx',
                'evento': 'https://nfe.sefazrs.rs.gov.br/ws/recepcaoevento/recepcaoevento4.asmx',
                'status': 'https://nfe.sefazrs.rs.gov.br/ws/NfeStatusServico/NfeStatusServico4.asmx',
            }
        },
        'SVRS': {  # SEFAZ Virtual RS - usado por vários estados
            'homologacao': {
                'autorizacao': 'https://nfe-homologacao.svrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao4.asmx',
                'retorno': 'https://nfe-homologacao.svrs.rs.gov.br/ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx',
                'consulta': 'https://nfe-homologacao.svrs.rs.gov.br/ws/NfeConsulta/NfeConsulta4.asmx',
                'inutilizacao': 'https://nfe-homologacao.svrs.rs.gov.br/ws/NfeInutilizacao/NfeInutilizacao4.asmx',
                'evento': 'https://nfe-homologacao.svrs.rs.gov.br/ws/recepcaoevento/recepcaoevento4.asmx',
                'status': 'https://nfe-homologacao.svrs.rs.gov.br/ws/NfeStatusServico/NfeStatusServico4.asmx',
            },
            'producao': {
                'autorizacao': 'https://nfe.svrs.rs.gov.br/ws/NfeAutorizacao/NFeAutorizacao4.asmx',
                'retorno': 'https://nfe.svrs.rs.gov.br/ws/NfeRetAutorizacao/NFeRetAutorizacao4.asmx',
                'consulta': 'https://nfe.svrs.rs.gov.br/ws/NfeConsulta/NfeConsulta4.asmx',
                'inutilizacao': 'https://nfe.svrs.rs.gov.br/ws/NfeInutilizacao/NfeInutilizacao4.asmx',
                'evento': 'https://nfe.svrs.rs.gov.br/ws/recepcaoevento/recepcaoevento4.asmx',
                'status': 'https://nfe.svrs.rs.gov.br/ws/NfeStatusServico/NfeStatusServico4.asmx',
            }
        },
        'SP': {
            'homologacao': {
                'autorizacao': 'https://homologacao.nfe.fazenda.sp.gov.br/ws/nfeautorizacao4.asmx',
                'retorno': 'https://homologacao.nfe.fazenda.sp.gov.br/ws/nferetautorizacao4.asmx',
                'consulta': 'https://homologacao.nfe.fazenda.sp.gov.br/ws/nfeconsultaprotocolo4.asmx',
                'inutilizacao': 'https://homologacao.nfe.fazenda.sp.gov.br/ws/nfeinutilizacao4.asmx',
                'evento': 'https://homologacao.nfe.fazenda.sp.gov.br/ws/nferecepcaoevento4.asmx',
                'status': 'https://homologacao.nfe.fazenda.sp.gov.br/ws/nfestatusservico4.asmx',
            },
            'producao': {
                'autorizacao': 'https://nfe.fazenda.sp.gov.br/ws/nfeautorizacao4.asmx',
                'retorno': 'https://nfe.fazenda.sp.gov.br/ws/nferetautorizacao4.asmx',
                'consulta': 'https://nfe.fazenda.sp.gov.br/ws/nfeconsultaprotocolo4.asmx',
                'inutilizacao': 'https://nfe.fazenda.sp.gov.br/ws/nfeinutilizacao4.asmx',
                'evento': 'https://nfe.fazenda.sp.gov.br/ws/nferecepcaoevento4.asmx',
                'status': 'https://nfe.fazenda.sp.gov.br/ws/nfestatusservico4.asmx',
            }
        }
    }

    # Códigos IBGE dos estados
    CODIGO_UF = {
        'AC': '12', 'AL': '27', 'AM': '13', 'AP': '16', 'BA': '29',
        'CE': '23', 'DF': '53', 'ES': '32', 'GO': '52', 'MA': '21',
        'MG': '31', 'MS': '50', 'MT': '51', 'PA': '15', 'PB': '25',
        'PE': '26', 'PI': '22', 'PR': '41', 'RJ': '33', 'RN': '24',
        'RO': '11', 'RR': '14', 'RS': '43', 'SC': '42', 'SE': '28',
        'SP': '35', 'TO': '17'
    }

    def __init__(self, empresa, certificado_service=None):
        """
        Inicializa o serviço de NFe

        Args:
            empresa: Objeto ConfiguracaoEmpresa
            certificado_service: Instância de CertificadoService já configurada
        """
        self.empresa = empresa
        self.certificado_service = certificado_service
        self.uf = empresa.uf if empresa else 'RS'
        self.ambiente = empresa.ambiente_nfe if empresa else 2

    def gerar_xml_nfe(self, nota_fiscal):
        """
        Gera o XML completo da NFe (Layout 4.00)

        Args:
            nota_fiscal: Objeto NotaFiscal com todos os dados

        Returns:
            str: XML da NFe pronto para assinatura
        """
        # Gera código numérico aleatório (8 dígitos)
        codigo_numerico = str(random.randint(10000000, 99999999))

        # Gera chave de acesso
        ano_mes = nota_fiscal.data_emissao.strftime('%y%m')
        cnpj_limpo = self.empresa.cnpj.replace('.', '').replace('/', '').replace('-', '')

        chave_acesso = self._gerar_chave_acesso(
            self.CODIGO_UF.get(self.uf, '43'),
            ano_mes,
            cnpj_limpo,
            nota_fiscal.modelo,
            nota_fiscal.serie,
            nota_fiscal.numero,
            1,  # Tipo emissão normal
            codigo_numerico
        )

        # Namespace
        NSMAP = {None: self.NS_NFE}

        # Elemento raiz NFe
        nfe = etree.Element('NFe', nsmap=NSMAP)

        # infNFe
        inf_nfe = etree.SubElement(nfe, 'infNFe', versao=self.VERSAO_NFE, Id=f'NFe{chave_acesso}')

        # ide - Identificação da NFe
        ide = etree.SubElement(inf_nfe, 'ide')
        self._add_element(ide, 'cUF', self.CODIGO_UF.get(self.uf, '43'))
        self._add_element(ide, 'cNF', codigo_numerico)
        self._add_element(ide, 'natOp', nota_fiscal.natureza_operacao[:60])
        self._add_element(ide, 'mod', nota_fiscal.modelo)
        self._add_element(ide, 'serie', str(nota_fiscal.serie))
        self._add_element(ide, 'nNF', str(nota_fiscal.numero))
        self._add_element(ide, 'dhEmi', nota_fiscal.data_emissao.strftime('%Y-%m-%dT%H:%M:%S-03:00'))

        if nota_fiscal.data_saida_entrada:
            self._add_element(ide, 'dhSaiEnt', nota_fiscal.data_saida_entrada.strftime('%Y-%m-%dT%H:%M:%S-03:00'))

        self._add_element(ide, 'tpNF', str(nota_fiscal.tipo_operacao))  # 0=Entrada, 1=Saída
        self._add_element(ide, 'idDest', '1')  # 1=Operação interna, 2=Interestadual, 3=Exterior
        self._add_element(ide, 'cMunFG', self.empresa.codigo_municipio)
        self._add_element(ide, 'tpImp', '1')  # 1=Retrato, 2=Paisagem
        self._add_element(ide, 'tpEmis', '1')  # 1=Normal
        self._add_element(ide, 'cDV', chave_acesso[-1])
        self._add_element(ide, 'tpAmb', str(self.ambiente))
        self._add_element(ide, 'finNFe', str(nota_fiscal.finalidade))
        self._add_element(ide, 'indFinal', str(nota_fiscal.indicador_consumidor_final))
        self._add_element(ide, 'indPres', str(nota_fiscal.indicador_presenca))
        self._add_element(ide, 'procEmi', '0')  # 0=Aplicativo do contribuinte
        self._add_element(ide, 'verProc', 'TermanOS 1.0')

        # emit - Emitente
        emit = etree.SubElement(inf_nfe, 'emit')
        self._add_element(emit, 'CNPJ', cnpj_limpo)
        self._add_element(emit, 'xNome', self.empresa.razao_social[:60])

        if self.empresa.nome_fantasia:
            self._add_element(emit, 'xFant', self.empresa.nome_fantasia[:60])

        # Endereço do emitente
        ender_emit = etree.SubElement(emit, 'enderEmit')
        self._add_element(ender_emit, 'xLgr', self.empresa.logradouro[:60])
        self._add_element(ender_emit, 'nro', self.empresa.numero[:60])

        if self.empresa.complemento:
            self._add_element(ender_emit, 'xCpl', self.empresa.complemento[:60])

        self._add_element(ender_emit, 'xBairro', self.empresa.bairro[:60])
        self._add_element(ender_emit, 'cMun', self.empresa.codigo_municipio)
        self._add_element(ender_emit, 'xMun', self.empresa.cidade[:60])
        self._add_element(ender_emit, 'UF', self.empresa.uf)
        self._add_element(ender_emit, 'CEP', self.empresa.cep.replace('-', ''))
        self._add_element(ender_emit, 'cPais', self.empresa.codigo_pais or '1058')
        self._add_element(ender_emit, 'xPais', self.empresa.pais or 'Brasil')

        if self.empresa.telefone:
            self._add_element(ender_emit, 'fone', self._limpar_telefone(self.empresa.telefone))

        self._add_element(emit, 'IE', self.empresa.inscricao_estadual.replace('.', '').replace('-', ''))
        self._add_element(emit, 'CRT', str(self.empresa.regime_tributario))

        # dest - Destinatário
        dest = etree.SubElement(inf_nfe, 'dest')

        cpf_cnpj_dest = nota_fiscal.destinatario_cpf_cnpj.replace('.', '').replace('/', '').replace('-', '') if nota_fiscal.destinatario_cpf_cnpj else ''

        if len(cpf_cnpj_dest) == 11:
            self._add_element(dest, 'CPF', cpf_cnpj_dest)
        elif len(cpf_cnpj_dest) == 14:
            self._add_element(dest, 'CNPJ', cpf_cnpj_dest)

        self._add_element(dest, 'xNome', nota_fiscal.destinatario_razao_social[:60] if nota_fiscal.destinatario_razao_social else 'CONSUMIDOR')
        self._add_element(dest, 'indIEDest', str(nota_fiscal.indicador_ie_destinatario))

        if nota_fiscal.destinatario_ie and nota_fiscal.indicador_ie_destinatario == 1:
            self._add_element(dest, 'IE', nota_fiscal.destinatario_ie.replace('.', '').replace('-', ''))

        if nota_fiscal.destinatario_email:
            self._add_element(dest, 'email', nota_fiscal.destinatario_email[:60])

        # det - Detalhamento dos produtos/serviços
        for item in nota_fiscal.itens:
            det = etree.SubElement(inf_nfe, 'det', nItem=str(item.numero_item))

            prod = etree.SubElement(det, 'prod')
            self._add_element(prod, 'cProd', item.codigo[:60])
            self._add_element(prod, 'cEAN', item.ean or 'SEM GTIN')
            self._add_element(prod, 'xProd', item.descricao[:120])
            self._add_element(prod, 'NCM', item.ncm)

            if item.cest:
                self._add_element(prod, 'CEST', item.cest)

            self._add_element(prod, 'CFOP', item.cfop)
            self._add_element(prod, 'uCom', item.unidade[:6])
            self._add_element(prod, 'qCom', self._format_decimal(item.quantidade, 4))
            self._add_element(prod, 'vUnCom', self._format_decimal(item.valor_unitario, 10))
            self._add_element(prod, 'vProd', self._format_decimal(item.valor_total, 2))
            self._add_element(prod, 'cEANTrib', item.ean_tributavel or 'SEM GTIN')
            self._add_element(prod, 'uTrib', item.unidade_tributavel or item.unidade[:6])
            self._add_element(prod, 'qTrib', self._format_decimal(item.quantidade_tributavel or item.quantidade, 4))
            self._add_element(prod, 'vUnTrib', self._format_decimal(item.valor_unitario_tributavel or item.valor_unitario, 10))
            self._add_element(prod, 'indTot', '1')

            if item.valor_desconto and item.valor_desconto > 0:
                self._add_element(prod, 'vDesc', self._format_decimal(item.valor_desconto, 2))

            # Impostos
            imposto = etree.SubElement(det, 'imposto')

            # Valor aproximado de tributos (Lei de Transparência)
            if item.valor_aproximado_tributos and item.valor_aproximado_tributos > 0:
                self._add_element(imposto, 'vTotTrib', self._format_decimal(item.valor_aproximado_tributos, 2))

            # ICMS
            icms = etree.SubElement(imposto, 'ICMS')
            self._gerar_icms(icms, item)

            # IPI (se aplicável)
            if item.cst_ipi:
                ipi = etree.SubElement(imposto, 'IPI')
                self._gerar_ipi(ipi, item)

            # PIS
            pis = etree.SubElement(imposto, 'PIS')
            self._gerar_pis(pis, item)

            # COFINS
            cofins = etree.SubElement(imposto, 'COFINS')
            self._gerar_cofins(cofins, item)

            # Informações adicionais do produto
            if item.informacoes_adicionais:
                self._add_element(det, 'infAdProd', item.informacoes_adicionais[:500])

        # total - Totais da NFe
        total = etree.SubElement(inf_nfe, 'total')
        icms_tot = etree.SubElement(total, 'ICMSTot')

        self._add_element(icms_tot, 'vBC', self._format_decimal(nota_fiscal.valor_bc_icms, 2))
        self._add_element(icms_tot, 'vICMS', self._format_decimal(nota_fiscal.valor_icms, 2))
        self._add_element(icms_tot, 'vICMSDeson', '0.00')
        self._add_element(icms_tot, 'vFCPUFDest', '0.00')
        self._add_element(icms_tot, 'vICMSUFDest', '0.00')
        self._add_element(icms_tot, 'vICMSUFRemet', '0.00')
        self._add_element(icms_tot, 'vFCP', self._format_decimal(nota_fiscal.valor_fcp, 2))
        self._add_element(icms_tot, 'vBCST', self._format_decimal(nota_fiscal.valor_bc_icms_st, 2))
        self._add_element(icms_tot, 'vST', self._format_decimal(nota_fiscal.valor_icms_st, 2))
        self._add_element(icms_tot, 'vFCPST', '0.00')
        self._add_element(icms_tot, 'vFCPSTRet', '0.00')
        self._add_element(icms_tot, 'vProd', self._format_decimal(nota_fiscal.valor_produtos, 2))
        self._add_element(icms_tot, 'vFrete', self._format_decimal(nota_fiscal.valor_frete, 2))
        self._add_element(icms_tot, 'vSeg', self._format_decimal(nota_fiscal.valor_seguro, 2))
        self._add_element(icms_tot, 'vDesc', self._format_decimal(nota_fiscal.valor_desconto, 2))
        self._add_element(icms_tot, 'vII', self._format_decimal(nota_fiscal.valor_ii, 2))
        self._add_element(icms_tot, 'vIPI', self._format_decimal(nota_fiscal.valor_ipi, 2))
        self._add_element(icms_tot, 'vIPIDevol', '0.00')
        self._add_element(icms_tot, 'vPIS', self._format_decimal(nota_fiscal.valor_pis, 2))
        self._add_element(icms_tot, 'vCOFINS', self._format_decimal(nota_fiscal.valor_cofins, 2))
        self._add_element(icms_tot, 'vOutro', self._format_decimal(nota_fiscal.valor_outras_despesas, 2))
        self._add_element(icms_tot, 'vNF', self._format_decimal(nota_fiscal.valor_total, 2))
        self._add_element(icms_tot, 'vTotTrib', self._format_decimal(nota_fiscal.valor_aproximado_tributos, 2))

        # transp - Transporte
        transp = etree.SubElement(inf_nfe, 'transp')
        self._add_element(transp, 'modFrete', str(nota_fiscal.modalidade_frete))

        if nota_fiscal.transportadora_cnpj:
            transporta = etree.SubElement(transp, 'transporta')
            cnpj_transp = nota_fiscal.transportadora_cnpj.replace('.', '').replace('/', '').replace('-', '')
            if len(cnpj_transp) == 14:
                self._add_element(transporta, 'CNPJ', cnpj_transp)
            else:
                self._add_element(transporta, 'CPF', cnpj_transp)
            if nota_fiscal.transportadora_razao_social:
                self._add_element(transporta, 'xNome', nota_fiscal.transportadora_razao_social[:60])

        if nota_fiscal.veiculo_placa:
            veiculo = etree.SubElement(transp, 'veicTransp')
            self._add_element(veiculo, 'placa', nota_fiscal.veiculo_placa)
            self._add_element(veiculo, 'UF', nota_fiscal.veiculo_uf or self.uf)

        if nota_fiscal.quantidade_volumes and nota_fiscal.quantidade_volumes > 0:
            vol = etree.SubElement(transp, 'vol')
            self._add_element(vol, 'qVol', str(nota_fiscal.quantidade_volumes))
            if nota_fiscal.especie_volumes:
                self._add_element(vol, 'esp', nota_fiscal.especie_volumes[:60])
            if nota_fiscal.peso_liquido:
                self._add_element(vol, 'pesoL', self._format_decimal(nota_fiscal.peso_liquido, 3))
            if nota_fiscal.peso_bruto:
                self._add_element(vol, 'pesoB', self._format_decimal(nota_fiscal.peso_bruto, 3))

        # pag - Pagamento
        pag = etree.SubElement(inf_nfe, 'pag')
        det_pag = etree.SubElement(pag, 'detPag')

        # Forma de pagamento
        forma_pag = self._mapear_forma_pagamento(nota_fiscal.forma_pagamento)
        self._add_element(det_pag, 'tPag', forma_pag)
        self._add_element(det_pag, 'vPag', self._format_decimal(nota_fiscal.valor_pagamento or nota_fiscal.valor_total, 2))

        # infAdic - Informações Adicionais
        if nota_fiscal.informacoes_complementares or nota_fiscal.informacoes_fisco:
            inf_adic = etree.SubElement(inf_nfe, 'infAdic')

            if nota_fiscal.informacoes_fisco:
                self._add_element(inf_adic, 'infAdFisco', nota_fiscal.informacoes_fisco[:2000])

            if nota_fiscal.informacoes_complementares:
                self._add_element(inf_adic, 'infCpl', nota_fiscal.informacoes_complementares[:5000])

        # Responsável técnico (obrigatório NFe 4.00)
        if self.empresa.resp_tecnico_cnpj:
            inf_resp_tec = etree.SubElement(inf_nfe, 'infRespTec')
            self._add_element(inf_resp_tec, 'CNPJ', self.empresa.resp_tecnico_cnpj.replace('.', '').replace('/', '').replace('-', ''))
            self._add_element(inf_resp_tec, 'xContato', self.empresa.resp_tecnico_contato[:60])
            self._add_element(inf_resp_tec, 'email', self.empresa.resp_tecnico_email[:60])
            self._add_element(inf_resp_tec, 'fone', self._limpar_telefone(self.empresa.resp_tecnico_telefone))

        # Atualiza a nota com a chave gerada
        nota_fiscal.chave_acesso = chave_acesso

        return etree.tostring(nfe, encoding='unicode', pretty_print=False)

    def _gerar_icms(self, parent, item):
        """Gera o grupo de ICMS baseado no CST/CSOSN"""
        cst = item.cst_icms or '102'

        # Simples Nacional (CSOSN)
        if self.empresa.regime_tributario == 1:
            if cst in ['101']:
                icms_sn = etree.SubElement(parent, 'ICMSSN101')
                self._add_element(icms_sn, 'orig', item.origem or '0')
                self._add_element(icms_sn, 'CSOSN', cst)
                self._add_element(icms_sn, 'pCredSN', self._format_decimal(item.aliquota_icms or 0, 2))
                self._add_element(icms_sn, 'vCredICMSSN', self._format_decimal(item.valor_icms or 0, 2))
            elif cst in ['102', '103', '300', '400']:
                icms_sn = etree.SubElement(parent, 'ICMSSN102')
                self._add_element(icms_sn, 'orig', item.origem or '0')
                self._add_element(icms_sn, 'CSOSN', cst)
            elif cst == '500':
                icms_sn = etree.SubElement(parent, 'ICMSSN500')
                self._add_element(icms_sn, 'orig', item.origem or '0')
                self._add_element(icms_sn, 'CSOSN', cst)
            else:
                icms_sn = etree.SubElement(parent, 'ICMSSN102')
                self._add_element(icms_sn, 'orig', item.origem or '0')
                self._add_element(icms_sn, 'CSOSN', '102')
        else:
            # Regime Normal (CST)
            if cst == '00':
                icms00 = etree.SubElement(parent, 'ICMS00')
                self._add_element(icms00, 'orig', item.origem or '0')
                self._add_element(icms00, 'CST', cst)
                self._add_element(icms00, 'modBC', str(item.modalidade_bc_icms or 3))
                self._add_element(icms00, 'vBC', self._format_decimal(item.valor_bc_icms, 2))
                self._add_element(icms00, 'pICMS', self._format_decimal(item.aliquota_icms, 2))
                self._add_element(icms00, 'vICMS', self._format_decimal(item.valor_icms, 2))
            elif cst in ['40', '41', '50']:
                icms40 = etree.SubElement(parent, 'ICMS40')
                self._add_element(icms40, 'orig', item.origem or '0')
                self._add_element(icms40, 'CST', cst)
            elif cst == '60':
                icms60 = etree.SubElement(parent, 'ICMS60')
                self._add_element(icms60, 'orig', item.origem or '0')
                self._add_element(icms60, 'CST', cst)
            else:
                icms00 = etree.SubElement(parent, 'ICMS00')
                self._add_element(icms00, 'orig', item.origem or '0')
                self._add_element(icms00, 'CST', '00')
                self._add_element(icms00, 'modBC', '3')
                self._add_element(icms00, 'vBC', self._format_decimal(item.valor_bc_icms or 0, 2))
                self._add_element(icms00, 'pICMS', self._format_decimal(item.aliquota_icms or 0, 2))
                self._add_element(icms00, 'vICMS', self._format_decimal(item.valor_icms or 0, 2))

    def _gerar_ipi(self, parent, item):
        """Gera o grupo de IPI"""
        cst = item.cst_ipi or '99'

        self._add_element(parent, 'cEnq', '999')  # Código de enquadramento

        if cst in ['00', '49', '50', '99']:
            if item.valor_ipi and item.valor_ipi > 0:
                ipi_trib = etree.SubElement(parent, 'IPITrib')
                self._add_element(ipi_trib, 'CST', cst)
                self._add_element(ipi_trib, 'vBC', self._format_decimal(item.valor_bc_ipi, 2))
                self._add_element(ipi_trib, 'pIPI', self._format_decimal(item.aliquota_ipi, 2))
                self._add_element(ipi_trib, 'vIPI', self._format_decimal(item.valor_ipi, 2))
            else:
                ipi_nt = etree.SubElement(parent, 'IPINT')
                self._add_element(ipi_nt, 'CST', '53')  # Não tributado
        else:
            ipi_nt = etree.SubElement(parent, 'IPINT')
            self._add_element(ipi_nt, 'CST', cst)

    def _gerar_pis(self, parent, item):
        """Gera o grupo de PIS"""
        cst = item.cst_pis or '07'

        if cst in ['01', '02']:
            pis_aliq = etree.SubElement(parent, 'PISAliq')
            self._add_element(pis_aliq, 'CST', cst)
            self._add_element(pis_aliq, 'vBC', self._format_decimal(item.valor_bc_pis, 2))
            self._add_element(pis_aliq, 'pPIS', self._format_decimal(item.aliquota_pis, 2))
            self._add_element(pis_aliq, 'vPIS', self._format_decimal(item.valor_pis, 2))
        else:
            pis_nt = etree.SubElement(parent, 'PISNT')
            self._add_element(pis_nt, 'CST', cst)

    def _gerar_cofins(self, parent, item):
        """Gera o grupo de COFINS"""
        cst = item.cst_cofins or '07'

        if cst in ['01', '02']:
            cofins_aliq = etree.SubElement(parent, 'COFINSAliq')
            self._add_element(cofins_aliq, 'CST', cst)
            self._add_element(cofins_aliq, 'vBC', self._format_decimal(item.valor_bc_cofins, 2))
            self._add_element(cofins_aliq, 'pCOFINS', self._format_decimal(item.aliquota_cofins, 2))
            self._add_element(cofins_aliq, 'vCOFINS', self._format_decimal(item.valor_cofins, 2))
        else:
            cofins_nt = etree.SubElement(parent, 'COFINSNT')
            self._add_element(cofins_nt, 'CST', cst)

    def assinar_nfe(self, xml_nfe):
        """
        Assina o XML da NFe

        Args:
            xml_nfe: String do XML da NFe

        Returns:
            str: XML assinado
        """
        if not self.certificado_service:
            raise Exception("Certificado digital não configurado")

        # Extrai o ID para referência na assinatura
        root = etree.fromstring(xml_nfe.encode('utf-8'))
        inf_nfe = root.find('.//{http://www.portalfiscal.inf.br/nfe}infNFe')
        if inf_nfe is not None:
            reference_uri = f"#{inf_nfe.get('Id')}"
        else:
            reference_uri = ''

        return self.certificado_service.assinar_xml(xml_nfe, reference_uri)

    def transmitir_nfe(self, xml_assinado):
        """
        Transmite a NFe para a SEFAZ

        Args:
            xml_assinado: XML da NFe assinado

        Returns:
            dict: Resposta da SEFAZ
        """
        try:
            # Monta envelope SOAP
            ambiente = 'producao' if self.ambiente == 1 else 'homologacao'
            url = self._get_ws_url('autorizacao')

            envelope = self._criar_envelope_soap('NfeAutorizacao', xml_assinado)

            # Obtém certificado PEM
            cert_pem = self.certificado_service.obter_certificado_pem()
            key_pem = self.certificado_service.obter_chave_pem()

            # Salva certificados temporariamente
            import tempfile
            cert_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
            cert_file.write(cert_pem)
            cert_file.write(key_pem)
            cert_file.close()

            # Headers SOAP
            headers = {
                'Content-Type': 'application/soap+xml; charset=utf-8',
                'SOAPAction': 'http://www.portalfiscal.inf.br/nfe/wsdl/NFeAutorizacao4/nfeAutorizacaoLote'
            }

            # Faz requisição
            response = requests.post(
                url,
                data=envelope.encode('utf-8'),
                headers=headers,
                cert=cert_file.name,
                verify=True,
                timeout=60
            )

            # Remove arquivo temporário
            os.unlink(cert_file.name)

            # Parse da resposta
            return self._parse_resposta_sefaz(response.text)

        except Exception as e:
            logger.error(f"Erro ao transmitir NFe: {str(e)}")
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': str(e)
            }

    def consultar_nfe(self, chave_acesso):
        """
        Consulta situação de uma NFe na SEFAZ

        Args:
            chave_acesso: Chave de acesso da NFe (44 dígitos)

        Returns:
            dict: Situação da NFe
        """
        try:
            url = self._get_ws_url('consulta')

            # Monta XML de consulta
            NSMAP = {None: self.NS_NFE}
            cons_sit = etree.Element('consSitNFe', versao=self.VERSAO_NFE, nsmap=NSMAP)
            self._add_element(cons_sit, 'tpAmb', str(self.ambiente))
            self._add_element(cons_sit, 'xServ', 'CONSULTAR')
            self._add_element(cons_sit, 'chNFe', chave_acesso)

            xml_consulta = etree.tostring(cons_sit, encoding='unicode')
            envelope = self._criar_envelope_soap('NfeConsulta', xml_consulta)

            # Obtém certificado
            cert_pem = self.certificado_service.obter_certificado_pem()
            key_pem = self.certificado_service.obter_chave_pem()

            import tempfile
            cert_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
            cert_file.write(cert_pem)
            cert_file.write(key_pem)
            cert_file.close()

            headers = {
                'Content-Type': 'application/soap+xml; charset=utf-8',
                'SOAPAction': 'http://www.portalfiscal.inf.br/nfe/wsdl/NFeConsultaProtocolo4/nfeConsultaNF'
            }

            response = requests.post(
                url,
                data=envelope.encode('utf-8'),
                headers=headers,
                cert=cert_file.name,
                verify=True,
                timeout=30
            )

            os.unlink(cert_file.name)

            return self._parse_resposta_consulta(response.text)

        except Exception as e:
            logger.error(f"Erro ao consultar NFe: {str(e)}")
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': str(e)
            }

    def cancelar_nfe(self, chave_acesso, protocolo, justificativa):
        """
        Cancela uma NFe autorizada

        Args:
            chave_acesso: Chave de acesso da NFe
            protocolo: Protocolo de autorização
            justificativa: Motivo do cancelamento (15-255 chars)

        Returns:
            dict: Resultado do cancelamento
        """
        if len(justificativa) < 15:
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': 'Justificativa deve ter pelo menos 15 caracteres'
            }

        try:
            return self._enviar_evento(
                chave_acesso,
                '110111',  # Código de cancelamento
                1,  # Sequência do evento
                justificativa,
                protocolo
            )
        except Exception as e:
            logger.error(f"Erro ao cancelar NFe: {str(e)}")
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': str(e)
            }

    def carta_correcao(self, chave_acesso, sequencia, correcao):
        """
        Envia Carta de Correção Eletrônica

        Args:
            chave_acesso: Chave de acesso da NFe
            sequencia: Número sequencial do evento (1-20)
            correcao: Texto da correção (15-1000 chars)

        Returns:
            dict: Resultado do evento
        """
        if len(correcao) < 15 or len(correcao) > 1000:
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': 'Correção deve ter entre 15 e 1000 caracteres'
            }

        try:
            return self._enviar_evento(
                chave_acesso,
                '110110',  # Código de CC-e
                sequencia,
                correcao
            )
        except Exception as e:
            logger.error(f"Erro ao enviar CC-e: {str(e)}")
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': str(e)
            }

    def inutilizar_numeracao(self, ano, serie, numero_inicial, numero_final, justificativa):
        """
        Inutiliza uma faixa de numeração de NFe

        Args:
            ano: Ano (2 dígitos)
            serie: Série da NFe
            numero_inicial: Número inicial
            numero_final: Número final
            justificativa: Motivo (15-255 chars)

        Returns:
            dict: Resultado da inutilização
        """
        try:
            url = self._get_ws_url('inutilizacao')

            # Monta ID da inutilização
            cnpj = self.empresa.cnpj.replace('.', '').replace('/', '').replace('-', '')
            id_inut = f"ID{self.CODIGO_UF[self.uf]}{'55'}{str(ano).zfill(2)}{cnpj}{str(serie).zfill(3)}{str(numero_inicial).zfill(9)}{str(numero_final).zfill(9)}"

            NSMAP = {None: self.NS_NFE}
            inut_nfe = etree.Element('inutNFe', versao=self.VERSAO_NFE, nsmap=NSMAP)
            inf_inut = etree.SubElement(inut_nfe, 'infInut', Id=id_inut)

            self._add_element(inf_inut, 'tpAmb', str(self.ambiente))
            self._add_element(inf_inut, 'xServ', 'INUTILIZAR')
            self._add_element(inf_inut, 'cUF', self.CODIGO_UF[self.uf])
            self._add_element(inf_inut, 'ano', str(ano).zfill(2))
            self._add_element(inf_inut, 'CNPJ', cnpj)
            self._add_element(inf_inut, 'mod', '55')
            self._add_element(inf_inut, 'serie', str(serie))
            self._add_element(inf_inut, 'nNFIni', str(numero_inicial))
            self._add_element(inf_inut, 'nNFFin', str(numero_final))
            self._add_element(inf_inut, 'xJust', justificativa[:255])

            xml_inut = etree.tostring(inut_nfe, encoding='unicode')

            # Assina
            xml_assinado = self.certificado_service.assinar_xml(xml_inut, f'#{id_inut}')

            envelope = self._criar_envelope_soap('NfeInutilizacao', xml_assinado)

            cert_pem = self.certificado_service.obter_certificado_pem()
            key_pem = self.certificado_service.obter_chave_pem()

            import tempfile
            cert_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
            cert_file.write(cert_pem)
            cert_file.write(key_pem)
            cert_file.close()

            headers = {
                'Content-Type': 'application/soap+xml; charset=utf-8',
                'SOAPAction': 'http://www.portalfiscal.inf.br/nfe/wsdl/NFeInutilizacao4/nfeInutilizacaoNF'
            }

            response = requests.post(
                url,
                data=envelope.encode('utf-8'),
                headers=headers,
                cert=cert_file.name,
                verify=True,
                timeout=30
            )

            os.unlink(cert_file.name)

            return self._parse_resposta_inutilizacao(response.text)

        except Exception as e:
            logger.error(f"Erro ao inutilizar numeração: {str(e)}")
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': str(e)
            }

    def consultar_status_servico(self):
        """
        Consulta status do serviço SEFAZ

        Returns:
            dict: Status do serviço
        """
        try:
            url = self._get_ws_url('status')

            NSMAP = {None: self.NS_NFE}
            cons_stat = etree.Element('consStatServ', versao=self.VERSAO_NFE, nsmap=NSMAP)
            self._add_element(cons_stat, 'tpAmb', str(self.ambiente))
            self._add_element(cons_stat, 'cUF', self.CODIGO_UF[self.uf])
            self._add_element(cons_stat, 'xServ', 'STATUS')

            xml_status = etree.tostring(cons_stat, encoding='unicode')
            envelope = self._criar_envelope_soap('NfeStatusServico', xml_status)

            cert_pem = self.certificado_service.obter_certificado_pem()
            key_pem = self.certificado_service.obter_chave_pem()

            import tempfile
            cert_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
            cert_file.write(cert_pem)
            cert_file.write(key_pem)
            cert_file.close()

            headers = {
                'Content-Type': 'application/soap+xml; charset=utf-8',
                'SOAPAction': 'http://www.portalfiscal.inf.br/nfe/wsdl/NFeStatusServico4/nfeStatusServicoNF'
            }

            response = requests.post(
                url,
                data=envelope.encode('utf-8'),
                headers=headers,
                cert=cert_file.name,
                verify=True,
                timeout=30
            )

            os.unlink(cert_file.name)

            root = etree.fromstring(response.text.encode('utf-8'))
            ret = root.find('.//{http://www.portalfiscal.inf.br/nfe}retConsStatServ')

            if ret is not None:
                c_stat = ret.findtext('{http://www.portalfiscal.inf.br/nfe}cStat')
                x_motivo = ret.findtext('{http://www.portalfiscal.inf.br/nfe}xMotivo')

                return {
                    'sucesso': c_stat == '107',
                    'codigo': c_stat,
                    'mensagem': x_motivo,
                    'online': c_stat == '107'
                }

            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': 'Resposta inválida',
                'online': False
            }

        except Exception as e:
            logger.error(f"Erro ao consultar status: {str(e)}")
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': str(e),
                'online': False
            }

    def _enviar_evento(self, chave_acesso, tipo_evento, sequencia, descricao, protocolo=None):
        """Envia evento para SEFAZ (cancelamento, CC-e, etc)"""
        try:
            url = self._get_ws_url('evento')

            cnpj = self.empresa.cnpj.replace('.', '').replace('/', '').replace('-', '')
            dh_evento = datetime.now().strftime('%Y-%m-%dT%H:%M:%S-03:00')

            # ID do evento
            id_evento = f"ID{tipo_evento}{chave_acesso}{str(sequencia).zfill(2)}"

            NSMAP = {None: self.NS_NFE}
            evento = etree.Element('envEvento', versao='1.00', nsmap=NSMAP)
            self._add_element(evento, 'idLote', str(random.randint(1, 999999999999999)))

            event = etree.SubElement(evento, 'evento', versao='1.00')
            inf_evento = etree.SubElement(event, 'infEvento', Id=id_evento)

            self._add_element(inf_evento, 'cOrgao', self.CODIGO_UF[self.uf])
            self._add_element(inf_evento, 'tpAmb', str(self.ambiente))
            self._add_element(inf_evento, 'CNPJ', cnpj)
            self._add_element(inf_evento, 'chNFe', chave_acesso)
            self._add_element(inf_evento, 'dhEvento', dh_evento)
            self._add_element(inf_evento, 'tpEvento', tipo_evento)
            self._add_element(inf_evento, 'nSeqEvento', str(sequencia))
            self._add_element(inf_evento, 'verEvento', '1.00')

            det_evento = etree.SubElement(inf_evento, 'detEvento', versao='1.00')

            if tipo_evento == '110111':  # Cancelamento
                self._add_element(det_evento, 'descEvento', 'Cancelamento')
                self._add_element(det_evento, 'nProt', protocolo)
                self._add_element(det_evento, 'xJust', descricao)
            elif tipo_evento == '110110':  # CC-e
                self._add_element(det_evento, 'descEvento', 'Carta de Correcao')
                self._add_element(det_evento, 'xCorrecao', descricao)
                self._add_element(det_evento, 'xCondUso',
                    'A Carta de Correcao e disciplinada pelo paragrafo 1o-A do art. 7o do Convenio S/N, '
                    'de 15 de dezembro de 1970 e pode ser utilizada para regularizacao de erro ocorrido na '
                    'emissao de documento fiscal, desde que o erro nao esteja relacionado com: I - as variaveis '
                    'que determinam o valor do imposto tais como: base de calculo, aliquota, diferenca de preco, '
                    'quantidade, valor da operacao ou da prestacao; II - a correcao de dados cadastrais que '
                    'implique mudanca do remetente ou do destinatario; III - a data de emissao ou de saida.')

            xml_evento = etree.tostring(evento, encoding='unicode')

            # Assina
            xml_assinado = self.certificado_service.assinar_xml(xml_evento, f'#{id_evento}')

            envelope = self._criar_envelope_soap('RecepcaoEvento', xml_assinado)

            cert_pem = self.certificado_service.obter_certificado_pem()
            key_pem = self.certificado_service.obter_chave_pem()

            import tempfile
            cert_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
            cert_file.write(cert_pem)
            cert_file.write(key_pem)
            cert_file.close()

            headers = {
                'Content-Type': 'application/soap+xml; charset=utf-8',
                'SOAPAction': 'http://www.portalfiscal.inf.br/nfe/wsdl/NFeRecepcaoEvento4/nfeRecepcaoEvento'
            }

            response = requests.post(
                url,
                data=envelope.encode('utf-8'),
                headers=headers,
                cert=cert_file.name,
                verify=True,
                timeout=30
            )

            os.unlink(cert_file.name)

            return self._parse_resposta_evento(response.text)

        except Exception as e:
            logger.error(f"Erro ao enviar evento: {str(e)}")
            raise

    def _get_ws_url(self, servico):
        """Obtém URL do WebService para o serviço especificado"""
        ambiente = 'producao' if self.ambiente == 1 else 'homologacao'
        uf = self.uf

        # Determina qual SEFAZ usar
        if uf in self.WS_URLS:
            return self.WS_URLS[uf][ambiente][servico]
        else:
            # Usa SEFAZ Virtual RS para estados não listados
            return self.WS_URLS['SVRS'][ambiente][servico]

    def _criar_envelope_soap(self, metodo, xml_dados):
        """Cria envelope SOAP para envio"""
        envelope = f'''<?xml version="1.0" encoding="UTF-8"?>
<soap12:Envelope xmlns:soap12="{self.NS_SOAP}">
    <soap12:Body>
        <nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/{metodo}4">
            {xml_dados}
        </nfeDadosMsg>
    </soap12:Body>
</soap12:Envelope>'''
        return envelope

    def _parse_resposta_sefaz(self, xml_resposta):
        """Parse da resposta de autorização"""
        try:
            root = etree.fromstring(xml_resposta.encode('utf-8'))
            ret = root.find('.//{http://www.portalfiscal.inf.br/nfe}retEnviNFe')

            if ret is None:
                ret = root.find('.//{http://www.portalfiscal.inf.br/nfe}retConsReciNFe')

            if ret is not None:
                c_stat = ret.findtext('.//{http://www.portalfiscal.inf.br/nfe}cStat')
                x_motivo = ret.findtext('.//{http://www.portalfiscal.inf.br/nfe}xMotivo')

                prot = ret.find('.//{http://www.portalfiscal.inf.br/nfe}protNFe')
                protocolo = None
                dh_recbto = None

                if prot is not None:
                    inf_prot = prot.find('.//{http://www.portalfiscal.inf.br/nfe}infProt')
                    if inf_prot is not None:
                        c_stat = inf_prot.findtext('{http://www.portalfiscal.inf.br/nfe}cStat')
                        x_motivo = inf_prot.findtext('{http://www.portalfiscal.inf.br/nfe}xMotivo')
                        protocolo = inf_prot.findtext('{http://www.portalfiscal.inf.br/nfe}nProt')
                        dh_recbto = inf_prot.findtext('{http://www.portalfiscal.inf.br/nfe}dhRecbto')

                return {
                    'sucesso': c_stat == '100',
                    'codigo': c_stat,
                    'mensagem': x_motivo,
                    'protocolo': protocolo,
                    'data_autorizacao': dh_recbto,
                    'xml_retorno': xml_resposta
                }

            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': 'Resposta inválida da SEFAZ',
                'xml_retorno': xml_resposta
            }

        except Exception as e:
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': str(e),
                'xml_retorno': xml_resposta
            }

    def _parse_resposta_consulta(self, xml_resposta):
        """Parse da resposta de consulta"""
        try:
            root = etree.fromstring(xml_resposta.encode('utf-8'))
            ret = root.find('.//{http://www.portalfiscal.inf.br/nfe}retConsSitNFe')

            if ret is not None:
                c_stat = ret.findtext('{http://www.portalfiscal.inf.br/nfe}cStat')
                x_motivo = ret.findtext('{http://www.portalfiscal.inf.br/nfe}xMotivo')

                return {
                    'sucesso': c_stat in ['100', '150'],
                    'codigo': c_stat,
                    'mensagem': x_motivo,
                    'autorizada': c_stat == '100',
                    'cancelada': c_stat == '101',
                    'denegada': c_stat in ['110', '205', '301', '302']
                }

            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': 'Resposta inválida'
            }

        except Exception as e:
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': str(e)
            }

    def _parse_resposta_evento(self, xml_resposta):
        """Parse da resposta de evento"""
        try:
            root = etree.fromstring(xml_resposta.encode('utf-8'))
            ret = root.find('.//{http://www.portalfiscal.inf.br/nfe}retEvento')

            if ret is not None:
                inf_evento = ret.find('.//{http://www.portalfiscal.inf.br/nfe}infEvento')
                if inf_evento is not None:
                    c_stat = inf_evento.findtext('{http://www.portalfiscal.inf.br/nfe}cStat')
                    x_motivo = inf_evento.findtext('{http://www.portalfiscal.inf.br/nfe}xMotivo')
                    n_prot = inf_evento.findtext('{http://www.portalfiscal.inf.br/nfe}nProt')

                    return {
                        'sucesso': c_stat in ['135', '136'],
                        'codigo': c_stat,
                        'mensagem': x_motivo,
                        'protocolo': n_prot,
                        'xml_retorno': xml_resposta
                    }

            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': 'Resposta inválida',
                'xml_retorno': xml_resposta
            }

        except Exception as e:
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': str(e)
            }

    def _parse_resposta_inutilizacao(self, xml_resposta):
        """Parse da resposta de inutilização"""
        try:
            root = etree.fromstring(xml_resposta.encode('utf-8'))
            ret = root.find('.//{http://www.portalfiscal.inf.br/nfe}retInutNFe')

            if ret is not None:
                inf_inut = ret.find('.//{http://www.portalfiscal.inf.br/nfe}infInut')
                if inf_inut is not None:
                    c_stat = inf_inut.findtext('{http://www.portalfiscal.inf.br/nfe}cStat')
                    x_motivo = inf_inut.findtext('{http://www.portalfiscal.inf.br/nfe}xMotivo')
                    n_prot = inf_inut.findtext('{http://www.portalfiscal.inf.br/nfe}nProt')

                    return {
                        'sucesso': c_stat == '102',
                        'codigo': c_stat,
                        'mensagem': x_motivo,
                        'protocolo': n_prot,
                        'xml_retorno': xml_resposta
                    }

            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': 'Resposta inválida',
                'xml_retorno': xml_resposta
            }

        except Exception as e:
            return {
                'sucesso': False,
                'codigo': '999',
                'mensagem': str(e)
            }

    def _gerar_chave_acesso(self, cuf, aamm, cnpj, mod, serie, nnf, tpemis, cnf):
        """Gera chave de acesso de 44 dígitos"""
        chave = f"{cuf}{aamm}{cnpj}{str(mod).zfill(2)}{str(serie).zfill(3)}"
        chave += f"{str(nnf).zfill(9)}{tpemis}{str(cnf).zfill(8)}"

        # Calcula dígito verificador (módulo 11)
        pesos = [2, 3, 4, 5, 6, 7, 8, 9]
        soma = 0
        for i, digito in enumerate(reversed(chave)):
            soma += int(digito) * pesos[i % 8]

        resto = soma % 11
        dv = 0 if resto < 2 else 11 - resto

        return chave + str(dv)

    def _add_element(self, parent, tag, text):
        """Adiciona elemento com texto"""
        element = etree.SubElement(parent, tag)
        element.text = str(text) if text is not None else ''
        return element

    def _format_decimal(self, value, decimals=2):
        """Formata decimal para XML"""
        if value is None:
            value = 0
        return f"{float(value):.{decimals}f}"

    def _limpar_telefone(self, telefone):
        """Remove caracteres não numéricos do telefone"""
        if not telefone:
            return ''
        return ''.join(filter(str.isdigit, telefone))

    def _mapear_forma_pagamento(self, forma):
        """Mapeia forma de pagamento para código NFe"""
        mapeamento = {
            'dinheiro': '01',
            'cheque': '02',
            'cartao_credito': '03',
            'cartao_debito': '04',
            'credito_loja': '05',
            'vale_alimentacao': '10',
            'vale_refeicao': '11',
            'vale_presente': '12',
            'vale_combustivel': '13',
            'boleto': '15',
            'deposito_bancario': '16',
            'pix': '17',
            'transferencia': '18',
            'sem_pagamento': '90',
            'outros': '99'
        }
        return mapeamento.get(forma, '99')
