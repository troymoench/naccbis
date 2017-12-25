import pandas as pd
import psycopg2
import sys
import json
import ScrapeFunctions as sf

YEAR = "2016-17"
OUTPUT = "csv"
# TODO: Add support for in-season scraping
# TODO: Add support for conference stats


class TeamPitchingScraper:
    BASE_URL = "http://naccsports.org/sports/bsb/"  # add constants to ScrapeFunctions.py?
    PITCHING_COLS = ['no.', 'name', 'yr', 'pos', 'app', 'gs', 'w', 'l', 'ip', 'h', 'r', 'er',
                    'era']
    COACHES_VIEW_COLS = ['no.', 'player', 'era', 'w', 'l', 'app', 'gs', 'ip', 'h', 'r', 'er', '2b', '3b', 'hr', 'ab']
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
    TABLES = {"overall": "raw_team_pitching_overall", "conference": "raw_team_pitching_conference"}

    def __init__(self, year, output, verbose=False):
        self._year = year
        self._output = output
        self._verbose = verbose
        self._data = pd.DataFrame()
        self._runnable = True

        # TODO: Add error handling
        with open('config.json') as f:
            self._config = json.load(f)

    def info(self):
        print("Team Pitching Scraper")
        print("Year:", self._year)
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

            teamSoup = sf.get_soup("{}{}/{}".format(self.BASE_URL, self._year, team['url']), verbose=self._verbose)

            df = self._scrape(teamSoup)
            # print(df.info())
            df = self._clean(df, team['team'])

            self._data = pd.concat([self._data, df], ignore_index=True)
            # exit(0)
        self._runnable = False

    def _scrape(self, team_soup):
        # find index of pitching table
        tableNum1 = sf.find_table(team_soup, self.PITCHING_COLS)[0]
        pitching = sf.scrape_table(team_soup, tableNum1 + 1, skip_rows=1)
        # select the totals row
        pitching = pitching[(pitching.Name == "Totals") | (pitching.Name == "Total")]
        pitching = pitching.reset_index(drop=True)
        # make sure that only one row remains
        # print(pitching.shape[0])

        # make sure that the name is Totals
        if pitching["Name"][0] != "Totals":
            pitching["Name"][0] = "Totals"

        tags = team_soup.find_all('a', string="Coach's View")
        if len(tags) != 1:
            print("Can't find Coach's View")
            exit(1)
        url = tags[0].get('href')
        url = sf.url_union(self.BASE_URL, url)
        coach_soup = sf.get_soup(url, verbose=self._verbose)
        tableNum2 = sf.find_table(coach_soup, self.COACHES_VIEW_COLS)[0]
        coach_view = sf.scrape_table(coach_soup, tableNum2 + 1, first_row=3, skip_rows=1)

        if 'Player' in coach_view.columns:
            coach_view = coach_view.rename(columns={'Player': 'Name'})

        coach_view["Name"] = coach_view["Name"].apply(sf.strip_dots)

        coach_view = coach_view[(coach_view.Name == "Totals") | (coach_view.Name == "Total")]
        coach_view = coach_view.reset_index(drop=True)

        # make sure that the name is Totals
        if coach_view["Name"][0] != "Totals":
            coach_view["Name"][0] = "Totals"

        return pd.merge(coach_view, pitching, on=['No.', 'Name'])

    def _clean(self, data, team):
        unnecessaryCols = ['No.', 'Name', 'Pos', 'Yr', 'app', 'gs', 'GS', 'w', 'l', 'sv', 'cg', 'ip', 'h', 'r', 'er', 'bb', 'k', 'hr', 'era']
        intCols = ['G', 'W', 'L', 'SV', 'CG', 'SHO', 'IP', 'H', 'R', 'ER', 'BB', 'SO',
                   'x2B', 'x3B', 'HR', 'AB', 'WP', 'HBP', 'BK', 'SF', 'SH']
        floatCols = ['ERA', 'AVG', 'SO_9']
        newColNames = ['ERA', 'W', 'L', 'G', 'CG', 'SHO', 'SV', 'IP', 'H', 'R', 'ER', 'BB', 'SO',
                       'x2B', 'x3B', 'HR', 'AB', 'AVG', 'WP', 'HBP', 'BK', 'SF', 'SH', 'SO_9']
        finalColNames = ['Name', 'Season', 'G', 'W', 'L', 'SV', 'CG', 'SHO', 'IP',
                         'H', 'R', 'ER', 'BB', 'SO', 'ERA', 'x2B', 'x3B', 'HR', 'AB', 'AVG', 'WP', 'HBP',
                         'BK', 'SF', 'SH', 'SO_9']

        # remove unnecessary columns
        data = data.drop(columns=unnecessaryCols)

        data.columns = newColNames
        # print(data.info())
        # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>
        for col in intCols:
            data[col] = data[col].apply(sf.replace_dash, replacement=0)
        for col in floatCols:
            data[col] = data[col].apply(sf.replace_dash, replacement=None)
            data[col] = data[col].apply(sf.replace_inf, replacement=None)

        data["Name"] = team
        data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64

        return data[finalColNames]

    def export(self):
        print("Export")
        print(self._data.info())
        # export scraped and cleaned data to csv or database
        if self._runnable:
            print("Cannot export. Scraper has not been run yet. Use run() to do so.")
            sys.exit(1)
        else:
            tableName = self.TABLES['overall']

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
    scraper = TeamPitchingScraper(YEAR, OUTPUT, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()

