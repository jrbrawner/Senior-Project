from api.models.OrgModels import Role, Permission
from api.models.db import db
from flask import Blueprint, request, jsonify
import logging
from flask_security import current_user
from api.services.WebHelpers import WebHelpers

role_bp = Blueprint("role_bp", __name__)


@role_bp.get("/api/role/<int:id>")
def get_role(id):

    role = Role.query.get(id)
    if role:
        logging.info(f"User id - {current_user.id} - accessed role id - {role.id} -")
        resp = jsonify(role.serialize_p())
        resp.status_code = 200
        return resp
    return WebHelpers.EasyResponse(f"Role with id {id} doesnt exist.", 404)


@role_bp.get("/api/role")
def get_roles():

    role = Role.query.all()
    logging.info(f"User id - {current_user.id} accessed all roles.")
    roles = [x.serialize() for x in role]
    resp = jsonify(roles)
    resp.status_code = 200
    return resp


@role_bp.post("/api/role")
def create_role():

    role_name = request.form["name"]
    role_description = request.form["description"]
    

    role = Role(name=role_name, description=role_description)

    db.session.add(role)
    db.session.commit()
    logging.warning(f"User id - {current_user.id} - created new role id - {role.id} -")
    return role.serialize()


@role_bp.put("/api/role/<int:id>")
def update_role(id):

    role = Role.query.get(id)

    if role:
        role_name = request.form["name"]
        role_description = request.form["description"]

        # :(
        permissions_selected = {
            "VIEW_ALL_ORGANIZATIONS": request.form.get("VIEW_ALL_ORGANIZATIONS"),
            "VIEW_CURRENT_ORGANIZATION": request.form.get("VIEW_CURRENT_ORGANIZATION"),
            "VIEW_SPECIFIC_ORGANIZATION": request.form.get("VIEW_SPECIFIC_ORGANIZATION"),
            "CREATE_NEW_ORGANIZATION": request.form.get("CREATE_NEW_ORGANIZATION"),
            "UPDATE_CURRENT_ORGANIZATION": request.form.get("UPDATE_CURRENT_ORGANIZATION"),
            "UPDATE_ALL_ORGANIZATIONS": request.form.get("UPDATE_ALL_ORGANIZATIONS"),
            "DELETE_ORGANIZATION": request.form.get("DELETE_ORGANIZATION"),
            "VIEW_ALL_PEOPLE": request.form.get("VIEW_ALL_PEOPLE"),
            "VIEW_ALL_CURRENT_ORG_PEOPLE": request.form.get("VIEW_ALL_CURRENT_ORG_PEOPLE"),
            "VIEW_ALL_CURRENT_ORG_EMPLOYEE": request.form.get("VIEW_ALL_CURRENT_ORG_EMPLOYEE"),
            "VIEW_ALL_CURRENT_ORG_PATIENTS": request.form.get("VIEW_ALL_CURRENT_ORG_PATIENTS"),
            "VIEW_ALL_MESSAGES": request.form.get("VIEW_ALL_MESSAGES"),
            "VIEW_ALL_CURRENT_ORG_MESSAGES": request.form.get("VIEW_ALL_CURRENT_ORG_MESSAGES"),
            "VIEW_ALL_CURRENT_LOCATION_MESSAGES": request.form.get("VIEW_ALL_CURRENT_LOCATION_MESSAGES"),
            "SEND_ANNOUNCEMENT": request.form.get("SEND_ANNOUNCEMENT"),
            "VIEW_ALL_LOCATIONS": request.form.get("VIEW_ALL_LOCATIONS"),
            "VIEW_ALL_CURRENT_ORG_LOCATIONS": request.form.get("VIEW_ALL_CURRENT_ORG_LOCATIONS"),
            "VIEW_CURRENT_LOCATION": request.form.get("VIEW_CURRENT_LOCATION"),
            "CREATE_NEW_LOCATION": request.form.get("CREATE_NEW_LOCATION"),
            "UPDATE_CURRENT_LOCATION": request.form.get("UPDATE_CURRENT_LOCATION"),
            "UPDATE_ALL_LOCATIONS": request.form.get("UPDATE_ALL_LOCATIONS"),
            "DELETE_LOCATION": request.form.get("DELETE_LOCATION")
        }
        ###################NEED TO FINISH
        for name,checked in permissions_selected.items():
            permission_id = Permission.query.filter_by(name = name)
            if checked == 'on':
                for x in role.permissions:
                    if name not in [j.serialize_name() for j in x]:
                        role.add_permission(id, permission_id)
            else:
                # change to list comprehension later
                for x in role.permissions:
                    if name in [j.serialize_name() for j in x]:
                        role.remove_permission(id, permission_id)

        role.name = role_name
        role.description = role_description
        db.session.commit()

        logging.warning(f"User id - {current_user.id} - modified role - {role.id} -")
        return WebHelpers.EasyResponse(f"Role id {role.id} updated.", 200)
    return WebHelpers.EasyResponse(f"Role with id {id} does not exist.", 404)


@role_bp.delete("/api/role/<int:id>")
def delete_role(id):

    role = Role.query.get(id)

    if role:
        db.session.delete(role)
        db.session.commit()
        logging.warning(f"User id - {current_user.id} - deleted role - {id} -")
        return WebHelpers.EasyResponse(f"Role deleted.", 200)
    return WebHelpers.EasyResponse(f"Role with id {id} does not exist.", 404)


@role_bp.get("/api/permission")
def get_permissions():

    permissions = Permission.query.all()

    resp = jsonify([x.serialize() for x in permissions])
    resp.status_code = 200

    return resp
