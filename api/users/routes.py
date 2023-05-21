import sqlalchemy
from sqlalchemy import create_engine, text
from flask import Blueprint, request, jsonify
from api.users.utils import validate_name, validate_passowrd, validate_email, salt_password
from api import db
from api.data_model import User

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
Authenticate user
'''
@users.route('/login', methods=['GET'])
def login():
    rsp = request.get_json()
    username = rsp['username']
    password = rsp['password'] 
    try:
        validate_name(username)
        validate_passowrd(password)

        engine  = db.get_engine()
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
Add user to databasefl
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

