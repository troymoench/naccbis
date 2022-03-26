from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from naccbis.api.database import create_session
from naccbis.api.main import app, get_db
from naccbis.common.models import GameLog
from naccbis.common.settings import Settings

NACCBIS_DB_URL = "postgresql:///naccbisdb_test"

test_settings = Settings(app_name="naccbis-tests", db_url=NACCBIS_DB_URL)
TestingSessionLocal = create_session(test_settings)


@pytest.fixture
def db(db_conn) -> Iterator[Session]:
    """Create a session that does a rollback after each test"""
    db_conn.begin()
    session = TestingSessionLocal(bind=db_conn)
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def client(db: Session) -> Iterator[TestClient]:
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client


def test_ping(client: TestClient):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"


@pytest.mark.xfail
def test_player(client: TestClient):
    response = client.get("/player/engelcu01")
    assert response.status_code == 200
    print(response.json())


def test_game_log(client: TestClient, db: Session):
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
        params={"team": "Wisconsin Lutheran", "season": "2018"},
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
