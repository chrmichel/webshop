from fastapi.testclient import TestClient
import pytest


def test_get_admin(client: TestClient, admin_in: dict):
    response = client.get(f"/users/{admin_in['username']}")
    assert response.status_code == 200
    assert response.json()["username"] == admin_in["username"]


def test_login_admin(client: TestClient, admin_in: dict):
    form_data = {"username": admin_in["username"], "password": admin_in["plainpw"]}
    response = client.post("/token", data=form_data)
    assert response.status_code == 200


def test_ban_mike(admin_client: TestClient, mike_in):
    r = admin_client.get(f"/users/{mike_in['username']}")
    assert r.status_code == 200
    mike_id = r.json()["id"]
    assert isinstance(mike_id, int)
    r2 = admin_client.put(f"/admin/ban/{mike_id}")
    assert r2.status_code == 200
    r3 = admin_client.get(f"/users/{mike_in['username']}")
    assert r3.status_code == 200
    assert r3.json()["is_active"] == False
