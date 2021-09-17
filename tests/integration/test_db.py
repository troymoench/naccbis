import pytest
from naccbis.Common import utils


@pytest.mark.integration
def test_connect_db(db_url: str):
    with utils.connect_db(db_url) as conn:
        assert not conn.closed
        result = conn.execute("select version()").fetchone()
        assert len(result) == 1
        print(result)
    assert conn.closed


@pytest.mark.integration
def test_engine(db_conn):
    print(db_conn.connection.dsn)
    assert not db_conn.closed
    result = db_conn.execute("select version()").fetchone()
    assert len(result) == 1
