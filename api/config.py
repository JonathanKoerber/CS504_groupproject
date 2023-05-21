import secrets
import os

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost:3306/CS_504_PROJECT'
    SQLALCHEMY_DATABASE_PASSWORD ="root"


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(DevelopmentConfig):
   
   pass

class DeployMentConfig(Config):
	
    pass