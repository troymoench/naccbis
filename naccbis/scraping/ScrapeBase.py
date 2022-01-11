""" This module provides the BaseScraper class """
# Standard library imports
from abc import ABC, abstractmethod
from datetime import date
import logging
from pathlib import Path
from typing import Dict, Union, Optional

# Third party imports
import pandas as pd
from sqlalchemy.engine import Connection

# Local imports
from naccbis.common import utils
from naccbis.common.splits import Split, GameLogSplit


class BaseScraper(ABC):

    """This is the abstract base class for the scrapers.

    It provides only the shared functionality between all scrapers.
    Don't directly create an instance of the base class!

    General procedure that each scraper follows:

    1. Scrape the data from the web
    2. Clean the data
    3. Export the data

    """

    BASE_URL = "https://naccsports.org/sports/bsb/"
    TEAM_IDS = {
        "Aurora": "AUR",
        "Benedictine": "BEN",
        "Concordia Chicago": "CUC",
        "Concordia Wisconsin": "CUW",
        "Dominican": "DOM",
        "Edgewood": "EDG",
        "Illinois Tech": "ILLT",
        "Lakeland": "LAK",
        "MSOE": "MSOE",
        "Marian": "MAR",
        "Maranatha": "MARN",
        "Rockford": "ROCK",
        "Wisconsin Lutheran": "WLC",
    }
    TABLES: Dict[str, str] = {}
    VALID_OUTPUT = ["csv", "sql"]

    def __init__(
        self,
        year: str,
        split: Union[Split, GameLogSplit],
        output: str,
        inseason: bool = False,
        verbose: bool = False,
        conn: Optional[Connection] = None,
    ) -> None:
        """Class constructor
        :param year: The school year. A string.
        :param split: overall or conference stats. A string.
        :param output: Output format. Currently csv and sql.
        :param inseason: Is this scraping taking place in season?
        :param verbose: Print extra information to standard out?
        """
        self._name = "Base Scraper"
        self._year = year
        self._split = split
        if output not in self.VALID_OUTPUT:  # pragma: no cover
            raise ValueError(f"Invalid output: {output}")
        self._output = output
        self._inseason = inseason
        self._verbose = verbose
        self._data = pd.DataFrame()
        self._runnable = True
        self._conn = conn
        self._csv_path = Path("csv/")

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError

    def info(self) -> None:
        """Print the scraper information to standard out
        :returns: None
        """
        print("\n--------------------------")
        print(self._name)
        print("Year:", self._year)
        print("Split:", self._split)
        if self._verbose:  # pragma: no cover
            print("In-Season:", self._inseason)
            print("Output format:", self._output)
        print("--------------------------")

    def export(self) -> None:
        """Export scraped and cleaned data to csv or database.
        If exporting to database, the table must already exist
        :returns: None
        """
        logging.info("Exporting data from %s", self._name)
        if self._runnable:  # pragma: no cover
            raise ValueError(
                "Cannot export. Scraper has not been run yet. Use run() to do so."
            )
        tableName = self.TABLES[str(self._split)]
        if self._output == "csv":
            self._export_csv(tableName)
        elif self._output == "sql":
            self._export_db(tableName)

    def _export_csv(self, table_name: str) -> None:
        """Helper method to export data to a csv file"""
        if self._inseason:
            filename = f"{table_name}{str(date.today())}.csv"
        else:
            filename = f"{table_name}{utils.year_to_season(self._year)}.csv"
        try:
            self._data.to_csv(self._csv_path / filename, index=False)
        except Exception as e:
            logging.error("Unable to export to CSV: %s", e)
        else:
            logging.info("Successfully exported to CSV file")

    def _export_db(self, table_name: str) -> None:
        """Helper method to export data to a database"""
        if not self._conn:
            raise RuntimeError("Not connected to database. Cannot export data!")

        if self._inseason:
            table_name += "_inseason"

        utils.db_load_data(
            self._data, table_name, self._conn, if_exists="append", index=False
        )

    def get_data(self) -> pd.DataFrame:  # pragma: no cover
        return self._data
