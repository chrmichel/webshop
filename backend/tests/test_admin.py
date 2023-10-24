from fastapi.testclient import TestClient
import pytest

def test_get_admin(client: TestClient, admin_in: dict):
    response = client.get(f"/users/{admin_in['username']}")
    assert response.status_code == 200
    assert response.json()["username"] == admin_in["username"]

def test_login_admin(client: TestClient, admin_in: dict):
    form_data = {
        "username": admin_in["username"],
        "password": admin_in["plainpw"]
    }
    response = client.post("/token", data=form_data)
    assert response.status_code == 200
