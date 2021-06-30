import io

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import send_file, request
from flask_restful import Resource


class PrivateKey(Resource):

    @classmethod
    def get(cls):
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

        return send_file(
            io.BytesIO(pem),
            attachment_filename='privatekey.cer',
            mimetype='application/x-x509-ca-cert'
        )


class PublicKey(Resource):

    @classmethod
    def get(cls):
        print(request.files)
        private_key = request.files['private_key']
        private_key = serialization.load_pem_private_key(
            private_key.read(),
            password=None,
            backend=default_backend()
        )

        public_key = private_key.public_key()
        pub = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return send_file(
            io.BytesIO(pub),
            attachment_filename='publickey.cer',
            mimetype='application/x-x509-ca-cert'
        )
