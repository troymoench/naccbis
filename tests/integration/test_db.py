import pytest
from naccbis.Common import utils


class TestDB:
    @pytest.mark.integration
    def test_connect_db(self, db_url):
        with utils.connect_db(db_url) as conn:
            assert not conn.closed
            result = conn.execute("select version()").fetchone()
            assert len(result) == 1
            print(result)
        assert conn.closed
