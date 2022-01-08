""" This script is used to clean team offense data and load into database """
# Standard library imports
import logging
from pathlib import Path

# Third party imports
import pandas as pd

# Local imports
from naccbis.common import utils, metrics
from naccbis.common.splits import Split


class TeamOffenseETL:
    """ETL class for team offense"""

    CSV_DIR = Path("csv/")

    def __init__(
        self,
        year: int,
        split: Split,
        load_db: bool,
        conn: object,
        inseason: bool = False,
    ) -> None:
        self.year = year
        self.split = split
        self.load_db = load_db
        self.conn = conn
        self.inseason = inseason
        self.data: pd.DataFrame

    def extract(self) -> None:
        table = f"raw_team_offense_{self.split}"
        if self.inseason:
            table += "_inseason"
        logging.info("Reading data from %s", table)
        self.data = pd.read_sql_table(table, self.conn)
        logging.info("Read %s records from %s", len(self.data), table)
        if self.year:
            self.data = self.data[self.data["season"] == self.year]

    def transform(self) -> None:
        self.data = metrics.basic_offensive_metrics(self.data)
        columns = [
            "name",
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
            "hbp",
            "tb",
            "xbh",
            "sf",
            "sh",
            "gdp",
            "sb",
            "cs",
            "go",
            "fo",
            "go_fo",
            "hbp_p",
            "bb_p",
            "so_p",
            "iso",
            "babip",
            "avg",
            "obp",
            "slg",
            "ops",
            "sar",
        ]
        if self.inseason:
            columns.insert(2, "date")
        self.data = self.data[columns]

    def load(self) -> None:
        table = f"team_offense_{self.split}"
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
