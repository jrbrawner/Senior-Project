"""Initialize app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging

UPLOADS = 'api/uploads'

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.from_object('config.Config')
    app.config['UPLOADS'] = UPLOADS
    app.config['MESSAGES_PER_PAGE'] = 10

    #authentication
    app.config['LOGIN_DISABLED'] = True

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    #Set up logging
    logging.basicConfig(filename='record.log',level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s : %(message)s', filemode='w+')
    
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)


    with app.app_context():
        
        #import blueprints
        from .routes.auth import auth_bp
        from .routes.app import app_bp
        from .routes.provider import provider_bp
        
        # Register Blueprints
        app.register_blueprint(app_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(provider_bp)
        
        # Create Database Models
        db.create_all()

        # Compile static assets
        if app.config['FLASK_ENV'] == 'development':
            pass

        return app