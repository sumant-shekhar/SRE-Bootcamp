# support/model.py

from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse

db = SQLAlchemy()

class StudentModel(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"


# Request parser
student_args = reqparse.RequestParser()

student_args.add_argument("id", type=int)

student_args.add_argument("name",type=str,required=True,help="Name of the student is required")

student_args.add_argument("email",type=str,required=True,help="Email of the student is required")

student_args.add_argument("age",type=int,required=True,help="Age of the student is required")