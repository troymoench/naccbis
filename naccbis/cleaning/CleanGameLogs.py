""" This script is used to clean game log data and load into the database """
# Standard library imports
import datetime
import logging
from pathlib import Path
import re
from typing import List

# Third party imports
import pandas as pd

# Local imports
from naccbis.common import utils


class GameLogETL:
    """ETL class for game logs"""

    CONFERENCE_TEAMS = [
        "Aurora",
        "Benedictine",
        "Concordia Chicago",
        "Concordia Wisconsin",
        "Dominican",
        "Edgewood",
        "Lakeland",
        "MSOE",
        "Marian",
        "Maranatha",
        "Rockford",
        "Wisconsin Lutheran",
    ]
    CSV_DIR = Path("csv/")

    def __init__(
        self, year: int, load_db: bool, conn: object, inseason: bool = False
    ) -> None:
        self.year = year
        self.load_db = load_db
        self.conn = conn
        self.inseason = inseason

    def extract(self) -> None:
        table = "raw_game_log_hitting"
        if self.inseason:
            table += "_inseason"

        logging.info("Reading data from %s", table)
        self.data = pd.read_sql_table(table, self.conn)
        logging.info("Read %s records from %s", len(self.data), table)
        if self.year:
            self.data = self.data[self.data["season"] == self.year]

    def transform(self) -> None:
        columns = ["game_num", "date", "season", "name", "opponent", "score"]
        if self.inseason:
            columns = ["scrape_date"] + columns
        self.data = self.data[columns]
        self.data["result"] = self.data["score"].apply(self.extract_result)
        # runs scored, runs against

        self.data["inter"] = self.data["score"].apply(
            self.extract_runs
        )  # intermediate column
        self.data["rs"] = [x[0] for x in self.data["inter"]]
        self.data["ra"] = [x[1] for x in self.data["inter"]]

        self.data.drop(columns=["inter"], inplace=True)

        # home/away

        self.data["home"] = self.data["opponent"].apply(self.extract_home)

        # conference/non-conference

        self.data["conference"] = list(
            map(
                lambda x, y: self.extract_conference(x, y, self.CONFERENCE_TEAMS),
                self.data["opponent"],
                self.data["season"],
            )
        )
        self.data["opponent"] = self.data["opponent"].apply(self.extract_opponent)
        self.data.rename(columns={"name": "team"}, inplace=True)
        self.data.drop(columns=["score"], inplace=True)

        self.data["date"] = list(
            map(
                lambda x, y: self.extract_date(x, y),
                self.data["date"],
                self.data["season"],
            )
        )

    def load(self) -> None:
        table = "game_log"
        if self.inseason:
            table += "_inseason"

        if self.load_db:
            logging.info("Loading data into database")
            utils.db_load_data(
                self.data, table, self.conn, if_exists="append", index=False
            )
        else:
            filename = f"{table}.csv"
            logging.info("Dumping to csv")
            self.data.to_csv(self.CSV_DIR / filename, index=False)

    def run(self) -> None:
        logging.info("Running %s", type(self).__name__)
        logging.info("Year: %s Load: %s", self.year, self.load_db)
        self.extract()
        self.transform()
        self.load()

    @staticmethod
    def extract_runs(score: str) -> List[int]:
        """Extract the runs scored and runs against from the score

        :param score: The score
        :returns: A list where first element is runs scored and
                  second element is runs against. Format: [rs, ra]
        """
        split_score = score.split(",")
        result = split_score[0].strip()
        temp = split_score[1].split("-")
        run_list = [int(x.strip()) for x in temp]

        if result == "W":
            run_list.sort(reverse=True)
        else:
            run_list.sort()
        return run_list

    @staticmethod
    def extract_result(score: str) -> str:
        """Extract the result (W/L) from the score

        :param score: The score
        :returns: The result (W/L)
        """
        return score.split(",")[0].strip()

    @staticmethod
    def extract_home(opponent: str) -> bool:
        """Extract home/away from the opponent

        :param opponent: The opponent
        :returns: True for home, False for away
        """
        opponent = opponent.strip()
        if re.match(r"\b[Aa][Tt]\b", opponent):
            home = False
        else:
            home = True
        return home

    @staticmethod
    def extract_opponent(opponent: str) -> str:
        """Extract the team name from the raw opponent

        :param opponent: The opponent
        :returns: The team name of the opponent
        """
        opponent = opponent.strip()
        return re.sub(r"\b[Aa][Tt]\b|\b[Vv][Ss][.]*", "", opponent).strip()

    @staticmethod
    def extract_conference(opponent: str, season: int, teams: List[str]) -> bool:
        """Determine if the opponent is conference or non-conference"""
        # TODO: Get list of conference teams from database

        # Maranatha is non-conference after 2013
        if opponent == "Maranatha" and season > 2013:
            return False

        matched = False
        for team in teams:
            if re.search(team, opponent):
                matched = True
        return matched

    @staticmethod
    def extract_date(date_str: str, season: str) -> datetime.datetime:
        date_str = f"{date_str} {season}"
        return datetime.datetime.strptime(date_str, "%b %d %Y")
