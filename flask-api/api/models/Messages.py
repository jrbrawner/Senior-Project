from .. import db
from datetime import datetime
from flask import current_app as app
from .Physicians import Physician

class Message(db.Model):
    """Model for messages between physicians and patients."""
    __tablename__ = 'Message'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('Patient.id'), nullable=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('Physician.id'), nullable=True)
    body = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)

    def serialize(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'recipient_id': self.recipient_id,
            'body': self.body,
            'timestamp': self.timestamp
        }

class PNumbertoUser(db.Model):
    __tablename__ = 'PNumbertoUser'
    phone_number = db.Column(db.String(16), nullable=False, index=True, primary_key=True)
    user_id = db.Column(db.ForeignKey('Patient.id'))
    physician_id = db.Column(db.ForeignKey('Physician.id'))