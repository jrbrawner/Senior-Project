from flask import Blueprint, request, send_from_directory, session

# from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from api.models.Users import User, Role
from api.models.db import db
from api.services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin
from flask_login import current_user
from api.services.twilio.TwilioClient import TwilioClient
from api.models.OrganizationModels import Location, Organization
from api import user_datastore

user_bp = Blueprint("user_bp", __name__)

@user_bp.get("/api/user")
@login_required
@cross_origin()
def get_users():
    """
    GET: Returns all users.
    """

    users = User.query.all()
    resp = jsonify([x.serialize() for x in users])
    resp.status_code = 200
    #logging.info(f"User id - {current_user.id} - accessed all users.")

    return resp


@user_bp.get("/api/user/<int:id>")
@login_required
@cross_origin()
def get_user(id):
    """
    GET: Returns user with specified id.
    """
    user = User.query.get(id)
    if user is None:
        return WebHelpers.EasyResponse("User with that id does not exist.", 404)

    resp = jsonify(user.serialize())
    resp.status_code = 200
    logging.info(f"User id - {current_user.id} - accessed patient with id of {id}.")

    return resp


@user_bp.route("/api/user/<int:id>", methods=["PUT"])
@login_required
@cross_origin()
def update_user(id):
    """
    PUT: Updates specified user.
    """
    user = User.query.filter_by(id=id).first()
    old_name = user.name

    if user:
        name = request.form["name"]
        user.name = str(name)
        logging.warning(
            f"User id - {current_user.id} - updated user with id - {user.id} -"
        )
        return WebHelpers.EasyResponse(f"Name updated.", 200)
    return WebHelpers.EasyResponse(f"user with that id does not exist.", 404)


@login_required
@cross_origin()
@user_bp.delete("/api/user/<int:id>")
def delete_user(id):
    """
    DELETE: Deletes specified user.
    """
    user = User.query.filter_by(id=id).first()
    user_name = user.name
    user_id = user.id
    if user:

        db.session.delete(user)
        db.session.commit()
        logging.warning(
            f"User id - {current_user.id} - deleted user with id {user_id} and name of {user_name}."
        )
        return WebHelpers.EasyResponse(f"{user.name} deleted.", 200)

    return WebHelpers.EasyResponse(f"user with that id does not exist.", 404)


@login_required
@cross_origin()
@user_bp.get("/api/user/new")
def get_new_users():

    # get all pending users
    # 6 is role id for pending patient, could look it up but its faster if we keep id's the same
    #pending_patient = Role.query.filter_by(name='Pending Patient').first()
    #new_users = User.query.filter(User.roles.any(id=pending_patient)).all() 

    new_users = User.query.filter(User.roles.any(id=6)).all() 

    resp = jsonify([x.serialize() for x in new_users])
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

    if user and 'Pending Patient' in user.roles:

        user_datastore.remove_role_from_user(user, 'Pending Patient')
        user_datastore.add_role_to_user(user, 'Patient')
        logging.warning(f" User id ({current_user.id}) accepted {user.id} as a patient.")
        db.session.commit()
        twilioClient.send_message(
            location.phone_number,
            user.phone_number,
            f"{user.name}, your physician has accepted your registration.",
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
        logging.warning(f"User id ({current_user.id}) declined {user_name} as a patient.")
        return WebHelpers.EasyResponse(
            f"{current_user.name} declined {user_name} as a patient.", 200
        )
    return WebHelpers.EasyResponse(f"user with that id does not exist.", 404)


@login_required
@cross_origin()
@user_bp.get("/api/user/<int:id>/messages")
def get_user_msgs(id):


    user = user_datastore.find_user(id=id)
    if user:
        resp = jsonify([x.serialize() for x in user.messages_sent])
        resp.status_code = 200

        return resp
