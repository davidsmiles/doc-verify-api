from time import time

from bson import json_util
from flask_bcrypt import generate_password_hash, check_password_hash
from mongoengine import QuerySet

from extensions import db


class CustomQuerySet(QuerySet):
    def to_json(self):
        return "[%s]" % (",".join([doc.to_json() for doc in self]))


class Users(db.Document):
    institution = db.StringField(max_length=50)
    inst_code = db.StringField(max_length=50)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    created_at = db.IntField(default=time())

    @classmethod
    def hash_password(cls, password):
        password = generate_password_hash(password).decode('utf8')
        return password

    def check_password(self, password):
        return check_password_hash(self.password, password)

    meta = {'queryset_class': CustomQuerySet}

    def to_json(self):
        data = self.to_mongo()
        del (data['_id'])

        data['id'] = str(self.pk)

        return json_util.dumps(data)
