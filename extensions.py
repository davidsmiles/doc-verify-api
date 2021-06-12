from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
ma = Marshmallow()
db = SQLAlchemy()


def initialize_extensions(app):
    bcrypt.init_app(app)
    db.init_app(app)
    ma.init_app(app)

