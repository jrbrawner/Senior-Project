from flask import Blueprint, request, send_from_directory, session, Response
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from api.models.db import db
from api.services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin
from flask_login import current_user
from api.services.twilio.TwilioClient import TwilioClient
from api.models.OrgModels import Location, Organization, User, Role, roles_users
from api import user_datastore
from flask_security.utils import hash_password
from flask_security import roles_accepted
from api.permissions import Permissions
from flask_security.utils import verify_password

user_bp = Blueprint("user_bp", __name__)


@user_bp.get("/api/user")
@login_required
@cross_origin()
def get_users():
    """
    GET: Returns all users.

    Super Admin: View All People
    Admin: View All People in Their Organization
    Physician: View All Employees & Patients
    Employee: View All Patients
    """
    data = []

    #Super Admin
    if current_user.has_permission(Permissions.VIEW_ALL_PEOPLE):
        users = User.query.all()
        resp = jsonify([x.serialize_user_display() for x in users])
        resp.status_code = 200
        logging.info(f"User id - {current_user.id} - accessed all users.")
        return resp
    #Admin
    if current_user.has_permission(Permissions.VIEW_ALL_CURRENT_ORG_PEOPLE):
        users = User.query.filter_by(organization_id = current_user.organization_id).all()
        resp = jsonify([x.serialize_user_display() for x in users])
        resp.status_code = 200
        logging.info(f"User id - {current_user.id} - accessed all current users.")
        return resp
    #Physician
    if current_user.has_permission(Permissions.VIEW_ALL_CURRENT_ORG_EMPLOYEE):

        users = User.query.filter_by(organization_id = current_user.organization_id).all()
        resp_users = []
        #Only grab users with employee or patient in their roles
        for x in users:
            user_roles = [z.name for z in x.roles]
            if 'Patient' in user_roles or 'Employee' in user_roles or 'Pending Patient' in user_roles:
                resp_users.append(x)

        resp = jsonify([x.serialize_user_display() for x in resp_users])
        resp.status_code = 200
        logging.info(f"User id - {current_user.id} - accessed all current employees & patients.")
        return resp
    #Employee
    if current_user.has_permission(Permissions.VIEW_ALL_CURRENT_ORG_PATIENTS):
        users = User.query.filter_by(organization_id = current_user.organization_id).all()
        resp_users = []
        
        for x in users:
            user_roles = [z.name for z in x.roles]
            if 'Patient' in user_roles or 'Pending Patient' in user_roles:
                resp_users.append(x)

        resp = jsonify([x.serialize_user_display() for x in resp_users])
        resp.status_code = 200
        logging.info(f"User id - {current_user.id} - accessed all current patients.")
        return resp
    else:
        return WebHelpers.EasyResponse('You are not authorized for this functionality.', 403)
        


@user_bp.get("/api/user/<int:id>")
@login_required
@cross_origin()
def get_user(id):
    """
    GET: Returns user with specified id. Required to edit a user.
    """
    if current_user.has_permission(Permissions.UPDATE_ALL_PEOPLE):
        user = User.query.get(id)
        if user is None:
            return WebHelpers.EasyResponse("User with that id does not exist.", 404)

        resp = jsonify(user.serialize_user_display())
        resp.status_code = 200
        # logging.info(f"User id - {current_user.id} - accessed patient with id of {id}.")

        return resp
    if current_user.has_permission(Permissions.UPDATE_CURRENT_ORG_PEOPLE):
        user = User.query.get(id)
        if user is None:
            return WebHelpers.EasyResponse("User with that id does not exist.", 404)
        
        if user.organization_id == current_user.organization_id:
            resp = jsonify(user.serialize_user_display())
            resp.status_code = 200
            # logging.info(f"User id - {current_user.id} - accessed patient with id of {id}.")

            return resp
        return WebHelpers.EasyResponse('You are not authorized to edit this user.', 403)
    else:
        return WebHelpers.EasyResponse('You are not authorized for this functionality.', 403)


