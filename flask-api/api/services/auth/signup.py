from ...services.WebHelpers import WebHelpers
from ...models.Patients import db, Patient
from ...models.Physicians import Physician
import logging
from flask_login import login_user

class SignUp:

    def signup_patient(request):
        """ Handles logic for creating a new patient."""
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        #see if patient exists
        existing_patient = Patient.query.filter_by(email=email).first()
        
        #make sure patient doesnt already exist
        if existing_patient is None:
            patient = Patient(
                name= name,
                email= email
                #physician = None
            )

            patient.set_password(password)
            patient.set_creation_date()
            db.session.add(patient)
            db.session.commit()  # Create new Patient
            logging.debug(f'New patient {patient.id} created {patient.name}')
            login_user(patient)  # Log in as newly created Patient
            
            return WebHelpers.EasyResponse(f'New patient {patient.name} created.' , 201)

        return WebHelpers.EasyResponse('Patient with that email already exists. ', 400)

    def signup_physician(request):
        """ Handles logic for creating a new physician. """
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        #see if patient exists
        existing_physician = Physician.query.filter_by(email=email).first()
        
        #make sure patient doesnt already exist
        if existing_physician is None:
            physician = Physician(
                name= name,
                email= email
            )

            physician.set_password(password)
            physician.set_creation_date()
            db.session.add(physician)
            db.session.commit()  # Create new Patient
            logging.debug(f'New physician {physician.id} created {physician.name}')
            login_user(physician)  # Log in as newly created Physician
            
            return WebHelpers.EasyResponse(f'New patient {physician.name} created.' , 201)

        return WebHelpers.EasyResponse('Physician with that email already exists. ', 400)


    
        