'''
Unit test for utils.py
'''
import pytest
from unittest.mock import patch
import os
from api.users.utils import validate_email, validate_phone_number, validate_name

@pytest.mark.parametrize('target', ['success'])
def test_validate_email(target, email_fixture):
    """
    GIVEN a valid email
    WHEN the validate_email function is called
    THEN check that the email is valid
    """
    arg = email_fixture[target]
    assert validate_email(arg['email']) is arg['result']

@pytest.mark.parametrize('phone_number', ['success'])
def test_valiate_phone_number(phone_number, phone_fixture):
    """
    GIVEN a valid phone number
    WHEN the validate_phone_number function is called
    THEN check that the phone number is valid
    """
    number = phone_fixture[phone_number]
    assert validate_phone_number(number['phone_number']) is number['result']

@pytest.mark.xfail(raises=ValueError)
@pytest.mark.parametrize('phone_number', ['null_phone_number', 'missing_space', 'invalid_format', 'invalid_phone_number2', 'invalid_char'])
def test_invalid_phone_number_raise_error(phone_number, phone_value_error_fixture):
    """
    GIVEN a valid phone number
    WHEN the validate_phone_number function is called
    THEN check that the phone number is valid
    """
    data = phone_value_error_fixture[phone_number]
    try:
        validate_phone_number(data['phone_number'])
    except ValueError:
        assert True
        return
  

@pytest.mark.parametrize('name', ['success'])
def test_validate_name(name, name_fixture, test_client):
    """
    GIVEN a valid phone number
    WHEN the validate_phone_number function is called
    THEN check that the phone number is valid
    Mocks User.query.filter_by(username=username).first() to return None
    """
    
    data = name_fixture[name]
    with test_client.application.app_context():
        with patch ('api.data_model.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = data['db_return']
            assert validate_name(data['name']) is data['result']

@pytest.mark.xfail(raises=ValueError)
@pytest.mark.parametrize('name', ['name_exists', 'name_too_long'])
def test_validate_name_raise_error(name, name_value_error_fixture, test_client):
    """
    GIVEN a valid phone number
    WHEN the validate_phone_number function is called
    THEN check that the phone number is valid
    Mocks User.query.filter_by(username=username).first() to return None
    """
    
    data = name_value_error_fixture[name]
    with test_client.application.app_context():
        with patch ('api.data_model.User.query') as mock_query:
            mock_query.filter_by.return_value.first.return_value = data['db_return']
            validate_name(data['name'])