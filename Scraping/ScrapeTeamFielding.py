""" This module provides the TeamFieldingScraper class """
# Standard library imports
from datetime import date
import json
import logging
import sys
# Third party imports
import pandas as pd
# Local imports
import ScrapeFunctions as sf
from ScrapeBase import BaseScraper
import Common.utils as utils

YEAR = "2017-18"
SPLIT = "conference"
OUTPUT = "sql"
INSEASON = True


class TeamFieldingScraper(BaseScraper):

    """ This scraper is responsible for scraping team fielding stats. """

    FIELDING_COLS = ['name', 'gp', 'tc', 'po', 'a', 'e', 'fpct', 'dp']
    TABLES = {"overall": "raw_team_fielding_overall", "conference": "raw_team_fielding_conference"}

    def __init__(self, year, split, output, inseason=False, verbose=False):
        """ Class constructor
        :param year: The school year. A string.
        :param split: overall or conference stats. A string.
        :param output: Output format. Currently csv and sql.
        :param inseason: Is this scraping taking place in season?
        :param verbose: Print extra information to standard out?
        """
        super().__init__(year, split, output, inseason, verbose)
        self._name = "Team Fielding Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

        # TODO: Add error handling
        with open('../config.json') as f:
            self._config = json.load(f)

    def run(self):
        # run the scraper
        # TODO: add argument export=True
        logging.info("%s", self._name)
        logging.info("Fetching teams")
        soup = sf.get_soup(self.BASE_URL + self._year + "/teams", verbose=self._verbose)
        logging.info("Looking for fielding table")
        df = self._scrape(soup)
        logging.info("Cleaning scraped data")
        self._data = self._clean(df)

        self._runnable = False

    def _scrape(self, soup):
        if self._split == "overall":
            index = 0
        elif self._split == "conference":
            index = 1
        else:
            print("Invalid split:", self._split)
            sys.exit(1)

        # find index of fielding table
        tableNum1 = sf.find_table(soup, self.FIELDING_COLS)[index]
        fielding = sf.scrape_table(soup, tableNum1 + 1, skip_rows=0)

        # may want to normalize the column names eg, lower(), gp to g
        return fielding

    def _clean(self, data):
        unnecessaryCols = ['Rk']
        renameCols = {'gp': 'g', 'rcs': 'cs', 'rcs%': 'cspct'}
        intCols = ['g', 'tc', 'po', 'a', 'e', 'dp', 'sba', 'cs', 'pb', 'ci']
        floatCols = ['fpct', 'cspct']
        finalColNames = ['Name', 'Season', 'g', 'tc', 'po', 'a', 'e', 'fpct', 'dp', 'sba', 'cs', 'cspct', 'pb', 'ci']
        if self._inseason:
            finalColNames = ['Name', 'Season', 'Date', 'g', 'tc', 'po', 'a', 'e', 'fpct', 'dp', 'sba', 'cs', 'cspct',
                             'pb', 'ci']

        # remove unnecessary columns
        data.drop(columns=unnecessaryCols, inplace=True)

        # rename columns
        data.rename(columns=renameCols, inplace=True)

        # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>
        data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))  # replace '-' with '0'
        data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))  # replace '-' with None
        data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_inf(x, None))  # replace 'inf' with None

        data["Season"] = str(utils.year_to_season(self._year))  # converts to str for now, should be numpy.int64
        if self._inseason:
            data["Date"] = str(date.today())

        return data[finalColNames]


# ***********************************
# ****** BEGINNING OF SCRIPT ********
# ***********************************
if __name__ == "__main__":
    scraper = TeamFieldingScraper(YEAR, SPLIT, OUTPUT, INSEASON, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()
