import logging
from datetime import date
from typing import Optional
from urllib.parse import urljoin

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy.engine import Connection

from naccbis.common import utils
from naccbis.common.splits import GameLogSplit

from . import ScrapeFunctions
from .ScrapeBase import BaseScraper


class GameLogScraper(BaseScraper):

    """This scraper is responsible for scraping game log stats."""

    HITTING_COLS = [
        "date",
        "opponent",
        "score",
        "ab",
        "r",
        "h",
        "2b",
        "3b",
        "hr",
        "bb",
        "k",
    ]
    EXTENDED_HITTING_COLS = ["date", "opponent", "score", "hbp", "sf", "sh", "tb", "pa"]
    PITCHING_COLS = ["date", "opponent", "score", "w", "l", "ip", "h", "r", "er", "era"]
    FIELDING_COLS = ["date", "opponent", "score", "tc", "po", "a", "e", "fpct"]
    TABLES = {
        "hitting": "raw_game_log_hitting",
        "pitching": "raw_game_log_pitching",
        "fielding": "raw_game_log_fielding",
    }

    def __init__(
        self,
        year: str,
        split: GameLogSplit,
        output: str,
        inseason: bool = False,
        verbose: bool = False,
        conn: Optional[Connection] = None,
    ) -> None:
        """Class constructor
        :param year: The school year. A string.
        :param split: hitting, pitching, or fielding stats. A string.
        :param output: Output format. Currently csv and sql.
        :param inseason: Is this scraping taking place in season?
        :param verbose: Print extra information to standard out?
        """
        super().__init__(year, split, output, inseason, verbose, conn)
        self._name = "Game Log Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

    def run(self) -> None:
        """Run the scraper"""
        logging.info("%s", self._name)

        team_urls = ScrapeFunctions.get_team_list(
            self.BASE_URL, self._year, self.TEAM_IDS
        )
        logging.info("Found %d teams to scrape", len(team_urls))

        # iterate over the teams
        for team in team_urls:
            logging.info("Fetching %s", team.team)

            url = f"{self.BASE_URL}{self._year}/{team.url}"
            team_soup = ScrapeFunctions.get_soup(url)
            logging.info("Looking for game log table")
            df = self._scrape(team_soup)
            logging.info("Cleaning scraped data")
            df = self._clean(df, team.team)

            self._data = pd.concat([self._data, df], ignore_index=True)
        self._runnable = False

    def _scrape(self, team_soup: BeautifulSoup) -> pd.DataFrame:
        """Scrape game logs for hitting, pitching, fielding"""

        tags = team_soup.find_all("a", string="Game Log")
        if len(tags) != 1:
            logging.error("Can't find Game Log")
            raise RuntimeError("Can't find Game Log")
        url = tags[0].get("href")
        url = urljoin(self.BASE_URL, url)

        game_soup = ScrapeFunctions.get_soup(url)

        if self._split == GameLogSplit.HITTING:
            table_num1 = ScrapeFunctions.find_table(game_soup, self.HITTING_COLS)[0]
            hitting = ScrapeFunctions.scrape_table(
                game_soup, table_num1 + 1, first_row=2, skip_rows=0
            )

            table_num2 = ScrapeFunctions.find_table(
                game_soup, self.EXTENDED_HITTING_COLS
            )[0]
            extended_hitting = ScrapeFunctions.scrape_table(
                game_soup, table_num2 + 1, first_row=2, skip_rows=0
            )

            # may want to normalize the column names before merging, eg, lower()
            return pd.merge(hitting, extended_hitting, on=["Date", "Opponent", "Score"])

        elif self._split == GameLogSplit.PITCHING:
            table_num1 = ScrapeFunctions.find_table(game_soup, self.PITCHING_COLS)[0]
            pitching = ScrapeFunctions.scrape_table(
                game_soup, table_num1 + 1, first_row=2, skip_rows=0
            )

            return pitching
        elif self._split == GameLogSplit.FIELDING:
            table_num1 = ScrapeFunctions.find_table(game_soup, self.FIELDING_COLS)[0]
            fielding = ScrapeFunctions.scrape_table(
                game_soup, table_num1 + 1, first_row=2, skip_rows=0
            )

            return fielding

    def _clean(self, data: pd.DataFrame, team: str) -> pd.DataFrame:
        if self._split == GameLogSplit.HITTING:
            int_cols = [
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
            float_cols = ["go_fo"]
            rename_cols = {
                "2b": "x2b",
                "3b": "x3b",
                "k": "so",
                "hdp": "gdp",
                "go/fo": "go_fo",
            }

        elif self._split == GameLogSplit.PITCHING:
            int_cols = ["w", "l", "sv", "h", "r", "er", "bb", "so", "hr"]
            float_cols = ["era"]
            rename_cols = {"k": "so"}

        elif self._split == GameLogSplit.FIELDING:
            int_cols = ["tc", "po", "a", "e", "dp", "sba", "cs", "pb", "ci"]
            float_cols = ["fpct", "cspct"]
            rename_cols = {"rcs": "cs", "rcs%": "cspct"}

        data.rename(columns=rename_cols, inplace=True)

        data[int_cols] = data[int_cols].replace("-", "0")
        data[float_cols] = data[float_cols].replace("-", np.nan)
        data[float_cols] = data[float_cols].replace("INF", np.nan)

        # replace tabs
        data["Opponent"] = [x.replace("\t", "") for x in data["Opponent"]]
        # strip excessive whitespace
        data["Opponent"] = [" ".join(x.split()) for x in data["Opponent"]]

        # replace strange # in Date column (Maranatha 2012)
        data["Date"] = [x.replace("#", "").strip() for x in data["Date"]]

        data["Name"] = team
        data["Season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["scrape_date"] = str(date.today())

        # filter out cancelled games that don't have a result
        data = data[data["Score"] != ""]
        data["game_num"] = list(range(1, len(data) + 1))
        data["game_num"] = data["game_num"].apply(str)

        final_col_names = data.axes[1].tolist()
        final_col_names.remove("Season")
        final_col_names.remove("Name")
        if self._inseason:
            final_col_names.remove("scrape_date")

        final_col_names.insert(1, "Season")
        final_col_names.insert(2, "Name")
        if self._inseason:
            final_col_names.insert(0, "scrape_date")

        final_col_names.remove("game_num")
        final_col_names.insert(0, "game_num")
        data = data[final_col_names]
        data.columns = data.columns.to_series().str.lower()
        return data
