from extensions import ma
from models.studentmodel import StudentModel


class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StudentModel
        # load_only = ("id", "confirmation")
        load_instance = False
