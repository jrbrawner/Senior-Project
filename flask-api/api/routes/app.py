from tracemalloc import start
from flask import Blueprint
from flask import current_app as app
import time
from flask_security.decorators import login_required
from api.services.DB_Startup import seed_db



app_bp = Blueprint("app_bp", __name__)


@app.before_first_request
def start_up():
    seed_db()
    pass

@app_bp.route("/", methods=["GET"])
@login_required
def index():
    return "Index"


@app_bp.route("/api/time", methods=["GET"])
def get_time():
    return {"time": time.time()}
