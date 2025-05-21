import click
from flask.cli import with_appcontext
from .models import User, db

@click.command('create-admin')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin(email, password):
    """Cria um usuário administrador"""
    user = User(
        email=email,
        role='admin'
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f'Administrador criado com sucesso: {email}') 