""" This module provides data cleaning unit tests """
# Standard library imports
import datetime
import unittest
# Third party imports
import pandas as pd
# Local imports
import CleanFunctions as cf
import CleanGameLogs as cgl
import GenerateIds as gi
import CleanIndividualPitching as cip


class TestCleanFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_id(self):
        self.assertEqual(cf.create_id("Curtis", "Engelbrecht"), "engelcu01")

    def test_add_n(self):
        self.assertEqual(cf.add_n("engelcu01", 2), "engelcu03")

    def test_normalize_names(self):
        df1 = pd.DataFrame({"name": ["Jeffrey  Mayes", "D.J.  Dillon", "Quinlan Milne Rojek"],
                            "team": ["AUR", "BEN", "DOM"],
                            "season": [2017, 2017, 2016]}, columns=["name", "team", "season"])
        df2 = pd.DataFrame(df1)
        df2["fname"] = ["Jeffrey", "DJ", "Quinlan"]
        df2["lname"] = ["Mayes", "Dillon", "Milne Rojek"]
        self.assertTrue(cf.normalize_names(df1).equals(df2))

    # def test_apply_corrections(self):
    #     pass

    def test_convert_ip(self):
        values = [{"raw": "10.0", "expected": 10.0},
                  {"raw": "10.1", "expected": 10 + (1/3)},
                  {"raw": "10.2", "expected": 10 + (2/3)}]
        for value in values:
            self.assertEqual(cf.convert_ip(value["raw"]), value["expected"])

    def tearDown(self):
        pass


class TestGenerateIds(unittest.TestCase):
    def setUp(self):
        pass

    def test_update_id_conflicts(self):
        #          lname   fname  team  season  player_id       full_name
        # 2916    Balind  Garett   CUC    2011  balinga01   Garett Balind
        # 1765    Balind  Garett   CUC    2010  balinga01   Garett Balind
        # 1113  Balinski   Galen  MARN    2013  balinga01  Galen Balinski
        # 2176  Schoemann  Tyler  WLC    2018  schoety01  Tyler Schoemann
        # 1937     Schoen  Tyler  WLC    2010  schoety01     Tyler Schoen
        # 1692     Schoen  Tyler  WLC    2011  schoety01     Tyler Schoen
        # 1436     Schoen  Tyler  WLC    2012  schoety01     Tyler Schoen
        # 1176     Schoen  Tyler  WLC    2013  schoety01     Tyler Schoen

        raw = pd.DataFrame([("Balind", "Garett", "CUC", 2011, "balinga01", "Garett Balind"),
                            ("Balind", "Garett", "CUC", 2010, "balinga01", "Garett Balind"),
                            ("Balinski", "Galen", "MARN", 2013, "balinga01", "Galen Balinski"),
                            ("Schoemann", "Tyler", "WLC", 2018, "schoety01", "Tyler Schoemann"),
                            ("Schoen", "Tyler", "WLC", 2010, "schoety01", "Tyler Schoen"),
                            ("Schoen", "Tyler", "WLC", 2011, "schoety01", "Tyler Schoen"),
                            ("Schoen", "Tyler", "WLC", 2012, "schoety01", "Tyler Schoen"),
                            ("Schoen", "Tyler", "WLC", 2013, "schoety01", "Tyler Schoen")],
                            columns=["lname", "fname", "team", "season", "player_id", "full_name"])

        expected = pd.DataFrame([("Balind", "Garett", "CUC", 2011, "balinga01", "Garett Balind"),
                                 ("Balind", "Garett", "CUC", 2010, "balinga01", "Garett Balind"),
                                 ("Balinski", "Galen", "MARN", 2013, "balinga02", "Galen Balinski"),
                                 ("Schoemann", "Tyler", "WLC", 2018, "schoety02", "Tyler Schoemann"),
                                 ("Schoen", "Tyler", "WLC", 2010, "schoety01", "Tyler Schoen"),
                                 ("Schoen", "Tyler", "WLC", 2011, "schoety01", "Tyler Schoen"),
                                 ("Schoen", "Tyler", "WLC", 2012, "schoety01", "Tyler Schoen"),
                                 ("Schoen", "Tyler", "WLC", 2013, "schoety01", "Tyler Schoen")],
                                 columns=["lname", "fname", "team", "season", "player_id", "full_name"])

        self.assertTrue(gi.update_id_conflicts(raw).equals(expected))

    def tearDown(self):
        pass


