from re import T
from flask import Blueprint, request, send_from_directory

from flask_login import logout_user, login_required, current_user
from sqlalchemy import create_engine, MetaData
from flask import current_app as app, jsonify, session
from api.models.Messages import Message
from api.models.db import db
from ..services.WebHelpers import WebHelpers
from ..services.twilio.SignUpHelpers import TwilioSignUpHelpers
from ..services.twilio.MessageTracking import MessageTracking
import logging
from flask_cors import cross_origin
from twilio.twiml.messaging_response import MessagingResponse
from ..models.Users import User
from ..models.db import db
from ..services.twilio.TwilioClient import TwilioClient
from twilio.base.exceptions import TwilioRestException
from ..services.twilio.MessageTracking import MessageTracking
from ..models.OrganizationModels import Location, Organization


message_bp = Blueprint("message", __name__)


@message_bp.get("/api/message")
@login_required
@cross_origin()
def get_messages():
    """
    GET: Returns all messages.
    """

    if request.method == "GET":

        messages = Message.query.all()

        resp = jsonify([x.serialize() for x in messages])
        resp.status_code = 200

        return resp


@message_bp.get("/api/message/<int:id>")
@login_required
@cross_origin()
def get_message(id):
    """
    GET: Returns message with specified id.
    """
    message = Message.query.get(id)
    if message is None:
        return WebHelpers.EasyResponse("Message with that id does not exist.", 404)

    resp = jsonify(message.serialize())
    resp.status_code = 200

    return resp


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
                phone_number=phone_number, body=body
            )
            twilioClient.send_message(
                location.phone_number,
                phone_number,
                status_msg,
            )
            return WebHelpers.EasyResponse("Success.", 200)

        # if new, prepare db table for new account registration
        elif user_status == "New":
            status_msg = TwilioSignUpHelpers.InitiateUserSignUp(
                phone_number, location, organization, body
            )
            twilioClient.send_message(
                location.phone_number, phone_number, text=status_msg
            )
            return WebHelpers.EasyResponse("Success.", 200)

        # see if user has signed up but not been accepted,
        elif user_status == "Pending":
            status_msg = (
                f"Your physician is in the process of accepting your registration."
            )
            twilioClient.send_message(
                location.phone_number, phone_number, text=status_msg
            )
            return WebHelpers.EasyResponse("Success.", 200)

        # user has signed up but account not made yet, initiate signup form
        elif user_status == "Signup":
            status_msg = TwilioSignUpHelpers.CompleteUserSignUp(
                phone_number=phone_number, msg=body
            )
            twilioClient.send_message(location.phone_number, phone_number, status_msg)
            return WebHelpers.EasyResponse("Success.", 200)
    except TwilioRestException as e:
        logging.warning(e)
        return WebHelpers.EasyResponse("Error", 400)


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


@message_bp.route("/api/message/<int:id>", methods=["POST"])
def physician_message(id):

    if session["login_type"] == "physician":
        user = Patient.query.get(id)
        message = request.form["msg"]
        Location_id = current_user.Location_id
        Location = Location.query.get(Location_id)
        Organization_id = Location.Organization_id
        Organization = Organization.query.get(Organization_id)
        twilioClient = TwilioClient(
            Organization.twilio_account_id, Organization.twilio_auth_token
        )

        if user:
            twilioClient.send_message(Location.phone_number, user.phone_number, message)
            MessageTracking.create_new_message_physician_to_patient(
                current_user.id, user.phone_number, message
            )
            logging.warning(
                f"{current_user.name} sent a message to patient with id ({user.id})"
            )
            return WebHelpers.EasyResponse(f"Message sent.", 200)

        return WebHelpers.EasyResponse(f"User with id {id} does not exist.", 404)
