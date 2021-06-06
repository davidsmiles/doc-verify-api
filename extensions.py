from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine

bcrypt = Bcrypt()
db = MongoEngine()


def initialize_extensions(app):
    bcrypt.init_app(app)
    db.init_app(app)
