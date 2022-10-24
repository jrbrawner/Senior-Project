from api.models.Users import User, Role, Permission
from api.models.db import db
from api import user_datastore
from flask_security.utils import hash_password
import logging
from api.models.OrganizationModels import Organization, Location
from api.models.Messages import Message
from api.permissions import Permissions

def seed_db():
    """Initial seeding of database on application start up."""

    if Role.query.count() == 0:
        super_admin_role = Role(
            id=1,
            name="Super Admin",
            description="Role for users that manage the platform utilized by organizations.",
        )

        admin_role = Role(
            id=2,
            name="Admin",
            description="Role for users that manage an organizations instance of the platform.",
        )

        physician_role = Role(
            id=3,
            name="Physician",
            description="Role for users that are physicians for an organization.",
        )

        employee_role = Role(
            id=4,
            name="Employee",
            description="Role for users that are employees of an organization.",
        )

        patient_role = Role(
            id=5,
            name="Patient",
            description="Role for users that are patients of an organization.",
        )

        pending_patient_role = Role(
            id=6,
            name="Pending Patient",
            description="Role for users that are patients of an organization, pending approval by a member of the organization.",
        )

        db.session.add(super_admin_role)
        db.session.add(admin_role)
        db.session.add(physician_role)
        db.session.add(employee_role)
        db.session.add(patient_role)
        db.session.add(pending_patient_role)

        db.session.commit()
        logging.warning(f"No roles found, default roles created.")

        # CREATING PERMISSIONS
        view_all_organizations = Permission(
            id=Permissions.VIEW_ALL_ORGANIZATIONS.value,
            name=Permissions.VIEW_ALL_ORGANIZATIONS.name,
            description="Allows the role to view all organization data."
        )

        view_user_organizations = Permission(
            id=Permissions.VIEW_CURRENT_ORGANIZATION.value,
            name=Permissions.VIEW_CURRENT_ORGANIZATION.name,
            description="Allows the role to view the organization they belong to."
        )

        view_specific_organizations = Permission(
            id=Permissions.VIEW_SPECIFIC_ORGANIZATION.value,
            name=Permissions.VIEW_SPECIFIC_ORGANIZATION.name,
            description="Allows the role to view a specific organization."
        )

        create_new_organization = Permission(
            id=Permissions.CREATE_NEW_ORGANIZATION.value,
            name=Permissions.CREATE_NEW_ORGANIZATION.name,
            description="Allows the role to create new organizations."
        )

        update_current_organization = Permission(
            id=Permissions.UPDATE_CURRENT_ORGANIZATION.value,
            name=Permissions.UPDATE_CURRENT_ORGANIZATION.name,
            description="Allows the role to update the organization they belong to."
        )

        update_all_organizations = Permission(
            id=Permissions.UPDATE_ALL_ORGANIZATIONS.value,
            name=Permissions.UPDATE_ALL_ORGANIZATIONS.name,
            description="Allows the role to update all organizations."
        )

        delete_organization = Permission(
            id=Permissions.DELETE_ORGANIZATION.value,
            name=Permissions.DELETE_ORGANIZATION.name,
            description="Allows the role to delete organizations."
        )        

        view_all_people = Permission(
            id=Permissions.VIEW_ALL_PEOPLE.value,
            name=Permissions.VIEW_ALL_PEOPLE.name,
            description="Allows the role to view all people."
        )

        view_all_current_org_people = Permission(
            id=Permissions.VIEW_ALL_CURRENT_ORG_PEOPLE.value,
            name=Permissions.VIEW_ALL_CURRENT_ORG_PEOPLE.name,
            description="Allows the role to view all people that belong to their organization."
        )

        view_all_current_org_employee = Permission(
            id=Permissions.VIEW_ALL_CURRENT_ORG_EMPLOYEE.value,
            name=Permissions.VIEW_ALL_CURRENT_ORG_EMPLOYEE.name,
            description="Allows the role to view all the employees, patients, and pending patients that belong to their organization."
        )

        view_all_current_org_patients = Permission(
            id=Permissions.VIEW_ALL_CURRENT_ORG_PATIENTS.value,
            name=Permissions.VIEW_ALL_CURRENT_ORG_PATIENTS.name,
            description="Allows the role to view all the patients and pending patients that belong to their organization."
        )

        view_all_messages = Permission(
            id=Permissions.VIEW_ALL_MESSAGES.value,
            name=Permissions.VIEW_ALL_MESSAGES.name,
            description="Allows the role to view all messages sent & received on the platform."
        )

        view_all_current_org_messages = Permission(
            id=Permissions.VIEW_ALL_CURRENT_ORG_MESSAGES.value,
            name=Permissions.VIEW_ALL_CURRENT_ORG_MESSAGES.name,
            description="Allows the role to view all messages sent & received by their current organization."
        )

        view_all_current_location_messages = Permission(
            id=Permissions.VIEW_ALL_CURRENT_LOCATION_MESSAGES.value,
            name=Permissions.VIEW_ALL_CURRENT_LOCATION_MESSAGES.name,
            description="Allows the role to view all the messages sent & received by their current location."
        )

        db.session.add(view_all_organizations)
        db.session.add(view_user_organizations)
        db.session.add(view_specific_organizations)
        db.session.add(create_new_organization)
        db.session.add(update_current_organization)
        db.session.add(update_all_organizations)
        db.session.add(delete_organization)
        db.session.add(view_all_people)
        db.session.add(view_all_current_org_employee)
        db.session.add(view_all_current_org_people)
        db.session.add(view_all_current_org_patients)
        db.session.add(view_all_messages)
        db.session.add(view_all_current_org_messages)
        db.session.add(view_all_current_location_messages)
        db.session.commit()
        ###ADD PERMISSIONS TO APPROPRIATE ROLES
        #MAKE SURE TO SAVE THIS PART

        #SUPERADMIN ROLE
        super_admin_role.add_permission(super_admin_role.id, Permissions.VIEW_ALL_ORGANIZATIONS.value)
        super_admin_role.add_permission(super_admin_role.id, Permissions.VIEW_ALL_PEOPLE.value)
        super_admin_role.add_permission(super_admin_role.id, Permissions.VIEW_ALL_MESSAGES.value)
        #ADMIN ROLE
        admin_role.add_permission(admin_role.id, Permissions.VIEW_CURRENT_ORGANIZATION.value)
        admin_role.add_permission(admin_role.id, Permissions.VIEW_ALL_CURRENT_ORG_PEOPLE.value)
        #PHYSICIAN ROLE
        physician_role.add_permission(physician_role.id, Permissions.VIEW_ALL_CURRENT_ORG_EMPLOYEE.value)
        physician_role.add_permission(physician_role.id, Permissions.VIEW_ALL_CURRENT_ORG_MESSAGES.value)
        #EMPLOYEE ROLE
        employee_role.add_permission(employee_role.id, Permissions.VIEW_ALL_CURRENT_ORG_PATIENTS.value)
        employee_role.add_permission(employee_role.id, Permissions.VIEW_ALL_CURRENT_LOCATION_MESSAGES.value)



    if User.query.count() == 0:
        password = hash_password("password")
        admin = user_datastore.create_user(
            name="admin",
            email="admin@email.com",
            password=password,
            organization_id=1,
            location_id=1,
        )

        user_datastore.add_role_to_user(admin, "Super Admin")
        db.session.add(admin)
        db.session.commit()
        logging.warning(
            f"No admin found, default admin account made. Make sure default credentials are changed."
        )


    if Organization.query.count() == 0:
        organization = Organization(
            name="Platform Owner",
            twilio_account_id="",
            twilio_auth_token="",
        )
        db.session.add(organization)
        db.session.commit()

    if Location.query.count() == 0:
        location = Location(
            name="Corporate HQ",
            phone_number="+18124671234",
            address="1234 Corporate Lane",
            city="Evansville",
            state="Indiana",
            zip_code="47720",
            organization_id=1,
        )
        db.session.add(location)
        db.session.commit()



    # everything past here is extra for testing purposes
    if Organization.query.count() == 1:
        organization1 = Organization(
            name="Healthcare Overlords", twilio_account_id="", twilio_auth_token=""
        )
        db.session.add(organization1)
        db.session.commit()

    if Organization.query.count() == 2:
        organization2 = Organization(
            name="Organzation 2", twilio_account_id="blablabla", twilio_auth_token="blablabla"
        )
        db.session.add(organization2)
        db.session.commit()

    if Location.query.count() == 1:
        location = Location(
            name="Clean Eyes",
            phone_number="+18155510787",
            address="1001 Banana Republic",
            city="Evansville",
            state="Indiana",
            zip_code="47720",
            organization_id=2,
        )
        db.session.add(location)
        db.session.commit()

    if Location.query.count() == 2:
        location1 = Location(
            name="Sweet Water Healthcare",
            phone_number="+18126789028",
            address="1000 Test Avenue",
            city="Testville",
            state="Kentucky",
            zip_code="47714",
            organization_id=3,
        )
        db.session.add(location1)
        db.session.commit()

    #if User.query.count() == 1:
    #
    #    password = hash_password("password")
    #    user = user_datastore.create_user(
    #        name="testpatient",
    #        email="testpatient@email.com",
    #        organization_id=2,
    #        location_id=2,
    #        password=password,
    #        phone_number="+18124536789",
    #    )
    #    db.session.add(user)
    #    db.session.commit()
    #    user_datastore.add_role_to_user(user, "Patient")
    #    user_datastore.commit()
    if User.query.count() == 2:

        password = hash_password("password")
        user = user_datastore.create_user(
            name="TestDoctor",
            email="testdoctor@email.com",
            organization_id=2,
            location_id=2,
            password=password,
            phone_number="+18124533801",
        )
        db.session.add(user)
        db.session.commit()
        user_datastore.add_role_to_user(user, "Physician")
        user_datastore.commit()


    if User.query.count() == 3:
        password = hash_password("password")
        user = user_datastore.create_user(
            name="TestAdmin",
            email="testadmin@email.com",
            organization_id=2,
            location_id=2,
            password=password,
            phone_number="+18127831029",
        )
        db.session.add(user)
        db.session.commit()
        user_datastore.add_role_to_user(user, "Admin")
        user_datastore.commit()

    if User.query.count() == 4:
        password = hash_password("password")
        user = user_datastore.create_user(
            name="TestEmployee",
            email="testemployee@email.com",
            organization_id=2,
            location_id=2,
            password=password,
            phone_number="+18124581234",
        )
        db.session.add(user)
        db.session.commit()
        user_datastore.add_role_to_user(user, "Employee")
        user_datastore.commit()
    if User.query.count() == 5:
        password = hash_password("password")
        user = user_datastore.create_user(
            name="Test1Admin",
            email="test1admin@email.com",
            organization_id=2,
            location_id=3,
            password=password,
            phone_number="+1812",
        )
        db.session.add(user)
        db.session.commit()
        user_datastore.add_role_to_user(user, "Admin")
        user_datastore.commit()


        logging.warning(f"Database seeded.")

