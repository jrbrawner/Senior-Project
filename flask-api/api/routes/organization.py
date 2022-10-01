from flask import Blueprint, request, send_from_directory

# from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from ..models.OrganizationModels import Organization
from api.models.db import db
from ..services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin

organization_bp = Blueprint("organization_bp", __name__)


@organization_bp.route("/api/Organization", methods=["GET"])
@login_required
@cross_origin()
def get_Organizations():
    """
    GET: Returns all Organizations.
    """

    if request.method == "GET":

        Organizations = Organization.query.all()

        resp = jsonify([x.serialize() for x in Organizations])
        resp.status_code = 200

        return resp


@organization_bp.route("/api/Organization/<int:id>", methods=["GET"])
@login_required
@cross_origin()
def get_Organization(id):
    """
    GET: Returns Organization with specified id.
    """

    if request.method == "GET":

        Organization = Organization.query.get(id)

        if Organization is None:
            return WebHelpers.EasyResponse(
                "Organization with that id does not exist.", 404
            )

        resp = jsonify(Organization.serialize())
        resp.status_code = 200

        return resp


@organization_bp.route("/api/Organization", methods=["POST"])
@login_required
def create_Organization():
    """
    POST: Creates new Organization.

    To-Do: Implement authorization, i.e. only certain users can make Organization.
    """

    if request.method == "GET":
        return WebHelpers.EasyResponse(f"Use GET method to retrive Organization.", 405)

    if request.method == "POST":

        name = request.form["name"]
        twilio_account_id = request.form["twilio_account_id"]
        twilio_auth_token = request.form["twilio_auth_token"]

        Organization = Organization(
            name=name,
            twilio_account_id=twilio_account_id,
            twilio_auth_token=twilio_auth_token,
        )

        db.session.add(Organization)
        db.session.commit()
        logging.debug(f"New Organization {Organization.name} created.")

        return WebHelpers.EasyResponse(
            f"New Organization {Organization.name} created.", 201
        )


@organization_bp.route("/api/Organization/<int:id>", methods=["PUT"])
@login_required
def update_Organization(id):
    """
    PUT: Deletes Organization with specified id, then creates Organization with specified data from form.

    """

    Organization = Organization.query.filter_by(id=id).first()
    Organization_name = Organization.name

    if request.method == "PUT":
        if Organization:

            db.session.delete(Organization)
            db.session.commit()

            name = request.form["name"]

            Organization = Organization(id=id, name=name)

            db.session.add(Organization)
            db.session.commit()
            logging.info(f"Organization {Organization.id} updated.")
            return WebHelpers.EasyResponse(f"{Organization_name} updated.", 200)

            # return redirect(f'api/Organization/{id}')

        return WebHelpers.EasyResponse(
            f"Organization with that id does not exist.", 404
        )


@organization_bp.route("/api/Organization/<int:id>", methods=["DELETE"])
def delete_Organization(id):

    Organization = Organization.query.filter_by(id=id).first()

    if request.method == "DELETE":
        if Organization:

            db.session.delete(Organization)
            db.session.commit()
            # return redirect('/api/Organization')
            logging.info(f"{Organization.name} deleted.")
            return WebHelpers.EasyResponse(f"{Organization.name} deleted.", 200)

        return WebHelpers.EasyResponse(
            f"Organization with that id does not exist.", 404
        )


@organization_bp.route("/api/Organization/<int:id>/offices", methods=["GET"])
def get_Organization_offices(id):

    Organization = Organization.query.get(id)

    if Organization:
        offices = Organization.offices

        resp = jsonify([x.serialize() for x in offices])

        resp.status_code = 200

        return resp
