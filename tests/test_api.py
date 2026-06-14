import pytest
from app import app, db

# TESTS FOR STUDENT API ENDPOINTS
@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()

        yield client

        with app.app_context():
            db.drop_all()

# CREATE STUDENT
def test_create_student(client):
    response = client.post("/v1/api/students/", json={
        "name": "John",
        "email": "john@test.com",
        "age": 22
    })

    assert response.status_code == 201
    assert response.json["email"] == "john@test.com"


# GET ALL STUDENTS
def test_get_students(client):
    client.post("/v1/api/students/", json={
        "name": "John",
        "email": "john@test.com",
        "age": 22
    })

    response = client.get("/v1/api/students/")

    assert response.status_code == 200
    assert len(response.json) >= 1


# GET ONE STUDENT
def test_get_single_student(client):
    res = client.post("/v1/api/students/", json={
        "name": "John",
        "email": "john@test.com",
        "age": 22
    })

    student_id = res.json["id"]

    response = client.get(f"/v1/api/students/{student_id}")

    assert response.status_code == 200
    assert response.json["id"] == student_id


# DELETE STUDENT
def test_delete_student(client):
    res = client.post("/v1/api/students/", json={
        "name": "John",
        "email": "john@test.com",
        "age": 22
    })

    student_id = res.json["id"]

    response = client.delete(f"/v1/api/students/{student_id}")

    assert response.status_code == 204