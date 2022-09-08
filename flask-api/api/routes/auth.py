from flask import Blueprint, redirect, render_template, flash, request, session, url_for, send_from_directory, Response, jsonify, session
from flask_login import login_required, logout_user, login_user, current_user
from ..models.Patients import db, Patient
from flask import current_app as app
from .. import login_manager
from ..services.WebHelpers import WebHelpers
import logging
from ..services.auth.signup import SignUp
from ..services.auth.login import Login
from ..models.Physicians import Physician

auth_bp = Blueprint('auth_bp', __name__)
sign_up = SignUp
log_in = Login

@auth_bp.route('/api/signup/<string:type>', methods=['GET', 'POST'])
def signup(type):
    """
    Patient sign-up page.
    GET requests serve sign-up page.
    POST requests handle Patient creation.
    """

    """
    Sign-Up Form:

    name = Patientname associated with new account.
    email = Patient email associated with new account.
    password = Password associated with new account.
    
    """
    if request.method == 'GET':

        return WebHelpers.EasyResponse('Use POST method for creating a new Patient.', 405)
    
    if request.method == 'POST':

        if type == 'patient':
            return sign_up.signup_patient(request)

        if type == 'physician':
            return sign_up.signup_physician(request)

        else:
            return WebHelpers(f'Resource type not recognized.', 404)

        
@auth_bp.route('/api/login/<string:type>', methods=['GET', 'POST'])
def login(type):
    """
    Log-in page for registered Patients & Physicians.
    GET requests serve Log-in page.

    POST requests validate and redirect Physicians to dashboard.
    Login Form

    email = email associated with existing account
    password = password associated with existing account
    
    """

    if request.method == 'GET':
        return WebHelpers.EasyResponse('Login with POST method.', 405)

    if request.method == 'POST':
        
        if type == 'patient':
            return log_in.login_patient(request)

        if type == 'physician':
            return log_in.login_physician(request)

        
@login_manager.user_loader
def load_user(id):
    """Check if user is logged-in on every page load."""
    
    login_type = session.get('login_type')
    if login_type == 'patient':
        if id is not None:
            return Patient.query.get(id)
    elif login_type == 'physician':
            return Physician.query.get(id)
    else:
        return None
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized Patients to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route("/api/logout", methods=['GET'])
@login_required
def logout():
    """Patient log-out logic."""

    name = current_user.name
    logout_user()

    return WebHelpers.EasyResponse(name + ' logged out.', 200)

@auth_bp.route("/api/troubleshoot", methods=['GET'])
@login_required
def troubleshoot():

    data = {
        'testing': current_user.name,
        'testing1': current_user.id
    }

    return data