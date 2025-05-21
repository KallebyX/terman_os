#!/bin/bash

set -e

function wait_for_postgres() {
    echo "Waiting for PostgreSQL..."
    while ! pg_isready -h db -p 5432 -U postgres; do
        sleep 1
    done
    echo "PostgreSQL is ready!"
}

function wait_for_redis() {
    echo "Waiting for Redis..."
    while ! redis-cli -h redis ping; do
        sleep 1
    done
    echo "Redis is ready!"
}

# Esperar pelos serviços
wait_for_postgres
wait_for_redis

# Aplicar migrações do banco de dados
flask db upgrade || flask db init && flask db migrate && flask db upgrade

# Iniciar a aplicação
if [ "$FLASK_ENV" = "development" ]; then
    flask run --host=0.0.0.0
else
    gunicorn --bind 0.0.0.0:5000 --workers 4 --threads 4 run:app
fi 