""" This script is used to clean team pitching data and load into database """
import logging
from pathlib import Path

import pandas as pd
from sqlalchemy.engine import Connection

from naccbis.common import metrics, utils
from naccbis.common.splits import Split

from . import CleanFunctions


class TeamPitchingETL:
    """ETL class for team pitching"""

    CSV_DIR = Path("csv/")

    def __init__(
        self,
        year: int,
        split: Split,
        load_db: bool,
        conn: Connection,
        inseason: bool = False,
    ) -> None:
        self.year = year
        self.split = split
        self.load_db = load_db
        self.conn = conn
        self.inseason = inseason
        self.data: pd.DataFrame

    def extract(self) -> None:
        table = f"raw_team_pitching_{self.split}"
        if self.inseason:
            table += "_inseason"
        logging.info("Reading data from %s", table)
        self.data = pd.read_sql_table(table, self.conn)
        logging.info("Read %s records from %s", len(self.data), table)
        if self.year:
            self.data = self.data[self.data["season"] == self.year]

    def transform(self) -> None:
        self.data["ip"] = self.data["ip"].apply(CleanFunctions.convert_ip)
        conference = self.split == Split.CONFERENCE
        self.data = metrics.basic_pitching_metrics(self.data, conference=conference)

    def load(self) -> None:
        table = f"team_pitching_{self.split}"
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
        logging.info("Year: %s Split: %s Load: %s", self.year, self.split, self.load_db)
        self.extract()
        self.transform()
        self.load()
