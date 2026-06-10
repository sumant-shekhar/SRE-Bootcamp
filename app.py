# importing the necessary libraries
from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, fields, reqparse, Resource, marshal_with, abort
from sqlalchemy.exc import IntegrityError


# creating the Flask app
app = Flask(__name__)

# creating the API object
api = Api(app)

# data Base
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy()
db.init_app(app)


# model for DataBase
class StudentModel(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"
    
# request parser for the API endpoints"ORM"
student_args = reqparse.RequestParser()
student_args.add_argument("name",type=str,required=True,help="Name of the student is required")
student_args.add_argument("email",type=str,required=True,help="Email of the student is required")
student_args.add_argument("age",type=int,required=True,help="Age of the student is required")


# serializer for the API endpoints
studentFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "age": fields.Integer,
}

# Views for CRUD operations
class StudentResource(Resource):
    @marshal_with(studentFields)
    def get(self, id=None):
        # Get single student
        if id is not None:
            student = db.session.get(StudentModel, id)
            if not student:
                abort(404, message="Student not found")
            return student
        
        # Get all students
        students = StudentModel.query.all()
        return students
    
    @marshal_with(studentFields)
    def post(self):
        args = student_args.parse_args()
        student = StudentModel(name=args["name"], email=args["email"], age=args["age"])
        db.session.add(student)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Email already exists")
        return student, 201
    
    @marshal_with(studentFields)
    def put(self, id):
        args = student_args.parse_args()
        student = db.session.get(StudentModel, id)
        if not student:
            abort(404, message="Student not found")
        student.name = args["name"]
        student.email = args["email"]
        student.age = args["age"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Email already exists")
        return student
    
    @marshal_with(studentFields)
    def delete(self, id):
        student = db.session.get(StudentModel, id)
        if not student:
            abort(404, message="Student not found")
        db.session.delete(student)
        db.session.commit()
        return "deleted", 204

# Url routings
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# API endpoints
api.add_resource(
    StudentResource,
    "/v1/api/students/",
    "/v1/api/students/<int:id>",
)

# app runner
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=4000, debug=True)
