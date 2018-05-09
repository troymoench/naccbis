import pandas as pd
import psycopg2
import sys
import json
from datetime import date
import ScrapeFunctions as sf
from ScrapeBase import BaseScraper

YEAR = "2017-18"
SPLIT = "hitting"  # hitting/pitching/fielding
OUTPUT = "sql"
INSEASON = True

# TODO: Add game number column to prevent double inserts for inseason


class GameLogScraper(BaseScraper):
    HITTING_COLS = ['date', 'opponent', 'score', 'ab', 'r', 'h', '2b', '3b', 'hr', 'bb', 'k']
    EXTENDED_HITTING_COLS = ['date', 'opponent', 'score', 'hbp', 'sf', 'sh', 'tb', 'pa']
    PITCHING_COLS = ['date', 'opponent', 'score', 'w', 'l', 'ip', 'h', 'r', 'er', 'era']
    FIELDING_COLS = ['date', 'opponent', 'score', 'tc', 'po', 'a', 'e', 'fpct']
    TABLES = {"hitting": "raw_game_log_hitting", "pitching": "raw_game_log_pitching",
              "fielding": "raw_game_log_fielding"}

    def __init__(self, year, split, output, inseason=False, verbose=False):
        super().__init__(year, split, output, inseason, verbose)
        self._name = "Game Log Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

        # TODO: Add error handling
        with open('../config.json') as f:
            self._config = json.load(f)
    #
    # def info(self):
    #     print("\n----------------")
    #     print("Game Log Scraper")
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
    #     print("----------------")

    def run(self):
        # run the scraper
        # TODO: add argument export=True

        teamList = sf.get_team_list(self.BASE_URL, self._year, self.TEAM_IDS)

        # iterate over the teams
        for team in teamList:
            print("Fetching", team['team'])

            teamSoup = sf.get_soup("{}{}/{}".format(self.BASE_URL, self._year, team['url']), verbose=self._verbose)
            df = self._scrape(teamSoup)
            df = self._clean(df, team['team'])

            self._data = pd.concat([self._data, df], ignore_index=True)
        self._runnable = False

    def _scrape(self, team_soup):
        # scrape game logs for hitting, pitching, fielding

        tags = team_soup.find_all('a', string="Game Log")
        if len(tags) != 1:
            print("Can't find Game Log")
            exit(1)
        url = tags[0].get('href')
        url = sf.url_union(self.BASE_URL, url)

        game_soup = sf.get_soup(url, verbose=self._verbose)

        if self._split == "hitting":
            tableNum1 = sf.find_table(game_soup, self.HITTING_COLS)[0]
            hitting = sf.scrape_table(game_soup, tableNum1 + 1, first_row=2, skip_rows=0)

            tableNum2 = sf.find_table(game_soup, self.EXTENDED_HITTING_COLS)[0]
            extendedHitting = sf.scrape_table(game_soup, tableNum2 + 1, first_row=2, skip_rows=0)

            # may want to normalize the column names before merging, eg, lower()
            return pd.merge(hitting, extendedHitting, on=["Date", "Opponent", "Score"])

        elif self._split == "pitching":
            tableNum1 = sf.find_table(game_soup, self.PITCHING_COLS)[0]
            pitching = sf.scrape_table(game_soup, tableNum1 + 1, first_row=2, skip_rows=0)

            return pitching
        elif self._split == "fielding":
            tableNum1 = sf.find_table(game_soup, self.FIELDING_COLS)[0]
            fielding = sf.scrape_table(game_soup, tableNum1 + 1, first_row=2, skip_rows=0)

            return fielding
        else:
            print("Invalid split:", self._split)
            sys.exit(1)

    def _clean(self, data, team):
        if self._split == "hitting":
            intCols = ['ab', 'r', 'h', 'x2b', 'x3b', 'hr', 'rbi', 'bb', 'so', 'sb', 'cs', 'hbp', 'sf', 'sh', 'tb',
                       'xbh', 'gdp', 'go', 'fo', 'pa']
            floatCols = ['go_fo']
            renameCols = {'2b': 'x2b', '3b': 'x3b', 'k': 'so', 'hdp': 'gdp', 'go/fo': 'go_fo'}

        elif self._split == "pitching":
            intCols = ['w', 'l', 'sv', 'h', 'r', 'er', 'bb', 'so', 'hr']
            floatCols = ['era']
            renameCols = {'k': 'so'}

        elif self._split == "fielding":
            intCols = ['tc', 'po', 'a', 'e', 'dp', 'sba', 'cs', 'pb', 'ci']
            floatCols = ['fpct', 'cspct']
            renameCols = {'rcs': 'cs', 'rcs%': 'cspct'}

        else:
            print("Invalid split:", self._split)
            sys.exit(1)

        # rename columns
        data.rename(columns=renameCols, inplace=True)

        # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>
        data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))  # replace '-' with '0'
        data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))  # replace '-' with None
        data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_inf(x, None))  # replace 'inf' with None

        # replace tabs
        data["Opponent"] = [x.replace('\t', '') for x in data["Opponent"]]
        # strip excessive whitespace
        data["Opponent"] = [' '.join(x.split()) for x in data["Opponent"]]

        # replace strange # in Date column (Maranatha 2012)
        data["Date"] = [x.replace("#", "").strip() for x in data["Date"]]

        data["Name"] = team
        data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64
        if self._inseason:
            data["ScrapeDate"] = str(date.today())

        finalColNames = data.axes[1].tolist()
        finalColNames.remove("Season")
        finalColNames.remove("Name")
        if self._inseason:
            finalColNames.remove("ScrapeDate")

        finalColNames.insert(1, "Season")
        finalColNames.insert(2, "Name")
        if self._inseason:
            finalColNames.insert(0, "ScrapeDate")

        return data[finalColNames]

    # def export(self):
    #     # export scraped and cleaned data to csv or database
    #     if self._runnable:
    #         print("Cannot export. Scraper has not been run yet. Use run() to do so.")
    #         sys.exit(1)
    #     else:
    #         tableName = self.TABLES[self._split]
    #
    #         if self._output == "csv":
    #             if self._inseason:
    #                 self._data.to_csv(
    #                     "{}{}{}.csv".format(self._config["csv_path"], tableName, str(date.today())),
    #                     index=False)
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
    # def get_date(self):
    #     return self._data


# ***********************************
# ****** BEGINNING OF SCRIPT ********
# ***********************************
if __name__ == "__main__":
    scraper = GameLogScraper(YEAR, SPLIT, OUTPUT, INSEASON, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()

