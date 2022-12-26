from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#initialize SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

# Connect to db
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    db.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "login_page"
    login_manager.login_message_category = "info"

    #blueprint for auth routes in app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    
    from app import routes
    from app.designers import views
    from app.projects import views