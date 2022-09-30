from api.models.db import db
from datetime import datetime
from flask import current_app as app
from sqlalchemy_utils import EncryptedType



class Message(db.Model):
    """Model for messages between physicians and patients."""

    __tablename__ = "Message"
    __key = '123456'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(
        db.Integer, db.ForeignKey("User.id"), nullable=True
    )
    recipient_id = db.Column(
        db.Integer, db.ForeignKey("User.id"), nullable=True
    )
    
    patient_phone_number = db.Column(db.String(16), nullable=False, index=True)
    body = db.Column(EncryptedType(db.String, __key), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Message {}>".format(self.body)

    def serialize(self):
        return {
            "id": self.id,
            "patient_sender_id": self.patient_sender_id,
            "physician_recipient_id": self.physician_recipient_id,
            "body": self.body,
            "timestamp": self.timestamp,
        }


class PNumbertoUser(db.Model):
    __tablename__ = "PNumbertoUser"
    phone_number = db.Column(
        db.String(16), nullable=False, index=True, primary_key=True
    )
    user_id = db.Column(db.ForeignKey("User.id"))
    physician_id = db.Column(db.ForeignKey("User.id"))
