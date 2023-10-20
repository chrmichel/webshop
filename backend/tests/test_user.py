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

#TODO: add test for creation date
def test_get_user(client: TestClient):
    response = client.get("/users/mbiggie")
    assert response.status_code == 200
    assert response.json()["username"] == "mbiggie"
    assert response.json()["credit"] == 5212


def test_get_all_users(client: TestClient):
    response = client.get("/users/all")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    user = users[0]
    assert user["username"] == "mbiggie"
    assert user["credit"] == 5212


def test_create_user(client: TestClient, molly_in):
    response = client.post("/users/register", json=molly_in)
    assert response.json()["username"] == "rollymolly"
    assert response.json()["credit"] == 0
    assert response.status_code == 201


def test_create_user_email_repeat(client: TestClient, user_repeat_email):
    response = client.post("/users/register", json=user_repeat_email)
    assert response.status_code == 451


def test_create_user_username_repeat(
        client: TestClient, user_repeat_username
):
    response = client.post("/users/register", json=user_repeat_username)
    assert response.status_code == 451


def test_current_user(auth_client: TestClient):
    response = auth_client.get("/users/my-account")
    assert response.status_code == 200


def test_update_user(auth_client: TestClient, user_upate):
    response = auth_client.patch("/users/my-account", json=user_upate)
    assert response.status_code == 200


def test_delete_user(auth_client: TestClient):
    response = auth_client.delete("/users/delete")
    assert response.status_code == 204


def test_reset_password(auth_client: TestClient):
    new_pw = "NEW_Test_pw"
    response = auth_client.post(
        "/users/reset-password", json={"new_pw": new_pw}
    )
    assert response.status_code == 200


def test_add_credit(auth_client: TestClient, mike_in: dict):
    amount = 1
    response = auth_client.post("/users/add-credit", json={"amount": amount})
    assert response.status_code == 200
    assert response.json()["credit"] == mike_in["credit"] + amount


def test_add_credit_negative(auth_client: TestClient):
    amount = -2
    response = auth_client.post("/users/add-credit", json={"amount": amount})
    assert response.status_code == 422
    msg = """Input should be greater than 0"""
    assert response.json()["detail"][0]["msg"] == msg


def test_add_credit_float(auth_client: TestClient):
    amount = 1.6
    response = auth_client.post("/users/add-credit", json={"amount": amount})
    assert response.status_code == 422
    msg = "Input should be a valid integer, got a number with a fractional part"
    assert response.json()["detail"][0]["msg"] == msg
    