from ...models.Messages import Message, PNumbertoUser, db
from ...models.Patients import Patient
import logging

class MessageTracking:

    @staticmethod
    def create_new_message_patient(phone_number, body):
        """
        Standard function for creating messages between a patient and physician.
        """

        user = Patient.query.filter_by(phone_number=phone_number).first()

        if user:
            message = Message(
                patient_sender_id = user.id,
                physician_recipient_id = user.physician_id,
                body=body
            )

            db.session.add(message)
            db.session.commit()

            logging.warning(f'New message created from {user.name} to their physician.')
            return True
        else:
            return False


