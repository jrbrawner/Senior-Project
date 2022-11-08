from flask import Blueprint, request, send_from_directory
from flask import current_app as app, jsonify
from ..models.OrgModels import Organization, Location, User
from api.models.db import db
from ..services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin
from flask_security import login_required, current_user
from api.permissions import Permissions
from flask import session

organization_bp = Blueprint("organization_bp", __name__)


@organization_bp.get("/api/organization")
@login_required
@cross_origin()
def get_organizations():
    """
    GET: Returns organizations depending on user role.\n
    Super Admin - All organizations.
    Admin - Only organization the admin belongs to.
    """
    if current_user.has_permission(Permissions.VIEW_ALL_ORGANIZATIONS):
        organizations = Organization.query.all()
        resp = jsonify([x.serialize() for x in organizations])
        resp.status_code = 200
        logging.info(f"User id {current_user.id} accessed all organizations")
        return resp

    if current_user.has_permission(Permissions.VIEW_CURRENT_ORGANIZATION):
        organization_id = current_user.organization_id
        organization = Organization.query.get(organization_id)
        logging.info(f"User id ({current_user.id}) accessed their organization.")
        # javascript is expecting a list, only one element returned will return a dictionary instead of the list needed
        format = []
        format.append(organization.serialize())
        resp = jsonify(format)
        resp.status_code = 200
        return resp
    else:
        return WebHelpers.EasyResponse('You are not authorized for this functionality.', 403)


@organization_bp.get("/api/organization/<int:id>")
@login_required
@cross_origin()
def get_organization(id):
    """
    GET: Returns Organization with specified id.
    """
    organization = Organization.query.get(id)

    if organization is None:
        return WebHelpers.EasyResponse("Organization with that id does not exist.", 404)

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
    logging.debug(
        f"User id {current_user.id} created new organization id - {organization.id} -"
    )

    return WebHelpers.EasyResponse(
        f"New organization {organization.name} created.", 201
    )


@organization_bp.put("/api/organization/<int:id>")
@login_required
def update_organization(id):
    """
    PUT: Updates specified organization.
    """
    name = request.form["name"]
    twilio_account_id = request.form['twilio_account_id']
    twilio_auth_token = request.form['twilio_auth_token']

    organization = Organization.query.get(id)

    if organization:
        organization.name = name
        organization.twilio_account_id = twilio_account_id
        organization.twilio_auth_token = twilio_auth_token
        db.session.commit()
        logging.info(f"User id {current_user.id} updated organization id - {id} -")
        return WebHelpers.EasyResponse(f"{name} updated.", 200)
    return WebHelpers.EasyResponse(f"Organization with that id does not exist.", 404)


@organization_bp.delete("/api/organization/<int:id>")
def delete_organization(id):

    locations = Location.query.filter_by(organization_id=id).all()

    for i in locations:
        db.session.delete(i)
        db.session.commit()
    
    users = User.query.filter_by(organization_id = id).all()
    for i in users:
        db.session.delete(i)
        db.session.commit()

    organization = Organization.query.get(id)

    if organization:
        db.session.delete(organization)
        db.session.commit()
        logging.info(f"User id {current_user.id} deleted org id - {id} -")
        return WebHelpers.EasyResponse(f"Organization deleted.", 200)
    return WebHelpers.EasyResponse(f"Organization with that id does not exist.", 404)


@organization_bp.get("/api/organization/<int:id>/locations")
def get_organization_locations(id):

    organization = Organization.query.get(id)

    if organization:
        locations = organization.locations
        resp = jsonify([x.serialize_name() for x in locations])
        resp.status_code = 200

        return resp
