# Description: This file contains the data model for the database.
from api import db #, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask_authorize import RestrictionsMixin, AllowancesMixin, PermissionsMixin, OwnerPermissionsMixin

import secrets
import os
from flask import current_app
import jwt

class User(db.Model, UserMixin):
    __tablename__='user'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(120), nullable=False)


    def __init__(self, user_id, username, email, password, phone_number):
        """
        constructs and initializes the users database class.
        :param user_id:
        :param username:
        :param email:
        :param password:
        :param phone_number:
        """
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.phone_number = phone_number


    def get_reset_token(self, expires_sec=1800):
        s = jwt.encode(
            {
            "confirm": self.id, 
            "exp": datetime.utcnow() + datetime.timedelta(seconds=expires_sec)
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(self, token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=datetime.timedelta(seconds=10),
                algorithms=["HS256"]
            )
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
        



    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
