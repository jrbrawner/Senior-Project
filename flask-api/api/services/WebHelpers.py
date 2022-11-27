from flask import jsonify, request
from werkzeug.utils import secure_filename
from flask_login import current_user
import mimetypes
import os
from flask import current_app as app
import requests
from urllib.parse import urlparse
from api.models.Messages import Photo
from api.models.db import db


class WebHelpers:
    @staticmethod
    def allowed_file_extension(filename):
        """Checks for designated extensions in a filename."""
        ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    @staticmethod
    def EasyResponse(msg, status_code):
        """Allows for easy creation of flask response."""

        data = {"msg": msg}

        resp = jsonify(data)
        resp.status_code = status_code

        return resp

    @staticmethod
    def HandleUserPictureUpload(folder_name):
        """
        Handles uploading and saving of a picture to designated folder as specified in app config.
        Expects picture to come in form with specified id 'picture'.
        Path is saved in user attribute 'profile_pic'
        """

        if request.method == "POST":
            # check if request has the file part
            if "picture" not in request.files:
                return WebHelpers.EasyResponse("No picture provided.", 400)

            picture = request.files["picture"]

            # make sure filename is not empty
            if picture.filename == "":
                return WebHelpers.EasyResponse("No picture provided.", 400)

            # make sure picture exists, and file extension is in allowed extensions
            if picture and WebHelpers.allowed_file_extension(picture.filename):

                filename = secure_filename(picture.filename)
                filename = str(current_user.id) + "_" + filename

                picture.save(os.path.join(app.config[folder_name], filename))
                current_user.profile_pic = filename
                db.session.commit()

                return WebHelpers.EasyResponse("Profile picture uploaded.", 200)
        else:
            return WebHelpers.EasyResponse("Error.", 400)

    @staticmethod
    def HandleUserPictureTwilioMMS(media_files, user_id):
        """
        Handles retrieving of a users photo sent in an MMS.
        Expects picture to come in form with specified id 'picture'.
        Path is saved in user attribute 'profile_pic'
        """
        photos = []

        if media_files is not None:
            for (media_url, mime_type) in media_files:
                print(media_url)
                file_extension = mimetypes.guess_extension(mime_type)
                media_sid = os.path.basename(urlparse(media_url).path)
                photo = requests.get(media_url).content
                filename = secure_filename(f"{user_id}_{media_sid}{file_extension}")

                if photo and WebHelpers.allowed_file_extension(filename):
                    file_path = os.path.join(app.config["PHOTOS"], filename)
                    with open(file_path, "wb") as file:
                        file.write(photo)
                    file.close()
                    photo = Photo(photo_url=filename)
                    db.session.add(photo)
                    db.session.commit()
                    photos.append(photo)

            return photos
