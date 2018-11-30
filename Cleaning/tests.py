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
import LeagueTotals as lt


class TestCleanFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_id(self):
        values = [{"fname": "Curtis", "lname": "Engelbrecht", "expected": "engelcu01"},
                  {"fname": "Garrett", "lname": "Balind", "expected": "balinga01"},
                  {"fname": "Galen", "lname": "Balinski", "expected": "balinga01"},
                  {"fname": "Patrick", "lname": "O'Malley", "expected": "omallpa01"}]
        for value in values:
            self.assertEqual(cf.create_id(value["fname"], value["lname"]), value["expected"])

    def test_add_n(self):
        values = [{"id": "engelcu01", "n": 0, "expected": "engelcu01"},
                  {"id": "engelcu01", "n": 1, "expected": "engelcu02"},
                  {"id": "engelcu01", "n": 2, "expected": "engelcu03"}]
        for value in values:
            self.assertEqual(cf.add_n(value["id"], value["n"]), value["expected"])

    def test_normalize_names(self):
        df1 = pd.DataFrame({"name": ["Jeffrey  Mayes", "D.J.  Dillon", "Quinlan Milne Rojek"],
                            "team": ["AUR", "BEN", "DOM"],
                            "season": [2017, 2017, 2016]}, columns=["name", "team", "season"])
        df2 = pd.DataFrame(df1)
        df2["fname"] = ["Jeffrey", "DJ", "Quinlan"]
        df2["lname"] = ["Mayes", "Dillon", "Milne Rojek"]
        self.assertTrue(cf.normalize_names(df1).equals(df2))

    def test_apply_corrections(self):
        #          uc_fname     uc_lname uc_team  uc_season      c_fname           c_lname
        # 0        Steven       Jaquez     AUR       2014           Ty            Jaquez
        # 1        Steven       Jaquez     AUR       2015           Ty            Jaquez
        # 2        Steven       Jaquez     AUR       2016           Ty            Jaquez
        # 3           Dan     Lo dolce     CUC       2014          Dan          Lo Dolce
        # 4           Dan      Lodolce     CUC       2015          Dan          Lo Dolce
        # 5            Tj        McCoy     MAR       2013           TJ             McCoy
        # 6            Tj        McCoy     MAR       2014           TJ             McCoy
        # 7            Aj       Alessi     MAR       2014           AJ            Alessi

        corrections = pd.DataFrame([("Steven", "Jaquez", "AUR", 2014, "Ty", "Jaquez", "C"),
                                    ("Steven", "Jaquez", "AUR", 2015, "Ty", "Jaquez", "C"),
                                    ("Steven", "Jaquez", "AUR", 2016, "Ty", "Jaquez", "C"),
                                    ("Dan", "Lo dolce", "CUC", 2014, "Dan", "Lo Dolce", "T"),
                                    ("Dan", "Lodolce", "CUC", 2015, "Dan", "Lo Dolce", "T"),
                                    ("Tj", "McCoy", "MAR", 2013, "TJ", "McCoy", "T"),
                                    ("Tj", "McCoy", "MAR", 2014, "TJ", "McCoy", "T"),
                                    ("Aj", "Alessi", "MAR", 2014, "AJ", "Alessi", "T")],
                                   columns=["uc_fname", "uc_lname", "uc_team",
                                            "uc_season", "c_fname", "c_lname", "type"])

        data = pd.DataFrame([("Jaquez", "Steven", "AUR", 2014),
                             ("Jaquez", "Steven", "AUR", 2015),
                             ("Jaquez", "Steven", "AUR", 2016),
                             ("Jaquez", "Ty", "AUR", 2017),
                             ("Ackerman", "Kamren", "BEN", 2015),
                             ("Ackerman", "Kamren", "BEN", 2016),
                             ("Ackerman", "Kamren", "BEN", 2017),
                             ("Lo dolce", "Dan", "CUC", 2014),
                             ("Lo dolce", "Dan", "CUC", 2014),
                             ("Lodolce", "Dan", "CUC", 2015),
                             ("McCoy", "Tj", "MAR", 2013),
                             ("McCoy", "Tj", "MAR", 2014),
                             ("McCoy", "TJ", "MAR", 2015)],
                            columns=["lname", "fname", "team", "season"])
        expected = pd.DataFrame([("Jaquez", "Ty", "AUR", 2014),
                                 ("Jaquez", "Ty", "AUR", 2015),
                                 ("Jaquez", "Ty", "AUR", 2016),
                                 ("Jaquez", "Ty", "AUR", 2017),
                                 ("Ackerman", "Kamren", "BEN", 2015),
                                 ("Ackerman", "Kamren", "BEN", 2016),
                                 ("Ackerman", "Kamren", "BEN", 2017),
                                 ("Lo Dolce", "Dan", "CUC", 2014),
                                 ("Lo Dolce", "Dan", "CUC", 2014),
                                 ("Lo Dolce", "Dan", "CUC", 2015),
                                 ("McCoy", "TJ", "MAR", 2013),
                                 ("McCoy", "TJ", "MAR", 2014),
                                 ("McCoy", "TJ", "MAR", 2015)],
                                columns=["lname", "fname", "team", "season"])
        # make sure apply_corrections doesn't remove any columns
        data["pos"] = "INF"
        expected["pos"] = "INF"
        self.assertTrue(cf.apply_corrections(data, corrections).equals(expected))

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


