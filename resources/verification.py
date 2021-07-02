import io

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from flask import request, render_template, make_response, send_from_directory, send_file
from flask_restful import Resource
from marshmallow import INCLUDE

from libs.strings import gettext
from models.studentmodel import StudentModel
from schemas.student import StudentSchema

student_schema = StudentSchema(unknown=INCLUDE)


class Verification(Resource):

    @classmethod
    def post(cls):
        doc_id = request.form['doc_id']

        with open("publickey.cer", "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

        try:
            signature = open(f"signatures/signature-{doc_id}.txt", "rb").read()
            document = open(f'files/{doc_id}-file.pdf', 'rb').read()
        except FileNotFoundError:
            return {'message': 'doc not found'}, 404

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

            student = StudentModel.find_by_matno(doc_id)
            if not student:
                return {'message': gettext("user_not_found")}, 404

            return student_schema.dump(student), 200
        except InvalidSignature:
            return {'message': 'invalid'}, 401


class StudentImage(Resource):

    @classmethod
    def get(cls, matric_no):
        filename = f'{matric_no}.png'
        return send_file(
            io.BytesIO(open(f'images/{filename}', 'rb').read()),
            attachment_filename=filename,
            mimetype='image/png'
        )

