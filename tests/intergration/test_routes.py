"""
Intergration tests
Make HTTP requests test_client
"""

import pytest
from unittest.mock import patch
from api.users.routes import users
from api.data_model import User
from flask import jsonify


def test_get_users(users_to_load, test_client):
    """
    adds users to db
    requests users from db
    """
    with test_client.application.app_context():
        for user in users_to_load:
            response = test_client.post("/users", json=user)
            assert response.status_code == 200

        response = test_client.get("/")
        assert response.status_code == 200


@pytest.mark.parametrize("usr_pass", ["success", "wrong_password", "wrong_username"])
def test_get_login(usr_pass, username_password, test_client):
    """
    Request login form
    """
    data = username_password[usr_pass]
    with test_client.application.app_context():
        with patch("api.users.routes.request_verification_token") as mock_request:
            response = test_client.get("/login", json=data["body"])
            assert response.status_code == username_password[usr_pass]["status_code"]
            if response.status_code == 200:
                assert mock_request.called == True

def test_sql_injection(test_client):
    '''
    Test sql injection
    '''
    with test_client.application.app_context():
        response = test_client.get("/login", json={"username": "test user one", "password": "password' OR '1'='1", "mfa_method": "sms"})
        print(response.data)
        assert response.status_code == 400
        assert response.data == b'{\n  "error": "Invalid username or password!"\n}\n'

# def test_get_login_mfa(test_client):
#     '''
#     Test longin_mfa route
#     make sure that pin in verifed it returns 200
#     '''
#     class mock_response:
#         status = 'approved'

#     with test_client.application.app_context():

#         with patch('api.users.mfa.check_verification_token') as mock_check:
#             mock_check.return_value = mock_response()
#         response = test_client.get('/login_mfa', json={'pin': '123456', 'username': 'test user one'})
#         assert response.status_code == 200
#         assert mock_check.called == True



@pytest.mark.parametrize("user", ["user1", "user2"])
def test_create_user(user, create_user_fixture, test_client):
    """
    Test create user route
    check that users that are created are in the db
    test for sql injection
    """
    with test_client.application.app_context():
        response = test_client.post("/users", json=create_user_fixture[user])
        assert response.status_code == 200


def test_update_user(test_client, update_user_fixture):
    """
    Test update user route
    """
    update_user = update_user_fixture["user2"]
    with test_client.application.app_context():
        rsp_one = test_client.post("/users", json=update_user_fixture["user1"])
        id = rsp_one.data[1]
        update_user["id"] = id
        rsp_two = test_client.put("/users", json=update_user)
        assert rsp_one.status_code == 200
        assert rsp_two.status_code == 308

        assert rsp_one.data[3] != rsp_two.data[3]


def test_delete_user(test_client, delete_user_fixture):
    """
    Test delete user route

    """
    with test_client.application.app_context():
        create_one = test_client.post("/users", json=delete_user_fixture["user1"])
        id = create_one.data[1]
        delete_one = test_client.delete("/users", json={"id": id})
        create_two = test_client.post("/users", json=delete_user_fixture["user2"])
        user_name = create_two.data[3]
        delete_two = test_client.delete("/users", json={"username": user_name})
        assert create_one.status_code == 200
        assert delete_one.status_code == 308
        assert create_two.status_code == 200
        assert delete_two.status_code == 308
