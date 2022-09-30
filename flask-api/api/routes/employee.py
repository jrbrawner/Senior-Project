from flask import Blueprint, request, send_from_directory, session
from .. import login_manager
from flask_login import logout_user, login_required, current_user
from sqlalchemy import create_engine, MetaData
from flask import current_app as app, jsonify
from ..models import db
from ..models.Users import User as Employee
from ..models.Messages import PNumbertoUser
from ..services.WebHelpers import WebHelpers
import logging
from flask_cors import cross_origin
from flask_login import current_user
from ..services.auth.login import physician_required

employee_bp = Blueprint("employee_bp", __name__)


@employee_bp.get("/api/employee")
@physician_required
@cross_origin()
def get_employees():
    """
    Returns all employees.
    """

    employees = Employee.query.all()
    resp = jsonify([x.serialize() for x in employees])
    resp.status_code = 200
    logging.info(f"{current_user.name} accessed all employees.")
    return resp


@employee_bp.get("/api/employee/<int:id>")
@physician_required
@cross_origin()
def get_employee(id):
    """
    GET: Returns employee with specified id.
    """

    employee = Employee.query.get(id)
    if employee is None:
        return WebHelpers.EasyResponse("Employee with that id does not exist.", 404)
    resp = jsonify(employee.serialize())
    resp.status_code = 200
    logging.info(f"{current_user.name} accessed employee with id of {id}.")

    return resp


@employee_bp.put("/api/employee/<int:id>")
@physician_required
@cross_origin()
def update_employee(id):
    """
    PUT: Deletes employee with specified id, then creates employee with specified data from form.
    """
    employee = Employee.query.filter_by(id=id).first()
    old_name = employee.name

    if employee:
        name = request.form["name"]
        employee.name = str(name)
        db.session.commit()

        logging.warning(
            f"{current_user.name} updated employee with id {employee.id} name from {old_name} to {employee.name}."
        )
        return WebHelpers.EasyResponse(f"Name updated.", 200)
    return WebHelpers.EasyResponse(f"employee with that id does not exist.", 404)


@employee_bp.delete("/api/employee/<int:id>")
@physician_required
@cross_origin()
def delete_employee(id):
    """
    Deletes employee with specified id.
    """

    employee = Employee.query.filter_by(id=id).first()
    employee_name = employee.name
    employee_id = employee.id

    if employee:
        db.session.delete(employee)
        db.session.commit()
        logging.warning(
            f"{current_user.name} deleted patient with id {employee_id} and name of {employee_name}."
        )
        return WebHelpers.EasyResponse(f"{employee.name} deleted.", 200)
    return WebHelpers.EasyResponse(f"employee with that id does not exist.", 404)
