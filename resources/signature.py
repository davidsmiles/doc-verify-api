import io

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from flask import request, send_file
from flask_restful import Resource

import helper
from helper import sign


class Signature(Resource):

    @classmethod
    def post(cls):
        data = request.files
        data_f = request.form
        private_key = data['private_key']
        private_key = serialization.load_pem_private_key(
            private_key.read(),
            password=None,
            backend=default_backend()
        )

        document = data['document']
        filename = f"{data_f['matno']}.pdf"
        document.save(filename)

        signature = sign(private_key, open(filename, 'rb').read())

        helper.add_qr_to_doc(filename, matno=data_f['matno'])

        # Save signature to Disk
        return send_file(
            io.BytesIO(signature),
            as_attachment=True,
            attachment_filename='signature.txt',
            mimetype='text/plain'
        )

