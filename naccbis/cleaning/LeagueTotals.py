""" Extract, Transform, Load League Offense and Pitching data

This script is used to calculate league totals for offense and pitching
and load into database
"""
import logging
from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Connection

from naccbis.common import metrics, utils
from naccbis.common.splits import Split


class LeagueOffenseETL:
    """ETL class for league offense"""

    CSV_DIR = Path("csv/")

    def __init__(
        self, year: int, split: Split, load_db: bool, conn: Connection
    ) -> None:
        self.year = year
        self.split = split
        self.load_db = load_db
        self.conn = conn
        self.team_data: pd.DataFrame
        self.batters: pd.DataFrame

    def extract(self) -> None:
        self.team_data = pd.read_sql_table(f"team_offense_{self.split}", self.conn)
        if self.year:
            self.team_data = self.team_data[self.team_data["season"] == self.year]
        self.batters = pd.read_sql_table(f"batters_{self.split}", self.conn)
        if self.year:
            self.batters = self.batters[self.batters["season"] == self.year]

    def transform(self) -> None:
        cols = [
            "season",
            "g",
            "pa",
            "ab",
            "r",
            "h",
            "x2b",
            "x3b",
            "hr",
            "rbi",
            "bb",
            "so",
            "sb",
            "cs",
            "hbp",
            "sf",
            "sh",
            "tb",
            "xbh",
            "gdp",
            "go",
            "fo",
        ]

        totals = self.team_data[cols].groupby("season").sum()
        totals = metrics.basic_offensive_metrics(totals)

        totals["lg_r_pa"] = totals["r"] / totals["pa"]
        totals["bsr_bmult"] = metrics.bsr_bmult(totals)
        totals["bsr"] = metrics.bsr(totals, bmult=totals["bsr_bmult"])
        lw = totals.apply(metrics.linear_weights_incr, axis=1)
        totals = totals.join(lw)
        ww = metrics.woba_weights(totals, totals["obp"])
        totals = totals.join(ww)
        totals["woba"] = metrics.woba(totals, ww)
        totals["sbr"] = metrics.sbr(totals, lw)
        totals["lg_wsb"] = metrics.lg_wsb(totals, lw)
        totals["wsb"] = metrics.wsb(totals, totals["lg_wsb"])
        totals["wraa"] = metrics.wraa(totals, totals["woba"], totals["woba_scale"])
        totals["off"] = metrics.off(totals)
        totals["wrc"] = metrics.wrc(
            totals, totals["woba"], totals["woba_scale"], totals["lg_r_pa"]
        )
        totals["wrc_p"] = metrics.wrc_p(totals, totals["lg_r_pa"])
        totals["off_p"] = metrics.off_p(totals, totals["lg_r_pa"])

        replacement_totals = self.calc_replacement_level(totals)
        totals["rep_level"] = replacement_totals["off_pa"]
        totals["rar"] = metrics.rar(totals, totals["rep_level"])

        self.replacement_totals = replacement_totals
        self.totals = totals

    def load(self) -> None:
        repl_table_name = f"replacement_level_{self.split}"
        if self.load_db:
            logging.info("Loading data into database")
            utils.db_load_data(
                self.replacement_totals,
                repl_table_name,
                self.conn,
                if_exists="append",
                index=True,
            )
        else:
            logging.info("Dumping to csv")
            fname = self.CSV_DIR / f"{repl_table_name}.csv"
            self.replacement_totals.to_csv(fname, index=True)

        table_name = f"league_offense_{self.split}"
        if self.load_db:
            logging.info("Loading data into database")
            utils.db_load_data(
                self.totals, table_name, self.conn, if_exists="append", index=True
            )
        else:
            logging.info("Dumping to csv")
            fname = self.CSV_DIR / f"{table_name}.csv"
            self.totals.to_csv(fname, index=True)

    def run(self) -> None:
        logging.info("Running %s", type(self).__name__)
        logging.info("Year: %s Split: %s Load: %s", self.year, self.split, self.load_db)
        self.extract()
        self.transform()
        self.load()

    @staticmethod
    def select_bench_players(data: pd.DataFrame) -> pd.DataFrame:
        """Select bench players. Used for determining replacement level

        :param data: A DataFrame of a team's player stats
        :returns: A DataFrame of players that weren't in the top 9 in PA
        """
        data = data.sort_values(by=["pa"], ascending=False)
        return data[9:]

    def calc_replacement_level(self, totals: pd.DataFrame) -> pd.DataFrame:
        """Calculate Replacement Level metrics
        Replacement Level is defined as the average bench player

        :param totals: A DataFrame of league totals
        :returns: A DataFrame of replacement level totals
        """
        temp = self.batters.loc[:, "fname":"fo"]  # type: ignore
        bench = temp.groupby(["season", "team"]).apply(self.select_bench_players)
        bench = bench.reset_index(drop=True)

        bench_totals = bench.groupby("season").sum()
        bench_totals = metrics.basic_offensive_metrics(bench_totals)
        bench_totals = metrics.advanced_offensive_metrics(bench_totals, totals)

        bench_totals["off_pa"] = bench_totals["off"] / bench_totals["pa"]
        return bench_totals


