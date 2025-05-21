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

3. **Edite os arquivos .env conforme necessário**

   **Backend (.env)**:
   ```
   DEBUG=True
   SECRET_KEY=sua-chave-secreta-muito-segura
   DATABASE_URL=postgresql://postgres:postgres@db:5432/terman_db
   ALLOWED_HOSTS=localhost,127.0.0.1,backend
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://frontend:3000
   JWT_SECRET_KEY=sua-chave-jwt-secreta
   JWT_ACCESS_TOKEN_LIFETIME=1h
   JWT_REFRESH_TOKEN_LIFETIME=7d
   ```

   **Frontend (.env)**:
   ```
   VITE_API_URL=http://localhost:8000/api/v1/
   VITE_JWT_SECRET=sua-chave-jwt-secreta
   ```

4. **Inicie os containers**
```bash
docker-compose up --build
```

5. **Crie um superusuário para acessar o sistema**
```bash
docker-compose exec backend python manage.py createsuperuser
```

6. **Acesse a aplicação**
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

2. **Configure o arquivo .env**
Crie um arquivo `.env` na pasta backend com as seguintes variáveis:
```
DEBUG=True
SECRET_KEY=sua-chave-secreta-muito-segura
DATABASE_URL=sqlite:///db.sqlite3
# Para PostgreSQL: DATABASE_URL=postgresql://usuario:senha@localhost:5432/terman_db
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
JWT_SECRET_KEY=sua-chave-jwt-secreta
JWT_ACCESS_TOKEN_LIFETIME=1h
JWT_REFRESH_TOKEN_LIFETIME=7d
```

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

2. **Configure o arquivo .env**
Crie um arquivo `.env` na pasta frontend com as seguintes variáveis:
```
VITE_API_URL=http://localhost:8000/api/v1/
VITE_JWT_SECRET=sua-chave-jwt-secreta
```

3. **Inicie o servidor de desenvolvimento**
```bash
npm run dev
```

## Autenticação e Uso da API

### Autenticação com JWT

O sistema utiliza JSON Web Tokens (JWT) para autenticação. Para consumir a API, siga os passos:

1. **Obtenha um token de acesso**

```javascript
// Exemplo com Axios
import axios from 'axios';

const login = async (email, password) => {
  try {
    const response = await axios.post('http://localhost:8000/api/v1/accounts/login/', {
      email,
      password
    });
    
    // Armazenar tokens
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    
    return response.data;
  } catch (error) {
    console.error('Erro ao fazer login:', error);
    throw error;
  }
};
```

2. **Configure o Axios para incluir o token em todas as requisições**

```javascript
// Configuração do interceptor
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para renovar token expirado
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Se o erro for 401 (não autorizado) e não for uma tentativa de refresh
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Tentar renovar o token
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post('http://localhost:8000/api/v1/accounts/token/refresh/', {
          refresh: refreshToken
        });
        
        // Armazenar novo token de acesso
        localStorage.setItem('access_token', response.data.access);
        
        // Atualizar o cabeçalho da requisição original
        originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
        
        // Repetir a requisição original
        return axios(originalRequest);
      } catch (refreshError) {
        // Se não conseguir renovar, redirecionar para login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);
```

3. **Exemplo de requisição autenticada**

```javascript
// Exemplo de requisição que requer autenticação
const fetchUserProfile = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/v1/accounts/me/');
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar perfil:', error);
    throw error;
  }
};
```

### Endpoints da API

#### Autenticação

- `POST /api/v1/accounts/register/` - Registro de novo usuário
- `POST /api/v1/accounts/login/` - Login de usuário
- `POST /api/v1/accounts/token/refresh/` - Renovar token de acesso
- `POST /api/v1/accounts/token/verify/` - Verificar validade do token
- `GET /api/v1/accounts/me/` - Obter perfil do usuário autenticado

#### Produtos

- `GET /api/v1/products/produtos/` - Listar produtos
- `POST /api/v1/products/produtos/` - Criar novo produto
- `GET /api/v1/products/produtos/{id}/` - Obter detalhes de um produto
- `PUT /api/v1/products/produtos/{id}/` - Atualizar produto
- `DELETE /api/v1/products/produtos/{id}/` - Excluir produto

#### Estoque

- `GET /api/v1/inventory/estoque/` - Listar itens de estoque
- `GET /api/v1/inventory/estoque/{id}/` - Obter detalhes de um item de estoque
- `GET /api/v1/inventory/movimentacoes/` - Listar movimentações de estoque
- `POST /api/v1/inventory/movimentacoes/` - Criar nova movimentação de estoque

#### Pedidos

- `GET /api/v1/orders/orders/` - Listar todos os pedidos (admin)
- `GET /api/v1/orders/my-orders/` - Listar pedidos do usuário atual
- `POST /api/v1/orders/create/` - Criar novo pedido
- `GET /api/v1/orders/orders/{id}/` - Obter detalhes de um pedido
- `PATCH /api/v1/orders/orders/{id}/` - Atualizar status de um pedido

## Executando Testes

### Testes do Backend

1. **Executando todos os testes**
```bash
# Localmente
cd backend
python -m pytest tests/ -v

# Com Docker
docker-compose exec backend ./run_tests.sh
```

2. **Executando testes específicos**
```bash
# Testes de autenticação
python -m pytest tests/test_accounts.py -v

# Testes de produtos
python -m pytest tests/test_products.py -v

# Testes de estoque
python -m pytest tests/test_inventory.py -v

# Testes de pedidos
python -m pytest tests/test_orders.py -v
```

3. **Executando testes com cobertura**
```bash
python -m pytest --cov=apps tests/
```

### Testes do Frontend

1. **Executando testes unitários**
```bash
cd frontend
npm test
```

2. **Executando testes com modo de observação**
```bash
npm test -- --watch
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
