import pytest
import os
import app as flask_app


@pytest.fixture
def client():
    flask_app.DATABASE = "test_experiments.db"
    flask_app.app.config["TESTING"] = True

    with flask_app.app.test_client() as client:
        yield client

    os_remove_if_exists("test_experiments.db")


def os_remove_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)


def test_sample_experiment_returns_200(client):
    response = client.get("/api/experiment")
    assert response.status_code == 200
    assert response.get_json()["name"] == "baseline_model"


def test_register_success(client):
    response = client.post(
        "/register",
        json={"username": "agent007", "password": "supersecret"}
    )
    assert response.status_code == 201
    assert response.get_json()["username"] == "agent007"


def test_register_missing_password(client):
    response = client.post(
        "/register",
        json={"username": "agent007"}
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "username and password are required"


def test_register_duplicate_username(client):
    client.post("/register", json={"username": "agent007", "password": "pass1"})
    response = client.post("/register", json={"username": "agent007", "password": "pass2"})
    assert response.status_code == 409


def test_upload_experiment_missing_file(client):
    response = client.post(
        "/upload-experiment",
        json={"title": "test_run", "filename": "does_not_exist.csv"}
    )
    assert response.status_code == 400