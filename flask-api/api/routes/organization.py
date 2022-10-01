from flask import Blueprint, request, send_from_directory
from flask_security import login_required
from flask import current_app as app, jsonify
from ..models.OrganizationModels import Organization
from api.models.db import db
from ..services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin
from flask_security import current_user

organization_bp = Blueprint("organization_bp", __name__)

@organization_bp.get("/api/organization")
@login_required
@cross_origin()
def get_Organizations():
    """
    GET: Returns all Organizations.
    """
    Organizations = Organization.query.all()

    resp = jsonify([x.serialize() for x in Organizations])
    resp.status_code = 200
    logging.info(f"User id {current_user.id} accessed all organizations")

    return resp


@organization_bp.get("/api/organization/<int:id>")
@login_required
@cross_origin()
def get_organization(id):
    """
    GET: Returns Organization with specified id.
    """
    organization = Organization.query.get(id)

    if organization is None:
        return WebHelpers.EasyResponse(
            "Organization with that id does not exist.", 404
        )


    resp = jsonify(organization.serialize())
    resp.status_code = 200
    logging.info(f"User id - {current_user.id} - accessed organization id - {id} - ")
    return resp


@organization_bp.post("/api/organization")
@login_required
def create_organization():
    """
    POST: Creates new Organization.
    """

    name = request.form["name"]
    twilio_account_id = request.form["twilio_account_id"]
    twilio_auth_token = request.form["twilio_auth_token"]

    organization = Organization(
        name=name,
        twilio_account_id=twilio_account_id,
        twilio_auth_token=twilio_auth_token,
    )

    db.session.add(organization)
    db.session.commit()
    logging.debug(f"User id {current_user.id} created new organization id - {organization.id} -")

    return WebHelpers.EasyResponse(
        f"New organization {organization.name} created.", 201
    )


@organization_bp.put("/api/organization")
@login_required
def update_organization():
    """
    PUT: Updates specified organization.
    """
    name = request.form["name"]
    org_id = request.form['id']

    organization = Organization.query.filter_by(id=org_id).first()
    
    if organization:
        organization.name = name
        db.session.commit()
        logging.info(f"User id {current_user.id} updated organization id - {org_id} -")
        return WebHelpers.EasyResponse(f"{name} updated.", 200)
    return WebHelpers.EasyResponse(
        f"Organization with that id does not exist.", 404
    )

@organization_bp.delete("/api/organization/<int:id>")
def delete_organization(id):
    organization = Organization.query.filter_by(id=id).first()

    if organization:
        db.session.delete(organization)
        db.session.commit()
        logging.info(f"User id {current_user.id} deleted org id - {id} -")
        return WebHelpers.EasyResponse(f"Organization deleted.", 200)
    return WebHelpers.EasyResponse(
        f"Organization with that id does not exist.", 404
    )


@organization_bp.get("/api/organization/<int:id>/locations")
def get_organization_locations(id):

    organization = Organization.query.get(id)

    if organization:
        locations = Organization.Locations
        resp = jsonify([x.serialize() for x in locations])
        resp.status_code = 200

        return resp
