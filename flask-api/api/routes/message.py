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
from ..services.twilio.test import TwilioClient
from twilio.base.exceptions import TwilioRestException


twilioClient = TwilioClient(account_sid='', auth_token='')
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

    """

    if request.method == 'POST':

            #get phone number and msg from twixml
            phone_number = request.values.get('From', None)
            body = request.values.get('Body', None)
            
            #logic for handling signup of new users
            try:
                #see if user has signed up and been accepted
                if TwilioSignUpHelpers.CheckIfAccepted(phone_number) == True:
                    status_msg = f'Your physician has received your message.'
                    twilioClient.send_message(phone_number, status_msg,)
                    return WebHelpers.EasyResponse('Success.', 200)
                #if new, prepare db table for new account registration
                elif TwilioSignUpHelpers.CheckForNewUser(phone_number) == True:
                    status_msg = TwilioSignUpHelpers.InitiateUserSignUp(phone_number)
                    twilioClient.send_message(phone_number, status_msg)
                    return WebHelpers.EasyResponse('Success.', 200)
                #see if user has signed up but not accepted,
                elif TwilioSignUpHelpers.CheckIfRegistered(phone_number) == True:
                    status_msg = f'Your physician is in the process of accepting your registration.'
                    twilioClient.send_message(phone_number, status_msg)
                    return WebHelpers.EasyResponse('Success.', 200)
                    #user has signed up but account not made yet, initiate signup form
                else:
                    status_msg = TwilioSignUpHelpers.CreateNewUser(phone_number=phone_number, msg=body)
                    twilioClient.send_message(phone_number, status_msg)
                    return WebHelpers.EasyResponse('Success.', 200)
            except TwilioRestException as e:
                logging.warning(e)
                return WebHelpers.EasyResponse('Error', 400)



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