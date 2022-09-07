from flask import Blueprint, request, send_from_directory
from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from ..models.Messages import Message, db
from ..services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin
from twilio.twiml.messaging_response import MessagingResponse

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
@login_required
@cross_origin
def create_message():
    """
    POST: Creates new message.

    To-Do: Implement receiving a message from Twilio.
    """

    #Start TwiML response
    resp = MessagingResponse()

    resp.message("Message received.")

    return str(resp)

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