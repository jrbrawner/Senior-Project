from flask import Blueprint, request, send_from_directory
from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from ..models.Messages import Message, db, PNumbertoUser
from ..services.WebHelpers import WebHelpers
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

        phone_number = request.form['phone_number']
        body = request.form['body']
        phone_number_user = PNumbertoUser.query.get(phone_number)

        if phone_number_user is None:
            logging.warning(f'New phone number {phone_number} recognized.')
            pnumbertouser = PNumbertoUser(
                phone_number=phone_number
            )
            db.session.add(pnumbertouser)
            db.session.commit()
            return WebHelpers.EasyResponse(f'Thanks for choosing to be with us! Please fill out this form to complete your registration.', 201)
        else:
            if phone_number_user is not None and phone_number_user.user_id is None:
                """
                Basic xample form to have user send in, seperate fields with '.' in message:
                Name.Email.
                """
                msg_array = body.split('.')
            
                name = msg_array[0]
                email = msg_array[1]

                new_patient = Patient(
                    name=name,
                    email=email,
                    phone_number=phone_number_user.phone_number
                )
                db.session.add(new_patient)
                new_patient.set_creation_date()
                db.session.commit()
                phone_number_user.user_id = new_patient.id
                db.session.commit()

                logging.warning(f'New patient registered. Name - {new_patient.name} Phone Number - {phone_number_user.phone_number}. ')
                return WebHelpers.EasyResponse(f'Thanks {new_patient.name}! You will be notified when your physician accepts your registration.', 201)
                



        #db.session.add(message)
        #db.session.commit()
        #logging.debug(f'New provider {provider.name} created.')

        #return WebHelpers.EasyResponse(f'New provider {provider.name} created.', 201)

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