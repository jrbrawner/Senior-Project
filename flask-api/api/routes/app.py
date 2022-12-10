from flask import Blueprint
from flask import current_app as app
from flask_security.decorators import login_required
from api.services.DB_Startup import seed_db
import flask
import flask_login
import datetime

app_bp = Blueprint("app_bp", __name__)


@app.before_first_request
def start_up():
    seed_db()


@app.before_request
def before_request():
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=15)
    flask.session.modified = True
    flask.g.user = flask_login.current_user


@app.errorhandler(404)
def not_found(e):
    return app.send_static_file("index.html")


@app_bp.route("/", methods=["GET"])
@login_required
def index():
    return "Index"
