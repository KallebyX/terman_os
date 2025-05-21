#!/bin/bash

set -e

host="db"
port="5432"
user="postgres"
password="postgres"
database="terman_db"

echo "⏳ Aguardando o PostgreSQL ficar disponível..."

# Espera até conseguir conectar na porta 5432 do container 'db'
until PGPASSWORD=$password psql -h "$host" -p "$port" -U "$user" -d "$database" -c '\q' 2>/dev/null; do
  echo "PostgreSQL não está disponível ainda - aguardando..."
  sleep 1
done

echo "✅ PostgreSQL está pronto! Iniciando o backend..."

# Executa o comando original (passado via CMD)
exec "$@"
