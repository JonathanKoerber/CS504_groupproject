import secrets
import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = secrets.token_hex(16)


    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_PASSWORD ="root"
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_VERIFY_SERVICE_ID = os.environ.get('TWILIO_VERIFY_SERVICE_ID')
    MAIL_SERVER = 'smtp://sandbox.smtp.mailtrap.io'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('EMAIL_ACC')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    MAIL_AUTH_METHOD = 'LOGIN'


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class TestingConfig(DevelopmentConfig):
   
   pass

class DeployMentConfig(Config):
	
    pass