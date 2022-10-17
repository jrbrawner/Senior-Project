import os
from twilio.rest import Client
import logging
from api.models.Messages import Message
from api import db, user_datastore


class TwilioClient:
    def __init__(self, account_sid, auth_token):
        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(account_sid, auth_token)

    def send_automated_message(self, location_number, user_number, text, location_id):
        """
        Send message using twilio client.
        """
        message = self.client.messages.create(
            body=text, from_=location_number, to=user_number
        )
        
        user_acc = user_datastore.find_user(phone_number=user_number)
        if user_acc is None:
            track_message = Message(
                sender_id=None,
                location_id=location_id,
                recipient_id=None,
                body=text
            )
            db.session.add(track_message)
            db.session.commit()
        else:
            track_message = Message(
                sender_id=None,
                location_id=location_id,
                recipient_id=user_acc.id,
                body=text
            )
            db.session.add(track_message)
            db.session.commit()


twilio_logger = logging.getLogger("twilio.http_client")
twilio_logger.setLevel(logging.CRITICAL)
