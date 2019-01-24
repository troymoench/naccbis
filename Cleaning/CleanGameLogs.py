""" This script is used to clean game log data and load into the database """
# Standard library imports
import argparse
import datetime
import os
import re
# Third party imports
import pandas as pd
# Local imports
import Common.utils as utils


class GameLogETL:
    """ ETL class for game logs """
    CONFERENCE_TEAMS = ["Aurora", "Benedictine", "Concordia Chicago", "Concordia Wisconsin",
                        "Dominican", "Edgewood", "Lakeland", "MSOE", "Marian", "Maranatha",
                        "Rockford", "Wisconsin Lutheran"]
    CSV_DIR = "csv/"

    def __init__(self, year, load_db, conn):
        self.year = year
        self.load_db = load_db
        self.conn = conn

    def extract(self):
        self.data = pd.read_sql_table("raw_game_log_hitting", self.conn)
        if self.year:
            self.data = self.data[self.data["season"] == self.year]

    def transform(self):
        self.data = self.data[["game_num", "date", "season", "name", "opponent", "score"]]
        self.data["result"] = self.data["score"].apply(self.extract_result)
        # runs scored, runs against

        self.data["inter"] = self.data["score"].apply(self.extract_runs)  # intermediate column
        self.data["rs"] = [x[0] for x in self.data["inter"]]
        self.data["ra"] = [x[1] for x in self.data["inter"]]

        self.data.drop(columns=["inter"], inplace=True)

        # home/away

        self.data["home"] = self.data["opponent"].apply(self.extract_home)

        # conference/non-conference

        self.data["conference"] = list(map(lambda x, y: self.extract_conference(x, y, self.CONFERENCE_TEAMS),
                                           self.data["opponent"], self.data["season"]))
        self.data["opponent"] = self.data["opponent"].apply(self.extract_opponent)
        self.data.rename(columns={"name": "team"}, inplace=True)
        self.data.drop(columns=["score"], inplace=True)

        self.data["date"] = list(map(lambda x, y: self.extract_date(x, y),
                                     self.data["date"], self.data["season"]))

    def load(self):
        if self.load_db:
            print("Loading data into database")
            utils.db_load_data(self.data, "game_log", self.conn, if_exists="append", index=False)
        else:
            print("Dumping to csv")
            self.data.to_csv(os.path.join(self.CSV_DIR, "game_log.csv"), index=False)

    def run(self):
        self.extract()
        self.transform()
        self.load()

    @staticmethod
    def extract_runs(score):
        """ Extract the runs scored and runs against from the score
        :param score: The score
        :returns: A list where first element is runs scored and
         second element is runs against. Format: [rs, ra]
        """
        split_score = score.split(',')
        result = split_score[0].strip()
        run_list = split_score[1].split('-')
        run_list = list(map(lambda x: int(x.strip()), run_list))

        if result == 'W':
            run_list.sort(reverse=True)
        else:
            run_list.sort()
        return run_list

    @staticmethod
    def extract_result(score):
        """ Extract the result (W/L) from the score
        :param score: The score
        :returns: The result (W/L)
        """
        return score.split(',')[0].strip()

    @staticmethod
    def extract_home(opponent):
        """ Extract home/away from the opponent
        :param opponent: The opponent
        :returns: True for home, False for away
        """
        opponent = opponent.strip()
        if re.match(r"\b[Aa][Tt]\b", opponent):
            home = False
        else:
            home = True
        return home

    @staticmethod
    def extract_opponent(opponent):
        """ Extract the team name from the raw opponent
        :param opponent: The opponent
        :returns: The team name of the opponent
        """
        opponent = opponent.strip()
        return re.sub(r"\b[Aa][Tt]\b|\b[Vv][Ss][.]*", "", opponent).strip()

    @staticmethod
    def extract_conference(opponent, season, teams):
        """ Determine if the opponent is conference or non-conference """
        # TODO: Get list of conference teams from database

        # Maranatha is non-conference after 2013
        if opponent == "Maranatha" and season > 2013:
            return False

        matched = False
        for team in teams:
            if re.search(team, opponent):
                matched = True
        return matched

    @staticmethod
    def extract_date(date_str, season):
        date_str = "{} {}".format(date_str, season)
        return datetime.datetime.strptime(date_str, "%b %d %Y")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract, Transform, Load Game Log data")
    parser.add_argument("--year", type=int, default=None, help="Filter by year")
    parser.add_argument("--load", action="store_true",
                        help="Load data into database")
    args = parser.parse_args()

    config = utils.init_config()
    utils.init_logging(config["LOGGING"])
    conn = utils.connect_db(config["DB"])
    game_log = GameLogETL(args.year, args.load, conn)
    game_log.run()
    conn.close()
