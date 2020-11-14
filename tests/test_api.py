from fastapi.testclient import TestClient
import pytest
from naccbis.api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"
