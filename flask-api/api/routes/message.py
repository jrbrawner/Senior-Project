from re import T
from flask import Blueprint, request, send_from_directory

from flask_login import logout_user, login_required, current_user
from sqlalchemy import create_engine, MetaData
from flask import current_app as app, jsonify, session, url_for, redirect
from api.models.Messages import Message
from api.models.db import db
from ..services.WebHelpers import WebHelpers
from ..services.twilio.SignUpHelpers import TwilioSignUpHelpers
from ..services.twilio.MessageTracking import MessageTracking
import logging
from flask_cors import cross_origin
from twilio.twiml.messaging_response import MessagingResponse
from ..models.db import db
from ..services.twilio.TwilioClient import TwilioClient
from twilio.base.exceptions import TwilioRestException
from ..services.twilio.MessageTracking import MessageTracking
from ..models.OrgModels import Location, Organization, User
from api.permissions import Permissions


message_bp = Blueprint("message", __name__)

"""
@message_bp.get("/api/message")
@login_required
@cross_origin()
def get_messages():
   
    if current_user.has_permission(Permissions.VIEW_ALL_MESSAGES):
        messages = Message.query.all()

        resp = jsonify([x.serialize() for x in messages])
        resp.status_code = 200

        return resp
    else:
        return WebHelpers.EasyResponse('You are not authorized for this functionality.', 403)

"""
"""
@message_bp.get("/api/message/<int:id>")
@login_required
@cross_origin()
def get_message(id):
    
    message = Message.query.get(id)
    if message is None:
        return WebHelpers.EasyResponse("Message with that id does not exist.", 404)

    resp = jsonify(message.serialize())
    resp.status_code = 200

    return resp
"""


@message_bp.route("/api/message/", methods=["POST"])
@cross_origin()
def create_message():
    """
    POST: Creates new message.

    """
    # get phone number and msg from twixml
    phone_number = request.values.get("From", None)
    body = request.values.get("Body", None)
    to = request.values.get("To", None)

    # handle photos
    num_media = int(request.values.get("NumMedia", 0))

    media_files = [
        (
            request.values.get(f"MediaUrl{i}", ""),
            request.values.get(f"MediaContentType{i}", ""),
        )
        for i in range(0, num_media)
    ]

    location = Location.query.filter_by(phone_number=to).first()
    organization_id = location.organization_id
    organization = Organization.query.get(organization_id)
    twilioClient = TwilioClient(
        organization.twilio_account_id, organization.twilio_auth_token
    )

    # logic for handling signup of new users
    try:
        user_status = TwilioSignUpHelpers.CheckUserState(phone_number)
        # see if user has signed up and been accepted
        if user_status == "Accepted":
            status_msg = f"Your physician has received your message."
            MessageTracking.create_new_message_patient(
                phone_number=phone_number,
                body=body,
                location_id=location.id,
                media_files=media_files,
            )
            # automated response when user is fully accepted
            # twilioClient.send_automated_message(
            #    location.phone_number,
            #    phone_number,
            #    status_msg,
            #    location_id=location.id
            # )
            return WebHelpers.EasyResponse("Success.", 200)

        # if new, prepare db table for new account registration
        elif user_status == "New":
            status_msg = TwilioSignUpHelpers.InitiateUserSignUp(
                phone_number, location, organization, body
            )
            twilioClient.send_automated_message(
                location.phone_number,
                phone_number,
                text=status_msg,
                location_id=location.id,
            )
            return WebHelpers.EasyResponse("Success.", 200)

        # see if user has signed up but not been accepted,
        elif user_status == "Pending":
            status_msg = (
                f"Your physician is in the process of accepting your registration."
            )
            twilioClient.send_automated_message(
                location.phone_number,
                phone_number,
                text=status_msg,
                location_id=location.id,
            )
            return WebHelpers.EasyResponse("Success.", 200)

        # user has signed up but account not made yet, initiate signup form
        elif user_status == "Signup":
            status_msg = TwilioSignUpHelpers.CompleteUserSignUp(
                phone_number=phone_number, msg=body
            )
            twilioClient.send_automated_message(
                location.phone_number, phone_number, status_msg, location_id=location.id
            )
            return WebHelpers.EasyResponse("Success.", 200)

    except TwilioRestException as e:
        logging.warning(e)
        return WebHelpers.EasyResponse("Error", 400)


"""
@message_bp.route("/api/message/<int:id>", methods=["DELETE"])
def delete_message(id):

    message = Message.query.filter_by(id=id).first()

    if request.method == "DELETE":
        if message:

            db.session.delete(message)
            db.session.commit()
            # return redirect('/api/message')
            logging.info(f"{message.name} deleted.")
            return WebHelpers.EasyResponse(f"{message.name} deleted.", 200)

        return WebHelpers.EasyResponse(f"message with that id does not exist.", 404)
"""


