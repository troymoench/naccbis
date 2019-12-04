# Standard library imports
from datetime import date
import logging
import sys
from urllib.parse import urljoin
# Third party imports
import pandas as pd
# Local imports
from . import ScrapeFunctions as sf
from .ScrapeBase import BaseScraper
import naccbis.Common.utils as utils


class GameLogScraper(BaseScraper):

    """ This scraper is responsible for scraping game log stats. """

    HITTING_COLS = ['date', 'opponent', 'score', 'ab', 'r', 'h', '2b', '3b', 'hr', 'bb', 'k']
    EXTENDED_HITTING_COLS = ['date', 'opponent', 'score', 'hbp', 'sf', 'sh', 'tb', 'pa']
    PITCHING_COLS = ['date', 'opponent', 'score', 'w', 'l', 'ip', 'h', 'r', 'er', 'era']
    FIELDING_COLS = ['date', 'opponent', 'score', 'tc', 'po', 'a', 'e', 'fpct']
    TABLES = {
        "hitting": "raw_game_log_hitting",
        "pitching": "raw_game_log_pitching",
        "fielding": "raw_game_log_fielding"
    }

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

    def run(self):
        """ Run the scraper """
        logging.info("%s", self._name)

        teamList = sf.get_team_list(self.BASE_URL, self._year, self.TEAM_IDS)
        logging.info("Found %d teams to scrape", len(teamList))

        # iterate over the teams
        for team in teamList:
            logging.info("Fetching %s", team['team'])

            url = "{}{}/{}".format(self.BASE_URL, self._year, team['url'])
            teamSoup = sf.get_soup(url)
            logging.info("Looking for game log table")
            df = self._scrape(teamSoup)
            logging.info("Cleaning scraped data")
            df = self._clean(df, team['team'])

            self._data = pd.concat([self._data, df], ignore_index=True)
        self._runnable = False

    def _scrape(self, team_soup):
        """ Scrape game logs for hitting, pitching, fielding """

        tags = team_soup.find_all('a', string="Game Log")
        if len(tags) != 1:
            print("Can't find Game Log")
            logging.error("Can't find Game Log")
            sys.exit(1)
        url = tags[0].get('href')
        url = urljoin(self.BASE_URL, url)

        game_soup = sf.get_soup(url)

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
            intCols = ['ab', 'r', 'h', 'x2b', 'x3b', 'hr', 'rbi', 'bb', 'so',
                       'sb', 'cs', 'hbp', 'sf', 'sh', 'tb', 'xbh', 'gdp',
                       'go', 'fo', 'pa']
            floatCols = ['go_fo']
            renameCols = {
                '2b': 'x2b',
                '3b': 'x3b',
                'k': 'so',
                'hdp': 'gdp',
                'go/fo': 'go_fo'
            }

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

        data.rename(columns=renameCols, inplace=True)

        data[intCols] = data[intCols].replace('-', '0')
        data[floatCols] = data[floatCols].replace('-', pd.np.nan)
        data[floatCols] = data[floatCols].replace('INF', pd.np.nan)

        # replace tabs
        data["Opponent"] = [x.replace('\t', '') for x in data["Opponent"]]
        # strip excessive whitespace
        data["Opponent"] = [' '.join(x.split()) for x in data["Opponent"]]

        # replace strange # in Date column (Maranatha 2012)
        data["Date"] = [x.replace("#", "").strip() for x in data["Date"]]

        data["Name"] = team
        data["Season"] = str(utils.year_to_season(self._year))
        if self._inseason:
            data["scrape_date"] = str(date.today())

        # filter out cancelled games that don't have a result
        data = data[data["Score"] != '']
        data["game_num"] = list(range(1, len(data) + 1))
        data["game_num"] = data["game_num"].apply(str)

        finalColNames = data.axes[1].tolist()
        finalColNames.remove("Season")
        finalColNames.remove("Name")
        if self._inseason:
            finalColNames.remove("scrape_date")

        finalColNames.insert(1, "Season")
        finalColNames.insert(2, "Name")
        if self._inseason:
            finalColNames.insert(0, "scrape_date")

        finalColNames.remove("game_num")
        finalColNames.insert(0, "game_num")
        data = data[finalColNames]
        data.columns = data.columns.to_series().str.lower()
        return data


if __name__ == "__main__":
    YEAR = "2017-18"
    SPLIT = "hitting"  # hitting/pitching/fielding
    OUTPUT = "sql"
    INSEASON = True
    scraper = GameLogScraper(YEAR, SPLIT, OUTPUT, INSEASON, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()
