from sqlalchemy import create_engine, text
from flask import Blueprint, request, jsonify


users = Blueprint('users', __name__)

@users.route('/login', methods=['GET'])
def login():
    
    re = request.get_json()
    username = re['username']
    password = re['password']
    try:
        # utils.validate_string(username)
        # utils.validate_string(password)
        engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/dbe')
        query = text("SELECT * FROM users WHERE username = :username AND password = :password ")
    
        with engine.connect() as con:
            rs = con.execute(query, {"username": username, "password": password})
        if rs.fetchone() is not None:
            print("Login successful!")
        else:
            print("Invalid username or password!")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({'username': username, 'password': password}), 200

@users.route('/')
def index():
    return 'Hello World!'

@users.route('/users', methods=['POST'])
def post_users_details():
    try:
        pass
        return 'Success', 200
    except Exception as e:
        print("Error during saving object ", e)
        return 'Failed', 400

@users.route('/users', methods=['PUT'])
def put_users_details():
    try:
        pass
    except Exception as e:
        print("Error during saving object ", e)
        return 'Failed', 400

@users.route('/users/<name>', methods=['GET'])
def get_users_details(name):
    try:
     pass
    except KeyError:
        return 'Record Not Found', 400
    
@users.route('/users/<name>', methods=['DELETE'])
def delete_users_details(name):
    try:
        pass
    except KeyError:
        return 'Record Not Found', 404
    except Exception as e:
        print("Error during removing object ", e)
        return 'Error while removing record', 400

