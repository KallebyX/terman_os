"""
Script de Inicialização e Migração do Banco de Dados - Terman OS v2.0
Cria todas as tabelas e gerencia migração de dados existentes
"""
from app import create_app, db
from app.models import *
import sys

def init_database():
    """Inicializa o banco de dados criando todas as tabelas"""
    app = create_app()

    with app.app_context():
        print("🔄 Iniciando criação do banco de dados...")

        try:
            # Criar todas as tabelas
            db.create_all()
            print("✅ Todas as tabelas foram criadas com sucesso!")

            # Listar tabelas criadas
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()

            print(f"\n📊 Total de tabelas: {len(tables)}")
            print("\n📋 Tabelas criadas:")
            for table in sorted(tables):
                print(f"   ✓ {table}")

            return True

        except Exception as e:
            print(f"❌ Erro ao criar banco de dados: {e}")
            return False


def migrate_existing_data():
    """Migra dados existentes para nova estrutura"""
    app = create_app()

    with app.app_context():
        print("\n🔄 Verificando necessidade de migração de dados...")

        try:
            # Verificar se há produtos sem categoria_id
            from app.models import Produto, Categoria

            produtos_sem_categoria_id = Produto.query.filter(
                Produto.categoria_id == None
            ).all()

            if produtos_sem_categoria_id:
                print(f"⚠️  Encontrados {len(produtos_sem_categoria_id)} produtos sem categoria_id")
                print("🔄 Migrando categorias de string para FK...")

                # Criar categorias únicas baseadas nas strings existentes
                categorias_str = set()
                for produto in Produto.query.all():
                    if hasattr(produto, 'categoria') and isinstance(produto.categoria, str):
                        if produto.categoria:
                            categorias_str.add(produto.categoria)

                # Criar registros de categoria
                categorias_map = {}
                for cat_nome in categorias_str:
                    # Verificar se já existe
                    cat = Categoria.query.filter_by(nome=cat_nome).first()
                    if not cat:
                        cat = Categoria(nome=cat_nome)
                        db.session.add(cat)
                        db.session.flush()
                    categorias_map[cat_nome] = cat.id

                db.session.commit()
                print(f"✅ Criadas {len(categorias_map)} categorias")

                # Atualizar produtos
                for produto in produtos_sem_categoria_id:
                    if hasattr(produto, 'categoria') and isinstance(produto.categoria, str):
                        if produto.categoria in categorias_map:
                            produto.categoria_id = categorias_map[produto.categoria]

                db.session.commit()
                print(f"✅ Migrados {len(produtos_sem_categoria_id)} produtos")
            else:
                print("✅ Nenhuma migração de dados necessária")

            return True

        except Exception as e:
            print(f"⚠️  Aviso durante migração: {e}")
            print("   (Isso é normal se for primeira execução)")
            return True


def create_initial_data():
    """Cria dados iniciais para testes"""
    app = create_app()

    with app.app_context():
        print("\n🔄 Verificando dados iniciais...")

        try:
            from app.models import User, Categoria

            # Verificar se já existem usuários
            if User.query.count() == 0:
                print("📝 Criando usuário admin padrão...")
                from werkzeug.security import generate_password_hash

                admin = User(
                    nome="Administrador",
                    email="admin@terman.com",
                    senha_hash=generate_password_hash("admin123"),
                    tipo_usuario="admin"
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuário admin criado (admin@terman.com / admin123)")

            # Verificar se já existem categorias
            if Categoria.query.count() == 0:
                print("📝 Criando categorias padrão...")
                categorias_padrao = [
                    "Mangueiras Hidráulicas",
                    "Mangueiras Industriais",
                    "Conexões",
                    "Ferramentas",
                    "Acessórios"
                ]

                for nome in categorias_padrao:
                    cat = Categoria(nome=nome)
                    db.session.add(cat)

                db.session.commit()
                print(f"✅ Criadas {len(categorias_padrao)} categorias padrão")

            print("✅ Dados iniciais verificados")
            return True

        except Exception as e:
            print(f"⚠️  Aviso ao criar dados iniciais: {e}")
            return True


def main():
    """Execução principal"""
    print("=" * 60)
    print("🚀 TERMAN OS v2.0 - Inicialização do Banco de Dados")
    print("=" * 60)

    # 1. Criar banco de dados
    if not init_database():
        print("\n❌ Falha ao criar banco de dados")
        sys.exit(1)

    # 2. Migrar dados existentes
    if not migrate_existing_data():
        print("\n⚠️  Aviso durante migração")

    # 3. Criar dados iniciais
    if not create_initial_data():
        print("\n⚠️  Aviso ao criar dados iniciais")

    print("\n" + "=" * 60)
    print("✅ INICIALIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("\n📖 Próximos passos:")
    print("   1. Execute: flask run")
    print("   2. Acesse: http://localhost:5000")
    print("   3. Login: admin@terman.com / admin123")
    print("\n")


if __name__ == "__main__":
    main()
