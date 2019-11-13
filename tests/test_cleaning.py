""" This module provides data cleaning unit tests """
# Standard library imports
import datetime
# Third party imports
import pandas as pd
import pytest
# Local imports
import naccbis.Cleaning.CleanFunctions as cf
from naccbis.Cleaning import GameLogETL as gl
import naccbis.scripts.GenerateIds as gi
from naccbis.Cleaning import LeagueOffenseETL as lo


class TestCleanFunctions():

    data = pd.DataFrame([
        ("Jaquez", "Steven", "AUR", 2014),
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
        ("McCoy", "TJ", "MAR", 2015)
    ], columns=["lname", "fname", "team", "season"])

    @pytest.mark.parametrize(
        'fname, lname, expected', [
            ("Curtis", "Engelbrecht", "engelcu01"),
            ("Garrett", "Balind", "balinga01"),
            ("Galen", "Balinski", "balinga01"),
            ("Patrick", "O'Malley", "omallpa01"),
        ]
    )
    def test_create_id(self, fname, lname, expected):
        assert cf.create_id(fname, lname) == expected

    @pytest.mark.parametrize(
        'id, n, expected', [
            ("engelcu01", 0, "engelcu01"),
            ("engelcu01", 1, "engelcu02"),
            ("engelcu01", 2, "engelcu03"),
        ]
    )
    def test_add_n(self, id, n, expected):
        assert cf.add_n(id, n) == expected

    def test_normalize_names(self):
        df1 = pd.DataFrame({"name": ["Jeffrey  Mayes", "D.J.  Dillon", "Quinlan Milne Rojek"],
                            "team": ["AUR", "BEN", "DOM"],
                            "season": [2017, 2017, 2016]}, columns=["name", "team", "season"])
        df2 = pd.DataFrame(df1)
        df2["fname"] = ["Jeffrey", "DJ", "Quinlan"]
        df2["lname"] = ["Mayes", "Dillon", "Milne Rojek"]
        assert cf.normalize_names(df1).equals(df2)

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

        corrections = pd.DataFrame([
            ("Steven", "Jaquez", "AUR", 2014, "Ty", "Jaquez", "C"),
            ("Steven", "Jaquez", "AUR", 2015, "Ty", "Jaquez", "C"),
            ("Steven", "Jaquez", "AUR", 2016, "Ty", "Jaquez", "C"),
            ("Dan", "Lo dolce", "CUC", 2014, "Dan", "Lo Dolce", "T"),
            ("Dan", "Lodolce", "CUC", 2015, "Dan", "Lo Dolce", "T"),
            ("Tj", "McCoy", "MAR", 2013, "TJ", "McCoy", "T"),
            ("Tj", "McCoy", "MAR", 2014, "TJ", "McCoy", "T"),
            ("Aj", "Alessi", "MAR", 2014, "AJ", "Alessi", "T")
        ], columns=["uc_fname", "uc_lname", "uc_team",
                    "uc_season", "c_fname", "c_lname", "type"])

        expected = pd.DataFrame([
            ("Jaquez", "Ty", "AUR", 2014),
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
            ("McCoy", "TJ", "MAR", 2015)
        ], columns=["lname", "fname", "team", "season"])
        # make sure apply_corrections doesn't remove any columns
        self.data["pos"] = "INF"
        expected["pos"] = "INF"
        assert cf.apply_corrections(self.data, corrections).equals(expected)

    def test_apply_corrections_no_change(self):
        corrections = pd.DataFrame([], columns=["uc_fname", "uc_lname", "uc_team",
                                                "uc_season", "c_fname", "c_lname", "type"])
        self.data["pos"] = "INF"
        expected = self.data
        assert cf.apply_corrections(self.data, corrections).equals(expected)

    @pytest.mark.parametrize(
        'raw, expected', [
            ("10.0", 10.0),
            ("10.1", 10 + (1/3)),
            ("10.2", 10 + (2/3)),
        ]
    )
    def test_convert_ip(self, raw, expected):
        assert cf.convert_ip(raw) == expected


