FROM node:18-alpine

WORKDIR /app

# Copiar package.json e instalar dependências
COPY package*.json ./
RUN npm install

# Copiar o código da aplicação
COPY . .

# Expor a porta da aplicação
EXPOSE 3000

# Comando para iniciar a aplicação em modo de desenvolvimento
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
