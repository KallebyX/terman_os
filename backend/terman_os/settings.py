INSTALLED_APPS = [
    # Outros apps do Django
]

MIDDLEWARE = [
    # Outros middlewares do Django
]

# Adicionando configuração de CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

INSTALLED_APPS += [
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
] + MIDDLEWARE
