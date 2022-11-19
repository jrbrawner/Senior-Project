"""Initialize app."""
from flask import Flask
import logging
from flask_security import SQLAlchemyUserDatastore, Security
from api.models.OrgModels import User, Role
from api.models.db import db

from flask import abort

UPLOADS = "api/uploads"
#login_manager = LoginManager()


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security()

def create_app(config):
    """Construct the core app object."""
    app = Flask(__name__)

    # Application Configuration
    if config == 'production':
        app.config.from_object("config.ProductionConfig")
        logging.warning('Running production configuration.')
    elif config == "dev":
        app.config.from_object("config.DevConfig")
        logging.warning('Running development configuration.')
    elif config == "test":
        app.config.from_object("config.TestConfig")
        logging.warning('Running test configuration.')

    
    # Initialize Plugins
    db.init_app(app)
    security_ctx = security.init_app(app, user_datastore)

    #disable security default views
    @security_ctx.context_processor
    def security_context_processor():
        return abort(404)

    #login_manager.init_app(app)


    # Set up logging
    logging.basicConfig(
        filename="record.log",
        level=logging.DEBUG,
        format=f"%(asctime)s %(levelname)s %(name)s : %(message)s",
        filemode="w+",
    )

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

    with app.app_context():

        # import blueprints
        from .routes.auth import auth_bp
        from .routes.app import app_bp
        from .routes.organization import organization_bp
        from .routes.location import location_bp
        from .routes.UserRoutes.user import user_bp
        from .routes.message import message_bp
        from .routes.UserRoutes.role import role_bp

        # Register Blueprints
        app.register_blueprint(app_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(organization_bp)
        app.register_blueprint(location_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(message_bp)
        app.register_blueprint(role_bp)
        # Create Database Models
        db.create_all()

        # Compile static assets
        if app.config["FLASK_ENV"] == "development":
            pass

        return app


def create_test_app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "xxxxxxtestdatabasexxx"
    # Dynamically bind SQLAlchemy to application
    db.init_app(app)
    app.app_context().push()  # this does the binding
    return app
