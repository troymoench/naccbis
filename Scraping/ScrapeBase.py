""" This module provides the BaseScraper class """

import pandas as pd
import psycopg2
import sys
import json
import logging
from datetime import date
import ScrapeFunctions as sf


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

        # TODO: Add error handling
        with open('../config.json') as f:
            self._config = json.load(f)

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
        """ Export scraped and cleaned data to csv or database
        :returns: None
        """
        # export scraped and cleaned data to csv or database
        # NOTE: If exporting to database, the table must already be created.
        logging.info("Exporting data from %s", self._name)
        if self._runnable:
            print("Cannot export. Scraper has not been run yet. Use run() to do so.")
            sys.exit(1)
        else:
            tableName = self.TABLES[self._split]
            if self._output == "csv":
                try:
                    if self._inseason:
                        self._data.to_csv(
                            "{}{}{}.csv".format(self._config["csv_path"], tableName, str(date.today())),
                            index=False)
                    else:
                        self._data.to_csv("{}{}{}.csv".format(self._config["csv_path"], tableName,
                                                              sf.year_to_season(self._year)), index=False)
                except Exception as e:
                    print("Unable to export to CSV")
                    print(e)
                    logging.error("Unable to export to CSV")
                    logging.error(e)
                    return
                else:
                    print("Successfully exported to CSV file")
                    logging.info("Successfully exported to CSV file")

            elif self._output == "sql":
                print("Connecting to database")
                logging.info("Connecting to database")

                try:
                    con = psycopg2.connect(host=self._config["host"], database=self._config["database"],
                                           user=self._config["user"], password=self._config["password"])
                except psycopg2.Error as e:
                    print("Unable to connect to database")
                    print(e)
                    logging.error("Unable to connect to database")
                    logging.error(e)
                    logging.debug("DB HOST: %s", self._config["host"])
                    logging.debug("DB USER: %s", self._config["user"])
                    logging.debug("DB NAME: %s", self._config["database"])
                    return
                except KeyError as e:
                    print("Config value {} not found".format(e))
                    logging.critical("Config value {} not found".format(e))
                    sys.exit(1)
                else:
                    if self._verbose:
                        print("Connection established")
                    logging.info("Connection established")
                    logging.debug("DB HOST: %s", self._config["host"])
                    logging.debug("DB USER: %s", self._config["user"])
                    logging.debug("DB NAME: %s", self._config["database"])

                if self._inseason:
                    tableName += "_inseason"
                try:
                    sf.df_to_sql(con, self._data, tableName, verbose=self._verbose)
                except psycopg2.Error:
                    print("Unable to export to database")
                    logging.error("Unable to export to database")
                    return
                else:
                    print("Successfully exported to database")
                    logging.info("Successfully exported to database")
                con.close()
            else:
                print("Invalid output type:", self._output)
                logging.critical("Invalid output type: %s", self._output)
                sys.exit(1)

    def get_data(self):
        return self._data
