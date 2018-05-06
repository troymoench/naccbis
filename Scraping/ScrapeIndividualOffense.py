import pandas as pd
import psycopg2
import sys
import json
from datetime import date
import ScrapeFunctions as sf
'''
This script scrapes individual offense for a given year
Script args: YEAR, SPLIT, OUTPUT, INSEASON
Will need to run this script twice if
you wish to scrape Overall and Conference stats

1. Scrape
2. Clean
3. Export
'''
YEAR = "2017-18"
SPLIT = "overall"
OUTPUT = "sql"
INSEASON = True
# TODO: Add support for in-season scraping
# add date of scraping column (DONE)
# add date of scraping to file name? (DONE)
# add new table in database for in-season
# TODO: Add getData() method (returns DataFrame)


class IndividualOffenseScraper:
    BASE_URL = "http://naccsports.org/sports/bsb/"  # add constants to ScrapeFunctions.py?
    HITTING_COLS = ['no.', 'name', 'yr', 'pos', 'g', 'ab', 'r', 'h', '2b', 'hr', 'avg', 'obp',
                    'slg']
    EXTENDED_HITTING_COLS = ['no.', 'name', 'yr', 'pos', 'g', 'hbp', 'sf', 'pa']
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
    TABLES = {"overall": "raw_batters_overall", "conference": "raw_batters_conference"}

    def __init__(self, year, split, output, inseason=False, verbose=False):
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
        print("Individual Offense Scraper")
        print("Year:", self._year)
        print("Split:", self._split)
        print("In-Season:", self._inseason)
        print("Output format:", self._output)
        if self._runnable:
            print("Scraper has not been run yet. Use run() to do so.")
        else:
            print("Scraper has been run")
            print(self._data.info())

    def run(self):
        # run the scraper
        # TODO: add argument export=True

        teamList = sf.get_team_list(self.BASE_URL, self._year, self.TEAM_IDS)

        # iterate over the teams
        for team in teamList:
            print("Fetching", team['team'])

            teamSoup = sf.get_soup("{}{}/{}".format(self.BASE_URL, self._year, team['url']), verbose=True)
            df = self._scrape(teamSoup)
            df = self._clean(df, team['id'])
            self._data = pd.concat([self._data, df], ignore_index=True)

        self._runnable = False

    def _scrape(self, team_soup):
        # Scrape both the hitting table and extended hitting table
        # and merge

        # Note: Finding the links for overall vs conference probably isn't necessary
        # because the html doesn't change based on the url choice
        # Instead, find the indices of the tables on the same page

        if self._split == "overall":
            index = 0  # overall is first item in list returned by find_table()
        elif self._split == "conference":
            index = 1  # conference is the second item in list returned by find_table()
        else:
            print("Invalid split:", self._split)
            sys.exit(1)

        # find index of hitting table
        tableNum1 = sf.find_table(team_soup, self.HITTING_COLS)[index]
        hitting = sf.scrape_table(team_soup, tableNum1 + 1, skip_rows=2)
        # find index of extended_hitting table
        tableNum2 = sf.find_table(team_soup, self.EXTENDED_HITTING_COLS)[index]
        extendedHitting = sf.scrape_table(team_soup, tableNum2 + 1, skip_rows=2)

        return pd.merge(hitting, extendedHitting, on=["No.", "Name", "Yr", "Pos", "g"])

    def _clean(self, data, team_id):
        # add TeamId, Season
        # replace dashes and strip dots from Yr (Fr. -> Fr)
        # column names cannot start with a digit in PostgreSQL!!!!!
        # disallowed column names: no., 2b, 3b, go/fo

        intCols = ["No.", "g", "ab", "r", "h", "2b", "3b", "hr", "rbi", "bb", "k",
                   "sb", "cs", "hbp", "sf", "sh", "tb", "xbh", "hdp", "go", "fo", "pa"]
        floatCols = ["avg", "obp", "slg", "go/fo"]
        newColNames = ["No", "Name", "Yr", "Pos", "G", "AB", "R", "H", "x2B", "x3B", "HR", "RBI", "BB", "SO", "SB", "CS",
                       "AVG", "OBP", "SLG", "HBP", "SF", "SH", "TB", "XBH", "GDP", "GO", "FO", "GO_FO", "PA"]
        finalColNames = ["No", "Name", "Team", "Season", "Yr", "Pos", "G", "PA", "AB", "R", "H", "x2B",
                         "x3B", "HR", "RBI", "BB", "SO", "SB", "CS", "AVG", "OBP", "SLG", "HBP", "SF", "SH",
                         "TB", "XBH", "GDP", "GO", "FO", "GO_FO"]
        if self._inseason:
            finalColNames = ["No", "Name", "Team", "Season", "Date", "Yr", "Pos", "G", "PA", "AB", "R", "H", "x2B",
                             "x3B", "HR", "RBI", "BB",  "SO", "SB", "CS", "AVG", "OBP", "SLG", "HBP", "SF", "SH",
                             "TB", "XBH", "GDP", "GO", "FO", "GO_FO"]


        # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>

        data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))  # replace '-' with '0'
        data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))  # replace '-' with None

        # convert column names to a friendlier format
        data.columns = newColNames

        data["Team"] = team_id
        data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64
        if self._inseason:
            data["Date"] = str(date.today())
        data["Yr"] = data["Yr"].apply(sf.strip_dots)
        data["Pos"] = data["Pos"].apply(sf.to_none)

        # data = data.sort_values(ascending=False, by=["PA"])  # This doesn't work currently

        return data[finalColNames]

    def export(self):
        # export scraped and cleaned data to csv or database
        # NOTE: If exporting to database, the table must already be created.

        if self._runnable:
            print("Cannot export. Scraper has not been run yet. Use run() to do so.")
            sys.exit(1)
        else:
            tableName = self.TABLES[self._split]

            if self._output == "csv":
                if self._inseason:
                    self._data.to_csv(
                        "{}{}{}.csv".format(self._config["csv_path"], tableName, str(date.today())),
                        index=False)
                else:
                    self._data.to_csv("{}{}{}.csv".format(self._config["csv_path"], tableName,
                                                          sf.year_to_season(self._year)), index=False)
            elif self._output == "sql":
                con = psycopg2.connect(host=self._config["host"], database=self._config["database"],
                                       user=self._config["user"], password=self._config["password"])

                if self._inseason:
                    tableName += "_inseason"
                sf.df_to_sql(con, self._data, tableName, verbose=self._verbose)
                con.close()
            else:
                print("Invalid output type:", self._output)
                sys.exit(1)
            if self._verbose:
                print("Successfully exported")

    def get_data(self):
        return self._data


# ***********************************
# ****** BEGINNING OF SCRIPT ********
# ***********************************
if __name__ == "__main__":
    scraper = IndividualOffenseScraper(YEAR, SPLIT, OUTPUT, inseason=INSEASON, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()
