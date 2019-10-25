""" This module provides the IndividualPitchingScraper class """
# Standard library imports
from datetime import date
import sys
import logging
from urllib.parse import urljoin
# Third party imports
import pandas as pd
# Local imports
import naccbis.Scraping.ScrapeFunctions as sf
from naccbis.Scraping.ScrapeBase import BaseScraper
import naccbis.Common.utils as utils


class IndividualPitchingScraper(BaseScraper):

    """ This scraper is responsible for scraping individual pitching stats. """

    PITCHING_COLS = ['no.', 'name', 'yr', 'pos', 'app', 'gs', 'w', 'l', 'ip', 'h',
                     'r', 'er', 'era']
    COACHES_VIEW_COLS = ['no.', 'player', 'era', 'w', 'l', 'app', 'gs', 'ip', 'h',
                         'r', 'er', '2b', '3b', 'hr', 'ab']
    TABLES = {"overall": "raw_pitchers_overall", "conference": "raw_pitchers_conference"}

    def __init__(self, year, split, output, inseason=False, verbose=False):
        """ Class constructor
        :param year: The school year. A string.
        :param split: overall or conference stats. A string.
        :param output: Output format. Currently csv and sql.
        :param inseason: Is this scraping taking place in season?
        :param verbose: Print extra information to standard out?
        """
        super().__init__(year, split, output, inseason, verbose)
        self._name = "Individual Pitching Scraper"
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
            teamSoup = sf.get_soup(url, verbose=self._verbose)
            if sf.skip_team(teamSoup):
                continue
            logging.info("Looking for pitching tables")
            df = self._scrape(teamSoup)
            logging.info("Cleaning scraped data")
            df = self._clean(df, team['id'])

            self._data = pd.concat([self._data, df], ignore_index=True)
        self._runnable = False

    def _scrape(self, team_soup):
        # more stats are available on coach's view
        # but coach's view doesn't provide conference stats

        if self._split == "overall":
            index = 0
            # find index of pitching table
            tableNum1 = sf.find_table(team_soup, self.PITCHING_COLS)[index]
            pitching = sf.scrape_table(team_soup, tableNum1 + 1, skip_rows=2)

            tags = team_soup.find_all('a', string="Coach's View")
            if len(tags) != 1:
                print("Can't find Coach's View")
                sys.exit(1)
            url = tags[0].get('href')
            url = urljoin(self.BASE_URL, url)
            coach_soup = sf.get_soup(url, verbose=self._verbose)
            tableNum2 = sf.find_table(coach_soup, self.COACHES_VIEW_COLS)[0]
            coach_view = sf.scrape_table(coach_soup, tableNum2 + 1, first_row=3, skip_rows=3)

            coach_view['Player'] = coach_view['Player'].apply(sf.strip_dots)
            pitching['Name'] = [x.replace('  ', ' ') for x in pitching['Name']]
            coach_view = coach_view.rename(columns={'Player': 'Name'})
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
            unnecessaryCols = ['app', 'gs', 'w', 'l', 'sv', 'cg', 'ip', 'h', 'r',
                               'er', 'bb', 'k', 'hr', 'era']
            intCols = ['No', 'Yr', 'G', 'GS', 'W', 'L', 'SV', 'CG', 'SHO', 'IP',
                       'H', 'R', 'ER', 'BB', 'SO', 'x2B', 'x3B', 'HR', 'AB',
                       'WP', 'HBP', 'BK', 'SF', 'SH']
            floatCols = ['ERA', 'AVG', 'SO_9']
            newColNames = ['No', 'Name', 'ERA', 'W', 'L', 'G', 'GS', 'CG',
                           'SHO', 'SV', 'IP', 'H', 'R', 'ER', 'BB', 'SO',
                           'x2B', 'x3B', 'HR', 'AB', 'AVG', 'WP', 'HBP', 'BK',
                           'SF', 'SH', 'Yr', 'Pos', 'SO_9']
            finalColNames = ['No', 'Name', 'Team', 'Season', 'Yr', 'Pos', 'G',
                             'GS', 'W', 'L', 'SV', 'CG', 'SHO', 'IP', 'H', 'R',
                             'ER', 'BB', 'SO', 'ERA', 'x2B', 'x3B', 'HR', 'AB',
                             'AVG', 'WP', 'HBP', 'BK', 'SF', 'SH', 'SO_9']
            if self._inseason:
                finalColNames = ['No', 'Name', 'Team', 'Season', 'Date', 'Yr',
                                 'Pos', 'G', 'GS', 'W', 'L', 'SV', 'CG', 'SHO',
                                 'IP', 'H', 'R', 'ER', 'BB', 'SO', 'ERA', 'x2B',
                                 'x3B', 'HR', 'AB', 'AVG', 'WP',
                                 'HBP', 'BK', 'SF', 'SH', 'SO_9']

            data.drop(columns=unnecessaryCols, inplace=True)

            data.columns = newColNames

            data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_inf(x, None))

            data["Team"] = team_id
            data["Season"] = str(utils.year_to_season(self._year))
            if self._inseason:
                data["Date"] = str(date.today())
            data["Yr"] = data["Yr"].apply(sf.strip_dots)
            data["Pos"] = data["Pos"].apply(sf.to_none)

            data = data[finalColNames]
            data.columns = data.columns.to_series().str.lower()
            return data
        elif self._split == "conference":
            renameCols = {'No.': 'No', 'app': 'g', 'k': 'so', 'k/9': 'so_9'}
            intCols = ['No', 'g', 'gs', 'w', 'l', 'sv', 'cg', 'h', 'r', 'er', 'bb', 'so', 'hr']
            floatCols = ['so_9', 'era']
            finalColNames = ['No', 'Name', 'Team', 'Season', 'Yr', 'Pos', 'g',
                             'gs', 'w', 'l', 'sv', 'cg', 'ip', 'h',
                             'r', 'er', 'bb', 'so', 'so_9', 'hr', 'era']

            if self._inseason:
                finalColNames = ['No', 'Name', 'Team', 'Season', 'Date', 'Yr',
                                 'Pos', 'g', 'gs', 'w', 'l', 'sv', 'cg', 'ip',
                                 'h', 'r', 'er', 'bb', 'so', 'so_9', 'hr', 'era']
            data.rename(columns=renameCols, inplace=True)

            data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_inf(x, None))

            data["Team"] = team_id
            data["Season"] = str(utils.year_to_season(self._year))
            if self._inseason:
                data["Date"] = str(date.today())
            data["Yr"] = data["Yr"].apply(sf.strip_dots)
            data["Pos"] = data["Pos"].apply(sf.to_none)

            data = data[finalColNames]
            data.columns = data.columns.to_series().str.lower()
            return data
        else:
            print("Invalid split:", self._split)
            sys.exit(1)


if __name__ == "__main__":
    YEAR = "2017-18"
    SPLIT = "overall"
    OUTPUT = "sql"
    INSEASON = True
    scraper = IndividualPitchingScraper(YEAR, SPLIT, OUTPUT, INSEASON, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()