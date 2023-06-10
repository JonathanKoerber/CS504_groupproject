"""
difine all the routes for the users
"""
import sqlalchemy
from flask import Blueprint, request, jsonify
from api import db
from api.users.utils import (
    validate_name,
    validate_passowrd,
    validate_email,
    validate_phone_number,
)
from api.data_model import User
from api.users.mfa import request_verification_token, check_verification_token


users = Blueprint("users", __name__)

"""
Display all users
"""


@users.route("/")
def index():
    """
    Returns all users
    """
    current_users = User.query.all()
    current_users = [user.to_dict() for user in current_users]  # convert to dict
    return jsonify(current_users), 200


@users.route("/login", methods=["GET"])
def login():
    """
    Authenticate user return pin and sent email for verification
    """
    rsp = request.get_json()
    print("login", rsp)
    username = rsp["username"]
    password = rsp["password"]
    mfa_method = rsp["mfa_method"]

    try:
        #
        validate_passowrd(password)

        user = User.query.filter_by(username=username).first()

        # if user is not None and validate_passowrd(user.password):
        if user is not None and user.verify_password(password):
            print("user: ", user, user.verify_password(password))
            phone_number = user.phone_number
            request_verification_token(phone_number)
        else:
            return jsonify({"error": "Invalid username or password!"}), 400
    except ValueError as error:
        print(error)
        return jsonify({"error": str(error)}), 400
    return (
        jsonify({"message": "Please check you {}".format(mfa_method), "id": user.id}),
        200,
    )


@users.route("/login_mfa", methods=["GET"])
def login_mfa():
    """
    Authenticate user return pin and sent email for verification
    """
    rsp = request.get_json()
    pin = rsp["pin"]
    username = rsp["username"]

    user = User.query.filter_by(username=username).first()
    print("user: ", user)
    try:
        mfa_rsp = check_verification_token(user.phone_number, pin)

    except ValueError as value_error:
        print("error check verification token", value_error)
        return jsonify({"error": str(value_error)}), 400
    if mfa_rsp == "approved":
        return (
            jsonify({"message": "Login successful", "id": user.id, "user": username}),
            200,
        )
    if mfa_rsp == "pending" or mfa_rsp == "denied":
        return (
            jsonify(
                {
                    "message": "Login pin verification failed please try to renter you pin"
                }
            ),
            400,
        )
    return jsonify({"message": "Login pin verification failed try to login again"}), 400


@users.route("/users", methods=["POST"])
def post_users_details():
    """
    Add user to database
    """
    user_request = request.get_json()
    username = user_request["username"]
    password = user_request["password"]
    phone_number = user_request["phone_number"]
    email = user_request["email"]
    try:
        user = User.query.filter_by(username=username).first()
        if user:
            raise ValueError("User already exists")
        validate_name(username)
        validate_passowrd(password)
        validate_email(email)
        validate_phone_number(phone_number)
        user = User(
            username=username, password=password, email=email, phone_number=phone_number
        )
        db.session.add(user)
        db.session.commit()

        return jsonify(user.to_dict()), 200
    except ValueError as value_error:
        print(value_error)
        return jsonify({"error": str(value_error)}), 400
    except sqlalchemy.exc.SQLAlchemyError as value_error:
        print(value_error)
        return jsonify({"error": str(value_error)}), 400


@users.route("/users/", methods=["PUT"])
def put_users_by_id_details():
    """
    Update user details
    """
    user_request = request.get_json()
    user_id = user_request["id"]
    username = user_request["username"]
    password = user_request["password"]
    email = user_request["email"]
    phone_number = user_request["phone_number"]

    try:
        validate_email(email)
        validate_name(username)
        validate_passowrd(password)
        validate_phone_number(phone_number)

        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise ValueError("User does not exist")
        user.password = password if password else user.password
        user.email = email if email else user.email
        user.username = username if username else user.username
        user.phone_number = phone_number if phone_number else user.phone_number

        db.session.add(user)
        db.session.commit()
        update_user = User.query.filter_by(id=user_id).first()
        return update_user.to_json(), 200
    except ValueError as value_error:
        print(value_error)
        return jsonify({"error": str(value_error)}), 400
    except sqlalchemy.exc.SQLAlchemyError as sql_error:
        print(sql_error)
        return jsonify({"error": str(sql_error)}), 400


@users.route("/users/", methods=["DELETE"])
def delete_users():
    """
    Delete user by id or username
    """
    user_request = request.get_json()
    user_id = username = None
    if "id" in user_request:
        user_id = user_request["id"]
    if "username" in user_request:
        username = user_request["username"]

    try:
        if username:
            user = User.query.filter_by(username=username).first()
        if user_id:
            user = User.query.filter_by(id=user_id).first()
        if not user:
            raise ValueError("User does not exist")
        db.session.delete(user)
        db.session.commit()
        return "Success", 200
    except sqlalchemy.exc.SQLAlchemyError as sql_error:
        return jsonify({"error": str(sql_error)}), 400

