import pytest
from  api import create_app, db
from  api.config import TestingConfig
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app(TestingConfig)
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()

@pytest.fixture
def test_app():
    app = create_app(TestingConfig)
    
    #os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client, db

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope="module")
def users_fixture():
    users = {
        "success": {
            "username": "testuser",
            "password": "testpass",
            "email": "testuser@test.com",
            "phone_number": "1234567890",
            "result" : True
        },
        "null_username": {  
            "username": None,   
            "password": "testpass",
            "email": "null_username@test.com",
            "phone_number": "1234567890",
            "result" : False
        },
        "null_password": {
            "username": "null_password",
            "password": None,
            "email": "null_password@pass.com",
            "phone_number": "1234567890",
            'result' : False
        },
        "null_email": {
            "username": "null_email",
            "password": "testpass",
            "email": None,
            "phone_number": "1234567890",
            "result" : False
        }, 
        "null_phone_number": {
            "username": "null_phone_number",
            "password": "testpass", 
            "email": "null_phone@number.com",
            "phone_number": None,
            "result" : False
        },
        'non_unique_username': {
            "username": "testuser",
            "password": "testpass",
            "email": "non_unique@unsername.com",
            "phone_number": "1234567890",
            "result" : False
        }, 
        "non_unique_email": {
            "username": "non_unique_email",
            "password": "testpass",
            "email": "testuser@test.com",
            "phone_number": "1234567890",
            "result" : False

        }
    }
    return users
