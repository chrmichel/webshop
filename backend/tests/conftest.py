import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.config import ADMIN, MIKE, MOLLY, ADDRESS
from db.base_class import Base
from db.models import User
from db.session import get_db
from routers.login import router as login_router, get_current_user
from routers.users import router as user_router
from main import app as app_

# establish connection to test database
TEST_DB_URL = "sqlite:///test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def start_app() -> FastAPI:
    app = app_
    app.include_router(login_router)
    app.include_router(user_router, prefix="/users")
    return app


@pytest.fixture
def app() -> FastAPI:
    Base.metadata.create_all(engine)
    _app = start_app()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session() -> Session:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    yield session
    transaction.rollback()
    connection.close()


# different client preparations


@pytest.fixture
def client(app, db_session, mike_in, admin_in) -> Session:
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as _client:
        r = _client.post("/users/register", json=mike_in)
        if r.status_code != 201:
            raise Exception(r.json())
        r2 = _client.post("/admin/register", json=admin_in)
        if r2.status_code != 201:
            raise Exception(r2.json())
        yield _client


@pytest.fixture
def auth_client(client: TestClient, mike_in) -> Session:
    login_data = {"username": mike_in["username"], "password": mike_in["plainpw"]}
    r = client.post("/token", data=login_data)
    token = r.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    yield client


@pytest.fixture
def admin_client(client: TestClient, admin_in) -> Session:
    login_data = {"username": admin_in["username"], "password": admin_in["plainpw"]}
    r = client.post("/token", data=login_data)
    token = r.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    yield client


# other fixtures


@pytest.fixture
def mike_in() -> dict:
    mike = MIKE.model_dump()
    return mike


@pytest.fixture
def admin_in() -> dict:
    admin = ADMIN.model_dump()
    return admin


@pytest.fixture
def molly_in() -> dict:
    molly = MOLLY.model_dump()
    return molly


@pytest.fixture
def user_upate():
    return {"fullname": "Geronimo Souvlakis", "address": ADDRESS}
