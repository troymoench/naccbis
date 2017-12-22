import pandas as pd
import psycopg2
import sys
import ScrapeFunctions as sf

YEAR = "2016-17"
OUTPUT = "csv"


class IndividualPitchingScraper:
    BASE_URL = "http://naccsports.org/sports/bsb/"  # add constants to ScrapeFunctions.py?
    PITCHING_COLS = ['No.', 'Name', 'yr', 'pos', 'app', 'gs', 'w', 'l', 'ip', 'h', 'r', 'er',
                    'era']
    COACHES_VIEW_COLS = ['No.', 'Player', 'ERA', 'W', 'L', 'APP', 'GS', 'IP', 'H', 'R', 'ER', '2B', '3B', 'HR', 'AB']
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
    TABLES = {"overall": "raw_pitchers_overall"}

    def __init__(self, year, output, verbose=False):
        self._year = year
        self._output = output
        self._verbose = verbose
        self._data = pd.DataFrame()
        self._runnable = True

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

    def _scrape(self):
        print("Scrape")

    def _clean(self):
        print("Clean")

    def export(self):
        print("Export")


# ***********************************
# ****** BEGINNING OF SCRIPT ********
# ***********************************
if __name__ == "__main__":
    scraper = IndividualPitchingScraper(YEAR, OUTPUT, verbose=True)
    scraper.info()
    scraper.run()
    # scraper.export()

