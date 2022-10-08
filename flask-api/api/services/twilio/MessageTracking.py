from ...models.Messages import Message
from ...models.Users import User
from ...models.db import db
import logging
from api import user_datastore


class MessageTracking:
    @staticmethod
    def create_new_message_patient(phone_number, body):
        """
        Standard function for creating messages between a patient and physician.
        """

        user = user_datastore.find_user(phone_number=phone_number)

        if user:
            message = Message(
                sender_id=user.id,
                recipient_id=user.location_id,
                body=body,
            )

            db.session.add(message)
            db.session.commit()

            logging.warning(f"New message created from {user.name} to their office.")
            return True
        else:
            return False

    @staticmethod
    def create_new_message_before_signup(user_id, body):

        message = Message(body=body, sender_id=user_id)

        db.session.add(message)
        db.session.commit()

        logging.warning(f"Message from brand new user to their office.")

        return True

    @staticmethod
    def create_new_message_physician_to_patient(physician_id, patient_number, body):

        user = User.query.filter_by(phone_number=patient_number).first()

        if user:
            message = Message(
                physician_sender_id=physician_id,
                patient_recipient_id=user.id,
                body=body,
                patient_phone_number=patient_number,
            )

            db.session.add(message)
            db.session.commit()

            logging.warning(
                f"New message created from {physician_id} to their patient {user.name}"
            )
            return True
        else:
            return False
