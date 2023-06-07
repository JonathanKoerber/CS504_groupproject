from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

mail = Mail()
db = SQLAlchemy()


def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    # need to create the database before importing the models
    from api.users.routes import users

    app.register_blueprint(users)

    return app
