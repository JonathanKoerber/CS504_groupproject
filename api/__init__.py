from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_authorize import Authorize



bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail
db = SQLAlchemy()

def create_app(Config):

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    print()
    from api.users.routes import users
    app.register_blueprint(users)

    return app