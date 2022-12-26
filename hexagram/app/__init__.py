from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from datetime import timedelta

#initialize SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"])
# Connect to db
def create_app():
    app = Flask(__name__)
    # app.config["SESSION_PERMANENT"] = False
    # app.config["SESSION_TYPE"] = "filesystem"
    # Session(app)
    app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    
    limiter.init_app(app)

    db.init_app(app)
    bcrypt.init_app(app)
        
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_page"
    login_manager.login_message_category = "info"

    from . import models
    # with app.app_context():
    #     db.create_all()

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    #blueprint for auth routes in app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)

    @app.errorhandler(404)
    # Inbuilt function which takes error as parameter
    def page_not_found(e):
        """
        Handles 404 error
        """
        return render_template("errors/404.html"), 404

    @app.errorhandler(410)
    # Inbuilt function which takes error as parameter
    def not_found(e):
        """
        Handles 410 error
        """
        return render_template("errors/404.html"), 410

    @app.errorhandler(500)
    # Inbuilt function which takes error as parameter
    def internal_server_error(e):
        """
        Handles 500 error
        """
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    # Inbuilt function which takes error as parameter
    def forbidden(e):
        """
        Handles 403 error
        """
        return render_template("errors/403.html"), 403

    return app