""" This module provides the TeamOffenseScraper class """
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


class TeamOffenseScraper(BaseScraper):

    """ This scraper is responsible for scraping team offensive stats. """

    HITTING_COLS = ['name', 'gp', 'ab', 'r', 'h', '2b', 'hr', 'avg', 'obp', 'slg']
    EXTENDED_HITTING_COLS = ['name', 'gp', 'hbp', 'sf', 'sh', 'pa']
    TABLES = {
        "overall": "raw_team_offense_overall",
        "conference": "raw_team_offense_conference"
    }

    def __init__(self, year, split, output, inseason=False, verbose=False):
        """ Class constructor
        :param year: The school year. A string.
        :param split: overall or conference stats. A string.
        :param output: Output format. Currently csv and sql.
        :param inseason: Is this scraping taking place in season?
        :param verbose: Print extra information to standard out?
        """
        super().__init__(year, split, output, inseason, verbose)
        self._name = "Team Offense Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

    def run(self):
        """ Run the scraper """
        logging.info("%s", self._name)
        logging.info("Fetching teams")
        url = "{}{}/teams".format(self.BASE_URL, self._year)
        soup = sf.get_soup(url)
        logging.info("Looking for hitting tables")
        df = self._scrape(soup)
        logging.info("Cleaning scraped data")
        self._data = self._clean(df)
        self._runnable = False

    def _scrape(self, soup):
        """ Scrape both the hitting table and extended hitting table and merge """

        if self._split == "overall":
            index = 0
        elif self._split == "conference":
            index = 1
        else:
            print("Invalid split:", self._split)
            sys.exit(1)

        # find index of hitting table
        tableNum1 = sf.find_table(soup, self.HITTING_COLS)[index]
        hitting = sf.scrape_table(soup, tableNum1 + 1, skip_rows=0)
        # find index of extended_hitting table
        tableNum2 = sf.find_table(soup, self.EXTENDED_HITTING_COLS)[index]
        extendedHitting = sf.scrape_table(soup, tableNum2 + 1, skip_rows=0)

        # may want to normalize the column names before merging, eg, lower(), gp to g
        return pd.merge(hitting, extendedHitting, on=["Rk", "Name", "gp"])

    def _clean(self, data):
        unnecessaryCols = ['Rk']
        intCols = ["gp", "ab", "r", "h", "2b", "3b", "hr", "rbi", "bb", "k",
                   "sb", "cs", "hbp", "sf", "sh", "tb", "xbh", "hdp", "go", "fo", "pa"]
        floatCols = ["avg", "obp", "slg", "go/fo"]
        newColNames = ["Name", "G", "AB", "R", "H", "x2B", "x3B", "HR", "RBI",
                       "BB", "SO", "SB", "CS", "AVG", "OBP", "SLG", "HBP", "SF",
                       "SH", "TB", "XBH", "GDP", "GO", "FO", "GO_FO", "PA"]

        finalColNames = ["Name", "Season", "G", "PA", "AB", "R", "H", "x2B",
                         "x3B", "HR", "RBI", "BB", "SO", "SB", "CS", "AVG",
                         "OBP", "SLG", "HBP", "SF", "SH", "TB", "XBH", "GDP",
                         "GO", "FO", "GO_FO"]
        if self._inseason:
            finalColNames = ["Name", "Season", "Date", "G", "PA", "AB", "R", "H",
                             "x2B", "x3B", "HR", "RBI", "BB", "SO", "SB", "CS",
                             "AVG", "OBP", "SLG", "HBP", "SF", "SH", "TB", "XBH",
                             "GDP", "GO", "FO", "GO_FO"]

        data.drop(columns=unnecessaryCols, inplace=True)

        data[intCols] = data[intCols].replace('-', '0')
        data[floatCols] = data[floatCols].replace('-', pd.np.nan)

        # convert column names to a friendlier format
        data.columns = newColNames

        data["Season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["Date"] = str(date.today())

        data = data[finalColNames]
        data.columns = data.columns.to_series().str.lower()
        return data


if __name__ == "__main__":
    YEAR = "2017-18"
    SPLIT = "conference"
    OUTPUT = "sql"
    INSEASON = True
    scraper = TeamOffenseScraper(YEAR, SPLIT, OUTPUT, INSEASON, verbose=True)
    # scraper.info()
    scraper.run()
    # scraper.info()
    scraper.export()
