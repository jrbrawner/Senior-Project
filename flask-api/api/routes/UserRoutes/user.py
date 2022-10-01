from flask import Blueprint, request, send_from_directory, session

# from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from api.models.Users import User, Role
from api.models.db import db
from api.models.Messages import PNumbertoUser
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
    logging.info(f"User id - {current_user.id} - accessed all users.")

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
@user_bp.route("/api/user/new", methods=["GET"])
def get_new_users():

    if session["login_type"] == "physician":

        # get all users without physician
        new_users = Patient.query.filter_by(physician_id=None).all()

        resp = jsonify([x.serialize() for x in new_users])
        resp.status_code = 200
        logging.info(f"{current_user} accessed all new users.")

        return resp

    else:
        return WebHelpers.EasyResponse("You are not authorized to view this page.", 403)


@login_required
@cross_origin()
@user_bp.route("/api/user/new/accept/<int:id>", methods=["PUT"])
def accept_new_user(id):

    if session["login_type"] == "physician":

        physician = Physician.query.get(current_user.id)
        user = Patient.query.get(id)
        Location_id = physician.Location_id
        Location = Location.query.get(Location_id)
        Organization_id = Location.Organization_id
        Organization = Organization.query.get(Organization_id)

        twilioClient = TwilioClient(
            Organization.twilio_account_id, Organization.twilio_auth_token
        )

        if user:
            user_name = user.name
            user.physician_id = physician.id
            p_number_to_user = PNumbertoUser.query.get(user.phone_number)
            p_number_to_user.physician_id = physician.id

            logging.warning(f"{current_user} accepted {user.name} as a patient.")
            db.session.commit()
            twilioClient.send_message(
                Location.phone_number,
                user.phone_number,
                f"{user_name}, your physician has accepted your registration.",
            )
            return WebHelpers.EasyResponse("Success.", 200)

        return WebHelpers.EasyResponse(f"user with that id does not exist.", 404)
    else:
        return WebHelpers.EasyResponse("You are not authorized to view this page.", 403)


@login_required
@cross_origin()
@user_bp.route("/api/user/new/decline/<int:id>", methods=["DELETE"])
def decline_new_user(id):

    if session["login_type"] == "physician":

        user = Patient.query.get(id)
        if user:
            user_name = user.name
            p_number_to_user = PNumbertoUser.query.get(user.phone_number)
            db.session.delete(user)
            db.session.delete(p_number_to_user)
            db.session.commit()
            logging.warning(f"{current_user} declined {user_name} as a patient.")
            return WebHelpers.EasyResponse(
                f"{current_user} declined {user_name} as a patient.", 200
            )

        return WebHelpers.EasyResponse(f"user with that id does not exist.", 404)
    else:
        return WebHelpers.EasyResponse("You are not authorized to view this page.", 403)


@login_required
@cross_origin()
@user_bp.route("/api/user/<int:id>/messages", methods=["GET"])
def get_user_msgs(id):

    if session["login_type"] == "physician":
        user = Patient.query.get(id)

        if user:
            resp = jsonify([x.serialize() for x in user.messages_sent])
            resp.status_code = 200

            return resp
