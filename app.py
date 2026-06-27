# importing the necessary libraries
import os
import logging
from dotenv import load_dotenv

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, fields, reqparse, Resource, marshal_with, abort
from flask_cors import CORS
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, OperationalError
from flask_migrate import Migrate

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# creating the Flask app
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
if not app.config['SECRET_KEY']:
    raise ValueError("SECRET_KEY is not set! Please add it to your .env file.")

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# cross-origin requests
CORS(app)

# creating the API object
api = Api(app)

# Create SQLAlchemy instance
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

# model for the database
class StudentModel(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"


# request parser
student_args = reqparse.RequestParser()
student_args.add_argument("name", type=str, required=True, help="Name of the student is required")
student_args.add_argument("email", type=str, required=True, help="Email of the student is required")
student_args.add_argument("age", type=int, required=True, help="Age of the student is required")


# serializer
studentFields = {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "age": fields.Integer,
}

# validate inp function
def validate_student_args(args):
    # age should be a realistic positive number
    if args["age"] <= 0 or args["age"] > 40:
        abort(400, message="Age must be between 1 and 40")

    # very basic email format check
    if "@" not in args["email"] or "." not in args["email"]:
        abort(400, message="Please provide a valid email address")

class StudentListResource(Resource):

    @marshal_with(studentFields)
    def get(self):
        # basic pagination boil
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 20, type=int)

        logger.info(f"Fetching students — page={page}, per_page={per_page}")
        students = StudentModel.query.paginate(page=page, per_page=per_page, error_out=False)
        return students.items

    @marshal_with(studentFields)
    def post(self):
        args = student_args.parse_args()
        validate_student_args(args)

        logger.info(f"Creating student with email={args['email']}")
        student = StudentModel(
            name=args["name"],
            email=args["email"],
            age=args["age"]
        )
        db.session.add(student)

        try:
            db.session.commit()
            logger.info(f"Student created with id={student.id}")
        except IntegrityError:
            logger.error("Email already exists")
            db.session.rollback()
            abort(400, message="Email already exists")

        return student, 201

class StudentDetailResource(Resource):

    @marshal_with(studentFields)
    def get(self, id):
        logger.info(f"Fetching student with id={id}")
        student = db.session.get(StudentModel, id)
        if not student:
            abort(404, message="Student not found")
        return student

    @marshal_with(studentFields)
    def put(self, id):
        args = student_args.parse_args()
        validate_student_args(args)

        student = db.session.get(StudentModel, id)
        if not student:
            abort(404, message="Student not found")

        student.name = args["name"]
        student.email = args["email"]
        student.age = args["age"]

        try:
            logger.info(f"Updating student with id={id}")
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="Email already exists")

        return student

    def delete(self, id):
        student = db.session.get(StudentModel, id)
        if not student:
            abort(404, message="Student not found")

        db.session.delete(student)
        logger.info(f"Deleting student with id={id}")
        db.session.commit()

        return {"message": "Student deleted successfully"}, 200

# HealthCheck 
class HealthCheck(Resource):
    def get(self):
        try:
            db.session.execute(text("SELECT 1"))
            return {"status": "ok", "database": "connected"}, 200
        except OperationalError as e:
            logger.error(f"Health check failed: Database unreachable. {str(e)}")
            return {"status": "unhealthy", "database": "disconnected", "error": "Database unreachable"}, 503
        except Exception as e:
            logger.error(f"Health check failed: Unexpected error. {str(e)}")
            return {"status": "unhealthy", "error": str(e)}, 500

# HTML page
@app.route("/list", methods=["GET"])
def list_students():
    return render_template("list.html", students=StudentModel.query.all())

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# API endpoints 
api.add_resource(StudentListResource, "/v1/api/students/")
api.add_resource(StudentDetailResource, "/v1/api/students/<int:id>")
api.add_resource(HealthCheck, "/v1/api/healthcheck/")

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 4000))
    app.run(host=host, port=port, debug=debug_mode)