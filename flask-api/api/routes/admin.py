from flask import Blueprint, request, send_from_directory, session
from .. import login_manager
from flask_login import logout_user, login_required, current_user
from sqlalchemy import create_engine, MetaData
from flask import current_app as app, jsonify
from ..models.Admins import Admin, db
from ..models.Messages import PNumbertoUser
from ..services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin
from flask_login import current_user
from ..services.auth.login import admin_required

admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.get("/api/admin")
@admin_required
@cross_origin()
def get_admins():
    """
    Returns all admins.
    """

    admins = Admin.query.all()
    resp = jsonify([x.serialize() for x in admins])
    resp.status_code = 200
    logging.info(f"{current_user.name} accessed all admins.")
    return resp


@admin_bp.get("/api/admin/<int:id>")
@admin_required
@cross_origin()
def get_admin(id):
    """
    GET: Returns admin with specified id.
    """
   
    admin = Admin.query.get(id)
    if admin is None:
        return WebHelpers.EasyResponse(
            "Admin with that id does not exist.", 404
        )
    resp = jsonify(admin.serialize())
    resp.status_code = 200
    logging.info(f"{current_user.name} accessed admin with id of {id}.")

    return resp
    


@admin_bp.put("/api/admin/<int:id>")
@admin_required
@cross_origin()
def update_admin(id):
    """
    PUT: Deletes admin with specified id, then creates admin with specified data from form.
    """
    admin = Admin.query.filter_by(id=id).first()
    old_name = admin.name

    if admin:
        name = request.form["name"]
        admin.name = str(name)
        db.session.commit()

        logging.warning(
            f"{current_user.name} updated admin with id {admin.id} name from {old_name} to {admin.name}."
        )
        return WebHelpers.EasyResponse(f"Name updated.", 200)
    return WebHelpers.EasyResponse(
        f"admin with that id does not exist.", 404
    )
   


@admin_bp.delete("/api/admin/<int:id>")
@admin_required
@cross_origin()
def delete_admin(id):
    """
    Deletes admin with specified id.
    """

    admin = Admin.query.filter_by(id=id).first()
    admin_name = admin.name
    admin_id = admin.id

    if admin:
        db.session.delete(admin)
        db.session.commit()
        logging.warning(
            f"{current_user.name} deleted patient with id {admin_id} and name of {admin_name}."
        )
        return WebHelpers.EasyResponse(f"{admin.name} deleted.", 200)
    return WebHelpers.EasyResponse(
        f"admin with that id does not exist.", 404
    )
    
