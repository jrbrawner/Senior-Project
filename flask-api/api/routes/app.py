from tracemalloc import start
from flask import Blueprint
from flask import current_app as app, jsonify
import time
import logging
from flask_security.decorators import login_required, roles_required
from flask_security.utils import hash_password
from ..models.Users import User, Role
from api import user_datastore
from ..models.db import db
from api.services.DB_Startup import seed_db


app_bp = Blueprint("app_bp", __name__)


@app.before_first_request
def start_up():
    seed_db()


@app_bp.route("/", methods=["GET"])
@login_required
def index():
    return "Index"


@app_bp.route("/api/time", methods=["GET"])
@roles_required("Super Admin")
def get_time():
    return {"time": time.time()}
