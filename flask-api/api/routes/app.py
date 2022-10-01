from flask import Blueprint
from flask import current_app as app, jsonify
import time
import logging
from flask_security.decorators import login_required, roles_required
from flask_security.utils import hash_password
from ..models.Users import User, Role
from api import user_datastore
from ..models.db import db

app_bp = Blueprint("app_bp", __name__)


@app.before_first_request
def start_up():
    """Initial seeding of database on application start up."""

    if Role.query.count() == 0:
        super_admin_role = Role(
            id=1,
            name="Super Admin",
            description="Role for users that manage the platform utilized by organizations.",
        )

        admin_role = Role(
            id=2,
            name="Admin",
            description="Role for users that manage an organizations instance of the platform.",
        )

        physician_role = Role(
            id=3,
            name="Physician",
            description="Role for users that are physicians for an organization.",
        )

        employee_role = Role(
            id=4,
            name="Employee",
            description="Role for users that are employees of an organization.",
        )

        patient_role = Role(
            id=5,
            name="Patient",
            description="Role for users that are patients of an organization.",
        )

        pending_patient_role = Role(
            id=6,
            name="Pending Patient",
            description="Role for users that are patients of an organization, pending approval by a member of the organization.",
        )

        db.session.add(super_admin_role)
        db.session.add(admin_role)
        db.session.add(physician_role)
        db.session.add(employee_role)
        db.session.add(patient_role)
        db.session.add(pending_patient_role)

        db.session.commit()

    if User.query.count() == 0:
        password = hash_password("password")
        admin = user_datastore.create_user(
            name="admin", email="admin@email.com", password=password
        )
        user_datastore.add_role_to_user(admin, "Super Admin")
        db.session.add(admin)
        db.session.commit()
        logging.warning(
            f"No admin found, default admin account made. Make sure default credentials are changed."
        )


@app_bp.route("/", methods=["GET"])
@login_required
def index():
    return "Index"


@app_bp.route("/api/time", methods=["GET"])
@roles_required("admin")
def get_time():
    return {"time": time.time()}