@user_bp.put("/api/user/<int:id>")
@login_required
@cross_origin()
def update_user(id):
    """
    PUT: Updates specified user.
    """
    if current_user.has_permission(Permissions.UPDATE_ALL_PEOPLE):

        user : User

        user = User.query.get(id)
        if user:
            name = request.form["name"]
            email = request.form["email"]
            location_id = request.form["locationId"]
            roles = request.form["roles"]
            phone_number = request.form["phoneNumber"]
            
            user.name = name
            user.email = email
            user.location_id = location_id
            # user.roles = roles
            user.phone_number = phone_number
            db.session.commit()
            logging.warning(
                f"User id - {current_user.id} - updated user with id - {user.id} -"
             )
            return WebHelpers.EasyResponse(f"Name updated.", 200)
        return WebHelpers.EasyResponse(f"user with that id does not exist.", 404)
    if current_user.has_permission(Permissions.UPDATE_CURRENT_ORG_PEOPLE):
        user = User.query.get(id)
        if user.organization_id == current_user.organization_id:
            if user:
                name = request.form["name"]
                email = request.form["email"]
                location_id = request.form["locationId"]
                roles = request.form["roles"]
                phone_number = request.form["phoneNumber"]

                user.name = name
                user.email = email
                user.location_id = location_id
                # user.roles = roles
                user.phone_number = phone_number
                db.session.commit()
                logging.warning(
                    f"User id - {current_user.id} - updated user with id - {user.id} -"
                )
                return WebHelpers.EasyResponse(f"Name updated.", 200)
            return WebHelpers.EasyResponse(f"user with that id does not exist.", 404)
    else:
        return WebHelpers.EasyResponse('You are not authorized for this functionality.', 403)


@user_bp.post("/api/user")
@login_required
@cross_origin()
def create_user():
    if current_user.has_permission(Permissions.CREATE_ALL_PEOPLE):
        user_name = request.form["name"]
        email = request.form["email"].lower()
        password = request.form["password"]
        phone_number = request.form["phoneNumber"]

        role = request.form.get("roleGroup")
        
        locations = Location.query.all()
        location_values = {}
        selected_locations = []
        
        for i in locations:
            location_values[i.name] = request.form.get(i.name)
        
        for name,checked in location_values.items():
            if checked == 'on':
                location = Location.query.filter_by(name=name).first()
                selected_locations.append(location)

        organization_id = selected_locations[0].organization_id

        user = user_datastore.find_user(email=email)
        if user is None:
            user = user_datastore.find_user(phone_number=phone_number)
            if user is None:
                password = hash_password(password)
                
                user = user_datastore.create_user(
                    email=email,
                    name=user_name,
                    password=password,
                    phone_number=phone_number,
                    location_id=selected_locations[0].id,
                    organization_id=organization_id,
                )

                db.session.commit()
                user_datastore.add_role_to_user(user, role)

                for i in selected_locations:
                    user.add_location(user.id, i.id)

                logging.debug(f"New user {email} created.).")
                return WebHelpers.EasyResponse(f"New user {user.name} created.", 201)
            return WebHelpers.EasyResponse(f"User with that phone number already exists.", 400)
        return WebHelpers.EasyResponse(f"User with that email already exists.", 400)
    if current_user.has_permission(Permissions.CREATE_CURRENT_ORG_PEOPLE):
        user_name = request.form["name"]
        email = request.form["email"].lower()
        password = request.form["password"]
        phone_number = request.form["phoneNumber"]

        role = request.form.get("roleGroup")
        
        locations = Location.query.filter_by(organization_id=current_user.organization_id).all()
        location_values = {}
        selected_locations = []
        
        for i in locations:
            location_values[i.name] = request.form.get(i.name)
        
        for name,checked in location_values.items():
            if checked == 'on':
                location = Location.query.filter_by(name=name).first()
                selected_locations.append(location)

        organization_id = current_user.organization_id

        user = user_datastore.find_user(email=email)
        if user is None:
            user = user_datastore.find_user(phone_number=phone_number)
            if user is None:
                password = hash_password(password)
                
                user = user_datastore.create_user(
                    email=email,
                    name=user_name,
                    password=password,
                    phone_number=phone_number,
                    location_id=selected_locations[0].id,
                    organization_id=organization_id,
                )

                db.session.commit()
                if role != "Super Admin":
                    user_datastore.add_role_to_user(user, role)
                else:
                    return WebHelpers.EasyResponse(f"Error. Please try again.", 400)

                for i in selected_locations:
                    user.add_location(user.id, i.id)

                logging.debug(f"New user {email} created.).")
                return WebHelpers.EasyResponse(f"New user {user.name} created.", 201)
            return WebHelpers.EasyResponse(f"User with that phone number already exists.", 400)
        return WebHelpers.EasyResponse(f"User with that email already exists.", 400)
    if current_user.has_permission(Permissions.CREATE_BASE_USER):
        user_name = request.form["name"]
        email = request.form["email"].lower()
        password = request.form["password"]
        phone_number = request.form["phoneNumber"]

        role = request.form.get("roleGroup")
        
        locations = Location.query.filter_by(organization_id=current_user.organization_id).all()
        location_values = {}
        selected_locations = []
        
        for i in locations:
            location_values[i.name] = request.form.get(i.name)
        
        for name,checked in location_values.items():
            if checked == 'on':
                location = Location.query.filter_by(name=name).first()
                selected_locations.append(location)

        organization_id = current_user.organization_id

        user = user_datastore.find_user(email=email)
        if user is None:
            user = user_datastore.find_user(phone_number=phone_number)
            if user is None:
                password = hash_password(password)
                
                user = user_datastore.create_user(
                    email=email,
                    name=user_name,
                    password=password,
                    phone_number=phone_number,
                    location_id=selected_locations[0].id,
                    organization_id=organization_id,
                )

                db.session.commit()
                if role != "Super Admin" or role != "Admin":
                    user_datastore.add_role_to_user(user, role)
                else:
                    return WebHelpers.EasyResponse(f"Error. Please try again.", 400)

                for i in selected_locations:
                    user.add_location(user.id, i.id)

                logging.debug(f"New user {email} created.).")
                return WebHelpers.EasyResponse(f"New user {user.name} created.", 201)
            return WebHelpers.EasyResponse(f"User with that phone number already exists.", 400)
        return WebHelpers.EasyResponse(f"User with that email already exists.", 400)
    else:
        return WebHelpers.EasyResponse('You are not authorized for this functionality.', 403)


