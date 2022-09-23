from flask import (
    Blueprint,
    redirect,
    render_template,
    flash,
    request,
    session,
    url_for,
    send_from_directory,
    Response,
    jsonify,
)
from flask_login import login_required, logout_user, login_user, current_user
from ..models.Patients import db, Patient
from flask import current_app as app
from .. import login_manager
from ..services.WebHelpers import WebHelpers
import logging
from ..services.auth.signup import SignUp
from ..services.auth.login import Login
from ..models.Physicians import Physician
from flask_session import Session
from functools import wraps
from ..models.Employees import Employee

auth_bp = Blueprint("auth_bp", __name__)
sign_up = SignUp
log_in = Login


@auth_bp.post("/api/signup/<string:type>")
def signup(type):
    """
    Account signups.
    POST requests handle Patient creation.
    """

    """
    Sign-Up Form:

    name = Patientname associated with new account.
    email = Patient email associated with new account.
    password = Password associated with new account.
    
    """

    if type == "patient":
        return sign_up.signup_patient(request)

    if type == "physician":
        return sign_up.signup_physician(request)

    if type == "employee":
        return sign_up.signup_employee(request)


@auth_bp.get("/api/login/<string:type>")
def login(type):
    """
    Log-in page for registered Patients, Physicians, and Employees.

    Login Form

    email = email associated with existing account
    password = password associated with existing account

    """

    if type == "patient":
        return log_in.login_patient(request)

    if type == "physician":
        return log_in.login_physician(request)

    if type == "employee":
        return log_in.login_employee(request)


@login_manager.user_loader
def load_user(id):
    """Check if user is logged-in on every page load."""

    login_type = session.get("login_type")
    if login_type == "patient":
        if id is not None:
            return Patient.query.get(id)
    elif login_type == "physician":
        return Physician.query.get(id)
    elif login_type == "employee":
        return Employee.query.get(id)
    else:
        return None
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized Patients to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/api/logout", methods=["GET"])
@login_required
def logout():
    """Log-out logic."""

    name = current_user.name
    logout_user()

    return WebHelpers.EasyResponse(name + " logged out.", 200)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session["login_type"] == "admin":
            return f(*args, **kwargs)
        else:
            return WebHelpers.EasyResponse(
                "You are not authorized to access this page.", 401
            )

    return wrap


def physician_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session["login_type"] == "physician" or session["login_type"] == "admin":
            return f(*args, **kwargs)
        else:
            return WebHelpers.EasyResponse(
                "You are not authorized to access this page.", 401
            )

    return wrap


def employee_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if (
            session["login_type"] == "physician"
            or session["login_type"] == "admin"
            or session["login_type"] == "employee"
        ):
            return f(*args, **kwargs)
        else:
            return WebHelpers.EasyResponse(
                "You are not authorized to access this page.", 401
            )

    return wrap


@auth_bp.route("/api/troubleshoot", methods=["GET"])
@login_required
def troubleshoot():

    login_type = session["login_type"]
    data = {
        "testing": current_user.name,
        "testing1": current_user.id,
        "login_type": login_type,
    }

    return data
