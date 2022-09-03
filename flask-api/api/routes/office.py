from audioop import add
from flask import Blueprint, request, send_from_directory
from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from ..models.ProviderModels import Office, db
from ..services.WebHelpers import WebHelpers
import logging

office_bp = Blueprint('office_bp', __name__)

@office_bp.route('/api/office', methods = ['GET'])
@login_required
def get_offices():
    """
    GET: Returns all offices.
    """

    if request.method == 'GET':
        data = {}
        offices = Office.query.all()
        counter = 1

        for i in offices:
            data[f'office{counter}'] = i.serialize()
            counter += 1

        resp = jsonify(data)
        resp.status_code = 200

        return resp
    

@office_bp.route('/api/office/<int:id>', methods = ['GET'])
@login_required
def get_office(id):
    """
    GET: Returns office with specified id.
    """

    if request.method == 'GET':

        office = Office.query.get(id)

        if office is None:
            return WebHelpers.EasyResponse('Office with that id does not exist.', 404)

        resp = jsonify(office.serialize())
        resp.status_code = 200

        return resp
    

@office_bp.route('/api/office/', methods = ['POST'])
@login_required
def create_office():
    """
    POST: Creates new office.

    To-Do: Implement authorization, i.e. only certain users can make office.
    """

    if request.method == 'GET':
        return WebHelpers.EasyResponse(f'Use GET method to retrive office.', 405)

    if request.method == 'POST':

        name = request.form['name']
        phone_number = request.form['phone_number']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip_code'] 
        provider_id = request.form['provider_id']


        office = Office(
            name=name,
            phone_number=phone_number,
            address=address,
            city=city,
            state=state,
            zip_code = zip_code,
            provider_id = provider_id
        )

        db.session.add(office)
        db.session.commit()
        logging.debug(f'New office {office.name} created.')

        return WebHelpers.EasyResponse(f'New office {office.name} created.', 201)

@office_bp.route('/api/office/<int:id>', methods = ['PUT'])
@login_required
def update_office(id):
    """
    PUT: Deletes office with specified id, then creates office with specified data from form.

    """

    office = Office.query.filter_by(id = id).first()
    office_name = office.name

    if request.method == 'PUT':
        if office:

            db.session.delete(office)
            db.session.commit()

            name = request.form['name']
            phone_number = request.form['phone_number']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            zip_code = request.form['zip_code']
            provider_id = request.form['provider_id']

            office = Office(
                name=name,
                phone_number=phone_number,
                address=address,
                city=city,
                state=state,
                zip_code=zip_code,
                provider_id = provider_id
            )
            
            db.session.add(office)
            db.session.commit()
            logging.info(f'office {office.id} updated.')
            return WebHelpers.EasyResponse(f'{office_name} updated.', 200)

            #return redirect(f'api/office/{id}')

        return WebHelpers.EasyResponse(f'Office with that id does not exist.', 404)
    
@office_bp.route('/api/office/<int:id>', methods=['DELETE'])
def delete_office(id):

    office = Office.query.filter_by(id = id).first()

    if request.method == 'DELETE':
        if office:

            db.session.delete(office)
            db.session.commit()
            #return redirect('/api/office')
            logging.info(f'{office.name} deleted.')
            return WebHelpers.EasyResponse(f'{office.name} deleted.', 200)

        return WebHelpers.EasyResponse(f'Office with that id does not exist.', 404)
    
 

        




        
        


