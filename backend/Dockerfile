FROM python:3.11

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y netcat-traditional && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o script de espera pelo PostgreSQL
COPY wait-for-postgres.sh /app/wait-for-postgres.sh
RUN chmod +x /app/wait-for-postgres.sh

# Copiar o código da aplicação
COPY . .

# Expor a porta da aplicação
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["/app/wait-for-postgres.sh", "python", "manage.py", "runserver", "0.0.0.0:8000"]
