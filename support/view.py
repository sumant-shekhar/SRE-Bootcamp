# support/view.py

from flask_restful import Resource, marshal_with

from support.model import db, StudentModel, student_args
from support.serializer import studentFields


class StudentResource(Resource):

    @marshal_with(studentFields)
    def get(self, id=None):

        # Get single student
        if id:
            student = StudentModel.query.get(id)

            if not student:
                return {"message": "Student not found"}, 404

            return student

        # Get all students
        return StudentModel.query.all()

    @marshal_with(studentFields)
    def post(self):
        args = student_args.parse_args()

        student = StudentModel(
            name=args["name"],
            email=args["email"],
            age=args["age"]
        )

        db.session.add(student)
        db.session.commit()

        return student, 201

    @marshal_with(studentFields)
    def patch(self, id):
        args = student_args.parse_args()

        student = StudentModel.query.filter_by(id=id).first()

        if not student:
            return {"message": "Student not found"}, 404

        student.name = args["name"]
        student.email = args["email"]
        student.age = args["age"]

        db.session.commit()

        return student, 200

    @marshal_with(studentFields)
    def delete(self, id):
        student = StudentModel.query.filter_by(id=id).first()

        if not student: 
            return {"message": "Student not found"}, 404

        db.session.delete(student)
        db.session.commit()
        return student