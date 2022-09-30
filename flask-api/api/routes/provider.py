from flask import Blueprint, request, send_from_directory
#from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from ..models.ProviderModels import Provider, db
from ..services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin

provider_bp = Blueprint("provider_bp", __name__)


@provider_bp.route("/api/provider", methods=["GET"])
@login_required
@cross_origin()
def get_providers():
    """
    GET: Returns all providers.
    """

    if request.method == "GET":

        providers = Provider.query.all()

        resp = jsonify([x.serialize() for x in providers])
        resp.status_code = 200

        return resp


@provider_bp.route("/api/provider/<int:id>", methods=["GET"])
@login_required
@cross_origin()
def get_provider(id):
    """
    GET: Returns provider with specified id.
    """

    if request.method == "GET":

        provider = Provider.query.get(id)

        if provider is None:
            return WebHelpers.EasyResponse("Provider with that id does not exist.", 404)

        resp = jsonify(provider.serialize())
        resp.status_code = 200

        return resp


@provider_bp.route("/api/provider", methods=["POST"])
@login_required
def create_provider():
    """
    POST: Creates new provider.

    To-Do: Implement authorization, i.e. only certain users can make provider.
    """

    if request.method == "GET":
        return WebHelpers.EasyResponse(f"Use GET method to retrive provider.", 405)

    if request.method == "POST":

        name = request.form["name"]
        twilio_account_id = request.form["twilio_account_id"]
        twilio_auth_token = request.form["twilio_auth_token"]

        provider = Provider(
            name=name,
            twilio_account_id=twilio_account_id,
            twilio_auth_token=twilio_auth_token,
        )

        db.session.add(provider)
        db.session.commit()
        logging.debug(f"New provider {provider.name} created.")

        return WebHelpers.EasyResponse(f"New provider {provider.name} created.", 201)


@provider_bp.route("/api/provider/<int:id>", methods=["PUT"])
@login_required
def update_provider(id):
    """
    PUT: Deletes provider with specified id, then creates provider with specified data from form.

    """

    provider = Provider.query.filter_by(id=id).first()
    provider_name = provider.name

    if request.method == "PUT":
        if provider:

            db.session.delete(provider)
            db.session.commit()

            name = request.form["name"]

            provider = Provider(id=id, name=name)

            db.session.add(provider)
            db.session.commit()
            logging.info(f"Provider {provider.id} updated.")
            return WebHelpers.EasyResponse(f"{provider_name} updated.", 200)

            # return redirect(f'api/provider/{id}')

        return WebHelpers.EasyResponse(f"Provider with that id does not exist.", 404)


@provider_bp.route("/api/provider/<int:id>", methods=["DELETE"])
def delete_provider(id):

    provider = Provider.query.filter_by(id=id).first()

    if request.method == "DELETE":
        if provider:

            db.session.delete(provider)
            db.session.commit()
            # return redirect('/api/provider')
            logging.info(f"{provider.name} deleted.")
            return WebHelpers.EasyResponse(f"{provider.name} deleted.", 200)

        return WebHelpers.EasyResponse(f"Provider with that id does not exist.", 404)


@provider_bp.route("/api/provider/<int:id>/offices", methods=["GET"])
def get_provider_offices(id):

    provider = Provider.query.get(id)

    if provider:
        offices = provider.offices

        resp = jsonify([x.serialize() for x in offices])

        resp.status_code = 200

        return resp
