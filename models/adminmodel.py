from time import time
from typing import List
from uuid import uuid4

from flask_bcrypt import generate_password_hash, check_password_hash

from extensions import db


class AdminModel(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(80), nullable=True, unique=True)
    password = db.Column(db.String(100), nullable=True)
    institution = db.Column(db.String(100), nullable=True)
    inst_code = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = uuid4().hex
        self.created_at = time()

    @classmethod
    def find_by_email(cls, email) -> "AdminModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_userid(cls, user_id) -> "AdminModel":
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_all(cls) -> List["AdminModel"]:
        return cls.query.all()

    @classmethod
    def hash_password(cls, password):
        password = generate_password_hash(password).decode('utf8')
        return password

    @classmethod
    def is_login_valid(cls, user, password):
        # Check if user exists and validate password
        if user and check_password_hash(user.password, password):
            return True
        return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
