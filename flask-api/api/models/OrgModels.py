from .db import db
from api.models.Messages import Message
from .db import db
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from api.models.Messages import Message
from .Notifications import Notification
import json
from sqlalchemy import insert
from flask import session
from sqlalchemy.orm import relationship, backref


class Organization(db.Model):
    """Model class for Organization. (Organization)"""

    __tablename__ = "Organization"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    twilio_account_id = db.Column(db.String(64), nullable=False)
    twilio_auth_token = db.Column(db.String(64), nullable=False)
    locations = db.relationship(
        "Location", backref=db.backref('Locations'), lazy='dynamic'
        )
    

    def serialize(self):

        return {
            "id": self.id,
            "name": self.name,
            # "Locations": [x.serialize() for x in self.locations],
            "twilio_account_id": self.twilio_account_id,
            "twilio_auth_token": self.twilio_auth_token
            #'Locations': jsonify([x.serialize() for x in self.Locations])
        }   


locations_users = db.Table(
    "locations_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("User.id", ondelete='CASCADE')),
    db.Column("location_id", db.Integer(), db.ForeignKey("Location.id", ondelete='CASCADE'))
)


class Location(db.Model):
    """Model for Locations."""

    __tablename__ = "Location"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    phone_number = db.Column(db.String(16), index=True)
    address = db.Column(db.String(128), index=True)
    city = db.Column(db.String(32), index=True)
    state = db.Column(db.String(16), index=True)
    zip_code = db.Column(db.String(16), index=True)
    organization_id = db.Column(
        db.Integer, db.ForeignKey("Organization.id"), nullable=False
    )
    
    users = relationship(
        "User",
        secondary=locations_users,
        back_populates="locations",
        cascade="all, delete",
    )


    def serialize(self):
        organization_name = Organization.query.get(self.organization_id).name
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "organization_id": self.organization_id,
            "organization_name": organization_name,
            "zip_code": self.zip_code,
            "messages_no_response": self.get_messages_with_no_response()

        }

    def serialize_name(self):
        return {"name": self.name, "id": self.id}

    def get_messages_with_no_response(self):
        # this could be slow but can be improved later

        unresponded = 0
        users = (
            User.query.filter(User.location_id == self.id)
            .filter(User.roles.any(name="Patient"))
            .all()
        )
        try:
            if users is not None:
                for i in users:
                    message_history = (
                        Message.query.order_by(Message.timestamp.desc())
                        .filter(
                            (Message.recipient_id == i.id) | (Message.sender_id == i.id)
                        )
                        .first()
                    )
                    if message_history.sender_id == i.id:
                        unresponded += 1

            return unresponded
        except:
            return 0


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("User.id", ondelete='CASCADE')),
    db.Column("role_id", db.Integer(), db.ForeignKey("Role.id", ondelete='CASCADE')),
)

roles_permissions = db.Table(
    "roles_permissions",
    db.Column("permission_id", db.Integer(), db.ForeignKey("Permission.id", ondelete='CASCADE')),
    db.Column("role_id", db.Integer(), db.ForeignKey("Role.id", ondelete='CASCADE')),
)


class Permission(db.Model):
    __tablename__ = "Permission"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String(255))

    def serialize(self):
        return {"id": self.id, "name": self.name, "description": self.description}

    def serialize_name(self):
        return {"name": self.name}


