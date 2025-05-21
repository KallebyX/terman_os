#!/bin/bash

# Configurar ambiente
export DJANGO_SETTINGS_MODULE=config.settings
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Executar os testes
python -m pytest tests/ -v
