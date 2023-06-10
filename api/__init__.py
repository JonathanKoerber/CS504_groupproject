"""
The api package is a Flask application package.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

mail = Mail()
db = SQLAlchemy()


def create_app(config):
    """
    Create and configure an instance of the Flask application.
    @param Config: the configuration object to use.
    @return: the Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    mail.init_app(app)
    
    from api.users.routes import users

    app.register_blueprint(users)

    return app
