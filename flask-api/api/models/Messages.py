from api.models.db import db
from datetime import datetime
from flask import current_app as app
from sqlalchemy_utils import EncryptedType
from datetime import datetime, timedelta


class Message(db.Model):
    """Model for messages between physicians and patients."""

    __tablename__ = "Message"
    __key = "123456"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=True)
    sender_name = db.Column(db.String())
    location_id = db.Column(db.Integer, db.ForeignKey("Location.id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=True)

    body = db.Column(EncryptedType(db.String, __key), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Message {}>".format(self.body)

    def serialize(self):
        str_date_time = self.timestamp.strftime("%Y %B %d, %H:%M")
        offset = "0700"

        res = datetime.strptime(str_date_time, '%Y %B %d, %H:%M') + \
        timedelta(hours=int(offset[:2]), minutes=int(offset[2:]))

        res = res.strftime("%B %d, %H:%M")
        

        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "sender_name": self.sender_name,
            "recipient_id": self.recipient_id,
            "body": self.body,
            "timestamp": str_date_time,
        }
