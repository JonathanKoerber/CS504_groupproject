# Description: This file contains the data model for the database.
from api import db
import base64
from datetime import datetime, timedelta
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
    

    