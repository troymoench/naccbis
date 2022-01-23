from fastapi.testclient import TestClient
import pytest
from sqlalchemy import delete
from naccbis.api.main import app, get_db
from naccbis.api.database import create_session
from naccbis.common.models import GameLog
from naccbis.common.settings import Settings

NACCBIS_DB_URL = "postgresql:///naccbisdb_test"

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


@pytest.fixture
def db():
    with TestingSessionLocal() as session:
        yield session


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"


@pytest.mark.xfail
def test_player(client):
    response = client.get("/player/engelcu01")
    assert response.status_code == 200
    print(response.json())


def test_game_log(client, db):
    game_log1 = GameLog(
        game_num=25,
        date="2018-04-21",
        season=2018,
        team="Wisconsin Lutheran",
        opponent="Dominican",
        result="W",
        rs=14,
        ra=1,
        home=False,
        conference=True,
    )
    game_log2 = GameLog(
        game_num=15,
        date="2018-04-08",
        season=2018,
        team="Edgwood",
        opponent="Wisconsin Lutheran",
        result="L",
        rs=3,
        ra=4,
        home=True,
        conference=True,
    )
    db.add_all([game_log1, game_log2])
    db.commit()
    response = client.get(
        "/game_log/",
        params={"team": "Wisconsin Lutheran", "season": 2018},
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "game_num": 25,
            "date": "2018-04-21",
            "season": 2018,
            "team": "Wisconsin Lutheran",
            "opponent": "Dominican",
            "result": "W",
            "rs": 14,
            "ra": 1,
            "home": False,
            "conference": True,
        }
    ]
    db.execute(delete(GameLog))
    db.commit()
