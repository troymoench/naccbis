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


class TeamOffenseScraper(BaseScraper):
    HITTING_COLS = ['name', 'gp', 'ab', 'r', 'h', '2b', 'hr', 'avg', 'obp',
                    'slg']
    EXTENDED_HITTING_COLS = ['name', 'gp', 'hbp', 'sf', 'sh', 'pa']
    TABLES = {"overall": "raw_team_offense_overall", "conference": "raw_team_offense_conference"}

    def __init__(self, year, split, output, inseason=False, verbose=False):
        super().__init__(year, split, output, inseason, verbose)
        self._name = "Team Offense Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

        # TODO: Add error handling
        with open('../config.json') as f:
            self._config = json.load(f)

    def run(self):
        # run the scraper
        # TODO: add argument export=True
        soup = sf.get_soup(self.BASE_URL + self._year + "/teams", verbose=self._verbose)
        df = self._scrape(soup)
        self._data = self._clean(df)
        self._runnable = False

    def _scrape(self, soup):
        # Scrape both the hitting table and extended hitting table
        # and merge

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
        newColNames = ["Name", "GP", "AB", "R", "H", "x2B", "x3B", "HR", "RBI", "BB", "SO", "SB", "CS",
                       "AVG", "OBP", "SLG", "HBP", "SF", "SH", "TB", "XBH", "GDP", "GO", "FO", "GO_FO", "PA"]

        finalColNames = ["Name", "Season", "GP", "PA", "AB", "R", "H", "x2B", "x3B", "HR", "RBI", "BB",
                         "SO", "SB", "CS", "AVG", "OBP", "SLG", "HBP", "SF", "SH", "TB", "XBH", "GDP", "GO", "FO",
                         "GO_FO"]
        if self._inseason:
            finalColNames = ["Name", "Season", "Date", "GP", "PA", "AB", "R", "H", "x2B", "x3B", "HR", "RBI", "BB",
                             "SO", "SB", "CS", "AVG", "OBP", "SLG", "HBP", "SF", "SH", "TB", "XBH", "GDP", "GO", "FO",
                             "GO_FO"]

        # remove unnecessary columns
        data.drop(columns=unnecessaryCols, inplace=True)

        # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>

        data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))  # replace '-' with '0'
        data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))  # replace '-' with None

        # convert column names to a friendlier format
        data.columns = newColNames

        data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64
        if self._inseason:
            data["Date"] = str(date.today())
        # data = data.sort_values(ascending=False, by=["PA"])  # This doesn't work currently

        return data[finalColNames]


# ***********************************
# ****** BEGINNING OF SCRIPT ********
# ***********************************
if __name__ == "__main__":
    scraper = TeamOffenseScraper(YEAR, SPLIT, OUTPUT, INSEASON, verbose=True)
    # scraper.info()
    scraper.run()
    # scraper.info()
    scraper.export()
