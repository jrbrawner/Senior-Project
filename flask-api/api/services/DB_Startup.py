from venv import create
from api.models.OrgModels import User, Role, Permission
from api.models.db import db
from api import user_datastore
from flask_security.utils import hash_password
import logging
from api.models.OrgModels import Organization, Location, User, Role, Permission
from api.models.Messages import Message
from api.permissions import Permissions
from datetime import datetime

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

        # ORGANIZATIONS
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

        #LOCATIONS

        view_all_locations = Permission(
            id=Permissions.VIEW_ALL_LOCATIONS.value,
            name=Permissions.VIEW_ALL_LOCATIONS.name,
            description="Allows the role to view all locations."
        )

        view_current_location = Permission(
            id=Permissions.VIEW_CURRENT_LOCATION.value,
            name=Permissions.VIEW_CURRENT_LOCATION.name,
            description="Allows the role to view the location they belong to."
        )

        view_current_org_locations = Permission(
            id=Permissions.VIEW_ALL_CURRENT_ORG_LOCATIONS.value,
            name=Permissions.VIEW_ALL_CURRENT_ORG_LOCATIONS.name,
            description="Allows the role to view all locations owned by their current organization."
        )

        create_new_location = Permission(
            id=Permissions.CREATE_NEW_LOCATION.value,
            name=Permissions.CREATE_NEW_LOCATION.name,
            description="Allows the role to create new locations."
        )

        update_current_location= Permission(
            id=Permissions.UPDATE_CURRENT_LOCATION.value,
            name=Permissions.UPDATE_CURRENT_LOCATION.name,
            description="Allows the role to update the location they belong to."
        )

        update_all_locations = Permission(
            id=Permissions.UPDATE_ALL_LOCATIONS.value,
            name=Permissions.UPDATE_ALL_LOCATIONS.name,
            description="Allows the role to update all locations."
        )

        delete_location = Permission(
            id=Permissions.DELETE_LOCATION.value,
            name=Permissions.DELETE_LOCATION.name,
            description="Allows the role to delete locations."
        )


        # PEOPLE
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

        # MESSAGES
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

        send_announcement = Permission(
            id=Permissions.SEND_ANNOUNCEMENT.value,
            name=Permissions.SEND_ANNOUNCEMENT.name,
            description="Allows the role to send an announcement to all users of a location."
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
        db.session.add(send_announcement)

        db.session.add(view_all_locations)
        db.session.add(view_current_location)
        db.session.add(create_new_location)
        db.session.add(delete_location)
        db.session.add(update_all_locations)
        db.session.add(update_current_location)
        db.session.add(view_current_org_locations)
        db.session.commit()
        ###ADD PERMISSIONS TO APPROPRIATE ROLES
        #MAKE SURE TO SAVE THIS PART

        #SUPERADMIN ROLE
        super_admin_role.add_permission(super_admin_role.id, Permissions.VIEW_ALL_ORGANIZATIONS.value)
        super_admin_role.add_permission(super_admin_role.id, Permissions.VIEW_ALL_PEOPLE.value)
        super_admin_role.add_permission(super_admin_role.id, Permissions.VIEW_ALL_MESSAGES.value)
        super_admin_role.add_permission(super_admin_role.id, Permissions.VIEW_ALL_LOCATIONS.value)
        #ADMIN ROLE
        admin_role.add_permission(admin_role.id, Permissions.VIEW_CURRENT_ORGANIZATION.value)
        admin_role.add_permission(admin_role.id, Permissions.VIEW_ALL_CURRENT_ORG_PEOPLE.value)
        admin_role.add_permission(admin_role.id, Permissions.VIEW_ALL_CURRENT_ORG_LOCATIONS.value)
        #PHYSICIAN ROLE
        physician_role.add_permission(physician_role.id, Permissions.VIEW_ALL_CURRENT_ORG_EMPLOYEE.value)
        physician_role.add_permission(physician_role.id, Permissions.VIEW_ALL_CURRENT_ORG_MESSAGES.value)
        physician_role.add_permission(physician_role.id, Permissions.VIEW_CURRENT_LOCATION.value)
        physician_role.add_permission(physician_role.id, Permissions.SEND_ANNOUNCEMENT.value)
        #EMPLOYEE ROLE
        employee_role.add_permission(employee_role.id, Permissions.VIEW_ALL_CURRENT_ORG_PATIENTS.value)
        employee_role.add_permission(employee_role.id, Permissions.VIEW_ALL_CURRENT_LOCATION_MESSAGES.value)
        



    if User.query.count() == 0:
        password = hash_password("password")
        admin = user_datastore.create_user(
            name="admin",
            email="admin@email.com",
            phone_number="+18129909999",
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
    if User.query.count() == 1:

        password = hash_password("password")
        user = user_datastore.create_user(
            name="TestDoctor",
            email="testdoctor@email.com",
            organization_id=2,
            location_id=2,
            password=password,
            phone_number="+1812453",
        )
        db.session.add(user)
        db.session.commit()

        user.add_location(user.id, 2)

        user_datastore.add_role_to_user(user, "Physician")
        user_datastore.commit()


    if User.query.count() == 2:
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
        user.add_location(user.id, 2)
        user_datastore.add_role_to_user(user, "Admin")
        user_datastore.commit()

    if User.query.count() == 3:
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
        user.add_location(user.id, 2)
        user_datastore.add_role_to_user(user, "Employee")
        user_datastore.commit()

    if User.query.count() == 4:
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
        user.add_location(user.id, 3)
        user_datastore.add_role_to_user(user, "Admin")
        user_datastore.commit()


        logging.warning(f"Database seeded.")

    """
    #Messages for testing
    
    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=25,
        name="Test P25",
        email="testpati3ent25@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99925",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1003,
        sender_id=25,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1004,
        sender_id=None,
        location_id=2,
        recipient_id=25,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=26,
        name="Test P26",
        email="testpati3ent26@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99926",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1005,
        sender_id=26,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1006,
        sender_id=None,
        location_id=2,
        recipient_id=26,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=27,
        name="Test P27",
        email="testpati3ent27@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99927",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1007,
        sender_id=27,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1008,
        sender_id=None,
        location_id=2,
        recipient_id=27,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=28,
        name="Test P28",
        email="testpati3ent28@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99928",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1009,
        sender_id=28,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1010,
        sender_id=None,
        location_id=2,
        recipient_id=28,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=29,
        name="Test P29",
        email="testpati3ent29@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99929",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1011,
        sender_id=29,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1012,
        sender_id=None,
        location_id=2,
        recipient_id=29,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=30,
        name="Test P30",
        email="testpati3ent30@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99930",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1013,
        sender_id=30,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1014,
        sender_id=None,
        location_id=2,
        recipient_id=30,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=31,
        name="Test P31",
        email="testpati3ent31@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99931",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1015,
        sender_id=31,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1016,
        sender_id=None,
        location_id=2,
        recipient_id=31,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=32,
        name="Test P32",
        email="testpati3ent32@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99932",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1017,
        sender_id=32,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1018,
        sender_id=None,
        location_id=2,
        recipient_id=32,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=33,
        name="Test P33",
        email="testpati3ent33@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99933",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1019,
        sender_id=33,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1020,
        sender_id=None,
        location_id=2,
        recipient_id=33,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=34,
        name="Test P34",
        email="testpati3ent34@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99934",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1021,
        sender_id=34,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1022,
        sender_id=None,
        location_id=2,
        recipient_id=34,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=35,
        name="Test P35",
        email="testpati3ent35@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99935",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1023,
        sender_id=35,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1024,
        sender_id=None,
        location_id=2,
        recipient_id=35,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=36,
        name="Test P36",
        email="testpati3ent36@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99936",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1025,
        sender_id=36,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1026,
        sender_id=None,
        location_id=2,
        recipient_id=36,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=37,
        name="Test P37",
        email="testpati3ent37@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99937",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1027,
        sender_id=37,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1028,
        sender_id=None,
        location_id=2,
        recipient_id=37,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=38,
        name="Test P38",
        email="testpati3ent38@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99938",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1029,
        sender_id=38,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1030,
        sender_id=None,
        location_id=2,
        recipient_id=38,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=39,
        name="Test P39",
        email="testpati3ent39@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99939",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1031,
        sender_id=39,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1032,
        sender_id=None,
        location_id=2,
        recipient_id=39,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=40,
        name="Test P40",
        email="testpati3ent40@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99940",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1033,
        sender_id=40,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1034,
        sender_id=None,
        location_id=2,
        recipient_id=40,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=41,
        name="Test P41",
        email="testpati3ent41@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99941",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1035,
        sender_id=41,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1036,
        sender_id=None,
        location_id=2,
        recipient_id=41,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=42,
        name="Test P42",
        email="testpati3ent42@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99942",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1037,
        sender_id=42,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1038,
        sender_id=None,
        location_id=2,
        recipient_id=42,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=43,
        name="Test P43",
        email="testpati3ent43@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99943",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1039,
        sender_id=43,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1040,
        sender_id=None,
        location_id=2,
        recipient_id=43,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=44,
        name="Test P44",
        email="testpati3ent44@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99944",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1041,
        sender_id=44,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1042,
        sender_id=None,
        location_id=2,
        recipient_id=44,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=45,
        name="Test P45",
        email="testpati3ent45@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99945",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1043,
        sender_id=45,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1044,
        sender_id=None,
        location_id=2,
        recipient_id=45,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=46,
        name="Test P46",
        email="testpati3ent46@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99946",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1045,
        sender_id=46,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1046,
        sender_id=None,
        location_id=2,
        recipient_id=46,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=47,
        name="Test P47",
        email="testpati3ent47@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99947",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1047,
        sender_id=47,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1048,
        sender_id=None,
        location_id=2,
        recipient_id=47,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=48,
        name="Test P48",
        email="testpati3ent48@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99948",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1049,
        sender_id=48,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1050,
        sender_id=None,
        location_id=2,
        recipient_id=48,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=49,
        name="Test P49",
        email="testpati3ent49@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99949",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1051,
        sender_id=49,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1052,
        sender_id=None,
        location_id=2,
        recipient_id=49,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=50,
        name="Test P50",
        email="testpati3ent50@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99950",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1053,
        sender_id=50,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1054,
        sender_id=None,
        location_id=2,
        recipient_id=50,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=51,
        name="Test P51",
        email="testpati3ent51@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99951",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1055,
        sender_id=51,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1056,
        sender_id=None,
        location_id=2,
        recipient_id=51,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=52,
        name="Test P52",
        email="testpati3ent52@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99952",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1057,
        sender_id=52,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1058,
        sender_id=None,
        location_id=2,
        recipient_id=52,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=53,
        name="Test P53",
        email="testpati3ent53@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99953",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1059,
        sender_id=53,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1060,
        sender_id=None,
        location_id=2,
        recipient_id=53,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()

    

    timestamp = datetime.utcnow()

    password = hash_password("password")
    user = user_datastore.create_user(
        id=54,
        name="Test P54",
        email="testpati3ent54@email.com",
        organization_id=2,
        location_id=2,
        password=password,
        phone_number="+99954",
    )

    db.session.add(user)
    db.session.commit()
    user_datastore.add_role_to_user(user, "Patient")
    user_datastore.commit()

    message1 = Message(
        id=1061,
        sender_id=54,
        location_id=2,
        recipient_id=None,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message1)
    db.session.commit()
    timestamp = datetime.utcnow()

    message2 = Message(
        id=1062,
        sender_id=None,
        location_id=2,
        recipient_id=54,
        body="Blalala",
        timestamp=timestamp
    )

    db.session.add(message2)
    db.session.commit()
    """
    



