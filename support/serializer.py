# support/serializer.py

from flask_restful import fields

studentFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "age": fields.Integer,
}