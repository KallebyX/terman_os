"""
Script para depurar a API de login
"""
import os
import django
import sys
import json
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def test_login_api(email, password, base_url="http://localhost:8000"):
    """
    Testa a API de login diretamente
    """
    print("\n===== DEPURAÇÃO DA API DE LOGIN =====")
    
    # Endpoint de login
    login_url = f"{base_url}/api/v1/auth/login/"
    
    # Dados de login
    login_data = {
        "email": email,
        "password": password
    }
    
    print(f"Enviando requisição para: {login_url}")
    print(f"Dados: {json.dumps(login_data, indent=2)}")
    
    try:
        # Faz a requisição
        response = requests.post(login_url, json=login_data)
        
        # Exibe o resultado
        print(f"\nStatus: {response.status_code}")
        print(f"Headers: {json.dumps(dict(response.headers), indent=2)}")
        
        try:
            # Tenta parsear o JSON
            response_data = response.json()
            print(f"Resposta: {json.dumps(response_data, indent=2)}")
        except json.JSONDecodeError:
            # Se não for JSON, exibe o texto
            print(f"Resposta (texto): {response.text}")
        
    except Exception as e:
        print(f"Erro ao fazer requisição: {e}")
    
    print("\n===== FIM DA DEPURAÇÃO =====")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        email = sys.argv[1]
        password = sys.argv[2]
    else:
        email = input("Email: ")
        password = input("Senha: ")
    
    test_login_api(email, password)
