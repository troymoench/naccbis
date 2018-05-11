import pandas as pd
import psycopg2
import sys
import json
from datetime import date
import ScrapeFunctions as sf

'''This is the base class for the scrapers
   It provides only the shared functionality between all
   scrapers. Don't directly create an instance of the base class!
'''


class BaseScraper:
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
        print("\n--------------------------")
        print(self._name)
        print("Year:", self._year)
        print("Split:", self._split)
        if self._verbose:
            print("In-Season:", self._inseason)
            print("Output format:", self._output)
        print("--------------------------")

    def export(self):
        # export scraped and cleaned data to csv or database
        # NOTE: If exporting to database, the table must already be created.

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
                    return
                else:
                    print("CSV successfully exported")

            elif self._output == "sql":
                print("Connecting to database")
                try:
                    con = psycopg2.connect(host=self._config["host"], database=self._config["database"],
                                           user=self._config["user"], password=self._config["password"])
                except psycopg2.Error as e:
                    print("Unable to connect to database")
                    print(e)
                    return
                else:
                    if self._verbose:
                        print("Connection established")
                if self._inseason:
                    tableName += "_inseason"
                try:
                    sf.df_to_sql(con, self._data, tableName, verbose=self._verbose)
                except psycopg2.Error:
                    print("Unable to export to database")
                    return
                else:
                    print("Successfully exported to database")
                con.close()
            else:
                print("Invalid output type:", self._output)
                sys.exit(1)

    def get_data(self):
        return self._data
