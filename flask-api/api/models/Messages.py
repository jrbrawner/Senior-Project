from api.models.db import db
from datetime import datetime
from flask import current_app as app
from sqlalchemy_utils import EncryptedType
from datetime import datetime, timedelta
from sqlalchemy import insert
from flask import send_from_directory

photos_message = db.Table(
    "photos_message",
    db.Column("photo_id", db.Integer(), db.ForeignKey("Photo.id")),
    db.Column("message_id", db.Integer(), db.ForeignKey("Message.id")),
)

class Photo(db.Model):
    __tablename__ = "Photo"

    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String(), nullable=False)
    message_id = db.Column(db.ForeignKey('Message.id'), nullable=True)

    def add_relation(self, photo_id, message_id):
        stmt = (
            insert(photos_message).
            values(photo_id=photo_id, message_id=message_id)
        )
        db.session.execute(stmt)
        self.message_id = message_id
        db.session.commit()

    


class Message(db.Model):
    """Model for messages between physicians and patients."""

    __tablename__ = "Message"
    __key = "123456"

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=True)
    sender_name = db.Column(db.String())
    location_id = db.Column(db.Integer, db.ForeignKey("Location.id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=True)
    photos = db.relationship(
        "Photo", secondary=photos_message, backref=db.backref("photos", lazy="dynamic")
    )
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
            "photos": [x.photo_url for x in self.photos],
            "recipient_id": self.recipient_id,
            "body": self.body,
            "timestamp": str_date_time,
        }
