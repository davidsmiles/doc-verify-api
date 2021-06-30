import datetime

from flask import request
from flask_jwt_extended import create_refresh_token, create_access_token
from flask_restful import Resource
from marshmallow import INCLUDE

from models.usermodel import UserModel
from models.adminmodel import AdminModel
from schemas.user import UserSchema

user_schema = UserSchema(unknown=INCLUDE)


class Login(Resource):

    @classmethod
    def post(cls):
        # Get the Json payload
        data = request.get_json()
        user = UserModel(**user_schema.load(data))

        user = UserModel.find_by_email(user.email)

        if UserModel.is_login_valid(user, data['password']):
            expires = datetime.timedelta(seconds=1000)
            access_token = create_access_token(identity=user.id, fresh=True, expires_delta=expires)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token,
                       'logged_in_as': "user"
                   }, 200

        admin = AdminModel(**user_schema.load(data))
        admin = AdminModel.find_by_email(admin.email)
        if AdminModel.is_login_valid(admin, data['password']):
            expires = datetime.timedelta(seconds=1000)
            access_token = create_access_token(identity=admin.id, fresh=True, expires_delta=expires)
            refresh_token = create_refresh_token(identity=admin.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token,
                       'logged_in_as': "admin"
                   }, 200

        return {'message': 'empty'}, 401