@user_bp.delete("/api/user/<int:id>")
@login_required
@cross_origin()
def delete_user(id):
    """
    DELETE: Deletes specified user.
    """
    if current_user.has_permission(Permissions.DELETE_ALL_PEOPLE):
        user = User.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            logging.warning(
                f"User id - {current_user.id} - deleted user with id {id}."
            )
            return WebHelpers.EasyResponse(f"User {id} deleted.", 200)
        return WebHelpers.EasyResponse(f"user with that id does not exist.", 404)
    if current_user.has_permission(Permissions.DELETE_CURRENT_ORG_PEOPLE):
        user = User.query.get(id)
        if user:
            if current_user.organization_id == user.organization_id:
                db.session.delete(user)
                db.session.commit()
                logging.warning(
                    f"User id - {current_user.id} - deleted user with id {id}."
                )
                return WebHelpers.EasyResponse(f"User {id} deleted.", 200)
        return WebHelpers.EasyResponse(f"user with that id does not exist.", 404)
    else:
        return WebHelpers.EasyResponse('You are not authorized for this functionality.', 403)




@login_required
@cross_origin()
@user_bp.get("/api/user/new")
def get_new_users():

    # get all pending users
    # 6 is role id for pending patient, could look it up but its faster if we keep id's the same
    # pending_patient = Role.query.filter_by(name='Pending Patient').first()
    # new_users = User.query.filter(User.roles.any(id=pending_patient)).all()
    new_users = []

    if current_user.has_permission(Permissions.VIEW_ALL_PEOPLE):
        users = User.query.filter(User.roles.any(id=6)).all()
        for x in users:
            new_users.append(x)
    else:
        for x in current_user.locations:
            users = User.query.filter(User.roles.any(id=6)).filter(User.location_id == x.id).all()
            for x in users:
                new_users.append(x)

    resp = jsonify([x.serialize_pending() for x in new_users])
    resp.status_code = 200
    logging.info(f"User id ({current_user.id}) accessed all new users.")

    return resp


