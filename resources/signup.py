import traceback

from flask import request, render_template, make_response
from flask_restful import Resource
from marshmallow import INCLUDE, EXCLUDE
from mongoengine.errors import NotUniqueError, ValidationError

from libs.errors import *
from models.usermodel import UserModel
from schemas.user import UserSchema

user_schema = UserSchema(unknown=INCLUDE)


class SignUp(Resource):

    @classmethod
    def post(cls):
        # Get the Json payload
        data = request.get_json()
        print(data)
        user = user_schema.load(data)

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
