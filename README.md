# 🧰 Mangueiras Terman — Sistema de Gestão e Marketplace

Plataforma web completa desenvolvida para a empresa **Mangueiras Terman LTDA**, especializada em soluções hidráulicas, industriais e para o agronegócio. O sistema unifica presença digital com automação operacional, integrando loja online, painel administrativo, controle de estoque, pedidos e dashboard de indicadores.

---

## 📦 Tecnologias Utilizadas

- **Backend**: Python 3.11+, Flask, SQLAlchemy
- **Frontend**: HTML5, Bootstrap 5, Jinja2
- **Banco de Dados**: SQLite (dev), PostgreSQL (prod)
- **Gerenciamento de Usuários**: Flask-Login
- **Upload de Arquivos**: `werkzeug` com manipulação segura
- **Templates**: `Jinja2`
- **Deploy (sugerido)**: Render, Railway ou VPS com Gunicorn

---

## 🧠 Funcionalidades

### 👥 Usuários
- Diferenciação entre **Cliente** e **Administrador**
- Login e cadastro com validação
- Redirecionamento dinâmico por tipo de usuário

### 🛍️ Marketplace
- Catálogo com imagens reais dos produtos
- Carrinho de compras com controle de sessão
- Finalização de pedido protegida por login
- Visualização do pedido (cliente e admin)

### 🧑‍💼 Painel Administrativo
- CRUD completo de Produtos e Categorias
- Upload de imagens diretamente pelo formulário
- Gerenciamento de pedidos em tempo real
- Controle de estoque automático

### 📈 Futuro (em construção)
- Dashboard com KPIs e gráficos interativos
- Geração de PDF dos pedidos
- Integração com WhatsApp e pagamentos via Pix
- Logs administrativos e notificações automáticas

---

## 📁 Estrutura de Pastas

terman_os/
├── app/
│   ├── templates/        # HTML com Jinja2
│   ├── static/           # CSS, imagens de produtos
│   ├── models/           # Modelos SQLAlchemy
│   ├── routes/           # Blueprints por módulo
│   ├── forms/            # (em breve) Flask-WTF
├── run.py                # App launcher
├── requirements.txt      # Dependências

---

## 📸 Prints (sugestão de imagens no futuro)

- Painel do Cliente
- Carrinho de Compras
- Administração de Produtos
- Visualização de Pedidos

---

## 🏗️ Para rodar localmente

```bash
# 1. Clonar o repositório
git clone https://github.com/seuusuario/mangueiras_terman.git
cd mangueiras_terman

# 2. Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate   # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar o servidor Flask
python run.py


⸻

✅ Status do Projeto
	•	✅ Funcionalidades principais concluídas
	•	🛠️ Dashboard e relatórios em desenvolvimento
	•	🧪 Testes automatizados em breve
	•	📲 Integrações externas planejadas

⸻

## 📄 Licença

Este projeto é desenvolvido pela empresa **Oryum Tech (CNPJ: 49.549.704/0001-07)** para uso exclusivo da **Mangueiras Terman LTDA**, de Caçapava do Sul - RS.  
Seu uso está restrito a fins educacionais e corporativos internos, salvo autorização contratual.

---

## 🤝 Desenvolvedor Responsável

**Kalleby Evangelho Mota**  
👨‍💻 Estudante de Engenharia Biomédica, fundador da Biomove e CEO da Oryum Tech  
🌐 [kallebyevangelho.com.br](https://www.kallebyevangelho.com.br)  
📧 kallebyevangelho03@gmail.com

---

## 📌 Agora faça o primeiro commit

```bash
git init
git add .
git commit -m "🔰 Primeiro commit - base do sistema da Mangueiras Terman"

Depois, conecte ao GitHub:

git remote add origin https://github.com/KallebyX/mangueiras_terman.git
git push -u origin main


⸻