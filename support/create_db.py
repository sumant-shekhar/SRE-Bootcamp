# support/create_db.py
from api import app, db

with app.app_context():
    db.create_all()