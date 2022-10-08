import os
from twilio.rest import Client
import logging


class TwilioClient:
    def __init__(self, account_sid, auth_token):
        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(account_sid, auth_token)

    def send_message(self, location_number, user_number, text):
        """
        Send message using twilio client.
        """
        message = self.client.messages.create(
            body=text, from_=location_number, to=user_number
        )


twilio_logger = logging.getLogger("twilio.http_client")
twilio_logger.setLevel(logging.CRITICAL)
