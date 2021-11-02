""" This module provides the IndividualPitchingScraper class """
# Standard library imports
from datetime import date
import logging
from typing import Optional
from urllib.parse import urljoin

# Third party imports
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from sqlalchemy.engine import Connection

# Local imports
from . import ScrapeFunctions
from .ScrapeBase import BaseScraper
from naccbis.common import utils
from naccbis.common.splits import Split


class IndividualPitchingScraper(BaseScraper):

    """This scraper is responsible for scraping individual pitching stats."""

    PITCHING_COLS = [
        "no.",
        "name",
        "yr",
        "pos",
        "app",
        "gs",
        "w",
        "l",
        "ip",
        "h",
        "r",
        "er",
        "era",
    ]
    COACHES_VIEW_COLS = [
        "no.",
        "player",
        "era",
        "w",
        "l",
        "app",
        "gs",
        "ip",
        "h",
        "r",
        "er",
        "2b",
        "3b",
        "hr",
        "ab",
    ]
    TABLES = {
        "overall": "raw_pitchers_overall",
        "conference": "raw_pitchers_conference",
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
        :param split: overall or conference stats.
        :param output: Output format. Currently csv and sql.
        :param inseason: Is this scraping taking place in season?
        :param verbose: Print extra information to standard out?
        """
        super().__init__(year, split, output, inseason, verbose, conn)
        self._name = "Individual Pitching Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

    def run(self) -> None:
        """Run the scraper"""
        logging.info("%s", self._name)

        teamList = ScrapeFunctions.get_team_list(
            self.BASE_URL, self._year, self.TEAM_IDS
        )
        logging.info("Found %d teams to scrape", len(teamList))

        for team in teamList:
            logging.info("Fetching %s", team["team"])

            url = "{}{}/{}".format(self.BASE_URL, self._year, team["url"])
            teamSoup = ScrapeFunctions.get_soup(url)
            if ScrapeFunctions.skip_team(teamSoup):
                continue
            logging.info("Looking for pitching tables")
            df = self._scrape(teamSoup)
            logging.info("Cleaning scraped data")
            df = self._clean(df, team["id"])

            self._data = pd.concat([self._data, df], ignore_index=True)
        self._runnable = False

    def _scrape_overall(self, team_soup: BeautifulSoup) -> pd.DataFrame:
        index = 0
        # find index of pitching table
        tableNum1 = ScrapeFunctions.find_table(team_soup, self.PITCHING_COLS)[index]
        pitching = ScrapeFunctions.scrape_table(team_soup, tableNum1 + 1, skip_rows=2)

        tags = team_soup.find_all("a", string="Coach's View")
        if len(tags) != 1:
            logging.error("Can't find Coach's View")
            raise RuntimeError("Can't find Coach's View")

        url = tags[0].get("href")
        url = urljoin(self.BASE_URL, url)
        coach_soup = ScrapeFunctions.get_soup(url)
        tableNum2 = ScrapeFunctions.find_table(coach_soup, self.COACHES_VIEW_COLS)[0]
        coach_view = ScrapeFunctions.scrape_table(
            coach_soup, tableNum2 + 1, first_row=3, skip_rows=3
        )

        coach_view["Player"] = coach_view["Player"].str.rstrip(".")
        pitching["Name"] = [x.replace("  ", " ") for x in pitching["Name"]]
        coach_view = coach_view.rename(columns={"Player": "Name"})
        return pd.merge(coach_view, pitching, on=["No.", "Name"])

    def _scrape_conference(self, team_soup: BeautifulSoup) -> pd.DataFrame:
        index = 1
        # find index of pitching table
        tableNum1 = ScrapeFunctions.find_table(team_soup, self.PITCHING_COLS)[index]
        conference = ScrapeFunctions.scrape_table(team_soup, tableNum1 + 1, skip_rows=2)

        # may want to normalize the column names eg, lower(), gp to g
        return conference

    def _scrape(self, team_soup: BeautifulSoup) -> pd.DataFrame:
        # more stats are available on coach's view
        # but coach's view doesn't provide conference stats

        if self._split == Split.OVERALL:
            return self._scrape_overall(team_soup)
        elif self._split == Split.CONFERENCE:
            return self._scrape_conference(team_soup)

    def _clean_overall(self, data: pd.DataFrame, team_id: str) -> pd.DataFrame:
        unnecessaryCols = [
            "app",
            "gs",
            "w",
            "l",
            "sv",
            "cg",
            "ip",
            "h",
            "r",
            "er",
            "bb",
            "k",
            "hr",
            "era",
        ]
        data.drop(columns=unnecessaryCols, inplace=True)
        data.columns = data.columns.to_series().str.lower()
        renameCols = {
            "no.": "no",
            "app": "g",
            "k": "so",
            "k/9": "so_9",
            "2b": "x2b",
            "3b": "x3b",
            "sfa": "sf",
            "sha": "sh",
            "b/avg": "avg",
        }
        data.rename(columns=renameCols, inplace=True)

        intCols = [
            "no",
            "yr",
            "g",
            "gs",
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
        ]
        floatCols = ["era", "avg", "so_9"]
        finalColNames = [
            "no",
            "name",
            "team",
            "season",
            "yr",
            "pos",
            "g",
            "gs",
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
            "era",
            "x2b",
            "x3b",
            "hr",
            "ab",
            "avg",
            "wp",
            "hbp",
            "bk",
            "sf",
            "sh",
            "so_9",
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
                "gs",
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
                "era",
                "x2b",
                "x3b",
                "hr",
                "ab",
                "avg",
                "wp",
                "hbp",
                "bk",
                "sf",
                "sh",
                "so_9",
            ]

        data[intCols] = data[intCols].replace("-", "0")
        data[floatCols] = data[floatCols].replace("-", "0.0")
        data[floatCols] = data[floatCols].replace("INF", np.nan)

        data["team"] = team_id
        data["season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["date"] = str(date.today())
        data["yr"] = data["yr"].str.rstrip(".")
        data["pos"] = data["pos"].replace("", np.nan)
        return data[finalColNames]

    def _clean_conference(self, data: pd.DataFrame, team_id: str) -> pd.DataFrame:
        data.columns = data.columns.to_series().str.lower()
        renameCols = {
            "no.": "no",
            "app": "g",
            "k": "so",
            "k/9": "so_9",
            "2b": "x2b",
            "3b": "x3b",
            "sfa": "sf",
            "sha": "sh",
            "b/avg": "avg",
        }
        data.rename(columns=renameCols, inplace=True)
        intCols = [
            "no",
            "g",
            "gs",
            "w",
            "l",
            "sv",
            "cg",
            "h",
            "r",
            "er",
            "bb",
            "so",
            "hr",
        ]
        floatCols = ["so_9", "era"]
        finalColNames = [
            "no",
            "name",
            "team",
            "season",
            "yr",
            "pos",
            "g",
            "gs",
            "w",
            "l",
            "sv",
            "cg",
            "ip",
            "h",
            "r",
            "er",
            "bb",
            "so",
            "so_9",
            "hr",
            "era",
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
                "gs",
                "w",
                "l",
                "sv",
                "cg",
                "ip",
                "h",
                "r",
                "er",
                "bb",
                "so",
                "so_9",
                "hr",
                "era",
            ]
        data.rename(columns=renameCols, inplace=True)

        data[intCols] = data[intCols].replace("-", "0")
        data[floatCols] = data[floatCols].replace("-", np.nan)
        data[floatCols] = data[floatCols].replace("INF", np.nan)

        data["team"] = team_id
        data["season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["date"] = str(date.today())
        data["yr"] = data["yr"].str.rstrip(".")
        data["pos"] = data["pos"].replace("", np.nan)
        return data[finalColNames]

    def _clean(self, data: pd.DataFrame, team_id: str) -> pd.DataFrame:
        data = data.copy()
        if self._split == Split.OVERALL:
            return self._clean_overall(data, team_id)
        elif self._split == Split.CONFERENCE:
            return self._clean_conference(data, team_id)
