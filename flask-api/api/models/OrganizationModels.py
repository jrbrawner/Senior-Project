from email import message
from .db import db
from flask import jsonify
from api.models.Messages import Message
from api.models.Users import User

class Organization(db.Model):
    """Model class for Organization. (Organization)"""

    __tablename__ = "Organization"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    twilio_account_id = db.Column(db.String(64), nullable=False)
    twilio_auth_token = db.Column(db.String(64), nullable=False)
    locations = db.relationship("Location", backref="Locations", lazy=True)

    def serialize(self):

        return {
            "id": self.id,
            "name": self.name,
            # "Locations": [x.serialize() for x in self.locations],
            "twilio_account_id": self.twilio_account_id,
            "twilio_auth_token": self.twilio_auth_token
            #'Locations': jsonify([x.serialize() for x in self.Locations])
        }


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
    # physicians = db.relationship("Physician", backref="physicians", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "organization_id": self.organization_id,
            "zip_code": self.zip_code,
            "messages_no_response": self.get_messages_with_no_response()
            #'physicians': jsonify([x.serialize() for x in self.physicians])
        }

    def get_messages_with_no_response(self):
        #this could be slow but can be improved later
        
        unresponded = 0
        users = User.query.filter(User.location_id==self.id).filter(User.roles.any(name='Patient')).all()
        
        if users is not None:
            for i in users:
                message_history = Message.query.order_by(Message.timestamp.desc()).filter((Message.recipient_id==i.id) | (Message.sender_id==i.id)).first()
                if message_history.sender_id == i.id:
                    unresponded += 1

        return unresponded
