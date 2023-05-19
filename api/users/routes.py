from sqlalchemy import create_engine, text
from flask import Blueprint, request, jsonify
from api.users.utils import validate_string, validate_email, salt_password


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
    re = request.get_json()
    username = re['username']
    password = re['password'] 
    try:
        validate_email(username)
        validate_string(password)

        engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/CS_504_PROJECT')
        query = text("SELECT * FROM users WHERE username = :username AND password = :password ")
    
        with engine.connect() as con:
            rs = con.execute(query, {"username": username, "password": password})
        if rs.fetchone() is not None:
            print("Login successful!")
        else:
            print("Invalid username or password!")
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    return jsonify({'username': username, 'password': password}), 200


'''
Add user to database
'''
@users.route('/users', methods=['POST'])
def post_users_details():
    try:
        pass
        return 'Success', 200
    except Exception as e:
        print("Error during saving object ", e)
        return 'Failed', 400
'''
Update user to database
'''
@users.route('/users', methods=['PUT'])
def put_users_details():
    try:
        pass
    except Exception as e:
        print("Error during saving object ", e)
        return 'Failed', 400

'''
Delete user from database
'''
@users.route('/users/<name>', methods=['DELETE'])
def delete_users_details(name):
    try:
        pass
    except KeyError:
        return 'Record Not Found', 404
    except Exception as e:
        print("Error during removing object ", e)
        return 'Error while removing record', 400

