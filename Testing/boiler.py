from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort

# ---------- App & DB setup ----------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///boiler_database.db"
db = SQLAlchemy(app)
api = Api(app)


# ---------- Model ----------
class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"<Item {self.name}>"


with app.app_context():
    db.create_all()


# ---------- Request parsers ----------
# POST: name required, description optional
create_args = reqparse.RequestParser()
create_args.add_argument("name", type=str, required=True, help="Name is required")
create_args.add_argument("description", type=str)

# PATCH: nothing required — only send the field(s) you want to change
patch_args = reqparse.RequestParser()
patch_args.add_argument("name", type=str)
patch_args.add_argument("description", type=str)


# ---------- Serializer ----------
item_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
}


# ---------- Resource ----------
class ItemResource(Resource):

    @marshal_with(item_fields)
    def get(self, id=None):
        if id is None:
            return ItemModel.query.all()
        item = db.session.get(ItemModel, id)
        if not item:
            abort(404, message="Item not found")
        return item

    @marshal_with(item_fields)
    def post(self):
        args = create_args.parse_args()
        item = ItemModel(name=args["name"], description=args["description"])
        db.session.add(item)
        db.session.commit()
        return item, 201

    @marshal_with(item_fields)
    def patch(self, id):
        item = db.session.get(ItemModel, id)
        if not item:
            abort(404, message="Item not found")

        args = patch_args.parse_args()
        if args["name"] is not None:
            item.name = args["name"]
        if args["description"] is not None:
            item.description = args["description"]

        db.session.commit()
        return item

    def delete(self, id):
        item = db.session.get(ItemModel, id)
        if not item:
            abort(404, message="Item not found")
        db.session.delete(item)
        db.session.commit()
        return "", 204


# ---------- Routes ----------
api.add_resource(ItemResource, "/items", "/items/<int:id>")


if __name__ == "__main__":
    app.run(debug=True) 