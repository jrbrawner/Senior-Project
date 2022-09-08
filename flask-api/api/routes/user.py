from flask import Blueprint, request, send_from_directory, session
from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from ..models.Patients import Patient, db
from ..services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin
from flask_login import current_user

user_bp = Blueprint('user_bp', __name__)

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

    if request.method == 'GET':

        user = Patient.query.get(id)

        if user is None:
            return WebHelpers.EasyResponse('User with that id does not exist.', 404)

        resp = jsonify(user.serialize())
        resp.status_code = 200

        return resp
    

@user_bp.route('/api/user/<int:id>', methods = ['PUT'])
@login_required
def update_user(id):
    """
    PUT: Deletes user with specified id, then creates user with specified data from form.

    """

    user = Patient.query.filter_by(id = id).first()
    user_name = user.name

    if request.method == 'PUT':
        if user:

            db.session.delete(user)
            db.session.commit()

            name = request.form['name']
            
            user = user(id=id, name=name)

            db.session.add(user)
            db.session.commit()
            logging.info(f'user {user.id} updated.')
            return WebHelpers.EasyResponse(f'{user_name} updated.', 200)

            #return redirect(f'api/user/{id}')

        return WebHelpers.EasyResponse(f'user with that id does not exist.', 404)
    
@user_bp.route('/api/user/<int:id>', methods=['DELETE'])
def delete_user(id):

    user = Patient.query.filter_by(id = id).first()

    if request.method == 'DELETE':
        if user:

            db.session.delete(user)
            db.session.commit()
            
            logging.info(f'{user.name} deleted.')
            return WebHelpers.EasyResponse(f'{user.name} deleted.', 200)

        return WebHelpers.EasyResponse(f'user with that id does not exist.', 404)
    
 

        




        
        


