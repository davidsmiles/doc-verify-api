import os

import PyPDF2
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for
import qrcode
from flask_restful import Api
from qrcode.constants import ERROR_CORRECT_L

from extensions import *
from helper import generate_keys, load_keys, sign, verify
from libs.errors import errors
from resources.keys import PrivateKey, PublicKey
from resources.login import Login
from resources.signature import Signature
from resources.signup import SignUp
from resources.verification import Verification

app = Flask(__name__)

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


api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(PrivateKey, '/privatekey')
api.add_resource(PublicKey, '/publickey')
api.add_resource(Signature, '/sign')
api.add_resource(Verification, '/verify')


if __name__ == '__main__':
    initialize_extensions(app)
    app.run(debug=True)
