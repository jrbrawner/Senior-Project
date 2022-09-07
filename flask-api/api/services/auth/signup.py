from ...services.WebHelpers import WebHelpers
from ...models.Patients import db, Patient
from ...models.Physicians import Physician
import logging
from flask_login import login_user
from flask import session

class SignUp:

    def signup_patient(request):
        """ Handles logic for creating a new patient."""
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        physician_id = request.form['physician_id']

        #see if patient exists
        existing_patient = Patient.query.filter_by(email=email).first()
        
        #make sure patient doesnt already exist
        if existing_patient is None:
            patient = Patient(
                name= name,
                email= email,
                physician = physician_id
            )

            patient.set_password(password)
            patient.set_creation_date()
            db.session.add(patient)
            db.session.commit()  # Create new Patient
            logging.debug(f'New patient {patient.id} created {patient.name}')
            login_user(patient)  # Log in as newly created Patient
            session['login_type'] = 'patient'
            
            return WebHelpers.EasyResponse(f'New patient {patient.name} created.' , 201)

        return WebHelpers.EasyResponse('Patient with that email already exists. ', 400)

    def signup_physician(request):
        """ Handles logic for creating a new physician. """
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        office_id = request.form['office_id']
        provider_id = request.form['provider_id']
        

        #see if patient exists
        existing_physician = Physician.query.filter_by(email=email).first()
        
        #make sure patient doesnt already exist
        if existing_physician is None:
            physician = Physician(
                name= name,
                email= email,
                office_id=office_id,
                provider_id=provider_id
            )

            physician.set_password(password)
            physician.set_creation_date()
            db.session.add(physician)
            db.session.commit()  # Create new Patient
            logging.debug(f'New physician {physician.name} created id ({physician.id}).')
            login_user(physician)  # Log in as newly created Physician
            session['login_type'] = 'physician'
            
            return WebHelpers.EasyResponse(f'New physician {physician.name} created.' , 201)

        return WebHelpers.EasyResponse('Physician with that email already exists. ', 400)


    
        