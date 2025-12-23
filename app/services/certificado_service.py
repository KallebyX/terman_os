# -*- coding: utf-8 -*-
"""
Serviço de Certificado Digital
Suporta certificados A1 (arquivo .pfx) e A3 (token USB/SmartCard)
"""

import os
import base64
import tempfile
from datetime import datetime, date
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from lxml import etree
import logging

logger = logging.getLogger(__name__)


class CertificadoService:
    """Serviço para manipulação de certificados digitais A1 e A3"""

    def __init__(self, certificado=None):
        """
        Inicializa o serviço de certificado

        Args:
            certificado: Objeto CertificadoDigital do banco de dados
        """
        self.certificado = certificado
        self._private_key = None
        self._certificate = None
        self._cert_pem = None
        self._key_pem = None

    def carregar_certificado_a1(self, pfx_data, senha):
        """
        Carrega um certificado A1 (arquivo .pfx)

        Args:
            pfx_data: Conteúdo binário do arquivo .pfx
            senha: Senha do certificado

        Returns:
            dict: Informações do certificado
        """
        try:
            # Decodifica o certificado PKCS12
            private_key, certificate, additional_certs = pkcs12.load_key_and_certificates(
                pfx_data,
                senha.encode() if isinstance(senha, str) else senha,
                default_backend()
            )

            self._private_key = private_key
            self._certificate = certificate

            # Extrai informações do certificado
            subject = certificate.subject
            issuer = certificate.issuer

            # Extrai CNPJ/CPF do subject
            cn = None
            for attribute in subject:
                if attribute.oid == x509.oid.NameOID.COMMON_NAME:
                    cn = attribute.value
                    break

            # Extrai CNPJ do CN (formato padrão: "NOME:CNPJ")
            cnpj = None
            if cn and ':' in cn:
                parts = cn.split(':')
                if len(parts) >= 2:
                    cnpj = parts[-1].strip()

            # Converte para PEM
            self._cert_pem = certificate.public_bytes(serialization.Encoding.PEM)
            self._key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )

            return {
                'sucesso': True,
                'nome': cn,
                'cnpj': cnpj,
                'serial_number': str(certificate.serial_number),
                'thumbprint': certificate.fingerprint(hashes.SHA1()).hex().upper(),
                'data_emissao': certificate.not_valid_before_utc.date() if hasattr(certificate, 'not_valid_before_utc') else certificate.not_valid_before.date(),
                'data_validade': certificate.not_valid_after_utc.date() if hasattr(certificate, 'not_valid_after_utc') else certificate.not_valid_after.date(),
                'emissor': self._get_issuer_name(issuer)
            }

        except Exception as e:
            logger.error(f"Erro ao carregar certificado A1: {str(e)}")
            return {
                'sucesso': False,
                'erro': str(e)
            }

    def carregar_certificado_a3(self, slot=0, pin=None, biblioteca=None):
        """
        Carrega um certificado A3 de token USB/SmartCard

        Args:
            slot: Slot do token (geralmente 0)
            pin: PIN do token
            biblioteca: Caminho para a biblioteca PKCS11 (.dll/.so)

        Returns:
            dict: Informações do certificado
        """
        try:
            # Importa PyKCS11 apenas quando necessário (A3)
            import PyKCS11

            # Detecta biblioteca automaticamente se não fornecida
            if not biblioteca:
                biblioteca = self._detectar_biblioteca_pkcs11()

            if not biblioteca or not os.path.exists(biblioteca):
                return {
                    'sucesso': False,
                    'erro': 'Biblioteca PKCS11 não encontrada. Instale o driver do token.'
                }

            # Inicializa PKCS11
            pkcs11 = PyKCS11.PyKCS11Lib()
            pkcs11.load(biblioteca)

            # Lista slots disponíveis
            slots = pkcs11.getSlotList(tokenPresent=True)
            if not slots:
                return {
                    'sucesso': False,
                    'erro': 'Nenhum token encontrado. Conecte o token USB.'
                }

            if slot >= len(slots):
                slot = 0

            # Abre sessão
            session = pkcs11.openSession(slots[slot])

            # Login com PIN
            if pin:
                session.login(pin)

            # Busca certificados
            certs = session.findObjects([
                (PyKCS11.CKA_CLASS, PyKCS11.CKO_CERTIFICATE)
            ])

            if not certs:
                session.logout()
                session.closeSession()
                return {
                    'sucesso': False,
                    'erro': 'Nenhum certificado encontrado no token.'
                }

            # Obtém o primeiro certificado
            cert_obj = certs[0]
            cert_der = bytes(session.getAttributeValue(cert_obj, [PyKCS11.CKA_VALUE])[0])

            # Parse do certificado
            certificate = x509.load_der_x509_certificate(cert_der, default_backend())

            # Extrai informações
            subject = certificate.subject
            cn = None
            for attribute in subject:
                if attribute.oid == x509.oid.NameOID.COMMON_NAME:
                    cn = attribute.value
                    break

            cnpj = None
            if cn and ':' in cn:
                parts = cn.split(':')
                if len(parts) >= 2:
                    cnpj = parts[-1].strip()

            # Armazena referências
            self._pkcs11_session = session
            self._pkcs11_lib = pkcs11
            self._certificate = certificate
            self._cert_pem = certificate.public_bytes(serialization.Encoding.PEM)

            return {
                'sucesso': True,
                'nome': cn,
                'cnpj': cnpj,
                'serial_number': str(certificate.serial_number),
                'thumbprint': certificate.fingerprint(hashes.SHA1()).hex().upper(),
                'data_emissao': certificate.not_valid_before_utc.date() if hasattr(certificate, 'not_valid_before_utc') else certificate.not_valid_before.date(),
                'data_validade': certificate.not_valid_after_utc.date() if hasattr(certificate, 'not_valid_after_utc') else certificate.not_valid_after.date(),
                'tipo': 'A3',
                'slot': slot
            }

        except ImportError:
            return {
                'sucesso': False,
                'erro': 'Biblioteca PyKCS11 não instalada. Execute: pip install PyKCS11'
            }
        except Exception as e:
            logger.error(f"Erro ao carregar certificado A3: {str(e)}")
            return {
                'sucesso': False,
                'erro': str(e)
            }

    def _detectar_biblioteca_pkcs11(self):
        """Detecta automaticamente a biblioteca PKCS11 do sistema"""
        bibliotecas_windows = [
            # Safenet/Thales
            r'C:\Windows\System32\eTPKCS11.dll',
            r'C:\Windows\System32\aetpkss1.dll',
            # Certisign
            r'C:\Windows\System32\acPKCS11.dll',
            # Valid
            r'C:\Program Files\Safenet\LunaClient\cryptoki.dll',
            # OpenSC
            r'C:\Program Files\OpenSC Project\OpenSC\pkcs11\opensc-pkcs11.dll',
        ]

        bibliotecas_linux = [
            # OpenSC
            '/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so',
            '/usr/lib/opensc-pkcs11.so',
            '/usr/local/lib/opensc-pkcs11.so',
            # Safenet
            '/usr/lib/libeTPkcs11.so',
            '/usr/lib/libeToken.so',
            # Certisign
            '/usr/lib/libacpkcs.so',
        ]

        bibliotecas_mac = [
            '/Library/OpenSC/lib/opensc-pkcs11.so',
            '/usr/local/lib/opensc-pkcs11.so',
        ]

        import platform
        sistema = platform.system()

        if sistema == 'Windows':
            bibliotecas = bibliotecas_windows
        elif sistema == 'Darwin':
            bibliotecas = bibliotecas_mac
        else:
            bibliotecas = bibliotecas_linux

        for lib in bibliotecas:
            if os.path.exists(lib):
                return lib

        return None

    def _get_issuer_name(self, issuer):
        """Extrai nome do emissor do certificado"""
        for attribute in issuer:
            if attribute.oid == x509.oid.NameOID.ORGANIZATION_NAME:
                return attribute.value
        return "Desconhecido"

    def assinar_xml(self, xml_string, reference_uri=''):
        """
        Assina um documento XML com o certificado carregado

        Args:
            xml_string: String do XML a ser assinado
            reference_uri: URI de referência para assinatura (ex: "#NFe...")

        Returns:
            str: XML assinado
        """
        try:
            from signxml import XMLSigner, methods

            # Parse do XML
            root = etree.fromstring(xml_string.encode('utf-8'))

            # Configura o assinador
            signer = XMLSigner(
                method=methods.enveloped,
                signature_algorithm='rsa-sha1',
                digest_algorithm='sha1',
                c14n_algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'
            )

            # Para A1, usa chave e certificado carregados
            if self._key_pem and self._cert_pem:
                signed_root = signer.sign(
                    root,
                    key=self._key_pem,
                    cert=self._cert_pem,
                    reference_uri=reference_uri
                )
            else:
                raise Exception("Certificado não carregado")

            return etree.tostring(signed_root, encoding='unicode', pretty_print=False)

        except ImportError:
            logger.error("Biblioteca signxml não instalada")
            raise Exception("Biblioteca signxml não instalada. Execute: pip install signxml")
        except Exception as e:
            logger.error(f"Erro ao assinar XML: {str(e)}")
            raise

    def assinar_xml_a3(self, xml_string, reference_uri=''):
        """
        Assina XML usando certificado A3 (token USB)

        Args:
            xml_string: String do XML a ser assinado
            reference_uri: URI de referência

        Returns:
            str: XML assinado
        """
        try:
            import PyKCS11
            from lxml import etree
            import hashlib
            import base64

            # Parse do XML
            root = etree.fromstring(xml_string.encode('utf-8'))

            # Namespace da assinatura
            NSMAP = {
                'ds': 'http://www.w3.org/2000/09/xmldsig#'
            }

            # Busca chave privada no token
            private_keys = self._pkcs11_session.findObjects([
                (PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY)
            ])

            if not private_keys:
                raise Exception("Chave privada não encontrada no token")

            # Prepara canonicalização e hash
            c14n = etree.tostring(root, method='c14n')
            digest = hashlib.sha1(c14n).digest()
            digest_b64 = base64.b64encode(digest).decode()

            # Cria estrutura SignedInfo
            signed_info = self._criar_signed_info(reference_uri, digest_b64)
            signed_info_c14n = etree.tostring(signed_info, method='c14n')

            # Assina com o token
            mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA1_RSA_PKCS, None)
            signature = bytes(self._pkcs11_session.sign(
                private_keys[0],
                signed_info_c14n,
                mechanism
            ))
            signature_b64 = base64.b64encode(signature).decode()

            # Monta assinatura completa
            signature_element = self._criar_elemento_assinatura(
                signed_info, signature_b64, self._cert_pem
            )

            # Insere assinatura no XML
            root.append(signature_element)

            return etree.tostring(root, encoding='unicode')

        except Exception as e:
            logger.error(f"Erro ao assinar XML com A3: {str(e)}")
            raise

    def _criar_signed_info(self, reference_uri, digest_value):
        """Cria elemento SignedInfo para assinatura"""
        NSMAP = {'ds': 'http://www.w3.org/2000/09/xmldsig#'}

        signed_info = etree.Element('{http://www.w3.org/2000/09/xmldsig#}SignedInfo', nsmap=NSMAP)

        # CanonicalizationMethod
        c14n = etree.SubElement(signed_info, '{http://www.w3.org/2000/09/xmldsig#}CanonicalizationMethod')
        c14n.set('Algorithm', 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315')

        # SignatureMethod
        sig_method = etree.SubElement(signed_info, '{http://www.w3.org/2000/09/xmldsig#}SignatureMethod')
        sig_method.set('Algorithm', 'http://www.w3.org/2000/09/xmldsig#rsa-sha1')

        # Reference
        reference = etree.SubElement(signed_info, '{http://www.w3.org/2000/09/xmldsig#}Reference')
        reference.set('URI', reference_uri)

        # Transforms
        transforms = etree.SubElement(reference, '{http://www.w3.org/2000/09/xmldsig#}Transforms')

        transform1 = etree.SubElement(transforms, '{http://www.w3.org/2000/09/xmldsig#}Transform')
        transform1.set('Algorithm', 'http://www.w3.org/2000/09/xmldsig#enveloped-signature')

        transform2 = etree.SubElement(transforms, '{http://www.w3.org/2000/09/xmldsig#}Transform')
        transform2.set('Algorithm', 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315')

        # DigestMethod
        digest_method = etree.SubElement(reference, '{http://www.w3.org/2000/09/xmldsig#}DigestMethod')
        digest_method.set('Algorithm', 'http://www.w3.org/2000/09/xmldsig#sha1')

        # DigestValue
        digest_value_el = etree.SubElement(reference, '{http://www.w3.org/2000/09/xmldsig#}DigestValue')
        digest_value_el.text = digest_value

        return signed_info

    def validar_certificado(self):
        """
        Valida se o certificado está válido

        Returns:
            dict: Status da validação
        """
        if not self._certificate:
            return {
                'valido': False,
                'erro': 'Certificado não carregado'
            }

        try:
            not_before = self._certificate.not_valid_before_utc if hasattr(self._certificate, 'not_valid_before_utc') else self._certificate.not_valid_before
            not_after = self._certificate.not_valid_after_utc if hasattr(self._certificate, 'not_valid_after_utc') else self._certificate.not_valid_after
            now = datetime.utcnow()

            if now < not_before:
                return {
                    'valido': False,
                    'erro': 'Certificado ainda não é válido'
                }

            if now > not_after:
                return {
                    'valido': False,
                    'erro': 'Certificado expirado'
                }

            dias_restantes = (not_after - now).days

            return {
                'valido': True,
                'dias_restantes': dias_restantes,
                'alerta': dias_restantes <= 30,
                'mensagem': f'Certificado válido por mais {dias_restantes} dias'
            }

        except Exception as e:
            return {
                'valido': False,
                'erro': str(e)
            }

    def obter_certificado_pem(self):
        """Retorna o certificado em formato PEM"""
        return self._cert_pem

    def obter_chave_pem(self):
        """Retorna a chave privada em formato PEM (apenas A1)"""
        return self._key_pem

    def listar_tokens_conectados(self):
        """Lista todos os tokens USB/SmartCards conectados"""
        try:
            import PyKCS11

            biblioteca = self._detectar_biblioteca_pkcs11()
            if not biblioteca:
                return []

            pkcs11 = PyKCS11.PyKCS11Lib()
            pkcs11.load(biblioteca)

            tokens = []
            slots = pkcs11.getSlotList(tokenPresent=True)

            for i, slot in enumerate(slots):
                info = pkcs11.getTokenInfo(slot)
                tokens.append({
                    'slot': i,
                    'label': info.label.strip() if info.label else 'Token',
                    'manufacturer': info.manufacturerID.strip() if info.manufacturerID else '',
                    'model': info.model.strip() if info.model else '',
                    'serial': info.serialNumber.strip() if info.serialNumber else ''
                })

            return tokens

        except ImportError:
            return []
        except Exception as e:
            logger.error(f"Erro ao listar tokens: {str(e)}")
            return []

    def fechar_sessao(self):
        """Fecha sessão PKCS11 (para A3)"""
        try:
            if hasattr(self, '_pkcs11_session'):
                self._pkcs11_session.logout()
                self._pkcs11_session.closeSession()
        except:
            pass
