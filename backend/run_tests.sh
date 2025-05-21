#!/bin/bash

# Configurar ambiente
export DJANGO_SETTINGS_MODULE=config.settings
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Verificar se o Python está instalado
if command -v python3 &>/dev/null; then
    PYTHON_CMD=python3
elif command -v python &>/dev/null; then
    PYTHON_CMD=python
else
    echo "Erro: Python não encontrado. Por favor, instale o Python 3."
    exit 1
fi

# Executar os testes
$PYTHON_CMD -m pytest tests/ -v
