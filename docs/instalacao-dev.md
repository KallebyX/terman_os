# 🧪 Guia de Instalação — Ambiente de Desenvolvimento

Este guia explica como rodar o sistema **Terman OS** localmente, usando Python, Flask e SQLite/PostgreSQL.

---

## 🧰 Pré-requisitos

Antes de começar, instale:

- [Python 3.11+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [pip](https://pip.pypa.io/en/stable/installation/)
- (Opcional) [PostgreSQL](https://www.postgresql.org/download/)

---

## 🚀 Clonando o Projeto

```bash
git clone https://github.com/KallebyX/terman_os.git
cd terman_os
```

---

## 🐍 Criando Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

---

## 📦 Instalando Dependências

```bash
pip install -r requirements.txt
```

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=superseguro
DATABASE_URL=sqlite:///dev.db
UPLOAD_FOLDER=app/static/produtos
MAX_CONTENT_LENGTH=16777216
```

---

## 🧱 Inicializando o Banco de Dados

```bash
flask db init      # apenas na primeira vez
flask db migrate -m "init"
flask db upgrade
```

---

## 🧪 Rodando Localmente

```bash
flask run
```

Acesse: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 👤 Criando um Admin

```bash
flask shell
```

No shell interativo:

```python
from app import db
from app.models.user import User

admin = User(nome="admin", email="admin@example.com", tipo_usuario="admin")
admin.set_senha("123456")
db.session.add(admin)
db.session.commit()
```

---

## 🧼 Dicas Adicionais

- Use `make run` se tiver o `Makefile` configurado
- Para testes, use `sqlite:///teste.db`
- Logs aparecem no terminal (modo debug)

---

Se tiver dúvidas, abra uma [Issue](https://github.com/KallebyX/terman_os/issues) ou entre em contato com o desenvolvedor.
