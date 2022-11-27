from api.models.db import db
from datetime import datetime
from sqlalchemy_utils import EncryptedType
from datetime import datetime
from sqlalchemy import insert
from dateutil import tz

photos_message = db.Table(
    "photos_message",
    db.Column("photo_id", db.Integer(), db.ForeignKey("Photo.id")),
    db.Column("message_id", db.Integer(), db.ForeignKey("Message.id")),
)


class Photo(db.Model):
    __tablename__ = "Photo"

    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String(), nullable=False)
    message_id = db.Column(db.ForeignKey("Message.id"), nullable=True)

    def add_relation(self, photo_id, message_id):
        stmt = insert(photos_message).values(photo_id=photo_id, message_id=message_id)
        db.session.execute(stmt)
        self.message_id = message_id
        db.session.commit()

    def serialize(self):
        return {"id": self.id, "photo": self.photo_url}


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

        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "sender_name": self.sender_name,
            "photos": [x.serialize() for x in self.photos],
            "recipient_id": self.recipient_id,
            "body": self.body,
            "timestamp": self.timestamp,
        }