class TestLeagueTotals(unittest.TestCase):

    def setUp(self):
        pass

    def test_select_bench_players(self):
        # print([tuple(x) for x in data.loc[:, "fname":"pa"].values])

        team = pd.DataFrame([('Kyle', 'Spooner', 'AUR', 2010, 'Fr', 'C', 1, 1),
                             ('Anthony', 'Amedei', 'AUR', 2010, 'Jr', 'IF', 43, 210),
                             ('Bobby', 'Wilson', 'AUR', 2010, 'So', 'IF', 43, 206),
                             ('Kirk', 'Williamson', 'AUR', 2010, 'Sr', 'C', 43, 198),
                             ('Joe', 'Singraber', 'AUR', 2010, 'Jr', 'OF', 43, 183),
                             ('Tony', 'Wellner', 'AUR', 2010, 'Sr', 'OF', 43, 202),
                             ('Josh', 'Davidson', 'AUR', 2010, 'Jr', 'OF', 40, 182),
                             ('Tim', 'Mackey', 'AUR', 2010, 'So', 'IF', 42, 183),
                             ('Matt', 'Anklam', 'AUR', 2010, 'Sr', 'DH', 41, 169),
                             ('Matt', 'Mulvaney', 'AUR', 2010, 'Sr', 'OF', 39, 119),
                             ('Steve', 'Brauer', 'AUR', 2010, 'Sr', 'IF', 22, 67),
                             ('Brad', 'Brandenburg', 'AUR', 2010, 'So', 'OF', 8, 18),
                             ('Tony', 'Gliffe', 'AUR', 2010, 'Fr', None, 4, 13),
                             ('Brennan', 'Moroni', 'AUR', 2010, 'Jr', 'C', 4, 13),
                             ('Mike', 'Foley', 'AUR', 2010, 'Fr', 'IF', 5, 4),
                             ('Chris', 'Galovic', 'AUR', 2010, 'So', 'OF', 3, 5),
                             ('Justin', 'Aloisio', 'AUR', 2010, 'Fr', 'OF', 1, 1),
                             ('Brian', 'Claesson', 'AUR', 2010, 'So', 'C', 1, 1),
                             ('Steven', 'Karasewski', 'AUR', 2010, 'Fr', 'IF', 4, 1),
                             ('Deric', 'Punke', 'AUR', 2010, 'Fr', 'C', 2, 2),
                             ('Jacob', 'Blackburn', 'AUR', 2010, 'Fr', 'IF', 1, 1),
                             ('Thomas', 'Ozlanski', 'AUR', 2010, 'Fr', 'P/IF', 7, 1)],
                            columns=["fname", "lname", "team", "season", "yr", "pos", "g", "pa"])

        expected = pd.DataFrame([('Steve', 'Brauer', 'AUR', 2010, 'Sr', 'IF', 22, 67),
                                 ('Brad', 'Brandenburg', 'AUR', 2010, 'So', 'OF', 8, 18),
                                 ('Tony', 'Gliffe', 'AUR', 2010, 'Fr', None, 4, 13),
                                 ('Brennan', 'Moroni', 'AUR', 2010, 'Jr', 'C', 4, 13),
                                 ('Chris', 'Galovic', 'AUR', 2010, 'So', 'OF', 3, 5),
                                 ('Mike', 'Foley', 'AUR', 2010, 'Fr', 'IF', 5, 4),
                                 ('Deric', 'Punke', 'AUR', 2010, 'Fr', 'C', 2, 2),
                                 ('Kyle', 'Spooner', 'AUR', 2010, 'Fr', 'C', 1, 1),
                                 ('Thomas', 'Ozlanski', 'AUR', 2010, 'Fr', 'P/IF', 7, 1),
                                 ('Steven', 'Karasewski', 'AUR', 2010, 'Fr', 'IF', 4, 1),
                                 ('Brian', 'Claesson', 'AUR', 2010, 'So', 'C', 1, 1),
                                 ('Jacob', 'Blackburn', 'AUR', 2010, 'Fr', 'IF', 1, 1),
                                 ('Justin', 'Aloisio', 'AUR', 2010, 'Fr', 'OF', 1, 1)],
                                 columns=["fname", "lname", "team", "season", "yr", "pos", "g", "pa"])

        temp = lt.select_bench_players(team)

        temp.sort_values(by=["pa", "lname"], ascending=False, inplace=True)
        temp.reset_index(drop=True, inplace=True)
        expected.sort_values(by=["pa", "lname"], ascending=False, inplace=True)
        expected.reset_index(drop=True, inplace=True)

        self.assertTrue(temp.equals(expected))

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()
