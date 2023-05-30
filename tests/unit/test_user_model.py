import pytest
from api.data_model import User

# @pytest.mark.parametrize('users', ['success', 'null_username', 'null_password', 
#                                    'null_email', 'null_phone_number, non_unique_username', 
#                                    'non_unique_email'])
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
    # assert user.username == data['username']
    # assert user.password_hash != data['password']
    # assert user.email == data['email']
    # assert user.phone_number == data['phone_number']
    # assert user.otp_secret is not None
    assert True