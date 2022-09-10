import os
from twilio.rest import Client

class TwilioClient():

    def __init__(self, account_sid, auth_token):
        # Find your Account SID and Auth Token at twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = Client(account_sid, auth_token)

    def send_message(self, user_number, text):
        """
        Send message using twilio client.
        """
        message = self.client.messages \
                        .create(
                            body=text,
                            from_='+18155510787',
                            to=user_number
                 )

        print(message.sid)