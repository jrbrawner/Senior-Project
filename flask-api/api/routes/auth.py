from flask import (
    Blueprint,
    redirect,
    flash,
    request,
    session,
    url_for,
    session,
)
from flask_security import login_required, logout_user, login_user, current_user
from ..models.Users import User
from ..models.db import db
from flask import current_app as app
from .. import login_manager
from ..services.WebHelpers import WebHelpers
import logging
from ..services.auth.signup import SignUp
from ..services.auth.login import Login
from ..models.Users import User
from api import user_datastore

auth_bp = Blueprint("auth_bp", __name__)
sign_up = SignUp
log_in = Login


@auth_bp.post("/api/signup")
def signup():
    """
    Account sign up route.
    """
    """
    Sign-Up Form:
    name = Patientname associated with new account.
    email = Patient email associated with new account.
    password = Password associated with new account. (Not needed for patients.)
    """

    return sign_up.signup_user(request)


@auth_bp.post("/api/login")
def login():
    """
    Log-in page for registered Employees, Physicians, & Admins.

    Login Form
    email = email associated with existing account
    password = password associated with existing account

    """

    return log_in.login_user(request)


@login_manager.user_loader
def load_user(id):
    """Check if user is logged-in on every page load."""
    return user_datastore.get_user(id)


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

