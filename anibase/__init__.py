import os

from dotenv import load_dotenv
from flask import Flask

from .model import db_uri
from .auth import csrf


def create_app():

    load_dotenv()

    app = Flask(__name__)

    # Random secret key for development purposes
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config['PER_PAGE'] = 20

    from .views import views
    from .auth import auth
    from .users import users

    app.register_blueprint(views)
    app.register_blueprint(users)
    app.register_blueprint(auth)

    # Database setup
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    # CSRF Protection
    csrf.init_app(app)

    return app
