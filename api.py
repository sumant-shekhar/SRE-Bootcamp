from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from support.model import db
from support.view import StudentResource

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

api = Api(app)
CORS(app)

api.add_resource(StudentResource,"/api/students/","/api/students/<int:id>")

if __name__ == "__main__":
    app.run(debug=True)