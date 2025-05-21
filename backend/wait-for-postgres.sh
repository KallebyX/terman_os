#!/bin/bash

set -e

host="db"
port="5432"
user="postgres"
password="postgres"
database="terman_db"

echo "⏳ Aguardando o PostgreSQL ficar disponível..."

# Função para verificar se o PostgreSQL está pronto
check_postgres() {
  pg_isready -h "$host" -p "$port" -U "$user"
  return $?
}

# Função para verificar se o banco de dados existe
check_database_exists() {
  PGPASSWORD=$password psql -h "$host" -p "$port" -U "$user" -lqt | cut -d \| -f 1 | grep -qw "$database"
  return $?
}

# Espera até conseguir conectar no PostgreSQL
until check_postgres; do
  echo "PostgreSQL não está disponível ainda - aguardando..."
  sleep 2
done

echo "PostgreSQL está disponível!"

# Verificar se o banco de dados existe
if ! check_database_exists; then
  echo "Banco de dados $database não existe. Criando..."
  PGPASSWORD=$password psql -h "$host" -p "$port" -U "$user" -c "CREATE DATABASE $database;" || {
    echo "Falha ao criar o banco de dados $database"
    exit 1
  }
  echo "Banco de dados $database criado com sucesso!"
else
  echo "Banco de dados $database já existe."
fi

echo "✅ PostgreSQL está pronto! Iniciando o backend..."

# Executa o comando original (passado via CMD)
exec "$@"
