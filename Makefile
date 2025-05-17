# Makefile – Terman OS (dev + prod)

FLASK_APP=run.py
ENV_FILE=.env

run:
	@echo "🔄 Rodando servidor Flask (modo $(FLASK_ENV))..."
	FLASK_APP=$(FLASK_APP) FLASK_ENV=$(FLASK_ENV) flask run

env-dev:
	@echo "🔧 Carregando .env de desenvolvimento"
	ENV_FILE=.env FLASK_ENV=development make env

env-prod:
	@echo "🚀 Carregando .env de produção"
	ENV_FILE=.env.production FLASK_ENV=production make env

env:
	@echo "📦 Exportando variáveis do $(ENV_FILE)"
	export $$(cat $(ENV_FILE) | xargs)

install:
	@echo "📦 Instalando dependências..."
	pip install -r requirements.txt

freeze:
	@echo "📋 Atualizando requirements.txt..."
	pip freeze > requirements.txt

init-db:
	@echo "🧱 Inicializando migrações..."
	flask db init

migrate:
	@echo "📌 Gerando arquivo de migração..."
	flask db migrate -m "Atualização de banco"

upgrade:
	@echo "🚀 Aplicando migração no banco de dados..."
	flask db upgrade

deploy:
	@echo "🚀 Subindo para o GitHub e preparando deploy..."
	git add .
	git commit -m "🚀 Atualização de produção"
	git push origin main

test-db:
	@echo "🔍 Testando conexão com o banco"
	curl http://127.0.0.1:5000/test-db

create-admin:
	@echo "👤 Acessando shell do Flask..."
	FLASK_APP=$(FLASK_APP) flask shell

docs-serve:
	@echo "📘 Servindo documentação localmente..."
	mkdocs serve

docs-build:
	@echo "🏗️  Construindo documentação..."
	mkdocs build

docs-deploy:
	@echo "🚀 Publicando documentação no GitHub Pages..."
	mkdocs gh-deploy --clean