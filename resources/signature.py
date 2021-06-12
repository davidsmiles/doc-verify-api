import io

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from flask import request, send_file, make_response, render_template
from flask_restful import Resource

from helper import sign


class Signature(Resource):

    @classmethod
    def post(cls):
        print(request.files)

        data = request.files
        private_key = data['private_key']
        private_key = serialization.load_pem_private_key(
            private_key.read(),
            password=None,
            backend=default_backend()
        )

        document = data['document'].read()
        signature = sign(private_key, document)

        # Save signature to Disk
        return send_file(
            io.BytesIO(signature),
            as_attachment=True,
            attachment_filename='signature.txt',
            mimetype='text/plain'
        )

