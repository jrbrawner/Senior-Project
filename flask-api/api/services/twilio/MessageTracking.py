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
                body=body,
                patient_phone_number=phone_number
            )

            db.session.add(message)
            db.session.commit()

            logging.warning(f'New message created from {user.name} to their physician.')
            return True
        else:
            return False

    @staticmethod
    def create_new_message_before_signup(phone_number, body):
        
            message = Message(
                body=body,
                patient_phone_number=phone_number
            )

            db.session.add(message)
            db.session.commit()

            logging.warning(f'Message from brand new user to their office.')
            return True

    @staticmethod
    def create_new_message_physician_to_patient(physician_id, patient_number, body):

        user = Patient.query.filter_by(phone_number=patient_number).first()

        if user:
            message = Message(
                physician_sender_id = physician_id,
                patient_recipient_id = user.id,
                body=body,
                patient_phone_number=patient_number
            )

            db.session.add(message)
            db.session.commit()

            logging.warning(f'New message created from {physician_id} to their patient {user.name}')
            return True
        else:
            return False