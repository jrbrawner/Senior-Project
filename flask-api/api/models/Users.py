from .db import db
from flask_security import UserMixin, Security, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import create_engine
from flask import current_app as app
from api.models.Messages import Message
from .Notifications import Notification
import json
from sqlalchemy import insert
from api.permissions import Permissions
from flask import session
from api.models.OrganizationModels import Location

roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("User.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("Role.id")),
)

roles_permissions = db.Table(
    "roles_permissions",
    db.Column("permission_id", db.Integer(), db.ForeignKey("Permission.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("Role.id"))
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
    permissions = db.relationship("Permission", secondary=roles_permissions, backref=db.backref("roles"))

    def serialize(self):
        return {"id": self.id, "name": self.name, "description": self.description}

    def serialize_name(self):
        return {"name": self.name}
    
    def add_permission(self, role_id, permission_id):
        stmt = (
            insert(roles_permissions).
            values(role_id=role_id, permission_id=permission_id)
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
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    profile_pic = db.Column(db.String(), index=False, unique=False, nullable=True)
    location_id = db.Column(db.ForeignKey("Location.id"), nullable=False)
    organization_id = db.Column(db.ForeignKey("Organization.id"), nullable=False)
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

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return (
            Message.query.filter_by(recipient=self)
            .filter(Message.timestamp > last_read_time)
            .count()
        )

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), User=self)
        db.session.add(n)
        return n

    def has_permission(self, permission):

        ###DATABASE WAY
        #all roles that have the permission to do this action
        #roles_allowed = Role.query.join(Role.permissions, aliased=True)\
        #            .filter_by(id=permission.value).all()
       
        #for x in self.roles:
        #    if x in roles_allowed:
        #        return True

        #session way
        if permission.value in session['permissions']:
            return True
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "roles": [x.serialize_name() for x in self.roles],
            "location_id": self.location_id,
            "email": self.email,
            "phone_number": self.phone_number,
        }

    def serialize_user_display(self):

        location = Location.query.get(self.location_id)
        

        return {
            "id": self.id,
            "name": self.name,
            "roles": [x.serialize_name() for x in self.roles],
            "location_id": location.name,
            "email": self.email,
            "phone_number": self.phone_number,
        }