import os
import shutil
from pathlib import Path

def cleanup_project():
    # Definir o diretório base (backend)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base_dir)
    
    print(f"Trabalhando no diretório: {base_dir}")
    
    # Arquivos a serem removidos
    files_to_remove = [
        'manage.py',
        'debug_login_api.py',
        'debug_auth.py',
        'create_superuser.py',
        'celery_app.py'
    ]
    
    # Diretórios a serem removidos
    dirs_to_remove = [
        'apps',
        'config',
        'terman_os'
    ]
    
    # Remover arquivos
    for file in files_to_remove:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"✅ Removido: {file}")
        except Exception as e:
            print(f"❌ Erro ao remover {file}: {str(e)}")
    
    # Remover diretórios
    for dir_name in dirs_to_remove:
        try:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
                print(f"✅ Removido diretório: {dir_name}")
        except Exception as e:
            print(f"❌ Erro ao remover diretório {dir_name}: {str(e)}")
    
    # Criar nova estrutura
    dirs_to_create = [
        'app/models',
        'app/blueprints/auth',
        'app/blueprints/admin',
        'app/blueprints/cliente',
        'app/blueprints/pdv',
        'app/api',
        'app/tasks',
        'app/static/img',
        'app/templates/auth',
        'app/templates/admin',
        'app/templates/cliente',
        'app/templates/pdv',
        'migrations',
        'tests',
        'scripts'
    ]
    
    # Criar diretórios
    for dir_path in dirs_to_create:
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"✅ Criado diretório: {dir_path}")
        except Exception as e:
            print(f"❌ Erro ao criar diretório {dir_path}: {str(e)}")
    
    # Criar __init__.py nos diretórios Python
    python_dirs = [
        'app',
        'app/models',
        'app/blueprints',
        'app/blueprints/auth',
        'app/blueprints/admin',
        'app/blueprints/cliente',
        'app/blueprints/pdv',
        'app/api',
        'app/tasks',
        'tests'
    ]
    
    for dir_path in python_dirs:
        init_file = os.path.join(dir_path, '__init__.py')
        try:
            if not os.path.exists(init_file):
                Path(init_file).touch()
                print(f"✅ Criado: {init_file}")
        except Exception as e:
            print(f"❌ Erro ao criar {init_file}: {str(e)}")

if __name__ == '__main__':
    print("Iniciando limpeza e reorganização do projeto...")
    cleanup_project()
    print("\nProcesso finalizado!") 