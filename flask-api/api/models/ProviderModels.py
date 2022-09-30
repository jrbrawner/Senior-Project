from .db import db
from flask import jsonify


class Provider(db.Model):
    """Model class for provider. (Organization)"""

    __tablename__ = "Provider"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    twilio_account_id = db.Column(db.String(64), nullable=False)
    twilio_auth_token = db.Column(db.String(64), nullable=False)
    offices = db.relationship("Office", backref="offices", lazy=True)

    def serialize(self):

        data = {
            "id": self.id,
            "name": self.name,
            "offices": str([x.serialize() for x in self.offices]),
            "twilio_account_id": self.twilio_account_id,
            "twilio_auth_token": self.twilio_auth_token
            #'offices': jsonify([x.serialize() for x in self.offices])
        }

        return data


class Office(db.Model):
    """Model for offices."""

    __tablename__ = "Office"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    phone_number = db.Column(db.String(16), index=True)
    address = db.Column(db.String(128), index=True)
    city = db.Column(db.String(32), index=True)
    state = db.Column(db.String(16), index=True)
    zip_code = db.Column(db.String(16), index=True)
    provider_id = db.Column(db.Integer, db.ForeignKey("Provider.id"), nullable=True)
    physicians = db.relationship("Physician", backref="physicians", lazy=True)

    def serialize(self):

        data = {
            "id": self.id,
            "name": self.name,
            "phone_number": self.phone_number,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "provider_id": self.provider_id,
            "zip_code": self.zip_code
            #'physicians': jsonify([x.serialize() for x in self.physicians])
        }

        return data
