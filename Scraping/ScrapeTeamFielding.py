import pandas as pd
import psycopg2
import sys
import json
from datetime import date
import ScrapeFunctions as sf
from ScrapeBase import BaseScraper

YEAR = "2017-18"
SPLIT = "conference"
OUTPUT = "sql"
INSEASON = True


class TeamFieldingScraper(BaseScraper):
    FIELDING_COLS = ['name', 'gp', 'tc', 'po', 'a', 'e', 'fpct', 'dp']
    TABLES = {"overall": "raw_team_fielding_overall", "conference": "raw_team_fielding_conference"}

    def __init__(self, year, split, output, inseason=False, verbose=False):
        super().__init__(year, split, output, inseason, verbose)
        self._name = "Team Fielding Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

        # TODO: Add error handling
        with open('../config.json') as f:
            self._config = json.load(f)
    #
    # def info(self):
    #     print("\n---------------------")
    #     print("Team Fielding Scraper")
    #     print("Year:", self._year)
    #     print("Split:", self._split)
    #     if self._verbose:
    #         print("In-Season:", self._inseason)
    #         print("Output format:", self._output)
    #         if self._runnable:
    #             print("Scraper has not been run yet. Use run() to do so.")
    #         else:
    #             print("Scraper has been run")
    #             print(self._data.info())
    #     print("---------------------")

    def run(self):
        # run the scraper
        # TODO: add argument export=True
        soup = sf.get_soup(self.BASE_URL + self._year + "/teams", verbose=self._verbose)
        df = self._scrape(soup)
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

        data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64
        if self._inseason:
            data["Date"] = str(date.today())

        return data[finalColNames]
    #
    # def export(self):
    #     # export scraped and cleaned data to csv or database
    #     if self._runnable:
    #         print("Cannot export. Scraper has not been run yet. Use run() to do so.")
    #         sys.exit(1)
    #     else:
    #
    #         tableName = self.TABLES[self._split]
    #
    #         if self._output == "csv":
    #
    #             if self._inseason:
    #                 self._data.to_csv("{}{}{}.csv".format(self._config["csv_path"], tableName,
    #                                                       str(date.today())), index=False)
    #             else:
    #                 self._data.to_csv("{}{}{}.csv".format(self._config["csv_path"], tableName,
    #                                                       sf.year_to_season(self._year)), index=False)
    #         elif self._output == "sql":
    #             con = psycopg2.connect(host=self._config["host"], database=self._config["database"],
    #                                    user=self._config["user"], password=self._config["password"])
    #             if self._inseason:
    #                 tableName += "_inseason"
    #             sf.df_to_sql(con, self._data, tableName, verbose=self._verbose)
    #             con.close()
    #         else:
    #             print("Invalid output type:", self._output)
    #             sys.exit(1)
    #         # if self._verbose:
    #         #     print("Successfully exported")
    #
    # def get_data(self):
    #     return self._data


# ***********************************
# ****** BEGINNING OF SCRIPT ********
# ***********************************
if __name__ == "__main__":
    scraper = TeamFieldingScraper(YEAR, SPLIT, OUTPUT, INSEASON, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()

