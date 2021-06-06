from flask import request, render_template, make_response
from flask_restful import Resource
from mongoengine.errors import NotUniqueError, ValidationError

from libs.errors import *
from models.user import Users


class SignUp(Resource):
    @classmethod
    def post(cls):
        # Get the Json payload
        data = dict(request.form)

        # Load it into Users data
        try:
            del data['remember']
            data['password'] = Users.hash_password(data['password'])
            user = Users(**data)
            user.save()
            _id = user.id

            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('admin.html'), 200, headers)
        except NotUniqueError:
            raise UserEmailExists
        except ValidationError:
            raise EmailInvalid

    @classmethod
    def get(cls):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('signup.html'), 200, headers)
