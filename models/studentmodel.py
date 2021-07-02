from time import time
from typing import List
from uuid import uuid4

from extensions import db


class StudentModel(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    graduation_year = db.Column(db.String(80), nullable=True)
    matric_no = db.Column(db.String(100), nullable=True)
    doc_id = db.Column(db.String(100), nullable=True, unique=True)
    course = db.Column(db.String(100), nullable=True)
    class_of_degree = db.Column(db.String(100), nullable=True)
    faculty = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = uuid4().hex
        self.created_at = time()

    @classmethod
    def find_by_email(cls, email) -> "StudentModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_matno(cls, matric_no) -> "StudentModel":
        return cls.query.filter_by(matric_no=matric_no).first()

    @classmethod
    def find_by_docid(cls, doc_id) -> "StudentModel":
        return cls.query.filter_by(doc_id=doc_id).first()

    @classmethod
    def find_all(cls) -> List["StudentModel"]:
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
