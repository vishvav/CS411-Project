from flask import Flask
from flask_sqlalchemy import SQLAlchemy  #1.3.18
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

# Create the app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'group1key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Picture
    
    # Create the database
    create_database(app)

    # Create the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # type: ignore
    login_manager.init_app(app)

    # Create the user loader
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    # if the database doesn't exist, create it
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('created Database.')
