import io

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from flask import request, send_file
from flask_restful import Resource
from marshmallow import INCLUDE

import helper
from helper import sign
from models.studentmodel import StudentModel
from schemas.student import StudentSchema

student_schema = StudentSchema(unknown=INCLUDE)


class Signature(Resource):

    @classmethod
    def post(cls):
        data = request.files
        data_f = request.form

        student = StudentModel.find_by_docid(data_f['doc_id'])
        if student:
            return student_schema.dump(student), 401

        student = StudentModel(**data_f)
        student.save_to_db()

        photo_path = f'images/{data_f["doc_id"]}.png'
        data['photograph'].save(photo_path)

        with open("privatekey.cer", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        document = data['document']
        filename = f"{data_f['doc_id']}"
        document.save(filename)

        helper.add_qr_to_doc(request.url_root[:-1], filename)
        signature = sign(private_key, open(f'files/{filename}-file.pdf', 'rb').read())

        # Save signature to Disk
        with open(f'signatures/signature-{filename}.txt', 'wb') as sig:
            sig.write(signature)
            sig.close()

        return send_file(
            io.BytesIO(open(f'files/{filename}-file.pdf', 'rb').read()),
            attachment_filename=f'files/{filename}-file.pdf',
            mimetype='application/pdf'
        )


