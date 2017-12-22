import pandas as pd
import psycopg2
import sys
import ScrapeFunctions as sf

YEAR = "2016-17"
SPLIT = "overall"
OUTPUT = "csv"
# TODO: Add support for in-season scraping


class TeamOffenseScraper:
    BASE_URL = "http://naccsports.org/sports/bsb/"  # add constants to ScrapeFunctions.py?
    HITTING_COLS = ['name', 'gp', 'ab', 'r', 'h', '2b', 'hr', 'avg', 'obp',
                    'slg']
    EXTENDED_HITTING_COLS = ['name', 'gp', 'hbp', 'sf', 'sh', 'pa']
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

    def __init__(self, year, split, output, verbose=False):
        self._year = year
        self._split = split
        self._output = output
        self._verbose = verbose
        self._data = pd.DataFrame()
        self._runnable = True

    def info(self):
        print("Individual Offense Scraper")
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
        self._runnable = False

    def _scrape(self, soup):
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

        # may want to normalize the column names before merging, eg, tolower(), gp to g
        return pd.merge(hitting, extendedHitting, on=["Rk", "Name", "gp"])

    def _clean(self, data):
        intCols = ["gp", "ab", "r", "h", "2b", "3b", "hr", "rbi", "bb", "k",
                   "sb", "cs", "hbp", "sf", "sh", "tb", "xbh", "hdp", "go", "fo", "pa"]
        floatCols = ["avg", "obp", "slg", "go/fo"]
        newColNames = ["Name", "GP", "AB", "R", "H", "x2B", "x3B", "HR", "RBI", "BB", "SO", "SB", "CS",
                       "AVG", "OBP", "SLG", "HBP", "SF", "SH", "TB", "XBH", "GDP", "GO", "FO", "GO_FO", "PA"]

        finalColNames = ["Name", "Season", "GP", "PA", "AB", "R", "H", "x2B", "x3B", "HR", "RBI", "BB",
                         "SO", "SB", "CS", "AVG", "OBP", "SLG", "HBP", "SF", "SH", "TB", "XBH", "GDP", "GO", "FO",
                         "GO_FO"]
        del data["Rk"]

        # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>
        for col in intCols:
            data[col] = data[col].apply(sf.replace_dash, replacement=0)
            # data[col] = data[col].apply(to_int)
        for col in floatCols:
            data[col] = data[col].apply(sf.replace_dash, replacement=None)
            # data[col] = data[col].apply(to_float)

        # convert column names to a friendlier format
        data.columns = newColNames

        data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64
        # data = data.sort_values(ascending=False, by=["PA"])  # This doesn't work currently

        return data[finalColNames]

    def export(self):
        # export scraped and cleaned data to csv or database
        # TODO: Use config.json to configure database connection and csv path
        if self._runnable:
            print("Cannot export. Scraper has not been run yet. Use run() to do so.")
            sys.exit(1)
        else:
            tables = {"overall": "raw_teams_overall", "conference": "raw_teams_conference"}
            tableName = tables[self._split]

            if self._output == "csv":
                self._data.to_csv("{}{}.csv".format(tableName, self._year), index=False)
            elif self._output == "sql":
                con = psycopg2.connect(host="192.168.0.101", database="naccbisdb", user="troy", password="baseballisfun")
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
    scraper = TeamOffenseScraper(YEAR, SPLIT, OUTPUT, verbose=True)
    # scraper.info()
    scraper.run()
    scraper.info()
    scraper.export()
