"""Flask app configuration."""
import os
from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))

class DevConfig:
    """Set Flask configuration from environment variables."""
    load_dotenv(path.join(basedir, '.env'))

    FLASK_APP = 'wsgi.py'
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')

    # Flask-Assets
    LESS_BIN = environ.get('LESS_BIN')
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir + '/api/' 'development.db')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Flask-Session
    SESSION_TYPE = environ.get('SESSION_TYPE')
    SESSION_PERMANENT = environ.get('SESSION_PERMANENT')
    #SESSION_FILE_THRESHOLD = environ.get('SESSION_FILE_THRESHOLD')

    #Flask-Login
    LOGIN_DISABLED = False

    #Configure application settings
    UPLOADS = environ.get('UPLOADS')
    MESSAGES_PER_PAGE = environ.get('MESSAGES_PER_PAGE')

    #Flask-Security
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_TRACKABLE = environ.get('SECURITY_TRACKABLE')

class TestConfig:
    
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', '12345')
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = False
    DEBUG = True