class TestCleanGameLogs(unittest.TestCase):
    def setUp(self):
        pass

    def test_extract_result(self):
        scores = [{"raw": "L, 10-8", "expected": "L"},
                  {"raw": "W, 17-6", "expected": "W"},
                  {"raw": "W, 5-4", "expected": "W"},
                  {"raw": "L, 5-4", "expected": "L"}]
        for score in scores:
            self.assertEqual(cgl.extract_result(score["raw"]), score["expected"])

    def test_extract_runs(self):
        scores = [{"raw": "L, 10-8", "expected": [8, 10]},
                  {"raw": "W, 17-6", "expected": [17, 6]},
                  {"raw": "W, 5-4", "expected": [5, 4]},
                  {"raw": "L, 5-4", "expected": [4, 5]}]
        for score in scores:
            self.assertEqual(cgl.extract_runs(score["raw"]), score["expected"])

    def test_extract_opponent(self):
        opponents = [{"raw": "at Benedictine", "expected": "Benedictine"},
                     {"raw": "vs. Benedictine", "expected": "Benedictine"},
                     {"raw": "vs Benedictine", "expected": "Benedictine"},
                     {"raw": "Benedictine", "expected": "Benedictine"},
                     {"raw": "vs. St. Lawrence", "expected": "St. Lawrence"}]
        for opponent in opponents:
            self.assertEqual(cgl.extract_opponent(opponent["raw"]), opponent["expected"])

    def test_extract_home(self):
        opponents = [{"raw": "at Benedictine", "expected": False},
                     {"raw": "vs. Benedictine", "expected": True},
                     {"raw": "Benedictine", "expected": True}]
        for opponent in opponents:
            self.assertEqual(cgl.extract_home(opponent["raw"]), opponent["expected"])

    def test_extract_conference(self):
        values = [{"opponent": "Maranatha", "season": 2013, "expected": True},
                  {"opponent": "Maranatha", "season": 2014, "expected": False},
                  {"opponent": "Carthage", "season": 2018, "expected": False},
                  {"opponent": "Marian", "season": 2017, "expected": True}]
        teams = ["Aurora", "Benedictine", "Concordia Chicago", "Concordia Wisconsin", "Dominican",
                 "Edgewood", "Lakeland", "MSOE", "Marian", "Maranatha", "Rockford", "Wisconsin Lutheran"]
        for value in values:
            self.assertEqual(cgl.extract_conference(value["opponent"], value["season"], teams), value["expected"])

    def test_extract_date(self):
        values = [{"date_str": "Mar 6", "season": 2010, "expected": datetime.datetime(2010, 3, 6)},
                  {"date_str": "May 14", "season": 2010, "expected": datetime.datetime(2010, 5, 14)},
                  {"date_str": "Feb 28", "season": 2010, "expected": datetime.datetime(2010, 2, 28)},
                  {"date_str": "Apr 02", "season": 2014, "expected": datetime.datetime(2014, 4, 2)},
                  {"date_str": "May 20", "season": 2016, "expected": datetime.datetime(2016, 5, 20)},
                  {"date_str": "Apr 30", "season": 2018, "expected": datetime.datetime(2018, 4, 30)}]

        for value in values:
            self.assertEqual(cgl.extract_date(value["date_str"], value["season"]), value["expected"])

    def tearDown(self):
        pass


# class TestCleanIndividualPitching(unittest.TestCase):
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass


if __name__ == "__main__":
    unittest.main()
