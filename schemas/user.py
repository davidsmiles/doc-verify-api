from marshmallow import pre_dump

from extensions import ma
from models.adminmodel import AdminModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AdminModel
        # load_only = ("id", "confirmation")
        load_instance = False

    # @pre_dump
    # def _pre_dump(self, user: AdminModel, **kwargs):
    #     user.confirmation = [user.most_recent_confirmation]
    #     return user
