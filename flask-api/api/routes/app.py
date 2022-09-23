from flask import Blueprint, request, send_from_directory
from .. import login_manager
from flask_login import logout_user
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
import time

app_bp = Blueprint("app_bp", __name__)


@app_bp.route("/", methods=["GET"])
def index():
    return "Index"


@app_bp.route("/api/time", methods=["GET"])
def get_time():
    return {"time": time.time()}
