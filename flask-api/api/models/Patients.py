from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import create_engine
from flask import current_app as app
from .Messages import Message
from .Notifications import Notification
import json

class Patient(UserMixin, db.Model):
    """Patient account model."""

    __tablename__ = 'Patient'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False,nullable=True)
    last_login = db.Column(db.DateTime, index=False, unique=False,nullable=True)
    profile_pic = db.Column(db.String(), index=False, unique=False, nullable=True)
    
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')

    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')

    last_message_read_time = db.Column(db.DateTime)

    notifications = db.relationship('Notification', backref='Patient',
                                    lazy='dynamic')
    
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def set_creation_date(self):
        self.created_on = datetime.today()

    def set_last_login(self):
        self.last_login = datetime.today()
        db.session.commit()

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<Patient {}>'.format(self.name)

            
    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), Patient=self)
        db.session.add(n)
        return n

    def serialize(self):
        return {
            'Patient_id': self.id,
            'Patient_name': self.name,
        }