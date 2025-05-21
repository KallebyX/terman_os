.PHONY: build up down logs shell test lint format migrate collectstatic createsuperuser

# Variáveis
COMPOSE = docker-compose
MANAGE = docker-compose exec backend python manage.py

# Comandos Docker
build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f

shell:
	$(COMPOSE) exec backend python manage.py shell_plus

# Comandos Django
migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

collectstatic:
	$(MANAGE) collectstatic --noinput

createsuperuser:
	$(MANAGE) createsuperuser

# Testes e Qualidade de Código
test:
	$(COMPOSE) exec backend pytest

coverage:
	$(COMPOSE) exec backend pytest --cov=.

lint:
	$(COMPOSE) exec backend flake8 .
	$(COMPOSE) exec backend black . --check
	$(COMPOSE) exec backend isort . --check-only

format:
	$(COMPOSE) exec backend black .
	$(COMPOSE) exec backend isort .

# Celery
celery-worker:
	$(COMPOSE) exec backend celery -A config worker --loglevel=info

celery-beat:
	$(COMPOSE) exec backend celery -A config beat --loglevel=info

# Limpeza
clean:
	$(COMPOSE) down -v
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

# Produção
prod-build:
	$(COMPOSE) -f docker-compose.prod.yml build

prod-up:
	$(COMPOSE) -f docker-compose.prod.yml up -d

prod-down:
	$(COMPOSE) -f docker-compose.prod.yml down

# Backup
backup-db:
	$(COMPOSE) exec db pg_dump -U postgres terman_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db:
	$(COMPOSE) exec -T db psql -U postgres terman_db < $(file)
