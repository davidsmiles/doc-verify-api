import datetime

from flask import request, make_response, render_template
from flask_restful import Resource
from mongoengine.errors import DoesNotExist, ValidationError

from libs.errors import UserNotExist, UnauthorizedError, UserNotConfirmed, EmailInvalid
from models.user import Users


class Login(Resource):

    @classmethod
    def post(cls):
        data = request.form
        try:
            user = Users.objects.get(email=data['email'].lower())
            authorized = user.check_password(data['password'])

            if not authorized:
                raise UnauthorizedError

            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('home.html'), 200, headers)

        except DoesNotExist:
            raise UserNotExist

        except ValidationError:
            raise EmailInvalid

    @classmethod
    def get(cls):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)
