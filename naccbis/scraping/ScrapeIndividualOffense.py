""" This module provides the IndividualOffenseScraper class """
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


class IndividualOffenseScraper(BaseScraper):

    """This scraper is responsible for scraping individual offensive stats."""

    HITTING_COLS = [
        "no.",
        "name",
        "yr",
        "pos",
        "g",
        "ab",
        "r",
        "h",
        "2b",
        "hr",
        "avg",
        "obp",
        "slg",
    ]
    EXTENDED_HITTING_COLS = ["no.", "name", "yr", "pos", "g", "hbp", "sf", "pa"]
    TABLES = {"overall": "raw_batters_overall", "conference": "raw_batters_conference"}

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
        self._name = "Individual Offense Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

    def run(self) -> None:
        """Run the scraper"""
        logging.info("%s", self._name)

        team_urls = ScrapeFunctions.get_team_list(
            self.BASE_URL, self._year, self.TEAM_IDS
        )
        logging.info("Found %d teams to scrape", len(team_urls))

        for team in team_urls:
            logging.info("Fetching %s", team.team)

            url = f"{self.BASE_URL}{self._year}/{team.url}"
            teamSoup = ScrapeFunctions.get_soup(url)
            if ScrapeFunctions.skip_team(teamSoup):
                continue
            logging.info("Looking for hitting tables")
            df = self._scrape(teamSoup)
            logging.info("Cleaning scraped data")
            df = self._clean(df, team.id)
            self._data = pd.concat([self._data, df], ignore_index=True)

        self._runnable = False

    def _scrape(self, team_soup: BeautifulSoup) -> pd.DataFrame:
        """Scrape both the hitting table and extended hitting table and merge"""

        # Note: Finding the links for overall vs conference probably isn't necessary
        # because the html doesn't change based on the url choice
        # Instead, find the indices of the tables on the same page

        if self._split == Split.OVERALL:
            index = 0
        elif self._split == Split.CONFERENCE:
            index = 1

        # find index of hitting table
        tableNum1 = ScrapeFunctions.find_table(team_soup, self.HITTING_COLS)[index]
        hitting = ScrapeFunctions.scrape_table(team_soup, tableNum1 + 1, skip_rows=2)
        # find index of extended_hitting table
        tableNum2 = ScrapeFunctions.find_table(team_soup, self.EXTENDED_HITTING_COLS)[
            index
        ]
        extendedHitting = ScrapeFunctions.scrape_table(
            team_soup, tableNum2 + 1, skip_rows=2
        )

        return pd.merge(hitting, extendedHitting, on=["No.", "Name", "Yr", "Pos", "g"])

    def _clean(self, data: pd.DataFrame, team_id: str) -> pd.DataFrame:
        # add TeamId, Season
        # replace dashes and strip dots from Yr (Fr. -> Fr)
        # column names cannot start with a digit in PostgreSQL!!!!!
        # disallowed column names: no., 2b, 3b, go/fo
        data = data.copy()
        data.columns = data.columns.to_series().str.lower()
        renameCols = {
            "no.": "no",
            "k": "so",
            "go/fo": "go_fo",
            "2b": "x2b",
            "3b": "x3b",
            "hdp": "gdp",
        }
        data.rename(columns=renameCols, inplace=True)

        intCols = [
            "no",
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
        floatCols = ["avg", "obp", "slg", "go_fo"]
        finalColNames = [
            "no",
            "name",
            "team",
            "season",
            "yr",
            "pos",
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
            finalColNames = [
                "no",
                "name",
                "team",
                "season",
                "date",
                "yr",
                "pos",
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

        data[intCols] = data[intCols].replace("-", "0")
        data[floatCols] = data[floatCols].replace("-", np.nan)

        data["team"] = team_id
        data["season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["date"] = str(date.today())
        data["yr"] = data["yr"].str.rstrip(".")
        data["pos"] = data["pos"].replace("", np.nan)
        return data[finalColNames]