class LeaguePitchingETL:
    """ETL class for league pitching"""

    CSV_DIR = Path("csv/")

    def __init__(
        self, year: int, split: Split, load_db: bool, conn: Connection
    ) -> None:
        self.year = year
        self.split = split
        self.load_db = load_db
        self.conn = conn
        self.team_data: pd.DataFrame

    def extract(self) -> None:
        self.team_data = pd.read_sql_table(f"team_pitching_{self.split}", self.conn)
        if self.year:
            self.team_data = self.team_data[self.team_data["season"] == self.year]

    def transform(self) -> None:
        if self.split == "overall":
            cols = [
                "season",
                "g",
                "w",
                "l",
                "sv",
                "cg",
                "sho",
                "ip",
                "h",
                "r",
                "er",
                "bb",
                "so",
                "x2b",
                "x3b",
                "hr",
                "ab",
                "wp",
                "hbp",
                "bk",
                "sf",
                "sh",
                "pa",
            ]
            totals = self.team_data[cols].groupby("season").sum()
            totals = metrics.basic_pitching_metrics(totals)
            totals["lg_r_pa"] = totals["r"] / totals["pa"]
            totals["bsr_bmult"] = metrics.bsr_pitch_bmult(totals)
            totals["bsr"] = metrics.bsr_pitch(totals, totals["bsr_bmult"])
            totals["bsr_9"] = metrics.bsr_9(totals)
            # ra/bf-
            # bsr/bf-
            totals["fip_constant"] = metrics.fip_constant(totals)
            totals["fip"] = metrics.fip(totals, totals["fip_constant"])
            totals["raa"] = metrics.raa(totals, totals["ra_9"])
            totals["bsraa"] = metrics.bsraa(totals, totals["bsr_9"])
            totals["fipraa"] = metrics.fipraa(totals, totals["fip"])
            totals["era_minus"] = metrics.era_minus(totals, totals["era"])
            totals["fip_minus"] = metrics.fip_minus(totals, totals["fip"])
            totals["bsr_minus"] = metrics.bsr_minus(totals, totals["bsr_9"])

        if self.split == Split.CONFERENCE:
            cols = ["season", "g", "ip", "h", "r", "er", "bb", "so", "hr"]
            totals = self.team_data[cols].groupby("season").sum()
            conference = self.split == Split.CONFERENCE
            totals = metrics.basic_pitching_metrics(totals, conference)
            # totals["fip_constant"] = metrics.fip_constant(totals)  # noqa: E800
            # totals["fip"] = metrics.fip(totals, totals["fip_constant"])  # noqa: E800
            totals["raa"] = metrics.raa(totals, totals["ra_9"])
            # totals["fipraa"] = metrics.fipraa(totals, totals["fip"])  # noqa: E800
            totals["era_minus"] = metrics.era_minus(totals, totals["era"])
            # totals["fip_minus"] = metrics.fip_minus(totals, totals["fip"])  # noqa: E800

        self.totals = totals

    def load(self) -> None:
        table_name = f"league_pitching_{self.split}"
        if self.load_db:
            logging.info("Loading data into database")
            utils.db_load_data(
                self.totals, table_name, self.conn, if_exists="append", index=True
            )
        else:
            logging.info("Dumping to csv")
            self.totals.to_csv(self.CSV_DIR / f"{table_name}.csv", index=True)

    def run(self) -> None:
        logging.info("Running %s", type(self).__name__)
        logging.info("Year: %s Split: %s Load: %s", self.year, self.split, self.load_db)
        self.extract()
        self.transform()
        self.load()