class Role(db.Model, RoleMixin):
    __tablename__ = "Role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.relationship(
        "Permission", secondary=roles_permissions,  passive_deletes=True, backref=db.backref("roles")
    )

    def serialize(self):
        return {"id": self.id, "name": self.name, "description": self.description}

    def serialize_name(self):
        return {"name": self.name}

    def serialize_p(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "permissions": [x.serialize() for x in self.permissions],
        }

    def add_permission(self, role_id, permission_id):
        stmt = insert(roles_permissions).values(
            role_id=role_id, permission_id=permission_id
        )
        db.session.execute(stmt)
        db.session.commit()

    def remove_permission(self, role_id, permission_id):
        stmt = (
            roles_permissions.delete()
            .where(roles_permissions.c.permission_id == permission_id)
            .where(roles_permissions.c.role_id == role_id)
        )
        db.session.execute(stmt)
        db.session.commit()


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=True)
    email = db.Column(db.String(40), unique=True, nullable=True)
    password = db.Column(db.String(255), unique=False, nullable=True)
    active = db.Column(db.String(255))
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login_at = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    current_login_at = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    last_login_ip = db.Column(db.String())
    current_login_ip = db.Column(db.String())
    login_count = db.Column(db.Integer)
    roles = db.relationship(
        "Role", secondary=roles_users, passive_deletes=True, backref=db.backref("users", lazy="dynamic")
    )

    profile_pic = db.Column(db.String(), index=False, unique=False, nullable=True)

    # primary location
    location_id = db.Column(db.ForeignKey("Location.id", ondelete='CASCADE'), nullable=True)

    locations = db.relationship(
        "Location",
        secondary=locations_users,
        back_populates="users",
        passive_deletes=True,
    )

    organization_id = db.Column(db.ForeignKey("Organization.id", ondelete='CASCADE'), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)

    messages_sent = db.relationship(
        "Message",
        foreign_keys="Message.sender_id",
        backref="sent_User",
        lazy="dynamic",
    )

    messages_received = db.relationship(
        "Message",
        foreign_keys="Message.recipient_id",
        backref="received_User",
        lazy="dynamic",
    )

    last_message_read_time = db.Column(db.DateTime)

    notifications = db.relationship("Notification", backref="User", lazy="dynamic")

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def set_creation_date(self):
        self.created_on = datetime.today()

    def set_last_login(self):
        self.last_login = datetime.today()
        db.session.commit()

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {}>".format(self.name)

    def unread_messages(self):
        try:
            message_history = (
                Message.query.order_by(Message.timestamp.desc())
                .filter(
                    (Message.recipient_id == self.id) | (Message.sender_id == self.id)
                )
                .first()
            )
            if message_history.sender_id == self.id:
                return 1
        except:
            return 0

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return (
            Message.query.filter_by(recipient_id=self.id)
            .filter(Message.timestamp > last_read_time)
            .count()
        )

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), User=self)
        db.session.add(n)
        return n

    def add_location(self, user_id, location_id):

        stmt = insert(locations_users).values(user_id=user_id, location_id=location_id)
        db.session.execute(stmt)
        db.session.commit()

    def remove_location(self, user_id, location_id):
        stmt = (
            locations_users.delete()
            .where(locations_users.c.user_id == user_id)
            .where(locations_users.c.location_id == location_id)
        )
        db.session.execute(stmt)
        db.session.commit()

    def remove_all_roles(self):
        stmt = (
            roles_users.delete()
            .where(roles_users.c.user_id == self.id)
        )
        db.session.execute(stmt)
        db.session.commit()

    def has_permission(self, permission):

        ###DATABASE WAY
        # all roles that have the permission to do this action
        # roles_allowed = Role.query.join(Role.permissions, aliased=True)\
        #            .filter_by(id=permission.value).all()

        # for x in self.roles:
        #    if x in roles_allowed:
        #        return True

        # session way
        if permission.value in session["permissions"]:
            return True

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "organization_id": self.organization_id,
            "roles": [x.serialize_name() for x in self.roles],
            "location_id": self.location_id,
            "email": self.email,
            "phone_number": self.phone_number,
            "locations": [x.serialize_name() for x in self.locations],
        }

    def serialize_user_display(self):
        # used for displaying user on users page
        return {
            "id": self.id,
            "name": self.name,
            "roles": [x.serialize_name() for x in self.roles],
            "email": self.email,
            "phone_number": self.phone_number,
            "locations": [x.serialize_name() for x in self.locations],
            "organization_id": self.organization_id,
        }

    def serialize_msg_sidebar(self):
        # used for displaying user in message sidebar
        return {"id": self.id, "name": self.name, "unread_msg": self.unread_messages()}

    def serialize_pending(self):
        # used for displaying user in pending users page
        try:
            location = Location.query.get(self.location_id)
            name = location.name
        except:
            name = "Error"

        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone_number": self.phone_number,
            "location_name": name,
        }
