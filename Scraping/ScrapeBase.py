""" This module provides the BaseScraper class """
# Standard library imports
from datetime import date
import sys
import logging
# Third party imports
import pandas as pd
# Local imports
import Common.utils as utils


class BaseScraper:

    """ This is the abstract base class for the scrapers.

    It provides only the shared functionality between all scrapers.
    Don't directly create an instance of the base class!

    General procedure that each scraper follows:

    1. Scrape the data from the web
    2. Clean the data
    3. Export the data

    """

    BASE_URL = "http://naccsports.org/sports/bsb/"
    TEAM_IDS = {
        'Aurora': 'AUR',
        'Benedictine': 'BEN',
        'Concordia Chicago': 'CUC',
        'Concordia Wisconsin': 'CUW',
        'Dominican': 'DOM',
        'Edgewood': 'EDG',
        'Illinois Tech': 'ILLT',
        'Lakeland': 'LAK',
        'MSOE': 'MSOE',
        'Marian': 'MAR',
        'Maranatha': 'MARN',
        'Rockford': 'ROCK',
        'Wisconsin Lutheran': 'WLC'
    }
    TABLES = {}

    def __init__(self, year, split, output, inseason=False, verbose=False):
        """ Class constructor
        :param year: The school year. A string.
        :param split: overall or conference stats. A string.
        :param output: Output format. Currently csv and sql.
        :param inseason: Is this scraping taking place in season?
        :param verbose: Print extra information to standard out?
        """
        self._name = "Base Scraper"
        self._year = year
        self._split = split
        self._output = output
        self._inseason = inseason
        self._verbose = verbose
        self._data = pd.DataFrame()
        self._runnable = True
        self._config = utils.init_config()["DB"]
        self._config["csv_path"] = ""

    def info(self):
        """ Print the scraper information to standard out
        :returns: None
        """
        print("\n--------------------------")
        print(self._name)
        print("Year:", self._year)
        print("Split:", self._split)
        if self._verbose:
            print("In-Season:", self._inseason)
            print("Output format:", self._output)
        print("--------------------------")

    def export(self):
        """ Export scraped and cleaned data to csv or database.
        If exporting to database, the table must already exist
        :returns: None
        """
        logging.info("Exporting data from %s", self._name)
        if self._runnable:
            print("Cannot export. Scraper has not been run yet. Use run() to do so.")
            sys.exit(1)
        tableName = self.TABLES[self._split]
        if self._output == "csv":
            try:
                if self._inseason:
                    filename = "{}{}{}.csv".format(self._config["csv_path"],
                                                   tableName,
                                                   str(date.today()))
                    self._data.to_csv(filename, index=False)
                else:
                    filename = "{}{}{}.csv".format(self._config["csv_path"],
                                                   tableName,
                                                   utils.year_to_season(self._year))
                    self._data.to_csv(filename, index=False)
            except Exception as e:
                logging.error("Unable to export to CSV")
                logging.error(e)
                return
            else:
                logging.info("Successfully exported to CSV file")

        elif self._output == "sql":
            logging.info("Connecting to database")
            conn = utils.connect_db(self._config)

            if self._inseason:
                tableName += "_inseason"

            utils.db_load_data(self._data, tableName, conn, if_exists="append", index=False)
            conn.close()
        else:
            logging.critical("Invalid output type: %s", self._output)
            sys.exit(1)

    def get_data(self):
        return self._data
