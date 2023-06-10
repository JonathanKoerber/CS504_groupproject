"""
Define the database models
"""
import secrets
import os
import base64
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from api import db



class User(db.Model, UserMixin):
    """
    User model
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    otp_secret = db.Column(db.String(16), nullable=False, default=secrets.token_hex(16))

    def __init__(self, **kwargs):
        """
        Create instance
        """
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            self.otp_secret = base64.b32encode(os.urandom(10))

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        Return dict representation of user
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "phone_number": self.phone_number,
        }
