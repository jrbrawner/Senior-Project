from flask import jsonify, request
from werkzeug.utils import secure_filename
from flask_login import current_user
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
    def CheckUserState(phone_number):
        """
        Takes phone number and determines where a patient is at in the sign up process.
        """
        result = None

        user = user_datastore.find_user(phone_number=phone_number)
        # user exists,
        if user:
            # see if they have role assigned
            role_status = user.roles
            # have been accepted as a patient
            if "Patient" in role_status:
                result = "Accepted"
                return result
            # have completed sign up, but not accepted yet
            elif "Pending Patient" in role_status:
                result = "Pending"
                return result
            elif "Pending Patient" and "Patient" not in role_status:
                result = "Signup"
                return result
        # brand new, no account started
        result = "New"
        logging.warning(f"New phone number {phone_number} recognized.")
        return result

    @staticmethod
    def InitiateUserSignUp(phone_number, location, organization, msg):
        """
        Creates new user to be a pending patient.
        """
        new_patient = user_datastore.create_user(
            phone_number=phone_number,
            location_id=location.id,
            organization_id=organization.id,
        )
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

        phone_number_user = user_datastore.find_user(phone_number=phone_number)

        if (
            phone_number_user
            and "Pending Patient" not in phone_number_user.roles
            and "Patient" not in phone_number_user.roles
        ):
            """
            Basic example form to have user send in, seperate fields with '.' in message:
            Name.Email.
            """
            msg_array = msg.split(".")

            name = msg_array[0]
            email = msg_array[1]

            phone_number_user.name = name
            phone_number_user.email = email

            user_datastore.add_role_to_user(phone_number_user, "Pending Patient")
            db.session.commit()

            MessageTracking.create_new_message_before_signup(
                user_id=phone_number_user.id, body=msg
            )

            logging.warning(
                f"New user registered. Name - {phone_number_user.name} Phone Number - {phone_number_user.phone_number}. "
            )
            return f"Thanks {phone_number_user.name}! You will be notified when your physician accepts your registration."
