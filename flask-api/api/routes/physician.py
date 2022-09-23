from flask import Blueprint, request, send_from_directory, session
from .. import login_manager
from flask_login import logout_user, login_required, current_user
from sqlalchemy import create_engine, MetaData
from flask import current_app as app, jsonify
from ..models.Physicians import Physician, db
from ..models.Messages import PNumbertoUser
from ..services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin
from flask_login import current_user

physician_bp = Blueprint("physician_bp", __name__)


@physician_bp.route("/api/physician", methods=["GET"])
@login_required
@cross_origin()
def get_physicians():
    """
    GET: Returns all physicians.
    """
    if session["login_type"] == "physician":

        if request.method == "GET":

            physicians = Physician.query.all()

            resp = jsonify([x.serialize() for x in physicians])
            resp.status_code = 200
            logging.info(f"{current_user.name} accessed all physicians.")

            return resp
    else:
        return WebHelpers.EasyResponse("You are not authorized to view this page.", 403)


@physician_bp.route("/api/physician/<int:id>", methods=["GET"])
@login_required
@cross_origin()
def get_physician(id):
    """
    GET: Returns physician with specified id.
    """
    if session["login_type"] == "physician":
        if request.method == "GET":

            physician = Physician.query.get(id)

            if physician is None:
                return WebHelpers.EasyResponse(
                    "physician with that id does not exist.", 404
                )

            resp = jsonify(physician.serialize())
            resp.status_code = 200
            logging.info(f"{current_user.name} accessed physician with id of {id}.")

            return resp
    else:
        return WebHelpers.EasyResponse("You are not authorized to view this page.", 403)


@physician_bp.route("/api/physician/<int:id>", methods=["PUT"])
@login_required
@cross_origin()
def update_physician(id):
    """
    PUT: Deletes physician with specified id, then creates physician with specified data from form.
    """
    if session["login_type"] == "physician":

        physician = Physician.query.filter_by(id=id).first()
        old_name = physician.name

        if request.method == "PUT":
            if physician:

                name = request.form["name"]

                physician.name = str(name)
                db.session.commit()

                logging.warning(
                    f"{current_user.name} updated physician with id {physician.id} name from {old_name} to {physician.name}."
                )
                return WebHelpers.EasyResponse(f"Name updated.", 200)

            return WebHelpers.EasyResponse(
                f"physician with that id does not exist.", 404
            )
    else:
        return WebHelpers.EasyResponse("You are not authorized to view this page.", 403)


@login_required
@cross_origin()
@physician_bp.route("/api/physician/<int:id>", methods=["DELETE"])
def delete_physician(id):

    if session["login_type"] == "physician":

        physician = Physician.query.filter_by(id=id).first()
        physician_name = physician.name
        physician_id = physician.id

        if request.method == "DELETE":
            if physician:

                db.session.delete(physician)
                db.session.commit()

                logging.warning(
                    f"{current_user.name} deleted patient with id {physician_id} and name of {physician_name}."
                )

                return WebHelpers.EasyResponse(f"{physician.name} deleted.", 200)

            return WebHelpers.EasyResponse(
                f"physician with that id does not exist.", 404
            )
    else:
        return WebHelpers.EasyResponse("You are not authorized to view this page.", 403)


@login_required
@cross_origin()
@physician_bp.route("/api/physician/<int:id>/patients", methods=["GET"])
def get_patients(id):

    if session["login_type"] == "physician":

        physician = Physician.query.get(id)

        if physician:
            patients = physician.patients
            resp = jsonify([x.serialize() for x in patients])
            resp.status_code = 200

            return resp
