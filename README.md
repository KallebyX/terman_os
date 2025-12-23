# 🧰 Mangueiras Terman OS — Plataforma de Gestão, Vendas e Automação

![GitHub Pages](https://img.shields.io/badge/docs-online-blue?logo=github&style=flat-square)
![Licença](https://img.shields.io/badge/licença-uso%20restrito-red?style=flat-square)
![Segurança](https://img.shields.io/badge/segurança-reportar%20vulnerabilidades-orange?style=flat-square)
[📘 Documentação Completa](https://kallebyx.github.io/terman_os/)

Sistema web completo desenvolvido para a empresa **Mangueiras Terman LTDA**, de Caçapava do Sul/RS, especializada em soluções hidráulicas, industriais e para o agronegócio.  
Este sistema unifica presença digital, automação operacional e relacionamento com clientes em uma plataforma única, robusta, escalável e moderna.

---

## 🌐 URL de Produção

🔗 [https://terman-os.onrender.com](https://terman-os.onrender.com)

---

## 📦 Tecnologias Utilizadas

- **Backend**: Python 3.11+, Flask, Flask-Login, SQLAlchemy, Flask-Migrate
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2
- **Banco de Dados**: PostgreSQL (Render) e SQLite (desenvolvimento)
- **Deploy**: Render (Web Service + PostgreSQL)
- **Outros**: Gunicorn, Werkzeug, Pillow (upload de imagens), MkDocs

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
- Geração de relatórios em PDF e Excel
- Integração com Pix e WhatsApp
- Notificações automatizadas
- API REST para integrações externas

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
├── docs/                 # Documentação MkDocs
├── run.py                # Entry point da aplicação
├── requirements.txt      # Dependências do projeto
├── .env.example          # Variáveis de ambiente
├── render.yaml           # Configuração do deploy
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

## 📘 Documentação

Documentação completa com:

- Estrutura do projeto
- Autenticação
- Rotas e modelos
- API interna
- Deploy, FAQ, créditos e mais

🔗 Acesse: [https://kallebyx.github.io/terman_os](https://kallebyx.github.io/terman_os)

---

## 📌 Changelog (resumo)

- ✅ CRUD de produtos, categorias e usuários
- ✅ Upload de imagens com Pillow
- ✅ Carrinho de compras com sessão
- ✅ Visualização de pedidos para cliente e admin
- ✅ Deploy no Render com PostgreSQL
- 🚧 Dashboard e relatórios em desenvolvimento
- 🚧 Integração com Pix e WhatsApp (planejado)

---

## 📄 Licença e Direitos

Este sistema é de uso exclusivo da empresa **Mangueiras Terman LTDA**  
Desenvolvido pela **Oryum Tech (CNPJ: 04.625.577/0001-40)**.  
Reprodução, redistribuição ou modificação só são permitidas mediante autorização contratual.

---

## 🤝 Contribuindo

Contribuições são bem-vindas!  
Confira as diretrizes em [CONTRIBUTING.md](../main/CONTRIBUTING.md) para saber como colaborar com o projeto.

---

## 📜 Licença

Este projeto é distribuído sob licença de uso restrito.  
Para detalhes, veja [LICENSE](../main/LICENSE).

---

## 🔐 Segurança

Para reportar vulnerabilidades ou comportamentos suspeitos, consulte o [SECURITY.md](../main/SECURITY.md).

---

## 👨‍💻 Desenvolvedor Responsável

**Kalleby Evangelho Mota**  
CEO da Oryum Tech · Fundador da Biomove  
📧 kallebyevangelho03@gmail.com  
🌐 [kallebyevangelho.com.br](https://www.kallebyevangelho.com.br)  
🔗 [LinkedIn](https://www.linkedin.com/in/kalleby-evangelho)