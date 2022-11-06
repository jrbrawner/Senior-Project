from ...models.Messages import Message
from ...models.OrgModels import User
from ...models.db import db
import logging
from api import user_datastore
from flask_security import current_user
from ..WebHelpers import WebHelpers

class MessageTracking:
    @staticmethod
    def create_new_message_patient(phone_number, body, location_id, media_files):
        """
        Standard function for creating messages between a patient and physician.
        """

        user = user_datastore.find_user(phone_number=phone_number)
        photos = None
        #photos handling
        if len(media_files) > 0:
            photos = WebHelpers.HandleUserPictureTwilioMMS(media_files=media_files, user_id=user.id)

        if user:
            message = Message(
                sender_id=user.id,
                sender_name=user.name,
                recipient_id=None,
                body=body,
                location_id=location_id
            )

            db.session.add(message)
            db.session.commit()
        
        if photos:
            for i in photos:
                i.add_relation(i.id, message.id)
            db.session.commit()

            logging.warning(f"New message created from {user.name} to their office.")
            return True
        else:
            return False

    @staticmethod
    def create_new_message_before_signup(user_id, body, location_id):

        message = Message(body=body, sender_id=user_id, location_id=location_id)

        db.session.add(message)
        db.session.commit()

        logging.warning(f"Message from brand new user to their office.")

        return True

    @staticmethod
    def create_new_message_physician_to_patient(sender_id, patient_number, body, location_id):

        patient = User.query.filter_by(phone_number=patient_number).first()

        if patient:
            message = Message(
                sender_id=None,
                recipient_id=patient.id,
                sender_name=patient.name,
                body=body,
                location_id=location_id
            )

            db.session.add(message)
            db.session.commit()

            logging.warning(
                f"New message created from {sender_id} to patient {patient.id}"
            )
            return True
        else:
            return False
