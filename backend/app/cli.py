import click
from flask.cli import with_appcontext
from app.models.user import User
from app import db

@click.command('create-admin')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin_command(email, password):
    """Criar um usuário administrador."""
    user = User.query.filter_by(email=email).first()
    if user:
        click.echo('Usuário já existe!')
        return
        
    user = User(
        email=email,
        nome='Administrador',
        tipo='admin'
    )
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f'Administrador criado com sucesso: {email}')

def init_app(app):
    app.cli.add_command(create_admin_command) 