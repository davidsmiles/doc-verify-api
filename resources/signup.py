import traceback

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import request, render_template, make_response
from flask_restful import Resource
from marshmallow import INCLUDE, EXCLUDE
from mongoengine.errors import NotUniqueError, ValidationError

from libs.errors import *
from models.adminmodel import AdminModel
from models.usermodel import UserModel
from schemas.user import UserSchema

user_schema = UserSchema(unknown=EXCLUDE)


class Signup(Resource):

    @classmethod
    def post(cls):
        # Get the Json payload
        data = request.get_json()
        user = UserModel(**user_schema.load(data))

        if UserModel.find_by_email(user.email):
            return {'message': gettext("user_username_exists")}, 400

        # Load it into Users data
        try:
            user.password = UserModel.hash_password(data['password'])
            user.save_to_db()

            return {
                   'message': gettext("user_registered"),
                   'user_id': user.user_id
               }, 200
        except NotUniqueError:
            raise UserEmailExists
        except ValidationError:
            raise EmailInvalid
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {'message': gettext("user_error_creating")}


class AdminSignup(Resource):

    @classmethod
    def post(cls):
        # Get the Json payload
        data = request.get_json()
        print(data)
        user = AdminModel(**user_schema.load(data))

        if AdminModel.find_by_email(user.email):
            return {'message': gettext("user_username_exists")}, 400

        # Load it into Users data
        try:
            user.password = AdminModel.hash_password(data['password'])
            user.save_to_db()

            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )

            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            with open('privatekey.cer', 'wb') as f:
                f.write(pem)

            public_key = private_key.public_key()
            pub = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            with open('publickey.cer', 'wb') as f:
                f.write(pub)

            return {
                   'message': gettext("user_registered"),
                   'user_id': user.user_id
               }, 200
        except NotUniqueError:
            raise UserEmailExists
        except ValidationError:
            raise EmailInvalid
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {'message': gettext("user_error_creating")}
