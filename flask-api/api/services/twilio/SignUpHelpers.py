from flask import jsonify, request
from werkzeug.utils import secure_filename
from flask_login import current_user
import os
from flask import current_app as app
from ...models.Messages import PNumbertoUser, db
from ...models.Users import User
from ...models.db import db
import logging
from .MessageTracking import MessageTracking


class TwilioSignUpHelpers:
    @staticmethod
    def CheckForNewUser(phone_number):
        """
        Checks phone number to see if it is associated with a patient in the database.
        """
        phone_number_user = PNumbertoUser.query.get(phone_number)

        if phone_number_user is None:
            logging.warning(f"New phone number {phone_number} recognized.")
            return True
        else:
            logging.warning(f"Phone number {phone_number} recognized.")
            return False

    @staticmethod
    def CheckIfRegistered(phone_number):
        """
        Checks phone number to see if it is associated with a user id in the database.
        """
        phone_number_user = PNumbertoUser.query.get(phone_number)

        if phone_number_user.phone_number and phone_number_user.user_id is not None:
            return True
        else:
            return False

    @staticmethod
    def CheckIfAccepted(phone_number):
        """
        Checks phone number to see if it is associated with a physician in the database.
        """
        phone_number_user = PNumbertoUser.query.get(phone_number)

        if phone_number_user and phone_number_user.physician_id is not None:
            logging.warning(f"Registered patient sent a message.")
            return True
        else:
            logging.warning(
                f"Registered patient sent a message before being accepted by a physician."
            )
            return False

    @staticmethod
    def InitiateUserSignUp(phone_number, msg):
        """
        Creates an entry in the database that is associated with a users phone number.
        """
        pnumbertouser = PNumbertoUser(phone_number=phone_number)

        MessageTracking.create_new_message_before_signup(
            phone_number=phone_number, body=msg
        )
        db.session.add(pnumbertouser)
        db.session.commit()
        logging.warning(
            f"Phone number {phone_number} entry made. Ready for user sign-up."
        )

        return f"Thanks for choosing to be with us! Please fill out this form to complete your registration. Name.Email."

    @staticmethod
    def CreateNewUser(phone_number, msg):

        phone_number_user = PNumbertoUser.query.get(phone_number)
        if phone_number_user is not None and phone_number_user.user_id is None:

            """
            Basic example form to have user send in, seperate fields with '.' in message:
            Name.Email.
            """
            msg_array = msg.split(".")

            name = msg_array[0]
            email = msg_array[1]

            new_patient = Patient(
                name=name, email=email, phone_number=phone_number_user.phone_number
            )

            db.session.add(new_patient)
            new_patient.set_creation_date()
            db.session.commit()
            phone_number_user.user_id = new_patient.id
            db.session.commit()
            MessageTracking.create_new_message_before_signup(
                phone_number=phone_number, body=msg
            )

            logging.warning(
                f"New user registered. Name - {new_patient.name} Phone Number - {phone_number_user.phone_number}. "
            )
            return f"Thanks {new_patient.name}! You will be notified when your physician accepts your registration."