@login_required
@cross_origin()
@user_bp.put("/api/user/new/accept/<int:id>")
def accept_new_user(id):

    user = User.query.get(id)
    location_id = user.location_id
    location = Location.query.get(location_id)
    organization_id = location.organization_id
    organization = Organization.query.get(organization_id)

    twilioClient = TwilioClient(
        organization.twilio_account_id, organization.twilio_auth_token
    )

    if user and "Pending Patient" in user.roles:

        user_datastore.remove_role_from_user(user, "Pending Patient")
        user_datastore.add_role_to_user(user, "Patient")
        logging.warning(
            f" User id ({current_user.id}) accepted {user.id} as a patient."
        )
        db.session.commit()
        twilioClient.send_automated_message(
            location.phone_number,
            user.phone_number,
            f"{user.name}, your physician has accepted your registration.",
            location_id=location_id
        )
        return WebHelpers.EasyResponse("Success.", 200)

    return WebHelpers.EasyResponse(f"User with that id does not exist.", 404)


@login_required
@cross_origin()
@user_bp.delete("/api/user/new/decline/<int:id>")
def decline_new_user(id):

    user = User.query.get(id)
    if user:
        user_name = user.name

        user_datastore.delete_user(user)
        db.session.commit()
        logging.warning(
            f"User id ({current_user.id}) declined {user_name} as a patient."
        )
        return WebHelpers.EasyResponse(
            f"{current_user.name} declined {user_name} as a patient.", 200
        )
    return WebHelpers.EasyResponse("User with that id does not exist.", 404)


@login_required
@user_bp.get("/api/user/profile")
def user_profile() -> Response:

    user_data = {
        'id': current_user.id,
        'name': current_user.name,
        'email': current_user.email,
        'phone_number': current_user.phone_number,
        'primary_location': current_user.location_id,
        'locations': [x.serialize() for x in current_user.locations],
        'roles': [x.serialize() for x in current_user.roles]
    }

    return jsonify(user_data)

@login_required
@user_bp.post("/api/user/edit-profile")
def edit_profile() -> Response:

    name = request.form['name']
    email = request.form['email']
    phone_number = request.form['phoneNumber']
    current_user.name = name
    current_user.email = email
    current_user.phone_number = phone_number
    db.session.commit()
    return WebHelpers.EasyResponse('User profile information updated.', 200)
    #return WebHelpers.EasyResponse('Error', 400)

@login_required
@user_bp.post("/api/user/change-password")
def change_user_password() -> Response:
    
    current_password = request.form['currentPassword']
    new_password = request.form['newPassword']
    confirm_password = request.form['confirmPassword']

    password_matches = verify_password(current_password, current_user.password)

    if password_matches:
        if new_password == confirm_password:
            password = hash_password(new_password)
            current_user.password = password
            db.session.commit()
            return WebHelpers.EasyResponse('Password updated.', 200)
        return WebHelpers.EasyResponse('Passwords do not match', 400)
    return WebHelpers.EasyResponse('Current password does not match', 400)

@login_required
@user_bp.get("/api/user/create/locations")
def get_available_locations() -> Response:
    
    if current_user.has_permission(Permissions.CREATE_ALL_PEOPLE):
        orgs = Organization.query.all()
        locations = Location.query.all()
        return jsonify([x.serialize() for x in locations])

    if current_user.has_permission(Permissions.CREATE_CURRENT_ORG_PEOPLE):
        organization_id = current_user.organization_id
        locations = Location.query.filter_by(organization_id = organization_id).all()
        return jsonify([x.serialize() for x in locations])

    
    if current_user.has_permission(Permissions.CREATE_BASE_USER):

        return jsonify([x.serialize() for x in current_user.locations])

    else:
        return WebHelpers.EasyResponse('You are not authorized for this functionality.', 403)
    

