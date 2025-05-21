import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_login_success(client):
    user = User(email='test@test.com', nome='Test User', tipo='cliente')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()
    
    response = client.post('/auth/login', data={
        'email': 'test@test.com',
        'password': 'password'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Meu Perfil' in response.data 