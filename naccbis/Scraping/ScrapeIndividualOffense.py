""" This module provides the IndividualOffenseScraper class """
# Standard library imports
from datetime import date
import logging
import sys
# Third party imports
import pandas as pd
# Local imports
from . import ScrapeFunctions as sf
from .ScrapeBase import BaseScraper
import naccbis.Common.utils as utils


class IndividualOffenseScraper(BaseScraper):

    """ This scraper is responsible for scraping individual offensive stats. """

    HITTING_COLS = ['no.', 'name', 'yr', 'pos', 'g', 'ab', 'r', 'h', '2b', 'hr', 'avg', 'obp',
                    'slg']
    EXTENDED_HITTING_COLS = ['no.', 'name', 'yr', 'pos', 'g', 'hbp', 'sf', 'pa']
    TABLES = {"overall": "raw_batters_overall", "conference": "raw_batters_conference"}

    def __init__(self, year, split, output, inseason=False, verbose=False):
        """ Class constructor
        :param year: The school year. A string.
        :param split: overall or conference stats. A string.
        :param output: Output format. Currently csv and sql.
        :param inseason: Is this scraping taking place in season?
        :param verbose: Print extra information to standard out?
        """
        super().__init__(year, split, output, inseason, verbose)
        self._name = "Individual Offense Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

    def run(self):
        """ Run the scraper """
        logging.info("%s", self._name)

        teamList = sf.get_team_list(self.BASE_URL, self._year, self.TEAM_IDS)
        logging.info("Found %d teams to scrape", len(teamList))

        # iterate over the teams
        for team in teamList:
            logging.info("Fetching %s", team['team'])

            url = "{}{}/{}".format(self.BASE_URL, self._year, team['url'])
            teamSoup = sf.get_soup(url)
            if sf.skip_team(teamSoup):
                continue
            logging.info("Looking for hitting tables")
            df = self._scrape(teamSoup)
            logging.info("Cleaning scraped data")
            df = self._clean(df, team['id'])
            self._data = pd.concat([self._data, df], ignore_index=True)

        self._runnable = False

    def _scrape(self, team_soup):
        """ Scrape both the hitting table and extended hitting table and merge """

        # Note: Finding the links for overall vs conference probably isn't necessary
        # because the html doesn't change based on the url choice
        # Instead, find the indices of the tables on the same page

        if self._split == "overall":
            index = 0  # overall is first item in list returned by find_table()
        elif self._split == "conference":
            index = 1  # conference is the second item in list returned by find_table()
        else:
            print("Invalid split:", self._split)
            sys.exit(1)

        # find index of hitting table
        tableNum1 = sf.find_table(team_soup, self.HITTING_COLS)[index]
        hitting = sf.scrape_table(team_soup, tableNum1 + 1, skip_rows=2)
        # find index of extended_hitting table
        tableNum2 = sf.find_table(team_soup, self.EXTENDED_HITTING_COLS)[index]
        extendedHitting = sf.scrape_table(team_soup, tableNum2 + 1, skip_rows=2)

        return pd.merge(hitting, extendedHitting, on=["No.", "Name", "Yr", "Pos", "g"])

    def _clean(self, data, team_id):
        # add TeamId, Season
        # replace dashes and strip dots from Yr (Fr. -> Fr)
        # column names cannot start with a digit in PostgreSQL!!!!!
        # disallowed column names: no., 2b, 3b, go/fo

        intCols = ["No.", "g", "ab", "r", "h", "2b", "3b", "hr", "rbi", "bb", "k",
                   "sb", "cs", "hbp", "sf", "sh", "tb", "xbh", "hdp", "go", "fo", "pa"]
        floatCols = ["avg", "obp", "slg", "go/fo"]
        newColNames = ["No", "Name", "Yr", "Pos", "G", "AB", "R", "H", "x2B",
                       "x3B", "HR", "RBI", "BB", "SO", "SB", "CS",
                       "AVG", "OBP", "SLG", "HBP", "SF", "SH", "TB", "XBH",
                       "GDP", "GO", "FO", "GO_FO", "PA"]
        finalColNames = ["No", "Name", "Team", "Season", "Yr", "Pos", "G", "PA",
                         "AB", "R", "H", "x2B", "x3B", "HR", "RBI", "BB", "SO",
                         "SB", "CS", "AVG", "OBP", "SLG", "HBP", "SF", "SH",
                         "TB", "XBH", "GDP", "GO", "FO", "GO_FO"]
        if self._inseason:
            finalColNames = ["No", "Name", "Team", "Season", "Date", "Yr", "Pos",
                             "G", "PA", "AB", "R", "H", "x2B", "x3B", "HR", "RBI",
                             "BB",  "SO", "SB", "CS", "AVG", "OBP", "SLG", "HBP",
                             "SF", "SH", "TB", "XBH", "GDP", "GO", "FO", "GO_FO"]

        data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))
        data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))

        # convert column names to a friendlier format
        data.columns = newColNames

        data["Team"] = team_id
        data["Season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["Date"] = str(date.today())
        data["Yr"] = data["Yr"].apply(sf.strip_dots)
        data["Pos"] = data["Pos"].apply(sf.to_none)

        data = data[finalColNames]
        data.columns = data.columns.to_series().str.lower()
        return data


if __name__ == "__main__":
    YEAR = "2017-18"
    SPLIT = "overall"
    OUTPUT = "csv"
    INSEASON = True
    scraper = IndividualOffenseScraper(YEAR, SPLIT, OUTPUT, inseason=INSEASON, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()
