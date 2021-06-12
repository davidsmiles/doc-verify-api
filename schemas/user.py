from marshmallow import pre_dump

from extensions import ma
from models.usermodel import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        # load_only = ("id", "confirmation")
        load_instance = True

    # @pre_dump
    # def _pre_dump(self, user: UserModel, **kwargs):
    #     user.confirmation = [user.most_recent_confirmation]
    #     return user
