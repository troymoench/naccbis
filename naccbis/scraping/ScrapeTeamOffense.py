""" This module provides the TeamOffenseScraper class """
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


class TeamOffenseScraper(BaseScraper):

    """This scraper is responsible for scraping team offensive stats."""

    HITTING_COLS = ["name", "gp", "ab", "r", "h", "2b", "hr", "avg", "obp", "slg"]
    EXTENDED_HITTING_COLS = ["name", "gp", "hbp", "sf", "sh", "pa"]
    TABLES = {
        "overall": "raw_team_offense_overall",
        "conference": "raw_team_offense_conference",
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
        self._name = "Team Offense Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

    def run(self) -> None:
        """Run the scraper"""
        logging.info("%s", self._name)
        logging.info("Fetching teams")
        url = f"{self.BASE_URL}{self._year}/teams"
        soup = ScrapeFunctions.get_soup(url)
        logging.info("Looking for hitting tables")
        df = self._scrape(soup)
        logging.info("Cleaning scraped data")
        self._data = self._clean(df)
        self._runnable = False

    def _scrape(self, soup: BeautifulSoup) -> pd.DataFrame:
        """Scrape both the hitting table and extended hitting table and merge"""

        if self._split == Split.OVERALL:
            index = 0
        elif self._split == Split.CONFERENCE:
            index = 1

        # find index of hitting table
        table_num1 = ScrapeFunctions.find_table(soup, self.HITTING_COLS)[index]
        hitting = ScrapeFunctions.scrape_table(soup, table_num1 + 1, skip_rows=0)
        # find index of extended_hitting table
        table_num2 = ScrapeFunctions.find_table(soup, self.EXTENDED_HITTING_COLS)[index]
        extended_hitting = ScrapeFunctions.scrape_table(
            soup, table_num2 + 1, skip_rows=0
        )

        # may want to normalize the column names before merging, eg, lower(), gp to g
        return pd.merge(hitting, extended_hitting, on=["Rk", "Name", "gp"])

    def _clean(self, data: pd.DataFrame) -> pd.DataFrame:
        data.columns = data.columns.to_series().str.lower()
        unnecessary_cols = ["rk"]
        data.drop(columns=unnecessary_cols, inplace=True)
        rename_cols = {
            "no.": "no",
            "k": "so",
            "go/fo": "go_fo",
            "2b": "x2b",
            "3b": "x3b",
            "hdp": "gdp",
            "gp": "g",
        }
        data.rename(columns=rename_cols, inplace=True)

        int_cols = [
            "g",
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
            "pa",
        ]
        float_cols = ["avg", "obp", "slg", "go_fo"]
        final_col_names = [
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
            "sb",
            "cs",
            "avg",
            "obp",
            "slg",
            "hbp",
            "sf",
            "sh",
            "tb",
            "xbh",
            "gdp",
            "go",
            "fo",
            "go_fo",
        ]
        if self._inseason:
            final_col_names = [
                "name",
                "season",
                "date",
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
                "avg",
                "obp",
                "slg",
                "hbp",
                "sf",
                "sh",
                "tb",
                "xbh",
                "gdp",
                "go",
                "fo",
                "go_fo",
            ]

        data[int_cols] = data[int_cols].replace("-", "0")
        data[float_cols] = data[float_cols].replace("-", np.nan)

        data["season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["date"] = str(date.today())
        return data[final_col_names]
