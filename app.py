import io
import os

import PyPDF2
import qrcode
from PyPDF2 import PdfFileReader, PdfFileWriter
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from qrcode.constants import ERROR_CORRECT_L
from reportlab.pdfgen import canvas

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
    box_size=20,
    border=1
)

pem, pub = load_keys()
signature = sign(pem, b'whats up')
print(verify(pub, signature, b'whats up'))

qr.add_data("http://localhost:8080/verify")
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save('advanced.png')


input_file = 'fakecert.pdf'
watermark = 'advanced.pdf'
output_file = 'certificate.pdf'

with open(input_file, 'rb') as file:
    pdf = PyPDF2.PdfFileReader(input_file)

    with open(watermark, 'rb') as wm_file:
        wm_pdf = PyPDF2.PdfFileReader(wm_file)

        with open(output_file, 'wb') as output:
            p = PyPDF2.PdfFileMerger(strict=True)
            p.append(wm_pdf)
            p.append(pdf)
            p.write(output)


def add_image():
    from PyPDF2 import PdfFileWriter, PdfFileReader
    import io

    in_pdf_file = 'fakecert.pdf'
    out_pdf_file = 'certificate.pdf'
    img_file = 'advanced.png'

    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    # can.drawString(10, 100, "Hello world")
    x_start = 5
    y_start = 5
    can.drawImage(img_file, x_start, y_start, width=100, height=100, preserveAspectRatio=True, anchor='sw', mask='auto')
    can.showPage()
    can.showPage()
    can.showPage()
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)

    new_pdf = PdfFileReader(packet)

    # read the existing PDF
    existing_pdf = PdfFileReader(open(in_pdf_file, "rb"))
    output = PdfFileWriter()

    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.getPage(i)
        page.mergePage(new_pdf.getPage(i))
        output.addPage(page)

    outputStream = open(out_pdf_file, "wb")
    output.write(outputStream)
    outputStream.close()


add_image()


@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == '__main__':
    initialize_extensions(app)
    initialize_routes(api)
    app.run(debug=True)
