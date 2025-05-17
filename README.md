# 🧰 Mangueiras Terman OS — Plataforma de Gestão, Vendas e Automação

Sistema web desenvolvido para a empresa **Mangueiras Terman LTDA**, de Caçapava do Sul/RS, especializada em soluções hidráulicas, industriais e para o agronegócio.  
Este sistema unifica presença digital, automação operacional e relacionamento com clientes em uma plataforma única, robusta e escalável.

---

## 🌐 URL de Produção

[https://terman-os.onrender.com](https://terman-os.onrender.com)

---

## 📦 Tecnologias Utilizadas

- **Backend**: Python 3.11+, Flask, Flask-Login, SQLAlchemy, Flask-Migrate
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2
- **Banco de Dados**: PostgreSQL (Render) e SQLite (desenvolvimento)
- **Deploy**: Render (Web Service + PostgreSQL)
- **Outros**: Gunicorn, Werkzeug, Pillow (upload de imagens)

---

## 🧠 Funcionalidades

### 👥 Usuários
- Login e cadastro com diferenciação entre **Cliente** e **Administrador**
- Redirecionamento automático com base no perfil
- Área do cliente: pedidos, dados, acompanhamento
- Área administrativa protegida

### 🛍️ Marketplace
- Catálogo dinâmico com imagens reais
- Carrinho de compras com sessão persistente
- Visualização e acompanhamento de pedidos
- Responsividade total para mobile e desktop

### 🧑‍💼 Painel Administrativo
- CRUD completo de Produtos e Categorias
- Upload de imagens com validação
- Controle de pedidos e estoque em tempo real
- Visualização de detalhes, edição e exclusão

### 📈 Futuro (em desenvolvimento)
- Dashboard com KPIs e gráficos
- Geração de relatórios em PDF
- Integração com Pix e WhatsApp
- Notificações automatizadas

---

## 📁 Estrutura do Projeto

```
terman_os/
├── app/
│   ├── templates/        # HTML com Jinja2
│   ├── static/           # CSS, imagens, ícones
│   ├── models/           # SQLAlchemy Models
│   ├── routes/           # Blueprints organizados
│   ├── forms/            # Formulários com Flask-WTF
├── run.py                # Entry point da aplicação
├── requirements.txt      # Dependências do projeto
├── README.md             # Documentação principal
├── .env.example          # Variáveis de ambiente
```

---

## 🧪 Como rodar localmente

```bash
# 1. Clonar o repositório
git clone https://github.com/KallebyX/terman_os.git
cd terman_os

# 2. Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar o .env
cp .env.example .env
# Edite a DATABASE_URL conforme necessário

# 5. Migrar o banco
flask db upgrade

# 6. Rodar servidor
flask run
```

---

## ☁️ Deploy na Render

- Banco de dados PostgreSQL provisionado via Render
- Aplicação Flask rodando com Gunicorn (`web: gunicorn run:app`)
- Variáveis de ambiente configuradas:
  - `FLASK_APP=run.py`
  - `FLASK_ENV=production`
  - `SECRET_KEY=...`
  - `DATABASE_URL=postgresql://...`

---

## 📄 Licença e Direitos

Este sistema é de uso exclusivo da empresa **Mangueiras Terman LTDA**  
Desenvolvido pela **Oryum Tech (CNPJ: 49.549.704/0001-07)**.  
Reprodução, redistribuição ou modificação só são permitidas mediante autorização contratual.

---

## 👨‍💻 Desenvolvedor Responsável

**Kalleby Evangelho Mota**  
CEO da Oryum Tech · Fundador da Biomove  
📧 kallebyevangelho03@gmail.com  
🌐 [kallebyevangelho.com.br](https://www.kallebyevangelho.com.br)  
🔗 [LinkedIn](https://www.linkedin.com/in/kalleby-evangelho)