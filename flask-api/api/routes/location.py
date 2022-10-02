from audioop import add
from flask import Blueprint, request, send_from_directory
# from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify, url_for
from ..models.OrganizationModels import Location
from api.models.db import db
from ..services.WebHelpers import WebHelpers
import logging
from flask_security import current_user


location_bp = Blueprint("location_bp", __name__)


@location_bp.get("/api/location")
@login_required
def get_locations():
    """
    GET: Returns all Locations.
    """

    Locations = Location.query.all()

    resp = jsonify([x.serialize() for x in Locations])
    resp.status_code = 200

    return resp


@location_bp.get("/api/location/<int:id>")
@login_required
def get_Location(id):
    """
    GET: Returns Location with specified id.
    """

    location = Location.query.get(id)

    if location is None:
        return WebHelpers.EasyResponse("Location with that id does not exist.", 404)

    resp = jsonify(location.serialize())
    resp.status_code = 200

    return resp


@location_bp.post("/api/location")
@login_required
def create_Location():
    """
    POST: Creates new Location.
    """

    name = request.form["name"]
    phone_number = request.form["phone_number"]
    address = request.form["address"]
    city = request.form["city"]
    state = request.form["state"]
    zip_code = request.form["zip_code"]
    organization_id = request.form["organization_id"]

    location = Location(
        name=name,
        phone_number=phone_number,
        address=address,
        city=city,
        state=state,
        zip_code=zip_code,
        organization_id=organization_id,
    )

    db.session.add(location)
    db.session.commit()
    logging.debug(f"User id - {current_user.id} - created new location id - {location.id} -")

    return WebHelpers.EasyResponse(f"New location {location.name} created.", 201)


@location_bp.put("/api/location/<int:id>")
@login_required
def update_Location(id):
    """
    PUT: Updates Location with new information.
    """

    location = Location.query.filter_by(id=id).first()
    location_name = location.name

    if location:

        name = request.form["name"]
        phone_number = request.form["phoneNumber"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        zip_code = request.form["zipCode"]
        organization_id = request.form["organizationId"]

        location.name = name
        location.phone_number = phone_number
        location.address = address
        location.city = city
        location.state = state
        location.zip_code = zip_code
        location.organization_id = organization_id

        db.session.commit()
        #logging.info(f"User id - {current_user.id} - updated location id - {location.id} -")
        return url_for('location_bp.get_locations')


@location_bp.delete("/api/location/<int:id>")
def delete_Location(id):

    location = Location.query.get(id)

    if location:

        db.session.delete(location)
        db.session.commit()
        logging.info(f"User id - {current_user.id} - deleted location - {id} -")
        return WebHelpers.EasyResponse(f"Location deleted.", 200)
    return WebHelpers.EasyResponse(f"Location with that id does not exist.", 404)
