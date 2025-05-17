# Makefile – Terman OS

run:
	@echo "🔄 Rodando servidor Flask..."
	FLASK_APP=run.py FLASK_ENV=development flask run

env:
	@echo "🔄 Carregando variáveis do .env"
	export $$(cat .env | xargs)

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
	@echo "👤 Criando admin pelo shell interativo..."
	FLASK_APP=run.py flask shell