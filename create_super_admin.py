#!/usr/bin/env python3
"""
Script para criar o Super Admin inicial do sistema Terman OS.
Execute este script uma vez para criar o usuario super admin.

Uso:
    python create_super_admin.py
"""
from app import create_app, db
from app.models.user import User


def create_super_admin():
    """Cria o super admin do sistema"""
    app = create_app()

    with app.app_context():
        # Dados do Super Admin
        email = 'kallebyevangelho03@gmail.com'
        senha = 'kk030904K.k'
        nome = 'Kalleby Evangelho'

        # Verificar se ja existe
        existing = User.query.filter_by(email=email).first()

        if existing:
            # Se existir, atualizar para super_admin
            existing.tipo_usuario = 'super_admin'
            existing.ativo = True
            existing.set_senha(senha)
            db.session.commit()
            print(f'Usuario {email} atualizado para Super Admin!')
        else:
            # Criar novo super admin
            super_admin = User(
                nome=nome,
                email=email,
                tipo_usuario='super_admin',
                ativo=True
            )
            super_admin.set_senha(senha)
            db.session.add(super_admin)
            db.session.commit()
            print(f'Super Admin criado com sucesso!')

        print(f'\n=== CREDENCIAIS DO SUPER ADMIN ===')
        print(f'Email: {email}')
        print(f'Senha: {senha}')
        print(f'==================================\n')
        print('IMPORTANTE: Altere a senha apos o primeiro login!')


if __name__ == '__main__':
    create_super_admin()
