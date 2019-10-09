""" This module provides unit tests for common """
# Standard library imports
import unittest
# Third party imports
# Local imports
import naccbis.Common.utils as utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_parse_year(self):
        values = [{"year": "2017", "expected": [2017]},
                  {"year": "2016:2018", "expected": [2016, 2017, 2018]}]
        for value in values:
            self.assertEqual(utils.parse_year(value["year"]), value["expected"])

    def test_parse_stat(self):
        accepted = list(range(1, 8))
        values = [{"stats": "1", "expected": [1]},
                  {"stats": "1,2,3", "expected": [1, 2, 3]},
                  {"stats": "all", "expected": accepted}]
        for value in values:
            self.assertEqual(utils.parse_stat(value["stats"], accepted), value["expected"])

    def test_year_to_season(self):
        values = [{"year": "2010-11", "expected": 2011},
                  {"year": "2011-12", "expected": 2012},
                  {"year": "2012-13", "expected": 2013},
                  {"year": "2013-14", "expected": 2014},
                  {"year": "2014-15", "expected": 2015},
                  {"year": "2015-16", "expected": 2016},
                  {"year": "2016-17", "expected": 2017},
                  {"year": "2017-18", "expected": 2018}]
        for value in values:
            self.assertEqual(utils.year_to_season(value["year"]), value["expected"])

    def test_season_to_year(self):
        values = [{"season": 2011, "expected": "2010-11"},
                  {"season": 2012, "expected": "2011-12"},
                  {"season": 2013, "expected": "2012-13"},
                  {"season": 2014, "expected": "2013-14"},
                  {"season": 2015, "expected": "2014-15"},
                  {"season": 2016, "expected": "2015-16"},
                  {"season": 2017, "expected": "2016-17"},
                  {"season": 2018, "expected": "2017-18"}]
        for value in values:
            self.assertEqual(utils.season_to_year(value["season"]), value["expected"])

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
