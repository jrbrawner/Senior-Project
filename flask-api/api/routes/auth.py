from flask import (
    Blueprint,
    redirect,
    flash,
    request,
    session,
    url_for,
    session,
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
from ..models.Employees import Employee
from ..models.Admins import Admin

auth_bp = Blueprint("auth_bp", __name__)
sign_up = SignUp
log_in = Login


@auth_bp.post("/api/signup/<string:type>")
def signup(type):
    """
    Account sign up route.
    """
    """
    Sign-Up Form:
    name = Patientname associated with new account.
    email = Patient email associated with new account.
    password = Password associated with new account. (Not needed for patients.)
    """

    if type == "patient":
        return sign_up.signup_patient(request)

    if type == "physician":
        return sign_up.signup_physician(request)

    if type == "employee":
        return sign_up.signup_employee(request)

    if type == "admin":
        return sign_up.signup_admin(request)


@auth_bp.post("/api/login/<string:type>")
def login(type):
    """
    Log-in page for registered Employees, Physicians, & Admins.

    Login Form
    email = email associated with existing account
    password = password associated with existing account

    """

    if type == "physician":
        return log_in.login_physician(request)

    if type == "admin":
        return log_in.login_admin(request)

    if type == "employee":
        return log_in.login_employee(request)


@login_manager.user_loader
def load_user(id):
    """Check if user is logged-in on every page load."""

    login_type = session.get("login_type")
    if login_type == "employee":
        if id is not None:
            return Employee.query.get(id)
    elif login_type == "physician":
        if id is not None:
            return Physician.query.get(id)
    elif login_type == "admin":
        if id is not None:
            return Admin.query.get(id)
    else:
        return None
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized Patients to Login page."""
    flash("You must be logged in to view that page.")
    return redirect(url_for("auth_bp.login"))


@auth_bp.get("/api/logout")
@login_required
def logout():
    """User log-out logic."""

    name = current_user.name
    logout_user()

    return WebHelpers.EasyResponse(name + " logged out.", 200)


@auth_bp.route("/api/troubleshoot", methods=["GET"])
@login_required
def troubleshoot():

    data = {
        "testing": current_user.name,
        "testing1": current_user.id,
        "login_type": session["login_type"],
    }

    return data
