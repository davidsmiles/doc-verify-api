import io
import qrcode
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from PyPDF2 import PdfFileWriter, PdfFileReader
from qrcode import ERROR_CORRECT_L
from reportlab.pdfgen import canvas


def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open('privatekey.cer', 'wb') as f:
        f.write(pem)

    public_key = private_key.public_key()
    pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open('publickey.cer', 'wb') as f:
        f.write(pub)

    return pem, pub


def load_keys():
    with open("privatekey.cer", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    with open("publickey.cer", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    return private_key, public_key


def sign(private_key, message):
    # message = b'I love you'
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def verify(public_key, signature, document):
    try:
        public_key.verify(
            signature,
            document,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False


def add_qr_to_doc(domain, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=ERROR_CORRECT_L,
        box_size=20,
        border=1
    )

    qr.add_data(f"{domain}/verify/user?{filename}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save('advanced.png')

    out_pdf_file = f'files/{filename}-file.pdf'
    img_file = 'advanced.png'

    packet = io.BytesIO()
    can = canvas.Canvas(packet)
    # can.drawString(10, 100, "Hello world")
    x_start = 5
    y_start = 5
    can.drawImage(img_file, x_start, y_start, width=100, height=100,
                  preserveAspectRatio=True, anchor='sw', mask='auto')
    can.showPage()
    can.showPage()
    can.showPage()
    can.save()

    # move to the beginning of the StringIO buffer
    packet.seek(0)

    new_pdf = PdfFileReader(packet)

    # read the existing PDF
    existing_pdf = PdfFileReader(open(filename, "rb"))
    output = PdfFileWriter()

    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.getPage(i)
        page.mergePage(new_pdf.getPage(i))
        output.addPage(page)

    outputStream = open(out_pdf_file, "wb")
    output.write(outputStream)
    outputStream.close()

    import os
    if os.path.exists(filename):
        os.remove(filename)

