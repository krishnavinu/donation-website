from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_mail import Mail
import pymysql

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Load configuration from config.py
    app.config.from_object('app.config')
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.main import main
    from app.auth import auth
    from app.donations import donations
    from app.admin import admin
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(donations)
    app.register_blueprint(admin)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @app.context_processor
    def utility_processor():
        def is_admin():
            return current_user.is_authenticated and current_user.role == 'admin'
        return dict(is_admin=is_admin)
    
    return app 
