import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

from core.config import MIKE, MOLLY
from crud.hashing import Hasher
from db.base_class import Base
from db.models import User
from db.session import get_db
from routers.login import router as login_router
from routers.users import router as user_router
from main import app as app_

# establish connection to test database
TEST_DB_URL = "sqlite:///test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def start_app():
    app = app_
    # app.include_router(login_router)
    # app.include_router(user_router, prefix="/users")
    return app

@pytest.fixture
def app():
    Base.metadata.create_all(engine)
    _app = start_app()
    yield _app
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(mike_user):
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    # session.add(mike_user)
    # session.commit()
    yield session
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(app, db_session):

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as _client:
        yield _client

# other fixtures

@pytest.fixture
def mike_user():
    mike = MIKE.model_dump()
    plainpw = mike.pop("plainpw")
    mike["hashedpw"] = plainpw
    return User(**mike)

@pytest.fixture
def molly_user():
    molly = MOLLY.model_dump()
    plainpw = molly.pop("plainpw")
    molly["hashedpw"] = plainpw
    return User(**molly)

@pytest.fixture
def mike_json():
    return MIKE.model_dump_json()

@pytest.fixture
def molly_json():
    return MOLLY.model_dump_json()