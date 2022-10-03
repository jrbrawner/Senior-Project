from flask import (
    Blueprint,
    request,
    session,
)
from flask_login import login_user, logout_user, current_user
from ..models.Users import User
from ..models.db import db
from flask import current_app as app
from api import login_manager
from ..services.WebHelpers import WebHelpers
import logging
from ..services.auth.signup import SignUp
from ..services.auth.login import Login
from ..models.Users import User
from api import user_datastore
from flask_login import login_required
from flask_security.utils import verify_password


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
    password = Password associated with new account.
    """

    return sign_up.signup_user(request)


@auth_bp.post("/api/login")
def login():
    """
    Log-in for registered users.
    """

    if current_user.is_authenticated:
            return WebHelpers.EasyResponse(
                current_user.name + " already logged in.", 400
            )

    email = request.form["email"]
    password = request.form["password"]

    user = user_datastore.find_user(email=email)
    password_matches = verify_password(password, user.password)

    if user and password_matches:
        login_user(user)
        user.set_last_login()
        logging.debug(f" User with id {user.id} logged in.")

        return WebHelpers.EasyResponse(user.name + " logged in.", 200)
    return WebHelpers.EasyResponse(
        "Invalid email/password combination.", 405
    )

@auth_bp.post('/api/grant_role')
def grant_role():
    """Add a role to a users account."""

    user_id = request.form['user_id']
    role_name = request.form['role_name']
    user = User.query.get(user_id)
    if user:
        user_datastore.add_role_to_user(user, role_name)
        db.session.commit()
        logging.warning(f'User id - {current_user.id} - granted {role_name} role to User id - {user_id} - ')
        return WebHelpers.EasyResponse('Role granted to user.', 200)
    return WebHelpers.EasyResponse('User with that id does not exist.', 404)

@auth_bp.post('/api/revoke_role')
def revoke_rule():
    """Remove a role from a users account. """

    user_id = request.form['user_id']
    role_name = request.form['role_name']

    user = User.query.get(user_id)
    if user:
        user_datastore.remove_role_from_user(user, role_name)
        db.session.commit()
        logging.warning(f'User id - {current_user.id} - revoked {role_name} role from User id - {user_id} -')
        return WebHelpers.EasyResponse('Role revoked from user.', 200)
    return WebHelpers.EasyResponse('User with that id does not exist.', 404)

@auth_bp.get('/api/check_roles')
def check_roles():
    """Check a users roles. """

    user_id = request.form['user_id']
    user = User.query.get(user_id)

    if user:
        roles = [x.serialize() for x in user.roles]
        logging.info(f'User id {current_user.id} accessed User id - {user_id} - roles')
        return roles

@auth_bp.get("/api/logout")
@login_required
def logout():
    """User log-out logic."""
    name = current_user.name
    logout_user()
    return WebHelpers.EasyResponse(f'{name} logged out.', 200)

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    resp = 'You must be logged in to view this page.'
    resp.status_code = 400
    return resp


@auth_bp.route("/api/troubleshoot", methods=["GET"])
@login_required
def troubleshoot():

    user = user_datastore.get_user(2)
    test = None

    if user.roles:
        test = 'YEP'

    data = {
        "testing": test
    }
    return data
