""" This module provides the TeamPitchingScraper class """
# Standard library imports
from datetime import date
import logging
from urllib.parse import urljoin
# Third party imports
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
# Local imports
from . import ScrapeFunctions
from .ScrapeBase import BaseScraper
from naccbis.Common import utils


class TeamPitchingScraper(BaseScraper):

    """ This scraper is responsible for scraping team pitching stats. """

    PITCHING_COLS = ['no.', 'name', 'yr', 'pos', 'app', 'gs', 'w', 'l', 'ip',
                     'h', 'r', 'er', 'era']
    COACHES_VIEW_COLS = ['no.', 'player', 'era', 'w', 'l', 'app', 'gs', 'ip',
                         'h', 'r', 'er', '2b', '3b', 'hr', 'ab']
    CONFERENCE_COLS = ['name', 'gp', 'ip', 'h', 'r', 'er', 'bb', 'k', 'era']
    TABLES = {
        "overall": "raw_team_pitching_overall",
        "conference": "raw_team_pitching_conference"
    }

    def __init__(self, year: str, split: str, output: str,
                 inseason: bool = False, verbose: bool = False) -> None:
        """ Class constructor
        :param year: The school year. A string.
        :param split: overall or conference stats. A string.
        :param output: Output format. Currently csv and sql.
        :param inseason: Is this scraping taking place in season?
        :param verbose: Print extra information to standard out?
        """
        super().__init__(year, split, output, inseason, verbose)
        self._name = "Team Pitching Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

    def run(self) -> None:
        """ Run the scraper """
        logging.info("%s", self._name)

        if self._split == "overall":
            teamList = ScrapeFunctions.get_team_list(self.BASE_URL, self._year, self.TEAM_IDS)
            logging.info("Found %d teams to scrape", len(teamList))

            for team in teamList:
                logging.info("Fetching %s", team['team'])
                url = "{}{}/{}".format(self.BASE_URL, self._year, team['url'])
                teamSoup = ScrapeFunctions.get_soup(url)
                logging.info("Looking for pitching table")
                df = self._scrape(teamSoup)
                logging.info("Cleaning scraped data")
                df = self._clean(df, team['team'])
                self._data = pd.concat([self._data, df], ignore_index=True)

        elif self._split == "conference":
            logging.info("Fetching teams")
            url = "{}{}/teams".format(self.BASE_URL, self._year)
            soup = ScrapeFunctions.get_soup(url)
            logging.info("Looking for pitching table")
            df = self._scrape(soup)
            logging.info("Cleaning scraped data")
            self._data = self._clean(df, "")

        self._runnable = False

    def _scrape_overall(self, team_soup: BeautifulSoup) -> pd.DataFrame:
        # find index of pitching table
        tableNum1 = ScrapeFunctions.find_table(team_soup, self.PITCHING_COLS)[0]
        pitching = ScrapeFunctions.scrape_table(team_soup, tableNum1 + 1, skip_rows=1)
        # select the totals row
        pitching = pitching[(pitching.Name == "Totals") | (pitching.Name == "Total")]
        pitching = pitching.reset_index(drop=True)
        # make sure that only one row remains

        # make sure that the name is Totals
        if pitching["Name"][0] != "Totals":
            pitching["Name"][0] = "Totals"

        tags = team_soup.find_all('a', string="Coach's View")
        if len(tags) != 1:
            logging.error("Can't find Coach's View")
            raise RuntimeError("Can't find Coach's View")

        url = tags[0].get('href')
        url = urljoin(self.BASE_URL, url)
        coach_soup = ScrapeFunctions.get_soup(url)
        tableNum2 = ScrapeFunctions.find_table(coach_soup, self.COACHES_VIEW_COLS)[0]
        coach_view = ScrapeFunctions.scrape_table(
            coach_soup, tableNum2 + 1, first_row=3, skip_rows=1
        )

        if 'Player' in coach_view.columns:
            coach_view = coach_view.rename(columns={'Player': 'Name'})

        coach_view["Name"] = coach_view["Name"].str.rstrip('.')

        coach_view = coach_view[(coach_view.Name == "Totals") | (coach_view.Name == "Total")]
        coach_view = coach_view.reset_index(drop=True)

        # make sure that the name is Totals
        if coach_view["Name"][0] != "Totals":
            coach_view["Name"][0] = "Totals"

        return pd.merge(coach_view, pitching, on=['No.', 'Name'])

    def _scrape_conference(self, team_soup: BeautifulSoup) -> pd.DataFrame:
        index = 1

        tableNum1 = ScrapeFunctions.find_table(team_soup, self.CONFERENCE_COLS)[index]
        conference = ScrapeFunctions.scrape_table(team_soup, tableNum1 + 1, skip_rows=0)

        # may want to normalize the column names eg, lower(), gp to g
        return conference

    def _scrape(self, team_soup: BeautifulSoup) -> pd.DataFrame:
        # more stats are available on coach's view
        # but coach's view doesn't provide conference stats

        if self._split == "overall":
            return self._scrape_overall(team_soup)
        elif self._split == "conference":
            return self._scrape_conference(team_soup)

    def _clean_overall(self, data: pd.DataFrame, team: str) -> pd.DataFrame:
        unnecessaryCols = ['No.', 'Name', 'Pos', 'Yr', 'app', 'gs', 'GS',
                           'w', 'l', 'sv', 'cg', 'ip', 'h', 'r', 'er', 'bb',
                           'k', 'hr', 'era']
        intCols = ['G', 'W', 'L', 'SV', 'CG', 'SHO', 'IP', 'H', 'R', 'ER',
                   'BB', 'SO', 'x2B', 'x3B', 'HR', 'AB', 'WP', 'HBP', 'BK',
                   'SF', 'SH']
        floatCols = ['ERA', 'AVG', 'SO_9']
        renameCols = {
            'APP': 'G',
            '2B': 'x2B',
            '3B': 'x3B',
            'B/AVG': 'AVG',
            'SFA': 'SF',
            'SHA': 'SH',
            'k/9': 'SO_9'
        }
        finalColNames = ['Name', 'Season', 'G', 'W', 'L', 'SV', 'CG', 'SHO',
                         'IP', 'H', 'R', 'ER', 'BB', 'SO', 'ERA', 'x2B',
                         'x3B', 'HR', 'AB', 'AVG', 'WP', 'HBP',
                         'BK', 'SF', 'SH', 'SO_9']
        if self._inseason:
            finalColNames = ['Name', 'Season', 'Date', 'G', 'W', 'L', 'SV',
                             'CG', 'SHO', 'IP', 'H', 'R', 'ER', 'BB', 'SO',
                             'ERA', 'x2B', 'x3B', 'HR', 'AB', 'AVG', 'WP',
                             'HBP', 'BK', 'SF', 'SH', 'SO_9']

        data.drop(columns=unnecessaryCols, inplace=True)
        data.rename(columns=renameCols, inplace=True)

        data[intCols] = data[intCols].replace('-', '0')
        data[floatCols] = data[floatCols].replace('-', np.nan)
        data[floatCols] = data[floatCols].replace('INF', np.nan)

        data["Name"] = team
        data["Season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["Date"] = str(date.today())
        data = data[finalColNames]
        data.columns = data.columns.to_series().str.lower()
        return data

    def _clean_conference(self, data: pd.DataFrame, team: str) -> pd.DataFrame:
        unnecessaryCols = ['Rk']
        renameCols = {'gp': 'g', 'k': 'so', 'k/9': 'so_9'}
        intCols = ['g', 'h', 'r', 'er', 'bb', 'so', 'hr']
        floatCols = ['so_9', 'era']
        finalColNames = ['Name', 'Season', 'g', 'ip', 'h', 'r', 'er', 'bb',
                         'so', 'so_9', 'hr', 'era']
        if self._inseason:
            finalColNames = ['Name', 'Season', 'Date', 'g', 'ip', 'h', 'r',
                             'er', 'bb', 'so', 'so_9', 'hr', 'era']

        data = data.drop(columns=unnecessaryCols)
        data = data.rename(columns=renameCols)

        data[intCols] = data[intCols].replace('-', '0')
        data[floatCols] = data[floatCols].replace('-', np.nan)
        data[floatCols] = data[floatCols].replace('INF', np.nan)

        data["Season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["Date"] = str(date.today())

        data = data[finalColNames]
        data.columns = data.columns.to_series().str.lower()
        return data

    def _clean(self, data: pd.DataFrame, team: str) -> pd.DataFrame:
        if self._split == "overall":
            return self._clean_overall(data, team)
        elif self._split == "conference":
            return self._clean_conference(data, team)
