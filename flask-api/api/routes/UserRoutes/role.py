from api.models.OrgModels import Role, Permission, User, Organization, Location
from api.models.db import db
from flask import Blueprint, request, jsonify
import logging
from flask_security import current_user
from api.services.WebHelpers import WebHelpers
from api import user_datastore

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

    all_permissions = Permission.query.all()
    formValues = {}

    for i in all_permissions:
        formValues[i.name] = request.form.get(i.name)

    for name,checked in formValues.items():
        if checked == 'on':
            permission = Permission.query.filter_by(name = name).first()
            role.add_permission(role.id, permission.id)
            
    logging.warning(f"User id - {current_user.id} - created new role id - {role.id} -")
    return role.serialize()


@role_bp.put("/api/role/<int:id>")
def update_role(id):

    role = Role.query.get(id)

    if role:
        role_name = request.form["name"]
        role_description = request.form["description"]

        formValues = {}
        all_permissions = Permission.query.all()

        for i in all_permissions:
            formValues[i.name] = request.form.get(i.name)

        permissions = [x.name for x in role.permissions]
        
        for name,checked in formValues.items():
            if checked == 'on':
                if name in permissions:
                    continue
                elif name not in permissions:
                    permission = Permission.query.filter_by(name = name).first()
                    role.add_permission(role.id, permission.id)
            elif checked != 'on':
                # change to list comprehension later
                if name in permissions:
                    permission = Permission.query.filter_by(name = name).first()
                    role.remove_permission(role.id, permission.id)

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

@role_bp.post("/api/user/roles/<int:id>")
def modify_roles(id):

    user = User.query.get(id)
    roles = Role.query.all()
    organization_id = user.organization_id
    formValues = {}
    user_roles = []
    locationValues = {}
    user_locations = []

    locations = Location.query.filter_by(organization_id = organization_id).all()

    for location in user.locations:
        user_locations.append(location.name)

    for role in user.roles:
        user_roles.append(role.name)

    if user:
        for i in roles:
            formValues[i.name] = request.form.get(i.name)
        for i in locations:
            locationValues[i.name] = request.form.get(i.name)

        for name, checked in formValues.items():
            if checked == 'on':
                if name in user_roles:
                    continue
                elif name not in user_roles:
                    user_datastore.add_role_to_user(user, name)
                    db.session.commit()
            elif checked != 'on':
                if name in user_roles:
                    user_datastore.remove_role_from_user(user, name)
                    db.session.commit()

        for name, checked in locationValues.items():
            if checked == 'on':
                if 'Patient' or 'Pending Patient' in user.roles:
                    location = Location.query.filter_by(name=name).first()
                    user.location_id = location.id
                    db.session.commit()
                if name in user_locations:
                    continue
                elif name not in user_locations:
                    location = Location.query.filter_by(name=name).first()
                    user.add_location(user.id, location.id)
                    db.session.commit()
            elif checked != 'on':
                if name in user_locations:
                    location = Location.query.filter_by(name=name).first()
                    user.remove_location(user.id, location.id)
                    db.session.commit()


        return WebHelpers.EasyResponse(f"User Roles updated.", 200)
    return WebHelpers.EasyResponse(f"User not found.", 404)

@role_bp.get("/api/user/new/roles")
def get_available_roles():

    roles = []

    if 'Super Admin' in current_user.roles:
        roles = Role.query.all()
    elif 'Admin' in current_user.roles:
        roles = Role.query.filter(Role.name != 'Super Admin').all()
    elif 'Physician' in current_user.roles:
        roles = Role.query.filter(Role.name != 'Super Admin').filter(Role.name != 'Admin').all()
    elif 'Employee' in current_user.roles:
        roles = Role.query.filter(Role.name != 'Super Admin').filter(Role.name != 'Admin').filter(Role.name != 'Physician').all()

    resp = jsonify([x.serialize() for x in roles])
    resp.status_code = 200
    return resp


