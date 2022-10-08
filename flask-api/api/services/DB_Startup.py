from api.models.Users import User, Role
from api.models.db import db
from api import user_datastore
from flask_security.utils import hash_password
import logging
from api.models.OrganizationModels import Organization, Location

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

    if User.query.count() == 0:
        password = hash_password("password")
        admin = user_datastore.create_user(
            name="admin",
            email="admin@email.com",
            password=password,
            organization_id=0,
            location_id=0,
        )
        user_datastore.add_role_to_user(admin, "Super Admin")
        db.session.add(admin)
        db.session.commit()
        logging.warning(
            f"No admin found, default admin account made. Make sure default credentials are changed."
        )
        
    #everything past here is extra for testing purposes
        
    if User.query.count() == 1:

        password = hash_password("password")
        user = user_datastore.create_user(
            name="TestPatient",
            email="testpatient@email.com",
            organization_id=1,
            location_id=1,
            password=password,
            phone_number="+18124536789"
        )
        db.session.add(user)
        db.session.commit()
        user_datastore.add_role_to_user(user, 'Patient')
        user_datastore.commit()
    if User.query.count() == 2:

        password = hash_password("password")
        user = user_datastore.create_user(
            name="TestDoctor",
            email="TestDoctor@email.com",
            organization_id=1,
            location_id=1,
            password=password,
            phone_number="+18124533801"
        )
        db.session.add(user)
        db.session.commit()
        user_datastore.add_role_to_user(user, 'Physician')
        user_datastore.commit()
    if User.query.count() == 3:
        password = hash_password("password")
        user = user_datastore.create_user(
            name="TestAdmin",
            email="TestAdmin@email.com",
            organization_id=1,
            location_id=1,
            password=password,
            phone_number="+18127831029"
        )
        db.session.add(user)
        db.session.commit()
        user_datastore.add_role_to_user(user, 'Admin')
        user_datastore.commit()

    if User.query.count() == 4:
        password = hash_password("password")
        user = user_datastore.create_user(
            name="TestEmployee",
            email="TestEmployee@email.com",
            organization_id=1,
            location_id=1,
            password=password,
            phone_number="+18124581234"
        )
        db.session.add(user)
        db.session.commit()
        user_datastore.add_role_to_user(user, 'Employee')
        user_datastore.commit()
    if User.query.count() == 5:
        password = hash_password("password")
        user = user_datastore.create_user(
            name="Test1Admin",
            email="Test1Admin@email.com",
            organization_id=2,
            location_id=2,
            password=password,
            phone_number="+1812"
        )
        db.session.add(user)
        db.session.commit()
        user_datastore.add_role_to_user(user, 'Admin')
        user_datastore.commit()
    if Organization.query.count() == 0:
        organization = Organization(
            name = 'Healthcare Inc',
            twilio_account_id = 'AC7a914eac1184b21ab730290493c44e8a',
            twilio_auth_token = 'a2bbbe8a858f7e2f4c92ca096c45470c'
        )
        db.session.add(organization)
        db.session.commit()
    if Organization.query.count() == 1:
        organization1 = Organization(
            name = 'Healthcare Overlords',
            twilio_account_id = '',
            twilio_auth_token = ''
        )
        db.session.add(organization1)
        db.session.commit()

    if Location.query.count() == 0:
        location = Location(
            name = 'Clean Eyes',
            phone_number = '+18155510787',
            address = '1001 Banana Republic',
            city = 'Evansville',
            state = 'Indiana',
            zip_code = '47720',
            organization_id = '1'
        )
        db.session.add(location)
        db.session.commit()

    if Location.query.count() == 1:
        location1 = Location(
            name = 'Sweet Water Healthcare',
            phone_number = '+18126789028',
            address = '1000 Test Avenue',
            city = 'Testville',
            state = 'Kentucky',
            zip_code = '47714',
            organization_id = '2'
            )
        db.session.add(location1)
        db.session.commit()

        logging.warning(f"Database seeded.")
