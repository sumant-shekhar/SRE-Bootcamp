# importing the necessary libraries
import os
import logging
from dotenv import load_dotenv

from flask import Flask , render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, fields, reqparse, Resource, marshal_with, abort
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, OperationalError
from flask_migrate import Migrate

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# creating the Flask app
app = Flask(__name__)

# creating the API object
api = Api(app)

# data Base

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///database.db"
)
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

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
        logger.info(f"Fetching student with id={id}")
        # Get single student
        if id is not None:
            student = db.session.get(StudentModel, id)
            if not student:
                abort(404, message="Student not found")
            return student
        
        # Get all students
        logger.info("Fetching all students")
        students = StudentModel.query.all()
        return students
    
    @marshal_with(studentFields)
    def post(self):
        args = student_args.parse_args()
        logger.info(f"Creating student with email={args['email']}")
        student = StudentModel(name=args["name"], email=args["email"], age=args["age"])
        db.session.add(student)
        try:
            db.session.commit()
            logger.info(f"Student created with id={student.id}")
        except IntegrityError:
            logger.error("Email already exists")
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
            logger.info(f"Updating student with id={id}")
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
        logger.info(f"Deleting student with id={id}")
        db.session.commit()
        return "deleted", 204
    
class HealthCheck(Resource):
    def get(self):
        try:
            # Check database connectivity
            db.session.execute(text("SELECT 1"))
            return {"status": "ok", "database": "connected"}, 200
        except OperationalError as e:
            logger.error(f"Health check failed: Database unreachable. {str(e)}")
            return {"status": "unhealthy", "database": "disconnected", "error": "Database unreachable"}, 503
        except Exception as e:
            logger.error(f"Health check failed: Unexpected error. {str(e)}")
            return {"status": "unhealthy", "error": str(e)}, 500

# Url routings
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# API endpoints
# API endpoints
api.add_resource(
    StudentResource,
    "/v1/api/students/",
    "/v1/api/students/<int:id>",
)

api.add_resource(
    HealthCheck,
    "/v1/api/healthcheck/",
)

# app runner
if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=4000, debug=debug_mode)