from audioop import add
from flask import Blueprint, request, send_from_directory

# from .. import login_manager
from flask_login import logout_user, login_required
from sqlalchemy import create_engine, MetaData
import json
from flask import current_app as app, jsonify
from ..models.OrganizationModels import Location, db
from ..services.WebHelpers import WebHelpers
import logging

location_bp = Blueprint("location_bp", __name__)


@location_bp.route("/api/Location", methods=["GET"])
@login_required
def get_Locations():
    """
    GET: Returns all Locations.
    """

    if request.method == "GET":

        Locations = Location.query.all()

        resp = jsonify([x.serialize() for x in Locations])
        resp.status_code = 200

        return resp


@location_bp.route("/api/Location/<int:id>", methods=["GET"])
@login_required
def get_Location(id):
    """
    GET: Returns Location with specified id.
    """

    if request.method == "GET":

        Location = Location.query.get(id)

        if Location is None:
            return WebHelpers.EasyResponse("Location with that id does not exist.", 404)

        resp = jsonify(Location.serialize())
        resp.status_code = 200

        return resp


@location_bp.route("/api/Location/", methods=["POST"])
@login_required
def create_Location():
    """
    POST: Creates new Location.

    To-Do: Implement authorization, i.e. only certain users can make Location.
    """

    if request.method == "GET":
        return WebHelpers.EasyResponse(f"Use GET method to retrive Location.", 405)

    if request.method == "POST":

        name = request.form["name"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]
        city = request.form["city"]
        state = request.form["state"]
        zip_code = request.form["zip_code"]
        provider_id = request.form["provider_id"]

        Location = Location(
            name=name,
            phone_number=phone_number,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            provider_id=provider_id,
        )

        db.session.add(Location)
        db.session.commit()
        logging.debug(f"New Location {Location.name} created.")

        return WebHelpers.EasyResponse(f"New Location {Location.name} created.", 201)


@location_bp.route("/api/Location/<int:id>", methods=["PUT"])
@login_required
def update_Location(id):
    """
    PUT: Deletes Location with specified id, then creates Location with specified data from form.

    """

    Location = Location.query.filter_by(id=id).first()
    Location_name = Location.name

    if request.method == "PUT":
        if Location:

            name = request.form["name"]
            phone_number = request.form["phoneNumber"]
            address = request.form["address"]
            city = request.form["city"]
            state = request.form["state"]
            zip_code = request.form["zipCode"]
            provider_id = request.form["providerId"]

            Location.name = name
            Location.phone_number = phone_number
            Location.address = address
            Location.city = city
            Location.state = state
            Location.zip_code = zip_code
            Location.provider_id = provider_id

            db.session.commit()
            logging.info(f"Location {Location.id} updated.")
            return WebHelpers.EasyResponse(f"{Location_name} updated.", 200)

            # return redirect(f'api/Location/{id}')

        return WebHelpers.EasyResponse(f"Location with that id does not exist.", 404)


@location_bp.route("/api/Location/<int:id>", methods=["DELETE"])
def delete_Location(id):

    Location = Location.query.filter_by(id=id).first()

    if Location:

        db.session.delete(Location)
        db.session.commit()
        # return redirect('/api/Location')
        logging.info(f"{Location.name} deleted.")
        return WebHelpers.EasyResponse(f" deleted the {Location.name} Location.", 200)

    return WebHelpers.EasyResponse(f"Location with that id does not exist.", 404)


@location_bp.route("/api/Location/<int:id>/physicians", methods=["GET"])
def get_Location_physicians(id):

    Location = Location.query.get(id)

    if Location:
        physicians = Location.physicians
        data = jsonify([x.serialize() for x in physicians])
        resp = data
        resp.status_code = 200

        return resp


@location_bp.route("/api/Location/<int:id>/patients", methods=["GET"])
def get_Location_patients(id):

    Location = Location.query.get(id)
    data = {}

    if Location:
        physicians = Location.physicians

        resp = data
        # resp.status_code = 200

        return resp
