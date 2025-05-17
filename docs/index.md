# 📘 Documentação Técnica — Terman OS

> **Versão da documentação:** 1.0 • Última atualização: Maio de 2025

Bem-vindo à documentação oficial do sistema Terman OS, desenvolvido pela Oryum Tech para a empresa Mangueiras Terman LTDA.  
Aqui você encontrará informações sobre arquitetura, rotas, modelos de dados, deploy e extensões futuras.

---

## 📦 Visão Geral

- **Backend**: Flask (Python 3.11+)
- **Frontend**: HTML + Bootstrap 5 + Jinja2
- **Banco de Dados**: PostgreSQL (produção), SQLite (desenvolvimento)
- **Deploy**: Render.com
- **Relatórios**: PDF com `fpdf` e Excel com `xlsxwriter`

---

## 📂 Estrutura do Projeto

```
terman_os/
├── app/
│   ├── routes/        # Blueprints
│   ├── models/        # SQLAlchemy Models
│   ├── forms/         # Flask-WTF
│   ├── templates/     # Jinja2
│   ├── static/        # Imagens, CSS
├── scripts/           # Geração de relatórios
├── run.py             # Ponto de entrada
├── requirements.txt
├── render.yaml
```

---

## 🔐 Autenticação

- Flask-Login
- Sessão segura com `SECRET_KEY`
- Diferenciação de usuários (`cliente`, `admin`)

---

## 📊 Relatórios

- Geração em PDF: `scripts/gerar_relatorios.py`
- Geração em XLSX: mesma rotina com `xlsxwriter`
- Agendamento via CronJob no Render

---

## 🔁 Rotas principais

| Tipo   | Rota                   | Descrição                         |
|--------|------------------------|-----------------------------------|
| GET    | `/`                    | Página inicial                    |
| GET    | `/loja`                | Lista de produtos (marketplace)  |
| GET    | `/produto/<id>`        | Detalhes do produto               |
| POST   | `/carrinho/adicionar`  | Adiciona ao carrinho              |
| GET    | `/admin/produtos`      | Listagem de produtos (admin)      |
| POST   | `/admin/novo-produto`  | Cadastro de produto (admin)       |
| GET    | `/auth/login`          | Página de login                   |
| GET    | `/cliente/pedidos`     | Histórico de pedidos (cliente)    |

---

## 📦 Models (exemplo)

```python
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, default=0)
```

---

## 📤 Deploy

- Executado com `gunicorn run:app`
- Banco PostgreSQL via Render
- `.env` gerenciado pelo painel da Render
- `render.yaml` com configuração de staging, worker e cronJob

---

## ✨ Contribuições

Leia [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## 👨‍💻 Manutenção

Documentação mantida por [Kalleby Evangelho](https://www.kallebyevangelho.com.br) | Oryum Tech