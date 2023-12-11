from fastapi.testclient import TestClient


def test_startup(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    # assert response.json() == {"message": "Hello world"}
