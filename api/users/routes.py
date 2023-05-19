from flask import Blueprint, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required   
from api.data_model import User


users = Blueprint('users', __name__)


@users.route('/login', methods=['POST'])
def login():
    request = request.get_json()
    email = request.get('email')
    password = request.get('password')

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