@login_required
@cross_origin()
@message_bp.get("/api/user/locations")
def get_message_sidebar_locations():

    if current_user:
        if current_user.has_permission(Permissions.VIEW_ALL_MESSAGES):

            orgs = Organization.query.all()

            locations = Location.query.all()

            return jsonify([x.serialize() for x in locations])

        if current_user.has_permission(Permissions.VIEW_ALL_CURRENT_ORG_MESSAGES):

            organization_id = current_user.organization_id

            locations = Location.query.filter_by(organization_id=organization_id).all()

            return jsonify([x.serialize() for x in locations])

        if current_user.has_permission(Permissions.VIEW_ALL_CURRENT_LOCATION_MESSAGES):

            location_id = current_user.location_id
            location = Location.query.get(location_id)
            resp_locations = []
            resp_locations.append(location.serialize())
            return resp_locations

        else:
            return WebHelpers.EasyResponse(
                "You are not authorized for this functionality.", 403
            )
    else:
        return WebHelpers.EasyResponse("You must login to view this page", 401)


@login_required
@cross_origin()
@message_bp.get("/api/location/<int:id>/users")
def get_message_sidebar_users(id):

    if (
        current_user.has_permission(Permissions.VIEW_ALL_MESSAGES)
        or current_user.has_permission(Permissions.VIEW_ALL_CURRENT_ORG_MESSAGES)
        or current_user.has_permission(Permissions.VIEW_ALL_CURRENT_LOCATION_MESSAGES)
    ):
        page = request.args.get("page", 1, type=int)
        # users = User.query.filter(User.location_id==id).filter(User.roles.any(name='Patient')).paginate(page=page, per_page=10, error_out=False)
        users = (
            User.query.filter(User.location_id == id)
            .filter(User.roles.any(name="Patient"))
            .all()
        )

        return jsonify([x.serialize_msg_sidebar() for x in users])
    else:
        return WebHelpers.EasyResponse(
            "You are not authorized for this functionality.", 403
        )


@login_required
@cross_origin()
@message_bp.get("/api/user/<int:id>/messages")
def get_user_messages(id):

    if (
        current_user.has_permission(Permissions.VIEW_ALL_MESSAGES)
        or current_user.has_permission(Permissions.VIEW_ALL_CURRENT_ORG_MESSAGES)
        or current_user.has_permission(Permissions.VIEW_ALL_CURRENT_LOCATION_MESSAGES)
    ):

        all_messages = (
            Message.query.order_by(Message.timestamp.asc())
            .filter((Message.recipient_id == id) | (Message.sender_id == id))
            .all()
        )

        return jsonify([x.serialize() for x in all_messages])
    else:
        return WebHelpers.EasyResponse(
            "You are not authorized for this functionality.", 403
        )


@login_required
@cross_origin()
@message_bp.post("/api/message/user/<int:id>/location/<int:locationId>")
def message_user(id, locationId):

    location = Location.query.get(locationId)
    if (
        current_user.has_permission(Permissions.SEND_MESSAGE)
        and location in current_user.locations
    ):

        user = User.query.get(id)
        message = request.form["msg"]
        organization_id = location.organization_id
        organization = Organization.query.get(organization_id)

        twilioClient = TwilioClient(
            organization.twilio_account_id, organization.twilio_auth_token
        )

        if user:

            twilioClient.send_automated_message(
                location.phone_number, user.phone_number, message, location.id
            )

            logging.warning(
                f"{current_user.name} sent a message to patient with id ({user.id})"
            )
            return WebHelpers.EasyResponse(f"Message sent.", 200)

        return WebHelpers.EasyResponse(f"User with id {id} does not exist.", 404)
    else:
        return WebHelpers.EasyResponse(
            "You are not authorized for this functionality.", 403
        )


@login_required
@cross_origin()
@message_bp.post("/api/message/announcement/<int:id>")
def send_announcement(id):

    location = Location.query.get(id)
    if (
        current_user.has_permission(Permissions.SEND_ANNOUNCEMENT)
        and location in current_user.locations
    ):

        message = request.form["msg"]
        # roles = request.form['roles']

        organization_id = location.organization_id
        organization = Organization.query.get(organization_id)

        twilioClient = TwilioClient(
            organization.twilio_account_id, organization.twilio_auth_token
        )
        users = User.query.filter_by(location_id=id).all()

        for i in users:
            try:
                twilioClient.send_automated_message(
                    location.phone_number, i.phone_number, message, location.id
                )
                logging.warning(
                    f"{current_user.name} sent an announcement to users of location ({location.id})"
                )
            except TwilioRestException as e:
                logging.warning(e)

        return WebHelpers.EasyResponse(f"Announcement sent.", 200)
    else:
        return WebHelpers.EasyResponse(
            "You are not authorized for this functionality.", 403
        )


@login_required
@cross_origin()
@message_bp.get("/api/load-photo/<string:photo>")
def load_message(photo):
    if (
        current_user.has_permission(Permissions.VIEW_ALL_MESSAGES)
        or current_user.has_permission(Permissions.VIEW_ALL_CURRENT_ORG_MESSAGES)
        or current_user.has_permission(Permissions.VIEW_ALL_CURRENT_LOCATION_MESSAGES)
    ):
        return send_from_directory("static", f"photos/{photo}")
    else:
        return WebHelpers.EasyResponse(
            "You are not authorized for this functionality.", 403
        )
