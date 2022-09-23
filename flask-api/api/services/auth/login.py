from ..WebHelpers import WebHelpers
from flask_login import current_user, login_user
import logging
from ...models.Patients import Patient
from ...models.Physicians import Physician
from flask import session
from functools import wraps

class Login:

    def login_patient(request):

        if current_user.is_authenticated:
            return WebHelpers.EasyResponse(current_user.name + ' already logged in.', 400)

        email = request.form['email']
        password = request.form['password']
        #next_page = request.form['next_page']

        # Validate login attempt
        patient = Patient.query.filter_by(email=email).first()

        if patient and patient.check_password(password=password):
            #Patient exists and password matches password in db
            login_user(patient)
            patient.set_last_login()
            session['login_type'] = 'patient'
            logging.debug(f'{patient.name} logged in.')

            return WebHelpers.EasyResponse(patient.name + ' logged in.' , 405)
            
        #Patient exists but password does not match password in db
        return WebHelpers.EasyResponse('Invalid Patient email/password combination.', 405)

    def login_physician(request):
    
        if current_user.is_authenticated:
            return WebHelpers.EasyResponse(f'{current_user.name} already logged in.', 400)

        email = request.form['email']
        password = request.form['password']
        #next_page = request.form['next_page']

        # Validate login attempt
        physician = Physician.query.filter_by(email=email).first()

        if physician and physician.check_password(password=password):
            #Patient exists and password matches password in db

            login_user(physician)
            physician.set_last_login()
            session['login_type'] = 'physician'
            logging.debug(f'{physician.name} logged in.')

            return WebHelpers.EasyResponse(physician.name + ' logged in.' , 405)
            
        #Patient exists but password does not match password in db
        return WebHelpers.EasyResponse('Invalid Physician email/password combination.', 405)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        login_type = session.get('admin')
        if login_type == "admin":
            return f(*args, **kwargs)
        else:
            return(f'"You need to be an admin to use this route."')
    return wrap

def physician_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        login_type = session.get('login_type')
        if login_type == "physician":
            return f(*args, **kwargs)
        else:
            return(f'"You need to be a physician to use this route."')
    return wrap