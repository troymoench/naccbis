import pytest
from sqlalchemy import text

from naccbis.common import utils


@pytest.mark.integration
def test_connect_db(db_url: str) -> None:
    with utils.connect_db(db_url) as conn:
        assert not conn.closed
        result = conn.execute(text("select version()")).fetchone()
        print(result)
    assert conn.closed


@pytest.mark.integration
def test_engine(db_conn):
    print(db_conn.connection.dsn)
    assert not db_conn.closed
    result = db_conn.execute(text("select version()")).fetchone()
    assert len(result) == 1
