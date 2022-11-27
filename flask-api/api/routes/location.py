from audioop import add
from flask import Blueprint, request, send_from_directory
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify, url_for
from ..models.OrgModels import Location, Organization
from api.models.db import db
from ..services.WebHelpers import WebHelpers
import logging
from flask_security import current_user
from api.permissions import Permissions


location_bp = Blueprint("location_bp", __name__)


@location_bp.get("/api/location")
@login_required
def get_locations():
    """
    GET: Returns all Locations.

    Super Admin: View All Locations
    Admin: View All Locations in their Organization
    Physician: View Current Locations
    Employee: None at the moment

    """

    # Super Admin
    if current_user.has_permission(Permissions.VIEW_ALL_LOCATIONS):
        locations = Location.query.all()
        resp = jsonify([x.serialize() for x in locations])
        resp.status_code = 200
        logging.info(f"User id - {current_user.id} - accessed all locations.")
        return resp
    # Admin
    if current_user.has_permission(Permissions.VIEW_ALL_CURRENT_ORG_LOCATIONS):
        locations = Location.query.filter_by(
            organization_id=current_user.organization_id
        ).all()
        resp = jsonify([x.serialize() for x in locations])
        resp.status_code = 200
        logging.info(f"User id - {current_user.id} - accessed all current users.")
        return resp
    # Physician
    if current_user.has_permission(Permissions.VIEW_CURRENT_LOCATION):
        locations = current_user.locations
        resp = jsonify([x.serialize() for x in locations])
        resp.status_code = 200
        logging.info(
            f"User id - {current_user.id} - accessed all current employees & patients."
        )
        return resp
    else:
        return WebHelpers.EasyResponse(
            "You are not authorized for this functionality.", 403
        )


@location_bp.get("/api/location/<int:id>")
@login_required
def get_location(id):
    """
    GET: Returns Location with specified id.
    """
    if current_user.has_permission(Permissions.UPDATE_ALL_LOCATIONS):
        location = Location.query.get(id)

        if location is None:
            return WebHelpers.EasyResponse("Location with that id does not exist.", 404)

        resp = jsonify(location.serialize())
        resp.status_code = 200

        return resp
    if current_user.has_permission(Permissions.UPDATE_CURRENT_LOCATION):

        location = Location.query.get(id)

        if location.organization_id == current_user.organization_id:
            if location is None:
                return WebHelpers.EasyResponse(
                    "Location with that id does not exist.", 404
                )

            resp = jsonify(location.serialize())
            resp.status_code = 200

            return resp
        return
    else:
        return WebHelpers.EasyResponse(
            "You are not authorized for this functionality.", 403
        )


@location_bp.post("/api/location")
@login_required
def create_Location():
    """
    POST: Creates new Location.
    """
    # Super admin
    if current_user.has_permission(Permissions.CREATE_NEW_LOCATION_SUPERADMIN):

        organization = request.form["radioGroup"]
        organization_id = Organization.query.filter_by(name=organization).first().id

        name = request.form["name"]
        phone_number = request.form["phoneNumber"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        zip_code = request.form["zipCode"]

        if Location.query.filter_by(phone_number=phone_number).scalar() is None:

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
            logging.debug(
                f"User id - {current_user.id} - created new location id - {location.id} -"
            )
            return WebHelpers.EasyResponse(
                f"New location {location.name} created.", 201
            )
        return WebHelpers.EasyResponse(
            f"Location already exists with that phone number. ", 400
        )

    # Admin
    if current_user.has_permission(Permissions.CREATE_NEW_LOCATION):
        name = request.form["name"]
        phone_number = request.form["phoneNumber"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        zip_code = request.form["zipCode"]
        organization_id = current_user.organization_id

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

        logging.debug(
            f"User id - {current_user.id} - created new location id - {location.id} -"
        )

        return WebHelpers.EasyResponse(f"New location {location.name} created.", 201)
    else:
        return WebHelpers.EasyResponse(
            "You are not authorized for this functionality.", 403
        )


@location_bp.put("/api/location/<int:id>")
@login_required
def update_Location(id):
    """
    PUT: Updates Location with new information.
    """
    if current_user.has_permission(Permissions.UPDATE_ALL_LOCATIONS):
        location = Location.query.filter_by(id=id).first()

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
            # logging.info(f"User id - {current_user.id} - updated location id - {location.id} -")
            return WebHelpers.EasyResponse(f"Location updated.", 200)
    if current_user.has_permission(Permissions.UPDATE_CURRENT_LOCATION):
        location = Location.query.filter_by(id=id).first()
        if location.organization_id == current_user.organization_id:
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
                # logging.info(f"User id - {current_user.id} - updated location id - {location.id} -")
                return WebHelpers.EasyResponse(f"Location updated.", 200)
    else:
        return WebHelpers.EasyResponse(
            "You are not authorized for this functionality.", 403
        )


@location_bp.delete("/api/location/<int:id>")
def delete_Location(id):

    if current_user.has_permission(Permissions.DELETE_ALL_LOCATIONS):
        location = Location.query.get(id)

        if location:

            db.session.delete(location)
            db.session.commit()
            logging.info(f"User id - {current_user.id} - deleted location - {id} -")
            return WebHelpers.EasyResponse(f"Location deleted.", 200)
        return WebHelpers.EasyResponse(f"Location with that id does not exist.", 404)
    if current_user.has_permission(Permissions.DELETE_CURRENT_ORG_LOCATIONS):
        location = Location.query.get(id)
        if location.organization_id == current_user.organization_id:

            if location:
                db.session.delete(location)
                db.session.commit()
                logging.info(f"User id - {current_user.id} - deleted location - {id} -")
                return WebHelpers.EasyResponse(f"Location deleted.", 200)
            return WebHelpers.EasyResponse(
                f"Location with that id does not exist.", 404
            )
    else:
        return WebHelpers.EasyResponse(
            "You are not authorized for this functionality.", 403
        )
