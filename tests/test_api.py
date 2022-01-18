from fastapi.testclient import TestClient
import pytest
from naccbis.api.main import app, get_db
from naccbis.api.database import create_session
from naccbis.common.settings import Settings

NACCBIS_DB_URL = "postgresql://localhost/naccbisdb_test"

test_settings = Settings(app_name="naccbis-tests", db_url=NACCBIS_DB_URL)
TestingSessionLocal = create_session(test_settings)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    return TestClient(app)


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"


@pytest.mark.xfail
def test_player(client):
    response = client.get("/player/engelcu01")
    assert response.status_code == 200
    print(response.json())


def test_game_log(client):
    response = client.get(
        "/game_log/",
        params={"team": "Wisconsin Lutheran", "season": 2018},
    )
    assert response.status_code == 200
    assert response.json() == []
