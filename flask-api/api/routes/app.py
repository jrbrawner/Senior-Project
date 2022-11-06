from tracemalloc import start
from flask import Blueprint
from flask import current_app as app
import time
from flask_security.decorators import login_required
from api.services.DB_Startup import seed_db
from api.models.Messages import Message
from api.models.OrgModels import User
from flask import jsonify, send_from_directory

app_bp = Blueprint("app_bp", __name__)

@app.before_first_request
def start_up():
    #seed_db()
    pass

@app_bp.route("/", methods=["GET"])
@login_required
def index():
    return "Index"


@app_bp.route("/api/time", methods=["GET"])
def get_time():
    return {"time": time.time()}

@app_bp.get("/testing")
def test_message():

    user = User.query.get(55)
    messages = user.messages_sent
    print(messages[-1].photos)
    
    resp = jsonify([x.serialize() for x in messages])
    message = messages[-1]

    return resp