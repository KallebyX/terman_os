# 🚀 Deploy — Render.com

Este guia ensina como publicar o sistema **Terman OS** na nuvem usando a plataforma [Render](https://render.com), com PostgreSQL e suporte a ambiente `.env`.

---

## 🧱 Pré-requisitos

- Conta gratuita no [Render](https://render.com)
- Repositório no GitHub com o projeto
- Banco PostgreSQL (pode ser interno ou externo na Render)

---

## 🔐 Variáveis de Ambiente (.env)

No painel da Render, adicione as seguintes variáveis:

```env
FLASK_APP=run.py
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_db
UPLOAD_FOLDER=app/static/produtos
MAX_CONTENT_LENGTH=16777216
```

---

## ⚙️ Arquivos necessários

- `run.py`: ponto de entrada com `create_app()`
- `render.yaml`: arquivo de configuração do deploy
- `requirements.txt`: dependências, incluindo `gunicorn` e `psycopg2-binary`

---

## 🛠 render.yaml

```yaml
services:
  - type: web
    name: terman-os
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app
    envVars:
      - key: FLASK_APP
        value: run.py
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        sync: false
      - key: DATABASE_URL
        fromDatabase:
          name: terman-db
          property: connectionString
      - key: UPLOAD_FOLDER
        value: app/static/produtos
      - key: MAX_CONTENT_LENGTH
        value: "16777216"

databases:
  - name: terman-db
    databaseName: terman_db
    user: admin
```

---

## 🔄 Migrações

Após o deploy, acesse o terminal web do Render e execute:

```bash
flask db upgrade
```

---

## 🔁 CronJobs e Worker (opcional)

Use `render.yaml` para:

- Gerar relatórios automáticos
- Agendar tarefas recorrentes
- Processar filas (futuro)

---

## 📦 Publicação

Após salvar as configurações:

1. Clique em **New Web Service**
2. Selecione seu repositório
3. Escolha o ambiente **Python 3**
4. Configure variáveis e `startCommand`
5. Publique 🎉

---

## 🌐 Acesso

Acesse sua aplicação em:

```
https://terman-os.onrender.com
```

---

## 📩 Suporte

Se tiver dúvidas, entre em contato com o desenvolvedor:  
📧 **kallebyevangelho03@gmail.com**
