import pytest
from  api import create_app, db
from  api.config import TestingConfig
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from api.users.routes import users


@pytest.fixture(scope="module")
def context():
    flask_app = create_app(TestingConfig)
    db.create_all()
    testing_client = flask_app.test_client()
    ctx = flask_app.app_context()
    ctx.push()
    yield ctx
    ctx.pop()
    db.drop_all()

@pytest.fixture
def test_app():
    app = create_app(TestingConfig)
    db.create_all()
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client, db
            db.drop_all()

@pytest.fixture(scope="module")
def test_client():
    app = create_app(TestingConfig)
    with app.app_context():
        client = app.test_client()
        db.create_all()
        yield client
        db.drop_all()
# def test_client():
    # app = create_app(TestingConfig)
    # client = app.test_client()
    # ctx = app.test_request_context()
    # db.create_all()
    # ctx.push()
    # yield client
    # ctx.pop()
    # db.drop_all()

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

@pytest.fixture(scope="module")
def email_fixture():
    emails = {
        "success": {
            "email": "jello@mail.com",
            "result" : True
        }
    }
    return emails

@pytest.fixture(scope="module")
def email_value_error_fixture():
    emails = {
        "null_email": {
            "email": ''
        },
        "invalid_email": {
            "email": "jellomailcom"
        }
    }
    return emails
@pytest.fixture(scope="module")
def phone_fixture():
    num ={
        "success": {
            "phone_number": "1 (555) 555-5555",
            "result" : True
        }
    }
    return num
@pytest.fixture(scope="module")
def phone_value_error_fixture():
    num ={
        "null_phone_number": {
            "phone_number": ''
        },
        "missing_space": {
            "phone_number": "1(123)456-7890"
        },
        "invalid_format": {
            "phone_number": "12345609779"
        },
        "invalid_phone_number2": {
            "phone_number": "234567890"
        },
        'invalid_char': {
            "phone_number": "1(123) 456-789O"
        },
    }
    return num

@pytest.fixture(scope="module")
def name_fixture():
    names = {
        "success": {
            "name": "Atestname",
            "result" : True,
            "db_return": None
        },
    }
    return names

@pytest.fixture(scope="module")
def name_value_error_fixture():
    names = {
        "name_exists": {
            "name": "Atestname",
            "result" : False,
            "db_return": {}
        },
        "name_too_long": {
            "name": "Atestname"*10,
            "result" : False,
            "db_return": {}
        },
    }
    return names

@pytest.fixture(scope="module")
def get_response_fixture():
    rec = {
        "success": {
            "route": "/",
            "status_code": 200,
            "request_body": {}, 
            "expected_response": {},
            "verb": "GET"
        }
    }
    return rec
@pytest.fixture(scope="module")
def users_to_load():
    data = [
    {
        "username": "test user one",
        "password": "password",
        "phone_number": "1 (234) 567-1890",
        "email": "one@e.mail"
        },
        {
        "username": "test user two",
        "password": "password",
        "phone_number": "1 (234) 567-1890",
        "email": "two@ma.il"
        },
        {
        "username": "test user three",
        "password": "password",
        "phone_number": "1 (234) 567-1890",
        "email": "three@ma.il"
        }
    ]
    return data

@pytest.fixture(scope="module")
def username_password():
    data = {
    "wrong_password":{
        "body": {
            "username": "test user one",
            "password": "wrong_password",
            "mfa_method": "sms"
        },
        "status_code": 400 
        },
    "wrong_username":{
        "body":{
            "username": "wrong username",
            "password": "password",
            "mfa_method": "sms"
        },
        "status_code": 400
        },
        "success":{
        "body":{
            "username": "test user one",
            "password": "password",
            "mfa_method": "sms"
            },
        "status_code": 200
    },
    }
    return data

@pytest.fixture(scope="module")
def update_user_fixture():
     data ={
         "user1": {
        "username": "user",
        "password": "password",
        "phone_number": "1 (234) 567-1890",
        "email": "one@e.mail"
            },
        "user2": {
        "username": "test",
        "password": "new_password",
        "phone_number": "1 (555) 567-1890",
        "email": "twsdfso@ma.il"
        }
     }
     return data
@pytest.fixture(scope="module")
def delete_user_fixture():
    data ={
        "user1": {
        "username": "user delete",
        "password": "password",
        "phone_number": "1 (234) 567-1890",
        "email": "enm@mail.com"
            },
        "user2": {
        "username": "test delete", 
        "password": "new_password", 
        "phone_number": "1 (555) 567-1890",
        "email": "email@mail.com"
        }
    }   
    return data