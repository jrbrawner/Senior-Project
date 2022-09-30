from flask import Blueprint
from flask import current_app as app, jsonify
import time
import logging
from flask_security.decorators import login_required, roles_required

app_bp = Blueprint("app_bp", __name__)

"""

@app.before_first_request
def start_up():
    if Admin.query.count() == 0:

        admin = Admin(name="admin", email="admin@email.com", password="adminpassword")
        admin.set_creation_date()
        db.session.add(admin)
        db.session.commit()
        logging.warning(
            f"No admin found, default admin account made. Make sure default credentials are changed."
        )
"""

@app_bp.route("/", methods=["GET"])
@login_required
def index():
    return "Index"

@app_bp.route("/api/time", methods=["GET"])
@roles_required('admin')
def get_time():
    return {"time": time.time()}
