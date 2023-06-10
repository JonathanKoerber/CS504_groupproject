import pytest
from api import create_app, db
from api.config import TestingConfig


@pytest.fixture(scope="module")
def test_client():
    """
    Flask provides a way to test your application by exposing the Werkzeug test Client
    """
    app = create_app(TestingConfig)
    with app.app_context():
        client = app.test_client()
        db.create_all()
        yield client
        db.drop_all()


@pytest.fixture(scope="module")
def users_fixture():
    """
    Fixture to test the User model
    """
    users = {
        "success": {
            "username": "testuser",
            "password": "testpass",
            "email": "testuser@test.com",
            "phone_number": "1234567890",
            "result": True,
        },
        "null_username": {
            "username": None,
            "password": "testpass",
            "email": "null_username@test.com",
            "phone_number": "1234567890",
            "result": False,
        },
        "null_password": {
            "username": "null_password",
            "password": None,
            "email": "null_password@pass.com",
            "phone_number": "1234567890",
            "result": False,
        },
        "null_email": {
            "username": "null_email",
            "password": "testpass",
            "email": None,
            "phone_number": "1234567890",
            "result": False,
        },
        "null_phone_number": {
            "username": "null_phone_number",
            "password": "testpass",
            "email": "null_phone@number.com",
            "phone_number": None,
            "result": False,
        },
        "non_unique_username": {
            "username": "testuser",
            "password": "testpass",
            "email": "non_unique@unsername.com",
            "phone_number": "1234567890",
            "result": False,
        },
        "non_unique_email": {
            "username": "non_unique_email",
            "password": "testpass",
            "email": "testuser@test.com",
            "phone_number": "1234567890",
            "result": False,
        },
    }
    return users


@pytest.fixture(scope="module")
def email_fixture():
    """
    Fixture to test the email validation
    """
    emails = {"success": {"email": "jello@mail.com", "result": True}}
    return emails


@pytest.fixture(scope="module")
def email_value_error_fixture():
    """
    Fixture to test the email validation
    """
    emails = {"null_email": {"email": ""}, "invalid_email": {"email": "jellomailcom"}}
    return emails


@pytest.fixture(scope="module")
def phone_fixture():
    """
    Fixture to test the phone number validation
    """
    num = {"success": {"phone_number": "1 (555) 555-5555", "result": True}}
    return num


@pytest.fixture(scope="module")
def phone_value_error_fixture():
    """
    Fixture to test the phone number validation
    """
    num = {
        "null_phone_number": {"phone_number": ""},
        "missing_space": {"phone_number": "1(123)456-7890"},
        "invalid_format": {"phone_number": "12345609779"},
        "invalid_phone_number2": {"phone_number": "234567890"},
        "invalid_char": {"phone_number": "1(123) 456-789O"},
    }
    return num


@pytest.fixture(scope="module")
def name_fixture():
    """
    Fixture to test the name validation
    """
    names = {
        "success": {"name": "Atestname", "result": True, "db_return": None},
    }
    return names


@pytest.fixture(scope="module")
def name_value_error_fixture():
    """
    Fixture to test the name validation
    """
    names = {
        "name_exists": {"name": "Atestname", "result": False, "db_return": {}},
        "name_too_long": {"name": "Atestname" * 10, "result": False, "db_return": {}},
    }
    return names


@pytest.fixture(scope="module")
def get_response_fixture():
    """
    Fixture to test the get response
    """
    rec = {
        "success": {
            "route": "/",
            "status_code": 200,
            "request_body": {},
            "expected_response": {},
            "verb": "GET",
        }
    }
    return rec


@pytest.fixture(scope="module")
def users_to_load():
    """
    
    fixture to load users into the database
    """
    data = [
        {
            "username": "test user one",
            "password": "password",
            "phone_number": "1 (234) 567-1890",
            "email": "one@e.mail",
        },
        {
            "username": "test user two",
            "password": "password",
            "phone_number": "1 (234) 567-1890",
            "email": "two@ma.il",
        },
        {
            "username": "test user three",
            "password": "password",
            "phone_number": "1 (234) 567-1890",
            "email": "three@ma.il",
        },
    ]
    return data


@pytest.fixture(scope="module")
def username_password():
    """
    Fixture to test the username and password validation    
    """
    data = {
        "wrong_password": {
            "body": {
                "username": "test user one",
                "password": "wrong_password",
                "mfa_method": "sms",
            },
            "status_code": 400,
        },
        "wrong_username": {
            "body": {
                "username": "wrong username",
                "password": "password",
                "mfa_method": "sms",
            },
            "status_code": 400,
        },
        "success": {
            "body": {
                "username": "test user one",
                "password": "password",
                "mfa_method": "sms",
            },
            "status_code": 200,
        },
    }
    return data


@pytest.fixture(scope="module")
def update_user_fixture():
    """
    Fixture to test the update user endpoint
    """
    data = {
        "user1": {
            "username": "user",
            "password": "password",
            "phone_number": "1 (234) 567-1890",
            "email": "one@e.mail",
        },
        "user2": {
            "username": "test",
            "password": "new_password",
            "phone_number": "1 (555) 567-1890",
            "email": "twsdfso@ma.il",
        },
    }
    return data


@pytest.fixture(scope="module")
def delete_user_fixture():
    """
    Fixture to test the delete user endpoint
    """
    data = {
        "user1": {
            "username": "user delete",
            "password": "password",
            "phone_number": "1 (234) 567-1890",
            "email": "enm@mail.com",
        },
        "user2": {
            "username": "test delete",
            "password": "new_password",
            "phone_number": "1 (555) 567-1890",
            "email": "email@mail.com",
        },
    }
    return data

@pytest.fixture(scope="module")
def create_user_fixture():
    """
    Fixture to test the create user endpoint
    """
    data = {    
        "user1": {
            "username": "user create",
            "password": "password",
            "phone_number": "1 (234) 567-1890",
            "email": "email@mail.com"
        },
        "user2": {  
            "username": "test create",
            "password": "new_password",
            "phone_number": "1 (555) 567-1890",
            "email": "mial@e.com"
        }
    }
    return data
