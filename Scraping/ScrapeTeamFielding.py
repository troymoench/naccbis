import pandas as pd
import psycopg2
import sys
import json
import ScrapeFunctions as sf

YEAR = "2013-14"
SPLIT = "overall"
OUTPUT = "sql"
# TODO: Add support for in-season scraping


class TeamFieldingScraper:
    BASE_URL = "http://naccsports.org/sports/bsb/"  # add constants to ScrapeFunctions.py?
    FIELDING_COLS = ['name', 'gp', 'tc', 'po', 'a', 'e', 'fpct', 'dp']
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
    TABLES = {"overall": "raw_team_fielding_overall", "conference": "raw_team_fielding_conference"}

    def __init__(self, year, split, output, verbose=False):
        self._year = year
        self._split = split
        self._output = output
        self._verbose = verbose
        self._data = pd.DataFrame()
        self._runnable = True

        # TODO: Add error handling
        with open('config.json') as f:
            self._config = json.load(f)

    def info(self):
        print("Team Fielding Scraper")
        print("Year:", self._year)
        print("Split:", self._split)
        print("Output format:", self._output)
        if self._runnable:
            print("Scraper has not been run yet. Use run() to do so.")
        else:
            print("Scraper has been run")
            print(self._data.info())

    def run(self):
        # run the scraper
        # TODO: add argument export=True
        soup = sf.get_soup(self.BASE_URL + self._year + "/teams", verbose=self._verbose)
        df = self._scrape(soup)
        self._data = self._clean(df)
        # print(self._data)
        # print(self._data.info())

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

        # remove unnecessary columns
        data = data.drop(columns=unnecessaryCols)

        # rename columns
        data = data.rename(columns=renameCols)

        # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>
        for col in intCols:
            data[col] = data[col].apply(sf.replace_dash, replacement='0')
        for col in floatCols:
            data[col] = data[col].apply(sf.replace_dash, replacement=None)
            data[col] = data[col].apply(sf.replace_inf, replacement=None)

        data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64

        finalColNames = data.axes[1].tolist()
        finalColNames.remove("Season")
        finalColNames.insert(1, "Season")

        return data[finalColNames]

    def export(self):
        # export scraped and cleaned data to csv or database
        if self._runnable:
            print("Cannot export. Scraper has not been run yet. Use run() to do so.")
            sys.exit(1)
        else:

            tableName = self.TABLES[self._split]

            if self._output == "csv":
                self._data.to_csv("{}{}{}.csv".format(self._config["csv_path"], tableName, self._year), index=False)
            elif self._output == "sql":
                con = psycopg2.connect(host=self._config["host"], database=self._config["database"],
                                       user=self._config["user"], password=self._config["password"])
                sf.df_to_sql(con, self._data, tableName, verbose=self._verbose)
                con.close()
            else:
                print("Invalid output type:", self._output)
                sys.exit(1)
            if self._verbose:
                print("Successfully exported")


# ***********************************
# ****** BEGINNING OF SCRIPT ********
# ***********************************
if __name__ == "__main__":
    scraper = TeamFieldingScraper(YEAR, SPLIT, OUTPUT, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()

