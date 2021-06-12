from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from flask import request, render_template, make_response
from flask_restful import Resource


class Verification(Resource):

    @classmethod
    def post(cls):

        public_key = request.files['public_key']
        signature = request.files['signature'].read()
        document = request.files['document'].read()

        public_key = serialization.load_pem_public_key(
            public_key.read(),
            backend=default_backend()
        )

        headers = {'Content-Type': 'text/html'}
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

            return {'message': 'valid!'}, 200
        except InvalidSignature:
            return {'message': 'invalid'}, 401


