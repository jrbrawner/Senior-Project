from flask import Blueprint, request, send_from_directory, session
from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from ..models.Patients import Patient, db
from ..models.Physicians import Physician
from ..models.Messages import PNumbertoUser
from ..services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin
from flask_login import current_user
from ..services.twilio.test import TwilioClient

user_bp = Blueprint('user_bp', __name__)
twilioClient = TwilioClient(account_sid='', auth_token='')

@user_bp.route('/api/user', methods = ['GET'])
@login_required
@cross_origin()
def get_users():
    """
    GET: Returns all users.
    """
    if session['login_type'] == 'physician':

        if request.method == 'GET':
            
            users = Patient.query.all()
            
            resp = jsonify([x.serialize() for x in users])
            resp.status_code = 200
            logging.info(f'{current_user} accessed all users.')

            return resp
    else:
        return WebHelpers.EasyResponse('You are not authorized to view this page.', 403)
    

@user_bp.route('/api/user/<int:id>', methods = ['GET'])
@login_required
@cross_origin()
def get_user(id):
    """
    GET: Returns user with specified id.
    """
    if session['login_type'] == 'physician':
        if request.method == 'GET':

            user = Patient.query.get(id)

            if user is None:
                return WebHelpers.EasyResponse('User with that id does not exist.', 404)

            resp = jsonify(user.serialize())
            resp.status_code = 200
            logging.info(f'{current_user} accessed patient with id of {id}.')

            return resp
    else:
        return WebHelpers.EasyResponse('You are not authorized to view this page.', 403)

    

@user_bp.route('/api/user/<int:id>', methods = ['PUT'])
@login_required
@cross_origin()
def update_user(id):
    """
    PUT: Deletes user with specified id, then creates user with specified data from form.
    """
    if session['login_type'] == 'physician':

        user = Patient.query.filter_by(id=id).first()
        old_name = user.name
    
        if request.method == 'PUT':
            if user:

                name = request.form['name']
                
                user.name = str(name)
                
                logging.warning(f'{current_user} updated patient with id {user.id} name from {old_name} to {user.name}.')
                return WebHelpers.EasyResponse(f'Name updated.', 200)

                #return redirect(f'api/user/{id}')

            return WebHelpers.EasyResponse(f'user with that id does not exist.', 404)
    else:
        return WebHelpers.EasyResponse('You are not authorized to view this page.', 403)
    
@user_bp.route('/api/user/<int:id>', methods=['DELETE'])
def delete_user(id):

    if session['login_type'] == 'physician':

        user = Patient.query.filter_by(id = id).first()
        user_name = user.name
        user_id = user.id

        if request.method == 'DELETE':
            if user:

                db.session.delete(user)
                db.session.commit()
                
                logging.warning(f'{current_user.name} deleted patient with id {user_id} and name of {user_name}.')

                return WebHelpers.EasyResponse(f'{user.name} deleted.', 200)

            return WebHelpers.EasyResponse(f'user with that id does not exist.', 404)
    else:
        return WebHelpers.EasyResponse('You are not authorized to view this page.', 403)

@user_bp.route('/api/user/new', methods=['GET'])
def get_new_users():

    if session['login_type'] == 'physician':
        
        #get all users without physician
        new_users = Patient.query.filter_by(physician_id = None).all()

        resp = jsonify([x.serialize() for x in new_users])
        resp.status_code = 200
        logging.info(f'{current_user} accessed all new users.')

        return resp

    else:
        return WebHelpers.EasyResponse('You are not authorized to view this page.', 403)


@user_bp.route('/api/user/new/accept/<int:id>', methods = ['PUT'])
def accept_new_user(id):

    if session['login_type'] == 'physician':

        physician = Physician.query.get(current_user.id)
        user = Patient.query.get(id)
        if user:
            user_name = user.name
            user.physician_id = physician.id
            p_number_to_user = PNumbertoUser.query.get(user.phone_number)
            p_number_to_user.physician_id = physician.id

            logging.warning(f'{current_user} accepted {user.name} as a patient.')
            db.session.commit()
            twilioClient.send_message(user.phone_number, f'{user_name}, your physician has accepted your registration.')
            return WebHelpers.EasyResponse('Success.', 200)
            

        return WebHelpers.EasyResponse(f'user with that id does not exist.', 404)
    else:
        return WebHelpers.EasyResponse('You are not authorized to view this page.', 403)

@user_bp.route('/api/user/new/decline/<int:id>', methods = ['DELETE'])
def decline_new_user(id):

    if session['login_type'] == 'physician':

        user = Patient.query.get(id)
        if user:
            user_name = user.name
            p_number_to_user = PNumbertoUser.query.get(user.phone_number)
            db.session.delete(user)
            db.session.delete(p_number_to_user)
            db.session.commit()
            logging.warning(f'{current_user} declined {user_name} as a patient.')
            return WebHelpers.EasyResponse(f'{current_user} declined {user_name} as a patient.', 200)
        
        return WebHelpers.EasyResponse(f'user with that id does not exist.', 404)
    else:
        return WebHelpers.EasyResponse('You are not authorized to view this page.', 403)







    
 

        




        
        


