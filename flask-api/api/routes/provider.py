from flask import Blueprint, request, send_from_directory
from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app
from ..models.ProviderModels import Provider, db
from ..services.WebHelpers import WebHelpers

provider_bp = Blueprint('provider_bp', __name__)

@provider_bp('/api/provider/<int:id>')
@login_required
def get_provider(id):

    if request.method == 'GET':

        if id == None:
            providers = Provider.query.all()
            return providers
        else:
            provider = Provider.query.get(id)
            return provider
    
    if request.method == 'POST':
        return WebHelpers.EasyResponse(f'Use GET method to retrive provider.', 405)

@provider_bp('/api/provider/')
@login_required
def create_provider():

    if request.method == 'GET':
        return WebHelpers.EasyResponse(f'Use GET method to retrive provider.', 405)

    if request.method == 'POST':

        name = request.form['name']

        provider = Provider(
            name=name
        )

        
        


