# Sistema Fiscal PDV - Documentacao Tecnica

## Visao Geral

O sistema fiscal PDV e um modulo completo de emissao de documentos fiscais eletronicos (NF-e e NFC-e) com integracao total a SEFAZ, seguindo os padroes governamentais brasileiros.

## Arquitetura

```
app/
├── routes/
│   └── fiscal.py          # Blueprint principal (1500+ linhas)
├── models/
│   └── fiscal.py          # Models fiscais (ConfiguracaoEmpresa, NotaFiscal, etc)
├── services/
│   ├── nfe_service.py     # Servico de geracao/transmissao NFe
│   ├── certificado_service.py  # Gerenciamento de certificados ICP-Brasil
│   └── pdf_service.py     # Geracao de DANFE
├── templates/fiscal/
│   ├── dashboard.html     # Dashboard principal
│   ├── empresa/
│   │   └── form.html      # Configuracao da empresa emissora
│   ├── pdv/
│   │   └── terminal.html  # Interface do PDV
│   ├── certificados/
│   │   ├── lista.html     # Listagem de certificados
│   │   └── form.html      # Upload de certificado
│   ├── contabilistas/
│   │   ├── lista.html     # Listagem de contadores
│   │   └── form.html      # Cadastro de contador
│   ├── notas/
│   │   ├── lista.html     # Listagem de notas fiscais
│   │   └── detalhe.html   # Detalhe da nota fiscal
│   ├── relatorios/
│   │   └── lista.html     # Relatorios fiscais
│   ├── inutilizacao/
│   │   └── lista.html     # Inutilizacao de numeracao
│   └── impostos/
│       └── configurar.html # Configuracao de impostos
```

## Models Principais

### ConfiguracaoEmpresa
Armazena dados do emissor:
- CNPJ, Razao Social, Nome Fantasia
- Inscricao Estadual, Municipal, SUFRAMA
- Regime Tributario (Simples Nacional, Lucro Presumido/Real)
- Endereco completo com codigo IBGE
- Configuracoes NFe (serie, CSC, ambiente)
- Dados do Responsavel Tecnico

### CertificadoDigital
Certificados ICP-Brasil:
- Tipo A1 (arquivo .pfx) ou A3 (token/smartcard)
- Data de validade e validacao automatica
- Armazenamento seguro da chave privada

### NotaFiscal
Documento fiscal eletronico:
- Modelo 55 (NFe) ou 65 (NFCe)
- Dados do emitente e destinatario
- Status (rascunho, assinada, autorizada, rejeitada, cancelada)
- XML original, assinado e de autorizacao
- Protocolo SEFAZ

### ItemNotaFiscal
Itens da nota:
- Codigo, descricao, NCM, CFOP
- Quantidade, valor unitario, descontos
- Impostos (ICMS, IPI, PIS, COFINS)

## Rotas Principais

### Dashboard
- `GET /fiscal/` - Dashboard com estatisticas e alertas

### Empresa
- `GET /fiscal/empresa` - Formulario de configuracao
- `POST /fiscal/empresa/salvar` - Salvar configuracao

### Certificados
- `GET /fiscal/certificados` - Lista de certificados
- `GET /fiscal/certificados/novo` - Formulario de upload
- `POST /fiscal/certificados/upload` - Upload de certificado A1/A3
- `POST /fiscal/certificados/<id>/excluir` - Excluir certificado
- `POST /fiscal/certificados/<id>/definir-padrao` - Definir como padrao

### PDV
- `GET /fiscal/pdv` - Interface do terminal PDV
- `GET /fiscal/pdv/buscar-produto?q=termo` - Busca de produtos
- `GET /fiscal/pdv/buscar-cliente?q=termo` - Busca de clientes
- `POST /fiscal/pdv/emitir-nfe` - Emissao de NFe/NFCe

### Notas Fiscais
- `GET /fiscal/notas` - Listagem com filtros
- `GET /fiscal/notas/<id>` - Detalhes da nota
- `GET /fiscal/notas/<id>/xml` - Download do XML
- `GET /fiscal/notas/<id>/danfe` - Geracao do DANFE PDF
- `POST /fiscal/notas/<id>/cancelar` - Cancelamento
- `POST /fiscal/notas/<id>/carta-correcao` - Carta de Correcao (CC-e)

