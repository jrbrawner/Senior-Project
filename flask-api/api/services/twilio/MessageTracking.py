from ...models.Messages import Message
from ...models.Users import User
from ...models.db import db
import logging
from api import user_datastore
from flask_security import current_user


class MessageTracking:
    @staticmethod
    def create_new_message_patient(phone_number, body, location_id):
        """
        Standard function for creating messages between a patient and physician.
        """

        user = user_datastore.find_user(phone_number=phone_number)

        if user:
            message = Message(
                sender_id=user.id,
                recipient_id=None,
                body=body,
                location_id=location_id
            )

            db.session.add(message)
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
                sender_id=sender_id,
                recipient_id=patient.id,
                body=body,
                location_id=location_id
            )

            db.session.add(message)
            db.session.commit()

            logging.warning(
                f"New message created from {sender_id} to their patient {patient.id}"
            )
            return True
        else:
            return False
