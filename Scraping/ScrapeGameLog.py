# Standard library imports
from datetime import date
import json
import logging
import sys
from urllib.parse import urljoin
# Third party imports
import pandas as pd
# Local imports
import ScrapeFunctions as sf
from ScrapeBase import BaseScraper
import Common.utils as utils

YEAR = "2017-18"
SPLIT = "hitting"  # hitting/pitching/fielding
OUTPUT = "sql"
INSEASON = True


class GameLogScraper(BaseScraper):

    """ This scraper is responsible for scraping game log stats. """

    HITTING_COLS = ['date', 'opponent', 'score', 'ab', 'r', 'h', '2b', '3b', 'hr', 'bb', 'k']
    EXTENDED_HITTING_COLS = ['date', 'opponent', 'score', 'hbp', 'sf', 'sh', 'tb', 'pa']
    PITCHING_COLS = ['date', 'opponent', 'score', 'w', 'l', 'ip', 'h', 'r', 'er', 'era']
    FIELDING_COLS = ['date', 'opponent', 'score', 'tc', 'po', 'a', 'e', 'fpct']
    TABLES = {"hitting": "raw_game_log_hitting", "pitching": "raw_game_log_pitching",
              "fielding": "raw_game_log_fielding"}

    def __init__(self, year, split, output, inseason=False, verbose=False):
        """ Class constructor
        :param year: The school year. A string.
        :param split: hitting, pitching, or fielding stats. A string.
        :param output: Output format. Currently csv and sql.
        :param inseason: Is this scraping taking place in season?
        :param verbose: Print extra information to standard out?
        """
        super().__init__(year, split, output, inseason, verbose)
        self._name = "Game Log Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

        # TODO: Add error handling
        with open('../config.json') as f:
            self._config = json.load(f)

    def run(self):
        # run the scraper
        # TODO: add argument export=True
        logging.info("%s", self._name)

        teamList = sf.get_team_list(self.BASE_URL, self._year, self.TEAM_IDS)
        logging.info("Found %d teams to scrape", len(teamList))

        # iterate over the teams
        for team in teamList:
            print("Fetching", team['team'])
            logging.info("Fetching %s", team['team'])

            teamSoup = sf.get_soup("{}{}/{}".format(self.BASE_URL, self._year, team['url']), verbose=self._verbose)
            logging.info("Looking for game log table")
            df = self._scrape(teamSoup)
            logging.info("Cleaning scraped data")
            df = self._clean(df, team['team'])

            self._data = pd.concat([self._data, df], ignore_index=True)
        self._runnable = False

    def _scrape(self, team_soup):
        # scrape game logs for hitting, pitching, fielding

        tags = team_soup.find_all('a', string="Game Log")
        if len(tags) != 1:
            print("Can't find Game Log")
            logging.error("Can't find Game Log")
            sys.exit(1)
        url = tags[0].get('href')
        url = urljoin(self.BASE_URL, url)

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
        data["Season"] = str(utils.year_to_season(self._year))  # converts to str for now, should be numpy.int64
        if self._inseason:
            data["ScrapeDate"] = str(date.today())
        data["GameNum"] = list(range(1, len(data) + 1))
        data["GameNum"] = data["GameNum"].apply(str)

        finalColNames = data.axes[1].tolist()
        finalColNames.remove("Season")
        finalColNames.remove("Name")
        if self._inseason:
            finalColNames.remove("ScrapeDate")

        finalColNames.insert(1, "Season")
        finalColNames.insert(2, "Name")
        if self._inseason:
            finalColNames.insert(0, "ScrapeDate")

        finalColNames.remove("GameNum")
        finalColNames.insert(0, "GameNum")
        return data[finalColNames]


# ***********************************
# ****** BEGINNING OF SCRIPT ********
# ***********************************
if __name__ == "__main__":
    scraper = GameLogScraper(YEAR, SPLIT, OUTPUT, INSEASON, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()
