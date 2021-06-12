import os

import qrcode
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from qrcode.constants import ERROR_CORRECT_L

from extensions import *
from helper import load_keys, sign, verify
from libs.errors import errors
from resources.routes import initialize_routes

app = Flask(__name__)
jwt = JWTManager(app)

load_dotenv('.env')
app.config.from_object(os.environ['APPLICATION_SETTINGS'])

api = Api(app, errors=errors)

qr = qrcode.QRCode(
    version=1,
    error_correction=ERROR_CORRECT_L,
    box_size=50,
    border=1
)

pem, pub = load_keys()
signature = sign(pem, b'whats up')
print(verify(pub, signature, b'whats up'))

qr.add_data("")
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save('advanced.png')

#
# input_file = 'theo-yranscript.pdf'
# watermark = 'advanced.pdf'
# output_file = 'transcript.pdf'
#
# with open(input_file, 'rb') as file:
#     pdf = PyPDF2.PdfFileReader(input_file)
#
#     with open(watermark, 'rb') as wm_file:
#         wm_pdf = PyPDF2.PdfFileReader(wm_file)
#
#         with open(output_file, 'wb') as output:
#             p = PyPDF2.PdfFileMerger(strict=True)
#             p.append(wm_pdf)
#             p.append(pdf)
#             p.write(output)


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    initialize_extensions(app)
    initialize_routes(api)
    app.run(debug=True)
