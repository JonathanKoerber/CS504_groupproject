'''
Unit test to test the User model
'''
import os
import pytest
from api import db, create_app
from api.data_model import User
from sqlalchemy.exc import OperationalError

@pytest.mark.parametrize('users', ['success'])
def test_new_user(users_fixture, users):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, password, email, phone_number, and otp_secret fields are defined correctly
    """
    data = users_fixture[users]
    user = User(
        username=data['username'],
        password=data["password"],
        email=data["email"],
        phone_number=data["phone_number"],
    )
    assert user.username == data['username']
    assert user.password_hash != data['password']
    assert user.email == data['email']
    assert user.phone_number == data['phone_number']
    assert user.otp_secret is not None

@pytest.mark.xfail(raises=OperationalError)
@pytest.mark.parametrize('users', ['null_username', 'null_email', 'null_phone_number',
                                   'non_unique_email', 'non_unique_username'])
def test_new_user_raises_error(users_fixture, users, test_app):
    """
    GIVEN a User model
    WHEN a new User is created with a null username, password, email, phone_number, or non-unique username or email
    THEN check that an error is raised
    """
    data = users_fixture[users]
    client, db = test_app
    user = User(
        username=data['username'],
        password=data["password"],
        email=data["email"],
        phone_number=data["phone_number"],
    )
    db.session.add(user)
    try:
        db.session.commit()
    except OperationalError:
        db.session.rollback()
   
@pytest.mark.parametrize('users', ['success'])
def test_password_hashing(users_fixture, users):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the password is hashed
    """
    data = users_fixture[users]
    user = User(
        username=data['username'],
        password=data["password"],
        email=data["email"],
        phone_number=data["phone_number"],
    )
    assert user.password_hash != data['password']

@pytest.mark.parametrize('users', ['success'])
def test_password_verification(users_fixture, users):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the password is verified
    """
    data = users_fixture[users]
    user = User(
        username=data['username'],
        password=data["password"],
        email=data["email"],
        phone_number=data["phone_number"],
    )
    assert user.verify_password(data['password']) is True

@pytest.mark.parametrize('users', ['success'])
def test_password_salts_are_random(users_fixture, users):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the password salt is random
    """
    data = users_fixture[users]
    user_one = User(
        username=data['username'],
        password=data["password"],
        email=data["email"],
        phone_number=data["phone_number"],
    )
    user_two = User(
        username=data['username'],
        password=data["password"],
        email=data["email"],
        phone_number=data["phone_number"],
    )
    
    assert user_one.password_hash != user_two.password_hash





