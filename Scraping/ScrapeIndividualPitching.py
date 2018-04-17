import pandas as pd
import psycopg2
import sys
import json
import ScrapeFunctions as sf

YEAR = "2016-17"
SPLIT = "conference"
OUTPUT = "csv"
# TODO: Add support for in-season scraping


class IndividualPitchingScraper:
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
    TABLES = {"overall": "raw_pitchers_overall", "conference": "raw_pitchers_conference"}

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
        print("Individual Pitching Scraper")
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
            df = self._clean(df, team['id'])
            # print(df)
            # print(df.info())

            self._data = pd.concat([self._data, df], ignore_index=True)
        self._runnable = False

    def _scrape(self, team_soup):
        if self._split == "overall":
            index = 0
            # find index of pitching table
            tableNum1 = sf.find_table(team_soup, self.PITCHING_COLS)[index]
            pitching = sf.scrape_table(team_soup, tableNum1 + 1, skip_rows=2)

            tags = team_soup.find_all('a', string="Coach's View")
            if len(tags) != 1:
                print("Can't find Coach's View")
                exit(1)
            url = tags[0].get('href')
            url = sf.url_union(self.BASE_URL, url)
            coach_soup = sf.get_soup(url, verbose=self._verbose)
            tableNum2 = sf.find_table(coach_soup, self.COACHES_VIEW_COLS)[0]
            coach_view = sf.scrape_table(coach_soup, tableNum2 + 1, first_row=3, skip_rows=3)

            coach_view['Player'] = coach_view['Player'].apply(sf.strip_dots)
            pitching['Name'] = [x.replace('  ', ' ') for x in pitching['Name']]
            coach_view = coach_view.rename(columns={'Player': 'Name'})

            # print(coach_view.info())
            # print(pitching.info())
            return pd.merge(coach_view, pitching, on=['No.', 'Name'])
        elif self._split == "conference":
            index = 1
            # find index of pitching table
            tableNum1 = sf.find_table(team_soup, self.PITCHING_COLS)[index]
            conference = sf.scrape_table(team_soup, tableNum1 + 1, skip_rows=2)

            # may want to normalize the column names eg, lower(), gp to g
            return conference
        else:
            print("Invalid split:", self._split)
            sys.exit(1)

    def _clean(self, data, team_id):
        if self._split == "overall":
            unnecessaryCols = ['app', 'gs', 'w', 'l', 'sv', 'cg', 'ip', 'h', 'r', 'er', 'bb', 'k', 'hr', 'era']
            intCols = ['No', 'Yr', 'G', 'GS', 'W', 'L', 'SV', 'CG', 'SHO', 'IP', 'H', 'R', 'ER', 'BB', 'SO',
                       'x2B', 'x3B', 'HR', 'AB', 'WP', 'HBP', 'BK', 'SF', 'SH']
            floatCols = ['ERA', 'AVG', 'SO_9']
            newColNames = ['No', 'Name', 'ERA', 'W', 'L', 'G', 'GS', 'CG', 'SHO', 'SV', 'IP', 'H', 'R', 'ER', 'BB', 'SO',
                           'x2B', 'x3B', 'HR', 'AB', 'AVG', 'WP', 'HBP', 'BK', 'SF', 'SH', 'Yr', 'Pos', 'SO_9']
            finalColNames = ['No', 'Name', 'Team', 'Season', 'Yr', 'Pos', 'G', 'GS', 'W', 'L', 'SV', 'CG', 'SHO', 'IP',
                             'H', 'R', 'ER', 'BB', 'SO', 'ERA', 'x2B', 'x3B', 'HR', 'AB', 'AVG', 'WP', 'HBP',
                             'BK', 'SF', 'SH', 'SO_9']

            # remove unnecessary columns
            data.drop(columns=unnecessaryCols, inplace=True)

            data.columns = newColNames

            # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>
            data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))  # replace '-' with '0'
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))  # replace '-' with None
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_inf(x, None))  # replace 'inf' with None

            data["Team"] = team_id
            data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64
            data["Yr"] = data["Yr"].apply(sf.strip_dots)
            data["Pos"] = data["Pos"].apply(sf.to_none)

            return data[finalColNames]
        elif self._split == "conference":
            renameCols = {'No.': 'No', 'app': 'g', 'k': 'so', 'k/9': 'so_9'}
            intCols = ['No', 'g', 'gs', 'w', 'l', 'sv', 'cg', 'h', 'r', 'er', 'bb', 'so', 'hr']
            floatCols = ['so_9', 'era']

            # rename columns
            data.rename(columns=renameCols, inplace=True)

            # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>
            data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))  # replace '-' with '0'
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))  # replace '-' with None
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_inf(x, None))  # replace 'inf' with None

            data["Team"] = team_id
            data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64
            data["Yr"] = data["Yr"].apply(sf.strip_dots)
            data["Pos"] = data["Pos"].apply(sf.to_none)

            finalColNames = data.axes[1].tolist()
            finalColNames.remove("Team")
            finalColNames.remove("Season")
            finalColNames.insert(2, "Team")
            finalColNames.insert(3, "Season")

            return data[finalColNames]
        else:
            print("Invalid split:", self._split)
            sys.exit(1)

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
    scraper = IndividualPitchingScraper(YEAR, SPLIT, OUTPUT, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()

