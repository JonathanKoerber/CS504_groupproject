# Description: This file contains the data model for the database.
from api import db
import base64
from datetime import datetime
from flask_login import UserMixin
from flask_authorize import (
    RestrictionsMixin,
    AllowancesMixin,
    PermissionsMixin,
    OwnerPermissionsMixin,
)
from werkzeug.security import generate_password_hash, check_password_hash

import secrets
import os
from flask import current_app
import jwt


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    otp_secret = db.Column(db.String(16), nullable=False, default=secrets.token_hex(16))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            self.otp_secret = base64.b32encode(os.urandom(10))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = jwt.encode(
            {
                "confirm": self.id,
                "exp": datetime.utcnow() + datetime.timedelta(seconds=expires_sec),
            },
            self.otp_secret,
            algorithm="HS256",
        )
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(self, token):
        try:
            data = jwt.decode(
                token,
                self.otp_secret,
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"],
            )
        except:
            return False
        if data.get("confirm") != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    """return a json object of the user data"""

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "phone": self.phone_number,
            "email": self.email,
        }

    def __repr__(self):
        return f"User('{self.username}', '{self.email}'. '{self.phone_number}')"
