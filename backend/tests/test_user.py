from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def user_repeat_email(mike_in):
    return {
        "username": "name",
        "fullname": "Full Name",
        "email": mike_in["email"],
        "plainpw": "testpw"
    }

@pytest.fixture
def user_repeat_username(mike_in):
    return {
        "username": mike_in["username"],
        "fullname": "Full Name",
        "email": "bitch@aol.com",
        "plainpw": "testpw"
    }


def test_get_user(client: TestClient):
    response = client.get("/users/mbiggie")
    assert response.status_code == 200
    assert response.json()["username"] == "mbiggie"
    assert response.json()["fullname"] == "Michael Biggs"
    assert response.json()["credit"] == 5212


def test_create_user(client: TestClient, molly_in):
    response = client.post("/users/", json=molly_in)
    assert response.json()["username"] == "rollymolly"
    assert response.json()["fullname"] == "Molly Flynn"
    assert response.json()["credit"] == 0
    assert response.status_code == 201


def test_create_user_email_repeat(client: TestClient, user_repeat_email):
    response = client.post("/users", json=user_repeat_email)
    assert response.status_code == 451


def test_create_user_username_repeat(client: TestClient, user_repeat_username):
    response = client.post("/users", json=user_repeat_username)
    assert response.status_code == 451
