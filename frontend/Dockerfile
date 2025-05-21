FROM node:18-alpine

WORKDIR /app

# Instalar dependências
COPY package*.json ./
RUN npm install

# Copiar o código fonte
COPY . .

# Expor a porta
EXPOSE 3000

# Iniciar o servidor de desenvolvimento
CMD ["npm", "run", "dev"]