class TestGenerateIds():

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

        raw = pd.DataFrame([
            ("Balind", "Garett", "CUC", 2011, "balinga01", "Garett Balind"),
            ("Balind", "Garett", "CUC", 2010, "balinga01", "Garett Balind"),
            ("Balinski", "Galen", "MARN", 2013, "balinga01", "Galen Balinski"),
            ("Schoemann", "Tyler", "WLC", 2018, "schoety01", "Tyler Schoemann"),
            ("Schoen", "Tyler", "WLC", 2010, "schoety01", "Tyler Schoen"),
            ("Schoen", "Tyler", "WLC", 2011, "schoety01", "Tyler Schoen"),
            ("Schoen", "Tyler", "WLC", 2012, "schoety01", "Tyler Schoen"),
            ("Schoen", "Tyler", "WLC", 2013, "schoety01", "Tyler Schoen")
        ], columns=["lname", "fname", "team", "season", "player_id", "full_name"])

        expected = pd.DataFrame([
            ("Balind", "Garett", "CUC", 2011, "balinga01", "Garett Balind"),
            ("Balind", "Garett", "CUC", 2010, "balinga01", "Garett Balind"),
            ("Balinski", "Galen", "MARN", 2013, "balinga02", "Galen Balinski"),
            ("Schoemann", "Tyler", "WLC", 2018, "schoety02", "Tyler Schoemann"),
            ("Schoen", "Tyler", "WLC", 2010, "schoety01", "Tyler Schoen"),
            ("Schoen", "Tyler", "WLC", 2011, "schoety01", "Tyler Schoen"),
            ("Schoen", "Tyler", "WLC", 2012, "schoety01", "Tyler Schoen"),
            ("Schoen", "Tyler", "WLC", 2013, "schoety01", "Tyler Schoen")
        ], columns=["lname", "fname", "team", "season", "player_id", "full_name"])

        assert gi.update_id_conflicts(raw).equals(expected)


class TestCleanGameLogs():

    @pytest.mark.parametrize(
        'score, expected', [
            ("L, 10-8", "L"),
            ("W, 17-6", "W"),
            ("W, 5-4", "W"),
            ("L, 5-4",  "L"),
        ]
    )
    def test_extract_result(self, score, expected):
        assert gl.extract_result(score) == expected

    @pytest.mark.parametrize(
        'score, expected', [
            ("L, 10-8", [8, 10]),
            ("W, 17-6", [17, 6]),
            ("W, 5-4", [5, 4]),
            ("L, 5-4", [4, 5]),
        ]
    )
    def test_extract_runs(self, score, expected):
        assert gl.extract_runs(score) == expected

    @pytest.mark.parametrize(
        'opponent, expected', [
            ("at Benedictine", "Benedictine"),
            ("vs. Benedictine", "Benedictine"),
            ("vs Benedictine", "Benedictine"),
            ("Benedictine", "Benedictine"),
            ("vs. St. Lawrence", "St. Lawrence"),
        ]
    )
    def test_extract_opponent(self, opponent, expected):
        assert gl.extract_opponent(opponent) == expected

    @pytest.mark.parametrize(
        'opponent, expected', [
            ("at Benedictine", False),
            ("vs. Benedictine", True),
            ("Benedictine", True),
        ]
    )
    def test_extract_home(self, opponent, expected):
        assert gl.extract_home(opponent) == expected

    @pytest.mark.parametrize(
        'opponent, season, expected', [
            ("Maranatha", 2013, True),
            ("Maranatha", 2014, False),
            ("Carthage", 2018, False),
            ("Marian", 2017, True),
        ]
    )
    def test_extract_conference(self, opponent, season, expected):
        teams = ["Aurora", "Benedictine", "Concordia Chicago", "Concordia Wisconsin", "Dominican",
                 "Edgewood", "Lakeland", "MSOE", "Marian", "Maranatha", "Rockford", "Wisconsin Lutheran"]
        assert gl.extract_conference(opponent, season, teams) == expected

    @pytest.mark.parametrize(
        'date_str, season, expected', [
            ("Mar 6", 2010, datetime.datetime(2010, 3, 6)),
            ("May 14", 2010, datetime.datetime(2010, 5, 14)),
            ("Feb 28", 2010, datetime.datetime(2010, 2, 28)),
            ("Apr 02", 2014, datetime.datetime(2014, 4, 2)),
            ("May 20", 2016, datetime.datetime(2016, 5, 20)),
            ("Apr 30", 2018, datetime.datetime(2018, 4, 30)),
        ]
    )
    def test_extract_date(self, date_str, season, expected):
        assert gl.extract_date(date_str, season) == expected


class TestLeagueTotals():

    def test_select_bench_players(self):
        # print([tuple(x) for x in data.loc[:, "fname":"pa"].values])

        team = pd.DataFrame([
            ('Kyle', 'Spooner', 'AUR', 2010, 'Fr', 'C', 1, 1),
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
            ('Thomas', 'Ozlanski', 'AUR', 2010, 'Fr', 'P/IF', 7, 1)
        ], columns=["fname", "lname", "team", "season", "yr", "pos", "g", "pa"])

        expected = pd.DataFrame([
            ('Steve', 'Brauer', 'AUR', 2010, 'Sr', 'IF', 22, 67),
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
            ('Justin', 'Aloisio', 'AUR', 2010, 'Fr', 'OF', 1, 1)
        ], columns=["fname", "lname", "team", "season", "yr", "pos", "g", "pa"])

        temp = lo.select_bench_players(team)

        temp.sort_values(by=["pa", "lname"], ascending=False, inplace=True)
        temp.reset_index(drop=True, inplace=True)
        expected.sort_values(by=["pa", "lname"], ascending=False, inplace=True)
        expected.reset_index(drop=True, inplace=True)

        assert temp.equals(expected)
