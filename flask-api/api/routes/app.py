from flask import Blueprint, request, send_from_directory
from .. import login_manager
from flask_login import logout_user
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify

app_bp = Blueprint('app_bp', __name__)

@app_bp.route('/', methods = ['GET'])
def index():
    return 'Index'