### Inutilizacao
- `GET /fiscal/inutilizacao` - Lista de inutilizacoes
- `POST /fiscal/inutilizacao/salvar` - Nova inutilizacao

### Impostos
- `GET /fiscal/impostos` - Configuracao de impostos
- `POST /fiscal/impostos/salvar` - Salvar configuracoes

### Relatorios
- `GET /fiscal/relatorios` - Pagina de relatorios
- `POST /fiscal/relatorios/gerar` - Gerar relatorio
- `GET /fiscal/relatorios/notas-periodo` - Relatorio por periodo

### Status SEFAZ
- `GET /fiscal/status-sefaz` - Consulta status do servico

## Validadores

O sistema inclui validadores padrao da Receita Federal:

- `validar_cnpj(cnpj)` - Valida CNPJ com digitos verificadores
- `validar_cpf(cpf)` - Valida CPF com digitos verificadores
- `validar_inscricao_estadual(ie, uf)` - Valida IE por UF
- `validar_ncm(ncm)` - Valida codigo NCM (8 digitos)
- `validar_cfop(cfop)` - Valida codigo CFOP (4 digitos)

## Codigos e Tabelas

### Regimes Tributarios
- 1: Simples Nacional
- 2: Simples Nacional - Excesso de sublimite
- 3: Regime Normal (Lucro Presumido/Real)

### Formas de Pagamento
- 01: Dinheiro
- 03: Cartao de Credito
- 04: Cartao de Debito
- 15: Boleto Bancario
- 17: PIX
- 99: Outros

### CST ICMS (Regime Normal)
- 00: Tributada integralmente
- 10: Tributada com ICMS-ST
- 20: Com reducao de BC
- 40: Isenta
- 60: ICMS cobrado anteriormente por ST

### CSOSN (Simples Nacional)
- 101: Tributada com permissao de credito
- 102: Tributada sem permissao de credito
- 500: ICMS cobrado anteriormente por ST
- 900: Outros

## Fluxo de Emissao NFe

```
1. Usuario adiciona produtos no PDV
2. Seleciona cliente (opcional para NFCe)
3. Escolhe forma de pagamento
4. Clica em "Finalizar Venda"
   │
   ▼
5. Sistema cria registro NotaFiscal
6. Adiciona itens com calculo de impostos
7. Gera XML conforme layout SEFAZ 4.00
   │
   ▼
8. Carrega certificado digital
9. Assina XML com chave privada
10. Transmite para SEFAZ
    │
    ▼
11. SEFAZ valida e retorna
    ├── Autorizada: Grava protocolo
    └── Rejeitada: Grava motivo
    │
    ▼
12. Retorna resultado para usuario
```

## Seguranca

- Certificados A1 armazenados com senha criptografada
- Certificados A3 acessados via PIN do token
- Validacao de CNPJ do certificado vs empresa
- Log de todas operacoes fiscais
- Controle de acesso por decorator `@admin_required`

## Integracao SEFAZ

O sistema suporta comunicacao com todas as UFs via:
- SVRS (Sefaz Virtual Rio Grande do Sul)
- SVAN (Sefaz Virtual Ambiente Nacional)
- Webservices especificos por estado

### Ambientes
- 1: Producao (notas com validade fiscal)
- 2: Homologacao (testes sem validade)

## Dependencias

```
pynfe            # Geracao de XML NFe
signxml          # Assinatura digital
cryptography     # Manipulacao de certificados
PyKCS11          # Suporte a tokens A3
reportlab        # Geracao de DANFE PDF
```

## Configuracao Inicial

1. Cadastrar dados da empresa em `/fiscal/empresa`
2. Importar certificado digital em `/fiscal/certificados`
3. Configurar contador (opcional) em `/fiscal/contabilistas`
4. Definir CSC e ID CSC para NFCe
5. Configurar impostos padrao em `/fiscal/impostos`
6. Testar em ambiente de homologacao
7. Alterar para producao quando pronto

## Manutencao

### Certificado vencendo
O sistema alerta automaticamente 30 dias antes do vencimento.

### Inutilizacao
Deve ser feita ate o dia 10 do mes subsequente para numeros nao utilizados.

### Backups
Recomendado backup diario dos XMLs autorizados.
