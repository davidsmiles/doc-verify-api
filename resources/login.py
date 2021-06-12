import datetime

from flask import request, make_response, render_template
from flask_jwt_extended import create_refresh_token, create_access_token
from flask_restful import Resource
from marshmallow import INCLUDE

from models.usermodel import UserModel
from schemas.user import UserSchema

user_schema = UserSchema(unknown=INCLUDE)


class Login(Resource):

    @classmethod
    def post(cls):
        # Get the Json payload
        data = request.get_json()
        user = user_schema.load(data)

        user = UserModel.find_by_email(user.email)

        if UserModel.is_login_valid(user, data['password']):
            expires = datetime.timedelta(seconds=1000)
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=expires)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token,
                       'logged_in_as': user.email
                   }, 200
        return {'message': 'empty'}
