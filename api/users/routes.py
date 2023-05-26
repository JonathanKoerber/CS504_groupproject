import sqlalchemy
from sqlalchemy import create_engine, text
from flask import Blueprint, request, jsonify
from flask_mail import Message, Mail
from api.users.utils import validate_name, validate_passowrd, validate_email, send_pin_email
from api import db, mail
from api.data_model import User
from api.users.mfa import request_verification_token, check_verification_token
import os

users = Blueprint('users', __name__)

'''
Display all users
'''
@users.route('/')
def index():
    users = {}
    query = text("SELECT * FROM users")
    engine = db.get_engine()   
    with engine.connect() as con:
        rs = con.execute(query)
        for row in rs:
            users[row[0]] = [i for i in row[1:]]
    return jsonify(users), 200
'''
Authenticate user return pin and sent email for verification
'''
@users.route('/login', methods=['GET'])
def login():
    rsp = request.get_json()
    username = rsp['username']
    password = rsp['password'] 
    mfa_method = rsp['mfa_method']
    print(username, password , mfa_method  )   
    try:
        validate_name(username)
        validate_passowrd(password)

        user = User.query.filter_by(username=username).first()
        print('user: ', user)
        #if user is not None and validate_passowrd(user.password):
        if user is not None and user.verify_password(password):
            phone_number = os.environ.get('PHONE_NUMBER')
            request_verification_token(phone_number)
        else:
            return jsonify({"error":"Invalid username or password!"}), 400
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    return jsonify({'message': 'Please check you {}'.format(mfa_method), 'id': user.id}), 200

'''
verify user pin and token
TODO need a way to verify the pin
maybe a temporary storage for the pin
'''
@users.route('/login_mfa', methods=['GET'])
def login_mfa():
    rsp = request.get_json()
    pin = rsp['pin']
    username = rsp['username']
    
    user = User.query.filter_by(username=username).first()

    try:
        mfa_rsp = check_verification_token(os.environ.get('PHONE_NUMBER'), pin)
        
    except ValueError as e:
        print('error check verification token', e)
        return jsonify({"error": str(e)}), 400
    print('mfa_rsp: ', mfa_rsp.status)
    if mfa_rsp == 'approved':
        return jsonify({'message': 'Login successful', 'id': user.id, 'user': username}), 200
    if mfa_rsp == 'pending' or mfa_rsp == 'denied':
        return jsonify({'message': 'Login pin verification failed please try to renter you pin'}), 400
    return jsonify({'message': 'Login pin verification failed try to login again'}), 400
'''
Add user to database
'''
@users.route('/users', methods=['POST'])
def post_users_details():
    re = request.get_json()    
    username = re['username']
    password = re['password']
    email = re['email']
    try:
        user = User.query.filter_by(username=username).first()
        if user:
            print('user not null')
            raise ValueError("User already exists")
        validate_name(username)
        validate_passowrd(password)
        validate_email(email)
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 200
     
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400
'''
Update user to database
'''
    
@users.route('/users/', methods=['PUT'])
def put_users_by_id_details():
    re = request.get_json()    
    id = re['id']
    username = re['username']
    password = re['password']
    email = re['email']
   
    try:
        validate_email(email)
        validate_name(username)
        validate_passowrd(password)

        user = User.query.filter_by(id=id).first()
        if not user:
            raise ValueError("User does not exist")
        user.password = password if password else user.password
        user.email = email if email else user.email
        user.username = username if username else user.username
    
        db.session.add(user)
        db.session.commit()
        update_user = User.query.filter_by(id=id).first()
        return update_user.to_json(), 200
    except Exception as e:
        print("Error during saving object ", e)
        return 'Failed', 400
'''
Delete user from database
'''
@users.route('/users/', methods=['DELETE'])
def delete_users():
    re = request.get_json()
    id = username = None
    print(re)
    if 'id' in re:
        id = re['id']
    if 'username' in re:
        username = re['username']
    
    try:
        if username:
            user = User.query.filter_by(username=username).first()
        if id:
            user = User.query.filter_by(id=id).first()
        if not user:
            raise ValueError("User does not exist")
        db.session.delete(user)
        db.session.commit()
        return 'Success', 200
    except sqlalchemy.exc.SQLAlchemyError as e:
        print(e)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400

