import os

import PyPDF2
import qrcode
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from qrcode.constants import ERROR_CORRECT_L
from reportlab.pdfgen import canvas

from extensions import *
from libs.errors import errors
from resources.routes import initialize_routes

app = Flask(__name__)
jwt = JWTManager(app)

load_dotenv('.env')
app.config.from_object(os.environ['APPLICATION_SETTINGS'])

api = Api(app, errors=errors)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    initialize_extensions(app)
    initialize_routes(api)
    app.run(debug=True)
