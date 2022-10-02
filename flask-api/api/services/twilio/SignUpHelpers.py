from flask import jsonify, request
from werkzeug.utils import secure_filename
from flask_login import current_user
import os
from flask import current_app as app
from api.models.Users import User
from api.models.Messages import Message
from api.models.db import db
from ...models.Users import User
from ...models.db import db
import logging
from .MessageTracking import MessageTracking
from api import user_datastore


class TwilioSignUpHelpers:
    @staticmethod
    def CheckIfNewUser(phone_number):
        """
        Checks phone number to see if it is associated with a patient in the database.
        """
        phone_number_user = User.query.filter_by(phone_number=phone_number)

        if phone_number_user is None:
            logging.warning(f"New phone number {phone_number} recognized.")
            return True
        else:
            logging.warning(f"Phone number {phone_number} recognized.")
            return False

    @staticmethod
    def CheckIfRegistered(phone_number):
        """
        Checks phone number to see if sign-up process has been initiated.
        """
        phone_number_user = User.query.filter_by(phone_number=phone_number).first()

        if phone_number_user == None:
            return False

        if phone_number_user and phone_number_user.accepted_patient == False:
            return True
        return False


    @staticmethod
    def CheckIfAccepted(phone_number):
        """
        Checks phone number to see if new user has been accepted.
        """

        phone_number_user = User.query.filter_by(phone_number=phone_number).first()

        if phone_number_user == None:
            return False
            
        if phone_number_user and phone_number_user.accepted_patient == True:
            logging.warning(f"Registered patient sent a message.")
            return True
        else:
            logging.warning(
                f"Registered patient sent a message before being accepted by a physician."
            )
            return False

    @staticmethod
    def InitiateUserSignUp(phone_number, location, organization, msg):
        """
        Creates new user to be a pending patient.
        """
        """
        new_patient = User(
            phone_number = phone_number,
            location = location,
            organization = organization
        )
        """

        new_patient = user_datastore.create_user(
            phone_number = phone_number,
            location = location,
            organization = organization)

        user_datastore.commit()

        MessageTracking.create_new_message_before_signup(
            user_id=new_patient.id, body=msg
        )

        logging.warning(
            f"Phone number {phone_number} entry made. Ready for user sign-up."
        )

        return f"Thanks for choosing to be with us! Please fill out this form to complete your registration. Name.Email."

    @staticmethod
    def CompleteUserSignUp(phone_number, msg):

        phone_number_user = User.query.filter_by(phone_number=phone_number).first()

        if phone_number_user is not None and phone_number_user.user_id is None and phone_number_user.accepted_patient == False:
            """
            Basic example form to have user send in, seperate fields with '.' in message:
            Name.Email.
            """
            msg_array = msg.split(".")

            name = msg_array[0]
            email = msg_array[1]

            phone_number_user.name = name
            phone_number_user.email = email
            db.session.commit()
            MessageTracking.create_new_message_before_signup(
                user_id=phone_number_user.id, body=msg
            )

            logging.warning(
                f"New user registered. Name - {phone_number_user.name} Phone Number - {phone_number_user.phone_number}. "
            )
            return f"Thanks {phone_number_user.name}! You will be notified when your physician accepts your registration."
