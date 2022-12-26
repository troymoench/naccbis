""" This module provides the TeamFieldingScraper class """
import logging
from datetime import date
from typing import Optional

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy.engine import Connection

from naccbis.common import utils
from naccbis.common.splits import Split

from . import ScrapeFunctions
from .ScrapeBase import BaseScraper


class TeamFieldingScraper(BaseScraper):

    """This scraper is responsible for scraping team fielding stats."""

    FIELDING_COLS = ["name", "gp", "tc", "po", "a", "e", "fpct", "dp"]
    TABLES = {
        "overall": "raw_team_fielding_overall",
        "conference": "raw_team_fielding_conference",
    }

    def __init__(
        self,
        year: str,
        split: Split,
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
        super().__init__(year, split, output, inseason, verbose, conn)
        self._name = "Team Fielding Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

    def run(self) -> None:
        """Run the scraper"""
        logging.info("%s", self._name)
        logging.info("Fetching teams")
        url = f"{self.BASE_URL}{self._year}/teams"
        soup = ScrapeFunctions.get_soup(url)
        logging.info("Looking for fielding table")
        df = self._scrape(soup)
        logging.info("Cleaning scraped data")
        self._data = self._clean(df)

        self._runnable = False

    def _scrape(self, soup: BeautifulSoup) -> pd.DataFrame:
        if self._split == Split.OVERALL:
            index = 0
        elif self._split == Split.CONFERENCE:
            index = 1

        # find index of fielding table
        table_num1 = ScrapeFunctions.find_table(soup, self.FIELDING_COLS)[index]
        fielding = ScrapeFunctions.scrape_table(soup, table_num1 + 1, skip_rows=0)

        # may want to normalize the column names eg, lower(), gp to g
        return fielding

    def _clean(self, data: pd.DataFrame) -> pd.DataFrame:
        unnecessary_cols = ["Rk"]
        rename_cols = {"gp": "g", "rcs": "cs", "rcs%": "cspct"}
        int_cols = ["g", "tc", "po", "a", "e", "dp", "sba", "cs", "pb", "ci"]
        float_cols = ["fpct", "cspct"]
        final_col_names = [
            "Name",
            "Season",
            "g",
            "tc",
            "po",
            "a",
            "e",
            "fpct",
            "dp",
            "sba",
            "cs",
            "cspct",
            "pb",
            "ci",
        ]
        if self._inseason:
            final_col_names = [
                "Name",
                "Season",
                "Date",
                "g",
                "tc",
                "po",
                "a",
                "e",
                "fpct",
                "dp",
                "sba",
                "cs",
                "cspct",
                "pb",
                "ci",
            ]

        data.drop(columns=unnecessary_cols, inplace=True)
        data.rename(columns=rename_cols, inplace=True)

        data[int_cols] = data[int_cols].replace("-", "0")
        data[float_cols] = data[float_cols].replace("-", np.nan)
        data[float_cols] = data[float_cols].replace("INF", np.nan)

        data["Season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["Date"] = str(date.today())

        data = data[final_col_names]
        data.columns = data.columns.to_series().str.lower()
        return data
