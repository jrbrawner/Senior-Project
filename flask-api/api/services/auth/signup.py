from ...services.WebHelpers import WebHelpers
from ...models.Users import User
from ...models.db import db
from ...models.Users import User, Role
import logging
from flask_security import login_user
from flask import session
from .login import admin_required, employee_required, physician_required
from api import user_datastore
from flask_security.utils import hash_password


class SignUp:
    def create_user(request):
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form['role']

        user = user_datastore.find_user(email=email)

        if user is None:
            password = hash_password(password)
            user = user_datastore.create_user(email=email, name=name, password=password)
            user_datastore.add_role_to_user(user, role)
            db.session.commit()
            logging.debug(f"New user {email} created.).")
            return WebHelpers.EasyResponse(f"New user {user.name} created.", 201)
        return WebHelpers.EasyResponse(f"User with that email already exists.", 400)

    """
    @employee_required
    def signup_patient(request):
        Handles logic for creating a new patient.
        name = request.form["name"]
        email = request.form["email"]
        # not supporting patients logging into the site, dont need to set up a password for them
        # password = request.form['password']
        physician_id = request.form["physician_id"]

        # see if patient exists
        existing_patient = Patient.query.filter_by(email=email).first()

        # make sure patient doesnt already exist
        if existing_patient is None:
            patient = Patient(name=name, email=email, physician_id=physician_id)

            patient.set_creation_date()
            db.session.add(patient)
            db.session.commit()  # Create new Patient
            logging.debug(f"New patient {patient.id} created {patient.name}")
            login_user(patient)  # Log in as newly created Patient

            return WebHelpers.EasyResponse(f"New patient {patient.name} created.", 201)

        return WebHelpers.EasyResponse("Patient with that email already exists. ", 400)

    @physician_required
    def signup_physician(request):
        Handles logic for creating a new physician.
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        office_id = request.form["office_id"]
        provider_id = request.form["provider_id"]
        phone_number = request.form["phone_number"]

        # see if patient exists
        existing_physician = Physician.query.filter_by(email=email).first()

        # make sure patient doesnt already exist
        if existing_physician is None:
            physician = Physician(
                name=name,
                email=email,
                office_id=office_id,
                provider_id=provider_id,
                phone_number=phone_number,
            )

            physician.set_password(password)
            physician.set_creation_date()
            db.session.add(physician)
            db.session.commit()  # Create new Patient
            logging.debug(
                f"New physician {physician.name} created id ({physician.id})."
            )
            login_user(physician)  # Log in as newly created Physician
            session["login_type"] = "physician"

            return WebHelpers.EasyResponse(
                f"New physician {physician.name} created.", 201
            )

        return WebHelpers.EasyResponse(
            "Physician with that email already exists. ", 400
        )

    @physician_required
    def signup_employee(request):
        Handles logic for creating a new physician.
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        office_id = request.form["office_id"]
        provider_id = request.form["provider_id"]

        # see if patient exists
        existing_employee = Employee.query.filter_by(email=email).first()

        # make sure patient doesnt already exist
        if existing_employee is None:
            employee = Employee(
                name=name, email=email, office_id=office_id, provider_id=provider_id
            )

            employee.set_password(password)
            employee.set_creation_date()
            db.session.add(employee)
            db.session.commit()  # Create new Employee
            logging.debug(f"New employee {employee.name} created id ({employee.id}).")
            login_user(employee)  # Log in as newly created Employee
            session["login_type"] = "employee"

            return WebHelpers.EasyResponse(
                f"New employee {employee.name} created.", 201
            )

        return WebHelpers.EasyResponse("Employee with that email already exists. ", 400)

    @admin_required
    def signup_admin(request):
        Handles logic for creating a new physician.
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        # see if patient exists
        existing_admin = Admin.query.filter_by(email=email).first()

        # make sure patient doesnt already exist
        if existing_admin is None:
            admin = Admin(name=name, email=email)

            admin.set_password(password)
            admin.set_creation_date()
            db.session.add(admin)
            db.session.commit()  # Create new Admin
            logging.debug(f"New admin {admin.name} created id ({admin.id}).")

            return WebHelpers.EasyResponse(f"New admin {admin.name} created.", 201)
        return WebHelpers.EasyResponse("Admin with that email already exists. ", 400)
    """
