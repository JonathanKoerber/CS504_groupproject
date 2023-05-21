from sqlalchemy import create_engine, text
from flask import Blueprint, request, jsonify
from api.users.utils import validate_string, validate_email, salt_password, confirm_authentication, generate_pin, compare_pin, send_email, get_user_email, is_account_created, get_user

from sqlalchemy import insert, update, delete
import time

from api.data_model import User


users = Blueprint('users', __name__)

'''
Display all users
'''
@users.route('/')
def index():
    users = {}
    query = text("SELECT * FROM users")
    engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/CS_504_PROJECT')    
    with engine.connect() as con:
        rs = con.execute(query)
        for row in rs:
            users[row[0]] = [i for i in row[1:]]
    return jsonify(users), 200
'''
Authenticate user
'''
@users.route('/login', methods=['GET'])
def login():
    is_authenticated = False
    re = request.get_json()
    username = re['username']
    password = re['password'] 
    try:
        validate_string(username)
        validate_string(password)

        engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/CS_504_PROJECT')
        query = text("SELECT * FROM users WHERE username = :username AND password = :password ")
    
        with engine.connect() as con:
            rs = con.execute(query, {"username": username, "password": password})
        if rs.fetchone() is not None:
            is_authenticated = True
            confirm_authentication(is_authenticated)
            user_email = get_user_email(username)
            pin = generate_pin()
            send_email(user_email, pin)
            user_pin = input("Enter 4 digit pin that was sent to your email/phone number: ")
            compare_pin(pin, user_pin)
            return jsonify({'username': username, 'password': password}), 200
        else:
            is_authenticated = False
            confirm_authentication(is_authenticated)
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 400


'''
Add user to database
'''
@users.route('/users', methods=['POST'])
def post_users_details():
    username = input("Enter your username: ")
    email = input("Enter email address:  ")
    password = input("Enter your password: ")
    telephone = input("Enter your phone number: ")

    validate_string(username)
    validate_string(password)
    validate_email(email)

    engine = create_engine('mysql+mysqlconnector://root:root@localhost:6603/CS_504_PROJECT')

    """Because we are not using the auto-increment option for the user ID in the db,
    we should count the number of users in the table to get the ID-value of the last user 
    stored in the table"""
    conn_count = engine.connect()
    count_query = text("SELECT count(*) FROM users")
    exec_count = conn_count.execute(count_query)
    column_count = exec_count.scalar()

    #print(f"Number of users: {column_count}")
    user_id = int(column_count)
    user_id = user_id + 1

    #print(F"Next ID: {user_id}")

    # run the insert query
    query = text(
        "INSERT INTO users(id, username, email, password, telephone) VALUES(:id, :username, :email, :password, :telephone)")

    user_data = {"id": user_id, "username": username, "password": password, "email": email, "telephone": telephone}

    with engine.connect() as conn:
        conn.execute(query, user_data)
        is_created = is_account_created(username)
        if is_created:
            print("Account successfully created!")
        else:
            print("Unable to create account. Try again...")

    #     return 'Success', 200
    # except Exception as e:
    #     print("Error during saving object ", e)
    #     return 'Failed', 400


'''
Update user to database
'''
@users.route('/users', methods=['PUT'])
def put_users_details():
    # Update user details
    # Get user input
    user_input = int(input(
        "Enter \n1 to change username, \n2 to change password, \n3 to change email, \n4 to change phone number: \n"))

    print("Login to make the changes.\n")

    username = get_user()

    old_username = username

    username = ""

    engine = create_engine('mysql+mysqlconnector://root:root@localhost:6603/CS_504_PROJECT')

    if user_input == 1:
        username = input("Enter new username: ")
        validate_string(username)
        update_query = text(
            "UPDATE CS_504_PROJECT.users SET username = '" + username + "' WHERE username = '" + old_username + "'")
        user_data_update = {"useranem": username}
        with engine.connect() as conn:
            rs = conn.execute(update_query, user_data_update)
    elif user_input == 2:
        password = input("Enter new password: ")
        validate_string(username)
        update_query = text(
            "UPDATE CS_504_PROJECT.users SET password = '" + password + "' WHERE username = '" + old_username + "'")
        user_data_update = {"useranem": username}
        with engine.connect() as conn:
            rs = conn.execute(update_query, user_data_update)
    elif user_input == 3:
        email = input("Enter new email: ")
        validate_email(email)
        update_query = text(
            "UPDATE CS_504_PROJECT.users SET email = '" + email + "' WHERE username = '" + old_username + "'")
        user_data_update = {"useranem": username}
        with engine.connect() as conn:
            rs = conn.execute(update_query, user_data_update)
    elif user_input == 4:
        telephone = input("Enter new phone number: ")
        update_query = text(
            "UPDATE CS_504_PROJECT.users SET telephone = '" + telephone + "' WHERE username = '" + old_username + "'")
        user_data_update = {"useranem": username}
        with engine.connect() as conn:
            rs = conn.execute(update_query, user_data_update)
    # try:
    #     pass
    # except Exception as e:
    #     print("Error during saving object ", e)
    #     return 'Failed', 400

'''
Delete user from database
'''
@users.route('/users/<name>', methods=['DELETE'])
def delete_users_details(name):
    # Get user input
    print("Login to make the changes.\n")

    username = get_user()

    print(f"User name: {username}")

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if not validate_string(username) or not validate_string(password):
        raise ValueError("Username or password should not exceed 255 characters")

    #   Create SQL query to check the user's login credentials
    query = text("DELETE FROM CS_504_PROJECT.users WHERE username = :username")

    # Connect to the database and execute the query
    engine = create_engine('mysql+mysqlconnector://root:root@127.0.0.1:6603/CS_504_PROJECT')
    with engine.connect() as conn:
        result = conn.execute(query, {"username": username})
    # try:
    #     pass
    # except KeyError:
    #     return 'Record Not Found', 404
    # except Exception as e:
    #     print("Error during removing object ", e)
    #     return 'Error while removing record', 400

