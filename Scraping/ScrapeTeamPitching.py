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


class TeamPitchingScraper(BaseScraper):
    PITCHING_COLS = ['no.', 'name', 'yr', 'pos', 'app', 'gs', 'w', 'l', 'ip', 'h', 'r', 'er', 'era']
    COACHES_VIEW_COLS = ['no.', 'player', 'era', 'w', 'l', 'app', 'gs', 'ip', 'h', 'r', 'er', '2b', '3b', 'hr', 'ab']
    CONFERENCE_COLS = ['name', 'gp', 'ip', 'h', 'r', 'er', 'bb', 'k', 'era']
    TABLES = {"overall": "raw_team_pitching_overall", "conference": "raw_team_pitching_conference"}

    def __init__(self, year, split, output, inseason=False, verbose=False):
        super().__init__(year, split, output, inseason, verbose)
        self._name = "Team Pitching Scraper"
        self._data = pd.DataFrame()
        self._runnable = True

        # TODO: Add error handling
        with open('../config.json') as f:
            self._config = json.load(f)

    def run(self):
        # run the scraper
        # TODO: add argument export=True

        if self._split == "overall":
            teamList = sf.get_team_list(self.BASE_URL, self._year, self.TEAM_IDS)

            # iterate over the teams
            for team in teamList:
                print("Fetching", team['team'])

                teamSoup = sf.get_soup("{}{}/{}".format(self.BASE_URL, self._year, team['url']), verbose=self._verbose)

                df = self._scrape(teamSoup)
                df = self._clean(df, team['team'])

                self._data = pd.concat([self._data, df], ignore_index=True)
        elif self._split == "conference":
            soup = sf.get_soup(self.BASE_URL + self._year + "/teams", verbose=self._verbose)
            df = self._scrape(soup)
            self._data = self._clean(df, None)

        else:
            print("Invalid split:", self._split)
            sys.exit(1)

        self._runnable = False

    def _scrape(self, team_soup):
        # more stats are available on coach's view
        # but coach's view doesn't provide conference stats

        if self._split == "overall":
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
        elif self._split == "conference":
            index = 1

            # find index of fielding table
            tableNum1 = sf.find_table(team_soup, self.CONFERENCE_COLS)[index]
            conference = sf.scrape_table(team_soup, tableNum1 + 1, skip_rows=0)

            # may want to normalize the column names eg, lower(), gp to g
            return conference
        else:
            print("Invalid split:", self._split)
            sys.exit(1)

    def _clean(self, data, team):
        if self._split == "overall":
            unnecessaryCols = ['No.', 'Name', 'Pos', 'Yr', 'app', 'gs', 'GS', 'w', 'l', 'sv', 'cg', 'ip', 'h', 'r', 'er', 'bb', 'k', 'hr', 'era']
            intCols = ['G', 'W', 'L', 'SV', 'CG', 'SHO', 'IP', 'H', 'R', 'ER', 'BB', 'SO',
                       'x2B', 'x3B', 'HR', 'AB', 'WP', 'HBP', 'BK', 'SF', 'SH']
            floatCols = ['ERA', 'AVG', 'SO_9']
            renameCols = {'APP': 'G', '2B': 'x2B', '3B': 'x3B', 'B/AVG': 'AVG', 'SFA': 'SF', 'SHA': 'SH', 'k/9': 'SO_9'}
            finalColNames = ['Name', 'Season', 'G', 'W', 'L', 'SV', 'CG', 'SHO', 'IP',
                             'H', 'R', 'ER', 'BB', 'SO', 'ERA', 'x2B', 'x3B', 'HR', 'AB', 'AVG', 'WP', 'HBP',
                             'BK', 'SF', 'SH', 'SO_9']
            if self._inseason:
                finalColNames = ['Name', 'Season', 'Date', 'G', 'W', 'L', 'SV', 'CG', 'SHO', 'IP',
                                 'H', 'R', 'ER', 'BB', 'SO', 'ERA', 'x2B', 'x3B', 'HR', 'AB', 'AVG', 'WP', 'HBP',
                                 'BK', 'SF', 'SH', 'SO_9']

            # remove unnecessary columns
            data.drop(columns=unnecessaryCols, inplace=True)

            # rename columns
            data.rename(columns=renameCols, inplace=True)
            # print(data.info())

            # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>
            data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))  # replace '-' with '0'
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))  # replace '-' with None
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_inf(x, None))  # replace 'inf' with None

            data["Name"] = team
            data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64
            if self._inseason:
                data["Date"] = str(date.today())
            return data[finalColNames]
        elif self._split == "conference":
            unnecessaryCols = ['Rk']
            renameCols = {'gp': 'g', 'k': 'so', 'k/9': 'so_9'}
            intCols = ['g', 'h', 'r', 'er', 'bb', 'so', 'hr']
            floatCols = ['so_9', 'era']
            finalColNames = ['Name', 'Season', 'g', 'ip', 'h', 'r', 'er', 'bb', 'so', 'so_9', 'hr', 'era']
            if self._inseason:
                finalColNames = ['Name', 'Season', 'Date', 'g', 'ip', 'h', 'r', 'er', 'bb', 'so', 'so_9', 'hr', 'era']

            # remove unnecessary columns
            data = data.drop(columns=unnecessaryCols)

            # rename columns
            data = data.rename(columns=renameCols)

            # TODO: clean() should convert to <class 'numpy.int64'> and <class 'numpy.float'>
            data[intCols] = data[intCols].applymap(lambda x: sf.replace_dash(x, '0'))  # replace '-' with '0'
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_dash(x, None))  # replace '-' with None
            data[floatCols] = data[floatCols].applymap(lambda x: sf.replace_inf(x, None))  # replace 'inf' with None

            data["Season"] = str(sf.year_to_season(self._year))  # converts to str for now, should be numpy.int64
            if self._inseason:
                data["Date"] = str(date.today())

            return data[finalColNames]
        else:
            print("Invalid split:", self._split)
            sys.exit(1)


# ***********************************
# ****** BEGINNING OF SCRIPT ********
# ***********************************
if __name__ == "__main__":
    scraper = TeamPitchingScraper(YEAR, SPLIT, OUTPUT, INSEASON, verbose=True)
    scraper.info()
    scraper.run()
    scraper.export()

