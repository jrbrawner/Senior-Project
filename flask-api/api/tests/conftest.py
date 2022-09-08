import os
import pytest
import tempfile

from api import db as _db
from api import create_app
from api.models.Patients import Patient

class TestConfig(object):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.environ.get('SECRET_KEY', '12345')
    SQLALCHEMY_DATABASE_URI = 'sqlite://xxxtestdatabase.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

@pytest.fixture(scope='session')
def app(request):
    flask_app = create_app(TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.

    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return testing_client


@pytest.fixture(scope='session')
def db(app):
    # Create the database and the database table
    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()
   
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    # connect to the database
    connection = db.engine.connect()
    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual session to the connection
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    # overload the default session with the session above
    db.session = session

    def teardown():
        session.close()
        # rollback - everything that happened with the
        # session above (including calls to commit())
        # is rolled back.
        transaction.rollback()
        # return connection to the Engine
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session