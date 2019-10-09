""" This module provides the TeamFieldingScraper class """
# Standard library imports
from datetime import date
import logging
import sys
# Third party imports
import pandas as pd
# Local imports
import naccbis.Scraping.ScrapeFunctions as sf
from naccbis.Scraping.ScrapeBase import BaseScraper
import naccbis.Common.utils as utils

YEAR = "2017-18"
SPLIT = "conference"
OUTPUT = "sql"
INSEASON = True


class TeamFieldingScraper(BaseScraper):

    """ This scraper is responsible for scraping team fielding stats. """

    FIELDING_COLS = ['name', 'gp', 'tc', 'po', 'a', 'e', 'fpct', 'dp']
    TABLES = {"overall": "raw_team_fielding_overall",
              "conference": "raw_team_fielding_conference"}

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

    def run(self):
        """ Run the scraper """
        logging.info("%s", self._name)
        logging.info("Fetching teams")
        url = "{}{}/teams".format(self.BASE_URL, self._year)
        soup = sf.get_soup(url, verbose=self._verbose)
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
        finalColNames = ['Name', 'Season', 'g', 'tc', 'po', 'a', 'e', 'fpct',
                         'dp', 'sba', 'cs', 'cspct', 'pb', 'ci']
        if self._inseason:
            finalColNames = ['Name', 'Season', 'Date', 'g', 'tc', 'po', 'a',
                             'e', 'fpct', 'dp', 'sba', 'cs', 'cspct', 'pb', 'ci']

        data.drop(columns=unnecessaryCols, inplace=True)
        data.rename(columns=renameCols, inplace=True)

        data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))
        data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))
        data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_inf(x, None))

        data["Season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["Date"] = str(date.today())

        data = data[finalColNames]
        data.columns = data.columns.to_series().str.lower()
        return data


# ***********************************
# ****** BEGINNING OF SCRIPT ********
# ***********************************
if __name__ == "__main__":
    scraper = TeamFieldingScraper(YEAR, SPLIT, OUTPUT, INSEASON, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()
