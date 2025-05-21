# Documentação do Sistema Terman OS

## Visão Geral

O Terman OS é um sistema completo de gestão empresarial desenvolvido para a Mangueiras Terman, integrando diversos módulos essenciais para o gerenciamento eficiente do negócio.

## Arquitetura do Sistema

### Backend
- **Framework**: Django REST Framework 4.2.10
- **Autenticação**: JWT (JSON Web Tokens)
- **Banco de Dados**: 
  - Desenvolvimento: SQLite
  - Produção: PostgreSQL (recomendado)
- **Módulos Principais**:
  - accounts: Gerenciamento de usuários e autenticação
  - products: Cadastro e gestão de produtos
  - inventory: Controle de estoque
  - pos: Ponto de venda
  - orders: Pedidos e vendas
  - service_orders: Ordens de serviço
  - financial: Gestão financeira
  - fiscal: Emissão de notas fiscais
  - hr: Recursos humanos
  - dashboard: Painéis e relatórios

### Frontend
- **Framework**: React com Vite
- **Gerenciamento de Estado**: Context API
- **Comunicação com API**: Axios
- **Autenticação**: JWT com interceptores para refresh automático
- **Componentes Principais**:
  - Páginas de autenticação (login/registro)
  - Dashboard com painéis e gráficos
  - Gestão de inventário
  - Ordens de serviço com painel industrial
  - PDV com carrinho e finalização de vendas
  - Emissão fiscal

## Instalação e Configuração

### Requisitos
- Node.js 18+
- Python 3.11+
- PostgreSQL 14+ (para ambiente de produção)

### Instalação com Docker (Recomendado)

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/terman_os.git
cd terman_os
```

2. **Configure as variáveis de ambiente**
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. **Inicie os containers**
```bash
docker-compose up -d
```

4. **Acesse a aplicação**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/v1/
- Admin Django: http://localhost:8000/admin/

### Instalação Manual

#### Backend (Django)

1. **Configure o ambiente Python**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure o banco de dados**
- Para desenvolvimento, o SQLite já está configurado
- Para produção, configure o PostgreSQL no arquivo .env

3. **Execute as migrações**
```bash
python manage.py migrate
```

4. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

5. **Inicie o servidor**
```bash
python manage.py runserver 0.0.0.0:8000
```

#### Frontend (React)

1. **Configure o ambiente Node.js**
```bash
cd frontend
npm install
```

2. **Inicie o servidor de desenvolvimento**
```bash
npm run dev
```

## Funcionalidades Principais

### PDV e Cadastro de Clientes
- Ponto de venda completo com controle de estoque integrado
- Emissão de notas fiscais
- Cadastro e gestão de clientes

### Controle de Estoque
- Gestão de produtos e categorias
- Controle de entrada e saída
- Alertas de estoque baixo

### Ordem de Serviço
- Painel industrial para visualização em tempo real
- Acompanhamento de status
- Histórico de serviços

### Caixa / Financeiro
- Controle de receitas e despesas
- Relatórios financeiros
- Fluxo de caixa

### Marketplace Online
- Loja virtual integrada
- Pagamento online
- Gestão de pedidos

### Emissão Fiscal (NFe)
- Emissão de notas fiscais eletrônicas
- Gestão de documentos fiscais
- Conformidade com legislação

### RH e Funcionários
- Cadastro de funcionários
- Controle de acesso
- Gestão de permissões

## Suporte e Contato

Para obter suporte, entre em contato:
- Email: suporte@mangueirasterman.com.br
- Telefone: (XX) XXXX-XXXX

---

© 2025 Mangueiras Terman. Todos os direitos reservados.
