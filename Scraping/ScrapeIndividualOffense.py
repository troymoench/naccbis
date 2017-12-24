import pandas as pd
import psycopg2
import sys
import json
import ScrapeFunctions as sf
'''
This script scrapes individual offense for a given year
Script args: <period> ...
Will need to run this script twice if
you wish to scrape Overall and Conference stats

1. Scrape
2. Clean
3. Export
'''
YEAR = "2014-15"
SPLIT = "conference"
OUTPUT = "sql"
# TODO: Add support for in-season scraping


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

    def __init__(self, year, split, output, verbose=False):
        self._year = year
        self._split = split
        self._output = output
        self._verbose = verbose
        self._data = pd.DataFrame()
        self._runnable = True

        with open('config.json') as f:
            self._config = json.load(f)

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

        teamList = sf.get_team_list(self.BASE_URL, self._year, self.TEAM_IDS)

        # iterate over the teams
        for team in teamList:
            print("Fetching", team['team'])

            teamSoup = sf.get_soup("{}{}/{}".format(self.BASE_URL, self._year, team['url']), verbose=True)
            df = self._scrape(teamSoup)
            # print(df.info())
            df = self._clean(df, team['id'])
            # print(df.info())
            self._data = pd.concat([self._data, df], ignore_index=True)

        self._runnable = False

    def _scrape(self, team_soup):
        # TODO: Finding the links for overall vs conference probably isn't necessary
        # TODO: because the html doesn't change based on the url choice

        if self._split == "overall":
            # link = team_soup.find("a", {"class": "t_overall"})
            index = 0  # overall is first item in list returned by find_table()
        elif self._split == "conference":
            # link = team_soup.find("a", {"class": "t_conf"})
            index = 1  # conference is the second item in list returned by find_table()
        else:
            print("Invalid split:", self._split)
            sys.exit(1)

        # get the union of the BASE_URL and the link
        # url = sf.url_union(self.BASE_URL, sf.get_href(link))

        # get the soup of the page
        # pageSoup = sf.get_soup(url, verbose=self._verbose)

        # find index of hitting table
        tableNum1 = sf.find_table(team_soup, self.HITTING_COLS)[index]
        hitting = sf.scrape_table(team_soup, tableNum1 + 1, skip_rows=2)
        # find index of extended_hitting table
        tableNum2 = sf.find_table(team_soup, self.EXTENDED_HITTING_COLS)[index]
        extendedHitting = sf.scrape_table(team_soup, tableNum2 + 1, skip_rows=2)

        return pd.merge(hitting, extendedHitting, on=["No.", "Name", "Yr", "Pos", "g"])

    def _clean(self, data, team_id):
        # add TeamId, Season, convert '-' to 0, convert to int
        # column names cannot start with a digit in PostgreSQL!!!!!
        # disallowed column names: no., 2b, 3b, go/fo

        intCols = ["No.", "g", "ab", "r", "h", "2b", "3b", "hr", "rbi", "bb", "k",
                   "sb", "cs", "hbp", "sf", "sh", "tb", "xbh", "hdp", "go", "fo", "pa"]
        floatCols = ["avg", "obp", "slg", "go/fo"]
        newColNames = ["No", "Name", "Yr", "Pos", "G", "AB", "R", "H", "x2B", "x3B", "HR", "RBI", "BB", "SO", "SB", "CS",
                       "AVG", "OBP", "SLG", "HBP", "SF", "SH", "TB", "XBH", "GDP", "GO", "FO", "GO_FO", "PA"]

        finalColNames = ["No", "Name", "Team", "Season", "Yr", "Pos", "G", "PA", "AB", "R", "H", "x2B", "x3B", "HR", "RBI", "BB",
                         "SO", "SB", "CS", "AVG", "OBP", "SLG", "HBP", "SF", "SH", "TB", "XBH", "GDP", "GO", "FO",
                         "GO_FO"]

        # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>
        for col in intCols:
            data[col] = data[col].apply(sf.replace_dash, replacement=0)
            # data[col] = data[col].apply(to_int)
        for col in floatCols:
            data[col] = data[col].apply(sf.replace_dash, replacement=None)
            # data[col] = data[col].apply(to_float)

        # convert column names to a friendlier format
        data.columns = newColNames

        data["Team"] = team_id
        data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64
        data["Yr"] = data["Yr"].apply(sf.strip_dots)
        data["Pos"] = data["Pos"].apply(sf.to_none)

        # data = data.sort_values(ascending=False, by=["PA"])  # This doesn't work currently

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
    scraper = IndividualOffenseScraper(YEAR, SPLIT, OUTPUT, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()
