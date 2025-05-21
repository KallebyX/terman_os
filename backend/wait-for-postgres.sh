#!/bin/sh

echo "⏳ Aguardando o PostgreSQL ficar disponível..."

# Espera até conseguir conectar na porta 5432 do container 'db'
until nc -z db 5432; do
  sleep 1
done

echo "✅ PostgreSQL está pronto! Iniciando o backend..."

# Executa o comando original (passado via CMD)
exec "$@"
