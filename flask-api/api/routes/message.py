from flask import Blueprint, request, send_from_directory
from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from ..models.Messages import Message, db, PNumbertoUser
from ..services.WebHelpers import WebHelpers
from ..services.twilio.SignUpHelpers import TwilioSignUpHelpers
from ..services.twilio.MessageTracking import MessageTracking
import logging
from flask_cors import cross_origin
from twilio.twiml.messaging_response import MessagingResponse
from ..models.Patients import Patient

message_bp = Blueprint('message', __name__)


@message_bp.route('/api/message', methods = ['GET'])
@login_required
@cross_origin()
def get_messages():
    """
    GET: Returns all messages.
    """

    if request.method == 'GET':
        
        messages = Message.query.all()
        
        resp = jsonify([x.serialize() for x in messages])
        resp.status_code = 200

        return resp
    

@message_bp.route('/api/message/<int:id>', methods = ['GET'])
@login_required
@cross_origin()
def get_message(id):
    """
    GET: Returns message with specified id.
    """

    if request.method == 'GET':
        message = Message.query.get(id)
        if message is None:
            return WebHelpers.EasyResponse('Message with that id does not exist.', 404)

        resp = jsonify(message.serialize())
        resp.status_code = 200

        return resp
    

@message_bp.route('/api/message/', methods = ['POST'])
@cross_origin()
def create_message():
    """
    POST: Creates new message.

    To-Do: Implement receiving a message from Twilio.
    """

    if request.method == 'GET':
        return WebHelpers.EasyResponse(f'Use GET method to create message.', 405)

    if request.method == 'POST':

            #get phone number and msg from twixml
            phone_number = request.form['phone_number']
            body = request.form['body']

            #logic for handling signup of new users

            #see if user has signed up and been accepted
            if TwilioSignUpHelpers.CheckIfAccepted(phone_number) == True:
                # if signed up and accepted, create new message to track conversation
                if MessageTracking.create_new_message_patient(phone_number, body) == True:
                    return f'Your physician has received your message.'

            #if new, prepare db table for new account registration
            elif TwilioSignUpHelpers.CheckForNewUser(phone_number) == True:
                status_msg = TwilioSignUpHelpers.InitiateUserSignUp(phone_number)
                return WebHelpers.EasyResponse(status_msg, 201)
            #see if user has signed up but not accepted,
            elif TwilioSignUpHelpers.CheckIfRegistered(phone_number) == True:
                return f'Your physician is in the process of accepting your registration.'
                #user has signed up but account not made yet, initiate signup form
            else:
                status_msg = TwilioSignUpHelpers.CreateNewUser(phone_number=phone_number, msg=body)
                return WebHelpers.EasyResponse(status_msg, 201)



@message_bp.route('/api/message/<int:id>', methods=['DELETE'])
def delete_message(id):

    message = Message.query.filter_by(id = id).first()

    if request.method == 'DELETE':
        if message:

            db.session.delete(message)
            db.session.commit()
            #return redirect('/api/message')
            logging.info(f'{message.name} deleted.')
            return WebHelpers.EasyResponse(f'{message.name} deleted.', 200)

        return WebHelpers.EasyResponse(f'message with that id does not exist.', 404)