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
    mike_username = r.json()["username"]
    assert isinstance(mike_username, str)
    r2 = admin_client.put(f"/admin/ban/{mike_username}")
    assert r2.status_code == 200
    r3 = admin_client.get(f"/users/{mike_in['username']}")
    assert r3.status_code == 200
    assert r3.json()["is_active"] == False


def test_unban_mike(admin_client: TestClient, mike_in):
    r = admin_client.get(f"/users/{mike_in['username']}")
    assert r.status_code == 200
    mike_username = r.json()["username"]
    assert isinstance(mike_username, str)
    r2 = admin_client.put(f"/admin/ban/{mike_username}")
    assert r2.status_code == 200
    r3 = admin_client.get(f"/users/{mike_in['username']}")
    assert r3.status_code == 200
    assert r3.json()["is_active"] == False
    r4 = admin_client.put(f"/admin/unban/{mike_username}")
    assert r4.status_code == 200
    r5 = admin_client.get(f"/users/{mike_in['username']}")
    assert r5.status_code == 200
    assert r5.json()["is_active"] == True


def test_promote_mike(admin_client: TestClient, mike_in):
    r = admin_client.post(f"/admin/promote/{mike_in['username']}")
    assert r.status_code == 200
    assert r.json()["role"] == "admin"
