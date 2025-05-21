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
  PGPASSWORD=$password psql -h "$host" -p "$port" -U "$user" -d "$database" -c '\q' 2>/dev/null
  return $?
}

# Verificar se o host está acessível primeiro
echo "Verificando conectividade com o host $host..."
timeout 5 bash -c "until nc -z $host $port; do echo 'Aguardando porta $port em $host...'; sleep 1; done" || echo "Não foi possível conectar ao host $host:$port"

# Contador para timeout
count=0
max_attempts=60

# Espera até conseguir conectar no PostgreSQL
until check_postgres; do
  count=$((count+1))
  echo "PostgreSQL não está disponível ainda - aguardando... (tentativa $count/$max_attempts)"
  
  # Verificar status do contêiner PostgreSQL a cada 5 tentativas
  if [ $((count % 5)) -eq 0 ]; then
    echo "Verificando status do contêiner PostgreSQL..."
    docker ps | grep postgres || echo "Contêiner PostgreSQL não encontrado"
  fi
  
  # Timeout após 60 tentativas (1 minuto)
  if [ $count -ge $max_attempts ]; then
    echo "Timeout ao aguardar PostgreSQL. Verifique se o serviço está rodando corretamente."
    exit 1
  fi
  
  sleep 1
done

echo "✅ PostgreSQL está pronto! Iniciando o backend..."

# Executa o comando original (passado via CMD)
exec "$@"
