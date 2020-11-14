""" This module provides unit tests for common """
# Standard library imports
# Third party imports
import pytest
# Local imports
from naccbis.Common import (utils, models)


@pytest.fixture
def accepted_stats():
    return list(range(1, 8))


class TestUtils():
    @pytest.mark.parametrize(
        'year, expected', [('2017', [2017]), ('2016:2018', [2016, 2017, 2018])]
    )
    def test_parse_year(self, year, expected):
        assert utils.parse_year(year) == expected

    @pytest.mark.parametrize(
        'year, expected', [
            ('2010-11', 2011),
            ('2011-12', 2012),
            ('2012-13', 2013),
            ('2013-14', 2014),
            ('2014-15', 2015),
            ('2015-16', 2016),
            ('2016-17', 2017),
            ('2017-18', 2018),
        ]
    )
    def test_year_to_season(self, year, expected):
        assert utils.year_to_season(year) == expected

    @pytest.mark.parametrize(
        'season, expected', [
            (2011, '2010-11'),
            (2012, '2011-12'),
            (2013, '2012-13'),
            (2014, '2013-14'),
            (2015, '2014-15'),
            (2016, '2015-16'),
            (2017, '2016-17'),
            (2018, '2017-18'),
        ]
    )
    def test_season_to_year(self, season, expected):
        assert utils.season_to_year(season) == expected


@pytest.fixture()
def db_config():
    return utils.init_config().get("DB")


class TestDB():
    @pytest.mark.integration
    def test_connect_db(self, db_config):
        with utils.connect_db(db_config) as conn:
            assert not conn.closed
            result = conn.execute("select version()").fetchone()
            assert len(result) == 1
            print(result)
        assert conn.closed
