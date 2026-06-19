import os

# Use an isolated in-memory database for tests, set BEFORE importing app
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        with app.test_client() as test_client:
            yield test_client
        db.session.remove()
        db.drop_all()


def create_student(client, name="John Doe", email="john.doe@example.com", age=21):
    return client.post(
        "/v1/api/students/",
        json={"name": name, "email": email, "age": age},
    )


class TestHealthCheck:
    def test_healthcheck_returns_200_and_ok_status(self, client):
        response = client.get("/v1/api/healthcheck/")
        assert response.status_code == 200
        assert response.get_json()["status"] == "ok"


class TestCreateStudent:
    def test_create_student_returns_201(self, client):
        response = create_student(client)
        data = response.get_json()
        assert response.status_code == 201
        assert data["name"] == "John Doe"
        assert data["email"] == "john.doe@example.com"
        assert data["age"] == 21
        assert "id" in data

    def test_create_student_missing_field_returns_400(self, client):
        response = client.post(
            "/v1/api/students/",
            json={"name": "Jane Doe", "email": "jane@example.com"},  # missing age
        )
        assert response.status_code == 400

    def test_create_student_duplicate_email_returns_400(self, client):
        create_student(client, email="dup@example.com")
        response = create_student(client, name="Someone Else", email="dup@example.com")
        assert response.status_code == 400


class TestGetStudents:
    def test_get_all_students_returns_list(self, client):
        create_student(client, email="a@example.com")
        create_student(client, name="Jane Doe", email="b@example.com")

        response = client.get("/v1/api/students/")
        assert response.status_code == 200
        assert len(response.get_json()) == 2

    def test_get_single_student_returns_200(self, client):
        created = create_student(client).get_json()

        response = client.get(f"/v1/api/students/{created['id']}")
        assert response.status_code == 200
        assert response.get_json()["email"] == "john.doe@example.com"

    def test_get_nonexistent_student_returns_404(self, client):
        response = client.get("/v1/api/students/9999")
        assert response.status_code == 404


class TestUpdateStudent:
    def test_update_student_returns_200(self, client):
        created = create_student(client).get_json()

        response = client.put(
            f"/v1/api/students/{created['id']}",
            json={"name": "John Updated", "email": "john.updated@example.com", "age": 22},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "John Updated"
        assert data["age"] == 22

    def test_update_nonexistent_student_returns_404(self, client):
        response = client.put(
            "/v1/api/students/9999",
            json={"name": "Ghost", "email": "ghost@example.com", "age": 30},
        )
        assert response.status_code == 404


class TestDeleteStudent:
    def test_delete_student_returns_204(self, client):
        created = create_student(client).get_json()

        response = client.delete(f"/v1/api/students/{created['id']}")
        assert response.status_code == 204

        follow_up = client.get(f"/v1/api/students/{created['id']}")
        assert follow_up.status_code == 404

    def test_delete_nonexistent_student_returns_404(self, client):
        response = client.delete("/v1/api/students/9999")
        assert response.status_code == 404