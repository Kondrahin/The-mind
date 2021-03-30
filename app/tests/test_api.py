import os

from fastapi.testclient import TestClient
import pytest
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.main import app
from app.models.models import Player

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@host/db_name"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

with engine.connect() as conn:
    with open(os.path.abspath('app/db/schema.sql')) as schema:
        conn.execute(schema.read())


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

test_player1 = Player()
test_player2 = Player()
test_player3 = Player()


def test_create_room():
    response = client.post("http://127.0.0.1:8000/create/?player_nick=test_player1")
    data = response.json()
    test_player1.id = data['player_token']
    test_player1.room_token = data['room_token']
    assert response.status_code == 200


def test_is_admin():
    response = client.post(
        f"http://127.0.0.1:8000/is_admin/?player_token={test_player1.id}&room_token={test_player1.room_token}")
    data = response.json()
    assert response.status_code == 200
    assert data['result'] == True


def test_connect():
    response = client.post(
        f"http://127.0.0.1:8000/connect_to_room/?player_nick=test_player2&room_token={test_player1.room_token}")
    data = response.json()
    assert response.status_code == 200
    assert data['result'] == True


def test_bad_connect():
    response = client.post(
        f"http://127.0.0.1:8000/connect_to_room/?player_nick=test_player2&room_token=123")
    data = response.json()
    assert response.status_code == 404
    # assert data['result'] == False
