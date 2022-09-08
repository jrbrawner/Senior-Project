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
    app.config.from_object('config.DevelopmentConfig')

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
        from .routes.office import office_bp
        from .routes.user import user_bp
        
        # Register Blueprints
        app.register_blueprint(app_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(provider_bp)
        app.register_blueprint(office_bp)
        app.register_blueprint(user_bp)
        # Create Database Models
        db.create_all()

        # Compile static assets
        if app.config['FLASK_ENV'] == 'development':
            pass

        return app


def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "xxxxxxtestdatabasexxx"
    # Dynamically bind SQLAlchemy to application
    db.init_app(app)
    app.app_context().push() # this does the binding
    return app